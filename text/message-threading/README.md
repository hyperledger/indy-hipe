- Name: message-threading
- Author: Daniel Bluhm <daniel.bluhm@sovrin.org>
- Start Date: 2018-08-03
- PR:
- Jira Issue:

# Summary
[summary]: #summary

Definition of the message threading decorator.

# Motivation
[motivation]: #motivation

Messages are usually part of interactions. By establishing a common specification for message threading, we can avoid
having to re-roll the same spec for each message family that needs it.

# Tutorial
[tutorial]: #tutorial

The following was pulled from [this
document](https://raw.githubusercontent.com/sovrin-foundation/protocol/master/janus/message-packaging.md) written by
Daniel Hardman and stored in the Sovrin Foundation's `protocol` repository.

## Threaded Messages
Message threading will be implemented as a decorator to messages, for example:
```json
{
    "@type": "did:example:12345...;spec/example_family/1.0/example_type",
	"@thread": {
	    "tid": 123456789,
		"ptid": 987654321,
		"mid": 2,
		"lmid": 1
	},
	"msg": "this is my message"
}
```

#### Thread object
A thread object has the following fields discussed below:

* `tid`: A mutually agreed identifier for the interaction.
* `mid`: A message ID unique to the `tid` and sender.
* `ptid`: An optional parent `tid`. Used when branching or nesting a new interaction off of an existing one.
* `lmid`: A reference to the last message the sender received from the receiver (Missing if it is the first message in
  an interaction).

#### Thread ID (`tid`)
Because multiple interactions can happen simultaneously, it's important to differentiate between them. This is done with
a Thread ID or `tid`.

The first message in an interaction should set a `tid` (128-bit random number) that the two parties use to keep track of
an interaction.

#### Message ID (`mid`)
Each message in an interaction needs a way to be uniquely identified. This is done with Message ID (`mid`). The first
message from each party has a `mid` of 0, the second message sent from each party is 1, and so forth. A message is
uniquely identified in an interaction by its `tid`, the sender DID, and the `mid`. The combination of those three parts
would be a way to uniquely identify a message.

#### Last Message ID (`lmid`)
In an interaction, it may be useful for the recipient of a message to know if their last message was received. A Last
Message ID or `lmid` can be included to help detect missing messages.

##### Example
As an example, Alice is an issuer and she offers a credential to Bob.

* Alice establishes a Thread ID, 7.
* Alice sends a CRED_OFFER, `tid`=7, `mid`=0. 
* Bob responded with a CRED_REQUEST, `tid`=7, `mid`=0, `lmid`=0.
* Alice sends a CRED, `tid`=7, `mid`=1, `lmid`=0.
* Bob responds with an ACK, `tid`=7, `mid`=1, `lmid`=1.

#### Nested interactions (Parent Thread ID or `ptid`)
Sometimes there are interactions that need to occur with the same party, while an existing interaction is in-flight.

When an interaction is nested within another, the initiator of a new interaction can include a Parent Thread ID
(`ptid`). This signals to the other party that this is a thread that is branching off of an existing interaction.

##### Nested Example
As before, Alice is an issuer and she offers a credential to Bob. This time, she wants a bit more information before she
is comfortable providing a credential.

* Alice establishes a Thread ID, 7.
* Alice sends a CRED_OFFER, `tid`=7, `mid`=0. 
* Bob responded with a CRED_REQUEST, `tid`=7, `mid`=0, `lmid`=0.
* **Alice sends a PROOF_REQUEST, `tid`=11, `ptid`=7, `mid`=0.**
* **Bob sends a PROOF, `tid`=11,`mid`=0, `lmid`=0.**
* Alice sends a CRED, `tid`=7, `mid`=1, `lmid`=0.
* Bob responds with an ACK, `tid`=7, `mid`=1, `lmid`=1.

All of the steps are the same, except the two bolded steps that are part of a nested interaction.

The thread object can be associated with a message in one of two way.

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

- Using a wrapping method for threading has been discussed but most seemed in favor of the annotated method. Any
  remaining arguments to be made in favor of the wrapping method?
