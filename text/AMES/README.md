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

### Pack Message

#### pack_message() interface

packed_message = pack_message(wallet_handle, message, receiver_verkeys, sender_verkey)

#### pack_message() Params: 
- wallet_handle (i32): wallet handle that contains the sender_verkey.
- message (String): the message being sent as a string. If it's JSON object it should be in string format first
- receiver_verkeys (String): a list of recipient verkey's as string formatted as a JSON Array
- sender_verkey (String): the sender's verkey as a string. When an empty string ("") is passed in this parameter, anoncrypt mode is used

#### pack_message() return value (Authcrypt mode)
This is an example of an outputted message encrypting "Hello World" for two verkeys.

```json
{
  "protected": "eyJlbmMiOiJ4Y2hhY2hhMjBwb2x5MTMwNSIsInR5cCI6IkpXTS8xLjAiLCJhbGciOiJBdXRoY3J5cHQiLCJyZWNpcGllbnRzIjpbeyJlbmNyeXB0ZWRfa2V5IjoiR2djbWdrMjhpN0VIajBWTlM5elh5WHp3MnE5bWNxN0R3RV9SSldsbjJuYk93Y2R5eXJGX0JiNnNPX0poYXJ3TEFaejJIb0c3SWp6dWN3ekZGMUNIN1N5N25KWW5BU0UxY1NRWDBkYWVZd05TTURGcmNnY1pIRXM2MlJBUnVnVWYwOEszQ0pXYUVfR3U5bmFDeHRHTmFyOUtIRFJ6UmVYQVQ1aFJRQWNuOURPZHp3djRWNmNUR3BZbGY0d01sWVZ2UTdEVGJiTERRRFJDUW5KNlk3bXlMc1pNdUIzNmVYTk5vWEFEVzBRSzZMUy1BTG5MbGotd3NZOHRZTU9pN2FhX1l5U0d2aUw0RE81SS1JTHhlZUZTSGF4MGJOaz0iLCJoZWFkZXIiOnsia2lkIjoiR0oxU3pvV3phdlFZZk5MOVhrYUpkclFlamZ6dE40WHFkc2lWNGN0M0xYS0wifX0seyJlbmNyeXB0ZWRfa2V5Ijoid0gteW1ObGVyd1piZFVXaExzRkU2WlhhR2dGQWd4bUVSRnJORUlZZ0QxMlBXY3Y1eFZUZm1pbE9MLVpYT2JmSTg5am1WbmJVQ3VKNnowLXJNUy1ad01SQmdnbC1QYzZWWXBrdW5Ea1pIMVY1Nnh1TGMxQzB2MmxHQkFCTFVZNUhuY1EwZXgtQi15VGdIbkw0VmpBS1Y3VXI3X01yNEYzUlIxazN4X2F1VzU0M09CVTZCZHkzSWNNRkFFWUp5VEpsVU5Ed2VmWkt2dkk1T0FON0VoZTVmbG02RllJempaYjRuV2pnVUJWSnhqSTc0VVMwTmh1aWxlMjhtbGQ0NlJnMjYybm1vRlFROWM0X0d4bmh0N2hMTThCdVpBdz0iLCJoZWFkZXIiOnsia2lkIjoiaWJzMUZlVnZpTXBKYWVqOWI0TW5qdTJXRXl3dXRDRVpxTHJvenBKV3ZMdyJ9fV19",
  "iv": "Xk9VOdDdmWn-_WsC",
  "ciphertext": "s-M2cVcUaaC_0GE=",
  "tag": "HDJYCAG7cEtHiU0tx67FHQ=="
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
      "encrypted_key": "Ggcmgk28i7EHj0VNS9zXyXzw2q9mcq7DwE_RJWln2nbOwcdyyrF_Bb6sO_JharwLAZz2HoG7IjzucwzFF1CH7Sy7nJYnASE1cSQX0daeYwNSMDFrcgcZHEs62RARugUf08K3CJWaE_Gu9naCxtGNar9KHDRzReXAT5hRQAcn9DOdzwv4V6cTGpYlf4wMlYVvQ7DTbbLDQDRCQnJ6Y7myLsZMuB36eXNNoXADW0QK6LS-ALnLlj-wsY8tYMOi7aa_YySGviL4DO5I-ILxeeFSHax0bNk=",
      "header": {
        "kid": "GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL"
      }
    },
    {
      "encrypted_key": "wH-ymNlerwZbdUWhLsFE6ZXaGgFAgxmERFrNEIYgD12PWcv5xVTfmilOL-ZXObfI89jmVnbUCuJ6z0-rMS-ZwMRBggl-Pc6VYpkunDkZH1V56xuLc1C0v2lGBABLUY5HncQ0ex-B-yTgHnL4VjAKV7Ur7_Mr4F3RR1k3x_auW543OBU6Bdy3IcMFAEYJyTJlUNDwefZKvvI5OAN7Ehe5flm6FYIzjZb4nWjgUBVJxjI74US0Nhuile28mld46Rg262nmoFQQ9c4_Gxnht7hLM8BuZAw=",
      "header": {
        "kid": "ibs1FeVviMpJaej9b4Mnju2WEywutCEZqLrozpJWvLw"
      }
    }
  ]
}
```

#### pack output format (Authcrypt mode)

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

#### pack_message() return value (Anoncrypt mode)
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

#### pack output format (Anoncrypt mode)
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

#### Anoncrypt pack algorithm

1. generate a content encryption key (symmetrical encryption key)
2. encrypt the message with the content encryption key and generated "iv"
    2a. returns "tag" to serialize data later
3. encrypt the CEK for each recipient's public key using Anoncrypt (steps below)
    3a. libsodium.crypto_box_seal(recipient_verkey, msg_pack_output)
4. serialize the data into the structure listed above

### Unpack Message

#### unpack_message() inteface

unpacked_message = unpack_message(wallet_handle, jwe)

#### unpack_message() Params

- wallet_handle (i32): wallet handle that contains the sender_verkey
- jwe (String): a message which was returned from a pack_message() and follows the scheme format described below

#### unpack_message() return values (authcrypt mode)

```json
{
    "message":"Hello World",
    "sender_verkey":"HyFrZnjtkqQp1sxQVXvKhubFFhV1r7AbryEH7T4S4wq4"
}

```

#### unpack_message() return values (anoncrypt mode)
```json
{
    "message": "Hello World"
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
    "required": ["ciphertext", "iv", "protected", "tag"],
    "properties": {
        "protected": {
            "type": "object",
            "description": "Additional authenticated message data base64URL encoded",
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
                                "description": "The key used for encrypting the ciphertext. If authcrypt mode is used this field
                                contains the authcrypted cek concatenated with the sender_verkey and the nonce (authcrypt_cek|sender_verkey|nonce) which is then anoncrypted and base64url encoded. If anoncrypt mode is used 
                                this field contains the cek anoncrypted and then base64URL encoded"
                            },
                            "header": {
                                "type": "object",
                                "required": ["kid"],
                                "description": "The recipient to whom this message will be sent",
                                "properties": {
                                    "kid": {
                                        "type": "string",
                                        "description": "The DID key reference, or a base58 encoded verkey of the recipient."
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
            "description": "Integrity checksum/tag base64URL encoded to check ciphertext, protected, and iv"
        }
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
