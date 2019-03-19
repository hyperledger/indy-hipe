# Rich Schema Objects
- Name: rich-schemas
- Author: Ken Ebert ken@sovrin.org, Brent Zundel brent.zundel@evernym.com
- Start Date: 2019-03-19T15:39:48-06:00
- PR: 
- Jira Issue: 

## Summary
[summary]: #summary

A high-level description of the components of an anonymous credential
ecosystem that supports rich schemas, W3C Verifiable Credentials and
Presentations, and correspondingly rich presentation requests. Rich
schemas are hierarchically composable graph-based representations of
complex data. For these rich schemas to be incorporated into the indy
anonymous credential ecosystem, we also introduce such objects as
mappings, encodings, presentation definitions and their associated
contexts.

This HIPE provides a brief description of each rich schema object.
Future HIPEs will provide greater detail for each individual object and
will be linked to from this document.

## Motivation
[motivation]: #motivation

### Standards Compliance
The W3C Verifiable Claims Working Group (VCWG) will soon be releasing a
verifiable credential data model. This proposal brings the format of
Indy's anonymous credentials and presentations into compliance with that
standard.

## Interoperability
Compliance with the VCWG data model introduces the possibility of
interoperability with other credentials that also comply with the
standard.

Additionally, the new rich schemas are compatible with or the same as
existing schemas defined by industry standards bodies and communities of
interest. This means that the rich schemas should be interoperable with
those found on schema.org, for example. Schemas can also be readily
defined for those organizations that have standards for data
representation, but who do not have an existing formal schema
representation.

## Shared Semantic Meaning
The current format for schemas requires an implicit understanding of the
semantic meaning of the schema by issuers, holders, and verifiers. There
is currently no explicit typing or possible composability.

The rich schemas and associated constructs are linked data objects that
have an explicitly shared context. This allows for all entities in the
ecosystem to operate with a shared vocabulary.

Because rich schemas are composable, the potential data types that may
be used for field values are themselves specified in schemas that are
linked to in the property definitions. The shared semantic meaning gives
greater assurance that the meaning of a presentation matches the
intention of the issuer.

## Improved Predicate Proofs
The current encoding of properties for signatures supports only integer
and string data types. Introducing standard encoding methods for other
data types will enable predicate proof support for floating point
numbers, dates and times, and other assorted measurements. We also
introduce a mapping object that ties intended encoding methods to each
schema property that may be signed so that an issuer will have the
ability to canonically specify how the data they wish to sign maps to
the signature they provide.


## Tutorial
[tutorial]: #tutorial

TODO: Add introductory text
[Rich schema objects](rich-schema-objects.png)

### New Concepts

#### Contexts

#### Mappings

#### Encodings

#### Presentation Definitions

### Changes to Existing Concepts

#### Rich Schemas

#### Credential Definitions

#### Verifiable Credentials

#### Presentations

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

Discuss prior art, both the good and the bad, in relation to this proposal.
A few examples of what this can include are:

- Does this feature exist in other SSI ecosystems and what experience have
their community had?
- For other teams: What lessons can we learn from other attempts?
- Papers: Are there any published papers or great posts that discuss this?
If you have some relevant papers to refer to, this can serve as a more detailed
theoretical background.

This section is intended to encourage you as an author to think about the
lessons from other implementers, provide readers of your proposal with a
fuller picture. If there is no prior art, that is fine - your ideas are
interesting to us whether they are brand new or if they are an adaptation
from other communities.

Note that while precedent set by other communities is some motivation, it
does not on its own motivate an enhancement proposal here. Please also take
into consideration that Indy sometimes intentionally diverges from common
identity features.

## Unresolved questions
[unresolved]: #unresolved-questions

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
