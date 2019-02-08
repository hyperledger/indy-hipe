# 0020: Encryption Primitives
- Name: encryption-primitives
- Author: Kyle Den Hartog
- Start Date: July 6th, 2018

## Summary
[summary]: #summary

This HIPE describes two important crypto primitives that underpin
Indy's secure communications strategy: anon_crypt and auth_crypt.

## Motivation
[motivation]: #motivation

anon_crypt is an API level call that will be available within Hyperledger Indy in order to meet the following requirements:

* Encrypt a payload
* verify the integrity of the message with an HMAC

auth_crypt is an API level call that will be available within Hyperledger Indy in order to meet the following requirements:

* Encrypt a payload
* verify the integrity of the message with an HMAC
* verify the sender of the message in a repudiable way

## Tutorial
[tutorial]: #tutorial

#### anon_crypt
[anon_crypt]: anon_crypt

anon_crypt currently follows this pattern:

1. generate random ed25519 keys pair
2. get the ed25519 public key of receiver
3. call DH(random_priv_key, receiver_pub_key, random_nonce) to produce SYMMETRIC key
4. encrypt the message with SYMMETRIC key
5. add MAC
6. Return tuple (encrypted message, MAC, random_pub_key, random_nonce)
    
#### auth_crypt
[auth_crypt]: auth_crypt

auth_crypt currently follows this pattern:

1. get sender ed25519 key pair
2. get the ed25519 public key of receiver
3. call DH(sender_priv_key, receiver_pub_key, random_nonce) to produce SYMMETRIC key
4. encrypt the message with SYMMETRIC key
5. add MAC
6. Get tuple (encrypted message, MAC, random_nonce)
7. Add sender public key and anon_crypt the whole message


## Drawbacks
[drawbacks]: #drawbacks

Perfect Forward secrecy is currently not implemented with auth_crypt because it relies upon a non-ephemeral Diffie-Hellman key exchange to generate the symmetrical key.

## Rationale and alternatives
[alternatives]: #alternatives

anon_crypt is built from a reputable library that handles the crypto primitives for us. This means it's more likely to be a secure implementation of cryptography.

An alternative solution for auth_crypt, that would be more restrictive but easier to understand, would be to perform a non-repudiable signature on the message before encrypting and adding the signature field to the plaintext of the message before encryption. The downsides to this is that it provides more data than is necessary for the general usecase, so repudiable authentication was the better choice. This allows for a person to add a non-repudiable signature optionally as well.

## Prior art
[prior-art]: #prior-art

anon_crypt has been built from Libsodium's [sealed_box](https://download.libsodium.org/doc/public-key_cryptography/sealed_boxes).
auth_crypt has been built from Libsodium's [crypto_box](https://download.libsodium.org/doc/public-key_cryptography/authenticated_encryption) with some minor tweaks. 

## Unresolved questions
[unresolved]: #unresolved-questions

None; this is already implemented. This HIPE is being submitted to describe what we have.