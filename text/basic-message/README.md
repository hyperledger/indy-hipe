- Name: basic-message
- Author: Sam Curren (sam@sovrin.org)
- Start Date: (fill me in with today's date, 2019-01-16)
- PR: 

# Summary
[summary]: #summary

The BasicMessage message family describes a stateless, easy to support user message protocol. It has a single message type used to communicate.

# Motivation
[motivation]: #motivation

It is a useful feature to be able to communicate human written messages. BasicMessage is the most basic form of this written message communication, explicitly excluding advanced features to make implementation easier. 

# Tutorial
[tutorial]: #tutorial

#### Roles

There are two roles in this protocol: **sender** and **receiver**. It is anticipated that both roles are supported by agents that provide an interface for humans, but it is possible for an agent to only act as a sender (do not process received messages) or a receiver (will never send messages).

#### States

There are not really states in this protocol, as sending a message leaves both parties in the same state they were before.

#### Out of Scope

There are many useful features of user messaging systems that we will not be adding to this protocol message family. We anticipate the development of more advanced and full-featured message families to fill these needs. Features that are considered out of scope for this message family include:

- read receipts
- emojii responses
- typing indicators
- message replies (threading)
- multi-party (group) messages
- attachments

# Reference
[reference]: #reference

**Family**: did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/basicmessage/1.0/

**message**

- sent_time - timestamp in ISO 8601 UTC
- content - content of the user intended message as a string.

Example:

```json
{
    "@id": "123456780",
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/basicmessage/1.0/message",
    "sent_time": "2019-01-15 18:42:01Z",
    "content": "Your hovercraft is full of eels."
}
```



# Drawbacks
[drawbacks]: #drawbacks

- Creating this basicmessage may inhibit the creation of more advanced user messaging protocols.
- After more advanced user messaging protocols are created, the need to support this protocol may be annoying.

# Rationale and alternatives
[alternatives]: #alternatives

- Basic user messaging creates an easy useful feature in the early days of agent messaging.
- Even in the presence of better protocols, it can still be useful for basic devices or service messaging.

# Prior art
[prior-art]: #prior-art

BasicMessage has parallels to SMS, which led to the later creation of MMS and even the still-under-development RCS.

# Unresolved questions
[unresolved]: #unresolved-questions

- Should Internationalization be supported in this basic protocol? Perhaps only declaring language of sender?
- Receive receipts (NOT read receipts) may be implicitly supported by an ack decorator with pre-processing support. 

