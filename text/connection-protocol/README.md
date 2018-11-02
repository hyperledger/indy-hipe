- Name: Connection Protocol
- Authors: Ryan West ryan.west@sovrin.org, Daniel Bluhm daniel.bluhm@sovrin.org, Matthew Hailstone, Stephen Curran, Sam Curren <sam@sovrin.org>
- Start Date: 2018-6-29
- PR:
- Jira Issue: https://jira.hyperledger.org/browse/IA-18

# Summary
[summary]: #summary

This HIPE describes the protocol to establish connections between agents with the assumption that message transportation is [solved](https://github.com/hyperledger/indy-hipe/pull/21). We also describe how we will accommodate micro-ledger DIDs and how we will adapt this connection protocol when that work is complete.

# Motivation
[motivation]: #motivation

Indy agent developers want to create agents that are able to establish connections with each other and exchange secure information over those connections. For this to happen there must be a clear connection protocol.

# Tutorial
[tutorial]: #tutorial

We present the scenario in which Alice and Bob wish to communicate. The following interactions and messages that must be sent between them to establish a secure, persistent channel for communication:

1. [Invitation to connect](#1-invitation) (optional; dependent on scenario as explained later)
2. [Connection Request](#2-connection-request)
3. [Connection Response](#3-connection-response)
4. [Bob's Acknowledgement](#4-bobs-acknowledgement)
5. [Alice's Acknowledgement](#5-alices-acknowledgement)

Each of these steps is explored in detail below.

## 0. Invitation to Connect
[0-invitation]: #1-invitation

An invitation to connect may be implemented in any proprietary way. The result of an invitation to connect must result in the essential data necessary to initiate a [Connection Request](#2.-connection-request) message. An invitation to connect is an **out-of-band communication** and not a true agent [message type](https://github.com/hyperledger/indy-hipe/pull/19). The necessary data that an invitation to connect must result in is:
* endpoint did
* suggested label

The standard invitation format is a Base64URLEncoded json object, with the following fields

```javascript
b64urlencode({
	'did': 'A.did@B:A',
	'label': 'Alice'
})
```

The result is a block of invitation text that can be presented as plain text or as a QR code.

TODO: Check Digits?

IDEA: emoji hash for verification?


#### Example
Alice first creates an invitation to connect, which gives Bob the necessary information to initiate a connect request with her. This can be done in person (perhaps using a QR code), or remotely using a previously established secure connection.

After receiving Alice's invitation to connect, Bob may generate the DID and keys that will be used in the Alice to Bob (`A:B`) relationship and create a connection request message.


## 1. Connection Request
[1-connection-request]: #2-connection-request

The connection request message is used to communicate the DID and Verification key generated for a pairwise relationship from one of the connecting parties to the other.

#### Example
When Bob receives Alice's invitation to connect, he initiates establishing the connection by sending a connection request message. Bob sends Alice a message containing the following:

```
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/request",
  "DID": "B.did@B:A",
  "label": "Bob"
}
```
#### Attributes
* The `@type` attribute is a required string value that denotes that the received message is a connection request.
* The `DID` indicates the DID of the user requesting the connection.
* The `label` attribute provides a suggested label for the connection. This allows the user to tell multiple connection offers apart. This is not a trusted attribute.

#### Alice Receives the Request
After receiving the connection request, Alice resolves the DID,  and then stores the resulting verification key, and endpoint information in her wallet. Alice then prepares to send a connection response be generating her DID and key for the relationship. 

She writes the DID to the ledger, along with the key and endpoint information. She then prepares the response

## 2. Connection Response
[2-connection-response]: #3-connection-response

The connection response message is used to confirm the connection. This message is required in the flow, as it will be needed in the future for micro-ledger initialization.

#### Example
If Alice still wants to communicate with Bob, she sends a connection response.

```
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/response",
  "result: "accepted || rejected"
}
```

#### Attributes

* The `@type` attribute is a required string value that denotes that the received message is a connection request.
* The result attribute is a required string value and denotes success or failure of the connection request. 

#### Connection Established
The connection between Alice and Bob is now established and any subsequent messages in the relationship can be auth-encrypted from the sender to the receiver. The remaining steps of the connection process are intended to verify not only connectivity but also that the key exchange was successful.


The next step of establishing a connection could be exchanging credentials to prove both Alice's and Bob's identities.





# Diagram

![puml diagram](establishing_connection.svg)

# Micro-ledger Connections

Ongoing work with micro-ledgers will allow for pairwise connections without any record on a public ledger. When this work is finished, this connection protocol will need to be expanded to allow the bootstrapping of a connection. We anticipate expanding this spec to allow for DIDs in the transaction to be replaced by a key, endpoint, and routing information. The flow of of an optional invitation, a request, and a response will remain the same.

# Reference
[reference]: #reference

* https://docs.google.com/document/d/1mRLPOK4VmU9YYdxHJSxgqBp19gNh3fT7Qk4Q069VPY8/edit#heading=h.7sxkr7hbou5i
* [Agent to Agent Communication Video](https://drive.google.com/file/d/1PHAy8dMefZG9JNg87Zi33SfKkZvUvXvx/view)
* [Agent to Agent Communication Presentation](https://docs.google.com/presentation/d/1H7KKccqYB-2l8iknnSlGt7T_sBPLb9rfTkL-waSCux0/edit#slide=id.p)

# Drawbacks
[drawbacks]: #drawbacks

* DIDs be placed on the public ledger. This will be improved with micro-ledger work.
* Public invitations (say, a slide at the end of a presentation) all use the same DID. This is not a problem for public institutions, and only provides a minor increase in correlation over sharing an endpoint, key, and routing information.

# Rationale and alternatives
[alternatives]: #alternatives

- The acknowledgement steps are not necessarily vital to the connection process as all the necessary keys and DIDs needed for secure communication are transmitted to both parties by the end of the connection response step.

# Prior art
[prior-art]: #prior-art

- This process is similar to other key exchange protocols.

# Unresolved questions
[unresolved]: #unresolved-questions

- This HIPE makes some assumptions about the underlying secure transport protocol in the absence of an official HIPE detailing the specifics of that protocol. In general, this HIPE assumes that message transportation has been solved.

- Is the `negotiate_msg` flow outlined [here](https://github.com/sovrin-foundation/ssi-protocol/tree/master/flow/std/negotiate_msg) applicable and should terminology used here be altered to match those used in this flow?