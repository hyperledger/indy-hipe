# Indy HIPE 0160: W3C Compatible Verifiable Credentials
- Authors: Alexander Shcherbakov <alexander.shcherbakov@evernym.com>, Brent Zundel <brent.zundel@evernym.com>, Ken Ebert <ken@sovrin.org> 
- Start Date: 2020-03-19

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: 2019-03-19
- Status Note: just proposed



## Summary
[summary]: #summary

A new JSON-LD  format for anonymous (zero-knowledge proof based) verifiable credentials in Indy 
compatible with W3C Verifiable Credential standard. 
It's developed in the context of rich schema feature. 

Despite being compatible with W3C, Indy credentials have a number of explicit assumptions about the content and cardinality for 
some of W3C verifiable credential properties. 


## Motivation
[motivation]: #motivation

### Standards Compliance
The W3C has published the Verifiable Credentials Data Model 1.0
as an official recommendation. This proposal brings the format of
Indy's anonymous credentials and presentations into compliance with that
standard.

### Interoperability
Compliance with the Verifiable Credentials Data Model 1.0 introduces the possibility of
interoperability with other credentials that also comply with the
standard. The verifiable credential data model specification is limited to
defining the data structure of verifiable credentials and presentations.
This includes defining extension points, such as "proof" or
"credentialStatus."


## Tutorial
[tutorial]: #tutorial

The proposed credential format follows the W3C specification supporting the extension for zero-knowledge proof:
- [Basic Attributes](https://w3c.github.io/vc-data-model/#basic-concepts)
- [Zero-knowledge proof example](https://w3c.github.io/vc-data-model/#zero-knowledge-proofs)

Although in general Indy anonymous credentials follow and are compatible with
the Verifiable Credential Data Model 1.0 specification, there are a number of 
explicit requirements for Indy anonymous credentials (see the next two sections).

### Properties
Any Indy credential compatible with W3C standard MUST have the following properties:

#### @context 
JSON-LD Context. The value MUST be an ordered set where 
 - the first item MUST be a URI with the value `https://www.w3.org/2018/credentials/v1`.
 - other items MAY be `@id` of contexts used by the corresponding rich schema and mapping 
 (see [Rich Schema Context](https://github.com/hyperledger/indy-hipe/tree/master/text/0149-rich-schema-schema#context)).


#### type
A type of the verifiable sredential.
It MUST be an unordered set consisting of the following two values:
- `VerifiableCredential` which is a type common for all W3C verifiable credentials (see `https://www.w3.org/2018/credentials/v1` context).
- `@id` of a rich schema the credential is created against. 

A credential  MUST be created against one and only one rich schema 
(see [Relationship between Rich Schema objects](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#relationship)). 

#### credentialSchema
Specifies the credential definition the credential is created against.
The credential definition and the corresponding mapping
MUST reference the same rich schema as specified in the credential's `type`.

`credentialSchema` has two nested properties:
- `id` equal to the credential definition's ID;
- `type` equal to the credential definition's type; `cdf` is the only value currently supported.

A credential MUST be created against one and only one credential definition 
(see [Relationship between Rich Schema objects](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common#relationship)). 


#### issuer
A DID of the issuer who is the author of the credential definition on the Ledger.

If the credential definition transaction was endorsed to the Ledger by a different party, then 
the `issuer` property must point to the real transaction's author (`identifier` or `from` field), not 
the endorser (`endorser` field). 

As `issuer` is a default field in any [Mapping](https://github.com/hyperledger/indy-hipe/tree/master/text/0155-rich-schema-mapping), 
it must be signed as any other attribute from the `credentialSubject`.

#### issuanceDate
The value of the `issuanceDate` property MUST be a string value of an 
[RFC3339](https://w3c.github.io/vc-data-model/#bib-rfc3339) combined date and time string
representing the date and time the credential becomes valid, which could be a date and time
in the future. 

This is the date after which the claims in the credential 
 are considered valid by the issuer, which may be different from the date the credential was signed
 by the issuer or received by the holder.

As `issuanceDate` is a default field in any [Mapping](https://github.com/hyperledger/indy-hipe/tree/master/text/0155-rich-schema-mapping), 
it must be signed as any other attribute from  the `credentialSubject`.
 
#### credentialSubject
The value contains an unordered list of (nested) claims about each subject of the credential
and the corresponding values. 

The set of claims MUST match the ones defined by the mapping object.
Note: a credential may include claims about multiple subjects, e.g., a birth certificate credential may 
include claims about the child, the mother, and the father.

The value of the claims are 'raw' values according to the claim's type, as defined by the 
corresponding rich schema.

The integer representation of the claim values, as required by the CL (Camenisch-Lysyanskaya)
ZKP signature scheme, are included as attributes in the `proof` property. The transformation from
claim value to integer is defined by the encoding objects from the corresponding mapping. 
 
#### proof
An issuer's ZKP signature that can be used to derive verifiable presentations
that present information contained in the original verifiable credential in zero-knowledge.

The `proof` must contain a ZKP signature for the `issuer` and `issuanceDate` attributes as required by 
the [Mapping](https://github.com/hyperledger/indy-hipe/tree/master/text/0155-rich-schema-mapping). 
`issuer` and `issuanceDate` attributes are signed together with the other attributes from the schema in a common way.
 
The `proof` MUST contain a `type` property which indicates the ZKP signature scheme used. 
Currently the `type` MUST be equal to either `CL` or `CL2` for Camenisch-Lysyanskaya (Anoncreds 1.0) or
Camenisch-Lysyanskaya 2.0 (Anoncreds 2.0), correspondingly.  

The value of this `type` property MUST have the same value as the `signatureType` property of the
credential definition specified by `credentialSchema` .  
 
Other properties in the `proof` are type-specific and used by the crypto layer only.
End users should not have any assumptions sbout the fields and should not try to parse them.   
 
### Rules and Assumptions
A summary of explicit assumptions for W3C compatible verifiable credentials in Indy: 

- Indy supports zero-knowledge-based credentials only (anoncreds).
 The only supported zero-knowledge signature type for now is Camenisch-Lysyanskaya signature
  (either version 1.0 or 2.0).

- Any credential must be issued against one and only one rich schema.
If there is no existent single schema that may be used for the issuance of a credential,
a new schema must be created, potentially referencing or extending existing ones.

- The `id` of the credential's rich schema must be specified in the `type` property in addition to the common `VerifiableCredential`.

- Any credential must be issued against one and only one credential definition, which, in turn,
must reference only one mapping and rich schema.
The corresponding mapping must reference only one rich schema.
The same rich schema must be referenced by the credential, and its corresponding credential
definition and mapping.  
   

- The `id` of the credential's credential definition must be specified in the `credentialSchema`'s `id` property.

- Indy credentials use DIDs for identification and referencing. 
In particular, the following values are expected to be DIDs:
  - Rich schema's contexts (part of `@context` property)
  - Rich schema's `id` (part of `type`)
  - Credential definition's `id` (`credentialSchema`'s `id` property)
  - Issuer (`issuer` property)

- If the `id` of a credential or a rich schema object is defined as a DID, then the corresponding
DID's id-string should be the base58 representation of the SHA2-256 hash of the canonical form
 of the credential or rich schema `content`'s JSON.
 The canonicalization scheme we recommend is the IETF draft 
 [JSON Canonicalization Scheme (JCS)](https://tools.ietf.org/id/draft-rundgren-json-canonicalization-scheme-16.html).

- The set of attributes in `credentialSubject` must match the one defined by the mapping object.

- `issuer` and `issuanceDate` attributes must be signed by the issuer as any other attribute from the `credentialSubject`.
This allows the holder to selectively disclose `issuer` and `issuanceDate` attributes in the same way as other attributes from the schema.
 
- Any additional attributes from the Verifiable Credentials Data Model must also be signed by the 
issuer as any other attribute from the `credentialSubject`. This allows the holder to selectively disclose those
attributes in the same way as other attributes from the schema. 

- Currently Indy supports only the following values for some of the `type` properties:
  - The `proof`'s `type` must be equal to either `CL` or `CL2` for Camenisch-Lysyanskaya (Anoncreds 1.0) and
Camenisch-Lysyanskaya 2.0 (Anoncreds 2.0) signature schemes, respectively.
  - The `credentialSchema`'s `type` must be equal to `cdf`.     

The following diagram summarizes the relationship between W3C compatible verifiable credentilas in Indy and
the corresponding rich schema objects: 

![](relationship-diagram.png)



### Example
Let's consider a **Rich Schema** object with the following `content`: 
```
{
    "@id": "did:sov:4e9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    "@context": "did:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    "@type": "rdfs:Class",
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

Let's consider the corresponding **Mapping** object with the following `content`:
```
    '@id': "did:sov:5e9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    '@context': "did:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    '@type': "rdfs:Class",
    "schema": "did:sov:4e9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    "attribuites" : {
        "issuer": [{
            "enc": "did:sov:9x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
            "rank": 9
        }],
        "issuanceDate": [{
            "enc": "did:sov:119F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
            "rank": 10
        }],        
        "expirationDate": [{
            "enc": "did:sov:119F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
            "rank": 11
        }],        
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
    }
```
Finally, let's consider the corresponding **Credential Definition** object with `id=did:sov:9F9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD` 
and the following `content`:
```
"signatureType": "CL",
"mapping": "did:sov:5e9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
"schema": "did:sov:4e9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
"publicKey": {
    "primary": "...",
    "revocation": "..."
}
```

Then the corresponding **W3C Credential** for CL signature scheme may look as follows: 
```
{
  "@context": [
    "did:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    "https://www.w3.org/2018/credentials/v1"
  ]
  "type": ["VerifiableCredential", "did:sov:4e9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD"],
  "credentialSchema": {
    "id": "id:sov:9F9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    "type": "cdf"
  },
  "issuer": "did:sov:Wz4eUg7SetGfaUVCn8U9d62oDYrUJLuUtcy619",
  "issuanceDate": "2020-03-01T19:23:24Z",
  "credentialSubject": {
    "driver": "Jane Doe",
    "dateOfIssue": "2020-03-01",
    "issuingAuthority": "State of Utah",
    "licenseNumber": "ABC1234",
    "categoriesOfVehicles": {
      "vehicleType": "passenger",
      "dateOfIssue": "2018-06-03",
    },
    "administrativeNumber": "1234"
  },
  "proof": {
    "type": "CL2",
    "signature": "8eGWSiTiWtEA8WnBwX4T259STpxpRKuk...kpFnikqqSP3GMW7mVxC4chxFhVs",
    "signatureCorrectnessProof": "SNQbW3u1QV5q89qhxA1xyVqFa6jCrKwv...dsRypyuGGK3RhhBUvH1tPEL8orH",
    "revocationData": "...."
  }
}
```

Let's consider every field in details:
- `@content` points to two contexts: one common for all W3C credentials,
 and one used by the corresponding rich schema and mapping.
 - `type` is an array of two values: common for all W3C credentials `VerifiableCredential` type 
 (see `https://www.w3.org/2018/credentials/v1` context), and ID of the rich rchema the credential is created against.
 - `credentialSchema` points to the corresponding credential definition. 
 `cdf` is the type of credential definition object among rich schema objects.
 - `issuer` is the DID of the issuer who is the controller of the credential definition on the ledger.
 - `issuanceDate`is the date of the issuance. This is the date after which the claims in the credential 
 are considered valid by the issuer, which may be different from the date the credential was signed
 by the issuer or received by the holder.
 - `credentialSubject` contains a list of (nested) claims and the corresponding values. The set of claims 
 matches the ones defined by the mapping.
 -  `proof` contains a ZKP signature (of `CL2` type in this example). The content is specific to the signature type 
 and should not be parsed by applications. 

### Indy Node API
As Indy credentials are never stored on the Ledger, no changes in `indy-node` repository are required 
besides general rich schema support (see [Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common)).

### Indy VDR API
As Indy credentials are never stored on the Ledger, no changes in `indy-vdr` repository are required 
besides general rich schema support (see [Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common)).

### Indy Credx API

The W3C and Rich Schema compatible protocols will be implemented in `indy-credx` under the following assumptions:
- `indy-credx` already has a set of API calls for credential issuance and proof presentation protocols. 
These calls work with the "old" (non-W3C-compatible) credential format and the "old" (non-rich) schema objects. 
- W3C and Rich Schema compatible protocols will be implemented as a set of new API calls.
- The new W3C compatible API calls can be almost the same as for the current ("old") approach
 since issuance and presentation protocols are not changed. However, there is the following difference:
  - The expected format of credentials and presentations is the W3C compatible one.
  - All calls expect rich schema objects instead of "old" Schema objects.
  - The encoding of claim's attributes to integers is done according to the encoding objects specified by the corresponding mapping object.
- The new W3C compatible API calls have `w3c` prefix to be distinguished from non-W3C ("old") ones. 
      
#### Compatiblity with non-W3C credentials
The compatibility between "old" format of credentials and schemas and a "new" W3C one is **not** 
assumed on libindy layer. It means that
  - W3C compatible versions of issuance and presentation protocols will work with rich schema objects only.
  - W3C compatible presentation definitions (proof requests) expect W3C presentations, so that only W3C 
  compatible credentials can be used to generate a presentation.
  - We assume that on libindy level non-W3C compatible proof requests ("old" proof requests) will work with non-W3C compatible
  credentials only. Applications using libindy can, in theory, use W3C compatible credentials with "old" proof requests,
  but this is out-of-scope for the current HIPE.

|               | W3C compatible credentials | Non-W3C compatible credentials |
| ------------- | ------------- | --- |
| **W3C compatible proof request**  | Yes  | No  |
| **Non-W3C compatible proof request**  | No  | Yes |
  

  

#### Relationship with Rich Schema
libindy API will have the following assumptions:
- W3C compatible credentials will work with rich schema objects only.
- Non-W3C compatible ("old") credentials will work with the "old" Schema only.

Applications using libindy can, in theory, use rich schema for non-W3C compatible credentials,
  but this is out-of-scope for the current HIPE.  

|               | W3C compatible credentials | Non-W3C compatible credentials |
| ------------- | ------------- | --- |
| **Rich Schema**  | Yes  | No  |
| **Old Schema**  | No  | Yes |
  
#### Relationship with Anoncreds version   
Both W3C compatible and non-W3C compatible issuance and presentation protocols can work with either Anoncreds 1.0 (`CL`)
or Anoncreds 2.0 (`CL2`); the Anoncreds version is orthogonal to the Schema and credentials format.
 - Anoncreds 1.0 is already working with the Old Schema approach.
 - Both Anoncreds 1.0 and 2.0 must work the with rich schema approach.
 - It's questionable whether Anoncreds 2.0 should work with the old Schema approach.

|               | W3C compatible credentials  and Rich Schema | Non-W3C compatible credentials and Old Schema |
| ------------- | ------------- | --- |
| **Anoncreds 1.0**  | In Progress  | Already supported  |
| **Anoncreds 2.0**  | TBD  |  Questionable  |

## Reference
[reference]: #reference

- [W3C Verifiable Credentials Specification](https://w3c.github.io/vc-data-model)
- [0119: Rich Schema Objects](https://github.com/hyperledger/indy-hipe/tree/master/text/0119-rich-schemas)
- [0120: Rich Schema Objects Common](https://github.com/hyperledger/indy-hipe/tree/master/text/0120-rich-schemas-common) 

## Drawbacks
[drawbacks]: #drawbacks

- The credential object formats introduced here will not be backwards
compatible with the current set of credential objects.
- Rich schemas introduce greater complexity.
- The new formats rely largely on JSON-LD serialization and may be
dependent on full or limited JSON-LD processing.


## Unresolved questions and future work
[unresolved]: #unresolved-questions

- We may consider using old credentials for W3C compatible proof requets as well as using
of W3C compatilbe credentials for old proof requests.
- It may make sense to extend DID specification to include using DID as a credential ID.
- It may make sense to extend DID specification to include using DID for referencing rich schema objects.
- The proposed canonicalization form of a content to be used for DID's id-string generation is in a Draft version,
 so we may find a better way to do it.