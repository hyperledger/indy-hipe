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
    "encoding": {
        "input": {
            "id": "DateRFC3339",
            "type": "string"
        },
        "output": {
            "id": "UnixTime",
            "type": "256-bit integer"
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
```

### Transformation Algorithms

The purpose of a transformation algorithm is to deterministically convert
a value into a different encoding. For example, an attribute value may be
a string representation of a date, but the CL-signature signing mechanism
requires all inputs to be 256-bit integers. The transformation algorithm
takes this string value as input, parses it, and encodes it as a 256-bit
integer.  

It is anticipated that the encodings used for CL signatures and their
associated transformation algorithms will be used primarily by two
entities. First, the issuer will use the transformation algorithm to
prepare credential values for signing. Second, the verifier will use the
transformation algorithm to verify that revealed values were correctly
encoded and signed, and to properly transform values against which
predicates may be evaluated.

#### Integer Representation

In order to properly encode values as integers for use in predicate proofs,
a common 256-bit integer representation is needed. Predicate proofs are
kept simple by requiring all inputs to be represented as positive integers.
To accomplish this, we introduce a zero-offset and map all integer results
onto a range from 9 to 2<sup>256</sup> - 10. The zero point in this range
is 2<sup>255</sup>. 

Any transformation algorithm which outputs an integer value should use this
representation.

#### Floating Point Representation
In order to retain the provided precision of floating point values, we use
[Q number format](https://en.wikipedia.org/wiki/Q_(number_format)), a
binary, fixed-point number format. We use 64 fractional bits.


#### Reserved Values

For integer and floating point representations, there are some reserved
numeric strings which have a special meaning.

| Special Value | Representation         | Description |
| ------------- | ---------------------- | ----------- |
| -∞            | 8                      | The largest negative number.<br>Always less than any other valid integer. |
| ∞             | 2<sup>256</sup> - 9    | The largest positive number.<br>Always greater than any other valid integer. |
| NULL          | 7                      | Indicates that the value of a field is not supplied.<br>Not a valid value for comparisons. |
| NaN           | 2<sup>256</sup> - 8    | Floating point NaN.<br>Not a valid value for comparisons. |
| reserved      | 1 to 6                 | Reserved for future use. |
| reserved      | 2<sup>256</sup> - 7 to 2<sup>256</sup> - 1 | Reserved for future use. |


#### Documentation
The value of the documentation field is intended to be a URL which, when
dereferenced, will provide specific information about the transformation
algorithm such that it may be implemented. We recommend that the URL
reference some immutable content, such as a specific github commit, an IPFS
file, etc.


#### Implementation
The value of the implementation field is intended to be a URL which, when
dereferenced, will provide a reference implementation of the transformation
algorithm.

#### Test Vectors
Test vectors are very important. Although not comprehensive, a set of
public test vectors allows for multiple implementations to verify adherence
to the transformation algorithm for the set. Test vectors should consist of
a set of comma-separated input/output pairs. The input values should be
read from the file as strings. The output values should be byte strings
encoded as hex values.

The value of the test_vectors field is intended to be a URL which, when
dereferenced, will provide the file of test vectors. We recommend that the
URL reference some immutable content, such as a specific github commit, an
IPFS file, etc.

#### Example Test Vector for 
```

``` 


### Indy and Aries
The complete architecture for encoding objects involves three separate
repositories:
- `indy-node`: The code run by a validator node participating in an
instance of the indy ledger, e.g., the validators node in the Sovrin
network run `indy-node`. Changes to this code will enable encoding
objects to be written to and retrieved from an instance of indy.
- `indy-data-manager`: code which a client may use to communicate with
validator nodes in an indy network. Changes to this code will enable
encoding transaction requests to be sent to validator nodes.
`indy-data-manager` complies with the interface described by the
`aries-verifiable-data-registry-interface` and is built to plug in to the aries
ecosystem.
- `aries-vdri`: This is the location of the `aries-verifiable-data-registy-interface`.
Changes to this code will enable users of any data registry with an
`aries-vdri`-compatible data manager to handle encoding objects.

Only changes to the indy repositories are described here. For a description
of the changes to aries, please see
[this rfc](TBD).


### Indy Node encoding API
Indy Node processes ledger transaction requests via request handlers.
Adding `SET_ENCODING` and `GET_ENCODING` ledger transactions will involve
creating both a `write` request handler, and a `read` request handler.

The numerical code for a `SET_ENCODING` transaction is 204.
The numerical code for a `GET_ENCODING` transaction is 304.

This will be done following the pattern for `schema_handler.py` and
`get_schema_handler.py`

#### SET_ENCODING
Adds an encoding object to the ledger.

It's not possible to update an existing encoding object. So, if the
encoding object needs to be modified, a new encoding object needs to be
created.

- `data` (dict):

  Dictionary with encoding object's data:

  - `id`: The encoding object's DID 
  - `content`: 
    - `type`: "enc"
    - `name`: encoding object's name string
    - `version`: encoding object's version string
    - `hash`:
      - `type`: the type of hash,
      - `value`: the hexadecimal value of the hash of the canonical form of
      the data object
    - `data`: The value of this property is an encoding object
      - `encoding`:
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
        - `test_vectors`:
       
*Request Example*:
```
{
    "operation": {
        "type": "204",
        "data":{
            "id": "BmfFKwjEEA9W5xmSqwToBkrpYa3rGowtg5C54hepEVdA",
            "content":{
                "type": "ctx",
                "name":"DateRFC3339_UnixTime",
                "version":"1.0",
                "hash":{
                    "type": "SHA2-256",
                    "value": ""
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
                            "documentation": "https://github.com/sovrin-foundation/aries-credx-framework-rs/commit/efba6afd119ac53220ed4745265a95fd3344737d",
                            "implementation": "https://github.com/sovrin-foundation/aries-credx-framework-rs/"
                        },
                        "test_vectors": "https://github.com/sovrin-foundation/aries-credx-framework-rs/commit/a7b1712bd19c27b97a0db37920d98bfb9a3a6722"
                    }
                }
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
*Reply Example*:
```
{
    "op": "REPLY", 
    "result": {
        "ver": 1,
        "txn": {
            "type":"204",
            "protocolVersion":2,
            
            "data": {
                "ver":1,
                "data":{
                    "id": "BmfFKwjEEA9W5xmSqwToBkrpYa3rGowtg5C54hepEVdA",
                    "content":{
                        "type": "ctx",
                        "name":"DateRFC3339_UnixTime",
                        "version":"1.0",
                        "hash":{
                            "type": "SHA2-256",
                            "value": ""
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
                                    "documentation": "https://github.com/sovrin-foundation/aries-credx-framework-rs/commit/efba6afd119ac53220ed4745265a95fd3344737d",
                                    "implementation": "https://github.com/sovrin-foundation/aries-credx-framework-rs/"
                                },
                                "test_vectors": "https://github.com/sovrin-foundation/aries-credx-framework-rs/commit/a7b1712bd19c27b97a0db37920d98bfb9a3a6722"
                            }
                        }
                    }
                }
            },
            
            "metadata": {
                "reqId":1514280215504647,
                "from":"L5AD5g65TDQr1PPHHRoiGf",
                "endorser": "D6HG5g65TDQr1PPHHRoiGf",
                "digest":"6cee82226c6e276c983f46d03e3b3d10436d90b67bf33dc67ce9901b44dbc97c",
                "payloadDigest": "21f0f5c158ed6ad49ff855baf09a2ef9b4ed1a8015ac24bccc2e0106cd905685"
            },
        },
        "txnMetadata": {
            "txnTime":1513945121,
            "seqNo": 10,  
            "txnId":"7dxgcjqck9gPubLxMpkNniA6v",
        },
        "reqSignature": {
            "type": "ED25519",
            "values": [{
                "from": "L5AD5g65TDQr1PPHHRoiGf",
                "value": "5ZTp9g4SP6t73rH2s8zgmtqdXyTuSMWwkLvfV1FD6ddHCpwTY5SAsp8YmLWnTgDnPXfJue3vJBWjy89bSHvyMSdS"
            }]
        }
 		
        "rootHash": "5vasvo2NUAD7Gq8RVxJZg1s9F7cBpuem1VgHKaFP8oBm",
        "auditPath": ["Cdsoz17SVqPodKpe6xmY2ZgJ9UcywFDZTRgWSAYM96iA", "66BCs5tG7qnfK6egnDsvcx2VSNH6z1Mfo9WmhLSExS6b"],
		
    }
}
```

#### GET_ENCODING

Gets an encoding object from the ledger.

- `dest` (base58-encoded string):

    Encoding object DID as base58-encoded string for the 32 byte DID
    value. It differs from `identifier` metadata field, where `identifier`
    is the DID of the submitter.

    *Example*: `identifier` is a DID of the read request sender, and `dest`
    is the DID of the encoding object.

*Request Example*:
```
{
    "operation": {
        "type": "304"
        "dest": "BmfFKwjEEA9W5xmSqwToBkrpYa3rGowtg5C54hepEVdA",
    },
    
    "identifier": "L5AD5g65TDQr1PPHHRoiGf",
    "reqId": 1514308188474704,
    "protocolVersion": 2
}
```
*Reply Example*:
```
{
    "op": "REPLY", 
    "result": {
        "type": "304",
        "identifier": "L5AD5g65TDQr1PPHHRoiGf",
        "reqId": 1514308188474704,
        
        "seqNo": 10,
        "txnTime": 1514214795,

        "state_proof": {
            "root_hash": "81bGgr7FDSsf4ymdqaWzfnN86TETmkUKH4dj4AqnokrH",
            "proof_nodes": "+QHl+FGAgICg0he/hjc9t/tPFzmCrb2T+nHnN0cRwqPKqZEc3pw2iCaAoAsA80p3oFwfl4dDaKkNI8z8weRsSaS9Y8n3HoardRzxgICAgICAgICAgID4naAgwxDOAEoIq+wUHr5h9jjSAIPDjS7SEG1NvWJbToxVQbh6+Hi4dnsiaWRlbnRpZmllciI6Ikw1QUQ1ZzY1VERRcjFQUEhIUm9pR2YiLCJyb2xlIjpudWxsLCJzZXFObyI6MTAsInR4blRpbWUiOjE1MTQyMTQ3OTUsInZlcmtleSI6In42dWV3Um03MmRXN1pUWFdObUFkUjFtIn348YCAgKDKj6ZIi+Ob9HXBy/CULIerYmmnnK2A6hN1u4ofU2eihKBna5MOCHiaObMfghjsZ8KBSbC6EpTFruD02fuGKlF1q4CAgICgBk8Cpc14mIr78WguSeT7+/rLT8qykKxzI4IO5ZMQwSmAoLsEwI+BkQFBiPsN8F610IjAg3+MVMbBjzugJKDo4NhYoFJ0ln1wq3FTWO0iw1zoUcO3FPjSh5ytvf1jvSxxcmJxoF0Hy14HfsVll8qa9aQ8T740lPFLR431oSefGorqgM5ioK1TJOr6JuvtBNByVMRv+rjhklCp6nkleiyLIq8vZYRcgIA=", 
            "multi_signature": {
                "value": {
                    "timestamp": 1514308168,
                    "ledger_id": 1, 
                    "txn_root_hash": "4Y2DpBPSsgwd5CVE8Z2zZZKS4M6n9AbisT3jYvCYyC2y",
                    "pool_state_root_hash": "9fzzkqU25JbgxycNYwUqKmM3LT8KsvUFkSSowD4pHpoK",
                    "state_root_hash": "81bGgr7FDSsf4ymdqaWzfnN86TETmkUKH4dj4AqnokrH"
                },
                "signature": "REbtR8NvQy3dDRZLoTtzjHNx9ar65ttzk4jMqikwQiL1sPcHK4JAqrqVmhRLtw6Ed3iKuP4v8tgjA2BEvoyLTX6vB6vN4CqtFLqJaPJqMNZvr9tA5Lm6ZHBeEsH1QQLBYnWSAtXt658PotLUEp38sNxRh21t1zavbYcyV8AmxuVTg3",
                "participants": ["Delta", "Gamma", "Alpha"]
            }
        },
        
        "data":{
            "id": "BmfFKwjEEA9W5xmSqwToBkrpYa3rGowtg5C54hepEVdA",
            "content":{
                "type": "ctx",
                "name":"DateRFC3339_UnixTime",
                "version":"1.0",
                "hash":{
                    "type": "SHA2-256",
                    "value": ""
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
                            "documentation": "https://github.com/sovrin-foundation/aries-credx-framework-rs/commit/efba6afd119ac53220ed4745265a95fd3344737d",
                            "implementation": "https://github.com/sovrin-foundation/aries-credx-framework-rs/"
                        },
                        "test_vectors": "https://github.com/sovrin-foundation/aries-credx-framework-rs/commit/a7b1712bd19c27b97a0db37920d98bfb9a3a6722"
                    }
                }
            }
        },
        
        "dest": "BmfFKwjEEA9W5xmSqwToBkrpYa3rGowtg5C54hepEVdA"
    }
}
```

### Indy Data Manager API
Indy Data Manager methods for adding and retrieving encoding objects from
the ledger comply with the interface described
[in aries-vdri](TBD).
This means we define two external-facing methods:
- `indy_read_encoding`
- `indy_write_encoding`

#### write_encoding
```
Writes an encoding object to the ledger.

#Params
submitter: {
    key: public key of the submitter,
    keystore: key manager where private key is stored
}, 
data: {
    id: identifier for the encoding object,
    encoding: encoding object,
    name: encoding name string,
    version: encoding version string,
    ver: version of the encoding object JSON format
},
registry: identifier for the registry

#Returns
registry_response: result as json,
error: {
    code: aries common error code,
    description:  aries common error description
}
```
#### read_encoding
```
Reads an encoding object from the ledger.

#Params
submitter (optional): {
    key: public key of the submitter,
    keystore: key manager where private key is stored
}, 
id: identifier for the encoding object,
registry: identifier for the registry

#Returns
registry_response: encoding object,
error: {
    code: aries common error code,
    description:  aries common error description
}
```
These external methods will use internal methods which follow the common
pattern for methods in Indy-SDK that interact with the ledger. There is a
single method call to build a request to add a transaction to the ledger,
another to build a request to retrieve a transaction from the ledger, and a
third to parse the response from the ledger after submitting a request to
retrieve a transaction. 

The three internal methods we propose adding:
- `indy_build_set_encoding_request`
- `indy_build_get_encoding_request`
- `indy_parse_get_encoding_response`


#### indy_build_set_encoding_request
```
Builds a SET_ENCODING request. Request to add an encoding object to the
ledger.

#Params
command_handle: command handle to map callback to execution environment.
submitter_did: DID of the submitter stored in secured Wallet.
data: Encoding.
{
    id: identifier the encoding,
    encoding: proposed encoding object's value as JSON,
    name: proposed encoding's name string
    version: proposed encoding's version string,
    ver: the version of the generic ledger encoding object template
}
cb: Callback that takes command result as parameter.

#Returns
Request result as json.

#Errors
Common*
```
#### indy_build_get_encoding_request
```
Builds a GET_ENCODING request. Request to get an encoding object from the
ledger.

#Params
command_handle: command handle to map callback to execution environment.
submitter_did: (Optional) DID of the read request sender (if not provided
then default Libindy DID will be used).
id: encoding object ID in ledger
cb: Callback that takes command result as parameter.

#Returns
Request result as json.

#Errors
Common*
```
#### indy_parse_get_encoding_response
```
Parse a GET_ENCODING response to get the encoding object json.

#Params
command_handle: command handle to map callback to execution environment.
get_encoding_response: response of GET_ENCODING request.
cb: Callback that takes command result as parameter.

#Returns
Encoding object id and value as JSON.
{
    id: identifier of encoding object
    encoding: returned encoding object as JSON
    name: returned encoding object's name string
    version: returned encoding object's version string
    ver: the version of the generic ledger encoding object template
}

#Errors
Common*
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

