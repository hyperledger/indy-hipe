- Name: Wire Level Messages (JWM/JWEs)
- Author: Kyle Den Hartog, Stephen Curran (swcurran@gmail.com), Sam Curren (Sam@sovrin.org), Mike Lodder (Mike@sovrin.org)
- Start Date: 2018-07-10 (approximate, backdated)
- Feature Branch: https://github.com/kdenhartog/indy-sdk/tree/multiplex-rebase
- JIRA ticket: IS-1073
- HIPE PR: (leave this empty)
# Wire Messages
[summary]: #summary

There are two layers of messages that combine to enable **interoperable** self-sovereign identity Agent-to-Agent communication. At the highest level are Agent Messages - messages sent between Identities (sender, recievers) to accomplish some shared goal. For example, establishing a connection between identities, issuing a Verifiable Credential from an Issuer to a Holder or even the simple delivery of a text Instant Message from one person to another. Agent Messages are delivered via the second, lower layer of messaging - Wire. A Wire Message is a wrapper (envelope) around an Agent Message to permit sending the message from one Agent directly to another Agent. An Agent Message going from its Sender to its Receiver may be passed through a number of Agents, and a Wire Message is used for each hop of the journey.
# Motivation
[motivation]: #motivation

Wire messages are intended to be a standardized format built on the JWE spec that allows for all necessary information to encrypt, decrypt, and perform routing can be found in the message while remaining asynchronous. In this HIPE we'll describe the API of the Pack and Unpack functions. 

The purpose of this HIPE is to define how an Agent that needs to transport an arbitrary agent message delivers it to another agent through a direct (point-to-point) communication channel. A message created by a Sender Agent and intended for a Receiver Agent will usually be sent multiple times between Agents via Wire Messages in order to reach its ultimate destination. How this happens is not defined in this HIPE, but should be defined in another HIPE. This HIPE focuses specifically on the JSON format of messages as they move over the wire. This is also referred to as the wire messaging format.

Many aspects of this hipe have been derived from [JSON Web Encryption - RFC 7516](https://tools.ietf.org/html/rfc7516)Wire messages are intended to provide the following properties:

* provide a standard serialization format
* Handles encrypting messages for 1 or many receivers
* Keeps messaging protocol asynchronous

# Tutorial
[tutorial]: #tutorial

## Assumptions

For the purposes of this HIPE, the following are assumed about the sending and delivery of Wire Messages.

- Each Agent sending a Wire Message knows to what Agent the wire message is to be sent.
- Each Agent knows what encryption (if any) is appropriate for the wire message.
- If encryption is to be used, the sending Agent knows the appropriate public key (of a keypair controlled by the receiving Agent) to use.
- The sending Agent knows the physical endpoint to use for the receiver, and the appropriate Transport Protocol (https, zmq, etc.) to use in delivering the wire message.

> The term "Domain Endpoint" is defined in the Cross Domain Messaging HIPE. In short, this is assumed to be an Agency endpoint that receives messages for many Identities, each with many DIDs. Per that HIPE, all Domain Endpoints MUST be assumed to serve many Identities, even in the degenerate case implementation of an Identity self-hosting their Agent.

The assumptions can be made because either the message is being sent to an Agent within the sending Agent's domain and so the sender knows the internal configuration of Agents, or the message is being sent outside the sending Agent's domain and interoperability requirements are in force to define the sending Agent's behaviour.

## Example: Domain and DIDDoc

The example of Alice and Bob's domains are used for illustrative purposes in defining this HIPE.

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

For the purposes of this discussion we are defining the Wire Message Agent message flow to be:

> 1 --> 2 --> 8 --> 9 --> 3 --> 4

However, that flow is arbitrary. Even so, some Wire Message hops are required:

- 1 is the Sender Agent in this case and so must send the first or original message.
- 9 is the Domain Endpoint of Bob's domain and so must receive the message as a wire message
- 4 is the Receiver in this case and so must receive (and should be able to read) the first or original message.

## Wire Messages

A Wire Message is used to transport any Agent Message from one Agent directly to another. In our example message flow above, there are five Wire Messages sent, one for each hop in the flow. The process to send a Wire Message consists of the following steps:

- Call the standard function "pack()" (implemented in the Indy-SDK) to prepare the Agent Message
- Send the Wire Message using the transport protocol defined by the receiving endpoint
- Receive the Wire Message
- Call the standard function "unpack()" to retrieve the Agent Message from the Wire Message and potentially provenance of the message

An Agent sending a Wire Message must know information about the Agent to which it is sending.  That is, it must know its physical address (including the transport protocol to be used - https, zmq, etc.) and if the message is to be encrypted, the public key the receiving agent is expecting will be used for the message.

## The pack()/unpack() Functions

The pack() functions are implemented in the Indy-SDK and will evolve over time. The initial instance of pack() will have APIs built in that allow for a consumer of the APIs to be able The details of the outputs of packed messages are defined below. Additionally, there's a schema describing the intent of the key:value pairs below. 

Code for this might look like the following:

```
// Sending
tmsg = pack(msg, receivers, sender) // if sender_key is left off it will use AnonPack
send(toAgentEndpoint, tmsg)

// Receiving
tmsg = recv(myEndpoint)
msg = unpack(jwe, my_public_key) //outputs tmsg that was packed, with the sender's key if AuthPack was used
```

### Wire Message Formats


#### pack output (Authcrypted)

``` 
{
    "protected": "b64URLencoded({
        "enc": "xsalsa20poly1305",
        "typ": "JWM/1.0",
        "aad_hash_alg": "BLAKE2b",
        "cek_enc": "authcrypt"
    })"
    "recipients": [
        {
            "encrypted_key": <b64URLencode(encrypt(cek))>,
            "header": {
                "sender": <b64URLencode(anoncrypt(sender_pubkey))>,
                "kid": "b64URLencode(ver_key)"
            }
        },
    ],
    "aad": <b64URLencode(aad_hash_alg(b64URLencode(recipients)))>,
    "iv": <b64URLencode()>,
    "ciphertext": <b64URLencode(encrypt({'@type'...}, cek)>,
    "tag": <b64URLencode()>
}
```

#### pack output (Anoncrypted)
```
{
    "protected": "b64URLencoded({
        "enc": "xsalsa20poly1305",
        "typ": "JWM/1.0",
        "aad_hash_alg": "BLAKE2b",
        "cek_enc": "anoncrypt"
    })",
    "recipients": [
        {
            "encrypted_key": <b64URLencode(encrypt(cek))>,
            "header": {
                "kid": "b64URLencode(ver_key)",
            }
        },
    ],
    "aad": <b64URLencode(aad_hash_alg(b64URLencode(recipients)))>,
    "iv": <b64URLencode()>,
    "ciphertext": <b64URLencode(encrypt({'@type'...}, cek)>,
    "tag": <b64URLencode()>
}
```

## Schema
This spec is according [JSON Schema v0.7](https://json-schema.org/specification.html)
```json
{
    "id": "https://github.com/hyperledger/indy-agent/wiremessage.json",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Json Web Message format",
    "type": "object",
    "required": ["aad", "ciphertext", "iv", "protected", "recipients", "tag"],
    "properties": {
        "protected": {
            "type": "object",
            "description": "Additional authenticated message data",
            "required": ["enc", "typ", "aad_hash_alg", cek_alg],
            "properties": {
                "enc": {
                    "type": "string",
                    "enum": ["xsalsa20poly1305", "chacha20poly1305", "xchacha20poly1305", "aes256gcm"],
                    "description": "The authenticated encryption algorithm used to encrypt the ciphertext"
                },
                "typ": { 
                    "type": "string",
                    "description": "The message type. Ex: JWM/1.0"
                },
                "aad_hash_alg": {
                    "type": "string",
                    "enum": ["SHA512", "BLAKE2b", "BLAKE2s"],
                    "description": "The algorithm used to hash the recipients data to be put in the aad field"
                },
                "cek_alg": {
                    "type": "string",
                    "enum": ["xsalsa20poly1305", "chacha20poly1305", "xchacha20poly1305", "aes256gcm", 
                             "authcrypt", "anoncrypt"]
                }
            },
        },
        "recipients": {
            "type": "array",
            "description": "A list of the recipients who the message is encrypted for"
            "items": {
                "type": "object",
                "required": ["encrypted_key", "header"],
                "properties": {
                    "encrypted_key": {
                        "type": "string",
                        "description": "The key used for encrypting the ciphertext. This is encrypted either by authcrypting with the sender key in the header data or anoncrypted"
                    },
                    "header": {
                        "type": "object",
                        "required": ["kid"],
                        "description": "The recipient to whom this message will be sent",
                        "properties": {
                            "sender": {
                                "type": "string",
                                "description": "The anoncrypted verification key of the sender"
                            },
                            "kid": {
                                "type": "string",
                                "description": "The DID, key reference, or key of the recipient."
                            }
                        }
                    }
                }
            }
        },       
        "aad": {
            "type": "string",
            "description": "The hash of the recipients block base64 URL encoded value"
        },
        "iv": {
            "type": "string",
            "description": "base64 URL encoded nonce used to encrypt ciphertext"
        },
        "ciphertext": {
            "type": "string",
            "description": "base64 URL encoded authenticated encrypted message"
        },
        "tag": {
            "type": "string",
            "description": "Integrity checksum/tag to check ciphertext, protected, and iv"
        }
    }
}
```

# Drawbacks
[drawbacks]: #drawbacks

The current implementation of the "pack()" message is currently Hyperledger Indy specific. It is based on common crypto libraries ([NaCl](https://nacl.cr.yp.to/)), but the wrappers are not commonly used outside of Indy. There's currently work being done to fine alignment on a cross-ecosystem interopable protocol, but this hasn't been achieved yet. This work will hopefully bridge this gap.

# Rationale and alternatives
[alternatives]: #alternatives

As the [JWE](https://tools.ietf.org/html/rfc7516) standard currently stands, it does not follow this format. We're actively working with the lead writer of the JWE spec to find alignment and are hopeful the changes needed can be added.

# Prior art
[prior-art]: #prior-art

The [JWE](https://tools.ietf.org/html/rfc7516) family of encryption methods.

# Unresolved questions
[unresolved]: #unresolved-questions

- How transport protocols (https, zmq, etc.) will be be used to send Wire Messages?
    - These will need to be defined using seperate HIPEs. For example, HTTP might POST a message and place it in the body of the HTTP POST.
- How will the wire messages work with routing tables to pass a message through a domain, potentially over various transport protocols?
    - There's not much certainty whether routing tables or some other mechanism will be used. This needs to be defined in another HIPE.
- If the wire protocol fails, how is that failure passed back to those involved in the transmission?
    - TBD
