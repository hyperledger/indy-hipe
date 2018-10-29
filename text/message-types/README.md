- Name: message-types
- Author: Daniel Bluhm <daniel.bluhm@sovrin.org>
- Start Date: 2018-07-06
- PR:
- Jira Issue:

# Summary
[summary]: #summary

Define structure of message type strings used in agent to agent communication.

# Motivation
[motivation]: #motivation

A clear convention to follow for agent developers is necessary for interoperability and continued progress as a
community.

# Tutorial
[tutorial]: #tutorial

A "Message Type" is a required attribute of all communications sent between parties. The message type instructs the
receiving agent how to interpret the content and what content to expect as part of a given message.

We propose that message types are ledger resolvable DIDs with an endpoint specifier and path:

```
did:<method>:<id-string>;<service>/<message_family>/<major_family_version>.<minor_family_version>/<message_type>
```

## Example DID and DID Document for Message Type Specification

The following was taken from a presentation by Drummond Reed during the Agent Summit. A link to this presentation can be
found below in the [Reference](#reference) section.

### Problem
How to use a DID to identify a digital object that:

1. Can be widely referenced.
2. Is cryptographically verifiable.
3. Is human readable *enough* for developers.

### Solution
Use a full DID reference that contains a service name and path.

#### Example DID Reference
This DID reference contains a service name (`;spec`) followed by a path that expresses the semantics of an example
message type family.

```
did:sov:123456789abcdefghi1234;spec/messagefamily/1.0/offer
```

### Example DID Document
This example DID document shows a service endpoint that includes a name property (emphasized) whose purpose is to enable
creation of DID references that can deterministically select that service in order to have an algorithmic transformation
into a concrete URI.

```json
{
  "@context": "https://w3id.org/did/v1",
  "id": "did:example:123456789abcdefghi",
  "publicKey": [{
    "id": "did:example:123456789abcdefghi#keys-1",
    "type": "RsaSigningKey2018",
    "owner": "did:example:123456789abcdefghi",
    "publicKeyPem": "-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\r\n"
  }],
  "authentication": [{
    "type": "RsaSignatureAuthentication2018",
    "publicKey": "did:example:123456789abcdefghi#keys-1"
  }],
  "service": [{
    "type": "Document",
    "name": "spec", // <--- Name property
    "serviceEndpoint": "https://sovrin.org/specs/"
  }]
}
```

### Resolution Process
This is the full ABNF for a DID:

```ABNF
  did-reference      = did [ ";" did-service ] [ "/" did-path ] [ "?" did-query ]
                     [ "#" did-frag ]
  did                = "did:" method ":" specific-idstring
  method             = 1*namechar
  namechar           = %x61-7A / DIGIT
  specific-idstring  = idstring *( ":" idstring )
  idstring           = 1*idchar
  idchar             = ALPHA / DIGIT / "." / "-"
  did-service        = 1*servchar *( ";" 1*servchar )
  servchar           = idchar / "=" / "&"
```

The purpose of the `did-service` component that may optionally follow a DID is to enable construction of a DID reference
that may be algorithmically transformed into a concrete URL to access the target resource. There are two algorithms for
this transformation. Both begin with the same first step:

1. Extract the DID plus the `did-service` component from the DID reference. Call this the *DID service locator*. Call
   the rest of the DID reference the `service-specific` string.

### Service Selection by ID
This algorithm MUST be used if the `did-service` component does NOT begin with the string `type=`.

2. Select the first `service` object whose id property contains an exact match to the DID service locator.
3. Select the `serviceEndpoint` property of the selected `service` object.
4. Extract the value of the `serviceEndpoint` property. Call this the *endpoint URL*.
5. Append the service-specific string to the endpoint URL.
6. The final result is the concrete URL.

#### Example
Say the following DID reference was resolved against a DID document containing the example `service` block above:

```
did:sov:123456789abcdefghi1234;spec/messagefamily/1.0/offer
```

A DID resolver would algorithmically transform that DID reference to the following concrete URL:

```
https://sovrin.org/specs/messagefamily/1.0/offer
```

## Indy Core Message Namespace
`did:sov:BzCbsNYhMrjHiqZDTUASHg` will be used to namespace message families defined by the community as "core message
families" or message families that agents must minimally support.

This DID is currently held by Daniel Hardman. Ownership will be transferred to the correct entity as soon as possible.

## Message Families
Message families provide a logical grouping for message types. These families, along with each type belonging to that
family, are to be defined in future HIPEs or through means appropriate to subprojects.

### Family Versioning
Version numbering should essentially follow [Semantic Versioning 2.0.0](https://semver.org/), excluding patch version
number. To summarize, a change in the major family version number indicates a breaking change while the minor family
version number indicates non-breaking additions.

# Reference
[reference]: #reference
- [Drummond Reed's presentation on using DIDs as message type specifiers](https://docs.google.com/document/d/1t-AsCPjvERBZq9l-iXn2xffJwlNfFoQhktfIaMFjN-c/edit#heading=h.x1wbqftasrx2)
- [Daniel Hardman's Agent Summit Notes](http://bit.ly/2KkdWjE)
- [Stephen Curran's presentation summarizing the Agent Summit](https://docs.google.com/presentation/d/1l-po2IKVhXZHKlgpLba2RGq0Md9Rf19lDLEXMKwLdco/edit)
- [DID Spec](https://w3c-ccg.github.io/did-spec/)
- [Semantic Versioning](https://semver.org)
- [Core Message Structure](https://github.com/hyperledger/indy-hipe/pull/17)
