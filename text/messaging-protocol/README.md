- Name: Messaging Protocol
- Authors: Ryan West ryan.west@sovrin.org & Daniel Bluhm daniel.bluhm@sovrin.org
- Start Date: 2018-6-29
- PR: 
- Jira Issue: 

# Summary
[summary]: #summary

This HIPE describes the protocol to be used to establish a connection with and send messages between agents. Connections allow establishing relationships between identities. This is based on the Indy Core Message Structure HIPE.

# Motivation
[motivation]: #motivation

If the goal is to establish secure relationships between identities, then a  standard messaging protocol is needed.

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

The connection offer message is used to disclose the endpoint needed to exchange a connection request message. If the Endpoint DID is already known or discoverable on the ledger, *the connection offer is not necessary*. If the Endpoint DID is not on or discoverable on the ledger, then the connection offer message is a way to communicate the necessary information to an agent in order to establish a connection/relationship.

Alice first creates a connection offer, which gives Bob the necessary information to connect with her at a later point. This can be done in person (perhaps using a QR code), or remotely using previously established secure connection. The Connection Offer includes an endpoint, which allows Bob to encrypt messages and provides a destination address. 

```
con_off = {
    "id": offer_nonce
    "type": "urn:indy:sov:agent:message_type:sovrin.org/connection/1.0/connection_offer"
    "content": {
	    "ep": A.ep.did | (A.ep.url+A.ep.vk)
    }
}
```

* The `id` attribute of the base message is required and is a nonce used to correlate the connection request. The offer nonce is necessarily used when implementing an agency in order to route the connection request to the intended agent/wallet recipient.
* The `type` attribute of the base message is required and MUST be the value: urn:indy:sov:agent:message_type:sovrin.org/connection/1.0/connection_offer
* An endpoint `ep` contains a URL (or other location, if not using http/https) to provide a destination and a verification key (aka public key, vk) to encrypt the message so that only the autorized person can decrypt it. However, an endpoint can instead include a DID, which will be looked up on the ledger to retrieve its corresponding url+vk. Alice can use a DID so Bob can retrieve her url+vk on the Sovrin ledger, or directly share a url+vk if she prefers not to use the ledger.

### 2. Connection Request

The connection request message is used to provide a DID to an agent in establishing a connection. The generated DID will eventually become associated in a pairwise DID relationship in both participant’s wallets.

When Bob receives Alice's connection offer, he can initiate a relationship with a connection request. Bob sends Alice a message containing the following:

```
con_req = {  # anoncrypted using A.ep.vk
	"id": offer_nonce (optional)
	"to": A.did@A (public, optional)
	"type": "urn:indy:sov:agent:message_type:sovrin.org/connection/1.0/connection_request"
	"content": {  # plaintext (cannot yet be anoncrypted)
		"did": B.did@B:A
		"vk": B.vk@B:A
		"ep": B.ep
	}
}
``` 

* The `id` is optional and is the nonce received in the connection offer, proving that Bob received an authentic connection offer. This attribute is required if Bob did not / could not use Alice's public DID on the ledger.
* The `to` attribute is optional and contains Alice's public DID if she chose to make it available on the ledger. The connection response step is not required if this is the case, as Bob can obtain Alice's endpoint information with a ledger lookup.
* The `type` attribute of the base message is required and MUST be the value: urn:indy:sov:agent:message_type:sovrin.org/connection/1.0/connection_request
* The `content` attribute of the base message is required, is not encrypted, and is an object containing the following attributes:
  * The `did` attribute is required and is a DID created by the sender of the connection message.
  * A new, connection-specific verification key `vk` is required so that Alice can send Bob authcrypted messages
  * Bob's own endpoint information `ep` is required, so Alice can anoncrypt the entire message. **make this more clear**

Bob then anoncrypts the whole `con_req` message using Alice's endpoint verification key, so that only she can decrypt it.

### 3. Connection Response

The connection response message is used to respond to a connection request message and provide a DID to the sender of the connection request message to be used as a pairwise DID in an established connection/relationship.

If Alice still wants to communicate with Bob, she sends a connection response. 
```
con_res = { # anoncrypted using B.ep.vk
    "to": B.did@B:A,
    "type": "urn:indy:sov:agent:message_type:sovrin.org/connection/1.0/connection_response",
    "content": {  # anoncrypted using B.vk@B:A
            "did": A.did@A:B,
            "vk": A.vk@A:B
    }
}
```
* The `to` attribute is required and is `A.did@B:A`, the DID that Bob sent Alice. It is used to send the message to the correct destination.
* The `type` attribute of the base message is required and MUST be the value: urn:indy:sov:agent:message_type:sovrin.org/connection/1.0/connection_response
* `content` is anoncrypted using Bob's new verification key `B.vk@B:A`. It includes:
  * The `did` attribute is required and is a DID that Alice created for the Bob-to-Alice relationship. This is used in creating a pairwise DID with the DID sent in the connection request message.
  * `vk` is a required, connection-specific verification key, necessary so that Bob can send Alice authcrypted messages


The whole message is likewise anoncrypted using Bob's endpoint verification key. From this point forward, all inner message's `content` is authcrypted, and 

### 4. Bob's Acknowledgement

The connection acknowledgement message is used to confirm that a connection/relationship has been established. The connection acknowledgement message also contains an auth-encrypted message now possible between pairwise DIDs established on each side of the connection. This auth-encrypted pattern is important as a foundation for other message types to be designed requiring privacy and protected data.

When Bob receives the connection response, he sends an acknowledgement message back. At this point, Bob has Alice's new (owner) verification key, DID, and endpoint (with its own verification key and url), and can now send messages securely using `authcrypt`. But Alice needs to know that her `con_res` message was received successfully.

```
ack = {  # anoncrypted using A.ep.vk
    "to": A.did@A:B
    "type": "urn:indy:sov:agent:message_type:sovrin.org/connection/1.0/"
    "content": {  # authcrypted using A.vk@A:B and B.vk@B:A
    	str: "success" //valid json?
    }
}
```
* The `to` attribute of the base message is required and is the DID of the sender of the connection acknowledgement message in the pairwise DID established connection/relationship.
* The `type` attribute of the base message MUST be the value: urn:indy:sov:agent:message_type:sovrin.org/connection/1.0/connection_acknowledgement
* The `content` is the simple string value "success".

Note that no new information is sent here except for a "success" string. However, the message content is authcrypted using both Alice's and Bob's verification key. Thus, this simple message serves as proof that Bob's channel  of communication to Alice is now computationally secure.

### 5. Alice's Acknowledgement

When Alice receives Bob's acknowledgement, she too needs to acknowledge that she received it correctly. Bob does not yet know that the connection is secure until Alice sends this message.

```
ack = { # anoncrypted using A.ep.vk
    "id": B.did@B:A
    "type": "urn:indy:sov:agent:message_type:sovrin.org/connection/1.0/"
    "content": { # authcrypted using B.vk@B:A and A.vk@A:B
        	"success"
    }
}
```

This serves the same purpose as Bob's acknowledgement: now Bob knows that Alice knows that Bob's connection request was accepted. At this point, they have established a computationally secure relationsihp.

The next step would likely be to exchange credentials to prove identity.



![alt text](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/ryanwest6/indy-hipe/master/text/messaging-protocol/establishing_connection.puml? "")

# Reference
[reference]: #reference

There are 4 verification keys total between Alice and Bob. Alice has a public endpoint verification key, which is used by Bob to anoncrypt the entire message. Alice also generates a new verification key specific to her connection with Bob. Bob likewise has a public endpoint verification key and a connection-specific verification key.


* Add anoncrypt and authcrypt definition/link
* Add Daniel Hardman's Agent2agent video

* authcrypt/anoncrypt do not preserve sender and receiver anonymity as explained by nage. Do we ignore this for this layer of abstraction?
* 

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


**note** The inner message is not anoncrypted yet..
con_off vk for con_req? //remove

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
