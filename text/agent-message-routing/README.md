- Name: agent-message-routing //Connection Base Routing
- Author: Tobias Looker
- Start Date: 2018-11-22
- PR: (leave this empty)
- Jira Issue: (leave this empty)

# Summary
[summary]: #summary

In order to facilitate agent to agent (A2A) messaging the mechanism of message routing must be defined. The formal definition of routing in the context of A2A messaging is the concept of a message delivered to an agent which based on the message content....

# Motivation
[motivation]: #motivation

Routing records will underpin the ability to sucessfully deliver an agent message, it is therefore important that...

HIPE #22 introduced the forward message type and this HIPE intends to define the message types required for an agent to maintain the routing records to which the forward message type depends.

# Tutorial
[tutorial]: #tutorial

For the purposes of this HIPE the establishment of some nomenclature is required to reduce ambiguity
- Destination Agent = This is the agent to which the inner most message, or effectively the message contents is destined for (usually an edge agent).
- Intermediate Agent = This is an recipient agent who will recieve the message and un-wrap the layer destined for them, before sending the message to the next recipient agent.
- Sending Agent = This is an agent sending an agent message.
- Recipient Agent = This is an agent recieving an agent message, by definition this agent could be either a routing agent or a destination agent.

This HIPE hinges on the concept of connection based routing, which is the the idea that for each recipient agent required for a message to be sucessfully delivered, a connection must exist between the...

**High Level Example**
If we consider the basic routing example below where an abitrary message is routed from agent 1 to agent 4 via 2 and 3.

1. Sending Agent.
2. Intermediate Agent.
3. Intermediate Agent.
4. Destination Agent.

1 --> 2 --> 3 --> 4

Note - How agent 1 knows how to pack the message for delivery to agent 4 is out of scope of this immediate example.

What is important to note is that minimum set of connections required to host this message transfer.

- Agent 3 MUST have a connection with Agent 2 and vice versa.
- Agent 4 MUST have a connection with Agent 3 and vice versa.

The above connections must exist as this establishes the basis of trust required to underpin the maintenance of routing records.

**Detailed Example**
Bob wants to send Alice a message, they have sucessfully connected and have the following agent configuration.

![Example Domains: Alice and Bob](domains.jpg)

In the diagram above:

- Alice has
  - 1 Edge Agent - "1"
  - 1 Routing Agent - "2"
  - 1 Domain Endpoint - "8"
- Bob has
  - 3 Edge Agents - "4", "5" and "6"
    - "6" is an Edge Agent in the cloud, "4" and "5" are physical devices.
  - 1 Routing Agent - "3"
  - 1 Domain Endpoint - "9"

During connection Alice disclosed to Bob the following did doc representing her pairwise relationship to Bob.

```json
{
  "@context": "https://w3id.org/did/v1",
  "id": "did:sov:1234abcd",
  "publicKey": [
    {"id": "routing", "type": "RsaVerificationKey2018",  "owner": "did:sov:1234abcd","publicKeyPem": "-----BEGIN PUBLIC X…"},
    {"id": "4", "type": "RsaVerificationKey2018",  "owner": "did:sov:1234abcd","publicKeyPem": "-----BEGIN PUBLIC 9…"},
    {"id": "6", "type": "RsaVerificationKey2018",  "owner": "did:sov:1234abcd","publicKeyPem": "-----BEGIN PUBLIC A…"}
  ],
  "authentication": [
    {"type": "RsaSignatureAuthentication2018", "publicKey": "did:sov:1234abcd#4"}
  ],
  "service": [
    {"type": "Agency", "serviceEndpoint": "did:sov:fghi8377464" }
  ]
}
```

//TODO

# Goals

**Routing record definitions**
The following message types allow for the maintenance of routing records

Create Routing Record Message

```json
{
 “@type”: “did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routing/0.1/create”,
 “recipient” : "<recipient-identifier>"
}
```

Delete Routing Record Message

```json
{
 “@type”: “did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routing/0.1/delete”,
 “recipient” : "<recipient-identifier>"
}
```

Get Routing Records Message

```json
{
 “@type”: “did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routing/0.1/get"
}
```

Routing Record Message

```json
{
 “@type”: “did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routing/0.1/record”,
 “recipient” : "<recipient-identifier>"
}
```

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
