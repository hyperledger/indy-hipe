# Replace Indy-Crypto with Ursa
- Author: Michael Lodder
- Start Date: 2019-02-05

## Status
- Status: [ADOPTED](/README.md#hipe-lifecycle)
- Status Date: (date of first submission or last status change)
- Status Note: (explanation of current status; if adopted, 
  links to impls or derivative ideas; if superseded, link to replacement)

## Summary
Indy will replace [indy-crypto](https://github.com/hyperledger/indy-crypto) with [ursa](https://github.com/hyperledger/ursa)
as its library for handling encryption, key exchange, signing, and anonymous credentials.


## Motivation
Hyperledger Ursa currently contains the same APIs and crypto code as Indy-Crypto that is consumed by Indy-SDK.
Ursa plans to support many more cryptographic primitives than what is currently supported by Indy-Crypto.
Indy-Crypto which is the library that Indy uses for much of this is already included in Ursa.
Indy currently implements its own crypto code for handling encryption, key exchange,
signing, and anonymous credentials. Ursa offers the same primitives and more.

## Tutorial
There are many similarities between Indy-Crypto and Ursa so changes should be minimal.
Here is a short list of some required code changes


|  | Indy-Crypto | Ursa |
| - | ----------- | ---- |
| Function Prefix | indy\_crypto_ or indy_ | ursa_ |
| Error Names | IndyCryptoError | UrsaCryptoError |


Ursa is now available as a [crate](https://crates.io/crates/ursa). This means that
Indy SDK can use Ursa directly in rust. Ursa's rust APIs are identical otherwise
to Indy-Crypto. Indy-Node uses Indy-Crypto's python wrapper to handle the BLS
signature. The C callable interfaces for BLS are identical except as noted so the python wrapper
will need to change the name of the function calls only.

Indy-SDK could also remove dependencies used for encryption/decryption,
hashing, key exchange, signing and verification and use Ursa instead. Two
such dependencies are the crates sodium-oxide and openssl.

Indy-SDK will use Ursa stable crate releases and only choose the features it plans to consume.
Sovrin plans to have a CI pipeline for Ursa that chooses the features that Indy-SDK will need.

## Reference
https://github.com/hyperledger/ursa

[Ursa Project proposal](https://docs.google.com/document/d/1JtFT5L-82egj6shgGXzTsNAg6_UHuMheKfsst6NS_Xo/edit)

## Drawbacks
Indy uses signatures and anonymous credentials not used in other projects yet.
It might be easier to develop these without worry of breaking changes with
other Hyperledger projects.

## Rationale and alternatives
Ursa is the crypto project that will be adopted by most of Hyperledger.
By switching to Ursa, Indy will be able to utilize crypto used by other Hyperledger projects and
take advantage of the many cryptographers and crypto engineers that are involved verify crypto correctness
and its development.

## Prior art
None at this time.

## Unresolved questions
None at this time.
