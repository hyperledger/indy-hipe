- Name: AMES
- Author: Kyle Den Hartog
- Start Date: 2018-07-10 (approximate, backdated)
- HIPE PR: (leave this empty)
- Jira Issue: (leave this empty)

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
` <header_json> . <content_encryption_key> . <iv> . <ciphertext> . <tag> `

Each of these are base64URL encoded strings which are dot (.) separated. 
The base64URL decoded header json will adhere to the following format:

```
{
    "typ" : "x-b64nacl",
    "alg" : "x-anon",
	"enc" : "xsalsa20poly1305",
	"kid" : "<recipient_verkey>",
	"jwk" : "<sender_verkey>" 
}
```

An example looks like the following:
`
eyJ0eXAiOiJ4LWI2NG5hY2wiLCJhbGciOiJ4LWF1dGgiLCJlbmMiOiJ4c2Fsc2EyMHBvbHkxMzA1Iiwia2lkIjoiQzVxMk1EbWRHMjZuVnc3M3loVmhkeiIsImp3ayI6IkVGYkM0V3hEWG1GZkhveW43bUNCbksifQ==.ZW5jcnlwdGVkX2tleQ==.RkFLRV9JVlRPVEVTVEpXTVNFUklBTElaRQ==.dW5lbmNyeXB0ZWQgdGV4dCB3aGljaCB3b3VsZCBub3JtYWxseSBiZSBlbmNyeXB0ZWQgYWxyZWFkeQ==.RkFLRV9UQUdUT1RFU1RKV01TRVJJQUxJWkU=
`

which would decode to the following data in tuple form hence the parentheses on the outer most layer:
```
(
    {
        "typ":"x-b64nacl",
        "alg":"x-auth",
        "enc":"xsalsa20poly1305",
        "kid":"C5q2MDmdG26nVw73yhVhdz",
        "jwk":"EFbC4WxDXmFfHoyn7mCBnK"
    },
    "encrypted_key",
    "FAKE_IVTOTESTJWMSERIALIZE",
    "unencrypted text which would normally be encrypted already"
    "FAKE_TAGTOTESTJWMSERIALIZE"
)
```

## Additional IndySDK APIs

### unpack_message(JWM, my_vk) -> plaintext message :
The unpack function is used to decrypt a message on the receiver side. It will output the plaintext of the corresponding pack_message if the verkey provided is found within the header. This works for both compact serializations and for JSON serializations.

The parameters should be used in this way:

    JWM: This should pass in a json string that follows one of the two serializations provided above.

    my_vk: This should be the verkey that you wish to use to decrypt the message.

    output: A decrypted message

### pack_message(plaintext, auth, recv_keys, wallet_handle, my_vk) -> JSON String:
The purpose of this function is to take in a message, encrypt the message for the keys specified and output a JSON string with one of the two serializations identified above.

The parameters should be used in this way:
    
    plaintext: This should be the message that is intended to be encrypted. It's required and should be of type String. The most common forms of messages that will be passed in here are json strings that follow the format of a particular message family.
    
    auth: This is a boolean type that should be passed true if authcrypt should be used or false if anoncrypt should be used.
    
    recv_keys: This is a list of verkeys passed as a string. If only 1 key is passed in, then a Compact serialization will be outputed. If > 1 keys are passed in then JSON serialization will be outputted from this function.

    wallet_handle: this is the wallet_handle that contains the key used to encrypt the message (when using authcrypt). It is required even if using anoncrypt.

    my_vk: This is an optional parameter that must include a verkey as a string if auth is set to true (authcrypting). Otherwise, this must be set to none if anoncrypt is being used.  

    output: a string in the form of either JSON serialization or Compact serialization


