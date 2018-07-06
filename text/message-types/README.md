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

We propose that message types are a URN with the following structure:

```
urn:<project>:<subproject>:<context>:message_type:<organization_domain>/<message_family>/<major_family_version>.<minor_family_version>/<message_type>
```

For example, a message type for Sovrin implementations of Indy agents might look like the following:

```
urn:indy:sov:agent:message_type:sovrin.org/connection/1.0/offer
```

### Message Families
Message families provide a logical grouping for message types. These families, along with each type belonging to that
family, are to be defined in future HIPEs or through means appropriate to subprojects.

### Family Versioning
Version numbering should essentially follow [Semantic Versioning 2.0.0](https://semver.org/), excluding patch version
number. To summarize, a change in the major family version number indicates a breaking change while the minor family
version number indicates non-breaking additions.

# Reference
[reference]: #reference

- The message type form has been discussed by the community in this [Google Doc](https://docs.google.com/document/d/1mRLPOK4VmU9YYdxHJSxgqBp19gNh3fT7Qk4Q069VPY8/edit#heading=h.vscsgxe5ai5j)
- [Semantic Versioning](https://semver.org)
- [Core Message Structure](https://github.com/hyperledger/indy-hipe/pull/17)

# Drawbacks
[drawbacks]: #drawbacks

Just having something to follow as convention is necessary. Drawbacks may be identified later.

# Rationale and alternatives
[alternatives]: #alternatives

- Perhaps a simpler message structure as defined per application would be easier to implement but this does not address
  the problem of interoperability.

# Prior art
[prior-art]: #prior-art

Conventions that Evernym and/or BCGov with their VON Agent work may differ from those proposed here. Comments from
either of these parties and others are encouraged.

# Unresolved questions
[unresolved]: #unresolved-questions

- Should `<subproject>` be a part of the type? For instance, in `urn:indy:sov:agent`, should `sov` be dropped?
- Is `<context>` a necessary part of the type? For instance, in `urn:indy:sov:agent`, should `agent` be dropped?
- Is this level of granularity always required if `subproject` and `context` are kept?
- Are message types and expected contents something that may one day live on the ledger, similar to schema or credential
  definitions?
- Is there a better way? Is this significant enough to expend further resources on this topic at the moment?
