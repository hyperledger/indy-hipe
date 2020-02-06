# 0120: Rich Schema Objects Common
- Author: Alexander Shcherbakov alexander.shcherbakov@evernym.com
- Start Date: 2020-02-05

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: 2020-02-05
- Status Note: 

## Summary

A low-level description of the components of an anonymous credential ecosystem that supports rich schemas,
W3C Verifiable Credentials and Presentations, and correspondingly rich presentation requests. 

Please see [0119: Rich Schema Objects](https://github.com/hyperledger/indy-hipe/tree/master/text/0119-rich-schemas) 
for high-level description.

This HIPE provides more low-level description of Rich Schema objects defining how they are identified and referenced.
It also defines a general template and common part for all Rich Schema objects. 

## Motivation

Please see [0119: Rich Schema Objects](https://github.com/hyperledger/indy-hipe/tree/master/text/0119-rich-schemas)
for use cases and high-level description of why Rich Schemas are needed.

This HIPE serves as a low-level design of common parts between all Rich Schema objects, and can help developers to 
properly implement Rich Schema transactions on the Ledger and the corresponding client API. 

## Tutorial: General Principles

By Rich Schema objects we mean all objects related to Rich Schema concept
(Context, Rich Schema, Encoding, Mapping, Credential Definition, Presentation Definition)

Let's discuss a number of items common for all Rich Schema objects

### Immutability of Rich Schema Objects

The following Rich Schema objects are immutable:
- Context
- Rich Schema
- Encoding
- Mapping

The following Rich Schema objects can be mutable:
- Credential Definition
- Presentation Definition

Credential Definition is considered as a mutable object as the Issuer may rotate
keys present there.
However, rotation of Issuer's keys should be done carefully as it will invalidate all
credentials issued for this key.

Presentation Definition is considered as a mutable object since restrictions to Issuers, Schemas and 
Credential Definitions to be used in proof may evolve. 
For example, Issuer's key for a given Credential Definition may be compromised, so 
Presentation Definition can be updated to exclude this Credential Definition from the list
of recommended ones. 

### Identification of Rich Schema Objects

- Every Rich Schema object is identified by a DID.
- The id-string of the DID is the base58 representation of the SHA2-256 hash of the canonical form
 of the `content` field (see [Common template for all Rich Schema objects on the Ledger](#Common_template_for_all_Rich_Schema_objects_on_the_Ledger)).
 The canonicalization scheme we recommend is the IETF draft 
 [JSON Canonicalization Scheme (JCS).](https://tools.ietf.org/id/draft-rundgren-json-canonicalization-scheme-16.html) 
- There can be additional metadata (aliases) that can identify Rich Schema objects on the ledger 
in a more user-friendly way.
For Indy the following pair must uniquely identify any Rich Schema object:
   - name (set explicitly)
   - version (set explicitly)
   - type (set implicitly as transaction type)
- Issuer's or Endorser's DID is not part of metadata, which means that Rich Schema objects of a given type
must be unique among all Issuers and Endorsers.      

The suggested Identification scheme allows to have a unique Identifier for any Rich Schema object. 
DID's method name (for example `did:sov`) allows to identify Rich Schema objects with equal content within different 
data registries (ledgers).   

### Referencing Rich Schema Objects
- Any Rich Schema object is referenced by other Rich Schema objects by its DID.
- A Rich Schema object may reference a Rich Schema object from another ledger (as defined by DID's method name).

### Relationship
- A credential definition refers to a single mapping object
- A mapping object refers to 1 or more schema objects.
Each attribute in a schema may be included in the mapping one or more times (it is possible to encode a single attribute 
in multiple ways). A mapping may map only a subset of the attributes of a schema.
- A presentation definition refers to 1 or more schema and credential definition objects. A presentation definition may use only a
subset of the attributes of a schema.  

### How Rich Schema objects are stored on the Ledger

Any write request for Rich Schema object has the same fields:
```
'id': <Rich Schema object's ID>                # DID string 
'content': <Rich Schema object as JSON-LD>     # JSON-serialized string
'metadata': {
    'name': <name>                             # string
    'version': <version>                       # string
}
'ver': <format version>                        # integer                              
```
- `id` is a DID with a id-string being base58 representation of the SHA2-256 hash of the `content` field
- The `content` field here contains a Rich Schema object in JSON-LD format (see [0119: Rich Schema Objects](https://github.com/hyperledger/indy-hipe/tree/master/text/0119-rich-schemas)).
It's passed and stored as-is.
The `content` field must be serialized in the canonical form. The canonicalization scheme we recommend is the IETF draft 
 [JSON Canonicalization Scheme (JCS).](https://tools.ietf.org/id/draft-rundgren-json-canonicalization-scheme-16.html)
- `metadata` contains additional fields which can be used for human-readable identification    
- `ver` defines the version of the format. It defines what fields and metadata are there, how `id` is generated, what hash function is used there, etc. 
- Author's and Endorser's DIDs are also passed as a common metadata fields for any Request. 

### Querying Rich Schema objects from the Ledger
- Any Rich Schema object can be get from the Ledger by its DID
- It should be possible to get Rich Schema objects by metadata as well: `(name, version, transaction type)`.
- Currently it's supposed that every Rich Schema object is queried individually, so it's up to clients and applications
to get, query and cache all dependent Rich Schema objects.

The following information is returned from the Ledger in a reply for any get request of a Rich Schema object:
```
'id': <Rich Schema object's ID>              # DID string 
'content': <Rich Schema object as JSON-LD>   # JSON-serialized string
'metadata': {
    'name': <name>                           # string
    'version': <version>                     # string
}
'ver': <format version>                      # integer
'from': <author DID>,                        # DID string
'endorser': <endorser DID>,                  # DID string
```

Common fields such as state proof are also returned as for any reply for a get request. 

### Common validation for all Rich Schema objects on the Ledger
- Check that ID DID's id-string is the base58 representation of the SHA2-256 hash of the `content` field.
- If the object is supposed to be immutable: 
  - Make sure that no object with the given ID exist on the ledger
  - Make sure that no object with the `(name, version, transaction type)` exist on the ledger
- There can be additional validation logic depending on the Rich Schema object type such as checking that referenced objects are present on the ledger.
This validation can be tricky in case of objects belonging to other ledgers. 



### Indy Data Manager internal API

We can have a unified API to write and read Rich Schema objects from the Ledger.
Just three internal methods are sufficient to handle all Rich Schema types:

- `indy_build_rich_schema_object_request`
- `indy_build_get_rich_schema_object_request`
- `indy_parse_get_rich_schema_object_response`

## Tutorial: Common data structure 

### Indy Data Manager internal API 

##### indy_build_rich_schema_object_request
```
Builds a request to store a Rich Schema Object of the given type. 

#Params
command_handle: command handle to map callback to execution environment.
submitter_did: Identifier (DID) of the transaction author as base58-encoded string.
               Actual request sender may differ if Endorser is used (look at `indy_append_request_endorser`)
type: Rich Schema object's type enum
id: Rich Schema object's ID as a DID,
content: Rich Schema object as JSON-LD string,
metadata: Rich Schema object's metadata such as name and version as JSON
ver: the version of the generic object template
}
cb: Callback that takes command result as parameter.

#Returns
Request result as json.

#Errors
Common*
```

##### indy_build_get_schema_object_by_id_request
```
Builds a request to get a Rich Schema Object of the given type. 

#Params
command_handle: command handle to map callback to execution environment.
submitter_did: (Optional) DID of the read request sender (if not provided then default Libindy DID will be used).
type: Rich Schema object's type enum
id: Rich Schema object's ID as a DID,
}
cb: Callback that takes command result as parameter.

#Returns
Request result as json.

#Errors
Common*
```

##### indy_build_get_schema_object_by_metadata_request
```
Builds a request to get a Rich Schema Object of the given type. 

#Params
command_handle: command handle to map callback to execution environment.
submitter_did: (Optional) DID of the read request sender (if not provided then default Libindy DID will be used).
type: Rich Schema object's type enum
name: Rich Schema object's name,
version: Rich Schema object's version,
}
cb: Callback that takes command result as parameter.

#Returns
Request result as json.

#Errors
Common*
```

### Common template for all write requests for Rich Schema objects 
Every write request for Rich Schema objects follows the 
[Common write request structure](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#common-write-request-structure)
 and has the following form:
```
{
    'operation': {
        'type': <request type>,
        'ver': <operation version' # integer
                 
        'id': <Rich Schema object's ID>                # DID string 
        'content': <Rich Schema object as JSON-LD>   # JSON-serialized string
        'metadata': {
            'name': <name>        # string
            'version': <version>  # string
         }
    },
    
     # Common fields:
    'identifier': <author DID>,
    'endorser': <endorser DID>, 
    'reqId': <req_id unique integer>,
    'protocolVersion': <protocol version>,
    'signature': <signature_value>,
    'taaAcceptance': <taa acceptance fields>
}
```

### Common template for all read requests for Rich Schema objects 
Every read request for Rich Schema objects follows the 
[Common read request structure](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#common-request-structure)
 and has the following form:
```
{
    'operation': {
        'type': <request type>,
        
        'id': <Rich Schema object's ID>  # DID string 
        'name': <name>                 # string, mutually exclusive with `id`, must be set together with the `version`
        'version': <version>           # string, mutually exclusive with `id`, must be set together with the `name`
    },
    
     # Common fields:
    'identifier': <any DID>,
    'reqId': <req_id unique integer>,
    'protocolVersion': <protocol version>,
}
```
Either `id` or both `name` and `version` must be specified to get a Rich Schema objects. It means that a Rich Schema object
can be get either by its unique ID (DID), or metadata (name, version).

### Common template for all Rich Schema objects transactions on the Ledger 
Every Rich Schema object transaction follows the 
[Common transaction structure](https://github.com/hyperledger/indy-node/blob/master/docs/source/transactions.md#common-structure)
 and has the following form:
```
    'ver': <txn version>,
    'txn': {
        'type': <Rich Schema object type as in Request>,
        'protocolVersion': <protocol version>,

        'data': {
            'ver': <Rich Schema object format version>,
            'id': <Rich Schema object's ID>                # DID string 
            'content': <Rich Schema object as JSON-LD>   # JSON-serialized string
            'metadata': {
                'name': <name>        # string
                'version': <version>  # string
             }
        },

        'metadata': {
            'from': <author DID>,
            'endorser': <endorser DID>, 
            ..... # other metadata
        },
    },
    'txnMetadata': {
        ....
    },
    'reqSignature': {
        ....
    }
```

  
### Common template for any Rich Schema object representation in State
Any Rich Schema object is stored in a Patricia Merkle Trie State as key-value pairs.

There are two entries (key-value pairs) associated with every Rich Schema object:
- `id` : `value` 
- `type:name:version` : `id`

where
- `id` is a Rich Schema object ID (DID) as `id` field in request
- `type` is a unique marker for Rich Schema object type
- `name` and `version` are Rich Schema object name and versions metadata fields (as `name` and `version` fields in request)
- `value` has the following form:
    ```
        {
            'id': <Rich Schema object ID>                # DID string 
            'content': <Rich Schema object as JSON-LD>   # JSON-serialized string
            'name': <name>               # string
            'version': <version>         # string
            'from': <author DID>,        # DID string
            'endorser': <endorser DID>,  # DID string
        }
    ```
### Common template for Reply to Rich Schema object requests

Reply to write requests for Rich Schema objects follows the 
[Common reply structure for write requests](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#reply-structure-for-write-requests)

Reply to read requests for Rich Schema objects follows the 
[Common reply structure for read requests](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#reply-structure-for-read-requests)
and has the following form:
```
{
    'op': 'REPLY', 
    'result': {
        'data': {
            'id': <Rich Schema object's ID>                # DID string 
            'content': <Rich Schema object as JSON-LD>   # JSON-serialized string
            'name': <name>               # string
            'version': <version>         # string
            'from': <author DID>,        # DID string
            'endorser': <endorser DID>,  # DID string
        }
        'state_proof': <state proof and BLS aggregated signature>
        'seqNo': <seq no in ledger>,
        'txnTime': <txn write time>,
        
        # fields from the read request  
        ....
    }
}
```


### Relationship between Rich Schema Objects
TBD





## Reference
- [0119: Rich Schema Objects](https://github.com/hyperledger/indy-hipe/tree/master/text/0119-rich-schemas) 
- [Common write request structure](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#common-write-request-structure)
- [Common read request structure](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#common-request-structure)
- [Common transaction structure](https://github.com/hyperledger/indy-node/blob/master/docs/source/transactions.md#common-structure)
- [Common reply structure for write requests](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#reply-structure-for-write-requests)
- [Common reply structure for read requests](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#reply-structure-for-read-requests)

## Drawbacks

Rich schema objects introduce more complexity.

Implementing an Indy-Node ledger transaction for schema in a way that follows the existing methodology 
may increase the existing technical debt that is found in those libraries.

## Rationale and alternatives

This design proposes a simplified and unified approach for storing and processing any Rich Schema object on the Ledger.
Another approach could be to not store Rich Schema object as-is as JSON-LD, but define exact format and parse every field. 

The design proposed in this HIPE looks better because
- it simplifies workflow
- it simplifies HIPEs for every Rich Schema object
- it simplifies amount of work to be done on the Ledger side, so that all Rich Schema transactions can be implemented with a minimal amount of code
- it makes processing of transactions on the Ledger side faster (no need for additional serialization-deserialization and validation)
- it doesn't introduce more work on the client side or change the client workflow 

## Unresolved questions
Need to have a diagram for general workflow


