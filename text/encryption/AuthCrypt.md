- Name: AuthCrypt
- Author: Kyle Den Hartog (kyle.denhartog@evernym.com)
- Start Date: July 6th, 2018
- PR: a while ago
- Jira Issue: 

# Summary
[summary]: #summary

This is a description of the necessary constraints as well as the current implementation description for AuthCrypt.

# Motivation
[motivation]: #motivation

AuthCrypt is an API level call that will be available within Hyperledger Indy in order to meet the following requirements:
Current Requirements:
    * Encrypt a payload
    * verify the integrity of the message with an HMAC
    * verify the sender of the message in a repudiable way

# Tutorial
[tutorial]: #tutorial

auth_crypt currently follows this pattern:

    1. get sender ed25519 key pair
    2. get the ed25519 public key of receiver
    3. call DH(sender_priv_key, receiver_pub_key, random_nonce) to produce SYMMETRIC key
    4. encrypt the message with SYMMETRIC key
    5. add MAC
    6. Get tuple (encrypted message, MAC, random_nonce)
    7. Add sender public key and anon_crypt the whole message


# Drawbacks
[drawbacks]: #drawbacks

Perfect Forward secrecy is currently not implemented with AuthCrypt because it relies upon a non-ephemeral diffie-hellman key exchange to generate the symmetrical key

# Rationale and alternatives
[alternatives]: #alternatives

An alternative solution, that would be more restrictive but easier to understand, would be to perform a non-repudiable signature on the message before encrypting and adding the signature field to the plaintext of the message before encryption. The downsides to this is that it provides more data than is necessary for the general usecase, so repudiable authentication was the better choice. This allows for a person to add a non-repudiable signature optionally as well.

# Prior art
[prior-art]: #prior-art

This has been built from Libsodium's [crypto_box](https://download.libsodium.org/doc/public-key_cryptography/authenticated_encryption) with some minor tweaks.

# Unresolved questions
[unresolved]: #unresolved-questions

None this is currently implemented. This HIPE is being submitted to add a description about AuthCrypt.
