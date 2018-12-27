- Name: message-id-and-threading
- Authors: Daniel Bluhm <daniel.bluhm@sovrin.org>, Sam Curren (sam@sovin.org), Daniel Hardman (daniel.hardman@gmail.com)
- Start Date: 2018-08-03
- PR: https://github.com/hyperledger/indy-hipe/pull/30

# Summary
[summary]: #summary

Definition of the message id and threading decorators.

# Motivation
[motivation]: #motivation

Referring to messages is useful in many interactions. A standard method of adding a message ID promotes good patterns in message families. When multiple messages are coordinated in a message flow, the threading pattern helps avoid having to re-roll the same spec for each message family that needs it.

# Tutorial
[tutorial]: #tutorial

## Message IDs

Message IDs are specified with the @id attribute. The sender of the message is responsible for creating the message ID, and any message can be identified by the combination of the sender and the message ID. Message IDs should be considered to be opaque identifiers by any recipients.

#### Message ID Requirements

- A short stream of characters matching regex `[-_./a-ZA-Z0-9]{8,64}` (Note the
  [special semantics of a dotted suffix on IDs](
  https://github.com/hyperledger/indy-hipe/blob/996adb82e61ab63b37a56254b92f57100ff8c8d9/text/message-tracing/README.md#message-ids),
  as described in the message tracing HIPE proposal)
- Should be compared case-sensitive (no case folding)
- Sufficiently unique
- UUID recommended

#### Example

```json
{
    "@type": "did:example:12345...;spec/example_family/1.0/example_type",
    "@id": "98fd8d72-80f6-4419-abc2-c65ea39d0f38",
    "example_attribute": "stuff"
}
```

The following was pulled from [this document](https://raw.githubusercontent.com/sovrin-foundation/protocol/master/janus/message-packaging.md) written by Daniel Hardman and stored in the Sovrin Foundation's `protocol` repository.

## Threaded Messages
Message threading will be implemented as a decorator to messages, for example:
```json
{
    "@type": "did:example:12345...;spec/example_family/1.0/example_type",
    "@id": "98fd8d72-80f6-4419-abc2-c65ea39d0f38",
    "@thread": {
        "thid": "98fd8d72-80f6-4419-abc2-c65ea39d0f38",
        "pthid": "1e513ad4-48c9-444e-9e7e-5b8b45c5e325",
        "myindex": 3,
        "lrecs": {"did:sov:abcxyz":1}
    },
    "example_attribute": "example_value"
}
```

#### Thread object
A thread object has the following fields discussed below:

* `thid`: The ID of the message that serves as the thread start.
* `pthid`: An optional parent `thid`. Used when branching or nesting a new interaction off of an existing one.
* `myindex`: A number that tells where this message fits in the sequence of all messages that *the current sender* has contributed to this thread.
* `lrecs`: Reports the highest `myindex` value that the sender has seen
  from other sender(s) on the thread. (This value is often missing if it
  is the first message in an interaction, but should be used otherwise,
  as it provides an implicit ACK.)

#### Thread ID (`thid`)
Because multiple interactions can happen simultaneously, it's important to
differentiate between them. This is done with a Thread ID or `thid`.

The Thread ID is the Message ID (`@id`) of the first message in the thread. The
first message may or may not declare the `@thread` attribute block; it
does not, but carries an
implicit `thid` of its own `@id`. 

#### My Index (`myindex`)
It is desirable to know how messages within a thread should be ordered.
However, it is very difficult to know with confidence the absolute
ordering of events scattered across a distributed system. Alice and Bob
may each *send* a message before receiving the other's response, but be
unsure whether their message was *composed* before the other's.
Timestamping cannot resolve an impasse. Therefore, there is no
unified absolute ordering of all messages within a thread--but there
*is* an ordering of all messages emitted by a each participant.

In a given thread, the first message from each party has a `myindex` value
of 0, the second message sent from each party has a `myindex` value of 1,
and so forth. Note that *both* Alice and Bob use 0 and 1, without regard
to whether the other party may be known to have used them. This gives a
strong ordering with respect to each party's messages, and it means that
any message can be uniquely identified in an interaction by its `thid`,
the sender DID and/or key, and the `myindex`.

#### Last Received (`lrecs`)
In an interaction, it may be useful for the recipient of a message to
know if their last message was received. A Last Received or `lrecs` value
addresses this need, and could be included as a best practice to help
detect missing messages.

In the example above, if Alice is the sender, and Bob is identified by
`did:sov:abcxyz`, then Alice is saying, "Here's my message with
index 3 (`myindex`=3), and I'm sending it in response to your message
1 (`lrecs: {<bob's DID>: 1}`. Apparently Alice has been more chatty than
Bob in this exchange.

The `lrecs` field is plural to acknowledge the possibility of multiple
parties. In [pairwise](
https://docs.google.com/document/d/1gfIz5TT0cNp2kxGMLFXr19x1uoZsruUe_0glHst2fZ8/edit#heading=h.eurb6x3u0443)
interactions, this may seem odd. However, [n-wise](
 https://docs.google.com/document/d/1gfIz5TT0cNp2kxGMLFXr19x1uoZsruUe_0glHst2fZ8/edit#heading=h.cn50pi7diqgj)
interactions are possible (e.g., in a doctor ~ hospital ~ patient n-wise
relationship). Even in pairwise, multiple agents on either side may introduce other
actors. This may happen even if an interaction is designed to be 2-party (e.g., an
intermediate party emits an error unexpectedly).

In an interaction with more parties, the `lrecs` object has a key/value pair
for each `actor`/`myindex`, where `actor` is a DID or a key for an agent:

```json
"lrecs": {"did:sov:abcxyz":1, "did:sov:defghi":14}
```

Here, the `lrecs` fragment makes a claim about the last `myindex`
that the sender observed from `did:sov:abcxyz` and `did:sov:defghi`. The sender of
this fragment is presumably some other DID, implying that 3 parties are participating.
Any parties unnamed in `lrecs` have an undefined value for `lrecs`.
This is NOT the same as saying that they have made no observable contribution to the
thread. To make that claim, use the special value `-1`, as in:

```json
"lrecs": {"did:sov:abcxyz":1, "did:sov:defghi":14, "did:sov:jklmno":-1}
```

##### Example
As an example, Alice is an issuer and she offers a credential to Bob.

* Alice sends a CRED_OFFER as the start of a new thread, `@id`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `myindex`=0. 
* Bob responds with a CRED_REQUEST, `@id`=&lt;uuid2&gt;, `thid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `myindex`=0, `lrecs:{alice:0}`.
* Alice sends a CRED, `@id`=&lt;uuid3&gt;, `thid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `myindex`=1, `lrecs:{bob:0}`.
* Bob responds with an ACK, `@id`=&lt;uuid4&gt;, `thid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `myindex`=1, `lrecs:{alice:1}`.

#### Nested interactions (Parent Thread ID or `pthid`)
Sometimes there are interactions that need to occur with the same party, while an
existing interaction is in-flight.

When an interaction is nested within another, the initiator of a new interaction
can include a Parent Thread ID (`pthid`). This signals to the other party that this
is a thread that is branching off of an existing interaction.

##### Nested Example
As before, Alice is an issuer and she offers a credential to Bob. This time, she wants a bit more information before she is comfortable providing a credential.

* Alice sends a CRED_OFFER as the start of a new thread, `@id`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `myindex`=0. 
* Bob responds with a CRED_REQUEST, `@id`=&lt;uuid2&gt;, `thid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `myindex`=0, `lrecs:{alice:0}`.
* **Alice sends a PROOF_REQUEST, `@id`=&lt;uuid3&gt;, `pthid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `myindex`=0.** Note the subthread, the parent thread ID, and the reset `myindex` value.
* **Bob sends a PROOF, `@id`=&lt;uuid4&gt;, `thid`=&lt;uuid3&gt;,`myindex`=0, `lrecs:{alice:0}`.**
* Alice sends a CRED, `@id`=&lt;uuid5&gt;, `thid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `myindex`=1, `lrecs:{bob:0}`.
* Bob responds with an ACK, `@id`=&lt;uuid6&gt;, `thid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `myindex`=1, `lrecs:{alice:1}`.

All of the steps are the same, except the two bolded steps that are part of a nested interaction.

#### Implicit Threads

Threads reference a Message ID as the origin of the thread. This allows _any_ message to be the start of a thread, even if not originally intended. Any message without an explicit `@thread` attribute can be considered to have the following `@thread` attribute implicitly present.

```
"@thread": {
    "thid": <same as @id of the outer message>,
    "myindex": 0
}
```

#### Implicit Replies

A message that contains a `@thread` block with a `thid` different from the outer
message `@id`, but no `myindex` is considered an implicit reply. Implicit replies
have a `myindex` of `0` and an `lrecs:{other:0}`. Implicit replies should only be
used when a further message thread is not anticipated. When further messages in the
thread are expected, a full regular `@thread` block should be used.

Example Message with am Implicit Reply:

```json
{
    "@id': "<@id of outer message>",
    "@thread": {
    	"thid": "<different than @id of outer message>"
	}
}
```
Effective Message with defaults in place:
```json
{
    "@id': "<@id of outer message>",
    "@thread": {
    	"thid": "<different than @id of outer message>"
    	"myindex": 0,
    	"lrecs": { "DID of sender":0 }
	}
}
```


# Reference

[reference]: #reference

- [Message Packaging document from Sovrin Foundation Protocol Repo](https://raw.githubusercontent.com/sovrin-foundation/protocol/master/janus/message-packaging.md)
- [Very brief summary of discussion from Agent Summit on Decorators](https://docs.google.com/presentation/d/1l-po2IKVhXZHKlgpLba2RGq0Md9Rf19lDLEXMKwLdco/edit#slide=id.g29a85e4573632dc4_58)

# Drawbacks
[drawbacks]: #drawbacks

Why should we *not* do this?

# Rationale and alternatives
[alternatives]: #alternatives

- Implement threading for each message type that needs it.

# Prior art
[prior-art]: #prior-art

If you're aware of relevant prior-art, please add it here.

# Unresolved questions
[unresolved]: #unresolved-questions

- Using a wrapping method for threading has been discussed but most seemed in favor of the annotated method. Any remaining arguments to be made in favor of the wrapping method?
