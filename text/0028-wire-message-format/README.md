- Name: Wire Level Messages (JWM/JWEs)
- Author: Kyle Den Hartog(kyle.denhartog@evernym.com), Stephen Curran (swcurran@gmail.com), Sam Curren (Sam@sovrin.org), Mike Lodder (Mike@sovrin.org)
- Start Date: 2018-07-10 (approximate, backdated)
- Feature Branch: https://github.com/kdenhartog/indy-sdk/tree/multiplex-rebase
- JIRA ticket: IS-1073
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

- Call the standard function `pack()` (implemented in the Indy-SDK) to prepare the Agent Message
- Send the Wire Message using the transport protocol defined by the receiving endpoint
- Receive the Wire Message
- Call the standard function `unpack()` to retrieve the Agent Message from the Wire Message and potentially provenance of the message

An Agent sending a Wire Message must know information about the Agent to which it is sending.  That is, it must know its physical address (including the transport protocol to be used - https, zmq, etc.) and if the message is to be encrypted, the public key the receiving agent is expecting will be used for the message.

## The pack()/unpack() Functions

The pack() functions are implemented in the Indy-SDK and will evolve over time. The initial instance of pack() will have APIs built in that allow for a consumer of the APIs to be able The details of the outputs of packed messages are defined below. Additionally, there's a schema describing the intent of the key:value pairs below. 

### Pack Message

#### pack_message() interface

packed_message = pack_message(wallet_handle, message, receiver_verkeys, sender_verkey)

#### pack_message() Params: 
- wallet_handle: wallet handle that contains the sender_verkey.
- message: the message being sent as a string. If it's JSON object it should be in string format first
- receiver_verkeys: a list of recipient verkey's as string formatted as a JSON Array
- sender_verkey: the sender's verkey as a string. When an empty string ("") is passed in this parameter, anoncrypt mode is used

#### pack_message() return value (Authcrypt mode)
This is an example of an outputted message encrypting "Hello World" for two verkeys.

```json
{
  "protected":"eyJlbmMiOiJ4Y2hhY2hhMjBwb2x5MTMwNV9pZXRmIiwidHlwIjoiSldNLzEuMCIsImFsZyI6IkF1dGhjcnlwdCIsInJlY2lwaWVudHMiOlt7ImVuY3J5cHRlZF9rZXkiOiI5enBKd1lwZWZNTmFUQklrOVNlM2JuSERVTHNScTJkcHBFN0xCbElyTlEzOXlIRVVOSEVQV0c2UUxJR3pfMW1RIiwiaGVhZGVyIjp7ImtpZCI6IkdKMVN6b1d6YXZRWWZOTDlYa2FKZHJRZWpmenRONFhxZHNpVjRjdDNMWEtMIiwiaXYiOiJ3YjlmS3dsRGNic3RSZ2NjMVN3QWRvbVpMaW56Yjc0QiIsInNlbmRlciI6Ik1DaFFBZTdkNjhEN0RWU3pOX2FIb1RfWFVnMi1ZQ05fRVo5d1hEcjhRa21fU19zY2Z2bjNfemF6ZEg5SkxkbmVwQXlucENiNXVFYVRCTmk1bXZGZE1vYzVWQllKdGJwV0wwUEFYSFFEMzgwVXQtalRnYUhUR2M5U2Ribz0ifX0seyJlbmNyeXB0ZWRfa2V5IjoibFpXLUo0N3VLNkszRnQ1VVpnWDFwT294Qm9TamVzYVBzR3Nva2pTajB2ZjRwYzE0c2FtbGRrUTZPTW1kczNzMyIsImhlYWRlciI6eyJraWQiOiJFYlJSNDJnZHlaRW5vZktESzhjck1FN05QVTNGSHNrRUdzcDZDQVJYZzZTYiIsIml2IjoiY0hsSTJmQzgtbDdYSkdpS2cwcVdfRy1STUxfM3RGMlAiLCJzZW5kZXIiOiJ2OUNNN2t6U3lUV0YwR3JqcGVRbnpIMTJ1cV9pTUVjc2pPS0gyUDJlY3pfR3FlQnZWR3doeHYtR0U4NmR4NTNrZFMxVi1oWHBTanBuRFlvTVk3MjZHdXhMLWl4b0tDZ2ZHcElfb2owYjg2NDdPSnM1SHdyQXk5NnVHUlE9In19XX0=",
  "iv":"hZFhKEdb0pSLqAQ0",
  "ciphertext":"c4WYswQW7LHncecV6NhUIGV_-t4ynxkHxDifwi6xpmpLys-nima2VIFXUatl2LTqy0RF3zT844McjdwLqhjmWg2nyi2RXuNRtPEQfbnDOzIDNWbmH_Mi3yMJwsRZqbhx-6UWIEJrcpoNwtmbDeeBgzEuqk_uwWoiz4RX3FpQPQg4uJ7R_kAq3bZJvQHH2Lef69OFsf_LcgVm7z1UUkf4cizK-g4WG0nBFofZn623",
  "tag":"ooNMN8Q2cfjhX2lWJpXs4Q=="
}
```

The protected data base64URL decodes to this:
```json
{
  "enc":"xchacha20poly1305_ietf",
  "typ":"JWM/1.0",
  "alg":"Authcrypt",
  "recipients":[
    {
      "encrypted_key":"9zpJwYpefMNaTBIk9Se3bnHDULsRq2dppE7LBlIrNQ39yHEUNHEPWG6QLIGz_1mQ",
      "header":{
        "kid":"GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL",
        "iv":"wb9fKwlDcbstRgcc1SwAdomZLinzb74B",
        "sender":"MChQAe7d68D7DVSzN_aHoT_XUg2-YCN_EZ9wXDr8Qkm_S_scfvn3_zazdH9JLdnepAynpCb5uEaTBNi5mvFdMoc5VBYJtbpWL0PAXHQD380Ut-jTgaHTGc9Sdbo="
      }
    },
    {
      "encrypted_key":"lZW-J47uK6K3Ft5UZgX1pOoxBoSjesaPsGsokjSj0vf4pc14samldkQ6OMmds3s3",
      "header":{
        "kid":"EbRR42gdyZEnofKDK8crME7NPU3FHskEGsp6CARXg6Sb",
        "iv":"cHlI2fC8-l7XJGiKg0qW_G-RML_3tF2P",
        "sender":"v9CM7kzSyTWF0GrjpeQnzH12uq_iMEcsjOKH2P2ecz_GqeBvVGwhxv-GE86dx53kdS1V-hXpSjpnDYoMY726GuxL-ixoKCgfGpI_oj0b8647OJs5HwrAy96uGRQ="
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
                "encrypted_key": base64URLencode(libsodium.crypto_box(my_key, their_vk, cek, cek_iv))
                "header": {
                    "kid" : base58encode(recipient_verkey),
                    "sender" : base64URLencode(libsodium.crypto_box_seal(their_vk, sender_vk_string)),
                    "iv" : base64URLencode(iv) 
                }
            },
        ],
    })"
    "iv": b64URLencode(iv),
    "ciphertext": b64URLencode(encrypt_detached({'@type'...}, protected_value_encoded, iv, cek),
    "tag": b64URLencode(tag)
}
```

#### Authcrypt pack algorithm

1. generate a content encryption key (symmetrical encryption key)
2. encrypt the CEK for each recipient's public key using Authcrypt (steps below)
    1. set `encrypted_key` value to base64URLencode(libsodium.crypto_box(my_key, their_vk, cek, cek_iv))
        * Note it this step we're encrypting the cek, so it can be decrypted by the recipient
    2. set `sender` value to base64URLencode(libsodium.crypto_box_seal(their_vk, sender_vk_string))
        * Note in this step we're encrypting the sender_verkey to protect sender anonymity
    3. base64URLencode(cek_iv) and set to `iv` value in the header 
        * Note the cek_iv in the header is used for the `encrypted_key` where as `iv` is for ciphertext
3. base64URLencode the `protected` value
4. encrypt the message using libsodium.crypto_aead_chacha20poly1305_ietf_encrypt_detached(message, protected_value_encoded, iv, cek) this is the ciphertext.
5. base64URLencode the iv, ciphertext, and tag then serialize the format into the output format listed above.

For a reference implementation, see https://github.com/hyperledger/indy-sdk/libindy/src/commands/crypto.rs

#### pack_message() return value (Anoncrypt mode)
This is an example of an outputted message encrypting "Hello World" for two verkeys.

```json
{
  "protected":"eyJlbmMiOiJ4Y2hhY2hhMjBwb2x5MTMwNV9pZXRmIiwidHlwIjoiSldNLzEuMCIsImFsZyI6IkFub25jcnlwdCIsInJlY2lwaWVudHMiOlt7ImVuY3J5cHRlZF9rZXkiOiJtVXRTaTdpR25KcEVRU1llWWh0eGt3N3YtUVAycVI0ZEVSMGh5MGlCWlV6Z0tDQkVlMWJEb3AyNVN5clREWVpEWEl6MEFyNUFqWXBaakVaSURCTjRuRXAwMnB5Ti1sa2l5b2h6WmNjUEFSTT0iLCJoZWFkZXIiOnsia2lkIjoiR0oxU3pvV3phdlFZZk5MOVhrYUpkclFlamZ6dE40WHFkc2lWNGN0M0xYS0wifX0seyJlbmNyeXB0ZWRfa2V5IjoiWnBDeWl5NGdJZ0NiYTk5am9BSzd1NXBzRzhnQWQ0QTI4eVN6ZkRRaEtXV2lhS21ST0Q0QnV1UDhoTVNJWFh4d3o2T2dzVkJUWXF4eWlUZll1UGQ1SW11WlZsV1pjRGxTR2xoVlo4OXVkTUk9IiwiaGVhZGVyIjp7ImtpZCI6IkNRTmpjZmJCZTV2ZjdMNWY4OFJORFpZdUVGcHExNjU5MnpWWWZZQVZwRjQ3In19XX0=",
  "iv":"Ql4aE60uzYlxuFMB",
  "ciphertext":"gih4k0Pmj8aj03oXH65O3llM_q_pZIDkZKoX_dFTbc09DJt7FUnwpA9kxFt6Q3sKjrzmRsynj8jbdEDTSfzHxVQKPyYYVeqcDyztPGZ2AykEQN5nZAnDkBGDntdiBMwx0zahm-dyUznKwyJJhCBZHNBaJJCbwNXvvXEk8zG-QYy-8onOqUMKCYdjqcmfH9DmQrLZmoyR8447y8BleI__VUNh7rEOw89lcOrab1U=",
  "tag":"gAEu20TX-7L5zz6y4AYyLA=="
}
```

The protected data decodes to this:

```json
{
  "enc":"xchacha20poly1305_ietf",
  "typ":"JWM/1.0",
  "alg":"Anoncrypt",
  "recipients":[
    {
      "encrypted_key":"mUtSi7iGnJpEQSYeYhtxkw7v-QP2qR4dER0hy0iBZUzgKCBEe1bDop25SyrTDYZDXIz0Ar5AjYpZjEZIDBN4nEp02pyN-lkiyohzZccPARM=",
      "header":{
        "kid":"GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL"
      }
    },
    {
      "encrypted_key":"ZpCyiy4gIgCba99joAK7u5psG8gAd4A28ySzfDQhKWWiaKmROD4BuuP8hMSIXXxwz6OgsVBTYqxyiTfYuPd5ImuZVlWZcDlSGlhVZ89udMI=",
      "header":{
        "kid":"CQNjcfbBe5vf7L5f88RNDZYuEFpq16592zVYfYAVpF47"
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
                "encrypted_key": base64URLencode(libsodium.crypto_box_seal(their_vk, cek)),
                "header": {
                    "kid": base58encode(recipient_verkey),
                }
            },
        ],
    })",
    "iv": b64URLencode(iv),
    "ciphertext": b64URLencode(encrypt_detached({'@type'...}, protected_value_encoded, iv, cek),
    "tag": b64URLencode(tag)
}
```

#### Anoncrypt pack algorithm

1. generate a content encryption key (symmetrical encryption key)
2. encrypt the CEK for each recipient's public key using Authcrypt (steps below)
    1. set `encrypted_key` value to base64URLencode(libsodium.crypto_box_seal(their_vk, cek))
        * Note it this step we're encrypting the cek, so it can be decrypted by the recipient
3. base64URLencode the `protected` value
4. encrypt the message using libsodium.crypto_aead_chacha20poly1305_ietf_encrypt_detached(message, protected_value_encoded, iv, cek) this is the ciphertext.
5. base64URLencode the iv, ciphertext, and tag then serialize the format into the output format listed above.

For a reference implementation, see https://github.com/hyperledger/indy-sdk/libindy/src/commands/crypto.rs

### Unpack Message

#### unpack_message() inteface

unpacked_message = unpack_message(wallet_handle, jwe)

#### unpack_message() Params

- wallet_handle: wallet handle that contains the sender_verkey
- jwe: a message which was returned from a pack_message() and follows the scheme format described below


#### Unpack Algorithm

1. seralize data, so it can be used
    * For example, in rust-lang this has to be seralized as a struct.
2. Lookup the `kid` for each recipient in the wallet to see if the wallet possesses a private key associated with the public key listed
3. Check if a `sender` field is used.
    * If a sender is included use auth_decrypt to decrypto the `encrypted_key` by doing the following:
        1. decrypt sender verkey using libsodium.crypto_box_seal_open(my_private_key, base64URLdecode(sender))
        2. decrypt cek using libsodium.crypto_box_open(my_private_key, senderk_verkey, encrypted_key, cek_iv)
        3. decrypt ciphertext using libsodium.crypto_aead_chacha20poly1305_ietf_open_detached(base64URLdecode(ciphertext_bytes), base64URLdecode(protected_data_as_bytes), base64URLdecode(nonce), cek)
        4. return message and sender_verkey following the format listed below
    * If a sender is NOT included use a anon_decrypt to decrypt the `encrypted_key` by doing the following:
        1. decrypt `encrypted_key` using libsodium.crypto_box_seal_open(my_private_key, encrypted_key)
        2. decrypt ciphertext using libsodium.crypto_aead_chacha20poly1305_ietf_open_detached(base64URLdecode(ciphertext_bytes), base64URLdecode(protected_data_as_bytes), base64URLdecode(nonce), cek)
        3. 4. return message ONLY following the format listed below



For a reference implementation, see https://github.com/hyperledger/indy-sdk/libindy/src/commands/crypto.rs

#### unpack_message() return values (authcrypt mode)

```json
{
  "message":"{ \"@id\": \"123456780\",\"@type\":\"did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/basicmessage/1.0/message\",\"sent_time\": \"2019-01-15 18:42:01Z\",\"content\": \"Your hovercraft is full of eels.\"}",
  "sender_verkey":"4Wkv598mDVsEdHTpjEe2Bk1aB3PxNsKjg9t6k65SFQNX"
}

```

#### unpack_message() return values (anoncrypt mode)
```json
{
    "message":"{\"@id\": \"123456780\",\"@type\":\"did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/basicmessage/1.0/message\",\"sent_time\": \"2019-01-15 18:42:01Z\",\"content\": \"Your hovercraft is full of eels.\"}"
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
            "description": "Additional authenticated message data base64URL encoded, so it can be verified by the recipient using the tag",
            "required": ["enc", "typ", "alg", "recipients"],
            "properties": {
                "enc": {
                    "type": "string",
                    "enum": ["xchacha20poly1305_ietf"],
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
                                "description": "The key used for encrypting the ciphertext. This is also referred to as a cek"
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

# Additional Notes
[additional-notes]: #additional-notes

* All `kid` values used currently are base58 encoded ed25519 keys. If other keys types are used, say secp256k1, base58 encoding should also be used here for interoperability.

* All algorithm APIs which use libsodium are from [sodiumoxide](https://crates.io/crates/sodiumoxide) rust wrapping of the original C implementation.

# Future Changes
[future]: #future-changes

Currently only keys are used for this implementation.  This is due to lack of capability in libindy. As soon as libindy does allow for DID resolution we will transition to supporting DIDs with Key references in the kid and sender fields.

# Drawbacks
[drawbacks]: #drawbacks

The current implementation of the `pack()` message is currently Hyperledger Indy specific. It is based on common crypto libraries ([NaCl](https://nacl.cr.yp.to/)), but the wrappers are not commonly used outside of Indy. There's currently work being done to fine alignment on a cross-ecosystem interopable protocol, but this hasn't been achieved yet. This work will hopefully bridge this gap.



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
    - This should be handled using the error-reporting mechanism which is currently proposed HIPE #65 by Stephen Curran.
