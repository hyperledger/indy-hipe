- Name: wallets
- Author: Daniel Hardman, Darko Kulic, Vyacheslav Gudkov
- Start Date: 2018-05-22
- PR: (leave this empty)
- Jira Issue: (leave this empty)

# Summary
[summary]: #summary

Specify the external interfaces of identity wallets in the Indy ecosystem, as well
as some background concepts, theory, tradeoffs, and internal implementation guidelines.

![identity wallet](identity-wallet.png)

# Motivation
[motivation]: #motivation

Wallets are a familiar component metaphor that SSI has adopted from the world of
cryptocurrencies. The translation isn't perfect, though; crypto wallets have only a
subset of the features that an identity wallet needs. This causes problems, as
coders may approach wallets in Indy with assumptions that are more narrow than
our actual design target.

Since wallets are a major vector for hacking and cybersecurity issues, casual or
fuzzy wallet requirements are a recipe for frustration or disaster. Divergent
and substandard implementations could undermine security more broadly. This
argues for as much design guidance as possible. 

Wallets are also a unit of identity portability--if an identity owner doesn't
like how her software is working, she should be able to exercise her self-
sovereignty by taking the contents of her wallet to a new service. This implies
that wallets need certain types of interoperability in the ecosystem, if they
are to avoid vendor lock-in.

All of these reasons--to clarify design scope, to provide uniform high security, and
to guarantee interop--suggest that we need a formal HIIP to document wallet
architecture. 

# Tutorial
[tutorial]: #tutorial

### What Is an Identity Wallet?

Informally, an __identity wallet__ (not just "wallet") is a digital container
for data that's needed _to control a self-sovereign identity_. We borrow this
metaphor from physical wallets:

![physical wallet](physical-wallet.png)

Notice that we do not carry around in a physical wallet every document, key, card,
photo, piece of currency, or credential that we possess. A wallet is a mechanism
of _convenient control_, not an exhaustive repository. A wallet is _portable_.
A wallet is _worth safeguarding_. Good wallets are _organized so we can find
things easily_. A wallet has a _physical location_.

What does suggest about _identity wallets_?

### Types of Sovereign Data

Before we give a definitive answer to that question, let's take a detour for a
moment to consider digital data. Actors in a self-sovereign identity ecosystem
may own or control many different types of data:

* encryption and signing keys
* payment keys
* link secrets
* PII about themselves or others
* credentials
* personal documents (e.g., last year's tax filing, journal, love letters)
* digital breadcrumbs (e.g., purchase history)
* photos and videos
* receipts
* health records

...and much more. Different subsets of data may be worthy of different protection efforts:

![the data risk continuum](risk-continuum.png) 

The data can also show huge variety in its size and in its richness:

![data size and richness](size-richness.png)

Because of the sensitivity difference, the size and richness difference, joint
ownership, and different needs for access in different circumstances, we may
store digital data in many different locations, with different backup regimes,
different levels of security, and different cost profiles.

### What An Identity Wallet is NOT

##### Not a Vault
This variety suggests that an __identity wallet__ as a loose grab-bag of all our
digital "stuff" will give us a poor design. We won't be able to make good
tradeoffs that satisfy everybody; some will want rigorous, optimized search;
others will want to minimize storage footprint; others will be concerned about
maximizing security.

We reserve the term __vault__ to refer to this complex collection of all an
identity owner's data:

![not a vault](not-vault.png)

Note that a vault can _contain_ an identity wallet. A vault is an important
construct, and we may want to formalize its interface. But that is not the
subject of this spec.

##### Not A Cryptocurrency Wallet

The cryptocurrency community has popularized the term "wallet"--and because
identity wallets share both high-tech crypto and a need to store secrets with
crypto wallets, it is tempting to equate these two concepts. However, an
identity wallet can hold more than just cryptocurrency keys, just as a physical
wallet can hold more than paper currency. Also, identity wallets may need to
manage hundreds of millions of relationships (in the case of large organizations),
whereas most crypto wallets manage a small number of keys:

![not a crypto wallet](not-crypto-wallet.png)

##### Not a GUI

As used in this spec, an identity wallet is not a visible application, but
rather a data store. Although user interfaces (superb ones!) can and should
be layered on top of wallets, the wallet itself consists of a container and
its data; its friendly face is a separate construct. We may casually refer
to an application as a "wallet", but what we really mean is that the
application provides an interface to the underlying wallet.

### Managing Secrets

### Wallet Encryption

### Wallet Query Language

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
- What other designs have been considered and what is the rationale for not choosing them?
- What is the impact of not doing this?

# Prior art
[prior-art]: #prior-art

Discuss prior art, both the good and the bad, in relation to this proposal.
A few examples of what this can include are:

- Does this feature exist in other SSI ecosystems and what experience have their community had?
- For other teams: What lessons can we learn from other attempts?
- Papers: Are there any published papers or great posts that discuss this? If you have some relevant papers to refer to, this can serve as a more detailed theoretical background.

This section is intended to encourage you as an author to think about the lessons from other 
implementers, provide readers of your RFC with a fuller picture.
If there is no prior art, that is fine - your ideas are interesting to us whether they are brand new or if it is an adaptation from other languages.

Note that while precedent set by other ecosystems is some motivation, it does not on its own motivate an RFC.
Please also take into consideration that Indy sometimes intentionally diverges from common identity features.

# Unresolved questions
[unresolved]: #unresolved-questions

- What parts of the design do you expect to resolve through the RFC process before this gets merged?
- What parts of the design do you expect to resolve through the implementation of this feature before stabilization?
- What related issues do you consider out of scope for this RFC that could be addressed in the future independently of the solution that comes out of this RFC?
