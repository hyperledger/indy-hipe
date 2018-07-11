- Name: transport-layer-messaging
- Author: Stephen Curran (swcurran@gmail.com)
- Start Date: 2018-07-09
- PR: 
- Jira Issue: 

# Summary
[summary]: #summary

There are at least two layers of messages that combine to enable self-sovereign identity Agent-to-Agent communications. At the highest level (that we are considering) are Application messages - messages sent between Identities to accomplish some shared goal. For example, establishing a connection between identities, issuing a Verifiable Credential from an Issuer to a Holder or even the simple delivery of a text Instant Message from one person to another.

Application Layer Messages are delivered via the second, lower layer of messaging - Transport. There are two kinds of Transport Layer messages: routing and wire messages. Routing messages are wrappers (envelopes) around Application Layer messages that are used to route the App message through an arbitrarily complex web of Agents to the intended recipient Agent for processing. Wire Messages are used to send a message directly from one Agent to another along each step of the routing.

This HIPE focuses on Transport Layer Messaging - routing and wire messages.

# Motivation
[motivation]: #motivation

The purpose of this HIPE is to define the Transport Layer Messaging such that we can ignore the delivery of messages as we discuss the much richer Application Layer Messaging types and interactions.  That is, we can assume that there is no need to include in an Application Layer message anything about how to route the message to the recipient - it just happens.

This HIPE covers the most important routing for Agent to Agent interoperability: the handoff of a message from one domain to another. For example, the transmission of a message from Alice's domain to Bob's. In the assumptions, fewer constraints are put on the message handling within a domain, allowing for more elaborate capabilities that are implementation specific - and yet still interoperable.

# Tutorial
[tutorial]: #tutorial


## Core Messaging Requirements

These requirements are understood as standard in the Indy community:

1. **Sender Anonymity**: The receiver should not have to know about the routing tree or agent infrastructure of the sender in order for them to communicate.
2. **Receiver Anonymity**: The sender should not have to know about the routing tree or agent infrastructure of the receiver in order for them to communicate.
3. **Decentralized**: There is not a single agent that holds all the keys or data. The loss of any one agent is recoverable by the other agents (assuming the identity has multiple agents).
4. **Private Keys**: No private keys may be shared between agents.

## Assumptions

The following are assumptions upon which this HIPE is based, with (as necessary) the rationale behind the assumption.

### DIDDocs

The term "DIDDoc" is used in this HIPE to indicate a collection of public keys and endpoints about a DID. This is a shorthand to reference when the contents of a DIDDoc needs to be transmitted - either to/from the Public Ledger or between identities sharing a microledger.

### Collaborating Agents

It is assumed that the Agents within a domain collaborate in implementation specific ways. That is, we assume that the Agents within a domain are implemented by the same vendor, and as such, can know more about the behaviour of those Agents than is defined here.

Conversely, it is assumed that Agents in different domains **only** know how to transport messages to one another using the mechanisms defined here. In other words - interoperability.

### DIDs Can Be Resolved

All messages addressed to a DID can be resolved to a DIDDoc by the Agents involved in its transmission.

Currently, this is implied in Hyperledger Indy because all DIDs are on the public ledger. If and when the transition is made to microledgers, this assumption becomes a constraint on the microledger implementation. That is, a DIDDoc known to an Agent must be available to all Agents involved in the transmission of the message to its recipient.

### One DID and (at least) Two Public Keys

For a message to be transported from the Agent of one identity to another it is assumed that the recipient's DIDDoc contains all of the information necessary to transmit messages between the Identity Domains.

That implies there must be at least two identifiable public keys accessed using the DIDDoc - one for Application Layer messages and one for transmitting Transport Layer messages to the DID endpoint - by definition the Domain Endpoint. In theory, an implementation could use a single public key for both, but that would expose that the same Agent is both the endpoint and processing the message.

This further implies there is at least one endpoint that is specifically designated in an interoperable way in the DIDDoc as being the Domain Endpoint for the DID. This convention is necessary to meet the core requirement of "receiver anonymity".

### Transport DIDs (TDIDs) Known Within a Domain

> The term "Transport DID" (TDID) is introduced to mean the physical address and public encryption key for the transport of messages to an Agent. This is to differentiate the DIDs used solely for transport from the DIDs used for Application Layer Communications.

Within a domain, the TDIDs of Agents are known to other Agents with whom they need to communicate. How this information is created and shared is up to the implementation of the Agents within a domain.

Implied in this assumption is that the reason for Agents within a domain to communicate with one another are known and tracked by the Agents. This is easy if the structure of Agents is simple - e.g. Agency <-> Cloud Agent <-> Edge Agent, but gets increasingly more complex as the number, and purposes, of Agents in a domain increase. Such complexity is implementation specific.

### Domain Endpoint (aka Agency Endpoint)

A domain is assumed to have an TDID that is the endpoint of the domain. That TDID information (endpoint, public key) can be found using the recipient's DIDDoc (e.g. the DIDDoc of the recipient's pairwise DID).

Unlike the "within domain" case above, where the TDIDs and purpose for sending messages between Agents are known, in the cross domain case, the TDID information must be found.

### Inbound Domain Routing

Since a Domain Endpoint is assumed to be the endpoint for many Identities, each with many DIDs, it is assumed that the Agent managing a Domain Endpoint has knowledge of where in the domain to send the message based on the recipient pairwise DID.

This assumption is a requirement on the implementation of a Domain Endpoint agent based on the protocol in this HIPE. Further details of how this is expected to work is described in the Transport Layer Messaging section (below).

### Agents Track Connection of Pairwise DIDs

When two identities establish a connection via a set of pairwise DIDs, each must track the DIDs together so that knowing one DID implies knowledge of the other DID. It's the responsibility of the Agents involved to retain that state at all times.

This allows, for example, an Agent to receive a message to a pairwise DID it controls to know from whom the message was sent and hence, the sender's public key. This in turn defines when an Application Layer Message can be encrypted with AnonCrypt and the preferred AuthCrypt. This is detailed later in this HIPE.

## Transport Layer Messaging

This HIPE proposes two groups of messages with (initially) just one message type each. The lowest level is the Wire Message - the sending of a message directly from one Agent to another (no intermediaries). The second group are the message types for routing an application layer message.

### Wire Message Format

Messages sent across the wire go between Agents within the same domain or to another domain. Per the assumptions above, for messages being sent within a domain, the sender knows the TDID (Transport DID) of the receiver. If the message is being sent across domains, the DID to which the message is resolved to determine the endpoint and public key for that endpoint. This makes all wire messages simple:

```
  {
    "message": "<Base64(AnonEncrypt(RecvPubKey, message))>"
  }
  
```

The message is sent to the endpoint of the receiving Agent. On receipt, the recipient decrypts the wire message with the private key associated with the endpoint and processes the message.

#### Network Protocol

The network protocol to use for sending the message (https, zmq, etc.) must be known, presumably by the protocol implied by the endpoint. Still needed in this HIPE (or perhaps a separate HIPE) is how an essentially anonymous blob of text is to be delivered for each supported protocol.

#### Response

The following are the possible responses to the message:

- OK
- Invalid Message
  - The message could not be decrypted
- Not Found
  - The message could not be processed.

##### Response Issues

Should the message response be synchronous or asynchronous?  If the wire protocol fails, how is that failure passed back to those involved in the transmission?

If it is an asynchronous response, the message format must add a nonce and callback address, which seems onerous. If synchronous and the message decryption and determination if the message can be processed will take too long for a synchronous response, perhaps just an OK/Error response is acceptable based on the receipt of the wire message.

If the wire protocol fails, notifying the Application Layer message sender might be needed. That will be covered later in this process.

A reason for using a synchronous response to at least checking the ability to decrypt the message is cache handling. Agents might cache DID information for performance (fewer trips to the ledger) and so messages might be invalid due to undetected key rotations. If the "Invalid Message" response was synchronously returned to the Sender, the Sender could resolve the TDID it was using and retry without breaking the higher level protocol.

### Transport Message Types

#### Transport Message: Forward 

The primary transport message type is "Forward". The message is an envelope, securely wrapping an Application Layer Message by the message creator and addressed to the intended Application Layer recipient. Each Agent that receives the envelope either opens it if they are the Application Layer recipient, or resends it based on their knowledge of where it should go next (covered below in the "Forward Routing" section)

The contents of a Forward are:

```
{
  "type": "Forward"
  "to": "DID"
  "message": "<Base64(AuthCrypt or AnonCrypt(Application Layer Message)>"
}
```

The Sender - the Agent that constructs the Application Layer Message - also constructs the Forward message. No one other than the intended recipient can access anything about the Application Layer Message.

The choice of using AnonCrypt or AuthCrypt is based on the state of the known DIDs between the Sender and Receiver. If the message is being sent using one of a pairwise DID set, both sides implicitly know the state of the connection and AuthCrypt can be used. If only one DID is known by both parties at the time of transmission, AnonCrypt must be used. For example, on the first message of the sequence to initiate a connection, only one DID is known to both parties and so AnonCrypt must be used. After that, both sides know a DID for each other and AuthCrypt can be used.

##### Forward Routing

When an Agent receives a message intended for them (they control the "To" DID), they can decrypt the payload message and process it.

If an Agent receives a Forward message for which they are not the intended recipient, they must Forward the identical message on to another Agent. There are two cases to consider - forwarding the message to an agent within their domain, or to an agent outside their domain.

###### Forwarding Within A Domain

Within a domain, it is assumed that each Agent knows enough about their role in the domain to know what to do with the forward message they received. If the Agent is part of the outbound domain, they may know that all such messages go to an Agency Sender for cross domain delivery. If the Agent is receiving an inbound message for the domain, they may know how to send directly to the recipient - e.g. they have access to a mapping table of arbitrary DIDs to TDIDs.

**Question**: A protocol for managing TDIDs and DID mapping tables within a domain is necessary. Should it be included here?  It really is implementation specific, but an reference implementation might be useful to describe.

###### Forwarding Across Domains

When an Agent responsible for sending messages outside a domain receives an envelope, they resolve the "To" DID and, from the DIDDoc, determine what they need to know (physical endpoint and transport public key) to forward the message using the wire protocol.

**ASIDE**: This is where it might be useful for the endpoint in the pairwise DID to be the Domain Endpoint's TDID. If pairwise DIDs contains the actual endpoint and public key of the Domain Endpoint, every pairwise DID in an Agency must be updated when that Agency public key is rotated (or endpoint changed). If the pairwise DIDs contain the Domain Endpoint's TDID, it can be rotated within minimal effort. Pairwise DIDs would only need to be updated when changing the Domain Endpoint for the Identity Relationship - e.g. when changing Agencies - likely a far rarer event.

#### Transport Message: Multiplex

A possible second type of transport message is a Multiplex, where the Sender sends the message to multiple recipients identified within a DID. There is a lot of complexity with that on all sorts of levels, and so a Multiplex mechanism will be deferred for now. A later Pull Request might update this HIPE with the details.

Worst case, the Sender could send out multiple versions of an Application Layer Message using a Forward message to each intended recipient.

### Application Layer Error Handling

If the Transport Messages fail at any point, there is no way as specified to notify the original Sender. None of the Agents involved in the Transport know who sent the message, only who is supposed to receive it. To notify the Sender of an error, a ID for the Sender is needed - perhaps a resolvable DID or some other ephemeral ID that would work across domains.  Without that, only a timeout is possible for a User to be informed of a Transport-level error.

**Question**: Should this HIPE include this level of error notification?

# Reference
[reference]: #reference

The current summary of AuthCrypt and AnonCrypt are documented [here](https://github.com/hyperledger/indy-hipe/pull/9) - see May 29th comment from vimmerru.

# Drawbacks
[drawbacks]: #drawbacks

* The assumptions need to be reviewed to see if they are too onerous. The intention is that the assumptions are implementation specific - as long as they are met, the mechanisms will work. However, a reference implementation description of how to meet the assumptions is likely necessary.
* **Others to be added as we discuss this HIPE.**

# Rationale and alternatives
[alternatives]: #alternatives

**These will be added to the HIPE as discussions occur about it.**

# Prior art
[prior-art]: #prior-art

**This will be added to the HIPE as discussions occur about it.**

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

**These will be added to the HIPE as discussions occur about it.**

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
