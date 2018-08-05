- Name: transport-layer-messaging
- Author: Stephen Curran (swcurran@gmail.com)
- Start Date: 2018-07-09
- PR: 
- Jira Issue: 

# Summary
[summary]: #summary

There are (at least) two layers of messages that combine to enable self-sovereign identity Agent-to-Agent communication. At the highest level (that we are considering) are Agent messages - messages sent between Identities to accomplish some shared goal. For example, establishing a connection between identities, issuing a Verifiable Credential from an Issuer to a Holder or even the simple delivery of a text Instant Message from one person to another.

Agent Messages are delivered via the second, lower layer of messaging - Wire. A Wire Message is a wrapper (envelope) around an Agent Message to permit sending the message from one Agent directly to another Agent. An Agent Message going from its Sender to its Receiver may be passed through a number of Agents, and a Wire Message is used for each hop of the journey.

There is a family of Agent Messages (currently consisting of just one Message Type) that are used to route messages through a network of Agents in both the sender and receiver's domain. This HIPE provides the specification of the "Forward" Agent Message Type - an envelope that indicates the destination of the Message without revealing anything about the message.

In order to send a message from one Identity to another, the sending Identity must know a minimum about the receiver's domain - the receiver's configuration of Agents. This HIPE outlines how a domain must present itself to enable the sender to know enough to be able to send a message to an Agent in the domain.

This HIPE focuses on Wire Messages, the "Forward" Agent Message, and how a domain must be configured to support the receipt of messages. The goal is to define the rules that domains must adhere to enable the delivery of Agent messages from a Sending Agent to a Receiver Agent in a secure and privacy-preserving manner.

# Motivation
[motivation]: #motivation

The purpose of this HIPE is to define the Transport Layer Messaging such that we can ignore the transport of messages as we discuss the much richer Agent Messaging types and interactions. That is, we can assume that there is no need to include in an Agent message anything about how to route the message to the Receiver - it just magically happens. Alice (via her App Agent) sends a message to Bob, and (because of implementations based on this HIPE) we can ignore how the actual message got to Bob's App Agent.

Put another way - this HIPE is about envelopes. It defines a way to put a message - any message - into an envelope, put it into an outbound mailbox and have it magically appear in the Receiver's inbound mailbox in a secure and privacy-preserving manner. Once we have that, we can focus on letters and not how letters are sent.

Most importantly for Agent to Agent interoperability, this HIPE clearly defines the assumptions necessary to deliver a message from one domain to another - e.g. what exactly does Alice have to know about Bob's domain to send Bob a message? For messages moving within a domain there will be fewer constraints, allowing for more elaborate capabilities that are implementation specific. As long as the implementation supports the assumptions across domains, interoperability is possible.

# Tutorial
[tutorial]: #tutorial

## Core Messaging Goals

These are vital design goals for this HIPE:

1. **Sender Encapsulation**: We must minimize what the receiver has to know about the domain (routing tree or agent infrastructure) of the sender in order for them to communicate.
2. **Receiver Encapsulation**: We must minimize what the sender has to know about the domain (routing tree or agent infrastructure) of the receiver in order for them to communicate.
3. **Independent Keys**: Private signing keys should not be shared between agents; each agent should be separately identifiable for accounting and authorization/revocation purposes.
4. **Internet Transport independence**: The same rules should apply, and the same guarantees obtained, no matter what internet transport is used to move messages - e.g. HTTPS, ZeroMQ, etc.

## Assumptions

The following are assumptions upon which this HIPE is based, with (as necessary) the rationale behind each assumption.

### Terminology in this HIPE

The following terms are used in this HIPE with the following meanings:

- Domain - a set of Agents collaborating on behalf of an Identity
  - It's assumed that the Agents of a domain were developed by a single vendor and so know more about each other than about Agents in another domain.
  - An example of two Domains is provided in the image below.
- App Agents - the Agents involved in sending (creating) and receiving (processing) a message
  - Sender - the Agent sending an Agent Message
  - Receiver - the Agent receiving an Agent Message
  - **Note**: A message may pass through many Agents between the Sender and Receiver
- Domain Endpoint - a shared physical endpoint for messages into domains
  - Shared by many identities (e.g. https://endpoint.agentsRus.com)
  - Agency - the handler for messages sent to the Domain Endpoint.
    - E.g. the "domain endpoint" is passive, "agency" is active.
- Routing Agent - the single identity-controlled entry point for a domain per relationship
  - A message delivered to a Domain Endpoint is always passed directly to the Routing Agent for a domain
- DID - reference to the literal Decentralized ID text
  - e.g. did:sov:1234abcd
- DID#key - reference to the DID appended with "#" and a specific key from the DIDDoc
  - e.g. did:sov:1234abcd#domain
  - **Note**: The #key is NOT the actual Public Key - it's a reference to an entry in the DIDDoc that contains the Public Key.

#### DIDDocs

The term "DIDDoc" is used in this HIPE as it is defined in the [DID Specification](https://w3c-ccg.github.io/did-spec/):

- a collection of public keys and endpoints,
- controlled by an identity,
- associated with a DID, and
- used for a relationship.

A DID can be resolved to get its corresponding DIDDoc by any Agent that needs access to the DIDDoc. This is true whether talking about a DID on the Public Ledger, or a DID persisted to a microledger. In the case of a microledger, it's the (implementation specific) domain's responsibility to ensure such resolution is available to all Agents requiring it.

### Messages are Private

Agent Messages sent from a Sender to a Receiver are required to be private. That is, the Sender will encrypt the message with a public key for the Receiver. Any agent in between the Sender and Receiver will know only to whom the message is intended (by DID and possibly key within the DID), not anything about the message.

### The Sender Knows The Receiver

This HIPE assumes that the Sender knows the Receiver's DID and, within the DIDDoc for that DID, the key to use for the Receiver's Agent. How the Sender knows the DID and key to send the message is not defined within this HIPE - that is higher level concern.

The Receiver's DID may be a public or pairwise DID, and may be on a Public Ledger or a microledger.

## Example: Domain and DIDDoc

The following is an example of an arbitrary pair of domains that will be helpful in defining the requirements in this HIPE.

![Example Domains: Alice and Bob](domains.jpg)

In the diagram above:

- Alice has
  - 1 App Agent - "1"
  - 1 Routing Agent - "2"
  - 1 Domain Endpoint - "8"
- Bob has
  - 3 App Agents - "4", "5" and "6"
    - "6" is an App Agent in the cloud, "4" and "5" are physical devices.
  - 1 Routing Agent - "3"
  - 1 Domain Endpoint - "9"

### Bob's DID for his Relationship with Alice

Bob’s domain has 3 devices he uses for processing messages - two phones (4 and 5) and a cloud-based agent (6). However, in Bob's relationship with Alice, he ONLY uses one phone (4) and the cloud-based agent (6). Thus the key for device 5 is left out of the DIDDoc (see below).

Note that the key for the Routing Agent (3) is called "routing". This is an example of the kind of convention needed to allow the Sender's agents to know the keys for Agents with a designated role in the receiving domain.

```json
{
  "@context": "https://w3id.org/did/v1",
  "id": "did:sov:1234abcd",
  "publicKey": [
    {"id": "did:sov:1234abcd#routing", "type": "RsaVerificationKey2018",  "owner": "did:sov:1234abcd","publicKeyPem": "-----BEGIN PUBLIC X…”}",
    {"id": "did:sov:1234abcd#4", "type": "RsaVerificationKey2018",  "owner": "did:sov:1234abcd","publicKeyPem": "-----BEGIN PUBLIC 9…”}",
    {"id": "did:sov:1234abcd#6", "type": "RsaVerificationKey2018",  "owner": "did:sov:1234abcd","publicKeyPem": "-----BEGIN PUBLIC A…”}
  ],
  "authentication": [
    {"type": "RsaSignatureAuthentication2018", "publicKey": "did:sov:1234abcd#4"}
  ],
  "service": [
    {"type": "Agency", "serviceEndpoint": "did:sov:fghi8377464" }
    // or "serviceEndpoint": "https://example.com/endpoint/8377464" and add the #domain key (above)
  ]
}
```

For the purposes of this discussion we are defining the message flow to be:

> 1 --> 2 --> 8 --> 9 --> 3 --> 4

However, that flow is arbitrary. Even so, some Wire Message hops are required:

- 1 is the Sender and so must send the first message.
- 9 is the Domain Endpoint of Bob's domain and so must receive the message
- 4 is the Receiver and so must receive the message.

In the section below on Domain Configuration, we will also declare that:

- The Routing Agent for Bob's Domain (3) must receive the message from 9

## Wire Messages

A Wire Message is used to transport any Agent Message from one Agent directly to another. In our example message flow above, there are five Wire Messages sent, one for each hop in the flow. The process to send a Wire Message consists of the following steps:

- Call the standard function "pack()" (implemented in the Indy-SDK) to prepare the Agent Message
- Send the Wire Message using the transport protocol defined by the receiving endpoint
- Receive the Wire Message
- Call the standard function "unpack()" to retrieve the Agent Message from the Wire Message

An Agent sending a Wire Message must know information about the Agent to which it is sending.  That is, it must know its physical address (including the transport protocol to be used - https, zmq, etc.) and if the message is to be encrypted, the public key the receiving agent is expecting will be used for the message.

Code for this might look like the following:

```
// Sending
tmsg = pack(msg, toKey) // toKey could be left off - if so, no encryption
send(toAgentEndpoint, tmsg)

// Receiving
tmsg = recv(myEndpoint)
msg = unpack(tmsg, privKey) // If encrypted
```

Once the `msg` value has been extracted from the Wire Message, it is processed as an Agent message. That is, its type is evaluated and the entire message given to a handler configured for that message type.

### The pack()/unpack() Functions

The pack() function is implemented in the Indy-SDK and will evolve over time. The initial instance of pack() includes three variations, only the first two of which are used for Wire Messages. The third is used by the Routing family of Agent Messages.

```
pack(msg, null)  ⇒ JOSEhdr & “.” & base64url(msg)
pack(msg, toKey) ⇒ JOSEhdr & “.” & base64url( anonCrypt(msg, toKey) )
pack(msg, toKey, myPrivKey) ⇒ JOSEhdr & “.” & base64url( authCrypt(msg, toKey, myPrivKey) )
```

The JOSEhdr is discussed in the next section.

### The Provisional JOSE Header

The encryption algorithms in the initial version of pack() (anonCrypt, authCrypt) use a trusted, well-known cryptographic library base (NaCL), but are currently implemented only in the Indy-SDK. Over time, we expect the Indy-SDK will move to use more broadly implemented algorithms, most likely the proposed JSON Web Messages (JMW) format. Since we expect to use a format that includes a [JSON Object and Signing Encryption](http://jose.readthedocs.io/en/latest/) (JOSE) Header, the initial version of pack() will also implement a JOSE header as follows.

We anticipate that the typ attribute of a JWM will be ‘jwm’. Using a provisional type (`typ`) will make it easy to detect the difference between our initial format and the anticipated JWM format, and propose that the typ attribute of the provisional format be `x-b64nacl`.

As noted above, there are three expected algorithms within this type: unencrypted, anonCrypt, and authCrypt. We will use the `alg` attribute of the header to indicate which of these forms are present in the message. For brevity, we’ll use `x-plain`, `x-anon`, `x-auth` values for the `alg` attribute.

Thus, for the three variation so of the pack() function, the JOSE headers will be:

```
{"typ":"x-b64nacl","alg":"x-plain"}
{"typ":"x-b64nacl","alg":"x-anon"}
{"typ":"x-b64nacl","alg":"x-auth"}
```

The JOSE header is base64Url encoded, and prepended to the base64Url encoded Agent Message, with a period (.) delimiter.  As such, the following is an example plaintext Agent Message with a JOSE header:

```
eyJ0eXAiOiJ4LWI2NG5hY2wiLCJhbGciOiJ4LXBsYWluIn0=.ewogICJ0eXBlIiA6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9pbS8xLjAvdGV4dCIKICAidGV4dCIgIDogIkhlbGxvISIKfQ==
```

To unpack the message, extract the text up to the ".":

eyJ0eXAiOiJ4LWI2NG5hY2wiLCJhbGciOiJ4LXBsYWluIn0=

Then, Base64Url decode to get the JOSE Header:

{"typ":"x-b64nacl","alg":"x-plain"}

You can now inspect the typ attribute to verify that the provisional format is being used, and the alg attribute to determine how to process the rest of the message.

As newer versions of the pack() functions are released, the JOSE headers will be correspondingly revised to support a backwards-compatible evolution.

#### Notes

Approved values for alg: https://tools.ietf.org/html/rfc7518#section-4.1
Approved values for typ: https://tools.ietf.org/html/rfc7515#section-4.1.9 and https://www.iana.org/assignments/media-types/media-types.xhtml

## Agent Message Format

> **To Do**: Is this defined in the Core Message Spec HIPE? If not, add here.

## Interoperability Assumptions

A key goal for interoperability is that we want other domains to know just enough about the configuration of a domain to which they are delivering a message. The following walks through those minimum requirements.

### Required: The DID and DIDDoc

As noted in the assumptions, the Sender has the DID of the Receiver, and knows the key from the DIDDoc to use for the Receiver.

> Example: Alice wants to send a message from her phone (1) to Bob's phone (4). She has Bob's B:did@A:B, the DID/DIDDoc Bob created and gave to Alice to use for their relationship. Alice created A:did@A:B and gave that to Bob, but we don't need to use that in this example. The contents of the DIDDoc for B:did@A:B is presented above.

### Required: End-to-End encryption of the Agent Message

The Agent Message from the Sender must be hidden from all Agents other than the Receiver. Thus, it must be encrypted with the Public Key of the Receiver. Based on our assumptions, the Sender can get the Public Key of the Receiver because they know the DID#key string, can resolve the DID to the DIDDoc and find the public key associated with DID#key. In our example above, that is the key associated with "did:sov:1234abcd#4".

Most Sender-to-Receiver messages will be sent between parties that know each other's public keys. When that is true, the Sender will (usually) AuthCrypt the message. If that is not the case, or for some other reason the Sender does not want to AuthCrypt the message, AnonCrypt will be used. In either case, the underlying `pack()` function in the Indy-SDK includes the encryption method in the JOSEhdr part of its output.

To route the message to the Receiver, the Sender sends a "Forward" message with the "To" address being the DID#key of the Receiver.

```json
{
  "type" : "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routing/1.0/forward"
  "to"   : "did:sov:1234abcd#4"
  "from" : "#1"  // The key used i AuthCrypt'ing the message
  "msg"  : "<pack(AgentMessage,valueOf(did:sov:1234abcd#4), privKey(A.did@A:B#1))>"
}
```

**Notes**

- the *type* value is in the precise URI format for the "forward" message
- Indy-SDK's "pack" function is used to AuthCrypt the message using the receiver's public key and the sender's private key.
  - If the receiver does not know the sender's public key, AnonCrypt is used.
- Since AuthCrypt is used for the message, the Receiver must know which private key was used to send the message. As such the "from" field is included in the message so that the Receiver can find the public key from the Sender's DIDDoc.
  - Note that only the #key fragment is included, as the Receiver is assumed to be able to infer the sender's DID from the "to" DID - the pairwise relationship.

> **To Do**: The need to specify the Sender's Key has not been discussed. When a DID could only have a single Key, knowing the DID implied knowledge of the key used for AuthCrypt signing. With multiple keys, this must be more explicit.

### Required: Minimize information available to the Shared Domain Endpoint

We want to minimize the knowledge about the Receiver of the App Layer message for minimally trusted agents. In this case, "minimally trusted" are all agents before the designated "Routing Agent" for the Receiver. The "Routing Agent" must know the exact destination (B:did@A:B#key) of the Receiver, but Agents handling the message prior to the Routing Agent do not - they just need the DID (B:did@A:B) of the Receiver.

To hide other than the minimum information, the Sender wraps the "Forward" message in a second forward message, this time for the Routing Agent of the Receiver (`3` in our example). The Sender must be able to get the public key of the Routing Agent from the DIDDoc.

> **TO DO**: Define a convention such that the Routing Agent key is known to the Sender from the DIDDoc.

The Sender prepares the following message:

```json
{
  "type" : "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routing/1.0/forward"
  "to"   : "did:sov:1234abcd"
  "msg"  : "<pack(ForwardMessage,valueOf(did:sov:1234abcd#routing))>"
}
```

**Notes**

- Indy-SDK's "pack" function is used to Anon encrypt the message using the Routing Agent's public key.
- the "from" field is not needed in this case since the message is Anon encrypted.

The Sender can now send the message on its way via the first of the Wire messages. In our example, it sends the message to 2, who in turn sends it to 8. That of course, is arbitrary - the Sender's Domain could have any configuration of Agents.

The diagram below shows the required use of the 'forward' message type to encrypt the message all the way to the Receiver, and again all the way to the Routing Agent.

![Example Forward Messages](forwarding.jpg)

### Required: Cross Domain Wire Message Encryption

While within a domain the Agents may choose to use encryption or not when sending Wire Messages from Agent to Agent, encryption **must** be used when sending a Wire Message into the Receiver's domain. The shared Domain Endpoint (Agency) unpack()'s the encrypted Wire Message and based on the "To" field value (the DID), sends the message to a designated Agent for that DID. How the Domain Endpoint knows where to send the message is implementation specific - likely some sort of dynamic DID-to-Agent routing table. Typically the message will be sent directly to the Routing Agent, although it doesn't have to be. However, the message must eventually get to the Routing Agent (3 in our example) as the messaging being forwarded has been encrypted for it.

### Required: The Routing Agent Processes the Outer Forward

When the Routing Agent (eventually) receives the message, it determines it is the target of the outer Forward and so decrypts the `msg` value to reveal the inner "Forward" message. Recall that this inner Forward includes the full "DID#key" necessary to route the message to the intended Receiver agent. The Routing Agent uses its (implementation specific) knowledge to map from the DID#key to the Receiver, possibly via intermediary Agents.

### Required: The Receiver App Agent Decrypts/Processes the App Layer Message

When the intended Receiver Agent receives the message, it determines it is the target of the Forward and decrypts the payload and processes the message.

### Exposed Data

The following summarizes the information needed by the sender's agents:

- The DID to use for the relationship, and it's related DIDDoc
- Within the DIDDoc:
  - The Domain Endpoint's physical endpoint and public key, including how to identify that key within the DIDDoc
  - The Routing Agent's public key, including how to identify that key within the DIDDoc
  - The Receiver of the Application Layer Message's public key

Thus, every Messaging DIDDoc is assumed to have at least one endpoint and 3 keys:

- The endpoint for the Domain Endpoint
- The public key for the Domain Endpoint
- The public key for the Routing Agent
- The public key for the Receiver Agent

The DIDDoc will have an additional key for each additional App Layer Message Receiver.

#### Degenerate Cases

The sequence above requires there are at least three Agents within every domain, and there could be many more. However, what if there are only 2 or even 1 Agent in a domain?

The HIPE requirement in those degenerate cases is that the DIDDoc still contain the same data (one endpoint, three public keys), and the domain implementation handles "Agents with multiple roles" use case. The DIDDoc could reuse the same key for different purposes, or could have an Agent with different keys for different purposes to mask the simplified Agent structure.

### Data Not Exposed

Given the sequence specified above, following data is **NOT** exposed to the sender's agents:

- Routing-only Agents within the receiver's domain
- Agents the identity has that it chooses not to include in the DIDDoc
- The physical endpoints of Agents within the receiver's domain (other than the Domain Endpoint)
  - The physical endpoints and, as required, associated public keys, are shared as needed within the receiver's domain.

## Using a DID as the Domain Endpoint Endpoint

Recall that a DID used for Agent Messaging must have accessible through it's DIDDoc the endpoint address and public key for the shared Domain Endpoint. A recommended best practice is that rather than putting both of those pieces of information into each pairwise DIDDoc, the Agency provide the users of the Agency (Identities) with a publicly resolvable DID for the shared Domain Endpoint that the Agency controls.

That approach allows the Agency to rotate the keys for the endpoint as necessary without requiring updates be made to the DIDDocs created by the Agency users. If the DIDDocs of every Agency user contain the actual endpoint and public key of the Domain Endpoint, every DIDDoc created in the Agency would have to be updated when the Domain Endpoint public key is rotated (or the endpoint is changed).

By referencing a DID as the endpoint, the DIDDocs of DIDs owned by users of the Agency would only need to be updated when changing the Domain Endpoint for a relationship - such as when changing Agencies. Such events are likely to be far rarer than rotating the key of the Domain Endpoint.

This best practice **requires** that Agents know that when an endpoint in a DIDDoc is a DID, they **must** resolve that DID to retrieve the actual endpoint and public key.

## Network Protocol

The lower level network protocol (https, zmq, etc.) used for sending message must be known, presumably by the protocol implied by the Agent endpoints. To be defined in a separate HIPE is how a blob of text is to be delivered for each supported protocol.

### Response

The following are the possible responses to the message:

- OK
- Invalid Message
  - The message could not be decoded
- Not Handled
  - The message type is not handled by the Agent
- Not Found
  - The message could not be processed - e.g. a forward with an unknown "to" value.

#### Response Issues

Should the message response be synchronous or asynchronous?  If the wire protocol fails, how is that failure passed back to those involved in the transmission?

If it is an asynchronous response, the message format must add a nonce and callback address, which seems onerous. If synchronous and the message decryption and determination if the message can be processed will take too long for a synchronous response, perhaps just an OK/Error response is acceptable based on the receipt of the wire message.

If the wire protocol fails, notifying the Application Layer message sender might be needed.

A reason for using a synchronous response to at least checking the ability to decrypt the message is cache handling. Agents might cache DID information for performance (fewer trips to the ledger) and so messages might be invalid due to undetected key rotations. If the "Invalid Message" response was synchronously returned to the Sender, the Sender could resolve the DID it was using and retry without breaking the higher level protocol.

### Application Layer Error Handling

If the Transport Messages fail at any point, there is no way as specified to notify the original Sender. None of the Agents involved in the Transport know who sent the message, only who is supposed to receive it. To notify the Sender of an error, a ID for the Sender is needed - perhaps a resolvable DID or some other ephemeral ID that would work across domains.  Without that, only a timeout is possible for a User to be informed of a Transport-level error.

**Question**: Should this HIPE include this level of error notification?

# Message Types

The following Message Types are defined in this HIPE.

## Core:Routing:1.0:Forward

The core message type "forward", version 1.0 of the "routing" family is defined in this HIPE. An example of the message is the following:

```json
{
  "type" : "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routing/1.0/forward"
  "to"   : "did:sov:1234abcd#4"
  "from" : "#1"  // Optional: The key used to AuthCrypt the message
  "msg"  : "<pack(AgentMessage,valueOf(did:sov:1234abcd#4), privKey(A.did@A:B#1))>"
}
```

The `to` field is required and takes one of two forms:

- A DID without a key reference (e.g. `did:sov:1234abcd`)
- A DID with a key reference (e.g. `did:sov:1234abcd#4`)

The first form is used only when the `msg` field itself contains a `forward` message that includes the second format. It is used when sending forward messages across one or more agents that do not need to know the details of a domain. The Receiver of the message is the designated `Routing Agent` in a domain, as it controls the key used to decrypt messages sent to the domain, but not a specific Agent.

The second form is used when the precise key (and hence, agent controlling that key) used to encrypt the Agent Message placed in the `msg` field.

The `from` field is used and required only when a message is AuthCrypt'd by the Sender. The Receiver of the message can determine, based on the DID in the `to` field the corresponding pairwise DID of the Sender. However, it cannot from that determine the specific key used by the Sender to AuthCrypt the message. The `from` field provides that missing information. The exclusion of the DID in the from field reduces the information visible in the message.

The `msg` field calls the Indy-SDK `pack()` function to encrypt the Agent Message to be forwarded. The Sender calls the `pack()` with the suitable arguments to AnonCrypt or AuthCrypt the message.

# Reference
[reference]: #reference

The current summary of AuthCrypt and AnonCrypt are documented [here](https://github.com/hyperledger/indy-hipe/pull/9) - see May 29th comment from vimmerru.

# Drawbacks
[drawbacks]: #drawbacks

The need to double-encrypt the message, as outlined in the second diagram above to, for privacy, hide what seems to be a fairly limited piece of data (the `#key` fragment of the `to` field) seems onerous. A challenge will be to be able to explain to others implementing the protocol why this requirement is included. Only those that have a sufficient background in privacy are qualified to determine the extra layer of encryption is not needed. Until then, we'll leave it in.

# Rationale and alternatives
[alternatives]: #alternatives

A number of discussions were held about this HIPE. In those discussions, the rationale for the HIPE evolved into the text, and the alternatives were eliminated. See prior versions of the HIPE for details.

# Prior art
[prior-art]: #prior-art

N/A


# Unresolved questions
[unresolved]: #unresolved-questions

The following remain unresolved:

- How does a Sender know which of the keys in the Receiver's DIDDoc should be used for the Routing Agent?  A clear convention is necessary for this.
- If the endpoint and key for the shared Domain Endpoint are explicitly placed into the Receiver's DIDDoc, a clear convention is needed for determining which key is for the Domain Endpoint.
  - If the convention that the DIDDoc endpoint is a DID, it is understood that the Agent sending the Wire Message to the Domain Endpoint must resolve the endpoint DID in the DIDDoc to get the physical endpoint and public key for the Domain Endpoint.
  - However, if there are multiple endpoints in the DIDDoc, the Sender must know which endpoint is for the shared Domain Endpoint.
- It may be appropriate to have a convention in the DIDDoc to designate which keys (and potentially, endpoints) are used for different roles in the Domain.  For example:
  - A defined list of roles.
  - A convention for determining the roles associated with a key.
- Error handling at the Wire Message level.
- How transport protocols (https, zmq, etc.) will be be used to send Wire Messages