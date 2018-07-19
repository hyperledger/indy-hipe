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

The purpose of this HIPE is to define the Transport Layer Messaging such that we can ignore the delivery of messages as we discuss the much richer Application Layer Messaging types and interactions. That is, we can assume that there is no need to include in an Application Layer message anything about how to route the message to the recipient - it just magically happens. Alice (via her Edge Agent) sends a message to Bob, and (because of implementations based on this HIPE) we can ignore how the message got to Bob's Edge Agent.

Put another way - this HIPE is about envelopes. It defines a way to put a message - any message - into an envelope, put it into an outbound mailbox and have it magically appear in the recipient's inbound mailbox. Once we have that, we can focus on letters and not how the letters are sent.

This HIPE covers both how a message is sent from one Agent directly to another - the Wire protocol - and how the messages are routed to their ultimate destination through an arbitrary series of Agents.

Most importantly for Agent to Agent interoperability, this HIPE clearly defines the handoff of a message from one domain to another - e.g. how to transmit a message from Alice's domain to Bob's. Fewer constraints are put on message routing within a domain, allowing for more elaborate capabilities that are implementation specific - and yet still interoperable.

# Tutorial
[tutorial]: #tutorial


## Core Messaging Goals

These are vital design goals for this HIPE:

1. **Sender Encapsulation**: We must minimize what the receiver has to know about the routing tree or agent infrastructure of the sender in order for them to communicate.
2. **Receiver Encapsulation**: We must minimize what the sender has to know about the routing tree or agent infrastructure of the receiver in order for them to communicate.
3. **Independent Keys**: Private signing keys should not be shared between agents; each agent should be separately identifiable for accounting and authorization/revocation purposes.
4. **Granular privileges for agents**: It must be possible for an identity owner to assign different privileges to the various agents that work on his/her behalf. Without this feature, an agent can impersonate its owner because all entities within an sovereign domain are indistinguishable. Note that this goal follows naturally from #3, and creates a tension with goals 1 and 2. 
5. **Decentralization**: We should avoid having a single agent hold all the keys or data. The loss of any one agent should be recoverable by the other agents (assuming the identity has multiple agents).
6. **Extensibility**: New types of messages can be added without changing the protocol defined here.
7. **Transport independence**: The same rules should apply, and the same guarantees should obtain, no matter what transport is used to move messages.
8. **Repudiability**: It must be possible to [communicate off the record](https://github.com/sovrin-foundation/protocol/blob/master/janus/repudiation.md); Alice can talk to Bob, and Bob can know it is Alice, without Alice worrying that Bob can turn around and prove Alice's communications to an uninvolved party.

## Assumptions

The following are assumptions upon which this HIPE is based, with (as necessary) the rationale behind the assumption.

### DIDDocs

The term "DIDDoc" is used in this HIPE to indicate a collection of public keys and endpoints about a DID. This is a shorthand to reference when the contents of a DIDDoc needs to be transmitted - either to/from the Public Ledger or between identities sharing a microledger.

### Collaborating Agents

It is assumed that the Agents within a domain collaborate in implementation specific ways. That is, we assume that the Agents within a domain are implemented by the same vendor, and as such, can know more about the behaviour of those Agents than is defined here.

Conversely, it is assumed that Agents in different domains **only** know how to transport messages to one another using the mechanisms defined here. In other words - interoperability.

### DIDs Can Be Resolved

A DID must be resolved to a corresponding DIDDoc by any Agent that directly delivers messages to the sovereign domain of that DID.
Some other agents involved in delivery or routing may also need this capability. This is true whether we are talking about DIDs on the public ledger, or DIDs persisted to a microledger.

### One DID and (at least) Two Public Keys

For a message to be transported from the Agent of one identity to another it is assumed that the recipient's DIDDoc contains all of the information necessary to transmit messages between the Identity Domains.

That implies there must be at least two identifiable public keys accessed using the DIDDoc - one for Application Layer messages and one for transmitting Transport Layer messages to the DID endpoint - by definition the **Domain Endpoint**. In theory, an implementation could use a single public key for both, but that would expose that the same Agent is both the endpoint and processing the message.

This further implies there is at least one endpoint that is specifically designated in an interoperable way in the DIDDoc as being the Domain Endpoint for the DID. This convention is necessary to meet the core goal of "receiver encapsulation".

### Agent Metadata

Each agent must have a key pair. Agents that *receive* messages (as opposed to agents that only *send* messages) must also be reachable by other entities inside their sovereign domain. This implies that they have some sort of internally known endpoint.
 
For convenience of their owners, agents may also have an identifier. However, this identifier is an implementation detail, and it is not required by the spec.
As suggested by the encapsulation design goals listed above, how an identity owner refers to their agents should not be exposed externally.

Agents hold keys, and they use these keys to communicate securely. As required by the "Independent Keys" and "Granular Permissions" design goals, at least some of these keys are communicated externally. This is how an identity owner says something like, "This key should be trusted to sign for me. That key should not." Although keys often correspond to agents, this correspondence may be complex. For example, some keys authorized by an identity owner may be written down on a piece of paper and locked away in a safe--not held by an agent at all. Other keys may be known to an identity owner but not involved in a particular relationship and therefore not disclosed to a remote party (as in the case of a corporation that has thousands of agents but only uses two of them to interact with a customer). Thus, we balance the goals of encapsulation, independent keys, and granular permissions by assigning keys in a granular way; not sharing them; disclosing keys but agent infrastructure; and by disclosing only as much as is relevant.

The concept of key rotation is meaningful to identity owners, within their domain, but is not known for agents. An identity owner has no need to tell another party that a particular agent exists and has a consistent identity across key rotations; rather, the identity owner simply says "keys X and Y are authorized" at one point in time and "key Y and Z are authorized" at another. No relationship between these states matters to the other party.

### Domain Endpoint

A domain has an endpoint and an associated public key that receive inbound communication from other identity owners. That information can be found using the recipient's DIDDoc.

This domain endpoint does not need to be unique. That is, many different domains may (and, for herd privacy reasons, probably should) share the same endpoint. This might be the case for all identities running cloud agents at a single agency, for example. If endpoints are unique, a privacy/correlation risk arises.    

### Inbound Domain Routing

Since a Domain Endpoint may be the endpoint for many Identities, each with many DIDs, it is assumed that the Agent managing a Domain Endpoint has knowledge of where in the domain to send the message based on the recipient pairwise DID.

This assumption is a requirement on the implementation of a Domain Endpoint agent based on the protocol in this HIPE. Further details of how this is expected to work is described in the Transport Layer Messaging section (below).

### Agents Track Connection of Pairwise DIDs

When two identities establish a connection via a set of pairwise DIDs, each must track the DIDs together so that knowing one DID implies knowledge of the other DID. It's the responsibility of the Agents involved to retain that state at all times.

This allows, for example, an Agent to receive a message to a pairwise DID it controls to know from whom the message was sent and hence, the sender's public key. This in turn defines when an Application Layer Message can be encrypted with AnonCrypt or AuthCrypt. This is detailed later in this HIPE.

## Transport Layer Messaging

This HIPE proposes two groups of messages with (initially) just one message type each. The lowest level is the Wire Message - the sending of a message directly from one Agent to another (no intermediaries). The second group are the message types for routing an application layer message.

### Wire Message Format

Messages sent across the wire go between Agents within the same domain or to another domain. For messages being sent within a domain, the sender knows the endpoint and public key of the receiver. If the message is being sent across domains, the DID to which the message is going is resolved to determine the endpoint and public key for its domain endpoint. This makes all wire messages simple:

```
<Base64(AuthCrypt or AnonCrypt(RecvPubKey, message))>
```

Whether the message is AuthCrypted or AnonCrypted is the choice of the sender--but some encryption is
desirable to prevent eavesdropping. When crossing a domain--that is, in the hop that delivers a message
to the message routing endpoint at the border of a new sovereign domain--AnonCrypt is normally used,
because the message routing endpoint is assumed to have no need to know the sender, and is assumed to
receive only "Forward" messages; thus, it simply routes.

On receipt, the recipient decrypts the wire message with the private key associated with the endpoint and processes the message.

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
  "to": "DID or key needed to construct next hop"
  "message": "<Base64(AuthCrypt or AnonCrypt(Application Layer Message)>"
}
```

The original Sender - the Agent that constructs the Application Layer Message - also constructs the first wrapping Forward message. No one other than the intended recipient can access any data elements of the Application Layer Message.

The recipient of a Forward message knows to use its own key to decrypt the message; if decryption doesn't work, then it has received the message in error.

The "to" field may contain a DID, or it may contain just a key. If it's a key, then the forwarding is within the current domain. If it's a DID, then the forward crosses a domain boundary.

In some cases, not enough is known to use AuthCrypt, so the message must be AnonCrypted. In other cases,
either encryption algorithm is possible, and the sender can choose whether they want to be known to the receiver.
Some receivers may refuse to forward messages from anonymous senders, but others may permit it; the spec allows either choice...

Forward messages are only used when the recipient has a duty to forward to some other party; sending
party X a Forward message where the target of the forward is X is a degenerate case that should be
optimized into a simple wire message instead. However, if X receives a request to forward a message
to X, X should unpackage the forward and examine the inner payload, for maximum robustness. 

##### Forward Routing

The normal case when an agent receives a Forward message is that the message is not intended for them; that's why it's a "Forward".
In such a case, the agent takes the inner wire message (the "message" field of the Forward message) and transmits it to the new target, if they can reach the new target directly--or, if they do not know the full route to the recipient, they construct a new Forward message, suitable for an agent "closer" to the recipient, name the more distant recipient as before, and retransmit.

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
