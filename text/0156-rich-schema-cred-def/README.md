# Indy HIPE 0156: Rich Schema Credential Definition
- Authors: Alexander Shcherbakov <alexander.shcherbakov@evernym.com>, Brent Zundel <brent.zundel@evernym.com>, Ken Ebert <ken@sovrin.org>
- Start Date: 2020-13-03

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: 2019-13-03
- Status Note: part of [Rich Schema work](0119-rich-schemas/README.md)



## Summary
[summary]: #summary

Credential Definition can be used by the Issuer to set public keys for a particular
 [Rich Schema](https://github.com/hyperledger/indy-hipe/tree/master/text/0149-rich-schema-schema)
  and [Mapping](https://github.com/hyperledger/indy-hipe/tree/master/text/0155-rich-schema-mapping).
The public keys can be used for signing the credentials by the Issuer according to the order and encoding of attributes
defined by the referenced Mapping.


Credential Definition objects are processed in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common).


## Motivation
[motivation]: #motivation

The current format for Indy credential definitions provides a method for
issuers to specify a schema and provide public key data for credentials
they issue. This ties the schema and public key data values to the issuer's
DID. The verifier uses the credential definition to check the validity of
each signed credential attribute presented to the verifier.

The new credential definition object that uses rich schemas is a minor
modification of the current Indy credential definition. The new format has
the same public key data. In addition to referencing a schema, the new
credential definition can also reference a mapping object.


## Tutorial
[tutorial]: #tutorial

### Intro to Credential Definition
Credential definitions are written to the ledger so they can be used by holders and verifiers 
in presentation protocol.

A Credential Definition can reference a single Mapping and a single Rich Schema only.

Credential Definition is a JSON object.

Credential Definition should be immutable in most of the cases.
Some application may consider it as a mutable object since the Issuer may rotate
keys present there.
However, rotation of Issuer's keys should be done carefully as it will invalidate all
credentials issued for this key.

 

### Properties

Credential definition's properties follow the generic template defined in [Rich Schema Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#how-rich-schema-objects-are-stored-on-the-ledger).

Credential Definition's `content` field is a JSON-serialized string with the following fields:

#### signatureType
Type of the ZKP signature. `CL` (Camenisch-Lysyanskaya) is the only supported type now. 

#### mapping
An `id` of the corresponding Mapping

#### schema
An `id` of the corresponding Rich Schema. The `mapping` must reference the same Schema.

#### publicKey
Issuer's public keys. Consists of `primary` and `revocation` keys.

### Example Credential Definition
An example of the `content` field of a Credential Definition object:
```
"signatureType": "CL",
"mapping": "did:sov:UVj5w8DRzcmPVDpUMr4AZhJ",
"schema": "did:sov:U5x5w8DRzcmPVDpUMr4AZhJ",
"publicKey": {
    "primary": "...",
    "revocation": "..."
}
```

### Use in Verifiable Credentials
A ZKP credential created according to the `CL` signature scheme must reference a Credential Definition used 
for signing. A Credential Definition is referenced in the [credentialSchema](https://www.w3.org/TR/vc-data-model#data-schemas)
property. A Credential Definition is referenced by its `id`.


### Stored on Ledger
Credential Definition will be written to the ledger in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#how-rich-schema-objects-are-stored-on-the-ledger).


### Indy Node Rich Schema API
Indy Node processes ledger transaction requests via request handlers.

There is a write request handler for `RICH_SCHEMA_CRED_DEF` transaction.
The numerical code for a `RICH_SCHEMA_CRED_DEF` transaction is `204`.

A Rich Schema can be obtained from the Ledger by the generic `GET_RICH_SCHEMA_OBJECT_BY_ID` and `GET_RICH_SCHEMA_OBJECT_BY_METADATA`
requests (see [Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#querying-rich-schema-objects-from-the-ledger)).
The numerical code for a `GET_RICH_SCHEMA_OBJECT_BY_ID` transaction is `300`.
The numerical code for a `GET_RICH_SCHEMA_OBJECT_BY_METADATA` transaction is `301`.


#### RICH_SCHEMA_CRED_DEF Transaction
Adds a Credential Definition object as part of Rich Schema feature.


- `id` (string):

     A unique ID (for example a DID with an id-string being base58 representation of the SHA2-256 hash of the `content` field)
     
- `content` (json-serialized string): 

    Credential Definition object as JSON serialized in canonical form.
   
    - `signatureType` (string):  Type of the ZKP signature. `CL` (Camenisch-Lysyanskaya) is the only supported type now.
    - `mapping` (string):  An `id` of the corresponding Mapping
    - `schema` (string): An `id` of the corresponding Rich Schema. The `mapping` must reference the same Schema.
    - `publicKey` (dict): Issuer's public keys. Consists ot primary and revocation keys.
        - `primary` (dict): primary key
        - `revocation` (dict, optional): revocation key
    

- `rsType` (string):

    Rich Schema's type. Currently expected to be `cdf`.
    
- `rsName` (string):

    Rich Schema's name
    
- `rsVersion` (string):

    Rich Schema's version
        
The combination of `rsType`, `rsName`, and `rsVersion` must be unique among all rich schema objects on the ledger.

The generic patterns for `RICH_SCHEMA_CRED_DEF` transaction, request, and reply can be found in [Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#common-template-for-all-write-requests-for-rich-schema-objects).

### Indy VDR API
Indy VDR methods for adding and retrieving a Credential Definition from the
ledger comply with the generic approach described in [Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#indy-vdr-api).

This means the following methods can be used:
- `indy_build_rich_schema_object_request`
- `indy_build_get_schema_object_by_id_request`
- `indy_build_get_schema_object_by_metadata_request`'


## Reference
[reference]: #reference

More information on the Verifiable Credential data model use of `schemas`
may be found [here](https://w3c.github.io/vc-data-model/#data-schemas)

- [0119: Rich Schema Objects](https://github.com/hyperledger/indy-hipe/tree/master/text/0119-rich-schemas)
- [0120: Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common) 
- [Common write request structure](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#common-write-request-structure)
- [Common read request structure](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#common-request-structure)
- [Common transaction structure](https://github.com/hyperledger/indy-node/blob/master/docs/source/transactions.md#common-structure)
- [Common reply structure for write requests](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#reply-structure-for-write-requests)
- [Common reply structure for read requests](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#reply-structure-for-read-requests)



## Drawbacks
[drawbacks]: #drawbacks
Rich schema objects introduce more complexity.


## Unresolved Questions and Future Work
[unresolved]: #unresolved-questions

- Of all the Rich Schema objects, the CredDef most closely fits the format of a DID DOC.
- However, we are not defining Rich Schema objects as DID DOCs for now. We may re-consider this in future once DID DOC format
is finalized.
- It may make sense to extend DID specification to include using DID for referencing Rich Schema objects.
- The proposed canonicalization form of a content to be used for DID's id-string generation is in a Draft version, so we 
may find a better way to do it.

