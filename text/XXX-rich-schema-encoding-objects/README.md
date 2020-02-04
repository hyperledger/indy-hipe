# XXXX: Rich Schema Encoding Objects
- Author: Ken Ebert <ken@sovrin.org>, Mike Lodder <mike@sovrin.org>, Brent Zundel <brent.zundel@evernym.com>
- Start Date: 2019-03-19

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: 2020-01-16
- Status Note: part of [Rich Schema work](0119-rich-schemas/README.md)

## Summary

The introduction of rich schemas and their associated greater range of
possible attribute value data types require correspondingly rich
transformation algorithms. The purpose of the new encoding object is
to specify the algorithm used to perform transformations of each attribute
value data type into a canonical data encoding in a deterministic way. 

The initial use for these will be the transformation of attribute value
data into 256-bit integers so that they can be incorporated into the
anonymous credential signature schemes we use. The transformation
algorithms will also allow for extending the cryptographic schemes and
various sizes of canonical data encodings (256-bit, 384-bit, etc.). The
transformation algorithms will allow for broader use of predicate proofs,
and avoid hashed values as much as possible, as they do not support
predicate proofs.

## Motivation

All attribute values to be signed in anonymous credentials must be
transformed into 256-bit integers in order to support the 
[Camenisch-Lysyanskaya signature][CL-signatures] scheme.

The current Indy-SDK method for creating a credential only accepts
attributes which are encoded as 256-bit integers. The current libvcx
supports two source attribute types: numbers and strings. No configuration
method exists at this time to specify which transformation method will be
applied to a particular attribute for either the SDK or libvcx. All encoded
attribute values which are passed directly to the SDK were transformed by
software external to the SDK, relying on an implicit understanding of how
the external software should encode them. In libvcx, if the attribute value
at the time it is passed into libvcx is a number, it will be encoded as a
256-bit integer. If the attribute value is a string, the value will be
hashed using SHA-256, thereby encoding it as a 256-bit integer. The
resulting 256-bit integers may then be passed to the SDK and signed.

The current set of canonical encodings consists of integers and hashed
strings. The introduction of encoding objects allows for a means of
extending the current set of canonical encodings to include integer
representations of dates, lengths, boolean values, and floating point
numbers. All encoding objects describe how an input is transformed
into an encoding of an attribute value according to the transformation
algorithm selected by the issuer.

## Tutorial

### Intro to encoding objects
Encoding objects are JSON objects that describe the input types,
transformation algorithms, and output encodings. The encoding object
is stored on the ledger.

### Properties
An encoding object is identified by a DID, and is formatted as a DID
Document. It contains the following properties:

#### id
The DID which identifies the encodding object. The id-string of the
DID is the base58 representation of the SHA2-256 hash of the canonical form
of the value of the data object of the content property. The
canonicalization scheme we recommend is the IETF draft
[JSON Canonicalization Scheme (JCS).](https://tools.ietf.org/id/draft-rundgren-json-canonicalization-scheme-16.html)

#### name
The name of the encoding object as a utf-8 string value. By convention,
the name should be taken from the input and output encodings:
<input>_<output>

#### version
The version of this named encoding object.

#### hash_value
The hash of the encoding object contained in the content block data 
property.

#### encoding
The encoding object consists of:
- `input`: a description of the input value.
- `output`: a description of the output value
- `algorithm`:
  - `documentation`: a URL which references a specific github commit of
  the documentation that fully describes the transformation algorithm.
  - `implementation`: a URL that links to a reference implementation of the
  transformation algorithm. It is not necessary to use the implementation
  linked to here, as long as the implementation used implements the same
  transformation algorithm.
  - `description`: a brief description of the transformation algorithm.
- `test_vectors`: a URL which references a specific github commit of a
selection of test vectors that may be used to provide assurance that a
transformation algorithm implementation is correct. 


### Example Encoding
- data (object)
    The object with the encoding data
  - `@context`: Context for a DID document,
  - `id`: The encoding's DID; the id-string of its DID is the base58
  representation of the SHA2-256 hash of the canonical form of the value of
  the data object of the content property,
  - `content`: This property is used to hold immutable content:
    - `type`: "enc",
    - `name`: encoding's name string,
    - `version`: schema's version string,
    - `hash`:
      - `type`: the type of hash,
      - `value`: the hexadecimal value of the hash of the canonical form of
      the data object,
    - `data`: the encoding object

```
{
    "@context": [
        "https://www.w3.org/ns/did/v1", 
        "did:sov:yfXPxeoBtpQABpBoyMuYYGx"
    ],
    "id": "7u7cVZWrQ5VTdJxAsaaGFGqaDuuS4GU73d8DNWzVuMSX",
    "content":{
        "name":"DateRFC3339_UnixTime",
        "version":"1.0",
        "type": "enc",
        "hash":{
            "type": "SHA2-256",
            "value": "667fccbde4a43ea47922b9d943653f49c24cafecc2283db955348d60884aced8"
        },
        "data":{
            "encoding": {
                "input": {
                    "id": "DateRFC3339",
                    "type": "string"
                },
                "output": {
                    "id": "UnixTime",
                    "type": "integer"
                },
                "algorithm": {
                    "description": "This encoding transforms an
                        RFC3339-formatted datetime object into the number
                        of seconds since January 1, 1970 (the Unix epoch).",
                    "documentation": URL to specific github commit,
                    "implementation": URL to implementation
                },
                "test_vectors": URL to specific github commit
            }
        }
    },
    "identifier": "L5AD5g65TDQr1PPHHRoiGf",
    "endorser": "D6HG5g65TDQr1PPHHRoiGf",
    "reqId": 1514280215504647,
    "protocolVersion": 2,
    "signature": "5ZTp9g4SP6t73rH2s8zgmtqdXyTuSMWwkLvfV1FD6ddHCpwTY5SAsp8YmLWnTgDnPXfJue3vJBWjy89bSHvyMSdS"
}
```

## Reference
[reference]: #reference

The following is a 
[reference implementation of various transformation algorithms](https://github.com/sovrin-foundation/aries-credx-framework-rs/blob/master/src/encoding/mod.rs)

## Drawbacks
[drawbacks]: #drawbacks

This increases the complexity of issuing verifiable credentials and
verifiying the accompanying verifiable presentations. 

## Rationale and alternatives

Encoding attribute values as integers is already part of using anonymous
credentials, however the current method is implicit, and relies on use of a
common implementation library for uniformity. If we do not include
encodings as part of the Rich Schema effort, we will be left with an
incomplete set of possible predicates, a lack of explicit mechanisms for
issuers to specify which encoding methods they used, and a corresponding
lack of verifiablity of signed attribute values.

In another design that was considered, the encoding on the ledger was
actually a function an end user could call, with the ledger nodes
performing the transformation algorithm and returning the encoded value.
The benefit of such a design would have been the guarantee of uniformity
across encoded values. This design was rejected because of the
unfeasibility of using the ledger nodes for such calculations and the
privacy implications of submitting attribute values to a public ledger.

## Prior art

A description of a prior effort to add encodings to Indy may be found in
this [jira ticket](https://jira.hyperledger.org/browse/IS-786) and 
[pull request](https://github.com/hyperledger/indy-sdk/pull/1048).

What the prior effort lacked was a corresponding enhancement of schema
infrastructure which would have provided the necessary typing of attribute
values.

