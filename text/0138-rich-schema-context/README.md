# 0138: Contexts for Rich Schema Objects
- Name: rich-schema-contexts
- Author: Ken Ebert ken@sovrin.org, Brent Zundel brent.zundel@evernym.com
- Start Date: 2019-06-07T13:51:17-06:00

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: 2019-06-18
- Status Note: just proposed; community hasn't studied yet 

## Summary
[summary]: #summary

Every rich schema object has an associated `@context`. Contexts are JSON
objects. They are the standard mechanism for defining shared semantic
meaning among rich schema objects.

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

### Stored on ledger
`@context` will be written to the ledger in much the same way that schemas
and credential definitions are written to the ledger now.

### Example context
```
"@context": [
    "did:sov:11111111111111111111111;content-id=ctx:UVj5w8DRzcmPVDpUMr4AZhJ",
    "did:sov:11111111111111111111111;content-id=ctx:AZKWUJ3zArXPG36kyTJZZm",
    "did:sov:11111111111111111111111;content-id=ctx:9TDvb9PPgKQUWNQcWAFMo4",
    {
          "dct": "http://purl.org/dc/terms/",
          "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
          "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
          "Driver": "did:sov:11111111111111111111111;content-id=sch:35qJWkTM7znKnicY7dq5Yk",
          "DriverLicense": "did:sov:11111111111111111111111;content-id=sch:Q6kuSqnxE57waPFs2xAs7q",
          "CategoryOfVehicles": "DriverLicense:CategoryOfVehicles"
    }
]
```


### Indy Node context API
Indy Node processes ledger transaction requests via request handlers.
Adding `SET_CONTEXT` and `GET_CONTEXT` ledger transactions will involve
creating both a `write` request handler, and a `read` request handler.

The numerical code for a `SET_CONTEXT` transaction is 200.
The numerical code for a `GET_CONTEXT` transaction is 300.

This will be done following the pattern for `schema_handler.py` and
`get_schema_handler.py`

#### SET_CONTEXT
Adds a context to the ledger.

It's not possible to update existing context.
If the context needs to be changed, a new context with a new version or
name needs to be created.

- `data` (dict):

     Dictionary with context's data:

    - `name`: context's name string
    - `version`: context's version string
    - `context_array`: array of context values. Values may be context
    identifiers or dictionaries.

*Request Example*:
```
{
    "operation": {
        "type": "200",
        "data": {
            "name": "ISO18013_DriverLicenseContext",
            "version": "1.0",
            "context_array": [
                "did:sov:11111111111111111111111;content-id=ctx:UVj5w8DRzcmPVDpUMr4AZhJ",
                "did:sov:11111111111111111111111;content-id=ctx:AZKWUJ3zArXPG36kyTJZZm",
                "did:sov:11111111111111111111111;content-id=ctx:9TDvb9PPgKQUWNQcWAFMo4",
                {
                      "dct": "http://purl.org/dc/terms/",
                      "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                      "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                      "Driver": "did:sov:11111111111111111111111;content-id=sch:35qJWkTM7znKnicY7dq5Yk",
                      "DriverLicense": "did:sov:11111111111111111111111;content-id=sch:Q6kuSqnxE57waPFs2xAs7q",
                      "CategoryOfVehicles": "DriverLicense:CategoryOfVehicles"
                }
            ]
        }
    },

    "identifier": "L5AD5g65TDQr1PPHHRoiGf",
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
            "type":"200",
            "protocolVersion":2,

            "data": {
                "ver":1,
                "data": {
                    "name": "ISO18013_DriverLicenseContext",
                    "version": "1.0",
                    "context_array": [
                        "did:sov:11111111111111111111111;content-id=ctx:basetypes:v1",
                        "did:sov:11111111111111111111111;content-id=ctx:JjmmTqGfgvCBnnPJRas6f8x",
                        "did:sov:11111111111111111111111;content-id=ctx:3FtTB4kzSyApkyJ6hEEtxNH",
                        {
                            "dct": "http://purl.org/dc/terms/",
                            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                            "Driver": "did:sov:11111111111111111111111;content-id=sch:35qJWkTM7znKnicY7dq5Yk",
                            "DriverLicense": "did:sov:11111111111111111111111;content-id=sch:Q6kuSqnxE57waPFs2xAs7q",
                            "CategoryOfVehicles": "DriverLicense:CategoryOfVehicles"
                        }
                    ]
                }
            },
            "metadata": {
                "reqId":1514280215504647,
                "from":"L5AD5g65TDQr1PPHHRoiGf",
                "digest":"6cee82226c6e276c983f46d03e3b3d10436d90b67bf33dc67ce9901b44dbc97c",
                "payloadDigest": "21f0f5c158ed6ad49ff855baf09a2ef9b4ed1a8015ac24bccc2e0106cd905685"
            },
        },
        "txnMetadata": {
            "txnTime":1513945121,
            "seqNo": 10,
            "txnId": "A4AThL3TJn5TxfW3gZW5q1",
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

#### GET_CONTEXT

Gets a context from the ledger.

- `dest` (base58-encoded string):

    Context identifier as base58-encoded string, the transaction id from
    the SET_CONTEXT request.
    It differs from the `identifier` metadata field. `identifier` is the
    DID of the submitter of this GET_CONTEXT request.


*Request Example*:
```
{
    "operation": {
        "type": "300"
        "dest": "A4AThL3TJn5TxfW3gZW5q1",
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
        "type": "300",
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

        "data": {
            "name": "ISO18013_DriverLicenseContext",
            "version": "1.0",
            "context_array": [
                "did:sov:11111111111111111111111;content-id=ctx:basetypes:v1",
                "did:sov:11111111111111111111111;content-id=ctx:JjmmTqGfgvCBnnPJRas6f8x",
                "did:sov:11111111111111111111111;content-id=ctx:3FtTB4kzSyApkyJ6hEEtxNH",
                {
                    "dct": "http://purl.org/dc/terms/",
                    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                    "Driver": "did:sov:11111111111111111111111;content-id=sch:35qJWkTM7znKnicY7dq5Yk",
                    "DriverLicense": "did:sov:11111111111111111111111;content-id=sch:Q6kuSqnxE57waPFs2xAs7q",
                    "CategoryOfVehicles": "DriverLicense:CategoryOfVehicles"
                }
            ]
        },
        "submitter": "2VkbBskPNNyWrLrZq7DBhk",
        "dest": "A4AThL3TJn5TxfW3gZW5q1"
    }
}
```

### Indy SDK context API
Indy-SDK methods for adding and retrieving `@context` from the ledger
follow the common pattern for methods that interact with the ledger.
There is a single method call to build a request to add a transaction to
the ledger, another to build a request to retrieve a transaction from the
ledger, and a third to parse the response from the ledger after submitting
a request to retrieve a transaction.

The three methods we propose adding to the Indy-SDK ledger API:
- `indy_build_set_context_request`
- `indy_build_get_context_request`
- `indy_parse_get_context_response`

To describe the methods and parameters, we use the same style of inline
documentation as found in the current Indy-SDK API.

#### indy_build_set_context_request
```
/// Builds a SET_CONTEXT request. Request to add a context.
///
/// #Params
/// command_handle: command handle to map callback to execution environment.
/// submitter_did: DID of the submitter stored in secured Wallet.
/// data: Context.
/// {
///     id: identifier the context
///     context: array of context values
///     name: Context's name string
///     version: Context's version string,
///     ver: Version of the Context json
/// }
/// cb: Callback that takes command result as parameter.
///
/// #Returns
/// Request result as json.
///
/// #Errors
/// Common*
```
#### indy_build_get_context_request
```
/// Builds a GET_CONTEXT request. Request to get a context.
///
/// #Params
/// command_handle: command handle to map callback to execution environment.
/// submitter_did: (Optional) DID of the read request sender (if not provided then default Libindy DID will be used).
/// id: context ID in ledger
/// cb: Callback that takes command result as parameter.
///
/// #Returns
/// Request result as json.
///
/// #Errors
/// Common*
```
#### indy_parse_get_context_response
```
/// Parse a GET_CONTEXT response to get context json.
///
/// #Params
/// command_handle: command handle to map callback to execution environment.
/// get_context_response: response of GET_CONTEXT request.
/// cb: Callback that takes command result as parameter.
///
/// #Returns
/// Context id and context json.
/// {
///     id: identifier of context
///     context: array of context values
///     name: context's name string
///     version: context's version string
///     ver: Version of the context json
/// }
///
/// #Errors
/// Common*
```

## Reference
[reference]: #reference

More information on the Verifiable Credential data model use of `@context`
may be found [here](https://w3c.github.io/vc-data-model/#contexts)

More information on `@context` from the JSON-LD specification may be found
[here](https://w3c.github.io/json-ld-syntax/#the-context) and
[here](https://w3c.github.io/json-ld-syntax/#advanced-context-usage).

## Drawbacks
[drawbacks]: #drawbacks
Requiring a `@context` for each rich schema object introduces more
complexity.

Implementing an Indy-Node ledger transaction for `@context` and
accompanying Indy-SDK methods for submitting and retrieving `@context`
transactions in a way that follows the existing methodology may increase
the existing technical debt that is found in those libraries.

## Rationale and alternatives
[alternatives]: #alternatives

Though requiring a `@context` for each rich schema object increases the
complexity of the system, it also provides a means for better managing the
complexity already present.

## Unresolved questions and future work
[unresolved]: #unresolved-questions

- Should the GUID portion of the DID which identifies a `@context` be taken
from the DID of the transaction submitter, or should there be established
a common DID to be associated with all immutable content such as `@context`?

- Discovery of `@context` objects on the ledger is not considered part of
this initial phase of work.

- Adding `@context` functionality to the Indy-SDK language wrappers is not
considered part of this initial phase of work.
