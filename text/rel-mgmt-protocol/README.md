# 00??: Relationship Management Protocol
- Authors: Daniel Hardman <daniel.hardman@gmail.com>, Devin Fisher <devin.fisher@evernym.com>, Sam Curren <sam@sovrin.org>
- Start Date: 2018-10-01
- PR: 

## Summary

Define a non-centralized protocol (that is, one that does not involve a common
store of state like a blockchain), whereby parties synchronize the state of
their shared relationship by direct communication with one another.

## Motivation

For Alice and Bob to interact, they must establish and maintain state.
This state includes all the information in a DID Document: endpoint, keys, and
associated authorizations.

The [Connection Protocol](https://github.com/hyperledger/indy-hipe/blob/b3f5c388/text/connection-protocol/README.md)
describes how these DID Docs are initially exchanged as a relationship is
built. However, its mandate ends when a connection is established. The
protocol described here focuses on how peers maintain their relationship
thereafter, as DID Docs evolve.

# Tutorial
[tutorial]: #tutorial

### Background Concepts

##### Relationship versus Non-Relationship State

The state that's managed by this protocol is only the state that embodies
relationship knowledge in a DID Doc. Plenty of other state may exist, such
as a history of credentials presented in both directions, a history of
other messages and interactions, rich policy configured in either
direction, and so forth. Such things are not managed in this protocol.
(TODO: see [this note](#applying-this-protocol-to-other-state) about
reusing the protocol for other problems.)

A particular type of state that may cause confusion is authorization
state. Alice may ask Bob to help her enforce spending limits on
her devices. This might involve a certain authorization state.
For example, maybe her phone is only authorized to spend
money up to $10 per day, whereas her laptop can spend up to $1000, and
three of her agents must agree to spend any amount greater than $1000.
This is a rich authorization policy, but it is not the type of authorization
in a DID Doc. Therefore, it is out of scope as well. Only authorizations
of the types enumerated [below](#authorization-types) are in scope.

##### Authentication versus Authorization

A manager, a teller, and a vice president may all be legitimate employees
of a bank. However, the actions that each is authorized to perform on
behalf of their employer may be different.

The `authentication` section of a DID Doc enumerates keys that can act as
the DID subject (what the DID identifies). When such a key is used, it is like proving that they are an
employee of the bank. A key from the `authentication` section of a DID Doc
is able to exercise the identity of the DID subject.

_But what is that key authorized to do?_
Bank tellers can transact business, but probably not announce the appointment
of a new manager. Bank vice presidents may be able to appoint managers or
tellers, but for safety reasons may not be allowed to handle money
directly.

Delegating specific privileges is the job of the `authorization` section.

##### Types of Changes

All of the following operations can be performed on a DID Doc, and must be
supported by the relationship management protocol:

* Adding, removing, or rotating keys
* Adding and removing key references from the `authentication` or
  `authorization` section
* Adding, removing, or reconfiguring endpoints

##### DID Doc Deltas

In traditional databases, the concept of a _transaction_ exists to
bundle changes in a way that guarantees that the whole set of changes either
succeeds or fails, as an indivisible unit. This allows funds to be
transferred out of one account, and into another--but never to be
lost in limbo with only one of the two transfers complete.

This same requirement exists in relationship management. Several
relationship __operations__ may need to be performed as a unit on a DID Doc.
For example, an old key may need to be retired, a new key may need to be
announced, and the new key may need to be given authorizations, all as
an atomic unit of change.

To facilitate this, the relationship management protocol deals in 
a larger unit of change than an individual operation. This is a
DID Doc __delta__, and it consists of a list of operations that must
be applied in order. For security reasons, all operations in a delta
must share a common authorization. This means that it is illegal for
key 1 to authorize part of the list, and for key 2 to authorize another
part. All keys must authorize the complete delta, so each authorizer
knows the full scope of the change.

### Roles

In a peer relationship, we would expect only one role: `peer`. And this is
the case, at a high level.

However, at another level of detail, peers are composed of agents, and agents
have interesting differences. Agents may have different responsibilities, 
different capabilities, and different authorizations. Some agents may share
the same [sovereign domain](
https://docs.google.com/document/d/1gfIz5TT0cNp2kxGMLFXr19x1uoZsruUe_0glHst2fZ8/edit#heading=h.pufsrf9ucjvv)
with one another, while others may not.

For most of this discussion, we will describe messages as being passed
between two or more entities that have the `peer` role. However, we will
occasionally dip into a lower level as we explain granular agent behavior.

### Message Family

The messages used to establish, maintain, and end a relationship are members of
the `connection` message family. This family is identified by the following DID
reference (a form of URI [TODO: hyperlink to def of DID reference in DID spec]):

    did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connection/1.0

Of course, subsequent evolutions of the message family will replace `1.0` with
an appropriate update per [semver](https://semver.org) rules.

The following messages are defined within this family: `join_us`, `leave_us`
`update_us`, `my_view`, `query_view`, `introduce`. [TODO: should connections
move into this family too?] An overview of each message type follows. The
[Reference](#reference) section of this HIPE contains a detailed explanation
of each field of each message; here in the Tutorial, we will focus on just
a rough description.
 
##### `join_us`

This message announces that the sender is now modeling an interaction in terms
of a peer relationship. In other words, the sender is joining a group called
"us". A `join_us` message is sent by each party, to all other parties that are
part of "us". In a pairwise relationship, that means from Alice to Bob--and,
to complete the relationship, from Bob back to Alice. In an n-wise relationship
such as between Doctor~Patient~Hospital, each party sends to all the other
parties.

    [TODO: This message needs to be reconciled against the connection protocol.
    Connecting is a subset of relationship management, but it has specialized
    requirements that the rest of the relationship management task doesn't need
    to worry about. What's described here would only work for cases where there's
    a pre-exiting connection point, but not a relationship. Would that apply
    to how we contact an institution's anywise DID and propose a relationship?
    Or to an n-wise case where only parts of the graph are connected, and these
    messages need to be sent to achieve closure? Or to introductions?
    It is possible that this message disappears entirely, and we just hyperlink
    to the Connection HIPE--but that the notion of "me" and "you" and "us"
    gets moved over there. For now, I'm going to leave this message in because
    it makes sense in the context of the rest of the message family.]

The `join_us` message announces the DID by which the sender intends to be known
in the relationship, and the endpoint and key(s) that other parties should use
in future interactions. As such, it comprises a sort of "genesis transaction"
for that party with respect to the relationship.

An initial `join_us` message from Alice to Bob might look like this:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/relmgmt/1.0/join_us",
  "@id": "e61586dd-f50e-4ed5-a389-716a49817207",
  "me": {
    "doc": {
      "@context": "https://w3id.org/did/v1",
      "id": "did:peer:EMmo7oSqQk1twmgLDRNjzC",
      "publicKey": [
        {"id": "routing", "type": "Ed25519Verkey2018",  "owner": "did:peer:EMmo7oSqQk1twmgLDRNjzC","publicKey": "8HH5gYEeNc3z7PYXmd54d4x6qAfCNrqQqEB3nS7Zfu7K"},
        {"id": "4", "type": "Ed25519Verkey2018",  "owner": "did:peer:EMmo7oSqQk1twmgLDRNjzC","publicKey": "V8Tt75FZ2ZTu4Ar5P8bBr3vXMguTw3U14S6mN2rxrDsY"},
        {"id": "6", "type": "Ed25519Verkey2018",  "owner": "did:peer:EMmo7oSqQk1twmgLDRNjzC","publicKey": "DjbU8jgf1MjGWu6hGwr4N4EoAfhfTjutjWc8fgdxb3QP"}
      ],
      "authentication": [
        {"type": "Ed25519Verkey2018", "publicKey": "ddid:peer:EMmo7oSqQk1twmgLDRNjzC#4"}
      ],
      "service": [
        {"type": "Agency", "serviceEndpoint": "did:sov:QN8nuLJ4Av1e1Cpu2MavT6" }
      ]
    }
  }, 
  "you": [],
  "us": {},
  "comment_ltxt": "Let's be friends. This is Alice."
}
```

Here, the value of the `me.doc` key is a DID Doc that establishes the initial state
of Alice with respect to Bob. `comment_ltxt` is optional and [follows the conventions of
localized fields](https://github.com/hyperledger/indy-hipe/blob/f67741ae5b06bbf457f35b95818bd2e9419767d7/text/localized-messages/README.md).
The `you` and `us` fields are discussed later.

Bob's normal response, also a `join_us` message, would be quite similar, except
that the `you` section would acknowledge Alice's previous message. It does
this in the `you.<Alice's peer DID>.latest` key (here, `you.did:peer:EMmo7oSqQk1twmgLDRNjzC.latest`)
by hashing the received DID Doc from Alice and reporting how many versions
of Alice's state Bob has seen:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/relmgmt/1.0/join_us",
  "@id": "49817207-f50e-4ed5-a389-716ae61586dd",
  "@thread": { "thid": "e61586dd-f50e-4ed5-a389-716a49817207", "seqnum": 0 },
  "me": {
    "doc": {
      "@context": "https://w3id.org/did/v1",
      "id": "did:peer:qQk1twjzCmEMgLDRNmo7oS",
      "publicKey": [
        {"id": "routing", "type": "Ed25519Verkey2018",  "owner": "did:peer:qQk1twjzCmEMgLDRNmo7oS","publicKey": "4x6qAfCNrqQqEB3nS7Zfu7K8HH5gYEeNc3z7PYXmd54d"},
        {"id": "1", "type": "Ed25519Verkey2018",  "owner": "did:peer:qQk1twjzCmEMgLDRNmo7oS","publicKey": "Ar5P8bBr3vXMguTw3U14S6mN2rxrDsYV8Tt75FZ2ZTu4"}
      ],
      "authentication": [
        {"type": "Ed25519Verkey2018", "publicKey": "ddid:peer:qQk1twjzCmEMgLDRNmo7oS#1"}
      ],
      "service": [
        {"type": "Agency", "serviceEndpoint": "did:sov:Av1e1Cpu2MavT6QN8nuLJ4" }
      ]
    }
  },
  "you": [
    "did:peer:EMmo7oSqQk1twmgLDRNjzC": { 
      "latest": {
        "sha256": "5B67C6528002FE929A228FE9F914C4B0A668E6AAEE38031BDEC6E2A0C0462D0D",
        "v": 1
      }
    } 
  ],
  "us": {},
  "comment_ltxt": "Hi, Alice. This is Bob."
}
```

[TODO: should "sha256" be a merkle root instead?]

This `join_us` message is known to be a response because of the use of [message threading](
https://github.com/hyperledger/indy-hipe/blob/7bd05ee7191d5175dd6606bb5851980076b310aa/text/message-threading/README.md).
However, even without `@thread`, this is implicitly a reply of sorts, because it acknowledges
Alice's state in the `you` section.

Once every party has joined a relationship, it is considered established. However, a pairwise
relationship can be upgraded to n-wise, or an n-wise relationship can add participants, by
having the new member issue a `join_us` message of their own, and by receiving acknowledgments
of the same.

##### `leave_us`

This message is used to announce that a party is abandoning the relationship. In a self-sovereign
paradigm, abandoning a relationship can be done unilaterally, and does not require formal
announcement. Indeed, sometimes a formal announcement is impossible, if one of the parties
is offline. So while using this message is encouraged and best practice, it is not mandatory.

A `leave_us` message from Alice to Bob looks like this:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/relmgmt/1.0/leave_us",
  "@id": "c17147d2-ada6-4d3c-a489-dc1e1bf778ab",
  "ack_requested": false,
  "comment_ltxt": "It's not about you. It's about me..."
}
```

If Bob receives a message like this, he should assume that Alice no longer considers
herself part of "us", and take appropriate action. This could include destroying
data about Alice that he has accumulated over the course of their relationship,
removing her peer DID and its public key(s) and endpoints from his wallet, and so
forth. The nature of the relationship, the need for a historical audit trail, regulatory
requirements, and many other factors may influence what's appropriate; the protocol
simply requires that the message be understood to have permanent termination semantics.

If `ack_requested` is `true`, then it is best practice for Bob to send a `my_view`
message with Alice's DID removed from the `you` field. This acknowledges that she is
no longer in the relationship from his perspective. This will make more sense
when the `my_view` message is described, later on--but here's what such a `my_view`
message would look like if Alice and Bob were in a pairwise relationship:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/relmgmt/1.0/my_view",
  "@thread": { "thid": "c17147d2-ada6-4d3c-a489-dc1e1bf778ab", "seqnum": 0 },
  "you": [],
  "comment_ltxt": "Bye. I'm not retaining anything about you."
}
```

##### `update_us`

This message is used to inform other(s) in the relationship that a change has
been proposed. If the change is in the `me` section, then the proposal should
always be accepted by others because it represents a key rotation or a similar
update that's under the unilateral control of the sender. The only exception
to this is if the proposed change is not properly authorized.

[TODO: talk about why we only want one change to be made at a time; you can't
just replace a whole DID Doc.]

If the change is in the `us` section, then it affects something that is
agreed by mutual consent, so the recipient can reject or accept it.

The JSON looks like this:

[TODO: insert Sam's JSON Diff idea? Or something else? Lovesh's POC assumed
granular transactions for each type of change, and I think Devin was assuming
that, too. This might argue for a bunch of new message types, each of which
processes a single type of update. However, it would be nice not to have to
update the spec for the message family if we invented a new type of info we
wanted to be able to update--but instead ot say that all changes flow through
a single update message with some sort of DID Doc diff. Diff allows more than
one change in a single step. That's sort of problematic, because if you allow
multiple changes in one step, and those changes require different authorizations,
you have to create a single role that has all power over DID Doc edits. We don't
want that--it would be a security disaster. But we don't technically need one
change per message to prevent it; we just need all the changes in a given
message to share a common authorization.]

[TODO: do we need timestamping anywhere in here, so we communicate *when* transitions
were applied?]

[TODO: How is signing handled? Do we need any signature other than what authcrypt
provides, so we can later display a signature to prove to the other party that our
view of their state is accurate? Merkle roots... Need to reconcile this against
Lovesh's microledger ideas...]

##### `my_view`

This message is used to respond to another party's assertions about changes
in a relationship. It says, "Okay, based on what you just said, here is my
view of the state of our relationship." It can contain `me` and `you` sections,
but it is normally sparse -- communicating just enough to identify the
change or state issue at hand.

For example, if Alice announces, in an `update_us` message with `@id: "abc"`, a key
rotation that changes the version of her DID Doc from 1 to 2, Bob can acknowledge
and accept the rotation with this `my_view` response:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/relmgmt/1.0/my_view",
  "@thread": { "thid": "abc", "seqnum": 0 },
  "you": [
    "did:peer:EMmo7oSqQk1twmgLDRNjzC": { 
      "latest": {
        "sha256": "914C4B0A668E6AAEE38031BDEC6E2A0C0462D0D5B67C6528002FE929A228FE9F",
        "v": 2
      }
    } 
  ],
  "comment_ltxt": "Okay, I'll expect you to use the new key."
}
```

(As with all other messages in this family, `comment_ltxt` is optional here, and is
only added to the example to make the meaning of the message obvious in this
narrative. What makes this message an acceptance is Bob asserting a state for Alice
matches what she sent--not the human-friendly comment.)

On the other hand, if Alice's key rotation is invalid, Bob can reject it
by sending a `problem-report` where `explain_l10n.code` = `update-not-authorized`:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/notification/1.0/problem-report",
  "@thread": { "thid": "abc", "seqnum": 0 },
  "explain_ltxt": "Update not authorized.",
  "explain_l10n": { "code": "update-not-authorized" }
}
```


##### `query_view`

A `query_view` message asks another party to describe what it knows about
the current state of a relationship. The simplest use case for this message
is to fetch another party's DID Doc. Suppose Alice wants to know how Bob
describes his own state (the basic DID resolution operation):

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/relmgmt/1.0/query_view",
  "@id": "adfd4f7a-afd8-4578-8233-6c8d231329fa",
  "view_of": [ "did:peer:qQk1twjzCmEMgLDRNmo7oS" ]
}
```

The response in this case is a `my_view` message that contains *both* a DID Doc
and a hash+version:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/relmgmt/1.0/my_view",
  
  "me": {
    "doc": {
      "@context": "https://w3id.org/did/v1",
      "id": "did:peer:qQk1twjzCmEMgLDRNmo7oS",
      "publicKey": [
        {"id": "routing", "type": "Ed25519Verkey2018",  "owner": "did:peer:qQk1twjzCmEMgLDRNmo7oS","publicKey": "4x6qAfCNrqQqEB3nS7Zfu7K8HH5gYEeNc3z7PYXmd54d"},
        {"id": "1", "type": "Ed25519Verkey2018",  "owner": "did:peer:qQk1twjzCmEMgLDRNmo7oS","publicKey": "Ar5P8bBr3vXMguTw3U14S6mN2rxrDsYV8Tt75FZ2ZTu4"}
      ],
      "authentication": [
        {"type": "Ed25519Verkey2018", "publicKey": "ddid:peer:qQk1twjzCmEMgLDRNmo7oS#1"}
      ],
      "service": [
        {"type": "Agency", "serviceEndpoint": "did:sov:Av1e1Cpu2MavT6QN8nuLJ4" }
      ]
    },
    "latest": {
      "sha256": "C6E2914C4B0A668EAEE38031BDE6AA0C0462D0D5B676528002FE9C29A228FE9F",
      "v": 2
    }
  }
}
```

Besides standard DID resolution, `query_view` can be used in more flexible ways. Alice
could ask Bob what he knows about *her* DID by changing `view_of` to contain her DID
rather than Bob's. If she did that, Bob's answer would come back in the `you` section
of the response. Alice could ask Bob for what he knows about both DIDs, in which case
the response would fill out both the `me` (Bob) and `you` (Alice) sections. In an
n-wise relationship among 4 siblings, Sibling #1 could ask Sibling #2 what her view
of Siblings 1, 3, and 4 is--and get back 3 entries under the `you` section.

### Multiple Agents and Cooperative Synchronization

The significance of the error situation described above, where Alice attempts a key
rotation that Bob must reject, is greater than might casually be assumed.
We tend to think of Alice and Bob as monolithic entities--but in fact, each may have
multiple agents that they use inside their respective sovereign domains. Ideally,
all of Alice's agents would share a coherent, perfectly synchronized view of the Alice~Bob
relationship, all the time. But the real world is messier.

One way this is true is in highly complex sovereign domains of institutions. An enterprise
might control dozens of rich agents running as daemons on its servers--and maybe hundreds
or thousands of static agents embodied in cron jobs, web hooks, and other forms of
automation. (For a discussion about "rich" and "static" agents, see [Agent Taxonomy](
https://docs.google.com/presentation/d/1ExQM_suu9MISrPanpK9sBGqVZFxf8pp4GvytcsKbkVM/edit#slide=id.g445a9ada60_0_21).)
Achieving robust synchronization in such a world is nearly impossible--especially with
low latency. In particular, static agents might not participate in any kind of sophisticated
intra-domain synchronization, because they are so simple and their state engines are so
primitive. This could lead to them having their authorization cancelled without
notification from internal sources. If so, they should get a `problem_report` from Alice
when they attempt to exercise privileges in the Alice~Bob relationship.

This challenge with imperfect propagation of relationship state also manifests in
the agents of an ordinary consumer. Suppose Alice owns a phone and a tablet. She
temporarily misplaces the phone, so she sends Bob a message with her tablet, removing
the phone's keys from the list of authorized keys. If Alice later finds the phone and
tries to use it to send Bob a message, she should get a `problem_report` message as
described above, explaining that this operation looks invalid from Bob's perspective.

Both of these examples show that the responsibility for communicating about the state
of a relationship is not easily partitioned. Bob should do what he can to tell his
agents about any changes he makes, *and also* about any changes that Alice makes.
And he should be helpful about informing Alice's agents if he knows more about the
relationship state than they do. Alice should do the same. If both engage in cooperative
synchronization, then the overall knowledge about relationship state may not be
perfect, but it will be good enough to function robustly.

The `query_view` and `my_view` messages help, here. If an agent receives a `problem_report`
announcing that it is out-of-date on its view of relationship state, the agent can follow
up with a `query_view` to see what state it lacks. Bob's static agent may be able to discover
and plug the gap by talking to Alice, even if Bob hasn't been able to update his own static
agent directly.

[TODO: go back and explain how we use Merkle roots with all messages in this family

##### Split Brain

If an agent rotates its keys in Bob's domain and then sends an announcement of that change
to Alice, only to have Alice reject it because the agent's view of state is stale [TODO:
go back and add in something in `update_us` that ties the update to a merkle root, such that
we can detect staleness even if the agent is still authorized...], then we have a problem:
the agent's old key might have been authorized, but the new one is not. And the agent has
thrown away the old key. This phenomenon of having independent actors evolve in parallel in
incompatible ways is called "the split brain problem" in database theory.

To avoid this problem, agents should not fully commit a key rotation on their side until
receiving an acknowledgement from the other side of the relationship. 

Note that split brain can still happen, despite an agent's best efforts to delay the commit,
if the agent on the other side doesn't deliver a `problem-report` as described above. And even
if it does, there is still a corner case where split brain can occur, because Bob's stale
agent's proposed change might be acknowledged by one of Alice's agents that, itself, has a
stale view of the relationship. Therefore, a `problem-report` about the staleness is sendable
at any point when the the split brain is detected. [TODO: describe algorithm to undo split brain
if detected.]

# Reference
[reference]: #reference

### State and Sequence Rules

[TODO: create state machine matrices that show which messages can be sent in
which states, causing which transitions]

### Message Type Detail

[TODO: explain every possible field of every possible message type]

### Localized Message Catalog

[TODO: define some localized strings that could be used with these messages,
in errors or at other generally useful points?]
