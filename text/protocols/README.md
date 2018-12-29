- Name: protocols
- Authors: Daniel Hardman <daniel.hardman@gmail.com>
- Start Date: 2018-12-28
- PR:

# HIPE ??00: Protocols
[summary]: #summary

Defines protocols in the context of agent-to-agent interactions,
and shows how they should be designed and documented.

# Motivation
[motivation]: #motivation

When we began exploring agent-to-agent interactions, we imagined that
interoperability would be achieved by formally defining message families.
We have since learned that, although a message family definition is
highly useful, it is not quite enough. We also need to formally define the
roles in an interaction, the possible states those roles can have, the way
state changes in response to messages, and the errors that may arise.

In addition, we realized that we need clear examples of how to define all
these things, so designs are consistent and robust.

# Tutorial
[tutorial]: #tutorial

### What is a protocol?

A __protocol__ is a recipe for a stateful interaction. Protocols are all
around us, and are so ordinary that we take them for granted. Each of the
following interactions is stateful, and has conventions that constitute
a sort of "recipe":

* Ordering food at a restaurant
* Buying a house
* Playing a game of chess, checkers, tic-tac-toe, etc.
* Bidding on an item in an online auction.
* Going through security at the airport when we fly
* Applying for a loan

Protocols are a major concern for SSI agents. Agents need a recipe for
stateful interactions like:

* Connecting with one another
* Requesting and issuing credentials
* Proving things using credentials
* Putting things in escrow (and taking them out again)
* Paying
* Reporting errors
* Negotiating
* Cooperative debugging

Protocols are *composable*--meaning that you can nest one inside another.
The protocol for asking someone to repeat their last sentence can occur
inside the protocol for ordering food at a restaurant. The protocol for
reporting an error can occur inside an agent protocol for issuing
credentials.

### Ingredients

An agent protocol has the following ingredients:

* _name_ and _version_
* _roles_
* _state_ and _sequencing rules_
* _events that can change state_ -- notably, _messages_
* _constraints that provide trust and incentives_

### How to define a protocol

To define a protocol, write a HIPE. The [tictactoe 1.0 protocol](
tictactoe-1.0/README.md) is attached to this HIPE as an example.

A protocol HIPE conforms to general HIPE patterns, but includes some
specific substructure:

##### HIPE title (name and version)

The title of the HIPE should include the official name of the protocol
and its version. Because protocol names are likely to be used in filenames
and URIs, they are conventionally lower-kebab-case, but are compared
case-insensitively and ignoring punctuation.
Typically, the name of the protocol and the name of
its associated message family are identical, and so are the versions.
In the [tictactoe 1.0 example](tictactoe-1.0/README.md), the protocol
name and message family name are both "tictactoe", and the protocol
version and message family version are both "1.0".

However, these may diverge (e.g., in a case where a protocol
uses the same messages but has new states or new constraints on when
messages can be sent and how they are processed). It is also possible
for a protocol to use more than one message family, as for example
when a protocol uses a generic [`ack`]( https://github.com/hyperledger/indy-hipe/pull/77)
or a [`problem-report`](https://github.com/hyperledger/indy-hipe/pull/65)).
Therefore, the association between a protocol name+version and a
message family name+version is weak, not strong.

[Semver](http://semver.org) rules apply in cascading fashion to versions
of protocols, message families, and individual message types. Individual
message types are versioned as part of a coherent message family, which
constitutes a [public API in the semver sense](https://semver.org/#spec-item-1).
An individual message type can add new optional fields, or deprecate
existing fields, [with only a change to its message family's minor
version](https://semver.org/#spec-item-7).
Similarly, a message family can add new message types with only a change
to the minor version. These are all backwards-compatible changes.

A protocol has a dependency on one or more message families, and should be
versioned accordingly. If it declares a dependency on message family Y
version 1.X, the protocol's version need not change when message family Y
evolves to 1.X+1; this is a backwards-compatible change from the protocol's
perspective, because parties using the protocol can use either Y 1.X or
Y 1.X+1 and remain interoperable. However, if the protocol uses a new
feature introduced in Y version 1.X+1, then this causes the protocol's
own version to be updated. If the usage of the new feature is optional in
the protocol, then the dependency update is a backwards-compatible change,
and the protocol's minor version gets updated. If the usage of the new
feature is required, then [the protocol's major version gets updated](
https://semver.org/#spec-item-8).

##### "Key Concepts" under "Tutorial"

This is the first subsection under "Tutorial". It is short--a paragraph or
two. It defines terms and describes the flow of the interaction at a very
high level. Key preconditions should be noted (e.g., "You can't issue a
credential until you have completed the _connection_ protocol first"), as
well as ways the protocol can start and end, and what can go wrong. The
section might also talk about timing constraints and other assumptions.
After reading this section, a developer should know what problem your
protocol solves, and should have a rough idea of how the protocol works in
its simpler variants.

##### "Roles" under "Tutorial"

This is the next subsection. It gives a formal name to the roles in the
protocol, says who and how many can play each role, and describes constraints
associated with those roles (e.g., "You can only issue a credential if you
have a DID on the public ledger"). The issue of qualification for roles can
also be explored (e.g., "The holder of the credential must be known to the
issuer").

The formal names for each role are important because they are used when
[agents discover one another's capabilities](
https://github.com/hyperledger/indy-hipe/pull/73); an agent doesn't
just claim that it supports a protocol; it makes a claim about which
*roles* in the protocol it supports. An agent that supports credential
issuance and an agent that supports credential holding may have very
different features, but they both use the _credential-issuance_ protocol.
By convention, role names use lower-kebab-case but are compared
case-insensitively and ignoring punctuation.

##### "States" under "Tutorial"

This section lists the possible states that exist for each role. It also
enumerates the events (often but not always messages) that can occur,
including errors, and what should happen to state as a result. A formal
representation of this information is provided in a _state machine matrix_.
It lists events as columns, and states as rows; a cell answers the
question, "If I am in state X (=row), and event Y (=column) occurs,
what happens to my state?" The [Tic Tac Toe example](tictactoe-1.0/README.md#states)
is typical. UML-style state machine diagrams are also good artifacts here.
(The matrix form is nice because it forces an exhaustive analysis of every
possible event. The diagram style is usually simpler to create and consume,
but may not consider possibilities that it should. We leave it up to
the community to settle on whether it wants just one of these, or both.)

The formal names for each state are important, as they are used in [`ack`s]( https://github.com/hyperledger/indy-hipe/pull/77)
and [`problem-report`s](https://github.com/hyperledger/indy-hipe/pull/65)).
By convention, state names use lower-kebab-case but are compared
case-insensitively and ignoring punctuation.

Some protocols have only one role, and thus only one state machine.
But in many protocols, different participants may have different state
machines. This section has been neglected in many early efforts at protocol
definition, and its omission is a big miss. Analyzing all possible states
and events for all roles leads to robustness; skipping the analysis leads
to fragility.

##### "Messages" under "Tutorial"

If there is a message family associated with this protocol, this
section describes each member of it. It should also note the names and
versions of messages from other message families that are used by the
protocol (e.g., an [`ack`]( https://github.com/hyperledger/indy-hipe/pull/77)
or a [`problem-report`](https://github.com/hyperledger/indy-hipe/pull/65)).
Typically this section is written as a narrative, showing each message
type in the context of an end-to-end sample interaction. All possible
fields may not appear; an exhaustive catalog is saved for the "Reference"
section.

Sample messages that are presented in the narrative should also be checked
in next to the markdown of the HIPE, in [Agent Plaintext format](
https://github.com/hyperledger/indy-hipe/blob/master/text/0026-agent-file-format/README.md#agent-plaintext-messages-ap).

##### "Constraints" under "Tutorial"

Many protocols have constraints that help parties build trust.
For example, in buying a house, the protocol includes such things as
commission paid to realtors to guarantee their incentives, title insurance,
earnest money, and a phase of the process where a home inspection takes
place. If you are documenting a protocol that has attributes like
these, explain them here. If not, the section can be omitted.

##### "Messages" under "Reference"

Unless the "Messages" section under "Tutorial" covered everything that
needs to be known about all message fields, this is where the data type,
validation rules, and semantics of each field in each message type are
details. Enumerating possible values, or providing ABNF or regexes is
encouraged. Following conventions such as [those for date-
and time-related fields](https://github.com/hyperledger/indy-hipe/pull/76)
can save a lot of time here.

Each message type should be associated with one or more roles in the 
protocol. That is, it should be clear which roles can send and receive
which message types.

##### "Examples" under "Reference"

This section is optional. It can be used to show alternate flows through
the protocol.

##### "Collateral" under "Reference"

This section is optional. It could be used to reference files, code,
relevant standards, oracles, test suites, or other artifacts that would
be useful to an implementer. In general, collateral should be checked in
with the HIPE.

##### "Localization" under "Reference"

If communication in the protocol involves humans, then localization of
message content may be relevant. Default settings for localization of
all messages in the protocol can be specified in an `l10n.json` file
described here and checked in with the HIPE. See ["Decorators at Message
Type Scope"](https://github.com/hyperledger/indy-hipe/blob/318f265d508a3ddf1da7d91c79ae4ae27ab9142b/text/localized-messages/README.md#decorator-at-message-type-scope)
in the [Localization HIPE](https://github.com/hyperledger/indy-hipe/pull/64).

##### "Message Catalog" under "Reference"

If the protocol has a formally defined catalog of codes (e.g., for errors
or for statuses), define them in this section. See ["Message Codes and
Catalogs"](https://github.com/hyperledger/indy-hipe/blob/318f265d508a3ddf1da7d91c79ae4ae27ab9142b/text/localized-messages/README.md#message-codes-and-catalogs)
in the [Localization HIPE](https://github.com/hyperledger/indy-hipe/pull/64).

# Reference
[reference]: #reference

The [Tic-Tac-Toe 1.0 protocol](
tictactoe-1.0/README.md) is attached to this HIPE as an example of a good
definition.

# Drawbacks
[drawbacks]: #drawbacks

This HIPE creates some formalism around defining protocols. It doesn't go
nearly as far as SOAP or CORBA/COM did, but it is slightly more demanding
of a protocol author than the familiar world of RESTful [Swagger/OpenAPI](
https://swagger.io/docs/specification/about/).

The extra complexity is justified by the greater demands that agent-to-agent
communications place on the protocol definition. (See notes in [Prior Art](#prior-art)
section for details.)

# Rationale and alternatives
[alternatives]: #alternatives

Some of the simplest A2A protocols could be specified in a Swagger/OpenAPI
style. This would give some nice tooling. However, not all fit into that
mold. It may be desirable to create conversion tools that allow Swagger
interop.   

# Prior art
[prior-art]: #prior-art

* [WSDL](https://www.w3.org/TR/2001/NOTE-wsdl-20010315): A web-centric
 evolution of earlier, RPC-style interface definition languages like
 [IDL in all its varieties](https://en.wikipedia.org/wiki/Interface_description_language)
 and [CORBA](https://en.wikipedia.org/wiki/Common_Object_Request_Broker_Architecture).
 These technologies describe a *called* interface, but they don't describe
 the caller, and they lack a formalism for capturing state changes, especiall
 by the caller. They are also out of favor in the programmer community at
 present, as being too heavy, [too fragile](
 https://codecraft.co/2008/07/29/decoupling-interfaces-as-versions-evolve-part-1/),
 or poorly supported by current tools.
* [Swagger/OpenAPI](https://swagger.io/docs/specification/about/): Overlaps
 about 60% with the concerns of protocol definition in agent-to-agent
 interactions. We like the tools and the convenience of the paradigm
 offered by OpenAPI, but where these two do not overlap, we have impedance.
 Agent-to-agent protocols must support more than 2 roles, or
 two roles that are peers, whereas RESTful web services assume just client
 and server--and only the server has a documented API.
 Agent-to-agent protocols are fundamentally asynchronous,
 whereas RESTful web services mostly assume synchronous request~response.
 Agent-to-agent protocols have complex considerations for diffuse trust, 
 whereas RESTful web services centralize trust in the web server.
 Agent-to-agent protocols need to support transports beyond HTTP, whereas
 RESTful web services do not. Agent-to-agent protocols are nestable, while
 RESTful web services don't provide any special support for that construct.
* [Pdef (Protocol Definition Language)](https://github.com/pdef/pdef): An alternative to Swagger.
* [JSON RPC](https://www.jsonrpc.org/specification): Defines how invocation of
 remote methods can be accomplished by passing JSON messages. However, the
 RPC paradigm assumes request/response pairs, and does not provide a way
 to describe state and roles carefully.
* [IPC Protocol Definition Language (IPDL)](https://developer.mozilla.org/en-US/docs/Mozilla/IPDL):
 This is much closer to agent protocols in terms of its scope of concerns
 than OpenAPI. However, it is C++ only, and intended for use within browser
 plugins. 

# Unresolved questions
[unresolved]: #unresolved-questions

- Should we write a Swagger translator?
