- Name: Messaging Protocol
- Authors: Ryan West ryan.west@sovrin.org & Daniel Bluhm daniel.bluhm@sovrin.org
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

We present the scenario in which Alice and Bob wish to communicate. The following messages must be sent between them to establish a secure, persistent channel for communication:

1. Connection Offer
2. Connection Request
3. Connection Response
4. Bob's Acknowledgement
5. Alice's Acknowledgement

Each of these steps is explored in detail below.

### 1. Connection Offer

Alice first creates a **Connection Offer**, which gives Bob the necessary information to connect with her at a later point. This can be done in person using a QR code, or remotely using an encryption algorithm such as RSA. The Connection Offer includes an endpoint, which allows Bob to encrypt messages and provides a destination address. It also includes a nonce as a one-time validation.

```
con_off = {
    nonce
    ep@A: did or (url+vk)
    con_req vk?
}
```

**editing note**: If the offer is done remotely, then is an endpoint needed? Probably is.

An endpoint contains a URL to provide a destination and a verification key (aka public key, vk) to encrypt the message so that only the autorized person can decrypt it. However, an endpoint can instead include a DID, which will be looked up on the ledger to retrieve its corresponding url+vk.

### 2. Connection Request

When Bob receives Alice's connection offer, he can initiate a persistent connection with a **Connection Request**. Bob sends Alice a message containing the following:

```
con_req = {
	id: nonce  # from connection offer
	type: con_req
	content: {
		did@B:A
		vk@B:A
		ep@B
	}
}
``` 

The message id is the nonce received earlier and is proof that Bob received an authentic connection offer. In the message content, Bob sends a DID representing his side of the connection, so Alice can respond to him. He also sends a verification key so that Alice can send him encrypted messages, and his own endpoint information so Alice can anoncrypt the entire message.

Bob then anoncrypts the whole `con_req` message using Alice's provided verification key, so that only she can decrypt it.

**note** The inner message is not anoncrypted yet..

### 3. Connection Response

If Alice still wants to communicate with Bob, she sends a **Connection Response**.

```
con_res = {
    id: did@B:A
    type: con_res
    content:
        anoncrypt( {
            did: did@A:B
            vk: vk@A:B
            }, vk@B:A)
          }
```
Besides the type, there are a few differences from the connection request. Alice uses `did@B:A` that Bob sent her as the message `id`. She also anoncrypts the message content using Bob's verification key `vk@B:A`.

Similar to Bob's connection request, the message content includes Alice's pairwise `did` so that Bob has a persistent address to send messages to, and Alice's verification key **NOTE: so now Bob has 2 vks for Alice? Disambiguate this** so he can encrypt future messages to her.

The whole message is likewise anoncrypted using Bob's endpoint verification key.

### 4. Bob Acknowledges

When Bob receives the connection response, he sends an acknowledgement message back. At this point, Bob has Alice's verification key, DID, and endpoint, and can now send messages securely using `authcrypt`. But Alice needs to know that her `con_res` message was received successfully.

```
ack = {
    id: did@A:B
    type: ack
    content:
        authcrypt( {
            "success"
            }, vk@A:B, vk@B:A)
      }
anoncrypt(ack, ep vk@A)
```
Note that no new information is sent here except for a "success" string. However, the message content is authcrypted using both Alice's and Bob's verification key. Thus, this simple message serves as proof that Bob's channel  of communication to Alice is now computationally secure.

### 5. Alice Acknowledges

**Why do we need the second acknowledgement again?**

When Alice receives Bob's acknowledgement, she too needs to acknowledge that she received it correctly.

```
ack = {
    id: did@B:A
    type: ack
    content:
        authcrypt( {
            "success"
            }, vk@B:A, vk@A:B)
      }
anoncrypt(ack, ep vk@B)
```
This serves the same purpose as Bob's acknoledgement: now Bob knows that Alice knows that Bob's connection request was accepted.

(Now Bob knows that Alice knows that Bob knows what Alice knows.)


![alt text](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/ryanwest6/indy-hipe/master/text/messaging-protocol/establishing_connection.puml? "")

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
