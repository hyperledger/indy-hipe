# Contexts for Rich Schema Objects
- Name: rich-schema-contexts
- Author: Ken Ebert ken@sovrin.org, Brent Zundel brent.zundel@evernym.com
- Start Date: 2019-06-07T13:51:17-06:00
- PR:
- Jira Issue:

## Summary
[summary]: #summary

Every rich schema object has an associated `@context`. Contexts are JSON
objects. They are the standard mechanism for defining shared semantic
meaning among rich schema objects. Contexts allow schemas, mappings,
presentations, etc. to use a common vocabulary when referring to common
attributes, i.e. they provide an explicit shared semantic meaning.

## Motivation
[motivation]: #motivation

`@context` is JSON-LD’s namespacing mechanism.

## Tutorial
[tutorial]: #tutorial

### Intro to @context
`@context` is a JSON-LD construct that allows for namespacing and the
establishment of a common vocabulary.

They are referenced

### Stored on ledger
`@context` will be written to the ledger in much the same way that schemas
and credential definitions are written to the ledger now.

### Example @context

## Reference
[reference]: #reference

Provide guidance for implementers, procedures to inform testing,
interface definitions, formal function prototypes, error codes,
diagrams, and other technical details that might be looked up.
Strive to guarantee that:

- Interactions with other features are clear.
- Implementation trajectory is well defined.
- Corner cases are dissected by example.

## Drawbacks
[drawbacks]: #drawbacks

Why should we *not* do this?

## Rationale and alternatives
[alternatives]: #alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not
choosing them?
- What is the impact of not doing this?

## Prior art
[prior-art]: #prior-art

Please see [JSON-LD 1.1](https://w3c.github.io/json-ld-syntax#the-context)

## Unresolved questions
[unresolved]: #unresolved-questions

- Should the GUID portion of the DID which identifies a `@context` be taken
from the DID of the transaction submitter, or should there be established
a common DID to be associated with all immutable content such as `@context`?
