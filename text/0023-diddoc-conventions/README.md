# 0023: DID Doc Conventions
- Name: diddoc-conventions
- Author: Stephen Curran (swcurran@gmail.com), Tobias Looker (tobias.looker@spark.co.nz)
- Start Date: 2018-08-14
- PR: 
- Jira Issue: 

## Summary 
[summary]: #summary

This is one of a series of HIPEs that together enable interoperability across implementations of DID based identity agents and ideally in the future, agents rooted in other self-sovereign identity ecosystems. 

## Motivation
[motivation]: #motivation

In this HIPE the use of the DIDDocs and in particular some associated conventions are defined that enable standardised communication between with DID based identity agents.

## Tutorial
[tutorial]: #tutorial

### Core Messaging Goals

These are vital design goals for this HIPE:

1. **Sender Encapsulation**: We SHOULD minimize what the Receiver has to know about the domain (routing tree or agent infrastructure) of the Sender in order for them to communicate.
2. **Receiver Encapsulation**: We SHOULD minimize what the Sender has to know about the domain (routing tree or agent infrastructure) of the Receiver in order for them to communicate.
3. **Independent Keys**: Private signing keys SHOULD NOT be shared between agents; each agent SHOULD be separately identifiable for accounting and authorization/revocation purposes.
4. **Prevent correlation based on DIDDoc Contents**: The information in the set of DIDDocs owned by an Identity SHOULD NOT be so precise as to represent a fingerprint for that Identity suitable for correlation.

### Assumptions

The following are assumptions upon which this HIPE is predicated.

#### Terminology

The following terms are used in this HIPE with the following meanings:

- [Sovereign] Domain - a set of Agents collaborating on behalf of an Identity
  - It's assumed that the Agents of a Domain were developed by a single vendor and so may use implementation-specific mechanisms for tracking extra information one another.
  - An example of two Domains is provided in the image below.
- Mediators and Relays - defined in the [Mediators and Relays](https://github.com/hyperledger/indy-hipe/pull/85)
- Domain Endpoint - a physical endpoint for messages into domains
  - Sender Agent - the Agent that creates an Agent Message for the Receiver that is in another Domain.
- Receiver Agent - the Agent that ultimately receives and can decrypt and process the Agent Message from the Sender.
- DID - reference to the literal Decentralized ID text
  - e.g. did:sov:1234abcd
- DID#keyname - a DID key reference which leverages the [DID fragments syntax](https://w3c-ccg.github.io/did-spec/#fragments).
  - e.g. did:sov:1234abcd#1 references key "1" of the "did:sov:1234abcd" DIDDoc.
  - **Note**: The #keyname is NOT the actual Public Key - it's a reference to an entry in the DIDDoc that contains the Public Key.

##### DIDDoc

The term "DIDDoc" is used in this HIPE as it is defined in the [DID Specification](https://w3c-ccg.github.io/did-spec/#did-documents):

- a collection of public keys and service endpoints
- controlled by an identity
- associated with a DID

A DIDDoc defines how its controlling entity can be messaged by other agents for a given relationship.

A DID can be resolved to get its corresponding DIDDoc by any agent that needs access to the DIDDoc. This is true whether talking about a public DID published on a Public Ledger, or a non-public DID that is only shared between participants in a relationship. In the case of a non-public DID, it's the (implementation specific) domain's responsibility to ensure that the DIDDoc associated with the DID is available (resolvable) to all Agents requiring it.

### DIDDoc Service Conventions

In order to be able to communicate with an DID based identity agent using DID infrastructure, the underlying conventions that host this communication must be standardised in the DIDDoc.

Within the [DID Specification](https://w3c-ccg.github.io/did-spec/#did-documents) lies a section called [Service Endpoints](https://w3c-ccg.github.io/did-spec/#service-endpoints), this section of the DIDDoc is reserved for `any type of service the entity wishes to advertise, including decentralized identity management services for further discovery, authentication, authorization, or interaction`.

This HIPE introduces the specification of a new DID service endpoint type called `DidMessaging`, which takes the following form.

```json
{
  "service": [{
    "id": "did:example:123456789abcdefghi;did-messaging",
    "type": "DidMessaging",
    "priority" : 0,
    "recipientKeys" : [ "did:example:123456789abcdefghi#1" ],
    "routingKeys" : [ "did:example:123456789abcdefghi#1" ],
    "serviceEndpoint": "https://agent.example.com/"
  }]
}
```

- id : Required by the [Service Endpoints Spec](https://w3c-ccg.github.io/did-spec/#service-endpoints).
- type : Required by the [Service Endpoints Spec](https://w3c-ccg.github.io/did-spec/#service-endpoints).
- priority : This represents the priority of the service endpoint, used for distinction when multiple `DidMessaging` service endpoints are present in a single DIDDoc.
- recipientKeys : This is an array of did key references used to denote the default recipients of an endpoint. 
- routingKeys: This is an array, ordered from most srcward to most destward, of did key references used to denote the individual hops in between the sender and recipients
- serviceEndpoint : Required by the [Service Endpoints Spec](https://w3c-ccg.github.io/did-spec/#service-endpoints).

#### Message Preparation Conventions

1. Resolve the relevant `DidMessaging` service of the DIDDoc.
2. Take the raw message the sender would like to send and pack it for the recipient keys listed in the service definition.
3. If the `routingKeys` array is empty then go to step 5. Otherwise for each key:
    1. Pack the message from the previous step with the key of the current entry in the `routingKeys` array.
    2. Prepare a `forward_to_key` message for the current entry in the `routingKeys` array, where the message is the `pack()`'d message from the previous step.
4. Resolve the service endpoint:
    5. If it is a valid endpoint URI, send the resulting message in accordance with the URI's protocol.
    6. If the service endpoint resolves to another service endpoint (i.e like the below example with agents-r-us), resolve this service endpoint and repeat this process from the beginning. 

> Notes
> For step 1. there are two main situations that an agent will be in prior to preparing a new message.
    >1. The agent is responding to a message that has just been received and has the context of the sender key of the previous message.
    >2. The agent is creating a new message to a connection and will use the default `DidMessaging` service convention for preparation of a message.
> With case 1. A targeted lookup of the `DidMessaging` service definition could be done to find a service definition that features the sender key as a recipient key which would ensure that the response was delivered back to the sender.
> With case 2. The default `DidMessaging` service description would be used by resolving the lowest priority service definition from the connections DID doc*

### Example: Domain and DIDDoc

The following is an example of an arbitrary pair of domains that will be helpful in providing context to conventions defined above.

![Example Domains: Alice and Bob](domains.jpg)

In the diagram above:

- Alice has
  - 1 Edge Agent - "1"
  - 1 Cloud Agent - "2"
  - 1 Domain Endpoint - "8"
- Bob has
  - 2 Edge Agents - "4", "5"
  - 2 Cloud Agents - "3", "6"
  - 1 Domain Endpoint - "9"

#### Bob's DIDDoc for his Relationship with Alice

Bob’s domain has 3 devices he uses for processing messages - two phones (4 and 5) and a cloud-based agent (6). As well, Bob has one agent that he uses as a mediator (3) that can hold messages for the two phones when they are offline. However, in Bob's relationship with Alice, he ONLY uses one phone (4) and the cloud-based agent (6). Thus the key for device 5 is left out of the DIDDoc (see below). For further privacy preservation, Bob also elects to use a shared domain endpoint (agents-r-us), giving him an extra layer of isolation from correlation. This is represented by the `serviceEndpoint` in the service definition not directly resolving to a endpoint URI rather resolving to another `DidMessaging` service description which is owned and controlled by the endpoint owner (agents-r-us). 

```json
{
  "@context": "https://w3id.org/did/v1",
  "id": "did:example:1234abcd",
  "publicKey": [
    {"id": "3", "type": "RsaVerificationKey2018",  "controller": "did:example:1234abcd","publicKeyPem": "-----BEGIN PUBLIC X…"},
    {"id": "4", "type": "RsaVerificationKey2018",  "controller": "did:example:1234abcd","publicKeyPem": "-----BEGIN PUBLIC 9…"},
    {"id": "6", "type": "RsaVerificationKey2018",  "controller": "did:example:1234abcd","publicKeyPem": "-----BEGIN PUBLIC A…"}
  ],
  "authentication": [
    {"type": "RsaSignatureAuthentication2018", "publicKey": "did:example:1234abcd#4"}
  ],
  "service": [
    {
      "id": "did:example:123456789abcdefghi;did-messaging",
      "type": "DidMessaging",
      "priority" : 0,
      "recipientKeys" : [ "did:example:1234abcd#4" ],
      "routingKeys" : [ "did:example:1234abcd#3" ],
      "serviceEndpoint" : "did:example:xd45fr567794lrzti67;did-messaging"
    }
  ]
}
```

Agents r Us DIDDoc

```json
{
  "@context": "https://w3id.org/did/v1",
  "id": "did:example:xd45fr567794lrzti67",
  "publicKey": [
    {"id": "1", "type": "RsaVerificationKey2018",  "controller": "did:example:xd45fr567794lrzti67","publicKeyPem": "-----BEGIN PUBLIC X…"},
  ],
  "authentication": [
    {"type": "RsaSignatureAuthentication2018", "publicKey": "did:example:xd45fr567794lrzti67#1"}
  ],
  "service": [
    {
      "id": "did:example:xd45fr567794lrzti67;did-messaging",
      "type": "DidMessaging",
      "priority" : 0,
      "recipientKeys" : [ "did:example:xd45fr567794lrzti67#1" ],
      "routingKeys" : [ ],
      "serviceEndpoint" : "http://agents-r-us.com"
    }
  ]
}
```

#### Message Preparation Example

Alices agent goes to prepare a message `desired_msg` for Bob agent.

1. Alices agent resolves the above DID doc Bobs agent has shared with her and resolves the `DidMessaging` service definition.
2. Alices agent then packs the desired message she wishes to trasmit with the keys noted in the `recipientKeys` array. 
  `pack(wallet,desired_msg,[did-resolve(did:example:1234abcd#4)],sender_verkey)`
3. Because the the `routingKeys` array is not empty, the message is then wrapped inside a forward to keys message where the subject is the contents of the `recipientKeys` array resolved to raw key values.
4. The resulting message from the previous step is then packed for the first and only key in the `routingKeys` array.
  `pack(wallet,wrapped_message,[did-resolve(did:example:1234abcd#3)],sender_verkey)`
5. Resolution of the service endpoint leads to resolving another `DidMessaging` service definition, this time owned and controlled by `agents-r-us`.
6. Because in the `agents-r-us` service definition there is a recipient key. The newly packed message is then wrapped in another forward to key message where the subject is first and only key in the `routingKeys` array.
7. This wrapped message is then packed in a message for the keys noted in the `recipientKeys` array of the `agents-r-us` `DidMessaging` service defintion.
8. Finally as the endpoint listed in the serviceEndpoint field for the `agents-r-us` `DidMessaging` service definition is a valid endpoint URI, the message is tramitted in accordance with the URI's protocol.

## Reference
[reference]: #reference

## Drawbacks
[drawbacks]: #drawbacks

As noted in the `Unresolved Questions` section below, this HIPE is not complete. Further conventions need to be formalized to achieve reliable interoperability.

## Rationale and alternatives
[alternatives]: #alternatives

## Prior art
[prior-art]: #prior-art

N/A

## Unresolved questions
[unresolved]: #unresolved-questions

The following remain unresolved:

- The convention for packing the message for the required routes is dependent on the array order of key references, which could be viewed as a weak/brittle convention. 
- It may be appropriate to have a convention in the DIDDoc to designate which keys (and potentially, endpoints) are used for different roles beyond receivers and mediators in the Domain.  For example:
  - A defined list of roles.
  - A convention for determining the roles associated with a key.
- As noted in the DIDDoc Update Authorization section (above) for example, it is not clear in the DID Spec or in this HIPE (yet) what keys empower an Agent to make updates to the manifestation of the DIDDoc.