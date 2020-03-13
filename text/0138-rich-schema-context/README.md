# 0138: Contexts for Rich Schema Objects
- Author: Ken Ebert <ken@sovrin.org>, Brent Zundel <brent.zundel@evernym.com>, Alexander Shcherbakov <alexander.shcherbakov@evernym.com>
- Start Date: 2019-06-07T13:51:17-06:00

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: 2019-06-18
- Status Note: part of [Rich Schema work](0119-rich-schemas/README.md)

## Summary
[summary]: #summary

Every rich schema object may have an associated `@context`. Contexts are JSON or JSON-LD
objects. They are the standard mechanism for defining shared semantic
meaning among rich schema objects.

Context objects are processed in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common).

## Motivation
[motivation]: #motivation

`@context` is JSON-LD’s namespacing mechanism. Contexts allow schemas,
mappings, presentations, etc. to use a common vocabulary when referring to
common attributes, i.e. they provide an explicit shared semantic meaning.

## Tutorial
[tutorial]: #tutorial

### Intro to @context
`@context` is a JSON-LD construct that allows for namespacing and the
establishment of a common vocabulary.

Context object is immutable, so it's not possible to update existing Context, 
If the Context needs to be evolved, a new Context with a new version or name needs to be created.

Context object may be stored in either JSON or JSON-LD format.

### Example Context
An example of the `content` field of a Context object:
```
"@context": [
    "did:sov:UVj5w8DRzcmPVDpUMr4AZhJ,
    "did:sov:AZKWUJ3zArXPG36kyTJZZm",
    "did:sov:9TDvb9PPgKQUWNQcWAFMo4",
    {
          "dct": "http://purl.org/dc/terms/",
          "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
          "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
          "Driver": "did:sov:35qJWkTM7znKnicY7dq5Yk:8:driver:2.4",
          "DriverLicense": "did:sov:Q6kuSqnxE57waPFs2xAs7q:8:driver-license:3.5",
          "CategoryOfVehicles": "DriverLicense:CategoryOfVehicles"
    }
]
```

### Stored on Ledger
`@context` will be written to the ledger in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#how-rich-schema-objects-are-stored-on-the-ledger).


### Indy Node Context API
Indy Node processes ledger transaction requests via request handlers.

There is a write request handler for `JSON_LD_CONTEXT` transaction.
The numerical code for a `JSON_LD_CONTEXT` transaction is `200`.

A Context can be obtained from the Ledger by the generic `GET_RICH_SCHEMA_OBJECT_BY_ID` and `GET_RICH_SCHEMA_OBJECT_BY_METADATA`
requests (see [Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#querying-rich-schema-objects-from-the-ledger)).
The numerical code for a `GET_RICH_SCHEMA_OBJECT_BY_ID` transaction is `300`.
The numerical code for a `GET_RICH_SCHEMA_OBJECT_BY_METADATA` transaction is `301`.


#### JSON_LD_CONTEXT Transaction

Adds a JSON LD Context as part of Rich Schema feature.

It's not possible to update an existing Context.
If the Context needs to be evolved, a new Context with a new id and name-version needs to be created.



- `id` (string):

     A unique ID (for example a DID with an id-string being base58 representation of the SHA2-256 hash of the `content` field)
     
- `content` (json-serialized string): 

    Context object as JSON serialized in canonical form. It must have `@context` as a top level key.
    The `@context` value must be either:
    1) a URI (it should dereference to a Context object)
    2) a Context object (a dict)
    3) an array of Context objects and/or Context URIs

- `rsType` (string):

    Context's type. Currently expected to be `ctx`.
    
- `rsName` (string):

    Context's name
    
- `rsVersion` (string):

    Context's version
        
The combination of `rsType`, `rsName`, and `rsVersion` must be unique among all rich schema objects on the ledger.

The generic patterns for `JSON_LD_CONTEXT` transaction, request, and reply can be found in [Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#common-template-for-all-write-requests-for-rich-schema-objects).



### Indy VDR API
Indy VDR methods for adding and retrieving `@context` from the
ledger comply with the generic approach described in [Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#indy-vdr-api).

This means the following methods can be used:
- `indy_build_rich_schema_object_request`
- `indy_build_get_schema_object_by_id_request`
- `indy_build_get_schema_object_by_metadata_request`


## Reference
[reference]: #reference

More information on the Verifiable Credential data model use of `@context`
may be found [here](https://w3c.github.io/vc-data-model/#contexts).

More information on `@context` from the JSON-LD specification may be found
[here](https://w3c.github.io/json-ld-syntax/#the-context) and
[here](https://w3c.github.io/json-ld-syntax/#advanced-context-usage).

- [0119: Rich Schema Objects](https://github.com/hyperledger/indy-hipe/tree/master/text/0119-rich-schemas)
- [0120: Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common) 
- [Common write request structure](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#common-write-request-structure)
- [Common read request structure](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#common-request-structure)
- [Common transaction structure](https://github.com/hyperledger/indy-node/blob/master/docs/source/transactions.md#common-structure)
- [Common reply structure for write requests](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#reply-structure-for-write-requests)
- [Common reply structure for read requests](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#reply-structure-for-read-requests)


## Drawbacks
[drawbacks]: #drawbacks
Requiring a `@context` for each rich schema object introduces more
complexity.


## Rationale and alternatives
[alternatives]: #alternatives

Though requiring a `@context` for each rich schema object increases the
complexity of the system, it also provides a means for better managing the
complexity already present.

## Unresolved questions and future work
[unresolved]: #unresolved-questions

- We are not defining Rich Schema objects as DID DOCs for now. We may re-consider this in future once DID DOC format
is finalized.
- It may make sense to extend DID specification to include using DID for referencing Rich Schema objects.
- The proposed canonicalization form of a content to be used for DID's id-string generation is in a Draft version, so we 
may find a better way to do it.
- We don't check if the specified `@context` is valid by resolving all external links. 


