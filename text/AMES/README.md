- Name: AMES
- Author: Kyle Den Hartog, Stephen Curran (swcurran@gmail.com), Sam Curren (Sam@sovrin.org), Mike Lodder (Mike@sovrin.org)
- Start Date: 2018-07-10 (approximate, backdated)
- Feature Branch: https://github.com/kdenhartog/indy-sdk/tree/multiplex-poc
- JIRA ticket: IS-1073
- HIPE PR: (leave this empty)
# AMES
[summary]: #summary

There are two layers of messages that combine to enable **interoperable** self-sovereign identity Agent-to-Agent communication. At the highest level are Agent Messages - messages sent between Identities to accomplish some shared goal. For example, establishing a connection between identities, issuing a Verifiable Credential from an Issuer to a Holder or even the simple delivery of a text Instant Message from one person to another. Agent Messages are delivered via the second, lower layer of messaging - Wire. A Wire Message is a wrapper (envelope) around an Agent Message to permit sending the message from one Agent directly to another Agent. An Agent Message going from its Sender to its Receiver may be passed through a number of Agents, and a Wire Message is used for each hop of the journey.

Agent Message Encryption Serialization (AMES) are intended to be a standardized format built on the JWE spec that allows for all necessary information to encrypt, decrypt, and perform routing can be found in the message while remaining asynchronous. In this HIPE we'll describe the API of the Pack and Unpack functions. This HIPE does not currently go into detail about how to use the API to prevent data exposure, but should be updated to detail this before being accepted.
# Motivation
[motivation]: #motivation

The purpose of this HIPE is to define how an Agent that needs to transport an arbitrary Agent Message delivers it to another Agent through a direct (point-to-point) communication channel. A message created by a Sender Agent and intended for a Receiver Agent will usually be sent multiple times between Agents via Wire Messages in order to reach its ultimate destination.

Many aspects of this hipe have been derived from [JSON Web Encryption - RFC 7516](https://tools.ietf.org/html/rfc7516). We're actively working with the JWE spec writer (Mike Jones at Microsoft) to find alignment between our needs and the JWE Spec. AMES are intended to provide the following properties:

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

## Wire Messages

A Wire Message is used to transport any Agent Message from one Agent directly to another. In our example message flow above, there are five Wire Messages sent, one for each hop in the flow. The process to send a Wire Message consists of the following steps:

- Call one of the standard functions "auth_pack() or anon_pack()" (implemented in the Indy-SDK) to prepare the Agent Message
- Send the Wire Message using the transport protocol defined by the receiving endpoint
- Receive the Wire Message
- Call the standard function "unpack()" to retrieve the Agent Message from the Wire Message and potentially provenance of the message

An Agent sending a Wire Message must know information about the Agent to which it is sending.  That is, it must know its physical address (including the transport protocol to be used - https, zmq, etc.) and if the message is to be encrypted, the public key the receiving agent is expecting will be used for the message.

## The pack()/unpack() Functions

The pack() functions are implemented in the Indy-SDK and will evolve over time. The initial instance of pack() includes two variations, only the first two of which are used for Wire Messages. The details of the APIs and the structure is outlined below. 

### Formats


### Schema
This spec is according [JSON Schema v0.7](https://json-schema.org/specification.html)
```json
{
    "id": "https://github.com/hyperledger/indy-agent/wiremessage.json",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Json Web Message format",
    "type": "object",
    "required": ["aad", "ciphertext", "protected", "recipients"],
    "properties": {
        "aad": {
            "type": "string",
            "description": "The hash of the recipients block base64 URL encoded value"
        },
        "ciphertext": {
            "type": "string",
            "description": "base64 URL encoded authenticated encrypted message"
        },
        "protected": {
            "type": "object",
            "description": "Additional authenticated message data",
            "required": ["enc", "typ", "aad_hash_alg"],
            "properties": {
                "enc": {
                    "type": "string",
                    "enum": ["xsalsa20poly1305", "aes256gcm"],
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
                    "enum": ["xsalsa20poly1305", "aes256gcm", "authcrypt", "anoncrypt"]
                }
            },
            "recipients": {
                "type": "array",
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
                            "oneOf": [
                                {
                                    "required": ["did"],
                                    "not": { "required": ["key"] }
                                },
                                {
                                    "required": ["key"],
                                    "not": { "required": ["did"] }
                                }
                            ],
                            "description": "The recipient to whom this message will be sent",
                            "properties": {
                                "sender": {
                                    "type": "string",
                                    "description": "The anoncrypted verification key of the sender"
                                },
                                "kid": {
                                    "type": "string",
                                    "description": "The DID and key reference of the recipient. If this field is specified, key MUST be absent"
                                },
                                "key": {
                                    "type": "string",
                                    "description": "The VerKey of the recipient. If this field is specified, did MUST be absent"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

## IndySDK API Additions

### AuthPack

#### indy_auth_pack_message(command_handle, wallet_handle, message, recv_keys, my_vk) -> JSON String:
The purpose of this function is to take in a message, encrypt the message with authcrypt for the keys specified and output a JSON string using the JSON serialization format.

The parameters should be used in this way:
    
    command_handle: This command handle is used to track callbacks for the calls of this API.

    wallet_handle: this is the wallet_handle that contains the related data such as keys to be able to complete the function.

    message: This should be the message that is intended to be encrypted. It's required and should be of type String. The most common forms of messages that will be passed in here are json strings that follow the format of a particular message family.
    
    recv_keys: This is a list of verkeys passed as a string. If only 1 key is passed in, then a Compact serialization will be outputed. If > 1 keys are passed in then JSON serialization will be outputted from this function.

    my_vk: This is an optional parameter that must include a verkey as a string if auth is set to true (authcrypting). Otherwise, this must be set to none if anoncrypt is being used.  

#### auth_pack_message API and output format

```
indy_auth_pack_message(command_handle: i32, wallet_handle: i32, message: String, recv_keys: JSON array as String, my_vk: String) ⇒ 

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
                "sender": <b64URLencode(anoncrypt(r_key))>,
                "kid": "did:sov:1234512345#key-id",
                "key": "b64URLencode(ver_key)"
            }
        },
    ],
    "aad": <b64URLencode(aad_hash_alg(b64URLencode(recipients)))>,
    "iv": <b64URLencode()>,
    "ciphertext": <b64URLencode(encrypt({'@type'...}, cek)>,
    "tag": <b64URLencode()>
}
```

### auth_pack_message algorithm details

Authcrypting works by using two keys, one from the sender's DID Doc and one from the receiver's DID Document, to generate a symmetrical key specific to the two agents involved in the encryption process. The sender's key is explicitly listed ("from") and then encrypted in the "enc_header" object to prevent correlating the two keys ("to" and "from") which are communicating. These two keys are used to encrypt the cek.

The algorithm to encrypt a message with authenticated encryption (provides authentication) using this structure:

1. generate a random nonce ("iv")
2. generate a random ephemeral symmetrical key (plaintext of cek)
3. secretbox_detached (src/utils/crypto/xsalsa20/sodium.rs currently) encrypt the message (plaintext of ciphertext)
4. create an array of recipient keys (one "to" for each recipient key)
5. encrypt (uses crypto_box_easy from libsodium) the ephemeral symmetrical key with one "to" and sender's verkey keys and one "cek_nonce" for each recipient to produce one "cek" for each recipient key
6. encrypt the sender's verkey using sealed_encrypt (uses sealed_box from libsodium)
7. serialize the data into the Authcrypt json structure listed above

### AnonPack

#### indy_anon_pack_message(command_handle, wallet_handle, message, recv_keys) -> JSON String:
The purpose of this function is to take in a message, encrypt the message with anoncrypt for the keys specified and output a JSON string using the JSON serialization format.

The parameters should be used in this way:
    
    command_handle: This command handle is used to track callbacks for the calls of this API.
    
    message: This should be the message that is intended to be encrypted. It's required and should be of type String. The most common forms of messages that will be passed in here are json strings that follow the format of a particular message family.
    
    recv_keys: This is a list of verkeys passed as a string. If > 1 keys are passed in then JSON serialization will be outputted from this function. an example of what would be passed is "[]"

#### indy_anon_pack_message output format
```
indy_anon_pack_message(command_handle: i32, message: String, recv_keys: JSON array as String) ⇒ 

{
    "protected": "b64URLencoded({
        "enc": "xsalsa20poly1305",
        "typ": "JWM/1.0",
        "aad_hash_alg": "BLAKE2b",
        "cek_enc": "anoncrypt"
        "recipients": [
        {
            "encrypted_key": <b64URLencode(encrypt(cek))>,
            "header": {
                "kid": "did:sov:1234512345#key-id",
                "key": "b64URLencode(ver_key)"
            }
        },
    ],
    })"
    "aad": <b64URLencode(aad_hash_alg(b64URLencode(recipients)))>,
    "iv": <b64URLencode()>,
    "ciphertext": <b64URLencode(encrypt({'@type'...}, cek)>,
    "tag": <b64URLencode()>
}
```

#### anon_pack_message algorithm details

The algorithm to encrypt a message with anonymous encryption using this structure:

1. generate a random nonce ("iv")
2. generate a random ephemeral symmetrical key (plaintext of cek)
3. encrypt (src/utils/crypto/xsalsa20/sodium.rs currently which uses secretbox::seal from libsodium) encrypt the message (plaintext of ciphertext)
4. create an array of recipient keys (one "to" for each recipient key)
5. encrypt_sealed the "cek" using the "to" key. (The ephemeral sender's verkey and nonce is generated by the function and appended to the ciphertext)
6. serialize the data into the Anoncrypt json structure listed above

#### unpack_message(AMES, my_vk) -> plaintext message:
The unpack function is used to decrypt a message on the receiver side. It will output the plaintext of the corresponding pack_message if the verkey provided is found within the header. This works for both compact serializations and for JSON serializations.

The parameters should be used in this way:

    command_handle: This command handle is used to track callbacks for the calls of this API.

    wallet_handle: this is the wallet_handle that contains the related data such as keys to be able to complete the function.

    ames_json: This should pass in a json string that follows the serialization format from above.

    my_vk: This should be the verkey that you wish to use to decrypt the message.

output: A decrypted message, if authcrypt was used. Will return a verkey. If Anoncrypted will return empty string.

#### unpack_message algorithm details

The algorithm to decrypt the message with the structure from auth_pack_message is as follows:

1. identify the recipient verkey used to decrypt (e.g. my phone's key)
2. loop through the recipients list to identify the recipient object relevant to the agent performing the algorithm
3. decrypt the "enc_from" from the recipient object found in step 2 using the decrypt_sealed function and the key from step 1. This produces the sender's verkey
4. decrypt the "cek" using the recipient privkey and the decrypted "enc_from" and the cek_nonce with the decrypt function. This produces the ephemeral symmetrical key
5. decrypt the ciphertext with the ephemeral symmetrical key and the iv using decrypt_detached (src/utils/crypto/xsalsa20/sodium.rs currently). This will give you the decrypted message

The algorithm to decrypt a message with the structure from anon_pack_message is as follows:

1. identify the recipient verkey used to decrypt (e.g. my phone's key)
2. loop through the recipients list to identify the recipient object relevant to the agent performing the algorithm
3. decrypt_sealed the "cek" using the corresponding private key from the recipient key used in step 1
5. decrypt the ciphertext with the ephemeral symmetrical key and the iv using decrypt_detached (src/utils/crypto/xsalsa20/sodium.rs currently). This will give you the decrypted message

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
- How will the wire messages work with routing tables to pass a message through a domain, potentially over various transport protocols?
- If the wire protocol fails, how is that failure passed back to those involved in the transmission?
- A reason for using a synchronous response to at least checking the ability to decrypt the message is cache handling. Agents might cache public key information for performance reasons (fewer DID resolutions) and so messages might be invalid due to undetected key rotations. If the "Invalid Message" response was synchronously returned to the Sender, the Sender could resolve the DID it was using and retry without breaking the higher level protocol.
