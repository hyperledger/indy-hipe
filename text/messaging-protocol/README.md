- Name: Messaging Protocol
- Author: Daniel Bluhm & Ryan West ryan.west@sovrin.org
- Start Date: 2018-6-29
- PR: 
- Jira Issue: 

# Summary
[summary]: #summary

This HIPE describes the protocol to be used to establish a connection with and send messages between agents. This is based on the Indy Core Message Structure HIPE.

# Motivation
[motivation]: #motivation

If the goal is to allow any agent to commmunicate with any other agent, then a  standard messaging protocol is needed.

# Tutorial
[tutorial]: #tutorial

We present the scenario in which Alice and Bob wish to communicate. 

###1. Connection Offer

Alice first creates a **Connection Offer**, which gives Bob the necessary information to connect with her at a later point. This can be done in person using a QR code, or remotely using an encryption algorithm such as RSA. The Connection Offer includes an endpoint, which allows Bob to encrypt messages and provides a destination address. It also includes a nonce as a one-time validation.

**editing note**: If the offer is done remotely, then is an endpoint needed? Probably is.

An endpoint contains a URL to provide a destination and a verification key (aka public key, vk) to encrypt the message so that only the autorized person can decrypt it. However, an endpoint can instead include a DID, which will be looked up on the ledger to retrieve its corresponding url+vk.

###2. Connection Request

When Bob receives Alice's Connection Offer, he can initiate a line of communication with a **Connection Request**. This is done with 



![alt text](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/ryanwest6/indy-hipe/master/text/messaging-protocol/establishing_connection.puml "")

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

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
