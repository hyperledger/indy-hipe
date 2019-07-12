# 0139: Image As Attribute Via Aries-0036 Issue-Credential Protocol
- Author: Stephen Klump (stephen.klump@becker-carroll.com)
- Start Date: 2019-06-01

## Status
- Status: PROPOSED
- Status Date: 2019-07-12
- Status Note: Implements v1.0 of
[Aries-0036](
https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential)

## Summary

Engineering notes regarding implementation of the [Aries-0036](
https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential)
v1.0 issue-credential protocol in response to [JIRA IS-1281](
https://jira.hyperledger.org/browse/IS-1281).

## Motivation

[JIRA IS-1281](https://jira.hyperledger.org/browse/IS-1281) requested a
proof of concept using v1.0 of the credential exchange protocol to issue
and store a credential with a base64-encoded JPEG, of size least 100kB,
as an attribute.

## Tutorial

The work involved reviewing and then implementing the data structures and
algorithms constituting v1.0 of the
[Aries-0036](
https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential)
issue-credential protocol,
then using the platform to issue and store a credential having a
base64-encoded JPEG for an attribute value.

This discussion presents engineering notes regarding the exercise
experience.

### Aries-0036 Particulars

[Aries-0036](
https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential)
outlines two distinct paths to credential exchange, depending on
the initiator - issuer or holder. The [choreography diagram](
https://github.com/hyperledger/aries-rfcs/blob/master/features/0036-issue-credential/credential-issuance.png)
illustrates.

#### Credential Proposal, Bound Credential Offer, Credential Request, Credential

To initiate this path, the holder presents the issuer a credential proposal.
The issuer responds with a "bound" credential offer against the proposal.
The holder responds with a corresponding credential request and the issuer
issues the credential, which the holder stores.

#### Free Credential Offer, Credential Request, Credential

To initiate this path, the issuer presents the holder a credential offer
free of any credential proposal. The holder responds with a corresponding
credential request and the issuer issues the credential, which the holder
stores.

### Aries-0036 Review: Attribute Encoding

In implementing its data structures and algorithms, the exercise noted the
need in the standard for an `encoding` parameter for attributes in the
credential preview. The encoding value served on both sides of the exchange,
in concert with its MIME type, allowing:

- the issuer to decode and render incoming binary attribute values for
content inspection to judge suitability to issue
- the holder to decode and render stored attribute values for presentation.

Indy credentials require strings as raw attribute values; as such, attribute
values retain any encoding from proposal through storage.

The Aries working group accepted the update into the emerging version 1.0
of the standard; its status is PROPOSED.

### Aries-0036 Implementation

The exercise built on [aries-cloudagent-python](
https://github.com/hyperledger/aries-cloudagent-python) to implement message
types of [Aries-0036](
https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential):

- credential proposal
- credential offer
- credential request
- credential issue

in addition to the common inner credential preview block, which in itself
is not a message type.

### Aries-0017 Implementation

As a prerequisite, the demonstration implemented a subset of the attachment
decorator specification of [Aries-0017](
https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0017-attachments).

In particular, the credential exchange messages above required the [embedding](
https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0017-attachments#embedding)
approach regarding attachment decorators with base64-encoded JSON-dumped (indy
structure) `data` content.

### Credential Attribute Metadata

As discussed above, the (indy) issuer issues credentials with attributes
having string raw values, not binary; the (indy) holder stores these
credentials in the wallet as issued. To recall encoding regimen and MIME
type per attribute, the holder must store a small amount of additional metadata.

The implementation assumed that the same attributes would always feature the
same attribute encoding and MIME type, as per the credential preview exhibited in
the credential offer message of the credential exchange. This assumption represents
a simplification for demonstration purposes; conceivably, the holder could need
to store a record per credential; for example, to support multiple image formats.

The exercise stored this metadata, per credential definition, in a non-secret record
in the wallet. To present an attribute value to a human user, the holder would need to
fetch the MIME type and encoding, decode the raw value, and render it with a suitable
application.

Note that having issued a credential, an issuer would not need such metadata again: the
demonstration did not store such metadata in the wallet on the issuer side.

### Regarding Decorators

This section outlines considerations regarding the use of decorators within the
[Aries-0036](
https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential)
issue-credential protocol.

#### Decorators as Object Components

The [Aries-0036](
https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential)
standard defines decorators as integral parts of the credential offer, credential
request, and and credential issue messages. Prior implementations of Aries data
structures had used them orthogonally, traversing distinct Aries data structure
definitions while providing common abstraction semantics (e.g., threading).

As such, the [Aries cloud agent code base](
https://github.com/hyperledger/aries-cloudagent-python) had extracted all
attachments from message objects before validating them against their
respective schemas. This approach initially caused [marshmallow](
https://github.com/marshmallow-code) schema validation to fail for the
credential offer, credential request, and credential issue messages.

To obviate this result, the demonstration implemented a subclass of the default
decorator set (comprising those understood as orthogonal to agent messages). The
subclass inherited methods to load and extract decorator content; this processing
left attachment decorators intact, both allowing message validation and specifying
message schemas with the richness of their attachment decorators.

#### Decorators as Arrays

The [Aries-0036](
https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential)
standard introduces the novelty of the attachment decorator as an array of objects,
rather than as a simple object. The demonstration code limited itself to unitary
arrays of such attachments in practice.

Since the [Aries-0036](
https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential)
standard defines its attachment decorators as integral to its message
structures, and since the demonstration left these decorators intact on the
message, this novelty presented no special difficulties in processing.

However, the Aries standardization efforts should consider a separate marker
such as `~~` to denote list attachments. Since JSON allows arrays of objects
of different types, validating content of decorator arrays could present a
distinct problem relative to that of decorator objects.

#### Risk of Standard Drift

Since the attachment decorator has its own [Aries-0017](
https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0017-attachments)
standard independent of the [Aries-0036](
https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential)
issue-credential protocol, there is a risk that these specifications could
drift independently. A decorator implementation in the
main [aries-cloudagent-python](
https://github.com/hyperledger/aries-cloudagent-python) line could commit the entire
code base to a version of the attachment specification, reducing its flexibility.

The demonstration implemented the subset of the attachment decorator
specification of
[Aries-0017](
https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0017-attachments)
as noted [above](#aries-0017-implementation), as content within the
`issue-credential.v1_0` subpackage marking v1.0 of the [Aries-0036](
https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential)
standard. This version defines a state of both the issue-credential protocol standard
and, implicitly, its attachment decorator components. Any evolution of either
would entail an [Aries-0036](
https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential)
version increment, which a demonstration would put into its own corresponding
subpackage without forcing any change to the [Aries cloud agent code base](
https://github.com/hyperledger/aries-cloudagent-python) as a whole.

## Reference

The [draft pull request](
https://github.com/hyperledger/aries-cloudagent-python/pull/60)
contains the implementation discussed above, as an augmentation
of the hyperledger [aries-cloudagent-python](
https://github.com/hyperledger/aries-cloudagent-python) project.

## Drawbacks

The indy-sdk failed to issue credentials with attribute values over about
300kB. This is a known limitation that the indy group intends to consider
for possible remedy with anoncreds-2.0.

As discussed [above](#credential-attribute-metadata), the demonstration
assumed the same attribute metadata to apply across all credentials on a
credential definition. A production implementation would need to implement
a non-secret metadata record per wallet credential with any attribute
outside the defaults of MIME type `text/plain` and unencoded raw (string)
value.

As noted [above](#aries-0017-implementation), the demonstration assumed the
attachment of an encoded image in-band, embedded as an attribute in the
credential preview. The extension of attachment functionality to include
external links with SHA-256 hash content validation could provide
functionality useful in any context requiring the attachment decorator.

The demonstration code introduced a metadata format to satisfy immediate
holder requirements, but distinct agents could use distinct code bases
that may not understand each other's metadata formats. As such, moving
such an approach into production could restrict the holder in choice of
agents to present affected credential attributes intelligibly to humans.

## Rationale and alternatives

This design offered one means of issuing and accepting credentials with
larger binary values as credential attributes. More complete implementations
would address the [drawbacks](#drawbacks) above.

## Prior art

The existing [Aries cloud agent code base](
https://github.com/hyperledger/aries-cloudagent-python) worked with the
consensus credential exchange messages comprising what is commonly known
loosely as v0.1 of the protocol. This implementation assumes the
issuer-initiated path of the [free credential offer](
#free-credential-offer-credential-request-credential) above and does not
provide a holder-initiated credential proposal and corresponding
[bound credential offer](
#credential-proposal-bound-credential-offer-credential-request-credential).

The [Aries cloud agent](
https://github.com/hyperledger/aries-cloudagent-python), formerly known as
indy-catalyst-agent, was the first of its kind and largely fostered the
development of the [Aries-0036](
https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential)
standard itself.

## Unresolved questions

The demonstration motivates the discussion of reasonable sizes and types for
attribute values. For example, if images, why not video or interactive rich
media content?
