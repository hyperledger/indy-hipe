# Indy HIPE 0140: Rich Schema Schemas
- Authors: [Brent Zundel](<brent.zundel@evernym.com>), [Ken Ebert](<ken@sovrin.org>)
- Start Date: 2019-11-01

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: 2019-11-01
- Status Note: just proposed



## Summary
[summary]: #summary

The proposed schemas are [JSON-LD objects](https://json-ld.org/). This
allows credentials issued according to the proposed schemas to have a clear
semantic meaning, so that the verifier can know what the issuer intended.
They support explicitly typed properties and semantic inheritance. A schema
may include other schemas as property types, or extend another schema with
additional properties. For example a schema for "employee" may inherit from
the schema for "person."

## Motivation
[motivation]: #motivation

Many organizations, such as HL7 who publish the FHIR standard for heath
care data exchange, have invested time and effort into creating data
schemas that are already in use. Many schemas are shared publicly via web
sites such as https://schema.org/, whose mission is, "to create, maintain,
and promote schemas for structured data on the Internet, on web pages, in
email messages, and beyond."

These schemas ought to be usable as the basis for verifiable credentials.

Although verifiable credentials are the primary use case for schemas
considered in this document, other future uses may include defining message
formats or objects in a verifiable data registry.  

### Interoperability

Existing applications make use of schemas to organize and semantically
describe data. Using those same schemas within anonymous credentials
provides a means of connecting existing applications with this emerging
technology. This allows for an easy migration path for those applications
to incorporate anonymous credentials.

Using schemas which may be shared among verifiable credential ecosystems
allows for semantic interoperability between them, and enables a path
toward true multi-lateral credential exchange.

Using existing schemas, created in accordance with widely-supported common
standards, allows anonymous credentials to benefit from the decades of
effort and thought that went into those standards and to work with other
applications which also adhere to those standards.

### Re-use
Rich schemas can be re-used within Indy. Because these schemas are
hierarchical and composable, even unrelated schemas may share partial
semantic meaning due to the commonality of sub-schemas within both. For
example, a driver license schema and an employee record are not related
schemas, but both may include a person schema.

A schema that was created for a particular use-case and accepted within a
trust framework may be re-used within other trust frameworks for their
use-cases. The visibility of these schemas across trust boundaries
increases the ability of these schemas to be examined in greater detail and
evaluated for fitness of purpose. Over time the schemas will gain
reputation. 

### Extensibility
Applications can use these schemas as a basis for complex data objects for
use within the application, or exposed through external APIs.

### Immutability
One important aspect of relying on schemas to provide the semantic meaning
of data within a verifiable credential, is that the meaning of the
credential properties should not change. It is not enough for entities
within the ecosystem to have a shared understanding of the data in the
present, it may be necessary for them to have an understanding of the
credential at the time it was issued and signed. This depends on the trust
framework within which the credential was issued and the needs of the
parties involved. The Indy ledger can provide immutable storage of schemas.

## Tutorial
[tutorial]: #tutorial

### Intro to schemas
`schema` objects are used to enforce structure and semantic meaning on a
set of data. They allow Issuers to assert, and Holders and Verifiers to
understand, a particular semantic meaning for the properties in a
credential.

Rich schemas are JSON-LD objects. Examples of the type of schemas supported
here may be found at https://schema.org/docs/schemas.html. At this time we
do not support other schema representations such as RDFS, JSON Schema, XML
Schema, OWL, etc.

### Properties

#### @id
A rich schema must have an `@id` property. The value of this property must
be (or map to, via a context object) a URI. It is expected that rich
schemas stored in a verifiable data registry will be assigned a DID or
other identifier for identification within and resolution by that registry. 

A [rich schema](README.md) may refer to the `@id` of another rich schema to
define a parent schema. A property of a rich schema may use the `@id` of
another rich schema as the value of its `@type` or `@id` property.

A [mapping object](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0250-rich-schemas/README.md#mappings)
will contain the `@id` of the rich schema being mapped.

A [presentation definition](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0250-rich-schemas/README.md#presentation-definitions)
will contain the `@id` of any schemas a holder may use to present proofs to
a verifier.

#### @type
A rich schema must have a `@type` property. The value of this property must
be (or map to, via a context object) a URI. 

#### @context
A rich schema may have a `@context` property. If present, the value of this
property must be a
[context object](../0138-rich-schema-context/README.md) or a URI which can
be dereferenced to obtain a context object.

### Use in Verifiable Credentials
These schemas will be used in conjunction with the JSON-LD representation
of the verifiable credentials data model to specify which properties may be
included as part of the verifiable credential's `credentialSubject`
property, as well as the types of the property values.

The `@id` of a rich schema may be used as an additional value of the 
[type property](https://www.w3.org/TR/vc-data-model/#types) property of a
verifiable credential. Because the `type` values of a verifiable credential
are not required to be dereferenced, in order for the rich schema to
support assertion of the structure and semantic meaning of the claims in
the credential, an additional reference to the rich schema should be made
through the 
[credentialSchema](https://www.w3.org/TR/vc-data-model/#data-schemas)
property. This may be done as a direct reference to the rich schema `@id`,
or via another rich schema object which references the rich schema `@id`
such as a 
[credential definition](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0250-rich-schemas/README.md#credential-definitions) 
as would 
[be the case](https://www.w3.org/TR/vc-data-model/#zero-knowledge-proofs) 
for anonymous credentials, as discussed in the
[mapping section](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0250-rich-schemas/README.md#mappings) of
the rich schema overview RFC.

### Example schema
```
"schema": {
   "@context": {
    "schema": "http://schema.org/",
    "bibo": "http://purl.org/ontology/bibo/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dct": "http://purl.org/dc/terms/",
    "dcterms": "http://purl.org/dc/terms/",
    "dctype": "http://purl.org/dc/dcmitype/",
    "eli": "http://data.europa.eu/eli/ontology#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfa": "http://www.w3.org/ns/rdfa#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "schema": "http://schema.org/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "snomed": "http://purl.bioontology.org/ontology/SNOMEDCT/",
    "void": "http://rdfs.org/ns/void#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "xsd1": "hhttp://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "schema:recipeIngredient",
      "@type": "rdf:Property",
      "rdfs:comment": "A single ingredient used in the recipe, e.g. sugar, flour or garlic.",
      "rdfs:label": "recipeIngredient",
      "rdfs:subPropertyOf": {
        "@id": "schema:supply"
      },
      "schema:domainIncludes": {
        "@id": "schema:Recipe"
      },
      "schema:rangeIncludes": {
        "@id": "schema:Text"
      }
    },
    {
      "@id": "schema:ingredients",
      "schema:supersededBy": {
        "@id": "schema:recipeIngredient"
      }
    }
  ]
 }
```
recipeIngredient schema from 
[schema.org](https://schema.org/recipeIngredient.jsonld).

### Indy and Aries
The complete architecture for `schema` objects involves three separate
repositories:
- `indy-node`: The code run by a validator node participating in an
instance of the indy ledger, e.g., the validators node in the Sovrin
network run `indy-node`. Changes to this code will enable `schema`
objects to be written to and retrieved from an instance of indy.
- `indy-data-manager`: code which a client may use to communicate with
validator nodes in an indy network. Changes to this code will enable
`schema` transaction requests to be sent to validator nodes.
`indy-data-manager` complies with the interface described by the
`aries-verifiable-data-registry-interface` and is built to plug in to the
aries ecosystem.
- `aries-vdri`: This is the location of the
`aries-verifiable-data-registy-interface`. Changes to this code will enable
users of any data registry with an `aries-dri`-compatible data manager to
handle `schema` objects.

Only changes to the indy repositories are described here. For a description
of the changes to aries, please see
[this rfc](https://github.com/hyperledger/aries-rfcs/pull/281).


### Indy Node schema API
Indy Node processes ledger transaction requests via request handlers.
Adding `SET_RICH_SCHEMA` and `GET_RICH_SCHEMA` ledger transactions will involve
creating both a `write` request handler, and a `read` request handler.

The numerical code for a `SET_RICH_SCHEMA` transaction is 201.
The numerical code for a `GET_RICH_SCHEMA` transaction is 301.

This will be done following the pattern for `context_handler.py` and
`get_context_handler.py`

#### SET_RICH_SCHEMA
Adds a schema to the ledger.

It's not possible to update existing schema. So, if the schema needs to 
be evolved, a new schema with a new version or name needs to be created.

- `data` (object):

  Object with schema's data:

  - `schema`: This value must be a schema object

- `meta` (dict)

  Dictionary with schema's metadata

  - `name`: schema's name string
  - `version`: schema's version string
  - `type`: "sch"


*Request Example*:
```
{
    "operation": {
        "type": "201",
        "data":{
            "schema": {          
                "@context": {
                    "schema": "http://schema.org/",
                    "bibo": "http://purl.org/ontology/bibo/",
                    "dc": "http://purl.org/dc/elements/1.1/",
                    "dcat": "http://www.w3.org/ns/dcat#",
                    "dct": "http://purl.org/dc/terms/",
                    "dcterms": "http://purl.org/dc/terms/",
                    "dctype": "http://purl.org/dc/dcmitype/",
                    "eli": "http://data.europa.eu/eli/ontology#",
                    "foaf": "http://xmlns.com/foaf/0.1/",
                    "owl": "http://www.w3.org/2002/07/owl#",
                    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                    "rdfa": "http://www.w3.org/ns/rdfa#",
                    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                    "schema": "http://schema.org/",
                    "skos": "http://www.w3.org/2004/02/skos/core#",
                    "snomed": "http://purl.bioontology.org/ontology/SNOMEDCT/",
                    "void": "http://rdfs.org/ns/void#",
                    "xsd": "http://www.w3.org/2001/XMLSchema#",
                    "xsd1": "hhttp://www.w3.org/2001/XMLSchema#"
                },
                "@graph": [
                    {
                        "@id": "schema:recipeIngredient",
                        "@type": "rdf:Property",
                        "rdfs:comment": "A single ingredient used in the recipe, e.g. sugar, flour or garlic.",
                        "rdfs:label": "recipeIngredient",
                        "rdfs:subPropertyOf": {
                            "@id": "schema:supply"
                        },
                        "schema:domainIncludes": {
                            "@id": "schema:Recipe"
                        },
                        "schema:rangeIncludes": {
                            "@id": "schema:Text"
                        }
                    },
                    {
                        "@id": "schema:ingredients",
                        "schema:supersededBy": {
                            "@id": "schema:recipeIngredient"
                        }
                    }
                ]
            }
        },
        "meta": {
            "name":"recipeIngredient",
            "version":"1.0",
            "type": "sch"
        },
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
            "type":"201",
            "protocolVersion":2,
            
            "data": {
                "ver":1,
                "data":{
                    "schema": {          
                        "@context": {
                            "schema": "http://schema.org/",
                            "bibo": "http://purl.org/ontology/bibo/",
                            "dc": "http://purl.org/dc/elements/1.1/",
                            "dcat": "http://www.w3.org/ns/dcat#",
                            "dct": "http://purl.org/dc/terms/",
                            "dcterms": "http://purl.org/dc/terms/",
                            "dctype": "http://purl.org/dc/dcmitype/",
                            "eli": "http://data.europa.eu/eli/ontology#",
                            "foaf": "http://xmlns.com/foaf/0.1/",
                            "owl": "http://www.w3.org/2002/07/owl#",
                            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                            "rdfa": "http://www.w3.org/ns/rdfa#",
                            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                            "schema": "http://schema.org/",
                            "skos": "http://www.w3.org/2004/02/skos/core#",
                            "snomed": "http://purl.bioontology.org/ontology/SNOMEDCT/",
                            "void": "http://rdfs.org/ns/void#",
                            "xsd": "http://www.w3.org/2001/XMLSchema#",
                            "xsd1": "hhttp://www.w3.org/2001/XMLSchema#"
                        },
                        "@graph": [
                            {
                                "@id": "schema:recipeIngredient",
                                "@type": "rdf:Property",
                                "rdfs:comment": "A single ingredient used in the recipe, e.g. sugar, flour or garlic.",
                                "rdfs:label": "recipeIngredient",
                                "rdfs:subPropertyOf": {
                                    "@id": "schema:supply"
                                },
                                "schema:domainIncludes": {
                                    "@id": "schema:Recipe"
                                },
                                "schema:rangeIncludes": {
                                    "@id": "schema:Text"
                                }
                            },
                            {
                                "@id": "schema:ingredients",
                                "schema:supersededBy": {
                                    "@id": "schema:recipeIngredient"
                                }
                            }
                        ]
                    }
                },
                "meta": {
                    "name":"recipeIngredient",
                    "version":"1.0",
                    "type": "sch"
                },
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
            "txnId":"L5AD5g65TDQr1PPHHRoiGf1|recipeIngredient|1.0",
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

#### GET_RICH_SCHEMA

Gets a schema from the ledger.

- `dest` (base58-encoded string):

    Schema DID as base58-encoded string for 16 or 32 byte DID value. It 
    differs from `identifier` metadata field, where `identifier` is the DID
    of the submitter.

    *Example*: `identifier` is a DID of the read request sender, and `dest`
    is the DID of the schema.

- `meta` (dict):

  - `name` (string): schema's name string
  - `version` (string): schema's version string

*Request Example*:
```
{
    "operation": {
        "type": "301"
        "dest": "2VkbBskPNNyWrLrZq7DBhk",
        "meta": {
            "name": "recipeIngredient",
            "version": "1.0",
            "type": "sch"
        },
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
        "type": "301",
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
            "schema": {          
                "@context": {
                    "schema": "http://schema.org/",
                    "bibo": "http://purl.org/ontology/bibo/",
                    "dc": "http://purl.org/dc/elements/1.1/",
                    "dcat": "http://www.w3.org/ns/dcat#",
                    "dct": "http://purl.org/dc/terms/",
                    "dcterms": "http://purl.org/dc/terms/",
                    "dctype": "http://purl.org/dc/dcmitype/",
                    "eli": "http://data.europa.eu/eli/ontology#",
                    "foaf": "http://xmlns.com/foaf/0.1/",
                    "owl": "http://www.w3.org/2002/07/owl#",
                    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                    "rdfa": "http://www.w3.org/ns/rdfa#",
                    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                    "schema": "http://schema.org/",
                    "skos": "http://www.w3.org/2004/02/skos/core#",
                    "snomed": "http://purl.bioontology.org/ontology/SNOMEDCT/",
                    "void": "http://rdfs.org/ns/void#",
                    "xsd": "http://www.w3.org/2001/XMLSchema#",
                    "xsd1": "hhttp://www.w3.org/2001/XMLSchema#"
                },
                "@graph": [
                    {
                        "@id": "schema:recipeIngredient",
                        "@type": "rdf:Property",
                        "rdfs:comment": "A single ingredient used in the recipe, e.g. sugar, flour or garlic.",
                        "rdfs:label": "recipeIngredient",
                        "rdfs:subPropertyOf": {
                            "@id": "schema:supply"
                        },
                        "schema:domainIncludes": {
                            "@id": "schema:Recipe"
                        },
                        "schema:rangeIncludes": {
                            "@id": "schema:Text"
                        }
                    },
                    {
                        "@id": "schema:ingredients",
                        "schema:supersededBy": {
                            "@id": "schema:recipeIngredient"
                        }
                    }
                ]
            }
        },
        
        "meta": {
            "name":"recipeIngredient",
            "version":"1.0",
            "type": "sch"
        },
        
        "dest": "2VkbBskPNNyWrLrZq7DBhk"
    }
}
```

### Indy Data Manager API
Indy Data Manager methods for adding and retrieving `schema` from the
ledger comply with the interface described
[this rfc](https://github.com/hyperledger/aries-rfcs/pull/281).
This means we define two external-facing methods:
- `indy_read_schema`
- `indy_write_schema`

#### write_schema
```
Writes a schema to the ledger.

#Params
submitter: {
    key: public key of the submitter,
    keystore: key manager where private key is stored
}, 
data: {
    id: identifier for the schema,
    schema: schema object,
    name: schema name string,
    version: schema version string,
    ver: version of the schema JSON format
},
registry: identifier for the registry

#Returns
registry_response: result as json,
error: {
    code: aries common error code,
    description:  aries common error description
}
```
#### read_schema
```
Reads a schema from the ledger.

#Params
submitter (optional): {
    key: public key of the submitter,
    keystore: key manager where private key is stored
}, 
id: identifier for the schema,
registry: identifier for the registry

#Returns
registry_response: schema object,
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
- `indy_build_SET_RICH_SCHEMA_request`
- `indy_build_GET_RICH_SCHEMA_request`
- `indy_parse_GET_RICH_SCHEMA_response`


#### indy_build_SET_RICH_SCHEMA_request
```
Builds a SET_RICH_SCHEMA request. Request to add a schema to the ledger.

#Params
command_handle: command handle to map callback to execution environment.
submitter_did: DID of the submitter stored in secured Wallet.
data: schema.
{
    id: identifier the schema,
    schema: schema object,
    name: schema's name string
    version: schema's version string,
    ver: Version of the schema json
}
cb: Callback that takes command result as parameter.

#Returns
Request result as json.

#Errors
Common*
```
#### indy_build_GET_RICH_SCHEMA_request
```
Builds a GET_RICH_SCHEMA request. Request to get a schema from the ledger.

#Params
command_handle: command handle to map callback to execution environment.
submitter_did: (Optional) DID of the read request sender (if not provided then default Libindy DID will be used).
id: schema ID in ledger
cb: Callback that takes command result as parameter.

#Returns
Request result as json.

#Errors
Common*
```
#### indy_parse_GET_RICH_SCHEMA_response
```
Parse a GET_RICH_SCHEMA response to get schema json.

#Params
command_handle: command handle to map callback to execution environment.
GET_RICH_SCHEMA_response: response of GET_RICH_SCHEMA request.
cb: Callback that takes command result as parameter.

#Returns
schema id and schema json.
{
    id: identifier of schema
    schema: schema object
    name: schema's name string
    version: schema's version string
    ver: Version of the schema json
}

#Errors
Common*
```
### Note about existing Indy Schemas
This HIPE and associated RFC does not add support here or through Aries for
existing Indy schemas (which only contain a simple array of attribute names).

## Reference
[reference]: #reference

More information on the Verifiable Credential data model use of `schemas`
may be found [here](https://w3c.github.io/vc-data-model/#data-schemas)

## Drawbacks
[drawbacks]: #drawbacks
Rich schema objects introduce more complexity.

Implementing an Indy-Node ledger transaction for `schema` in a way that
follows the existing methodology may increase the existing technical debt
that is found in those libraries.

## Unresolved questions and future work
[unresolved]: #unresolved-questions

- Should the GUID portion of the DID which identifies a `schema` be taken
from the DID of the transaction submitter, or should there be established
a common DID to be associated with all immutable content such as `schema`?

- Discovery of `schema` objects on the ledger is not considered part of
this initial phase of work.
