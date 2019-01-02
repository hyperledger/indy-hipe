- Name: feature-discovery
- Author: Daniel Hardman
- Start Date: 2018-12-17

# feature-discovery 1.0
[summary]: #summary

Describes how agents can query one another to discover what protocols
they support.

# Motivation
[motivation]: #motivation

Though some agents will support just one protocol and will be
statically configured to interact with just one other party, many
exciting uses of agents are more dynamic and unpredictable. When
Alice and Bob meet, they won't know in advance what features are
supported by one another's agents. They need a way to find out.

# Tutorial
[tutorial]: #tutorial

This HIPE introduces a protocol for discussing the protocols an agent
can handle. The identifier for the message family used by this protocol is
`feature-discovery`, and the fully qualified URI for its definition is:

    did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/feature-discovery/1.0
    
### Roles

There are two roles in the `feature-discovery` protocol: `requester` and
`responder`. The requester asks the responder about the protocols it
supports, and the responder answers. Each role uses a single message type.

### States

This is a classic two-step request~response interaction, so it uses the
predefined state machines for any `requester` and `responder`:

[![state machines](state-machines.png)](https://docs.google.com/spreadsheets/d/1smY8qhG1qqGs0NH9g2hV4b7mDqrM6MIsmNI93tor2qk/edit)

### Messages
##### `request` Message Type

A `feature-discovery/request` message looks like this:

[![request](request.png)](request.json)

The `query` field may use the * wildcard. Usually this will be to
match a prefix.

Reuqest messages say, "Please tell me what your capabilities are with
respect to the protocols that match this string." This particular example
asks if another agent knows any 1.x versions of the [tictactoe protocol](
https://github.com/hyperledger/indy-hipe/blob/4a17a845da932609f1c6b7b8a4599bb686a1f440/text/protocols/tictactoe-1.0/README.md
).

Any agent may send another agent this message type at any time.
Implementers of agents that intend to support dynamic relationships
and rich features are *strongly* encouraged to implement support
for this message, as it is likely to be among the first messages
exchanged with a stranger.

##### `response` Message Type

A `feature-discovery/response` message looks like this:

[![response](response.png)](response.json)

The `protocols` field is a JSON object that contains zero or more keys that
match the query. Each key is a protocol version (fully qualified message
family identifier such as `did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/tictactoe/1.0`).
Its value is a JSON object that enumerates the roles the responding agent
can play in the associated protocol, and, optionally, the message types it
can *receive* (not send).

Response messages say, "Here are some protocols I know about that matched
your query, and some things I can do with each one."

##### Sparse Responses

Responses do not have to contain exhaustive detail. For example, the following
response is probably just as good:

[![simpler response](simpler-response.png)](simpler-response.json)

The reason why less detail probably suffices is that agents do not need to
know everything about one another's implementations in order to start an
interaction--usually the flow will organically reveal what's needed. For
example, the `outcome` message in the `tictactoe` protocol isn't needed
until the end, and is optional anyway. Alice can start a tictactoe game
with Bob and will eventually see whether he has the right idea about
`outcome` messages.

The empty `{}` in this response does not say, "I support no roles and no
message types in this protocol." It says, "I support the protocol but
I'm providing no detail about specific roles and messages."

Even an empty `protocols` map does not say, "I support no protocols
that match your query." It says, "I'm not telling you that I support any
protocols that match your query." An agent might not tell another that
it supports a protocol for various reasons, including: the trust that
it imputes to the other party based on cumulative interactions so far,
whether it's in the middle of upgrading a plugin, whether it's currently
under high load, and so forth. And responses to a `feature-discovery` request are
not guaranteed to be true forever; agents can be upgraded or downgraded,
although they probably won't churn in their protocol support from moment
to moment.

### Privacy Considerations

Because the regex in a `request` message can be very inclusive, the `feature-discovery`
protocol could be used to mine information suitable for agent fingerprinting,
in much the same way that browser fingerprinting works. This is antithetical
to the ethos of our ecosystem, and represents bad behavior. Agents should
use `feature-discovery` to answer legitimate questions, and not to build detailed
profiles of one another. However, fingerprinting may be attempted
anyway.

For agents that want to maintain privacy, several best practices are
recommended:

##### Do not always provide exhaustive detail in a response.

Patterns are easier to see in larger data samples. However, a pattern
of ultra-minimal data is also a problem, so be more forthcoming sometimes,
and less, others.

##### Consider adding some spurious details.

If a regex in a query could match multiple message families, then occasionally
you might add some made-up message family names as matches. If a regex
allows multiple versions of a protocol, then sometimes you might use some
made-up *versions*. And sometimes not.

##### Vary the format of responses.

Sometimes, you might prettify your agent plaintext message one way,
sometimes another.

##### Vary the order of keys in the `protocols` object.

If more than one key matches a query, do not always return them in
alphabetical order or version order. If you do return them in order,
do not always return them in ascending order.

##### Vary how you query, too.

How you ask questions may also be fingerprintable.
 
# Reference

### Localization
No message types in this protocol contain localized data. However, we
do define some error codes that can be localized. See next section.

### Message Catalog

If any agent wants to send [`problem-report`s](
https://github.com/hyperledger/indy-hipe/blob/6a5e4fe2d7e14953cd8e3aed07d886176332e696/text/error-handling/README.md#the-problem-report-message-type
) to complain about something related to `feature-discovery` issues, it should
ensure that [the following message catalog](catalog.json) is in scope:

[![error catalog for feature-discovery protocol](catalog.png)](catalog.json)

Note that `unsupported-protocol-or-version` is NOT sent when a query produces
empty results. However, it is declared here because we expect agents to
occasionally attempt a protocol that a remote party doesn't support. When
that happens, this is the error code to use.

When referencing this catalog, please be sure you have the correct
version. The official, immutable URL to this version of the catalog file
is:

    https://github.com/hyperledger/indy-hipe/blob/88352a556ddceaea2ad5d88384cd8eea3e4c82ed/text/agent-protocols/catalog.json

For more information, see the [Message catalog section of the localization
HIPE](https://github.com/hyperledger/indy-hipe/blob/95c6261dc6b857a36ceb348276a822dd730a5923/text/localized-messages/README.md#message-codes-and-catalogs).
      

# Drawbacks

# Rationale and alternatives

# Prior art

# Unresolved questions

- Do we want to support the discovery of features that are not protocol-related?
- Do we need to support a human comment in a query? (I think not, but just checking.)
- Do we need to support a quid-pro-quo (requesting agent also discloses)? Or
  would we say that what/how the requesting agent queries is an implicit
  disclosure? If the latter, does this need to be considered in privacy 
  best practices?