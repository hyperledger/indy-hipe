- Name: AnonCrypt
- Author: Kyle Den Hartog
- Start Date: July 6th, 2018

# Summary
[summary]: #summary

This is a description of the necessary constraints as well as a proposed solution for anon_crypt.

# Motivation
[motivation]: #motivation

AuthCrypt is an API level call that will be available within Hyperledger Indy in order to meet the following requirements:
     Current Requirements:
        * Encrypt a payload
        * verify the integrity of the message with an HMAC

# Tutorial
[tutorial]: #tutorial

anon_crypt currently follows this pattern:

    1. generate random ed25519 keys pair
    2. get the ed25519 public key of receiver
    3. call DH(sender_priv_key, receiver_pub_key, random_nonce) to produce SYMMETRIC key
    4. encrypt the message with SYMMETRIC key
    5. add MAC
    6. Return tuple (encrypted message, MAC, random_pub_key, random_nonce)

# Drawbacks
[drawbacks]: #drawbacks

None that I can identify

# Rationale and alternatives
[alternatives]: #alternatives

It's built from a reputable library that handles the crypto primitives for us. This means it's more likely to be a secure implementation of cryptography.

# Prior art
[prior-art]: #prior-art

This has been built from NaCl's [crypto_box](https://nacl.cr.yp.to/box.html).

# Unresolved questions
[unresolved]: #unresolved-questions

None this is currently implemented. This HIPE is being submitted to add a description about AnonCrypt.