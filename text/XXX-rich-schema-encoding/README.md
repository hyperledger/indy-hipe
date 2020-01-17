# XXXX: Rich Schema Encodings
- Author: Ken Ebert <ken@sovrin.org>, Mike Lodder <mike@sovrin.org>, Brent Zundel <brent.zundel@evernym.com>
- Start Date: 2019-03-19

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: 2020-01-16
- Status Note: part of [Rich Schema work](0119-rich-schemas/README.md)

## Summary

The introduction of rich schemas and their associated greater range of
possible attribute value data types require correspondingly rich encoding
algorithms. The purpose of the new encoding object is to specify the
algorithm used to perform transformations for each attribute value data
type. The new encoding algorithms will also allow for extending the
cryptographic schemes and various sizes of encodings (256-bit, 384-bit,
etc.). The new encoding algorithms will allow for broader use of predicate
proofs, and avoid hashed values where they are not needed, as they do not
support predicate proofs.

## Motivation

All attribute values to be signed in anonymous credentials must be
transformed into 256-bit integers in order to support the 
[Camenisch-Lysyanskaya signature][CL-signatures] scheme.

The current Indy-SDK method for creating a credential only accepts
attributes which are encoded as 256-bit integers. The current libvcx
supports two source attribute types: numbers and strings. No configuration
method exists at this time to specify which encoding method will be applied
to a particular attribute for either the SDK or libvcx. All encoded
attribute values which are passed directly to the SDK were encoded by the
software external to the SDK, relying on implicit understanding of how the
external software should encode them. In libvcx, if the attribute value at
the time it is passed into libvcx is a number, it will be encoded as a
256-bit integer. If the attribute value is a string, the value will be
hashed using SHA-256, thereby encoding it as a 256-bit integer. The
resulting 256-bit integers may then be passed to the SDK and signed.

The introduction of encoding objects allows for a means of extending the
current set of encodings. All encoding objects describe how the input is
transformed into an integer representation of an attribute value according
to the encoding algorithm selected by the issuer.

## Tutorial

### Intro to encodings
encoding objects are used to describe the algorithms used for 
deterministically transforming input data types into the desired output
data types. The initial use of encodings will be to transform various
standard attribute value data types into integer representations.

Encodings are JSON objects. They are stored on the ledger.

### Properties
An encoding object is identified by a DID, and is formatted as a DID
Document. Since it is a content document 
#### id
The DID which identifies the encoding object.
#### encoding

##### name
The name of the encoding as a utf-8 string value. By convention, the name
should be taken from <input_type>_<output_type>
##### version
##### documentation
##### input_type
##### output_type
##### algorithm
##### test_vectors


## Reference

Provide guidance for implementers, procedures to inform testing,
interface definitions, formal function prototypes, error codes,
diagrams, and other technical details that might be looked up.
Strive to guarantee that:

- Interactions with other features are clear.
- Implementation trajectory is well defined.
- Corner cases are dissected by example.

## Drawbacks

Why should we *not* do this?

## Rationale and alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not
choosing them?
- What is the impact of not doing this?

## Prior art

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

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
