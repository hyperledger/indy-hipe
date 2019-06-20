# 0017: Agent Message Structure
- Author: Daniel Bluhm <daniel.bluhm@sovrin.org>
- Start Date: June 25, 2018

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: (date of first submission or last status change)
- Status Note: (explanation of current status; if adopted, 
  links to impls or derivative ideas; if superseded, link to replacement)

## Summary
This HIPE describes Agent Messages, the messages exchanged between agents via "wire" messages.

## Motivation
Establishing an agent message structure for interoperability.

## Tutorial
### Agent Messages

Agent messages are the messages sent between agents through wire messages.

#### Structure

The following `json`-like object is a representation of the proposed agent message structure before being packaged and
sent over the transport layer or after it is received through the transport layer and unpackaged. However, using `json`
for messages is not necessarily part of this proposal.

```json
{
  "@type": "message_type",
  <other attributes as specified by type>
}
```

- The `@type` attribute is the only attribute required and is a type string as outlined by [0021: Message
  Types][message-types]. The value of type string must be a recognized type as defined by future HIPEs for message
  families. Additionally, the type attribute must always be visible after unpacking the message from the transport
  layer.
- All other attributes used in messaging are dictated by the message type following the guidelines
  given in [0021: Message Types][message-types]

## Reference
- A brief summary of Agent messages is given in [Stephen Curran's slides from the Agent Summit][agent-summit-slides].
- This structure has been discussed in community calls for agent development. Much of this discussion was originally
  collected and added to [this Google Doc][early-a2a-doc].

## Drawbacks
Up to this point, no drawbacks for this agent message structure have been identified.

## Rationale and alternatives
At this point, just having a message structure outlined will continue to facilitate development of agents. By
introducing this structure, necessary modifications will hopefully come to light as agent development continues.

## Prior art
- The structure formerly proposed included an `id` and generic `content` attributes in addition to the `type` attribute
  described as required here.

[message-types]: https://github.com/hyperledger/indy-hipe/tree/master/text/0021-message-types
[agent-summit-slides]: https://docs.google.com/presentation/d/1l-po2IKVhXZHKlgpLba2RGq0Md9Rf19lDLEXMKwLdco/edit#slide=id.g29a85e4573632dc4_48
[early-a2a-doc]: https://docs.google.com/document/d/1mRLPOK4VmU9YYdxHJSxgqBp19gNh3fT7Qk4Q069VPY8
