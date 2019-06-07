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

Explain the proposal as if it were already implemented and you
were teaching it to another Indy contributor or Indy consumer. That generally
means:

- Introducing new named concepts.
- Explaining the feature largely in terms of examples.
- Explaining how Indy contributors and/or consumers should *think* about the
feature, and how it should impact the way they use the ecosystem.
- If applicable, provide sample error messages, deprecation warnings, or
migration guidance.

Some enhancement proposals may be more aimed at contributors (e.g. for
consensus internals); others may be more aimed at consumers.

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

Please see [JSON-LD 1.1](https://w3c.github.io/json-ld-syntax)

## Unresolved questions
[unresolved]: #unresolved-questions

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
