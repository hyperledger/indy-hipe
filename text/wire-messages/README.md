- Name: wire-messages
- Author: Stephen Curran (swcurran@gmail.com)
- Start Date: 2018-08-13
- PR: 
- Jira Issue: 

# Summary
[summary]: #summary

There are two layers of messages that combine to enable **interoperable** self-sovereign identity Agent-to-Agent communication. At the highest level are Agent Messages - messages sent between Identities to accomplish some shared goal. For example, establishing a connection between identities, issuing a Verifiable Credential from an Issuer to a Holder or even the simple delivery of a text Instant Message from one person to another. Agent Messages are delivered via the second, lower layer of messaging - Wire. A Wire Message is a wrapper (envelope) around an Agent Message to permit sending the message from one Agent directly to another Agent. An Agent Message going from its Sender to its Receiver may be passed through a number of Agents, and a Wire Message is used for each hop of the journey.

This HIPE addresses only Wire Messages. There are a series of related HIPEs that combine with this HIPE to address the interoperability, including in particular, Agent Messages, DIDDoc Conventions, and Cross Domain Messaging. Those HIPEs should be considered together in understanding Agent-to-Agent interoperability.

# Motivation
[motivation]: #motivation

The purpose of this HIPE is to define how an Agent that needs to transport an arbitrary Agent Message delivers it to another Agent through a direct (point-to-point) communication channel. A message created by a Sender Agent and intended for a Receiver Agent will usually be sent multiple times between Agents via Wire Messages in order to reach it's ultimate destination.

# Tutorial
[tutorial]: #tutorial

## Assumptions

For the purposes of this HIPE, the following are assumed about the sending and delivery of Wire Messages.

- Each Agent sending a Wire Message knows to what Agent the wire message is to be sent.
- Each Agent knows what encryption (if any) is appropriate for the wire message.
- If encryption is to be used, the sending Agent knows the appropriate public key (of a keypair controlled by the receiving Agent) to use.
- The sending Agent knows the physical endpoint to use for the receiver, and the appropriate Internet Transport Protocol (https, zmq, etc.) to use in delivering the wire message.

> The term "shared Domain Endpoint" is defined in the Cross Domain Messaging HIPE. In short, this is assumed to be an Agency endpoint that receives messages for many Identities, each with many DIDs.

The assumptions can be made because either the message is being sent to an Agent within the sending Agent's domain, and so the sender knows the internal configuration of Agents, or the message is being sent outside the sending Agent's domain, and interoperability requirements are in force to define the sending Agent's behaviour.

## Example: Domain and DIDDoc

The example of Alice and Bob's domains are used for illustrative purposes in defining this HIPE.

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

For the purposes of this discussion we are defining the Wire Message Agent message flow to be:

> 1 --> 2 --> 8 --> 9 --> 3 --> 4

However, that flow is arbitrary. Even so, some Wire Message hops are required:

- 1 is the Sender and so must send the first message.
- 9 is the Domain Endpoint of Bob's domain and so must receive the message
- 4 is the Receiver and so must receive the message.

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
msg = unpack(tmsg, myPrivKey)
```

Once the `msg` value has been extracted from the Wire Message, it is processed as an Agent Message. That is, its type is evaluated and the entire message given to a handler configured for that message type.

### The pack()/unpack() Functions

The pack() function is implemented in the Indy-SDK and will evolve over time. The initial instance of pack() includes three variations, only the first two of which are used for Wire Messages. The third is used by the Routing family of Agent Messages (defined in the Cross Domain Messaging HIPE).

```
pack(msg, null)  ⇒ JOSEhdr & “.” & base64url(msg)
pack(msg, toKey) ⇒ JOSEhdr & “.” & base64url( anonCrypt(msg, toKey) )
pack(msg, toKey, myPrivKey) ⇒ JOSEhdr & “.” & base64url( authCrypt(msg, toKey, myPrivKey) )
```

The unpack() function returns the decoded message.

If the message being unpack()'d was pack()'d in the third form - e.g. signed by the sender using the Indy-SDK "authcrypt" mechanism, the unpack() function also returns the public key that was used to sign the message. This is necessary so that the receiving Agent can determine which key in the sender's DIDDoc was used to sign the message - and hence, which key should be used for a reply message.

The JOSEhdr is discussed in the next section.

### *Provisional* JOSE Header

The encryption methods in the initial version of pack() (anonCrypt, authCrypt) use a trusted, well-known cryptographic library base (NaCl), but are currently implemented only in the Indy-SDK. Over time, we expect the Indy-SDK will move to use more broadly known protocols, most likely the proposed JSON Web Messages (JMW) format. Since we expect to use a format that includes a [JSON Object and Signing Encryption](http://jose.readthedocs.io/en/latest/) (JOSE) Header, the version of pack() in the Indy-SDK will implement a JOSE header as follows.

We anticipate that the `typ` attribute of a JWM will be ‘`jwm`’. Using a provisional type (`typ`) will make it easy to detect the difference between our initial format and the anticipated JWM format. The provisional `typ` attribute for the first version of `pack()` will be `x-b64nacl`.

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

```
eyJ0eXAiOiJ4LWI2NG5hY2wiLCJhbGciOiJ4LXBsYWluIn0=
```

Then, Base64Url decode to get the JOSE Header:

```
{"typ":"x-b64nacl","alg":"x-plain"}
```

You can now inspect the typ attribute to verify that the provisional format is being used, and the alg attribute to determine how to process the rest of the message.

As newer versions of the pack() functions are released, the JOSE headers will be correspondingly revised to support a backwards-compatible evolution.

#### Notes - JOSE

Approved values for alg: https://tools.ietf.org/html/rfc7518#section-4.1
Approved values for typ: https://tools.ietf.org/html/rfc7515#section-4.1.9 and https://www.iana.org/assignments/media-types/media-types.xhtml

### Response

The following are the possible responses to the message:

- OK
- Invalid Message
  - The message could not be decoded or processed

# Reference
[reference]: #reference

The current summary of AuthCrypt and AnonCrypt are documented [here](https://github.com/hyperledger/indy-hipe/pull/9) - see May 29th comment from vimmerru.

References to the various messaging standards (JOSE, etc.) are listed earlier in the text.

# Drawbacks
[drawbacks]: #drawbacks

The current implementation of the "pack()" message is currently Hyperledger Indy specific. It is based on common crypto libraries ([NaCl](https://nacl.cr.yp.to/)), but the wrappers are not commonly used outside of Indy. That said, the Indy crypto libraries have been separated out into a separate repo from Indy, enabling them to be used elsewhere.

Each self-sovereign identity ecosystem (e.g. uPort, Veres-One, DIF Hub) is moving forward with a Wire Message protocol that is sufficient for their needs. At some point it will be important to merge these approaches to enable cross-ecosystem interoperability.

# Rationale and alternatives
[alternatives]: #alternatives

As the [JWE](https://tools.ietf.org/html/rfc7516) family expands to possibly include a new standard "JWM" (JSON Web Messages) protocol, the "pack()" could be upgraded to include that standard. The purpose of the JOSE header in the Wire Message format is to ease that evolution by supporting multiple Wire Message formats at the same time.

# Prior art
[prior-art]: #prior-art

The [JWE](https://tools.ietf.org/html/rfc7516) family of encryption methods.

# Unresolved questions
[unresolved]: #unresolved-questions

- How transport protocols (https, zmq, etc.) will be be used to send Wire Messages
- Should the Wire Message response be synchronous or asynchronous?  If the wire protocol fails, how is that failure passed back to those involved in the transmission?
  - A reason for using a synchronous response to at least checking the ability to decrypt the message is cache handling. Agents might cache public key information for performance reasons (fewer DID resolutions) and so messages might be invalid due to undetected key rotations. If the "Invalid Message" response was synchronously returned to the Sender, the Sender could resolve the DID it was using and retry without breaking the higher level protocol.