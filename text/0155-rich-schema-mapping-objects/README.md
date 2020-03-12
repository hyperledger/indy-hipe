# Indy HIPE 0155: Rich Schema Schemas
- Authors: [Alexander Shcherbakov](<alexander.shcherbakov@evernym.com>), [Brent Zundel](<brent.zundel@evernym.com>), [Ken Ebert](<ken@sovrin.org>)
- Start Date: 2020-12-03

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: 2019-12-03
- Status Note: part of [Rich Schema work](0119-rich-schemas/README.md)



## Summary
[summary]: #summary

Mappings serve as a bridge between rich schemas and the flat array of
signed integers. A mapping specifies the order in which attributes are
transformed and signed. It consists of a set of graph paths and the
encoding used for the attribute values specified by those graph paths. Each
claim in a mapping has a reference to an encoding, and those encodings are
defined in encoding objects.

Mapping objects are processed in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common).


## Motivation
[motivation]: #motivation

Rich schemas are complex, hierarchical, and possibly nested objects. The
[Camenisch-Lysyanskaya signature][CL-signatures] scheme used by Indy
requires the attributes to be represented by an array of 256-bit integers.
Converting data specified by a rich schema into a flat array of integers
requires a mapping object.


## Tutorial
[tutorial]: #tutorial

### Intro to mappings
Mappings are written to the ledger so they can be shared by multiple
credential definitions. 
A Credential Definition can reference a single Mapping only.

One or more Mappings can be referenced by a Presentation Definition.
The mappings serve as a vital part of the verification process. The
verifier, upon receipt of a presentation must not only check that the array
of integers signed by the issuer is valid, but that the attribute values
were transformed and ordered according to the mapping referenced in the
credential definition.
 
A Mapping references one and only one Rich Schema object. If there is no Schema Object 
a Mapping can reference, a new Schema must be created on the ledger.
If a Mapping needs to map attributes from multiple Schemas, then a new Schema embedding the multiple Schemas 
must be created and stored on the ledger.    
 
Mappings need to be discoverable.

Mapping is a JSON-LD object following the same structure (attributes and graph pathes) 
as the corresponding Rich Schema.
A Mapping may contain only a subset of the original Rich Schema's attributes.

The value of every schema attribute in a Mapping object is an array of the following pairs:
- encoding object (referenced by its `id`) to be used for representation of the attribute as an integer
- rank of the attribute to define the order in which the attribute is signed by the Issuer.

The value is an array as the same attribute may be used in Credential Definition multiple times
with different encodings. 
 
 
   

Note: The anonymous credential signature scheme used by Indy is
[Camenisch-Lysyanskaya signatures][CL-signatures]. It is the use of this
signature scheme in combination with rich schema objects that necessitates
a mapping object. If another signature scheme is used which does not have
the same requirements, a mapping object may not be necessary or a different
mapping object may need to be defined.

### Properties

Mapping's properties follow the generic template defined in [Rich Schema Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#how-rich-schema-objects-are-stored-on-the-ledger).

Mapping's `content` field is a JSON-LD with the following fields:

#### @id
A Mapping must have an `@id` property. The value of this property must
be equal to the `id` field which is a DID (see [Identification of Rich Schema Objects](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#identification-of-rich-schema-objects)). 

#### @type
A Mapping must have a `@type` property. The value of this property must
be (or map to, via a context object) a URI. 

#### @context
A Mapping may have a `@context` property. If present, the value of this
property must be a
[context object](../0138-rich-schema-context/README.md) or a URI which can
be dereferenced to obtain a context object.

#### schema

An `id` of the corresponding Rich Schema

#### Values
The value of every schema attribute in a Mapping object is an array of the following pairs:

- `enc` (string): encoding object (referenced by its `id`) to be used for representation of the attribute as an integer
- `rank` (int): rank of the attribute to define the order in which the attribute is signed by the Issuer

### Example Mapping
Let's consider the following Rich Schema:
```
    '@id': "did:sov:4e9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    '@context': "did:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    '@type': "rdfs:Class",
    "rdfs:comment": "ISO18013 International Driver License",
    "rdfs:label": "Driver License",
    "rdfs:subClassOf": {
        "@id": "sch:Thing"
    },
    "driver": "Driver",
    "dateOfIssue": "Date",
    "dateOfExpiry": "Date",
    "issuingAuthority": "Text",
    "licenseNumber": "Text",
    "categoriesOfVehicles": {
        "vehicleType": "Text",
        "dateOfIssue": "Date",
        "dateOfExpiry": "Date",
        "restrictions": "Text",
    },
    "administrativeNumber": "Text"
```

Then the corresponding Mapping object will look as follows:
```
    '@id': "did:sov:5e9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    '@context': "did:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    '@type': "rdfs:Class",
    "schema": "did:sov:4e9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    "driver": [{
        "enc": "did:sov:1x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
        "rank": 5
    }],
    "dateOfIssue": [{
        "enc": "did:sov:2x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
        "rank": 4
    }],
    "issuingAuthority": [{
        "enc": "did:sov:3x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
        "rank": 3
    }],
    "licenseNumber": [
        {
            "enc": "did:sov:4x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
            "rank": 1
        },
        {
            "enc": "did:sov:5x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
            "rank": 2
        },
    ],
    "categoriesOfVehicles": {
        "vehicleType": [{
            "enc": "did:sov:6x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
            "rank": 6
        }],
        "dateOfIssue": [{
         "enc": "did:sov:7x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
            "rank": 7
        }],
    },
    "administrativeNumber": [{
        "enc": "did:sov:8x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
        "rank": 8
    }]
```

### Stored on ledger
Mapping will be written to the ledger in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#how-rich-schema-objects-are-stored-on-the-ledger).


### Indy Node Rich Schema API
Indy Node processes ledger transaction requests via request handlers.

There is a write request handler for `RICH_SCHEMA_MAPPING` transaction.
The numerical code for a `RICH_SCHEMA_MAPPING` transaction is `203`.

A Rich Schema can be get from the Ledger by the generic `GET_RICH_SCHEMA_OBJECT_BY_ID` and `GET_RICH_SCHEMA_OBJECT_BY_METADATA`
requests (see [Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#querying-rich-schema-objects-from-the-ledger)).
The numerical code for a `GET_RICH_SCHEMA_OBJECT_BY_ID` transaction is `300`.
The numerical code for a `GET_RICH_SCHEMA_OBJECT_BY_METADATA` transaction is `301`.


#### RICH_SCHEMA_MAPPING Transaction
Adds a Mapping object as part of Rich Schema feature.

It's not possible to update an existing Rich Schema.
If the Rich Schema needs to be evolved, a new Rich Schema with a new id and name-version needs to be created.



- `id` (string):

     A unique ID (for example a DID with a id-string being base58 representation of the SHA2-256 hash of the `content` field)
     
- `content` (json-serialized string): 

    Mapping object as JSON serialized in canonical form.
    This value must be a json-ld object. json-ld supports many parameters that are optional for a rich schema txn.
    However, the following parameters must be there:
    
    - `@id`:  The value of this property must be (or map to, via a context object) a URI.
    - `@type`: The value of this property must be (or map to, via a context object) a URI.
    - `@context`(optional): If present, the value of this property must be a context object or a URI which can be dereferenced to obtain a context object.
    - `schema`:  An `id` of the corresponding Rich Schema
    
    The value of every schema attribute in a Mapping object is an array of the following pairs:
    - `enc` (string): encoding object (referenced by its `id`) to be used for representation of the attribute as an integer
    - `rank` (int): rank of the attribute to define the order in which the attribute is signed by the Issuer


- `rsType` (string):

    Rich Schema's type. Currently expected to be `sch`.
    
- `rsName` (string):

    Rich Schema's name
    
- `rsVersion` (string):

    Rich Schema's version
        
`rsType`, `rsName` and `rsVersion` must be unique among all rich schema objects on the ledger.

The generic patterns for `JSON_LD_CONTEXT` transaction, request and reply can be found in [Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#common-template-for-all-write-requests-for-rich-schema-objects).

### Indy VDR API
Indy VDR methods for adding and retrieving a Rich Schema from the
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

Implementing an Indy-Node ledger transaction for `mapping` in a way that
follows the existing methodology may increase the existing technical debt
that is found in those libraries.

## Unresolved questions and future work
[unresolved]: #unresolved-questions


