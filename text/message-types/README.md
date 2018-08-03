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

For example, a message type might look like the following:

```
did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connection/1.0/request
```

The DID Document corresponding to this DID would look something like:
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
    // this key can be used to authenticate as DID ...9938
    "type": "RsaSignatureAuthentication2018",
    "publicKey": "did:example:123456789abcdefghi#keys-1"
  }],
  "service": [{
    "type": "Document",
    "name": "spec",
    "serviceEndpoint": "https://sovrin.org/specs/"
  }]
}
```

The DID above would then resolve to `https://sovrin.org/specs/connection/1.0/request`.

### Message Families
Message families provide a logical grouping for message types. These families, along with each type belonging to that
family, are to be defined in future HIPEs or through means appropriate to subprojects.

### Family Versioning
Version numbering should essentially follow [Semantic Versioning 2.0.0](https://semver.org/), excluding patch version
number. To summarize, a change in the major family version number indicates a breaking change while the minor family
version number indicates non-breaking additions.

## Indy Core Message Namespace
`did:sov:BzCbsNYhMrjHiqZDTUASHg` will be used to namespace message families defined as "core message families" by the
community.

This DID is currently held by Daniel Hardman. Ownership will be transferred to the correct entity as soon as possible.

# Reference
[reference]: #reference
- [Drummond Reed's presentation on using DIDs as message type specifiers](https://docs.google.com/document/d/1t-AsCPjvERBZq9l-iXn2xffJwlNfFoQhktfIaMFjN-c/edit#heading=h.x1wbqftasrx2)
- [Daniel Hardman's Agent Summit Notes](http://bit.ly/2KkdWjE)
- [Stephen Curran's presentation summarizing the Agent Summit](https://docs.google.com/presentation/d/1l-po2IKVhXZHKlgpLba2RGq0Md9Rf19lDLEXMKwLdco/edit)
- [Semantic Versioning](https://semver.org)
- [Core Message Structure](https://github.com/hyperledger/indy-hipe/pull/17)
