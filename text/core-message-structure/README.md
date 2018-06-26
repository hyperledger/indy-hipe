- Name: core-message-structure
- Author: Daniel Bluhm <daniel.bluhm@sovrin.org>
- Start Date: June 25, 2018
- PR:
- Jira Issue:

# Summary
[summary]: #summary

This HIPE describes the core message structure for agent-to-agent communication.

# Motivation
[motivation]: #motivation

Establishing a core message structure will allow developers implementing agents to ensure interoperability in at least
the general structure of messages.

# Tutorial
[tutorial]: #tutorial

The following `json`-like object is a representation of the proposed core message structure before being packaged and
sent over the transport layer or after it is received through the transport layer and unpackaged. However, using `json`
for messages is not necessarily part of this proposal.

```json
{
  "id": "identifier/DID/nonce",
  "type": "URN message type",
  "message": {}
}
```

- The id attribute is required and needs to be either the DID of the sender that is a pairwise identifier in an
  established connection, a nonce used in establishing a connection, or another similar identifier used in a different
  custom message exchange.
- The type attribute is required and is a type string as outlined by a planned HIPE for message types.
- The message attribute is required or optional depending upon the value of the type attribute and would contain the
  contents specified in the definition of the message type.


# Reference
[reference]: #reference

This structure has been discussed in community calls for agent development. Much of this discussion has been collected
and added to [this Google Doc](https://docs.google.com/document/d/1mRLPOK4VmU9YYdxHJSxgqBp19gNh3fT7Qk4Q069VPY8).

# Drawbacks
[drawbacks]: #drawbacks

Up to this point, no drawbacks for this core message structure have been identified.

# Rationale and alternatives
[alternatives]: #alternatives

At this point, just having a message structure outlined will continue to facilitate development of agents. By
introducing this structure, necessary modifications will hopefully come to light as agent development continues.

# Prior art
[prior-art]: #prior-art

I'm sure that Evernym and BC Gov. have been following a convention similar to that which is proposed here; comments from
those who have already implemented differing message structures are especially encouraged to comment on differences and
their advantages or disadvantages.
