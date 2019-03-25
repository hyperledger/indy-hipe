- Name: Anonymous Credential Protocol
- Author: Mike Lodder and Brent Zundel
- Start Date: January 25, 2019
- PR:
- Jira Issue:

# Summary
[summary]: #summary

Anonymous credentials form the heart of Indy's identity capabilities.
This document describes the protocol for
[Camenisch-Lysyanskaya signatures][CL-signatures] and the anonymous credentials
they enable.

This document is a markdown-formatted version of work by Dmitry Khovratovich,
which is based on [CL signatures][CL-signatures].

# Motivation
[motivation]: #motivation

This HIPE is intended as a publication of the protocol behind the code that has
already been implemented in [indy-crypto][indy-crypto-github].

# Tutorial
[tutorial]: #tutorial

## Introduction
[intro]: #intro
### Concept

*Anonymous credentials* allow an identity owner to prove certain properties
about their identity an uncorrelatable way without revealing other identity
details. The properties can be raw identity attributes such as a birth date or
address, or more sophisticated predicates such as "A is older than 20 years
old".

We assume three parties: *issuer*, *holder*, and *verifier*. From the functional
perspective:
* the issuer gives a credential *C* based on identity schema *X*,
which asserts certain properties 𝒫 about *X*, to the holder.
* The credential consists of attributes represented by integers
*m<sub>1</sub>, m<sub>2</sub>,..., m<sub>l</sub>*.
* The holder then presents (𝒫,*C*) to the verifier, which can verify that the
issuer has asserted property 𝒫.

### Properties

* Credentials are *unforgeable* in the sense that no one can fool the verifier
with a credential not prepared by the issuer.

* Credentials are *unlinkable* in the sense that it is impossible to correlate
the presented credential across multiple presentations. This is implemented by
the holder *proving* with a zero-knowledge proof *that he has a credential*
rather than showing the credential. Unlinkability can be simulated by the issuer
generating a sufficient number of ordinary unrelated credentials.

Note: unlinkability may be turned off to make credentials *one-time use* so that
second and later presentations are detected.

## Generic notation

Attribute *m* is a *l<sub>a</sub>*-bit unsigned integer. Technically it is
possible to support credentials with different *l<sub>a</sub>*, but in Sovrin
it is set *l<sub>a</sub>*=256.


## Protocol Overview

The described protocol supports anonymous credentials given to multiple holders
by various issuers, which are presented to various relying parties.

Various types of anonymous credentials can be supported. In this section, the
combination of [CL-based credentials][CL-signatures] and
[pairing-based revocation][pairing-revocation] is described.

The simplest credential lifecycle, with one credential, single issuer, holder,
and verifier is as follows:
1. Issuer determines a credential schema 𝒮: the type of cryptographic signatures
used to sign the credentials, the number *l* of attributes in a credential, the
indices *A<sub>h</sub> ⊂ {1,2,...,l}* of hidden attributes, the public key
*P<sub>k</sub>*, the non-revocation credential attribute number *l<sub>r</sub>*
and non-revocation public key *P<sub>r</sub>* (Section~\ref{sec:iss-setup}).
Then he publishes it on the ledger and announces the attribute semantics.
1. Holder retrieves the credential schema from the ledger and sets the hidden
attributes.
1. Holder requests a credential from issuer. He sends hidden attributes in a
blinded form to issuer and agrees on the values of known attributes
*A<sub>k</sub> = {1,2,...,l} \ A<sub>h</sub>*.
1. Issuer returns a credential pair *(C<sub>p</sub>, C<sub>NR</sub>)* to holder.
The first credential contains the requested *l* attributes. The second
credential asserts the non-revocation status of the first one. Issuer publishes
the non-revoked status of the credential on the ledger.
1. Holder approaches verifier. Verifier sends the Proof Request ℰ to holder. The
Proof Request contains the credential schema *𝒮<sub>E</sub>* and disclosure
predicates 𝒟. The predicates for attribute *m* and value *V* can be of form
*m=V*, *m<V*, or *m>V*. Some attributes may be asserted to be the same:
*m<sub>i</sub>=m<sub>j</sub>*.
1. Holder checks that the credential pair he holds satisfies the schema
*𝒮<sub>E</sub>*. He retrieves the non-revocation witness from the ledger.
1. Holder creates a proof *P* that he has a non-revoked credential satisfying
the proof request ℰ and sends it to verifier.
1. Verifier verifies the proof.


If there are multiple issuers, the holder obtains credentials from them
independently. To allow credential chaining, issuers reserve one attribute
(usually *m<sub>1</sub>*) for a secret value hidden by holder. The holder is
supposed then to set it to the same hidden value in all issued credentials.
Relying Parties require them to be the same in all credentials. A proof request
should specify the list of schemas that credentials should satisfy in.

## Schema preparation

Credentials may have limited use to only authorized holder entities called
agents. Agents can prove authorization to use a credential by the holder
including a policy address **_I_** in primary credentials as attribute
*m<sub>3</sub>*.

### Attributes
Issuer defines the primary credential schema 𝒮 with *l* attributes
*m<sub>1</sub>,m<sub>2</sub>,..., m<sub>l</sub>* and the set of hidden
attributes *A<sub>h</sub> ⊂ {1,2,...,l}*.

By default, *{1,3} ⊂ A<sub>h</sub>* whereas *2 ∉ A<sub>h</sub>*

Issuer defines the non-revocation credential  with *2* attributes
*m<sub>1</sub>,m<sub>2</sub>*.

In Sovrin:
* *A<sub>h</sub> = {1}* and *m<sub>1</sub>* is reserved for the link secret of
the holder,
* *m<sub>2</sub>* is reserved for the context -- the enumerator for the holders,
* *m<sub>3</sub>* is reserved for the policy address **_I_**.

### Primary Credential Cryptographic Setup
In Sovrin, issuers use [CL-signatures][CL-signatures] for primary credentials.

For the CL-signature, the issuer generates:
1. Random 1536-bit primes *p',q'* such that  *p ← 2p'+1* and *q ← 2q'+1*
are also prime. Then computes *n ← pq*.
1. A random quadratic residue *S mod n*;
1. Random
![*x<sub>Z</sub>, x<sub>R1</sub>,...,x<sub>Rl</sub> ∈ \[2; p'q'-1\]*](Eq1.png)

Issuer computes:
![*Z ← S<sup>x<sub>Z<sub></sup>(mod n); {R<sub>i</sub> ← S<sup>x<sub>Ri</sub></sup>(mod n)\}<sub>1 ≤ i ≤ l</sub>;*](Eq2.png)


The issuer's public key is
![*P<sub>k</sub> = (n, S,Z,{R<sub>i</sub>}<sub>1 ≤ i ≤ l</sub>)*](iss-pub-key-full.png)
and the private key is *s<sub>k</sub> = (p, q)*.

### Issuer Setup Correctness Proof
1. Issuer generates random
![*x~<sub>Z</sub>, x!<sub>R1</sub>,...,x~<sub>Rl</sub> ∈ \[2; p'q'-1\]*](Eq4.png)
1. Computes:

    ![Eq1](Eq5.png)

Here *H<sub>I</sub>* is the issuer-defined hash function, by default SHA2-256.

3. Proof *𝒫<sub>I</sub>* of correctness is ![Eq6](Eq6.png)

### Non-revocation Credential Cryptographic Setup
In Sovrin, issuers use [CKS accumulators and signatures][pairing-revocation] to
track revocation status of primary credentials, although other signature types
will be supported too. Each primary credential is given an index from 1 to *L*.

The CKS accumulator is used to track revoked primary credentials, or
equivalently, their indices. The accumulator contains up to $L$ indices of
credentials. If issuer has to issue more credentials, another accumulator is
prepared, and so on. Each accumulator *A* has an identifier *I<sub>A</sub>*.

Issuer chooses:
* Groups *𝔾<sub>1</sub>,𝔾<sub>2</sub>,𝔾<sub>T</sub>* of
    prime order *q*
* Type-3 pairing operation *e: 𝔾<sub>1</sub> x 𝔾<sub>2</sub> → 𝔾<sub>T</sub>*.
* Generators: *g* for *𝔾<sub>1</sub>*, *g'* for
    *𝔾<sub>2</sub>*.

Issuer:
1. Generates
    1. Random ![Eq7](Eq7.png)
    1. Random ![Eq8](Eq8.png)
    1. Random *sk, x (mod q)*.
1. Computes ![Eq9](Eq9.png)

The revocation public key is
![Eq10](Eq10.png) and the secret key is *(x,sk)*.

#### New Accumulator Setup
To create a new accumulator *A*, issuer:
1. Generates random *γ (mod q)*.
1. Computes
   1. ![Eq11](Eq11.png)
   1. ![Eq12](Eq12.png)
   1. ![Eq13](Eq13.png)
1. Set *V ← ∅, acc ← 1*

The accumulator public key is *P<sub>a</sub> = z* and secret key is *γ*.

Issuer publishes *(P<sub>a</sub>,V)* on the ledger.
The accumulator identifier is *ID<sub>a</sub> = z*.

## Issuance of Credentials

### Holder Setup

Holder:
* Loads credential schema *𝒮*.
* Sets hidden attributes *{ m<sub>i</sub> }<sub>{i ∈ Ah}</sub>*.
* Establishes a connection with issuer and gets nonce *n<sub>0</sub>* either
from issuer or as a precomputed value. Holder is known to issuer with identifier
 *ℋ*.

Holder prepares data for primary credential:
1. Generate random 3152-bit *v'*.
1. Generate random 593-bit *{m̃<sub>i</sub>}<sub>{i ∈ Ah}*,
and random 3488-bit *ṽ'*.
1. Compute, taking *S,Z,R<sub>i</sub>* from *P<sub>k</sub>*:

    ![Eq14](Eq14.png)

1. Compute

    ![Eq15](Eq15.png)

1. Generate random 80-bit nonce *n<sub>1</sub>*
1. Send to the issuer:

    ![Eq16](Eq16.png)

Holder prepares for non-revocation credential:
1. Load issuer's revocation key *P<sub>R</sub>* and generate
random *s'<sub>R</sub>mod q*.
1. Compute *U<sub>R</sub> ← h<sub>2</sub><sup>s'<sub>R</sub></sup>*
taking *h<sub>2</sub>* from *P<sub>R</sub>*.
1. Send *U<sub>R</sub>* to the issuer.

#### Issuer Proof of Setup Correctness
To verify the proof *𝒫<sub>i</sub>* of correctness, holder computes:

![Eq17](Eq17.png)

and verifies 

![Eq18](Eq18.png)

### Primary Credential Issuance
Issuer verifies the correctness of holder's input:
1. Compute

    ![Eq19](Eq19.png)

1. Verify
*c = H( U || Û || n<sub>0</sub> )*
1. Verify that *v̂'* is a 673-bit number,
*{m̂<sub>i</sub> r̂<sub>i</sub>}<sub>i ∈ 𝒜c</sub>* are 594-bit numbers.

Issuer prepares the credential:
1. Assigns index *i<L* to holder, which is one of not yet taken indices for the
issuer's current accumulator *A*. Compute *m<sub>2</sub>← H(i||ℋ)* and store
information about holder and the value *i* in a local database.
1. Set, possibly in agreement with holder, the values of disclosed attributes,
i.e. with indices from *A<sub>k</sub>*.
1. Generate random 2724-bit number *v''* with most significant bit equal 1 and
random prime *e* such that
*2<sup>596</sup>≤ e ≤ 2<sup>596</sup> + 2<sup>119</sup>*
1. Compute

    ![Eq20](Eq20.png)
1. Generate random *r < p'q'*;
1. Compute

    ![Eq21](Eq21.png)
1. Send the primary pre-credential
*( {m<sub>i</sub>}<sub>i ∈ Ak</sub>, A, e, v'', s<sub>e</sub>, c' )*
to the holder.

### Non-Revocation Credential Issuance

Issuer:
1. Generate random numbers *s'', c mod q*.
1. Take *m<sub>2</sub>* from the primary
credential he is preparing for holder.
1. Take *A* as the accumulator value for which index *i* was taken. Retrieve
current set of non-revoked indices *V*.
1. Compute:

    ![Eq22](Eq22.png)
1. Send the non-revocation pre-credential
*( I<sub>A</sub>, σ, c, s'', wit<sub>i</sub>, g<sub>i</sub>, g<sub>i</sub>', i )*
to holder.
1.  Publish updated *V, A* on the ledger.

### Storing Credentials
Holder works with the primary pre-credential:
1. Compute *v ← v'+v''*.
1. Verify *e* is prime and satisfies
*2<sup>596</sup>≤ e ≤ 2<sup>596</sup> + 2<sup>119</sup>*
1. Compute

    ![Eq23](Eq23.png)
1. Verify *Q = A<sup>e</sup> mod n*
1. Compute

*Â ← A<sup>c' + se * e</sup>mod n*

1. Verify *c' = H( Q || A || Â || n<sub>2</sub> ).*
1. Store **primary credential**
*C<sub>p</sub> = ( { m<sub>i</sub> }<sub>i ∈ Cs</sub>, A, e, v )*.

Holder takes the non-revocation pre-credential
*( I<sub>A</sub>, σ, c, s'', wit<sub>i</sub>, g<sub>i</sub>, g<sub>i</sub>', i)*
computes *s<sub>R</sub> ← s'+s''* and stores the non-revocation credential
*C<sub>NR</sub> ← ( I<sub>A</sub>, σ, c, s, wit<sub>i</sub>, g<sub>i</sub>,*
*g<sub>i</sub>', i)*.

### Non revocation proof of correctness
Holder computes:

![Eq24](Eq24.png)

## Revocation
Issuer identifies a credential to be revoked in the database and retrieves its
index *i*, the  accumulator value *A*, and valid index set *V*. Then he
proceeds:
1. Set *V ← V \ {i}*;
1. Compute *A ← A/g'<sub>L+1-i</sub>*
1. Publish *{V,A}*.
    
## Presentation

### Proof Request

Verifier sends a proof request, where it specifies the ordered set of *d*
credential schemas *{ 𝒮<sub>1</sub>, 𝒮<sub>2</sub>, ..., 𝒮<sub>d</sub> }*,
so that the holder should provide a set of *d* credential pairs
*( C<sub>p</sub>, C<sub>NR</sub> )* that correspond to these schemas.

Let credentials in these schemas contain *X* attributes in total.
Suppose that the request is made:
* to reveal *x<sub>1</sub>* attributes,
* to prove *x<sub>2</sub>* equalities *m<sub>i</sub> = m<sub>j</sub>*
(from possibly distinct schemas)
* to prove *x<sub>3</sub>* predicates of form  *m<sub>i</sub> > ≥ ≤ < z*.

Then effectively *X - x<sub>1</sub>* attributes remain hidden (denoted
*A<sub>h</sub>*), which form *x<sub>4</sub> = (X - x<sub>1</sub>*
*- x<sub>2</sub>)* equivalence classes.
* Let ϕ map *A<sub>h</sub>* to *{ 1, 2, ..., x<sub>4</sub> }* according to this
equivalence.
* Let *A<sub>v</sub>* denote the set of indices of *x<sub>1</sub>* attributes
that are disclosed.

The proof request also specifies *A<sub>h</sub>, ϕ, A<sub>v</sub>* and the set
𝒟 of predicates. Along with a proof request, the verifier also generates and
sends an 80-bit nonce *n<sub>1</sub>*.

### Proof Preparation
Holder prepares all credential pairs ![Credential pairs](cred-pairs.png) to submit:
1. Generates *x<sub>4</sub>* random 592-bit values *$ỹ<sub>1</sub>,*
*ỹ<sub>2</sub>,...,ỹ<sub>x4</sub>* and set ![Eq25](Eq25.png) for
![Eq26](Eq26.png).
1. Create empty sets 𝓣 and 𝓒.
1. For all credential pairs ![Credential pairs](cred-pairs.png) execute
[Proof Preparation](#proof-preparation).
1. Executes [hashing](#hashing) once.
1. For all credential pairs ![Credential pairs](cred-pairs.png) execute
[Final Preparation](#final-preparation).
1. Executes [Final Preparation](#final-preparation) once.

Verifier:
1. For all credential pairs ![Credential pairs](cred-pairs.png) executes
[Verification](#verification).
1. Executes [final hashing](#final-hashing) once.


#### Non-revocation proof
Holder:
1. Load issuer's public revocation key
![issuer's public revocation key](issuer-pub-rev-key.png).
1. Load the non-revocation credential
![non-revocation credential](non-rev-cred-full.png);
1. Obtain recent *V, acc* (from verifier, Sovrin link, or elsewhere).
1. Update ![non-revocation credential](non-rev-cred.png):

    ![Eq27](Eq27.png)

    Here *V<sub>old</sub>* is taken from  wit<sub>i</sub> and updated there.

1. Select random ![Eq28](Eq28.png);
1. Compute

    ![Eq29](Eq29.png)

    and adds these values to 𝓒.

1. Compute

    ![Eq30](Eq30.png)

    and adds these values to 𝓒.

1. Generate random ![Eq31](Eq31.png)

1. Compute

    ![T1 and T2](T1-T2.png)

    ![T3](T3.png)

    ![T4 through T8](T4-T8.png)

    and add these values to 𝓣.

#### Validity proof
Holder:
1. Generate a random 592-bit number ![widetilde{m_j}](widetilde{m_j}.png)
for each ![j \in \mathcal{A}_{\overline{r}}](j-in-A_r-bar.png).
1. For each credential ![C_p = (\{m_j\},A,e,v)](p-cred.png) and issuer's
public key ![pk_I](pk_I.png):
   1. Choose random 3152-bit r.
   1. Take ![$n,S$](n-S.png) from ![pk_I](pk_I.png) compute

        ![Eq32](Eq32.png)

        and add to 𝓒.

   1. Compute ![$e' \leftarrow e - 2^{596}$](e'-full.png).
   1. Generate random 456-bit number ![e-tilde](e-tilde.png).
   1. Generate random 3748-bit number ![v-tilde](v-tilde.png).
   1. Compute

    ![T \leftarrow (A')^{\widetilde{e}}\left(\prod_{j\in \mathcal{A}_{\overline{r}}} R_j^{\widetilde{m_j}}\right)(S^{\widetilde{v}})\pmod{n}](T-full.png)

    and add to 𝓣.

1. Load *Z,S* from issuer's public key.
1. For each predicate *p* where the operator * is one of
![>, \geq, <, \leq](inequality-symbols.png).
   1. Calculate ![delta](delta.png) such that:

        ![delta-cases](delta-cases.png)

   1. Calculate *a* such that:

        ![a cases](a-cases.png)

   1. Find (possibly by exhaustive search) ![u1 through u4](u1-u4.png) such that:

   ![delta equation](delta-full.png)

   1. Generate random 2128-bit numbers ![r1 through r_delta](r1-r_delta.png).
   1. Compute

    ![T equations](T-equations.png)
    and add these values to 𝓒 in the order ![T1 through T_delta](T1-T_delta.png).

   1. Generate random 592-bit numbers ![u1-tilde through u4-tilde](u1-u4-tilde.png).
   1. Generate random 672-bit numbers ![r1 through u_delta-tilde](r1-r_delta-tilde.png).
   1. Generate random 2787-bit number ![alpha-tilde](alpha-tilde.png)
   1. Compute

    ![T-bar and Q equations](T-bar-and-Q-equations.png)
    and add these values to 𝓣 in the order ![T1-bar through Tdelta-bar](T1-T_delta-bar.png).

#### Hashing

Holder computes challenge hash

![challenge hash](challenge-hash.png)

and sends *c<sub>H</sub>* to verifier.

#### Final preparation
Holder:
1. For non-revocation credential *C<sub>NR</sub>* compute:

    ![Eq33](Eq33.png)

    and add them to 𝓧.

1. For primary credential *C<sub>p</sub>* compute:

    ![Eq34](Eq34.png)

    The values ![Eq35](Eq35.png) are the *sub-proof* for credential
    *C<sub>p</sub>*.

1. For each predicate *p* compute:

    ![Eq36](Eq36.png)

    The values ![Eq37](Eq37.png) are the *sub-proof* for predicate *p*.


#### Sending
Holder sends (*c*,𝓧, *{Pr<sub>C</sub>}*, *{Pr<sub>p</sub>}*, 𝓒)  to the
verifier.

### Verification
For the credential pair (*C<sub>p</sub>, C<sub>NR</sub>*), verifier retrieves
relevant variables from 𝓧, *{Pr<sub>C</sub>}*, *{Pr<sub>p</sub>}*, 𝓒.

#### Non-revocation check
 
Verifier computes:

![Eq38](Eq38.png)

![Eq39](Eq39.png)

![Eq40](Eq40.png)

and adds these values to ![widehat{T}](widehat-T.png).

#### Validity
Verifier uses all issuer public key ![pk_I](pk_I.png) involved into the
credential generation and  the received ![Eq41](Eq41.png). He also uses revealed
![Revealed attributes](rev-attrib.png). He initiates
![widehat script T](widehat-script-T.png) as an empty set.

1. For each credential *C<sub>p</sub>*, take each sub-proof *Pr<sub>C</sub>* and
compute:

    ![Eq42](Eq42.png)

    Add ![widehat{T}](widehat-T.png) to ![widehat script T](widehat-script-T.png).

1. For each predicate *p*:

    ![Eq43](Eq43.png)

    ![Eq44](Eq44.png)

   1. Using *Pr<sub>p</sub>* and 𝓒 compute

    ![Eq45](Eq45.png)

    and add these values to
    ![widehat script T](widehat-script-T.png) in the order
    ![Eq46](Eq46.png).

#### Final hashing
1. Verifier computes

    ![Eq47](Eq47.png)

1. If ![c = c-widehat](c-eq-c-widehat.png) output VERIFIED else FAIL.


 

# Reference
[reference]: #reference
* [Indy-Crypto library][indy-crypto-github]
* [Camenisch-Lysyanskaya Signatures][CL-signatures]
* [Parirings-based Revocation][pairing-revocation]

[indy-crypto-github]: (https://github.com/hyperledger/indy-crypto/tree/master/libindy-crypto/src/cl)
[CL-signatures]: (https://groups.csail.mit.edu/cis/pubs/lysyanskaya/cl02b.pdf)
[pairing-revocation]: (https://eprint.iacr.org/2008/539.pdf)

# Drawbacks
[drawbacks]: #drawbacks

One drawback to this approach is that the signatures for the primary
credential are RSA-based. This results in keys and proofs that are much
larger than other signature schemes would require for similar levels of
expected security.

Another drawback is that revocation is handled using a different, elliptic-curve
based signature that allows the use of the more-efficient set-membership
proofs and accumulators required by that part of the protocol.

This dual-credential model provides all of the functionality required by
the protocol, but uses two different signature schemes to accomplish it,
one of which is based in outdated technology that requires very large
keys and proofs. Using two signature types results in a more unwieldy
protocol.

# Rationale and alternatives
[alternatives]: #alternatives

As this protocol is describes the current implementation, rationale and
alternatives point necessarily to potential future work.

The dual-credential model is not ideal, so possible future anonymous credential
schemes should strive to find a data structure and proof scheme that meets the
required characteristics of selective disclosure of attributes, predicate
proofs, and set membership proofs. It is outside of the scope of this document
to speculate on what form those structures and proofs may take.

# Prior art
[prior-art]: #prior-art

It is the understanding of the authors that few production quality
implementations of anonymous credential signature schemes exist.

Two implementations we are aware of are Idemix, implemented by IBM, and IRMA,
implemented by The Privacy by Design Foundation.

# Unresolved questions
[unresolved]: #unresolved-questions

This protocol is already implemented in indy-crypto.