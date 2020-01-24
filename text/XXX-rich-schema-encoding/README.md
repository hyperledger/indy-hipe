# XXXX: Rich Schema Encodings
- Author: Ken Ebert <ken@sovrin.org>, Mike Lodder <mike@sovrin.org>, Brent Zundel <brent.zundel@evernym.com>
- Start Date: 2019-03-19

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: 2020-01-16
- Status Note: part of [Rich Schema work](0119-rich-schemas/README.md)

## Summary

The introduction of rich schemas and their associated greater range of
possible attribute value data types require correspondingly rich encoding
algorithms. The purpose of the new encoding object is to specify the
algorithm used to perform transformations of each attribute value data type
into a canonical data type in a deterministic way. 

The initial use for encodings will be the transformation of attribute value
data into 256-bit integers so that they can be incorporated into the
anonymous credential signature schemes we use. The encoding algorithms
will also allow for extending the cryptographic schemes and various sizes
of canonical data types (256-bit, 384-bit, etc.). The encoding algorithms
will allow for broader use of predicate proofs, and avoid hashed values
where they are not needed, as they do not support predicate proofs.

## Motivation

All attribute values to be signed in anonymous credentials must be
transformed into 256-bit integers in order to support the 
[Camenisch-Lysyanskaya signature][CL-signatures] scheme.

The current Indy-SDK method for creating a credential only accepts
attributes which are encoded as 256-bit integers. The current libvcx
supports two source attribute types: numbers and strings. No configuration
method exists at this time to specify which encoding method will be applied
to a particular attribute for either the SDK or libvcx. All encoded
attribute values which are passed directly to the SDK were encoded by the
software external to the SDK, relying on implicit understanding of how the
external software should encode them. In libvcx, if the attribute value at
the time it is passed into libvcx is a number, it will be encoded as a
256-bit integer. If the attribute value is a string, the value will be
hashed using SHA-256, thereby encoding it as a 256-bit integer. The
resulting 256-bit integers may then be passed to the SDK and signed.

The current set of canonical values consists of integers and hashed
strings. The introduction of encoding objects allows for a means of
extending the current set of canonical values to include integer
representations of dates, lengths, and floating point numbers. All encoding
objects describe how the input is transformed into an integer
representation of an attribute value according to the encoding algorithm
selected by the issuer.

## Tutorial

### Intro to encodings
Encodings are JSON objects that describe the inputs, encoding algorithm,
and outputs. They are stored on the ledger.

### Properties
An encoding object is identified by a DID, and is formatted as a DID
Document. It contains the following properties:

#### id
The DID which identifies the encoding object. The id-string of its DID is
the base58 representation of the SHA2-256 hash of the canonical form of the
value of the data object of the content property. The canonicalization
scheme we recommend is the IETF draft JSON Canonicalization Scheme (JCS).

#### name
The name of the encoding as a utf-8 string value. By convention, the name
should be taken from <input>_<output>

#### version
The version of this named encoding.

#### hash_value
The hash of the encoding object contained in the content block data 
property.

#### encoding
The encoding object consists of:
- `input`: a description of the input value.
- `output`: a description of the output value
- `algorithm`:
  - `documentation`: a URL which references a specific github commit of
  the documentation that fully describes the algorithm.
  - `implementation`: a URL that links to a reference implementation of the
  algorithm. It is not necessary to use the implementation linked to here,
  as long as the implementation used implements the same algorithm.
  - `description`: a brief description of the algorithm.
- `test_vectors`: a URL which references a specific github commit of a
selection of test vectors that may be used to provide assurance that an
implementation is correct. 


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

Provide guidance for implementers, procedures to inform testing,
interface definitions, formal function prototypes, error codes,
diagrams, and other technical details that might be looked up.
Strive to guarantee that:

- Interactions with other features are clear.
- Implementation trajectory is well defined.
- Corner cases are dissected by example.

## Drawbacks

Why should we *not* do this?

## Rationale and alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not
choosing them?
- What is the impact of not doing this?

## Prior art

Discuss prior art, both the good and the bad, in relation to this proposal.
A few examples of what this can include are:

- Does this feature exist in other SSI ecosystems and what experience have
their community had?
- For other teams: What lessons can we learn from other attempts?
- Papers: Are there any published papers or great posts that discuss this?
If you have some relevant papers to refer to, this can serve as a more detailed
theoretical background.

This section is intended to encourage you as an author to think about the
lessons from other implementers, provide readers of your proposal with a
fuller picture. If there is no prior art, that is fine - your ideas are
interesting to us whether they are brand new or if they are an adaptation
from other communities.

Note that while precedent set by other communities is some motivation, it
does not on its own motivate an enhancement proposal here. Please also take
into consideration that Indy sometimes intentionally diverges from common
identity features.

## Unresolved questions

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
