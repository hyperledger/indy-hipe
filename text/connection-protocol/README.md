- Name: Connection Protocol
- Authors: Ryan West ryan.west@sovrin.org, Daniel Bluhm daniel.bluhm@sovrin.org, Matthew Hailstone, Stephen Curran, Sam Curren <sam@sovrin.org>
- Start Date: 2018-6-29
- PR:
- Jira Issue: https://jira.hyperledger.org/browse/IA-18

# Summary
[summary]: #summary

This HIPE describes the protocol to establish connections between agents with the assumption that message transportation is [solved](https://github.com/hyperledger/indy-hipe/pull/21). We assume that the DIDs exchanged are recorded on a public ledger. We also describe how we will accommodate Peer DIDs and how we will adapt this connection protocol when that work is complete.

# Motivation
[motivation]: #motivation

Indy agent developers want to create agents that are able to establish connections with each other and exchange secure information over those connections. For this to happen there must be a clear connection protocol.

# Tutorial
[tutorial]: #tutorial

We will explain how a connection is established, with the roles, states, and messages required.

### Roles

Connection uses two roles: __inviter__ and __invitee__.

The _inviter_ is the party that initiates the protocol with an `invitation` message. This party
must already have an agent and be capable of creating DIDs and endpoints
at which they are prepared to interact. It is desirable but not strictly required that inviters
have the ability to help the invitee with the process and/or costs associated with acquiring
an agent capable of participating in the ecosystem. For example, inviters may often be sponsoring institutions. The inviter sends a `connection-response` message at the end of the _share_ phase.

The _invitee_ has less preconditions; the only requirement is that this party be capable of
receiving invitations over traditional communication channels of some type, and acting on
it in a way that leads to successful interaction. The invitee sends a `connection-request` message at the beginning of the _share_ phase.

In cases where both parties already possess SSI capabilities, deciding who plays the role of inviter and invitee might be a casual matter of whose phone is handier.

### States

#### null
No connection exists or is in progress
#### invitation_shared
The invitation has been shared with the intended _invitee_(s), and they have not yet sent a _connection_request_.
#### requested
A _connection_request_ has been sent by the _invitee_ to the _inviter_ based on the information in the _invitation_. 
#### responded
A _connection_response_ has been sent by the _inviter_ to the _invitee_ based on the information in the _connection_request_.
#### complete
The invitation is valid.

TODO: Timeout or Error States

### Flow Overview
The _inviter_ gives provisional connection information to the _invitee_. 
The _invitee_ uses provisional information to send a DID and DIDDocument to the _inviter_.
The _inviter_ uses sent DIDDocument information to send a DID and DIDDocument to the _invitee_.

## 0. Invitation to Connect
[0-invitation]: #1-invitation

An invitation to connect may be transferred using any method that can reliably transmit text. The result  must be the essential data necessary to initiate a [Connection Request](#2.-connection-request) message. An connection invitation is a agent message with agent plaintext format, but is an **out-of-band communication** and therefore not communicated using wire level encoding or encryption. The necessary data that an invitation to connect must result in is:
*  suggested label
*  publicly resolvable did

  OR

* suggested label
* peer did
* key
* endpoint
  This information is used to create a provisional connection to the _inviter_. That connection will be made complete in the `connection_response` message.

The _inviter_ will either use an existing invitation DID, or provision a new one according to the did method spec. They will then create the invitation message in one of the following forms.

Invitation Message with Public Invitation DID:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
    "label": "Alice",
    "did": "did:sov:QmWbsNYhMrjHiqZDTUTEJs"
}
```
Invitation Message with Peer DID:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
    "label": "Alice",
    "did": "did:peer:oiSqsNYhMrjHiqZDTUthsw",
    "key": "8HH5gYEeNc3z7PYXmd54d4x6qAfCNrqQqEB3nS7Zfu7K",
    "endpoint": "https://example.com/endpoint"
}
```
##### Agency Endpoint

If the endpoint listed in the DID Doc of a Public DID, or present in the invitation of a peer DID, is not a URI but a DID itself, that DID refers to an Agency.

In that case, any messages must utilize a Forward Message, where the main message is wrapped in a forward request to the agency. For more information about message forwarding and routing, see the ??? HIPE.

#### Standard Invitation Encoding

Using a standard invitation encoding allows for easier interoperability between multiple projects and software platforms.

The standard invitation format is a URL with a Base64URLEncoded json object as a query parameter. Using a URL allows mobile apps to register as handlers for the URL for users who already have a Wallet App installed, and new users can be provided with getting started instructions.

The Invitation URL format is as follows, with some elements described below:

```text
https://<domain>/<path>?c_i=<invitationstring>
```

`<domain>` and `<path>` should be kept as short as possible, and the full URL should return human readable instructions when loaded in a browser. This is intended to aid new users. Additional path elements or query parameters are allowed, and can be leveraged to provide coupons or other promise of payment for new users. 

The `<invitationstring>` is an agent plaintext message (not a wire level message) that has been base64 url encoded. For brevity, the json encoding should minimize unnecessary white space.

```javascript
invitation_string = b64urlencode(<invitation_message>)
```

#### Invitation URL Encoding

During encoding, whitespace from the json string should be eliminated to keep the resulting invitation string as short as possible.
```text
eydAdHlwZSc6J2RpZDpzb3Y6QnpDYnNOWWhNcmpIaXFaRFRVQVNIZztzcGVjL2Nvbm5lY3Rpb25zLzEuMC9pbnZpdGF0aW9uJywnZGlkJzonZGlkOnNvdjpRbVdic05ZaE1yakhpcVpEVFVURUpzJywnbGFiZWwnOidBbGljZSd9
```
Example URL:
```text
http://example.com/ssi?c_i=eydAdHlwZSc6J2RpZDpzb3Y6QnpDYnNOWWhNcmpIaXFaRFRVQVNIZztzcGVjL2Nvbm5lY3Rpb25zLzEuMC9pbnZpdGF0aW9uJywnZGlkJzonZGlkOnNvdjpRbVdic05ZaE1yakhpcVpEVFVURUpzJywnbGFiZWwnOidBbGljZSd9
```
Invitation URLs can be transfered via any method that can send text, including an email, SMS, posting on a website, or via a QR Code. 

Example URL encoded as a QR Code:

![exampleqr](exampleqr.png)

#### Invitation Publishing
The _inviter_ will then publish or transmit the invitation URL in a manner available to the intended _invitee_. After publishing, we have entered the _invitation_shared_ state.

#### Invitation Processing

When they _invitee_ receives the invitation URL, there are two possible user flows that depend on the SSI preparedness of the individual. If the individual is new to the SSI universe, they will likely load the URL in a browser. The resulting page will contain instructions on how to get started by installing software or a mobile app. That install flow will transfer the invitation message to the newly installed software.
A user that already has those steps accomplished will have the URL received by software directly. That sofware can read the invitation message directly out of the `c_i` query parameter, without loading the URL.

If they _invitee_ wants to accept the connection invitation, they will use the information present in the invitation message to prepare the request

## 1. Connection Request
[1-connection-request]: #2-connection-request

The connection request message is used to communicate the DID document of the _invitee_ to the _inviter_ using the provisional connection information present in the _connection_invitation_ message.

The _invitee_ will provision a new DID according to the DID method spec. For a Peer DID, this involves creating a matching peer DID and key. The newly provisioned DID and DIDDoc is presented in the connection_request message as follows:

#### Example
```
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/request",
  "label": "Bob",
  "DID": "B.did@B:A",
  "DIDDoc": {
      // did Doc here.
  }
}
```
#### Attributes
* The `@type` attribute is a required string value that denotes that the received message is a connection request.
* The `label` attribute provides a suggested label for the connection. This allows the user to tell multiple connection offers apart. This is not a trusted attribute.
* The `DID` indicates the DID of the user requesting the connection.
* The `DIDDoc` contains the DID doc for the requesting user.

#### Request Transmission
The Request message is encoded according to the standards of the Agent Wire Level Protocol, using the provisional endpoint, key, and DID present in the invitation. This message is then transmitted to the provisional endpoint.

We are now in the `requested` state.

#### Request processing
After receiving the connection request, the _inviter_ evaluates the provided DID and DIDDoc according to the DID Method Spec.

The _inviter_ should check the information presented with the keys used in the wire-level message transmission to esure they match.

TODO: Specify error transmission back to _invitee_ in the event an error is found.
TODO: Specify error transmission back to _invitee_ in the event the request is rejected.

If the _inviter_ wishes to accept the connection, they will persist the received information in their wallet. They will then either update the provisional connection information to rotate the key, or provision a new DID entirely. The choice here will depend on the nature of the DID used in the invitation.

The _inviter_ will then craft a connection response using the newly updated or provisioned information.

## 2. Connection Response

[2-connection-response]: #3-connection-response

The connection response message is used to complete the connection. This message is required in the flow, as it updates the provisional information presented in the invitation.

#### Example
```
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/response",
  "DID":"A.did@A:B",
  "DIDDoc": {
      //did doc
  },
  "change_sig": "<signature of change with provisional key>"
}
```

#### Attributes

* The `@type` attribute is a required string value that denotes that the received message is a connection request.
* The `DID` attribute is a required string value and denotes DID in use by the _inviter_. Note that this may not be the same DID used in the invitation.
* The `DIDDoc` attribute contains the associated DID Doc.
* The `change_sig` attribute contains the authorization signature from the provisional key. This validates that this new DID Doc has been authorized by the provisional key.

In addition to a new DID, the associated DID Doc might contain a new endpoint. This new DID and endpoint are to be used going forward in the connection.

#### Response Transmission
The message should be packaged in the wire level format, using the keys from the request, and the new keys presented in the internal did doc. 

When the message is transmitted, we are now in the `responded` state.

#### Response Processing
When the _invitee_ receives the `response` message, they will verify the `change_sig` provided. After validation, theywill update their wallet with the new connection information. If the endpoint was changed, they may wish to execute a Trust Ping to verify that new endpoint.

TODO: Design the error report message if the change_sig fails.

We are now in the `complete` state.

#### Next Steps
The connection between the _inviter_ and the _invitee_ is now established. This connection has no trust associated with it. The next step should be the exchange of proofs to built trust sufficient for the purpose of the relationship.

#### Connection Maintenance
Upon establishing a connection, it is likely that both Alice and Bob will want to perform some relationship maintenance such as key rotations. Future HIPE updates will add these maintenance features.

# Reference
[reference]: #reference

* https://docs.google.com/document/d/1mRLPOK4VmU9YYdxHJSxgqBp19gNh3fT7Qk4Q069VPY8/edit#heading=h.7sxkr7hbou5i
* [Agent to Agent Communication Video](https://drive.google.com/file/d/1PHAy8dMefZG9JNg87Zi33SfKkZvUvXvx/view)
* [Agent to Agent Communication Presentation](https://docs.google.com/presentation/d/1H7KKccqYB-2l8iknnSlGt7T_sBPLb9rfTkL-waSCux0/edit#slide=id.p)

# Drawbacks
[drawbacks]: #drawbacks

* Public invitations (say, a slide at the end of a presentation) all use the same DID. This is not a problem for public institutions, and only provides a minor increase in correlation over sharing an endpoint, key, and routing information in a way that is observable by multiple parties.

# Prior art
[prior-art]: #prior-art

- This process is similar to other key exchange protocols.

# Unresolved questions
[unresolved]: #unresolved-questions

- This HIPE makes some assumptions about the underlying secure transport protocol in the absence of an official HIPE detailing the specifics of that protocol. In general, this HIPE assumes that message transportation has been solved.