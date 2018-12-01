- Name: localized_messages
- Author: Daniel Hardman
- Start Date: 2018-11-30
- HIPE PR:

# Localized Messages
[summary]: #summary

Defines how to send an agent message in a way that facilitates interoperable
localization, so humans communicating through agents can interact without
natural language barriers.

# Motivation
[motivation]: #motivation

The primary use case for agent messages is to support automated processing,
as with messages that lead to credential issuance, proof exchange, and so
forth. Automated processing may be the *only* way that certain agents can
process messages, if they are IoT devices or pieces of software run by
organizations with no human intervention.

However, humans are also a crucial component of the agent ecosystem, and
many interactions have them as either a primary or a secondary audience. In
credential issuance, a human may need to accept terms and conditions from the
issuer, even if their agent navigates the protocol. Some protocols, like a
chat between friends, may be entirely human-centric. And in any protocol
between agents, a human may have to interpret errors.

When humans are involved, locale and potential translation into various
natural languages becomes important. Normally, localization is the concern
of individual software packages. However, in agent-to-agent communication,
the participants may be using different software, and the localization may
be a cross-cutting concern--Alice's software may need to send a localized
message to Bob, who's running different software. It therefore becomes useful
to explore a way to facilitate localization that allows interoperability
without imposing undue burdens on any implementer or participant.

# Tutorial
[tutorial]: #tutorial

Here we introduce some flexible and easy-to-use conventions. Software that
uses these conventions should be able to add localization value in several ways,
depending on needs.

### Suffixes on Field Names

The JSON object that embodies an agent message may contain many strings. Some
will be keys; others may be values. We assume that *keys* do not need to be localized,
as they will be interpreted by software. Among string *values*, some may be
locale-sensitive, while others may not. For example, consider the following
fictional message that proposes a meeting between Alice and Bob:

[![sample1.png](sample1.png)](sample1.json)

Here, the string value named `proposed_location` need not be changed, no matter what
language Bob speaks. But `note` might be worth localizing, in case Bob speaks
French instead of English. To facilitate this, we change the name of the `note`
field so it declares its localizable status, using the `_ltxt` suffix. This makes it
a __localizable field__. And we change its data type to be a JSON object that maps
locale codes to alternative string values. Locale codes use the same format as [Posix locales](
https://www.gnu.org/software/gettext/manual/html_node/Locale-Names.html#Locale-Names)
except that region codes are optional, charset is not specified, and [ISO 639-2](https://en.wikipedia.org/wiki/ISO_639-2)
or [ISO 639-3](https://en.wikipedia.org/wiki/ISO_639-3) language codes may be used
if the [ISO 639-1 language code](https://en.wikipedia.org/wiki/ISO_639-1) code is
inadequate. This gives us the following modified JSON:

[![sample2.png](sample2.png)](sample2.json)

Now, when Bob's agent receives this message, it can detect that the `note_ltxt` field
is localizable, and submit the string value `"Let's have a picnic."` to a machine
translation service, with source language = English, to translate the message to French.

Senders of messages that use this convention can provide any number of __localized
alternatives__ by mapping more locales to strings inside the JSON dictionary:

[![sample3.png](sample3.png)](sample3.json)

### Catalogs and Message Codes

In advanced usage, it may be desirable to identify a piece of text by a code that describes
its meaning, and to publish an inventory of these codes and their localized alternatives.
This may be helpful, for example, to track a list of common errors (think of symbolic constants
like `EBADF` and `EBUSY`, and the short explanatory strings associated with them, in Posix's
&lt;errno.h&gt;). By publishing in this way, software can provide rich localization support
for high-value messages it doesn't write. Also, the meaning of a message can
be searched on the web, even when no localized alternatives exist for a particular language.
And the message text in a default language can undergo minor variation without invalidating
translations or searches.

If this usage is desired, a special subfield named `code` may be included inside the map
of localized alternatives:

[![sample4.png](sample4.png)](sample4.json)

Note, however, that a code for a localized message is not useful unless it's accompanied
by context that tells where that code is defined. This context can be defined globally when a
a message family is specified (so that the catalog is fixed for all messages of a given type),
or inside a message using the `@msg_catalog` decorator. The decorator may appear at any level
in a message; wherever it appears, it overrides any message catalog specified at a more general
level. The value of `@msg_catalog` is a URI (ideally, a DID reference):

[![sample5.png](sample5.png)](sample5.json)

Seeing a message like the one above, a recipient could browse to the catalog's URI and
search for `cant-route-to-agent` to learn more. A dynamic set of localized alternatives
for the message might be offered.

# Drawbacks
[drawbacks]: #drawbacks

* This convention may be hard for some schema handlers or parsers to support, since it
  requires them to understand a special kind of field that renders as text but that
  has a value that's actually a JSON dict.

# Rationale and alternatives
[alternatives]: #alternatives

We could choose not to support this feature.

# Prior art
[prior-art]: #prior-art

Java's property bundle mechanism, Posix's gettext() function, and many other localization
techniques are well known. They are not directly applicable, mostly because they don't address
the need to communicate with software that may or may not be using the same underlying
mapping/localization mechanism.

# Unresolved questions
[unresolved]: #unresolved-questions

- Is there any need to support localization of numeric or date values, in addition to
  strings?