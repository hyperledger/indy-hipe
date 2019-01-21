- Name: admin-messages
- Author: Sam Curren <sam@sovrin.org>
- Start Date: 2019-01-19
- PR: (leave this empty)
- Jira Issue: (leave this empty)

# Summary
[summary]: #summary

Admin Messages are used for agent control and administration, not for communication with agents in other domains.

# Motivation
[motivation]: #motivation

Most cloud agents run headless. Admin messages are used by authorized agents to control the cloud agent. This ability is needed in the following situations:

- User administration of a headless cloud agent via an Admin Console.
- Controlling an enterprise cloud agent from a static client on a backend system.
- Scripting Cloud Agents during Demos.
- Triggering behavior and arranging state during testing.

Standardizing admin messages also allows for tool reuse in all these situations.

# Tutorial
[tutorial]: #tutorial

Admin messages are grouped into message families just like regular messages. 

An admin message family usually relates to a regular message family. By convention, the name of the admin message family should use the same name as the main message family, with the suffix of `_admin`. For example, the `connections` message family should have admin messages grouped into the `connections_admin` message family. Using the `_admin` suffix will make it easier to correctly apply permissions.

#### Permissions

Admin family use should be limited to those agents (full or static) that have been explicitly given permission to perform administrative functions. For many cases, those keys and allowed permissions will be specified in configuration or at run time.

#### Admin Console

The term Admin Console refers to software used by a human to perform remote administrative tasks on a headless cloud agent. The Admin Console functions as a static agent. Initial versions are browser based, but no restrictions prevent native apps from being created, or native apps adopting admin console behavior.

# Examples
[examples]: #examples

**Family: [trust_ping](https://github.com/hyperledger/indy-hipe/blob/68073995bd472f1bc95259ca5a2e269b912bcc5f/text/trust-ping/README.md)** 

Admin Family: trust_ping_admin

- send_trust_ping - instructs the agent to initiate a trust ping

Commentary: The new send_trust_ping admin messages allows for the following use cases:

- Agent Test Suite requests agent under test to initiate the trust ping in the sender role. Without this admin message, testing the agent's ability to initiate a trust ping (instead of just respond) would be impossible.
- User requests trust ping from admin console.
- Enterprise Cloud agent instructed to initiate trust_ping by enterprise backend system.

**Family: [Connections](https://github.com/hyperledger/indy-hipe/blob/9e0d5804118235ba73948b0f866ddda70026e21f/text/connection-protocol/README.md)**

Admin Family: connections_admin

- connection_list_request - request a list of connections
- connection_list - lists connections
- send_invite - instruct agent to send invite
- invite_sent - notice that invite was sent
- invite_received - notice that an invite was received
- send_request - instruct agent to send request
- request_sent - notice that a request was sent
- request_received - notice that a request was received
- send_response - instruct agent to send response
- response_sent - notice that a response was sent
- response_received - notice that a response was received

Commentary: There are more admin messages (11) than there are regular messages (3). This may be necessary due to the inherent complexity of protocol state.

# Drawbacks
[drawbacks]: #drawbacks

Potential security hole. By standardizing and being explicit, we have a better chance of not making mistakes.

# Alternatives
[alternatives]: #alternatives

- Administration via some other protocol. Now we have _two_ protocols.

# Prior art
[prior-art]: #prior-art

The community has already experimented with both admin via separate interface and admin messages. Multiple parties within the community have moved toward admin message families.

# Unresolved questions
[unresolved]: #unresolved-questions

- Can we make admin messages simpler?
- Should the convention of a `_admin` suffix be more than convention?
- What else can we do to minimize attack risk?
