- Name: json-ld-compatibility
- Author: Daniel Hardman <daniel.hardman@gmail.com>
- Start Date: 2019-01-23
- PR: (leave this empty)

# Summary
[summary]: #summary

Explains the goals of Indy agent-to-agent messaging with respect to JSON-LD,
and how Indy proposes to accomplish them.

# Motivation
[motivation]: #motivation

JSON-LD is a familiar body of conventions that enriches the expressive power of
plain JSON. It is natural for people who arrive in the Indy agent-to-agent (A2A)
ecosystem to wonder whether we are using JSON-LD--and if so, how. We need a
coherent answer that clarifies our intentions and that keeps us true to those
intentions as the ecosystem evolves.

# Tutorial
[tutorial]: #tutorial

The [JSON-LD spec](https://w3c.github.io/json-ld-syntax/) is a recommendation
and work product of the [W3C Credentials Community Group](https://github.com/w3c-ccg/community).
It is not a formally approved W3C standard, but it has significant gravitas in
identity circles--and with good reason. It gives to JSON some capabilities that
are sorely needed to model the semantic web, including linking, namespacing,
datatyping, signing, and a strong story for schema (partly through the use of
JSON-LD on [schema.org](http://schema.org)).

However, JSON-LD also comes with some conceptual and technical baggage. It can
be hard for developers to master its subtleties; it requires very flexible parsing
behavior after built-in JSON support is used to deserialize; it references a family
of related specs that have their own learning curve; the formality of its test
suite and libraries may get in the way of a developer who just wants to read and
write JSON and "get stuff done."

In addition, the problem domain of agent-to-agent messaging (A2A) is somewhat
different from the places where JSON-LD has the most traction. The sweet spot
for A2A is small, relatively simple JSON documents where code behavior is
strongly bound to the needs of a specific interaction. A2A needs to work with
extremely simple agents on embedded platforms. Such agents may experience full
JSON-LD support as an undue burden when they don't even have a familiar desktop
OS. They don't need arbitrary semantic complexity.

If we wanted to use email technology to send a verifiable credential, we would
model the credential as an attachment, not enrich the schema of raw
email message bodies. A2A invites a [similar approach](https://github.com/hyperledger/indy-hipe/pull/78).

### Goal

The agent-to-agent messaging effort that began in the Indy community wants to
benefit from the accessibility of ordinary JSON, but leave an easy path for
more sophisticated JSON-LD-driven patterns when the need arises. We therefore
set for ourselves this goal:

> __Be compatible__ with JSON-LD, such that advanced use cases can take advantage
  of it where it makes sense, __but impose no dependencies__ on the mental model or
  the tooling of JSON-LD for the casual developer.

### What the Casual Developer Needs to Know

* __The `@` character in A2A messages is reserved for JSON-LD-isms__. Any usage
of JSON keys that begin with this character is required to be JSON-LD-compatible,
and any time you see it, you are seeing JSON-LD at work.

* __`@type` and `@id` are required at the root of every message__. The meaning of
these fields in A2A matches JSON-LD's expectations, but you don't need to learn
JSON-LD to use them.

* __JSON-LD's more advanced mechanisms are an option__--not invoked ad hoc on a
message-by-message basis, but specified in the formal description of a message
family. You will know how much JSON-LD is relevant to a protocol when you
implement it. In general, the community will want to discuss usage of new
JSON-LD constructs before embracing them in protocols with broad interoperability
intentions, because of the [goal articulated above](#goal).

* __The decorator concept in A2A is orthogonal to JSON-LD__, and is far more likely
to be relevant to your early learning. See the [Decorator HIPE](https://github.com/hyperledger/indy-hipe/pull/71).

That's it.

### Details

Compatibility with JSON-LD was evaluated against version 1.1 of the
JSON-LD spec, current in early 2019. If material changes in the spec
are forthcoming, a new analysis may be worthwhile. Our current
understanding follows.

#### `@type`

The type of an A2A message, and its associated route or handler in dispatching code,
is given by the JSON-LD `@type` property at the root of a message.
[JSON-LD requires this value to be an IRI](https://w3c.github.io/json-ld-syntax/#typed-values).
A2A DID references are [fully compliant](https://w3c-ccg.github.io/did-spec/#paths).
Instances of `@type` on any node other than a message root have JSON-LD meaning,
but no predefined relevance in A2A.

#### `@id`

The identifier for an A2A message is given by the JSON-LD `@id` property at the
root of a message. [JSON-LD requires this value to be an IRI](https://w3c.github.io/json-ld-syntax/#specifying-the-type).
A2A message IDs are relative IRIs, and can be converted to absolute form by
prepending `a2a://`. Instances of `@id` on any node other than a message root
have JSON-LD meaning, but no predefined relevance in A2A.

#### `@context`

This is JSON-LD’s namespacing mechanism. It is active in A2A messages, but can
be ignored for simple processing, in the same way namespaces in XML are often
ignored for simple tasks.

Every A2A message has an associated `@context`, but we
have chosen to follow the procedure described in [section
6 of the JSON-LD spec](https://w3c.github.io/json-ld-syntax/#interpreting-json-as-json-ld),
which focuses on how ordinary JSON can be intepreted as JSON-LD by communicating
`@context` out of band.

A2A messages communicate the context out of band by specifying it in the
protocol definition (e.g., HIPE) for the associated message type; thus, the
value of `@type` indirectly gives the relevant `@context`. In advanced use cases,
`@context` may appear in an A2A message, supplementing this behavior.

#### Ordering

[JSON-LD specifies](https://w3c.github.io/json-ld-syntax/#sets-and-lists) that
the order of items in arrays is NOT significant, and notes (correctly) that
this is the opposite of the standard assumption for plain JSON.
This makes sense when viewed through the lens of JSON-LD’s role as a
transformation of RDF.

Since we want to violate as few assumptions as possible for a developer with
general knowledge of JSON, A2A messages reverse this default, making arrays
an ordered construct, as if all A2A message `@context`s contained something
like:

```JSON
"each field": { "@container": "@list"}
 ```
To contravene the default, use a JSON-LD construction like this in `@context`:

```JSON
"myfield": { "@container": "@set"}
 ```

#### Decorators

Decorators are JSON fragments that can be included in any A2A message. They
enter the formally defined JSON-LD namespace via a JSON-LD fragment that
is automatically imputed to every A2A message:

```JSON
"@context": {
  "@vocab": "https://github.com/hyperledger/indy-hipe/"
}
```

All decorators use the reserved prefix char `~` (tilde). For more on
decorators, see the [Decorator HIPE](https://github.com/hyperledger/indy-hipe/pull/71).

#### Signing

JSON-LD is associated but not strictly bound to a signing mechanism,
[LD-Signatures](https://w3c-dvcg.github.io/ld-signatures/). It’s a good
mechanism, but it comes with some baggage: you must canonicalize, which means
you must resolve every “term” (key name) to its fully qualified form by
expanding contexts before signing. This raises the bar for JSON-LD
sophistication and library dependencies.

The A2A community is not opposed to using LD Signatures for problems that
need them, but has decided not to adopt the mechanism across the board.
There is [another signing mechanism](https://github.com/hyperledger/indy-hipe/pull/79)
that is far simpler, and adequate for many scenarios. We’ll use whichever
scheme is best suited to circumstances.

#### Type Coercion

A2A messages generally do not need [this feature of JSON-LD](
https://w3c.github.io/json-ld-syntax/#type-coercion), because there are
well understood [conventions around date-time datatypes](
https://github.com/hyperledger/indy-hipe/pull/76), and individual
HIPEs that define each message type can further clarify such subtleties.
However, it is available on a message-type-definition basis (not ad hoc).

#### Node References
JSON-LD lets one field reference another. See [example 67](
 https://w3c.github.io/json-ld-syntax/#ex-67-referencing-node-objects) (note
 that the ref could have just been “#me” instead of the fully qualified IRI).
 We may need this construct at some point in A2A, but it is not in active
 use yet.
 
 
#### Internationalization and Localization

[JSON-LD describes a mechanism](https://w3c.github.io/json-ld-syntax/#string-internationalization)
for this. It has approximately the same features as the one described in
[indy-hipe PR #64](https://github.com/hyperledger/indy-hipe/pull/64/), with a few exceptions:

* The JSON-LD mechanism only applies to strings; it is explicitly disallowed
for describing dates, numbers, or any strings that coerce to dates or numbers.
* The JSON-LD mechanism is *language-centric* rather than *locale-centric*.
For example, it doesn't specify sort order, time-of-day, or currency semantics.
* There is no notion of a code that maps to strings--just a notion of strings
that all have the same meaning. This means it doesn’t help us solve the
problem of [locale-independent error codes](https://github.com/hyperledger/indy-hipe/pull/65).
* The notion of mappings of values for different locales is separable into an
external catalog, but only if a value is referenced or included implicitly in
a doc. In other words, a processor has to see the full message catalog when
evaluating the doc.
* It’s a bit awkward to retrofit onto an existing schema, because it requires
a redefinition of the field that contains localized values, from being a
single string to being a dictionary with language mappings. In other words,
the schema before and after a developer adds localization support is not just
different by new, optional fields; it is a breaking change. This contrasts
with the indy PR approach, where the language mapping can be added after the
fact, and gets associated by convention.
* It doesn’t support localization of keys--only values. There are corner
cases where key localization is desirable.

Because of these misalignments, the A2A ecosystem plans to use [its own
solution](https://github.com/hyperledger/indy-hipe/pull/64/) to this problem.

#### Additional JSON-LD Constructs

The following [JSON-LD keywords](https://w3c.github.io/json-ld-syntax/#keywords)
may be useful in A2A at some point in the future: 
`@base`, `@index`, `@container` (cf `@list` and `@set`), `@nest`, `@value`,
`@graph`, `@prefix`, `@reverse`, `@version`.

# Drawbacks
[drawbacks]: #drawbacks

By attempting compatibility but only lightweight usage of JSON-LD, we are
neither all-in on JSON-LD, nor all-out. This could cause confusion. We are
making the bet that most developers won't need to know or care about the
details; they'll simply learn that `@type` and `@id` are special, required
fields on messages. Designers of protocols will need to know a bit more.

# Rationale and alternatives
[alternatives]: #alternatives

- We could go all-in on JSON-LD. This would require adoption of sophisticated
parsing that is impractical on embedded platforms, but it would add a lot
of semantic sophistication. 
- We could avoid JSON-LD entirely. This would force us to reinvent the wheel
in some cases, and it would be frustrating to our friends in other SSI
communities that are more JSON-LD-centric.

# Unresolved questions
[unresolved]: #unresolved-questions

- Is the reversal of JSON-LD's default of unordered arrays valid?
- Is there a good way to discover that new A2A proposals should
consider JSON-LD solutions, and make sure such questions get evaluated
thoughtfully?