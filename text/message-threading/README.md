- Name: message-id-and-threading
- Authors: Daniel Bluhm <daniel.bluhm@sovrin.org>, Sam Curren (sam@sovin.org)
- Start Date: 2018-08-03
- PR:
- Jira Issue:

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

- Not to exceed 64 characters
- Sufficiently Unique
- UUID recommended

#### Example

```json
{
    "@type": "did:example:12345...;spec/example_family/1.0/example_type",
    "@id": "98fd8d72-80f6-4419-abc2-c65ea39d0f38",
    "example_attribute": "stuff"
}
```

The following was pulled from [this
document](https://raw.githubusercontent.com/sovrin-foundation/protocol/master/janus/message-packaging.md) written by
Daniel Hardman and stored in the Sovrin Foundation's `protocol` repository.

## Threaded Messages
Message threading will be implemented as a decorator to messages, for example:
```json
{
    "@type": "did:example:12345...;spec/example_family/1.0/example_type",
    "@id": "98fd8d72-80f6-4419-abc2-c65ea39d0f38",
    "@thread": {
        "tid": "98fd8d72-80f6-4419-abc2-c65ea39d0f38",
        "ptid": "1e513ad4-48c9-444e-9e7e-5b8b45c5e325",
        "mid": 2,
        "lmid": 1
    },
    "msg": "this is my message"
}
```

#### Thread object
A thread object has the following fields discussed below:

* `tid`: The ID of the message that serves as the thread start.
* `mid`: A message sequence number unique to the `tid` and sender.
* `ptid`: An optional parent `tid`. Used when branching or nesting a new interaction off of an existing one.
* `lsid`: A reference to the last message the sender received from the receiver (Missing if it is the first message in an interaction).

#### Thread ID (`tid`)
Because multiple interactions can happen simultaneously, it's important to differentiate between them. This is done with a Thread ID or `tid`.

The first message in an interaction should set a `tid` (128-bit random number) that the two parties use to keep track of an interaction.

#### Message ID (`mid`)
Each message in an interaction needs a way to be uniquely identified. This is done with Message ID (`mid`). The first message from each party has a `mid` of 0, the second message sent from each party is 1, and so forth. A message is uniquely identified in an interaction by its `tid`, the sender DID, and the `mid`. The combination of those three parts would be a way to uniquely identify a message.

#### Last Message ID (`lmid`)
In an interaction, it may be useful for the recipient of a message to know if their last message was received. A Last Message ID or `lmid` can be included to help detect missing messages. On the first message of a thread, this is omitted.

##### Example
As an example, Alice is an issuer and she offers a credential to Bob.

* Alice establishes a Thread ID, 7.
* Alice sends a CRED_OFFER, `tid`=7, `mid`=0. 
* Bob responded with a CRED_REQUEST, `tid`=7, `mid`=0, `lmid`=0.
* Alice sends a CRED, `tid`=7, `mid`=1, `lmid`=0.
* Bob responds with an ACK, `tid`=7, `mid`=1, `lmid`=1.

#### Nested interactions (Parent Thread ID or `ptid`)
Sometimes there are interactions that need to occur with the same party, while an existing interaction is in-flight.

When an interaction is nested within another, the initiator of a new interaction can include a Parent Thread ID (`ptid`). This signals to the other party that this is a thread that is branching off of an existing interaction.

##### Nested Example
As before, Alice is an issuer and she offers a credential to Bob. This time, she wants a bit more information before she is comfortable providing a credential.

* Alice establishes a Thread ID, 7.
* Alice sends a CRED_OFFER, `tid`=7, `mid`=0. 
* Bob responded with a CRED_REQUEST, `tid`=7, `mid`=0, `lmid`=0.
* **Alice sends a PROOF_REQUEST, `tid`=11, `ptid`=7, `mid`=0.**
* **Bob sends a PROOF, `tid`=11,`mid`=0, `lmid`=0.**
* Alice sends a CRED, `tid`=7, `mid`=1, `lmid`=0.
* Bob responds with an ACK, `tid`=7, `mid`=1, `lmid`=1.

All of the steps are the same, except the two bolded steps that are part of a nested interaction.

The thread object can be associated with a message in one of two way.

#### Implicit Threads

Threads reference a Message ID as the origin of the thread. This allows _any_ message to be the start of a thread, even if not originally intended. Any message without an explicit `@thread` attribute can be considered to have the following `@thread` attribute implicitly present.

```
"@thread": {
    "tid": <same as @id of the outer message>,
    "mid": 0
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
- Should message be changed to sequence in the thread block, as in sid (sequence id) and lsid (last seen sequence id) to avoid confusion with the outer message id?
