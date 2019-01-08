- Name: Wire Level Messages (JWM/JWEs)
- Author: Kyle Den Hartog(kyle.denhartog@evernym.com), Stephen Curran (swcurran@gmail.com), Sam Curren (Sam@sovrin.org), Mike Lodder (Mike@sovrin.org)
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
        "alg": "Authcrypt",
        "recipients": [
            {
                "encrypted_key": anoncrypt(authcrypted_cek|sender_vk|nonce)
                "header": {
                    "kid": "base58encode(recipient_verkey)"
                }
            },
        ],
    })"
    "iv": <b64URLencode()>,
    "ciphertext": <b64URLencode(encrypt({'@type'...}, cek)>,
    "tag": <b64URLencode()>
}
```

##### pack example (Authcrypt)
This is an example of an outputted message encrypting "Hello World" for two verkeys.

```json
{
  "protected": "eyJlbmMiOiJ4Y2hhY2hhMjBwb2x5MTMwNSIsInR5cCI6IkpXTS8xLjAiLCJhbGciOiJBdXRoY3J5cHQiLCJyZWNpcGllbnRzIjpbeyJlbmNyeXB0ZWRfa2V5IjoiV3czVkU1eHFiM2wwSzFhY2FNNW1haERSWV9KY2tEZ3dXX0wzNjJxUVZ5UlFwOXdjVkJHYmVjUUNiYVRaU2ZDYzVQTE5FRWYtYXdRTUw4cmZ4SkRGajJZOXFZTWZYbm1RRVI1WmVlTGd1Y05jZHRneEgtM0wtLVczR3hvY2JJSGhsU05VTWc5VkpzdlZFQ1VYOWplLWNWLTVSRkRUemJ1UGFFdlZzbmdVTWNPMnNtQTg2M1J0RC1iMzF4QUFuV1J3eWZUeFZSY3FYNndSMncwMm52MllibkhXZmdCYTd5X1pia2lpSWlLTElENmZPdE9nNmE5MGx5NW9jMmVrOV9MbXBwUUJCZ1hYcnk4YVI3blRGbFlCc29TMmU5Yz0iLCJoZWFkZXIiOnsia2lkIjoiR0oxU3pvV3phdlFZZk5MOVhrYUpkclFlamZ6dE40WHFkc2lWNGN0M0xYS0wifX0seyJlbmNyeXB0ZWRfa2V5Ijoid2FIcWJaLWFuc3M2N1pMNEdyMmVYMkdDckNKVkJpUjI3TDRmeV9LZVNnSXBsR0ZwUUYyaTA1VFJEU2JGQ0xvU3VpYy1nUG53enFzT3RGMG10a3hzRGwxLUZOQnRfbTY0Rjd5N2RhaWpYZHlqRWtwMzNBOEdzaE9jenNYeWx4YW5jOFAtcEdMNUZDLVdNZk05Qm9kX3BRRzF4WnptQUlCUFV1THFLN19fb29EMnA0bmFSWVBUSGFqSnVtd2pYNVdGVWFiYW9JeTJBWGFkZFRMX2lPTGl5ckJpQ3dFbkw3Nkl5TVA4ZG9MSkF5SHpFOVdHRXNFYmhpc0QxdUlWWFV1c0tHQUVLc0RtMENEa2hOYUR0ZVl4OFFuTE1IST0iLCJoZWFkZXIiOnsia2lkIjoiQnVUZkNCak51azZOZ3B4aEp3SGJ5OG1aaEhQZ0hEMnlZU3RKV2F1cWUxNGYifX1dfQ==",
  "iv": "gfZEneTtNtmUo-n1",
  "ciphertext": "ZALOvOzgWeLdBhU=",
  "tag": "nYNeC49m63DOR-eghuqIpA=="
}
```

The protected data base64URL decodes to this:
```json
{
  "enc": "xchacha20poly1305",
  "typ": "JWM/1.0",
  "alg": "Authcrypt",
  "recipients": [
    {
      "encrypted_key": "Ww3VE5xqb3l0K1acaM5mahDRY_JckDgwW_L362qQVyRQp9wcVBGbecQCbaTZSfCc5PLNEEf-awQML8rfxJDFj2Y9qYMfXnmQER5ZeeLgucNcdtgxH-3L--W3GxocbIHhlSNUMg9VJsvVECUX9je-cV-5RFDTzbuPaEvVsngUMcO2smA863RtD-b31xAAnWRwyfTxVRcqX6wR2w02nv2YbnHWfgBa7y_ZbkiiIiKLID6fOtOg6a90ly5oc2ek9_LmppQBBgXXry8aR7nTFlYBsoS2e9c=",
      "header": {
        "kid": "GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL"
      }
    },
    {
      "encrypted_key": "waHqbZ-anss67ZL4Gr2eX2GCrCJVBiR27L4fy_KeSgIplGFpQF2i05TRDSbFCLoSuic-gPnwzqsOtF0mtkxsDl1-FNBt_m64F7y7daijXdyjEkp33A8GshOczsXylxanc8P-pGL5FC-WMfM9Bod_pQG1xZzmAIBPUuLqK7__ooD2p4naRYPTHajJumwjX5WFUabaoIy2AXaddTL_iOLiyrBiCwEnL76IyMP8doLJAyHzE9WGEsEbhisD1uIVXUusKGAEKsDm0CDkhNaDteYx8QnLMHI=",
      "header": {
        "kid": "BuTfCBjNuk6NgpxhJwHby8mZhHPgHD2yYStJWauqe14f"
      }
    }
  ]
}
```

#### Authcrypt pack algorithm

1. generate a content encryption key (symmetrical encryption key)
2. encrypt the message with the content encryption key and generated "iv"
    2a. returns "tag" to serialize data later
3. encrypt the CEK for each recipient's public key using Authcrypt (steps below)
    3a. perform libsodium.crypto_box(my_key, their_vk, message, nonce)
    3b. create tuple (base64(message), base58(sender_verkey), base64(nonce))
    3c. message_pack tuple
    3d. libsodium.crypto_box_seal(recipient_verkey, msg_pack_output) the message_pack
4. serialize the data into the structure listed above



#### pack format (Anoncrypted)
```
{
    "protected": "b64URLencoded({
        "enc": "xsalsa20poly1305",
        "typ": "JWM/1.0",
        "alg": "Anoncrypt",
        "recipients": [
            {
                "encrypted_key": <b64URLencode(anoncrypt(cek))>,
                "header": {
                    "kid": "base58encode(recipient_verkey)",
                }
            },
        ],
    })",
    "iv": <b64URLencode()>,
    "ciphertext": <b64URLencode(encrypt({'@type'...}, cek)>,
    "tag": <b64URLencode()>
}
```

##### pack example (Anoncrypt)
This is an example of an outputted message encrypting "Hello World" for two verkeys.

```json
{
  "protected": "eyJlbmMiOiJ4Y2hhY2hhMjBwb2x5MTMwNSIsInR5cCI6IkpXTS8xLjAiLCJhbGciOiJBbm9uY3J5cHQiLCJyZWNpcGllbnRzIjpbeyJlbmNyeXB0ZWRfa2V5IjoiVkVyT3E4a2Vldll6ZVRlZG93ckktQUlCc09sMlVFRGlaQ09qbGdUZWQySDFna2VFVkUtcjhteEZBTkpOaDBybGhPbWZ6QzgyN1kyOHFLODZUYVhHbkFYblZQclBYQ2hEdTNOT2p5YnRMd1U9IiwiaGVhZGVyIjp7ImtpZCI6IkdKMVN6b1d6YXZRWWZOTDlYa2FKZHJRZWpmenRONFhxZHNpVjRjdDNMWEtMIn19LHsiZW5jcnlwdGVkX2tleSI6IlppN0pSd1FDZVAyRmVINHVxUjR5djRFYm4xZU1PRDgwc3UzREdld0RPRjRJbldIM0k3dkFwcDVKMU9iOGJSMWhteXhIRXE2azgzNE5CaGVDbWJCUVZKNF8wRGY1RUhXMWZZbnRSUVM2RFdBPSIsImhlYWRlciI6eyJraWQiOiI0UVhQUVh6M2J3WnR5Z2VzRFV1UnNNTTgzcWNEVjJrRlpFandtb3ZkTm1rdiJ9fV19",
  "iv": "IIpOwYWxq3BrmLl7",
  "ciphertext": "J-I3w_OQcv_2Uzg=",
  "tag": "7LUptF-arfqs6Oxu-ZOKcg=="
}
```

The protected data decodes to this:

```json
{
  "enc": "xchacha20poly1305",
  "typ": "JWM/1.0",
  "alg": "Anoncrypt",
  "recipients": [
    {
      "encrypted_key": "VErOq8keevYzeTedowrI-AIBsOl2UEDiZCOjlgTed2H1gkeEVE-r8mxFANJNh0rlhOmfzC827Y28qK86TaXGnAXnVPrPXChDu3NOjybtLwU=",
      "header": {
        "kid": "GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL"
      }
    },
    {
      "encrypted_key": "Zi7JRwQCeP2FeH4uqR4yv4Ebn1eMOD80su3DGewDOF4InWH3I7vApp5J1Ob8bR1hmyxHEq6k834NBheCmbBQVJ4_0Df5EHW1fYntRQS6DWA=",
      "header": {
        "kid": "4QXPQXz3bwZtygesDUuRsMM83qcDV2kFZEjwmovdNmkv"
      }
    }
  ]
}
```

#### Authcrypt pack algorithm

1. generate a content encryption key (symmetrical encryption key)
2. encrypt the message with the content encryption key and generated "iv"
    2a. returns "tag" to serialize data later
3. encrypt the CEK for each recipient's public key using Anoncrypt (steps below)
    3a. libsodium.crypto_box_seal(recipient_verkey, msg_pack_output)
4. serialize the data into the structure listed above

## Schema
This spec is according [JSON Schema v0.7](https://json-schema.org/specification.html)
```json
{
    "id": "https://github.com/hyperledger/indy-agent/wiremessage.json",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Json Web Message format",
    "type": "object",
    "required": ["ciphertext", "iv", "protected", "tag"],
    "optional": ["aad"],
    "properties": {
        "protected": {
            "type": "object",
            "description": "Additional authenticated message data",
            "required": ["enc", "typ", "alg", "recipients"],
            "properties": {
                "enc": {
                    "type": "string",
                    "enum": ["xchacha20poly1305"],
                    "description": "The authenticated encryption algorithm used to encrypt the ciphertext"
                },
                "typ": { 
                    "type": "string",
                    "description": "The message type. Ex: JWM/1.0"
                },
                "alg": {
                    "type": "string",
                    "enum": [ "authcrypt", "anoncrypt"]
                },
                "recipients": {
                    "type": "array",
                    "description": "A list of the recipients who the message is encrypted for",
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
                                "optional": ["sender"],
                                "description": "The recipient to whom this message will be sent",
                                "properties": {
                                    "sender": {
                                        "type": "string",
                                        "description": "The anoncrypted DID key reference, or key of sender."
                                    },
                                    "kid": {
                                        "type": "string",
                                        "description": "The DID key reference, or key of the recipient."
                                    }
                                }
                            }
                        }
                    }
                 },     
            },
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
        },
        "aad": {
            "type": "string",
            "description": "The hash of the recipients block base64 URL encoded value"
        },
    }
}
```

# Future Changes
[future]: #future-changes

Currently only keys are used for this implementation.  This is due to lack of capability in libindy. As soon as libindy does allow for DID resolution we will transition to supporting DIDs with Key references in the kid and sender fields.

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
