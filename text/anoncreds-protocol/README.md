- Name: Anonymous Credential Protocol
- Author: Mike Lodder and Brent Zundel
- Start Date: January 25, 2019
- PR:
- Jira Issue:

# Summary
[summary]: #summary

Anonymous credentials form the heart of Indy's identity capabilities.
This document describes the protocol for Camenisch-Lysyanskaya signatures and the anonymous
credentials they enable.

# Motivation
[motivation]: #motivation

This HIPE is intended as a publication of the protocol behind the code that has already been implemented in
[indy-crypto](https://github.com/hyperledger/indy-crypto/tree/master/libindy-crypto/src/cl).

# Tutorial
[tutorial]: #tutorial

## Introduction
[intro]: #intro
### Concept

The concept of *anonymous credentials* allows users to prove that their identity satisfies certain properties in an uncorrelated way without revealing other identity details.  The properties can be raw identity attributes  such as
the birth date or the address, or more sophisticated predicates such as ``A is older than 20 years old''.

We assume three parties: *issuer*, *holder*, and *verifier*. From the functional perspective, the issuer gives a credential *C* based on identity schema *X*, which asserts certain properties 𝒫 about *X*, to the holder. The credential consists of attributes represented by integers *m<sub>1</sub>, m<sub>2</sub>,..., m<sub>l</sub>*. The holder then presents (𝒫,*C*) to the Verifier, which can verify that the issuer has asserted that holder's identity has property 𝒫.

### Properties

Credentials are *unforgeable* in the sense that no one can fool the Verifier with a credential not prepared by the issuer.

We say that credentials are  *unlinkable* if it is impossible to correlate the presented credential across multiple presentations. This is implemented by the holder *proving* with a zero-knowledge proof *that he has a credential* rather than showing the credential.

Unlinkability can be simulated by the issuer generating a sufficient number of ordinary unrelated credentials. Also unlinkability can be turned off to make credentials *one-time use* so that second and later presentations are detected.


### Pseudonyms
Typically a credential is bound to a certain pseudonym *nym*. It is supposed that holder has been registered as *nym* at the issuer, and communicated (part of) his identity *X* to him. After  that the issuer can issue a credential that couples *nym* and *X*.


The holder may have a pseudonym at the Verifier, but not necessarily. If there is no pseudonym then the Verifier provides the service to users who did not register. If the pseudonym *nym*<sub>V</sub> is required, it can be generated from a link secret *m<sub>1</sub>* together with *nym* in a way that *nym* can not be linked to *nym<sub>V</sub>*. However, holder is supposed to prove that the credential presented was issued to a pseudonym derived from the same link secret as used to produce *nym<sub>V</sub>*.

An identity owner also can create a policy address **_I_** that is used for managing agent proving authorization. The address are tied to credentials issued to holders such that agents cannot use these credentials without authorization.

## Generic notation

Attribute *m* is a *l<sub>a</sub>*-bit unsigned integer. Technically it is possible to support credentials with different *l<sub>a</sub>*, but in Sovrin for simplicity it is set *l<sub>a</sub>*=256.


## Protocol Overview

The described protocol supports anonymous credentials given to multiple holders  by various issuers, which are presented to various relying parties.

Various types of anonymous credentials can be supported. In this section, the combination of [CL-based credentials](https://groups.csail.mit.edu/cis/pubs/lysyanskaya/cl02b.pdf) and [pairing-based revocation](https://eprint.iacr.org/2008/539.pdf) is described.

The simplest credential lifecycle with one credential, single issuer, holder, and verifier is as follows:
1. Issuer determines a credential schema 𝒮: the type of cryptographic signatures used to sign the credentials, the number *l* of attributes in a credential, the indices *A<sub>h</sub> ⊂ {1,2,...,l}* of hidden attributes, the public key *P<sub>k</sub>*, the non-revocation credential attribute number *l<sub>r</sub>* and non-revocation public key *P<sub>r</sub>* (Section~\ref{sec:iss-setup}). Then he publishes it on the ledger and announces the attribute semantics.
1. Holder retrieves the credential schema from the ledger and sets the hidden attributes.
1. Holder requests a credential from issuer. He sends hidden attributes in a blinded form to issuer and agrees on the values of known attributes *A<sub>k</sub> = {1,2,...,l} \ A<sub>h</sub>*.
1. Issuer returns a credential pair *(C<sub>p</sub>, C<sub>NR</sub>)* to holder. The first credential contains the requested *l* attributes. The second credential asserts the non-revocation status of the first one. Issuer publishes the non-revoked status of the credential on the ledger.
1. Holder approaches verifier. Verifier sends the Proof Request ℰ
    to holder. The Proof Request contains the credential schema *𝒮<sub>E</sub>* and disclosure predicates 𝒟. The predicates for attribute *m* and value *V* can be of form *m=V*, *m<V*, or *m>V*. Some attributes may be asserted to be the same: *m<sub>i</sub>=m<sub>j</sub>*.
1. Holder checks that the credential pair he holds satisfy the schema *𝒮<sub>E</sub>*.
    He retrieves the non-revocation witness from the ledger.
1. Holder creates a proof *P* that he has a non-revoked credential satisfying the proof request ℰ and sends it to verifier.
1. Verifier verifies the proof.


If there are multiple issuers, the holder obtains  credentials from them independently. To allow credential chaining, issuers reserve one attribute (usually $m_1$)  for a secret value hidden by holder. Holder is supposed then to set it to the same value in all credentials, 
whereas Relying Parties require them to be equal along all credentials. A proof request should specify then a list of schemas that credentials should satisfy in certain order. 

## Schema preparation

Credentials should have limited use to only authorized holder entities called agents. Agents can prove authorization to use a credential by including a policy address **_I_** in primary credentials as attribute *m<sub>3</sub>*.

### Attributes
Issuer defines the primary credential schema 𝒮 with *l* attributes *m<sub>1</sub>,m<sub>2</sub>,..., m<sub>l</sub>* and the set of hidden attributes *A<sub>h</sub> ⊂ {1,2,...,l}*. In Sovrin, *m<sub>1</sub>* is reserved for the link secret of the holder, *m<sub>2</sub>* is reserved for the context -- the enumerator for the holders, *m<sub>3</sub>* is reserved for the policy address **_I_**. By default, *{1,3} ⊂ A<sub>h</sub>* whereas *2 ∉ A<sub>h</sub>*..

Issuer defines the non-revocation credential  with *2* attributes *m<sub>1</sub>,m<sub>2</sub>*. In Sovrin, *A<sub>h</sub> = {1}* and *m<sub>1</sub>* is reserved for the link secret of the holder, *m<sub>2</sub>* is reserved for the context -- the enumerator for the holders.

### Primary Credential Cryptographic Setup
In Sovrin, issuers use [CL-signatures](http://groups.csail.mit.edu/cis/pubs/lysyanskaya/cl02a.pdf) for primary credentials, although other signature types will be supported too.


For the CL-signatures issuer generates:
1. Random 1536-bit primes *p',q'* such that  *p ← 2p'+1* and *q ← 2q'+1* are primes too. Then compute *n ← pq*.
1. A random quadratic residue  *S mod n*;
1. Random ![*x<sub>Z</sub>, x<sub>R1</sub>,...,x<sub>Rl</sub> ∈ \[2; p'q'-1\]*](Eq1.png)

Issuer computes
![*Z ← S<sup>x<sub>Z<sub></sup>(mod n); {R<sub>i</sub> ← S<sup>x<sub>Ri</sub></sup>(mod n)\}<sub>1 ≤ i ≤ l</sub>;*](Eq2.png)


The issuer's public key is ![*P<sub>k</sub> = (n, S,Z,{R<sub>i</sub>}<sub>1 ≤ i ≤ l</sub>)*](Eq3.png) and the private key is *s<sub>k</sub> = (p, q)*.

### Issuer Setup Correctness Proof
1. Issuer generates random ![*x~<sub>Z</sub>, x!<sub>R1</sub>,...,x~<sub>Rl</sub> ∈ \[2; p'q'-1\]*](Eq4.png)
1. Computes

![Eq1](Eq5.png)


Here *H<sub>I</sub>* is the issuer-defined hash function, by default SHA2-256.

3. Proof *𝒫<sub>I</sub>* of correctness is ![Eq6](Eq6.png)


### Non-revocation Credential Cryptographic Setup
In Sovrin, issuers use [CKS accumulators and signatures](https://eprint.iacr.org/2008/539.pdf) to track revocation status of primary credentials, although other signature types will be supported too. Each primary credential is given an index from 1 to $L$.

The CKS  accumulator is used to track revoked primary credentials, or equivalently, their indices. The accumulator contains up to $L$ indices of credentials. If issuer has to issue more credentials, another accumulator is prepared, and so on. Each accumulator $A$ has an identifier $I_A$.

Issuer chooses
* Groups $\mathbb{G}_1,\mathbb{G}_2,\mathbb{G}_T$ of
    prime order $q$;
* Type-3 pairing operation $e:\, \mathbb{G}_1\times\mathbb{G}_2\rightarrow\mathbb{G}_T$.
* Generators: $g$ for $\mathbb{G}_1$, $g'$ for
    $\mathbb{G}_2$.

%Typically the triplet $(\mathbb{G}_1,\mathbb{G}_2,\mathbb{G}_T)$ is selected together with a pairing function as only a few combinations admit a suitable pairing. Existing implementations provide just a few possible pairing functions and thus triplets, thus making the group details in fact oblivious to the user. For the sake of curiosity we note that $\mathbb{G}_1,\mathbb{G}_2$ are different groups of elliptic curve points, whereas $\mathbb{G}_T$ is not a curve point group.\\
Issuer:
1. Generates
    1. Random $h,h_0,h_1,h_2,\widetilde{h}\in \mathbb{G}_1$;
    1. Random $u,\widehat{h}\in \mathbb{G}_2$;
    1. Random $sk,x \pmod{q}$.
1. Computes
\begin{align*}
    pk&\leftarrow g^{sk}; & y&\leftarrow \widehat{h}^x.
\end{align*}

The revocation public key is
$P_r = (h,h_0,h_1,h_2,\widetilde{h},\widehat{h},u,pk,y)$ and the secret key is $(x,sk)$.

#### New Accumulator Setup
To create a new accumulator $A$, issuer:
1. Generates random $\gamma\pmod{q}$.
1. Computes
   1. $g_1,g_2,\ldots,g_L,g_{L+2},\ldots,g_{2L}$ where
$g_i = g^{\gamma^i}$. 
   1. $g_1',g_2',\ldots,g_L',g_{L+2}',\ldots,g_{2L}'$ where
$g_i' = g'^{\gamma^i}$. 
   1. $z = (e(g,g'))^{\gamma^{L+1}}$.
1. Set $V \leftarrow\emptyset$, $\mathrm{acc}\leftarrow 1$.

The accumulator public key is $P_a = (z)$ and secret key is $(\gamma)$.

Issuer publishes $(P_a,V)$ on the ledger. The accumulator identifier is $ID_a = z$.

## Issuance of Credentials

### Holder Setup

Holder:
* Loads credential schema $\mathcal{S}$.
* Sets hidden attributes $\{m_i\}_{i \in A_h}$.
* Establishes a connection with issuer and gets nonce $n_0$ either from issuer or as a precomputed value. Holder is known to issuer with identifier $\mathcal{H}$.

Holder prepares data for primary credential:
1. Generate random 3152-bit $v'$.
1. Generate random 593-bit $\{\widetilde{m_i}
\}_{i \in A_h}$, and random 3488-bit $\widetilde{v'}$.
1. Compute taking $S,Z,R_i$ from $P_k$:
\begin{align}
U& \leftarrow (S^{v'}) \prod_{i \in A_c}{R_i^{m_i}} \pmod{n};
\end{align}
1. Compute
\begin{align}
\widetilde{U}&\leftarrow (S^{\widetilde{v'}}) \prod_{i \in A_c}{R_i^{\widetilde{m_i}}}\pmod{n};
&%\{\widetilde{C_i}& \leftarrow Z^{\widetilde{m_i}}S^{\widetilde{r_i}}\pmod{n}\}_{i \in A_c};&
%FOR COMMITMENTS
\\
c\leftarrow& H(U||\widetilde{U}||
%\{C_i, \widetilde{C_i} \}_{i \in A_c}|| %FOR COMMITMENTS
n_0);&
\widehat{v'}&\leftarrow \widetilde{v'} + c v';&\\
\{\widehat{m_i}&\leftarrow \widetilde{m_i} + c m_i\}_{i \in A_h};&
%\{\widehat{r_i}& \leftarrow \widetilde{r_i} + c r_i\}_{i \in A_c}
%FOR COMMITMENTS
\end{align}
1. Generate random 80-bit nonce $n_1$
1. Send $
\{U, c,\widehat{v'}, \{
%C_i, %FOR COMMITMENTS
\widehat{m_i}
%, \widehat{r_i} %FOR COMMITMENTS
\}_{i \in A_h}, n_1\}$ to the issuer.

Holder prepares for non-revocation credential:
1. Load issuer's revocation key $P_R$ and generate random $s'_R\bmod{q}$.
1. Compute $U_R \leftarrow h_2^{s'_R}$
taking $h_2$ from $P_R$.
1. Send $U_R$ to the issuer.

#### Issuer Proof of Setup Correctness
To verify the proof $\mathcal{P}_i$ of correctness, holder
computes
$$
\widehat{Z} \leftarrow Z^{-c} S^{\widehat{x_Z}}\pmod{n} ;\quad  \{\widehat{R_i} 
\leftarrow R_i^{-c} S^{\widehat{x_{R_i}}}\pmod{n}\}_{1\leq i \leq l};
$$
and verifies 
$$
c =  H_I(Z||\widehat{Z}||\{R_i,\widehat{R_i}\}_{1\leq i \leq l})
$$.
%For the new user issuer selects the accumulator index $A_{R_i}$ and the user index $i$ so that $(A_{R_i},i)$ is unique.  

### Primary Credential Issuance
Issuer verifies the correctness of holder's input:
1. Compute
\begin{align}
\widehat{U}& \leftarrow (U^{-c}) \prod_{i \in A_h}{R_i^{\widehat{m_i}}}(S^{\widehat{v'}})\pmod{n};
%\\
%\{\widehat{C_i}& \leftarrow {C_i}^{-c}Z^{\widehat{m_i}}S^{\widehat{r_i}}\pmod{n}\}_{i \in A_c}
\end{align}
1. Verify
$c= H(U||\widehat{U}||
%\{C_i,\widehat{C_i}\}_{i \in \mathcal{A}_c}||
n_0)$
1. Verify that $\widehat{v'}$ is a 673-bit number, $\{\widehat{m_i}, \widehat{r_i}\}_{i \in \mathcal{A}_c}$ are 594-bit numbers.

Issuer prepares the credential:
1. Assigns index $i<L$ to holder, which is one of not yet taken indices for the issuer's current accumulator $A$. Compute $m_2\leftarrow H(i||\mathcal{H})$ and store information about holder and the value $i$ in a local database.
1. Set, possibly in agreement with holder, the values of disclosed attributes, i.e. with indices from $A_k$.
1. Generate random 2724-bit number $v''$ with most significant bit equal 1 and random prime  $e$ such that
\begin{equation}\label{eq:e}
2^{596}\leq e \leq 2^{596}+ 2^{119}.
\end{equation}
1. Compute
\begin{align}
Q& \leftarrow \frac{Z}{U S^{v''} \prod_{i\in \mathcal{A}_k}{R_i^{m_i}}\pmod{n}};\\
A& \leftarrow Q^{e^{-1}\pmod{p'q'}}\pmod{n};
\end{align}
1. Generate random $r < p'q'$;
1. Compute
\begin{align}
\widehat{A}&\leftarrow Q^r\pmod{n};\\
c'&\leftarrow H(Q||A||\widehat{A}||n_1);\\
s_e&\leftarrow r - c'e^{-1}\pmod{p'q'};
\end{align}
1. Send the primary pre-credential  $(\{m_i\}_{i\in A_k},A,e,v'',s_e,c')$ to the holder.

### Non-Revocation Credential Issuance

%We assume that the attribute $m_2$ is used to enumerate holders by issuer (details are irrelevant for revocation).\newline\newline
Issuer:
1. Generate random numbers $s'',c\bmod{q}$.
1. Take $m_2$ from the primary
credential he is preparing for holder.
1. Take $A$ as the accumulator value for which index $i$ was taken. Retrieve current set of non-revoked indices $V$.
1. Compute:
\begin{align}
\sigma &\leftarrow \left( h_0 h_1^{m_2}\cdot U\cdot  g_i\cdot  h_2^{s''}\right)^{\frac{1}{x+c}};&
w &\leftarrow \prod_{j\in V}g_{L+1-j+i}';\\
\sigma_i &\leftarrow g'^{1/(sk+\gamma^i)};&
u_i &\leftarrow u^{\gamma^i};\\
A&\leftarrow A\cdot g'_{L+1-i};&
V&\leftarrow V\cup\{i\};\\
\mathrm{wit}_i&\leftarrow\{\sigma_i,u_i,g_i,w,V\}.
\end{align}
1. Send the non-revocation pre-credential  $(I_A,\sigma,c,s'',\mathrm{wit}_i,g_i,g_i',i)$ to holder.
1.  Publish updated $V, A$ on the ledger.

### Storing Credentials
Holder works with the primary pre-credential:
1. Compute $v \leftarrow v'+v''$.
1. Verify $e$ is prime and satisfies Eq.~\eqref{eq:e}.
1. Compute
\begin{align}
Q\leftarrow \frac{Z}{S^v\prod_{i \in C_s}R_i^{m_i}}\pmod{n};
\end{align}
1. Verify $Q = A^e\pmod{n}$
1. Compute
\footnote{We have removed factor $S^{v's_e}$ here from computing of $\widehat{A}$ as it seems to be a typo in the Idemix spec.}
\begin{align}
\widehat{A}\leftarrow A^{c'+s_e\cdot e} \pmod{n}.
\end{align}
1. Verify $c'=H(Q||A||\widehat{A}||n_2).$
1. Store *primary credential* $C_p=(\{m_i\}_{i \in C_s},A,e,v)$.

Holder takes the non-revocation pre-credential $(I_A,\sigma,c,s'',\mathrm{wit}_i,g_i,g_i',i)$ computes $s_R \leftarrow s'+s''$ and stores the non-revocation credential $C_{NR}\leftarrow(I_A,\sigma,c,s,\mathrm{wit}_i,g_i,g_i',i)$.
### Non revocation proof of correctness
Holder computes
\begin{align}
\frac{e(g_i,acc_V)}{e(g,w)} &\overset{\text{?}}{=} z;\\
e(pk\cdot g_i, \sigma_i) &\overset{\text{?}}{=} e(g,g');\\
e(\sigma,y\cdot \widehat{h}^c)& \overset{\text{?}}{=} e(h_0 \cdot h_1^{m_2}h_2^{s}g_i,\widehat{h}).
\end{align}
    

## Revocation
Issuer identifies a credential to be revoked in the database and retrieves its index $i$, the  accumulator value $A$, and valid index set $V$. Then he proceeds:
1. Set $V\leftarrow V\setminus\{i\}$;
1. Compute $A \leftarrow A/g'_{L+1-i}$.
1. Publish $\{V,A\}$.
    
## Presentation

### Proof Request

Verifier sends a proof request, where it specifies the ordered set of $d$ credential schemas
$\{\mathcal{S}_1,\mathcal{S}_2,\ldots,\mathcal{S}_d\}$, so that the holder should provide a set of $d$ credential pairs $(C_p,C_{NR})$ that correspond to these schemas.

Let credentials in these schemas contain $X$ attributes in total. Suppose that the request makes to open $x_1$ attributes, makes to prove $x_2$ equalities $m_i=m_j$ (from possibly distinct schemas) and makes to prove $x_3$ predicates of form  $m_i >\leq \geq<z$. Then effectively $X-x_1$ attributes are unknown (denote them $A_h$), which form $x_4=(X-x_1-x_2)$ equivalence classes. Let $\phi$ map $A_h$ to $\{1,2,\ldots,x_4\}$ according to this equivalence.  Let $A_v$ denote the set of indices of $x_1$ attributes that are disclosed.

The proof request also specifies $A_h,\phi,A_v$ and the set $\mathcal{D}$ of predicates. Along with a proof request, Verifier also generates and sends 80-bit nonce $n_1$.

### Proof Preparation
Holder prepares all credential pairs $(C_p,C_{NR})$ to submit:
1. Generates $x_4$ random 592-bit values $\widetilde{y_1},\widetilde{y_2},
\ldots,\widetilde{y_{x_4}}$ and set $\widetilde{m_j} \leftarrow \widetilde{y_{\phi(j)}} $ for  $j \in \mathcal{A}_{h}$. 
1. Create empty sets $\mathcal{T}$ and $\mathcal{C}$.
1. For all credential pairs $(C_p,C_{NR})$ executes Section~\ref{sec:prepare}.
1. Executes Section~\ref{sec:hash} once.
1. For all credential pairs $(C_p,C_{NR})$ executes Section~\ref{sec:final}.
1. Executes Section~\ref{sec:final} once.

Verifier:
1. For all credential pairs $(C_p,C_{NR})$ executes Section~\ref{sec:verify}.
1. Executes Section~\ref{sec:finalhash} once.

\label{sec:prepare}

\textbf{Non-revocation proof}
Holder:
1. Load issuer's public revocation key $p = (h,h_1,h_2,\widetilde{h},\widehat{h},u,pk,y)$.
1. Load the non-revocation credential $C_{NR}\leftarrow(I_A,\sigma,c,s,\mathrm{wit}_i,g_i,g_i',i)$;
1. Obtain recent $V,\mathrm{acc}$ (from Verifier, Sovrin link, or elsewhere).
1. Update $C_{NR}$:
\begin{align*}
w&\leftarrow w\cdot \frac{\prod_{j\in V\setminus V_{old}}g'_{L+1-j+i}}{\prod_{j\in V_{old}\setminus V}g'_{L+1-j+i}};\\
V_{old}&\leftarrow V.
\end{align*}
Here $ V_{old}$ is taken from $\mathrm{wit}_i$ and updated there.
1. Select random $\rho,\rho',r,r',r'',r''',o,o'\bmod{q}$;
1. Compute
\begin{align}
E &\leftarrow h^{\rho} \widetilde{h}^o &
D & \leftarrow g^r\widetilde{h}^{o'};\\
A &\leftarrow \sigma \widetilde{h}^{\rho}&
\mathcal{G} &\leftarrow g_i\widetilde{h}^r;\\
\mathcal{W} &\leftarrow w\widehat{h}^{r'} &
\mathcal{S}&\leftarrow \sigma_i \widehat{h}^{r''}\\
\mathcal{U}&\leftarrow u_i \widehat{h}^{r'''}
\end{align}
and adds these values to $\mathcal{C}$.
1. Compute
\begin{align}
m&\leftarrow \rho \cdot c \mod{q}; & t&\leftarrow o\cdot c \mod{q};\\
m'&\leftarrow r\cdot r''\mod{q}; & t'&\leftarrow o'\cdot r'' \mod{q};
\end{align}
and adds these values to $\mathcal{C}$.
1. Generate random $\widetilde{\rho},\widetilde{o},\widetilde{o'},\widetilde{c},
\widetilde{m},\widetilde{m'},\widetilde{t},\widetilde{t'},
\widetilde{m_2},\widetilde{s},
\widetilde{r},\widetilde{r'},\widetilde{r''},\widetilde{r'''},
\bmod{q}$.
1. Compute
\begin{align}
\overline{T_1}&\leftarrow h^{\widetilde{\rho}} \widetilde{h}^{\widetilde{o}} &
\overline{T_2}&\leftarrow E^{\widetilde{c}}h^{-\widetilde{m}}\widetilde{h}^{-\widetilde{t}}
\end{align}
\begin{equation}
\overline{T_3}\leftarrow e(A,\widehat{h})^{\widetilde{c}}\cdot e(\widetilde{h},\widehat{h})^{\widetilde{r}}\cdot
e(\widetilde{h},y)^{-\widetilde{\rho}}\cdot
e(\widetilde{h},\widehat{h})^{-\widetilde{m}}\cdot
e(h_1,\widehat{h})^{-\widetilde{m_2}}\cdot e(h_2,\widehat{h})^{-\widetilde{s}}\\
\end{equation}
\begin{align}
\overline{T_4}&\leftarrow e(\widetilde{h},\mathrm{acc})^{\widetilde{r}}\cdot
e(1/g,\widehat{h})^{\widetilde{r'}}&
\overline{T_5}&\leftarrow g^{\widetilde{r}}\widetilde{h}^{\widetilde{o'}}\\
\overline{T_6}&\leftarrow D^{\widetilde{r''}}g^{-\widetilde{m'}}
\widetilde{h}^{-\widetilde{t'}}&
\overline{T_7}&\leftarrow e(pk\cdot \mathcal{G},\widehat{h})^{\widetilde{r''}}\cdot 
e(\widetilde{h},\widehat{h})^{-\widetilde{m'}}\cdot
e(\widetilde{h},\mathcal{S})^{\widetilde{r}}\\
\overline{T_8}&\leftarrow e(\widetilde{h},u)^{\widetilde{r}}
\cdot e(1/g,\widehat{h})^{\widetilde{r'''}}
\end{align}
and add these values to $\mathcal{T}$.

\textbf{Validity proof}

Holder:
1. Generate a random 592-bit number $\widetilde{m_j}$ for each $j \in \mathcal{A}_{\overline{r}}$.
1. For each credential $C_p = (\{m_j\},A,e,v)$ and issuer's
public key $pk_I$:
   1. Choose random 3152-bit $r$.
   1. Take $n,S$ from $pk_I$ compute
\begin{equation}\label{eq:aprime}
A' \leftarrow A S^{r}\pmod{n}
\text{ and } v' \leftarrow v - e\cdot r\text{ as integers};
\end{equation}
and add to $\mathcal{C}$.
   1. Compute $e' \leftarrow e - 2^{596}$.
   1. Generate random 456-bit number $\widetilde{e}$.
   1. Generate random 3748-bit number $\widetilde{v}$.
   1. Compute
\begin{align}
T \leftarrow (A')^{\widetilde{e}}\left(\prod_{j\in \mathcal{A}_{\overline{r}}} R_j^{\widetilde{m_j}}\right)(S^{\widetilde{v}})\pmod{n}
\end{align}
and add to $\mathcal{T}$.
1. Load $Z,S$ from issuer's public key.
1. For each predicate $p$ where the operator $*$ is one of $>, \geq, <, \leq$.
   1. Calculate $\Delta$ such that:
$$
\Delta \leftarrow \begin{cases}
z_j-m_j; & \mbox{if } * \equiv\ \leq\\
z_j-m_j-1; & \mbox{if } * \equiv\ <\\
m_j-z_j; & \mbox{if } * \equiv\ \geq\\
m_j-z_j-1; & \mbox{if } * \equiv\ >
\end{cases}
$$
   1. Calculate $a$ such that:
$$
a \leftarrow \begin{cases}
-1 & \mbox{if } * \equiv \leq or <\\
1  & \mbox{if } * \equiv \geq or >
\end{cases}
$$
   1. Find (possibly by exhaustive search) $u_1, u_2,u_3, u_4$ such that:
 \begin{align}
\Delta = (u_1)^2+ (u_2)^2+ (u_3)^2+ (u_4)^2
\end{align}
   1. Generate random 2128-bit numbers $r_1,r_2,r_3,r_4, r_{\Delta}$.
   1. Compute
\begin{align}
\{T_i &\leftarrow Z^{u_i}S^{r_i} \pmod{n}\}_{1 \leq i \leq 4};\\
T_{\Delta} &\leftarrow  Z^{\Delta}S^{r_{\Delta}} \pmod{n};
\end{align}
and add these values to $\mathcal{C}$ in the order $T_1,T_2,T_3,T_4,T_{\Delta}$.
   1. Generate random 592-bit numbers $\widetilde{u_1},\widetilde{u_2},\widetilde{u_3},\widetilde{u_4}$.
   1. Generate random 672-bit numbers $\widetilde{r_1},\widetilde{r_2},\widetilde{r_3},\widetilde{r_4},\widetilde{r_{\Delta}}$.
   1. Generate random 2787-bit number $\widetilde{\alpha}$
   1. Compute
\begin{align}
\{\overline{T_i} &\leftarrow Z^{\widetilde{u_i}}S^{\widetilde{r_i}}\pmod{n}\}_{1 \leq i \leq 4};\\
\overline{T_{\Delta}} &\leftarrow  Z^{\widetilde{m_j}}S^{a \widetilde{r_{\Delta}}} \pmod{n};\\
Q &\leftarrow (S^{\widetilde{\alpha}})\prod_{i=1}^{4}{T_i^{\widetilde{u_i}}}\pmod{n};
\end{align}
and add these values to $\mathcal{T}$ in the order $\overline{T_1},\overline{T_2},\overline{T_3},\overline{T_4}, \overline{T_{\Delta}},Q$.


#### Hashing

Holder computes challenge hash
\begin{align}
c_H \leftarrow H(\mathcal{T},\mathcal{C},n_1);
\end{align}
and sends $c_H$ to Verifier. 

#### Final preparation
Holder:
1. For non-revocation credential $C_{NR}$ compute:
\begin{align*}
\widehat{\rho} &\leftarrow \widetilde{\rho} - c_H\rho\bmod{q} &
\widehat{o} &\leftarrow \widetilde{o} - c_H\cdot o\bmod{q}\\
\widehat{c} &\leftarrow \widetilde{c} - c_H\cdot c\bmod{q} &
\widehat{o'} &\leftarrow \widetilde{o'} - c_H\cdot o'\bmod{q}\\
\widehat{m} &\leftarrow \widetilde{m} - c_H m\bmod{q} &
\widehat{m'} &\leftarrow \widetilde{m'} - c_H m'\bmod{q}\\
\widehat{t} &\leftarrow \widetilde{t} - c_H t\bmod{q} &
\widehat{t'} &\leftarrow \widetilde{t'} - c_H t'\bmod{q}\\
\widehat{m_2} &\leftarrow \widetilde{m_2} - c_H m_2\bmod{q} &
\widehat{s} &\leftarrow \widetilde{s} - c_H s\bmod{q}\\
\widehat{r} &\leftarrow \widetilde{r} - c_H r\bmod{q} &
\widehat{r'} &\leftarrow \widetilde{r'} - c_H r'\bmod{q}\\
\widehat{r''} &\leftarrow \widetilde{r''} - c_H r''\bmod{q} &
\widehat{r'''} &\leftarrow \widetilde{r'''} - c_H r'''\bmod{q}.
\end{align*}
and add them to $\mathcal{X}$.
1. For primary credential $C_p$ compute:
\begin{align}
\widehat{e}& \leftarrow \widetilde{e}+c_H e';\\
\widehat{v}& \leftarrow \widetilde{v}+c_H v';\\
\{\widehat{m}_j& \leftarrow \widetilde{m_j} + c_H m_j\}_{j \in \mathcal{A}_{\overline{r}}};
\end{align}
The values $Pr_C=(\widehat{e},\widehat{v},\{\widehat{m_j}\}_{j \in \mathcal{A}_{\overline{r}}},A')$ are the *sub-proof*
for credential $C_p$.
1. For each predicate $p$ compute:
\begin{align}
\{\widehat{u_i}& \leftarrow \widetilde{u_i}+c_H u_i\}_{1\leq i \leq 4};\\
\{\widehat{r_i}& \leftarrow \widetilde{r_i}+c_H r_i\}_{1\leq i \leq 4};\\
\widehat{r_{\Delta}}& \leftarrow \widetilde{r_{\Delta}}+c_H r_{\Delta};\\
\widehat{\alpha}& \leftarrow \widetilde{\alpha}+c_H (r_{\Delta}- u_1r_1 - u_2r_2 - u_3r_3 - u_4r_4); 
\end{align}
The values $Pr_p =( \{\widehat{u_i}\}, \{\widehat{r_i}\},\widehat{r_{\Delta}},\widehat{\alpha},\widehat{m_j})$ are the sub-proof for predicate $p$.


#### Sending
Holder sends $(c,\mathcal{X},\{Pr_C\},\{Pr_p\},\mathcal{C})$  to the Verifier.

### Verification
For the credential pair $(C_p,C_{NR})$, Verifier retrieves relevant variables from $\mathcal{X},\{Pr_C\},\{Pr_p\},\mathcal{C}$. 

#### Non-revocation check
 
Verifier computes
\begin{align}
\widehat{T_1}&\leftarrow E^{c_H}\cdot h^{\widehat{\rho}} \cdot \widetilde{h}^{\widehat{o}} &
\widehat{T_2}&\leftarrow E^{\widehat{c}}\cdot h^{-\widehat{m}}\cdot\widetilde{h}^{-\widehat{t}}
\end{align}
\begin{equation}
\widehat{T_3}\leftarrow\left(\frac{e(h_0\mathcal{G},\widehat{h})}{e(A,y)} \right)^{c_H} \cdot e(A,\widehat{h})^{\widehat{c}}\cdot e(\widetilde{h},\widehat{h})^{\widehat{r}}\cdot
e(\widetilde{h},y)^{-\widehat{\rho}}\cdot
e(\widetilde{h},\widehat{h})^{-\widehat{m}}\cdot
e(h_1,\widehat{h})^{-\widehat{m_2}}\cdot e(h_2,\widehat{h})^{-\widehat{s}}\\
\end{equation}
\begin{align}
\widehat{T_4}&\leftarrow\left(\frac{e(\mathcal{G},\mathrm{acc})}{e(g,\mathcal{W})z}\right)^{c_H} \cdot e(\widetilde{h},\mathrm{acc})^{\widehat{r}}\cdot
e(1/g,\widehat{h})^{\widehat{r'}}
&
\widehat{T_5}&\leftarrow D^{c_H}\cdot g^{\widehat{r}}\widetilde{h}^{\widehat{o'}}\\
\widehat{T_6}&\leftarrow  D^{\widehat{r''}}\cdot g^{-\widehat{m'}}
\widetilde{h}^{-\widehat{t'}}&
\widehat{T_7}&\leftarrow
\left(\frac{e(pk\cdot\mathcal{G},\mathcal{S})}{e(g,g')}\right)^{c_H}\cdot e(pk\cdot \mathcal{G},\widehat{h})^{\widehat{r''}}\cdot 
e(\widetilde{h},\widehat{h})^{-\widehat{m'}}\cdot
e(\widetilde{h},\mathcal{S})^{\widehat{r}}\\
\widehat{T_8}&\leftarrow \left(\frac{e(\mathcal{G},u)}{e(g,\mathcal{U})}\right)^{c_H}\cdot e(\widetilde{h},u)^{\widehat{r}}
\cdot e(1/g,\widehat{h})^{\widehat{r'''}}
\end{align}
and adds these values to $\widehat{T}$.

#### Validity
Verifier uses all issuer public key $pk_I$ involved into the credential generation and  the received $(c,\widehat{e},\widehat{v},\{\widehat{m_j}\},A')$. He also uses revealed 
$\{m_j\}_{j \in \mathcal{A}_r}$. He initiates $\widehat{\mathcal{T}}$ as empty set.


\begin{legal}
1. For each credential $C_p$, take each sub-proof $Pr_C$ and compute
\begin{equation}\label{eq:that}
 \widehat{T} \leftarrow \left(
    \frac{Z}
    { \left(
        \prod_{j \in \mathcal{A}_r}{R_j}^{m_j}
    \right)
    (A')^{2^{596}}
    }\right)^{-c}
    (A')^{\widehat{e}}
    \left(\prod_{j\in (\mathcal{A}_{\widetilde{r}})}{R_j}^{\widehat{m_j}}\right)
    (S^{\widehat{v}})\pmod{n}.
\end{equation}
Add $\widehat{T}$ to $\widehat{\mathcal{T}}$.
1. For each predicate $p$:
$$
\Delta' \leftarrow \begin{cases}
z_j; & \mbox{if } * \equiv\ \leq\\
z_j-1; & \mbox{if } * \equiv\ <\\
z_j; & \mbox{if } * \equiv\ \geq\\
z_j+1; & \mbox{if } * \equiv\ >
\end{cases}
$$
$$
a \leftarrow \begin{cases}
-1 & \mbox{if } * \equiv \leq or <\\
1  & \mbox{if } * \equiv \geq or >
\end{cases}
$$
   1. Using $Pr_p$ and $\mathcal{C}$ compute
\begin{align}
\{\widehat{T_i} &\leftarrow T_i^{-c}Z^{\widehat{u_i}} S^{\widehat{r_i}}\pmod{n}\}_{1\leq i \leq 4};\label{eq:pr2}\\
\widehat{T_{\Delta}} &\leftarrow \left(T_{\Delta}^{a}Z^{\Delta'}\right)^{-c}Z^{\widehat{m_j}}S^{a\widehat{r_{\Delta}}}\pmod{n};\label{eq:pr1}\\
\widehat{Q}&\leftarrow (T_{\Delta}^{-c})\prod_{i=1}^{4}T_i^{\widehat{u_i}}(S^{\widehat{\alpha}})\pmod{n}\label{eq:pr3},
\end{align}
and add these values to  $\widehat{\mathcal{T}}$ in the order $\widehat{T_1},\widehat{T_2} ,\widehat{T_3},\widehat{T_4},\widehat{T_{\Delta}},\widehat{Q}$.

#### Final hashing
1. Verifier computes
$$
\widehat{c_H}\leftarrow H(\widehat{\mathcal{T}},\mathcal{C},n_1).
$$
1. If $c=\widehat{c}$ output VERIFIED else FAIL.


 

# Reference
[reference]: #reference

Provide guidance for implementers, procedures to inform testing,
interface definitions, formal function prototypes, error codes,
diagrams, and other technical details that might be looked up.
Strive to guarantee that:

- Interactions with other features are clear.
- Implementation trajectory is well defined.
- Corner cases are dissected by example.

# Drawbacks
[drawbacks]: #drawbacks

Why should we *not* do this?

# Rationale and alternatives
[alternatives]: #alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not
choosing them?
- What is the impact of not doing this?

# Prior art
[prior-art]: #prior-art

Discuss prior art, both the good and the bad, in relation to this proposal.
A few examples of what this can include are:

- Does this feature exist in other SSI ecosystems and what experience have
their community had?
- For other teams: What lessons can we learn from other attempts?
- Papers: Are there any published papers or great posts that discuss this?
If you have some relevant papers to refer to, this can serve as a more detailed
theoretical background.

This section is intended to encourage you as an author to think about the
lessons from other implementers, provide readers of your proposal with a
fuller picture. If there is no prior art, that is fine - your ideas are
interesting to us whether they are brand new or if they are an adaptation
from other communities.

Note that while precedent set by other communities is some motivation, it
does not on its own motivate an enhancement proposal here. Please also take
into consideration that Indy sometimes intentionally diverges from common
identity features.

# Unresolved questions
[unresolved]: #unresolved-questions

This protocol is already implemented in indy-crypto.
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?