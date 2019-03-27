# HIPE 00??: Introductions 1.0

- Authors: Daniel Hardman, Sam Curren, Stephen Curran, Tobias Looker
- Start Date: 2019-03-27
- PR: (leave this empty)
- Jira Issue: (leave this empty)

## Summary

Describes how a go-between can introduce two parties that
it already knows, but that do not know each other.

## Motivation
[motivation]: #motivation

Introductions are a fundamental activity in human relationships. They allow
us to bootstrap contact information and trust. We need a standard way to
do introductions in an SSI ecosystem, and it needs to be flexible, secure,
privacy-respecting, and well documented.

## Tutorial
[tutorial]: #tutorial

### Name and Version

This is the Introductions 1.0 protocol. It is uniquely identified by the URI:

    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/introductions/1.0"

### Key Concepts

The protocol targets scenarios like the following:

>Alice has already established a pairwise connection with either Bob or
Carol using [Connection Protocol 1.0](https://github.com/hyperledger/indy-hipe/blob/master/text/0031-connection-protocol/README.md)
or something like it. Alice has either an SSI-style connection or some
other type of connection (e.g., business:customer) with the other party.
Alice believes that Bob and Carol do not know
each other, and she wants to introduce them in a way that gives them
an opportunity to form a relationship.

![scenario diagram](scenario.png)

This use case is broader than it may sound. Any of the parties can be an
organization or thing instead of a person. Bob and Carol may actually know
each other already, without Alice realizing it. The introduction may be
rejected. It may create a new pairwise relationship between Bob and Carol
that is entirely invisible to Alice. Or it may create an n-wise relationship
in which Alice, Bob, and Carol know one another by the same identifiers.
 

## Reference
[reference]: #reference

Provide guidance for implementers, procedures to inform testing,
interface definitions, formal function prototypes, error codes,
diagrams, and other technical details that might be looked up.
Strive to guarantee that:

- Interactions with other features are clear.
- Implementation trajectory is well defined.
- Corner cases are dissected by example.

## Drawbacks
[drawbacks]: #drawbacks

Why should we *not* do this?

## Rationale and alternatives
[alternatives]: #alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not
choosing them?
- What is the impact of not doing this?

## Prior art
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

## Unresolved questions
[unresolved]: #unresolved-questions

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
