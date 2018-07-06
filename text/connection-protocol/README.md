- Name: Messaging Protocol
- Authors: Ryan West ryan.west@sovrin.org & Daniel Bluhm daniel.bluhm@sovrin.org
- Start Date: 2018-6-29
- PR:
- Jira Issue: https://jira.hyperledger.org/browse/IA-18

# Summary
[summary]: #summary

This HIPE describes the protocol to establish connections between agents.

# Motivation
[motivation]: #motivation

Indy agent developers want to create agents that are able to establish connections with each other and exchange secure
information over those connections. For this to happen there must be a clear connection protocol.

# Tutorial
[tutorial]: #tutorial

We present the scenario in which Alice and Bob wish to communicate. The following messages must be sent between them to
establish a secure, persistent channel for communication:

1. Connection Offer (optional; dependent on scenario as explained later)
2. Connection Request
3. Connection Response
4. Bob's Acknowledgement
5. Alice's Acknowledgement

Each of these steps is explored in detail below.

### 1. Connection Offer
[1-connection-offer]: #1-connection-offer

The connection offer message is **out-of-band communication** used to disclose the endpoint needed to exchange a
connection request message. If the Endpoint DID is already known or discoverable on the ledger, *the connection offer is
not necessary*. If the Endpoint DID is not on or discoverable on the ledger, then the connection offer message is a way
to communicate the necessary information to an agent in order to establish a connection/relationship.

**Example:** Alice first creates a connection offer, which gives Bob the necessary information to connect with her at a
later point. This can be done in person (perhaps using a QR code), or remotely using a previously established secure
connection. The Connection Offer message contains the following information:

```
{
    "id": offer_nonce
    "type": connection_offer
    "content": {
        "endpoint": {
            "did": A.endpoint.did
            --- or ---
            "uri": A.endpoint.uri
            "verkey": A.endpoint.vk
        }
    }
}
```

#### Attributes

* The `id` attribute of the base message is required and is a nonce used to correlate the connection request.
* The `type` attribute is a required string value (following the structure outlined by a future HIPE on message
  types) and denotes that the received message is a connection offer.
* The `endpoint` attribute is a structure that contains either `uri` and `verkey` or just a DID that will be resolved to
  a corresponding `uri` and `verkey` attributes from the public ledger.
    * `did`: public did that can resolve to a URI and verification key.
    * `uri`: URI of the endpoint to which a connection request and future messages will be sent.
    * `verkey`: verification key used to encrypt traffic to this endpoint.

#### Bob Receives the Offer
After receiving and accepting Alice's offer to connect, Bob generates the DID and keys that will be used in the Alice to
Bob (`A:B`) relationship and creates a connection request message.


### 2. Connection Request
[2-connection-request]: #2-connection-request

The connection request message is used to communicate the DID and Verification key generated for a pairwise relationship
from one of the connecting parties to the other.

**Example:** When Bob receives Alice's connection offer, he reciprocates in the connection establishment by responding
with a connection request. Bob sends Alice a message containing the following:

```
{
    "id": offer_nonce (optional; dependent on scenario)
    "type": connection_request
    "content": {
        "did": B.did@B:A
        "verkey": B.vk@B:A
        "endpoint": B.endpoint
    }
}
```

The entirety of this message (and all other messages in the connection process) is anon-encrypted using the endpoint
information that Alice sent in the connection offer, ensuring that all information is encrypted in transport and no
correlateble data can be leaked.  At this point, not enough information has been exchanged for Bob to be able to encrypt
the content for Alice only in the context of their relationship (Bob does not yet have a verification key for Alice in
the Alice to Bob relationship).

#### Attributes

* The `id` is required when a connection offer was used to initiate the connection establishment process and is the
  nonce received in the connection offer. If the connection request was sent without an offer (as in the case of one
  party having a discoverable public DID written to the ledger), this attribute is not required.
* The `type` attribute is a required string value (following the structure outlined by a future HIPE on message
  types) and denotes that the received message is a connection request.
* The `content` attribute of the base message is required, is not encrypted, and is an object containing the following
  attributes:
    * `did`: the DID created by the sender for the relationship.
    * `verkey`: the verification key created by the sender for the relationship. **This is not the same as the
      verification key used to encrypt messages in transport.**
    * `endpoint`: the endpoint that the sender receives messages on. This attribute is an object like the `endpoint`
      object described in [Connection Offer](#1-connection-offer). To be exact, `endpoint` will contain either a `uri` and
      `verkey` **or** a `did` used to resolve the `uri` and `verkey` from the ledger.

#### Alice Receives the Request
After receiving the connection request, Alice stores the DID, verification key, and endpoint information sent by Bob in
here wallet. Alice then prepares to send a Connection response be generating her DID and keys for the relationship.

### 3. Connection Response
[3-connection-response]: #3-connection-response

The connection response message is used to communicate the DID and Verification key generated for a pairwise relationship
from the remaining connecting party to the other.

**Example:** If Alice still wants to communicate with Bob, she sends a connection response.

```
{
    "to": A.did@B:A,
    "type": connection_response,
    "content": {  # anon-encrypted using B.vk@B:A
            "did": A.did@A:B,
            "verkey": A.vk@A:B
    }
}
```

The entirety of this message is anon-encrypted using Bob's endpoint verification key and sent to the endpoint URI. The
inner content of the message can also now be encrypted using Bob's verification key for the Alice to Bob
relationship.

#### Attributes

* The `to` attribute is required and is the DID sent in the connection request message from the other connecting party.
* The `type` attribute is a required string value (following the structure outlined by a future HIPE on message
  types) and denotes that the received message is a connection response.
* `content` is anon-encrypted using the receiver's verification key sent in the connection request message. It includes:
    * The `did` attribute is required and is the DID created by the sender for the relationship.
    * `verkey` is required and is the verification key created by the sender for the relationship.

#### Connection Established
The connection between Alice and Bob is now established and any subsequent messages in the relationship can be
auth-encrypted from the sender to the receiver. The remaining steps of the connection process are intended to verify not
only connectivity but also that the key exchange was successful.

### 4. Bob's Acknowledgement

The connection acknowledgement message is used to confirm that all DIDs and keys have been correctly exchanged between
the connecting parties. The connection acknowledgement message contains an auth-encrypted message that can now be
decrypted and verified by the receiver.

**Example:** When Bob receives the connection response, he sends an acknowledgement message back. At this point, Bob has
Alice's verification key for the Alice to Bob relationship, Alice's DID for the Alice to Bob relationship, and endpoint
(with its own verification key and URI), and can now send messages securely using `auth-crypt`. However, Alice needs to
know that her connection response message was received successfully.

```
{
    "to": A.did@A:B
    "type": message_acknowledgement
    "message": "success" #auth-encrypted using A.vk@A:B and B.vk@B:A
}
```

The entirety of this message is anon-encrypted using Alice's endpoint verification key and sent to Alice's endpoint.
The inner message is the string "success" auth-encrypted for Alice from Bob using the keys now established for the
relationship by both parties.

#### Attributes

* The `to` attribute of the base message is required and is the DID of the receiver of the Acknowledgment message.
* The `type` attribute is a required string value (following the structure outlined by a future HIPE on message
  types) and denotes that the received message is a connection acknowledgment.
* The `message` is the encrypted string "success".

It is valuable to note that no new information is sent here except for a "success" string. However, the message content
is auth-encrypted using both Alice's and Bob's verification key. Thus, this simple message serves as proof that the
messages being exchanged between Alice and Bob are computationally secure.

### 5. Alice's Acknowledgement

When Alice receives Bob's acknowledgement, she too needs to acknowledge that she received it correctly. Bob does not yet
know that the connection is secure until Alice sends this message.

```
{ # anon-encrypted using B.endpoint.vk
    "id": B.did@B:A
    "type": message_acknowledgement
    "message": "success" #auth-encrypted using B.vk@B:A and A.vk@A:B
}
```

This serves the same purpose as Bob's acknowledgement: now Bob knows that Alice knows that Bob's connection request was
accepted. At this point, they have established a computationally secure relationship.

The next step of establishing a connection could be exchanging credentials to prove both Alice's and Bob's identities.
Details on this protocol will be in future HIPEs.

# Diagram
![puml diagram](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/ryanwest6/indy-hipe/master/text/messaging-protocol/establishing_connection.puml? "")

# Reference
[reference]: #reference

* https://docs.google.com/document/d/1mRLPOK4VmU9YYdxHJSxgqBp19gNh3fT7Qk4Q069VPY8/edit#heading=h.7sxkr7hbou5i

# Drawbacks
[drawbacks]: #drawbacks

* In a connection request message, because the pairwise DIDs have not yet been created, Bob cannot auth-encrypt the
  content of his message. Thus, if an agency were to decrypt the overall message and forward it to Alice's edge agent,
  the agency would see the connection request's content in plaintext. This could potentially be a security concern.
  However, we have chosen to discuss agents and agencies in a future hipe rather than combine them.

# Rationale and alternatives
[alternatives]: #alternatives

- The acknowledgement steps are not technically necessary, as both pairwise DIDs and verification keys exchanged after
  the connection response.

# Prior art
[prior-art]: #prior-art

* [Agent to Agent Communication Video](https://drive.google.com/file/d/1PHAy8dMefZG9JNg87Zi33SfKkZvUvXvx/view)
* [Agent to Agent Communication Presentation](https://docs.google.com/presentation/d/1H7KKccqYB-2l8iknnSlGt7T_sBPLb9rfTkL-waSCux0/edit#slide=id.p)


# Unresolved questions
[unresolved]: #unresolved-questions

- In connection offer should content structure be collapsed into the main structure like this?
    ```
    {
        "id": offer_nonce
        "type": connection_offer
        "endpoint": {
            "did": A.endpoint.did
            --- or ---
            "uri": A.endpoint.url
            "verkey": A.endpoint.vk
        }
    }
    ```

- Is the `negotiate_msg` flow outlined
  [here](https://github.com/sovrin-foundation/ssi-protocol/tree/master/flow/std/negotiate_msg) applicable and should
  terminology used here be altered to match those used in this flow?
