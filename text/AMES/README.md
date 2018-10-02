- Name: AMES
- Author: Kyle Den Hartog
- Start Date: 2018-07-10 (approximate, backdated)
- HIPE PR: (leave this empty)
- Feature Branch: https://github.com/kdenhartog/indy-sdk/tree/multiplex-poc

# AMES
[summary]: #summary

Agent Message Encryption Serialization (AMES) are intended to be a standardized format that allows for all necessary information to encrypt, decrypt, and perform routing can be found in the message while remaining asynchronous. In this HIPE we'll describe the API of the Pack and Unpack functions. This HIPE does not currently go into detail about how to use the API to prevent data exposure, but should be updated to detail this before being accepted.

# Motivation
[motivation]: #motivation

Many aspects of this hipe have been derived from [JSON Web Encryption - RFC 7516](https://tools.ietf.org/html/rfc7516). It has diverged from this spec due to assumptions around TLS and encryption schemes, as well as to focus on the DIDs usecase. AMES are intended to provide the following properties:

* provide a standard serialization format
* Handles encrypting messages for 1 or many receivers
* Keeps messaging protocol asynchronous

# Technicals

## Serialization Examples

### JSON Serialization

```
{
    "recipients" : [
        {
            "header" : { 
                "typ" : "x-b64nacl"
                "alg" : "x-auth", 
                "to" : "<recipient_verkey>", 
                "from" : "<sender_verkey>",
            },
            "cek" : <encrypted symmetrical key to unlock ciphertext>
        },
        {    
            "header" : { 
                "typ" : "x-b64nacl",
                "alg" : "x-auth",
                "to" : "<recipient_verkey>",
                "from" : "<sender_verkey>"
            },
            "cek" : <encrypted symmetrical key to unlock ciphertext>
        }
    ],
    "enc" : "xsalsa20poly1305",
    "iv" : <Nonce>,
    "ciphertext" : <message ciphertext>,
    "tag" : <Authentication Tag from NaCl>
}
```

### Compact Serialization

Note: I have removed this serialization to consolidate to a single serialization format, however if there's a need it is possible to support compact serialization format similar to how JWEs do in the future. Right now it adds additional unnecessary complexity.


## Additional IndySDK APIs

### indy_auth_pack_message(command_handle, wallet_handle, message, recv_keys, my_vk) -> JSON String:
The purpose of this function is to take in a message, encrypt the message with authcrypt for the keys specified and output a JSON string using the JSON serialization format.

The parameters should be used in this way:
    
    command_handle: This command handle is used to track callbacks for the calls of this API.

    wallet_handle: this is the wallet_handle that contains the related data such as keys to be able to complete the function.

    message: This should be the message that is intended to be encrypted. It's required and should be of type String. The most common forms of messages that will be passed in here are json strings that follow the format of a particular message family.
    
    recv_keys: This is a list of verkeys passed as a string. If only 1 key is passed in, then a Compact serialization will be outputed. If > 1 keys are passed in then JSON serialization will be outputted from this function.

    my_vk: This is an optional parameter that must include a verkey as a string if auth is set to true (authcrypting). Otherwise, this must be set to none if anoncrypt is being used.  

    output: a string in the form of either JSON serialization or Compact serialization

### indy_anon_pack_message(command_handle, wallet_handle, message, recv_keys) -> JSON String:
The purpose of this function is to take in a message, encrypt the message with anoncrypt for the keys specified and output a JSON string using the JSON serialization format.

The parameters should be used in this way:
    
    command_handle: This command handle is used to track callbacks for the calls of this API.

    wallet_handle: this is the wallet_handle that contains the related data such as keys to be able to complete the function.
    
    message: This should be the message that is intended to be encrypted. It's required and should be of type String. The most common forms of messages that will be passed in here are json strings that follow the format of a particular message family.
    
    recv_keys: This is a list of verkeys passed as a string. If only 1 key is passed in, then a Compact serialization will be outputed. If > 1 keys are passed in then JSON serialization will be outputted from this function.

    output: a string in the form of either JSON serialization or Compact serialization

### unpack_message(AMES, my_vk) -> plaintext message:
The unpack function is used to decrypt a message on the receiver side. It will output the plaintext of the corresponding pack_message if the verkey provided is found within the header. This works for both compact serializations and for JSON serializations.

The parameters should be used in this way:

    command_handle: This command handle is used to track callbacks for the calls of this API.

    wallet_handle: this is the wallet_handle that contains the related data such as keys to be able to complete the function.

    ames_json: This should pass in a json string that follows the serialization format from above.

    my_vk: This should be the verkey that you wish to use to decrypt the message.

    output: A decrypted message

## Additional Questions

* Do we want this pack and unpack functionality to also handle the forwarding aspects on the next iteration?
* If so, how would we change the pack API to identify which person we want the message to go to if it's for multiple recipients? 
