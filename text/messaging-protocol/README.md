- Name: Messaging Protocol
- Authors: Ryan West ryan.west@sovrin.org & Daniel Bluhm daniel.bluhm@sovrin.org
- Start Date: 2018-6-29
- PR: 
- Jira Issue: https://jira.hyperledger.org/browse/IA-18

# Summary
[summary]: #summary

This HIPE describes the protocol to establish connections and send messages between agents. Connections allow establishing relationships between identities.

# Motivation
[motivation]: #motivation

Indy agent developers want to create agents that are able to establish connections with each other and exchange secure information over those connections. For this to happen there must be a clear messaging protocol standard.

# Tutorial
[tutorial]: #tutorial

We present the scenario in which Alice and Bob wish to communicate. The following messages must be sent between them to establish a secure, persistent channel for communication:

1. Connection Offer (optional dependent on transport used)
2. Connection Request
3. Connection Response
4. Bob's Acknowledgement
5. Alice's Acknowledgement

The format for a generic message is also given below.

Each of these steps is explored in detail below.

### 1. Connection Offer

The connection offer message is used to disclose the endpoint needed to exchange a connection request message. If the Endpoint DID is already known or discoverable on the ledger, *the connection offer is not necessary*. If the Endpoint DID is not on or discoverable on the ledger, then the connection offer message is a way to communicate the necessary information to an agent in order to establish a connection/relationship.

**Example:** Alice first creates a connection offer, which gives Bob the necessary information to connect with her at a later point. This can be done in person (perhaps using a QR code), or remotely using previously established secure connection. The Connection Offer includes an endpoint, which allows Bob to encrypt messages and provides a destination address. 

```
{
    "id": offer_nonce
    "type": connection_offer
    "content": {
	    "ep": {
            "did": A.ep.did
            --- or ---
            "ha": A.ep.url  
            "verkey": A.ep.vk 
        }
    }
}
```

* The `id` attribute of the base message is required and is a nonce used to correlate the connection request.
* The `type` attribute of the base message is required. The actual type value provided above will be defined in a future hipe. 
* The endpoint `ep` is a structure that contains either `ha` and `vk`, or just a DID that resolves to the corresponding ha and vk attributes from the public ledger.  Alice can use a DID so Bob can retrieve her url+vk on the Sovrin ledger, or directly share a url+vk if she prefers not to use the ledger.
    * `ha`, the url of the host address (or other location, if not using http/https) to provide a destination.
    * `vk`, verification key (aka public key, verkey) to encrypt the message so that only the autorized person can decrypt it.
    * `did`, public did that can resolve to a url and vk.


### 2. Connection Request

The connection request message is used to provide a DID to an agent in establishing a connection. The generated DID will eventually become associated in a pairwise DID relationship in both participant’s wallets.

**Example:** When Bob receives Alice's connection offer, he can initiate a relationship with a connection request. Bob sends Alice a message containing the following:

```
{ # anon-encrypted using A.ep.vk
	"id": offer_nonce (optional)
	"to": A.did@A (public, optional)
	"type": connection_request
	"content": {  # plaintext (cannot yet be encrypted)
		"did": B.did@B:A
		"verkey": B.vk@B:A
		"ep": B.ep
	}
}
``` 

* The `id` is optional and is the nonce received in the connection offer, proving that Bob received an authentic connection offer. This attribute is required if Bob did not / could not use Alice's public DID on the ledger.
* The `to` attribute is optional and contains Alice's public DID if she chose to make it available on the ledger. The connection response step is not required if this is the case, as Bob can obtain Alice's endpoint information with a ledger lookup.
* The `type` attribute of the base message is required.
* The `content` attribute of the base message is required, is not encrypted, and is an object containing the following attributes:
  * The `did` attribute is required and is a DID created by the sender of the connection message.
  * A new, relationship-specific verification key `vk` is required so that Alice can send Bob auth-encrypted messages
  * Bob's own endpoint information `ep` is required, so Alice can anon-encrypt the entire message.

Bob then anon-encrypts the whole `con_req` message using Alice's endpoint verification key, so that only she can decrypt it.

### 3. Connection Response

The connection response message is used to respond to a connection request message and provide a DID to the sender of the connection request message to be used as a pairwise DID in an established connection/relationship.

**Example:** If Alice still wants to communicate with Bob, she sends a connection response. 

```
{ # anon-encrypted using B.ep.vk
    "to": B.did@B:A,
    "type": connection_response,
    "content": {  # anon-encrypted using B.vk@B:A
            "did": A.did@A:B,
            "verkey": A.vk@A:B
    }
}
```
* The `to` attribute is required and is `A.did@B:A`, the DID that Bob sent Alice. It is used to send the message to the correct destination.
* The `type` attribute of the base message is required.
* `content` is anon-encrypted using Bob's new verification key `B.vk@B:A`. It includes:
  * The `did` attribute is required and is a DID that Alice created for the Bob-to-Alice relationship. This is used in creating a pairwise DID with the DID sent in the connection request message.
  * `verkey` is a required, connection-specific verification key, necessary so that Bob can send Alice auth-encrypted messages


The whole message is anon-encrypted using Bob's endpoint verification key. From this point forward, all inner messages' `content` is auth-encrypted.

### 4. Bob's Acknowledgement

The connection acknowledgement message is used to confirm that pairwise DIDs creating a connection/relationship have been established between each agent. The connection acknowledgement message contains an auth-encrypted message which is now possible because of the shared pairwise DIDs. This auth-encrypted pattern is important as a foundation for other message types to be designed requiring privacy and protected data.

**Example:** When Bob receives the connection response, he sends an acknowledgement message back. At this point, Bob has Alice's new (owner) verification key, DID, and endpoint (with its own verification key and url), and can now send messages securely using `auth-encrypt`. But Alice needs to know that her connection response message was received successfully.

```
{ # anon-encrypted using A.ep.vk
    "to": A.did@A:B
    "type": message_acknowledgement
    "message": "success" #auth-encrypted using A.vk@A:B and B.vk@B:A
}
```
* The `to` attribute of the base message is required and is the DID of the sender of the connection acknowledgement message in the pairwise DID established connection/relationship.
* The `type` attribute of the base message is required.
* The `message` is the encrypted string "success".

Note that no new information is sent here except for a "success" string. However, the message content is auth-encrypted using both Alice's and Bob's verification key. Thus, this simple message serves as proof that the messages being exchanged between Alice and Bob are computationally secure.

### 5. Alice's Acknowledgement

When Alice receives Bob's acknowledgement, she too needs to acknowledge that she received it correctly. Bob does not yet know that the connection is secure until Alice sends this message.

```
{ # anon-encrypted using B.ep.vk
    "id": B.did@B:A
    "type": message_acknowledgement
    "message": "success" #auth-encrypted using B.vk@B:A and A.vk@A:B
}
```

This serves the same purpose as Bob's acknowledgement: now Bob knows that Alice knows that Bob's connection request was accepted. At this point, they have established a computationally secure relationship.

The next step of establishing a connection could be exchanging credentials to prove both Alice's and Bob's identities. Details on this protocol will be in a future HIPEs.

### Future Communication
From this point forward messages sent from Alice to Bob or from Bob to Alice will typically be auth-encrypted. Details on the exact structure and layers of encryption of these messages will be detailed in future HIPEs.

![puml diagram](http://www.plantuml.com/plantuml/proxy?src=https://raw.githubusercontent.com/ryanwest6/indy-hipe/master/text/messaging-protocol/establishing_connection.puml? "")

# Reference
[reference]: #reference

* There are a total of 4 verification keys between Alice and Bob. Alice has a public endpoint verification key, which is used by Bob to anon-encrypt the entire message. Alice also generates a new verification key specific to her relationship with Bob. Bob likewise has a public endpoint verification key and a connection-specific verification key.
* https://docs.google.com/document/d/1mRLPOK4VmU9YYdxHJSxgqBp19gNh3fT7Qk4Q069VPY8/edit#heading=h.7sxkr7hbou5i

# Drawbacks
[drawbacks]: #drawbacks

* In a connection request message, because the pairwise DIDs have not yet been created, Bob cannot auth-encrypt the content of his message. Thus, if an agency were to decrypt the overall message and forward it to Alice's edge agent, the agency would see the connection request's content in plaintext. This could potentially be a security concern. However, we have chosen to discuss agents and agencies in a future hipe rather than combine them.

* auth-encrypt/anon-encrypt do not preserve sender and receiver anonymity as explained by nage. Do we ignore this for this layer of abstraction?

# Rationale and alternatives
[alternatives]: #alternatives

- The acknowledgement steps are not technically necessary, as both pairwise DIDs and verification keys exchanged after the connection response.

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
        "ep": {
            "did": A.ep.did
            --- or ---
            "ha": A.ep.url  
            "verkey": A.ep.vk 
        }
    }
    ```
- In connection offer end point, should a transport protocol be used?
    ```
    {
        "id": offer_nonce
        "type": connection_offer    
        "ep": {
            "did": A.ep.did
            --- or ---
            "protocol": <url, ssh, http, https, ...> 
            "ha": <host address>
            "verkey": A.ep.vk 
        }
    }
    ```