# Semver Rules for Protocols

[Semver](http://semver.org) rules apply in cascading fashion to versions
of protocols and individual message types. The version of a message type
or protocol is expressed in the `semver` portion of its [identifying URI](
uris.md).

Individual message types are versioned as part of a coherent protocol, which
constitutes a [public API in the semver sense](https://semver.org/#spec-item-1).
An individual message type can add new optional fields, or deprecate
existing fields, [with only a change to its protocol's minor
version](https://semver.org/#spec-item-7).
Similarly, a protocol can add new message types (or [adopted
ones](#adopted-messages)) with only a change
to the minor version. It can announce deprecated fields. It can add additional
semantics around optional decorators. These are all backwards-compatible
changes, also requiring only a minor version update.

Changes that remove fields or message types, that make formerly optional
things required, or that alter the state machine in incompatible
ways, must result in an [increase of the major version of the protocol/primary
message family](https://semver.org/#spec-item-8).
