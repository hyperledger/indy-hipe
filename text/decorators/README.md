- Name: decorators
- Author: Daniel Hardman
- Start Date: 2018-12-14
- HIPE PR: (leave this empty)

# HIPE ????-decorators
[summary]: #summary

Explain how decorators work in agent-to-agent communication.

# Motivation
[motivation]: #motivation

Certain semantic patterns manifest over and over again in communication. For
example, all communication needs the pattern of testing the type of message
received. The pattern of identifying a message and referencing it later is likely
to be useful in a high percentage of all agent protocols that are ever written.
A pattern that associates messages with debugging/tracing/timing metadata is equally
relevant.  And so forth.

We need a way to convey metadata that embodies these patterns, without complicating
schemas, bloating core definitions, managing complicated inheritance hierarchies,
or confusing one another. It needs to be elegant, powerful, and adaptable.

# Tutorial
[tutorial]: #tutorial

A decorator is an optional chunk of JSON that conveys metadata. Decorators are not
declared in a core schema but rather supplementary to it. Decorators add semantic
content broadly relevant to messaging in general, and not so much tied to the
problem domain of a specific type of interaction.

You can think of decorators as a sort of [mixin](https://en.wikipedia.org/wiki/Mixin)
for agent-to-agent messaging. This is not a perfect analogy, but it is a good one.
Decorators in A2A also have some overlap (but not a direct congruence) with
[annotations in Java]( https://en.wikipedia.org/wiki/Java_annotation), [attributes in
C#](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/attributes/), 
and both [decorators](https://www.python.org/dev/peps/pep-0318/) and
[annotations](https://www.python.org/dev/peps/pep-3107/) in python.
 
### Simple Example
Imagine we are designing a protocol and associated messages to arrange meetings
between two people. We might come up with a `meeting_proposal` message that looks
like this:

```JSON
{
  "proposed_time": "2019-12-23 17:00"
  "proposed_place": "at the cathedral, Barfüsserplatz, Basel",
  "comment": "Let's walk through the Christmas market."
}
```

Now we tackle the `meeting_proposal_response` messages. Maybe we start with something
exceedingly simple, like:

```JSON
{
  "agree": true,
  "comment": "See you there!"
}
```

But we quickly realize that the asynchronous nature of messaging will expose a gap
in our message design: _if Alice receives two meeting proposals from Bob at the same
time, there is nothing to bind a response back to the specific proposal it addresses._

We could extend the schema of our messages so proposals contain an `id`, and responses
reference that `id`. This would work. However, it does not satsify the [DRY principle
of software design](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself), because
when we tackle the protocol for negotiating a purchase between buyer and seller next
week, we will need the same solution all over again. The result would be a proliferation
of schemas that all address the same basic need for associating request and response.
Worse, they might do it in different ways, cluttering the mental model for everyone
and making the underlying patterns less obvious.

What we want instead is a way to inject into any message the idea of a thread, such
that we can easily associate responses with requests, errors with the messages that
triggered them, and child interactions that branch off of the main one. This is the
subject of the [message threading HIPE](
https://github.com/hyperledger/indy-hipe/blob/7bd05ee7191d5175dd6606bb5851980076b310aa/text/message-threading/README.md),
and the solution is a pair of decorators. `@id` can *decorate* **any** message:

```JSON
{
  "@id": "e2987006-a18a-4544-9596-5ad0d9390c8b",
  "proposed_time": "2019-12-23 17:00"
  "proposed_place": "at the cathedral, Barfüsserplatz, Basel",
  "comment": "Let's walk through the Christmas market."
}
```
...and `@thread` can *decorate* any response:

```JSON
{
  "@thread": {"thid": "e2987006-a18a-4544-9596-5ad0d9390c8b"},
  "agree": true,
  "comment": "See you there!"
}
```
These chunks of JSON are defined independent of any particular message schema, but
are understood to be available in all schemas.

### Basic Conventions

Decorators are defined in HIPEs that document a general pattern such as [message threading](
https://github.com/hyperledger/indy-hipe/blob/7bd05ee7191d5175dd6606bb5851980076b310aa/text/message-threading/README.md)
or [message localization](https://github.com/hyperledger/indy-hipe/pull/64).
The documentation for a decorator explains its semantics and offers examples.

Decorators are recognized by name. The name must begin with the `@` character (which
is reserved in A2A messages for decorator use), and be a short, single-line string
suitable for use as a JSON attribute name.

Decorators may be simple key:value pairs `"@id": "e2987006-a18a-4544-9596-5ad0d9390c8b"`.
Or they may associate a key with a more complex structure:

```JSON
"@thread": {
  "thid": "e2987006-a18a-4544-9596-5ad0d9390c8b",
  "pthid": "0c8be298-45a1-48a4-5996-d0d95a397006",
  "seqnum": 0
}
```

Decorators should be thought of as optional and supplementary in that they embody a
pattern more general than the domain of a specific message type. Entities that handle
messages should treat *all* unrecognized fields as valid but meaningless, and decorators
are no exception. Thus, software that doesn't recognize a decorator should ignore it.

However, some messages may intend something tied so tightly to a decorator's semantics
that the decorator effectively becomes required. An example of this is the relationship
between a [general error reporting mechanism](
https://github.com/hyperledger/indy-hipe/blob/6a5e4fe2d7e14953cd8e3aed07d886176332e696/text/error-handling/README.md)
and the `@thread` decorator: it's not very helpful to report errors without the context
that a thread provides.

Because decorators are general by design and intent, we don't expect namespacing to be
a major concern. The community agrees on decorators that everybody will recognize, and
they acquire global scope upon acceptance. Their globalness is part of their utility.
Effectively, decorator names are like reserved words in a shared public language of
messages.

As a special rule, constructs from JSON-LD such as `@context` are pre-reserved in the
global decorator namespace, allowing them to retain their JSON-LD semantics without
the possibility of collisions and ambiguity.

Namespacing *is also* supported, as we may discover legitimate uses. When
namespaces are desired, dotted name notation is used, as in
`@mynamespace.mydecoratorname`. We may elaborate this topic more in the future.

### Decorator Scope

A decorator may be understood to decorate (add semantics) at several different scopes.
The discussion thus far has focused on __message decorators__, and this
is by far the most important scope to understand. But there are more possibilities.

Suppose we wanted to decorate an individual field. This can be done with a __field
decorator__, which is a sibling field to the field it decorates. The name of
decorated field is combined with a decorator suffix in dotted notation, as follows:

```JSON
{
  "note": "Let's have a picnic.",
  "note.@l10n": { ... }
}
```
In this example, taken from the localization pattern, `note.@l10n` decorates `note`.

Besides a single message or a single field, consider the following scopes as decorator
targets:

* **Message Family**: An decorator can be declared in documentation for the
  message family, explaining semantics that apply to all message instances in the
  family unless overridden at a narrower scope. This is not the same as declaring the
  decorator's *structure* to be part of the *schema* of a message family; this is saying
  that the field *values* in a concrete instance of a decorator applies to all instances
  of a message family. The localization pattern contemplates this usage as a way to
  declare default localization semantics. 
* [**Message Type**](https://github.com/hyperledger/indy-hipe/blob/master/text/0021-message-types/README.md):
  A decorator can be declared in the documentation on a specific message
  type. If this happens, semantics of the decorator on the message type should be
  understood as overriding or enriching the semantics of that same decorator on the
  parent message family, since the scope is becoming more specific.
* [**Message Thread**](http://bit.ly/2SL5kab) **or thread tree**: A participant in a
  thread could send a message containing nothing but the `@thread` with one or
  more additional decorators *inside* it. This should be viewed as a statement of semantics that
  apply to subsequent communications from the sender, on that thread, until further
  notice or until overridden at the scope of an individual message instance. (While
  powerful, applying a decorator to this scope may be a burden on receivers because
  it requires them to be stateful. Therefore this usage, though theoretically possible,
  may be undesirable. If community members want to explore this, they are encouraged
  to discuss broadly, first.)
* **Connection**. It is conceivable that Alice could bundle up a set of decorators
  and send them to Bob as a way of saying "Hey, Bob: unless/until subsequent interactions
  give you more specific semantics, here's a set of semantics (settings for our connection)
  that you should assume for all interactions." (This may or may not be useful. It introduces ambiguity--should settings declared
  at this scope override those at the scope of a message family or message type? It
  also adds a burden of remembering to another party; some of what informs the interaction
  isn't present in the bits that flow later on. Thus, this style of decorator is also
  left as a possibility for future exploration and is not actively supported at present.)

# Reference
[reference]: #reference

This section of this HIPE will be kept up-to-date with a list of globally accepted
decorators, and links to the HIPEs that define them.

* [`@type`](https://github.com/hyperledger/indy-hipe/blob/master/text/0021-message-types/README.md): identify a message type
* [`@id` and `@thread`](http://bit.ly/2SL5kab): provide request/reply and threading semantics
* [`@timing`](https://github.com/hyperledger/indy-hipe/pull/68): timestamps, expiration, elapsed time
* [`@trace`](https://github.com/hyperledger/indy-hipe/pull/60): collaborative debugging and monitoring
* [`@l10n`](https://github.com/hyperledger/indy-hipe/pull/64): localization support
 

# Drawbacks
[drawbacks]: #drawbacks

By having fields that are meaningful yet not declared in core schemas, we run the risk that
parsing and validation routines will fail to enforce details that are significant but invisible.
We also accept the possibility that interop may look good on paper, but fail due to
different understandings of important metadata.

We believe this risk will take care of itself, for the most part, as real-life usage
accumulates and decorators become a familiar and central part of the thinking for
developers who work with agent-to-agent communication.

# Rationale and alternatives
[alternatives]: #alternatives

There is ongoing work in the `#indy-semantics` channel on Rocket.Chat to explore the concept
of __overlays__. These are layers of additional meaning that accumulate above a __schema
base__. Decorators as described here are quite similar in intent. There are some subtle
differences, though. The most interesting is that decorators as described here may be
applied to things that are not schema-like (e.g., to a message family as a whole, or to
a connection, not just to an individual message).

We may be able to resolve these two worldviews, such that decorators are viewed as overlays
and inherit some overlay goodness as a result. However, it is unlikely that decorators
will change significantly in form or substance as a result. We thus believe the current
mental model is already HIPE-worthy, and represents a reasonable foundation for immediate
use.

# Prior art
[prior-art]: #prior-art

See references to similar features in programming languages like Java, C#, and Python,
mentiond above.

See also this series of blog posts about semantic gaps and the need to manage intent
in a declarative style: [ [Lacunas Everywhere](https://codecraft.co/2014/07/16/lacunas-everywhere/),
[Bridging the *Lacuna Humana*](https://codecraft.co/2014/07/21/bridging-the-lacuna-humana/),
[Introducing Marks](https://codecraft.co/2014/07/24/introducing-marks/), [Mountains,
 Molehills, and Markedness](https://codecraft.co/2014/07/28/mountains-molehills-and-markedness/) ]

# Unresolved questions
[unresolved]: #unresolved-questions

- Are we doing enough about namespacing and collision avoidance with JSON-LD?
- What should we do, if anything, about versioning decorators?
- What should we do, if anything, about applying decorators to stateful scopes
  like a connection or a thread?
