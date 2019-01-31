# 0001: Agents
- Author: Daniel Hardman <daniel.hardman@gmail.com>
- Start Date: 2017-11-01 (approx, backdated)
- PR: (leave this empty)
- Jira Issue: (leave this empty)

## Summary
[summary]: #summary

Provide a high-level introduction to the concepts of agents in
the self-sovereign identity ecosystem.

## Tutorial
[tutorial]: #tutorial

Managing an identity is complex. We need tools to help us.

In the physical world, we often delegate complexity to trusted proxies
that can help. We hire an accountant to do our taxes, a real estate
_agent_ and to help us buy a house, and a talent _agent_ to help us
pitch an album to a recording studio.

On the digital landscape, humans and organizations (and sometimes,
IoT things) cannot directly consume and emit bytes, store and manage
data, or perform the crypto that self-sovereign identity demands.
They need delegates--__agents__--to help. [Agents are a vital
dimension across which we exercise sovereignty over identity](
https://medium.com/evernym/three-dimensions-of-identity-bc06ae4aec1c).

### Essential Characteristics

When we use the term "agent" in this community, we more properly mean
"an agent of self-sovereign identity." Such an agent has three defining
characteristics:

1. It acts as a fiduciary on behalf of a single [identity owner](
https://docs.google.com/document/d/1gfIz5TT0cNp2kxGMLFXr19x1uoZsruUe_0glHst2fZ8/edit#heading=h.2e5lma3u6c9g)
(or, for agents of IoT things, a single _controller_). 
2. It holds keys that uniquely embody its delegated authorization.
3. It interacts using interoperable [agent-to-agent protocols](
https://github.com/hyperledger/indy-hipe/pull/69).

### Canonical Examples

* A mobile app that Alice uses to manage secrets and to [connect
to others](https://github.com/hyperledger/indy-hipe/pull/54) is an
agent for Alice.
* A cloud-based service that Alice uses to expose a stable endpoint
where other agents can talk to her is an agent for Alice.
* A server run by Faber College, allowing it to issue credentials
to its students, is an agent for Faber.

Agents can be big or small, complex or simple. They can be packaged
in various ways, and the variety in how they interact is huge. [Some
are more canonical than others](#less-canonical-examples). But all
share the [three essential characteristics](#essential-characteristics)
described above.

### How Agents Talk

[Agent-to-agent communication](x) (A2A), and the [protocols built atop
it](https://github.com/hyperledger/indy-hipe/pull/69) are each rich
subjects unto themselves. Here, we will stay very high-level.

Agents can speak over many different communication transports: HTTP(S)
1.x and 2.0, WebSockets, IRC, Bluetooth, AMQP, NFC, Signal, email, push
notifications to mobile devices, and more. However, all A2A is
message-based, and is secured by modern, best-practice public key
cryptography. _How_ messages flow over a transport may vary--but their
security and privacy toolset, their links to the [DIDs and DID Docs of
identity owners](https://w3c-ccg.github.io/did-spec/), and the ways
their messages are packaged and handled are standard. That's what makes
agents interoperable.

Because agents speak so many different ways, and because many of them
won't have a permanent, accessible point of presence on the network, they
can't all be thought of as web servers with a Swagger-compatible API
for request-response. The analog to an API construct for agents is
_protocols_. These are patterns for stateful interactions; they specify
things like, "If you want to negotiate a sale with an agent, send it a
message of type X. It will respond with a message of type Y or type Z,
or with an error message of type W. Repeat until the negotiation
finishes." Some interesting A2A protocols include the one where two
parties connect to one another to build a relationship, the one where
agents discover what protocols they each support, the one credentials
are issued, and the one where proof is requested and sent.
Hundreds of other protocols are being defined.

### How to Get an Agent

The average person or organization will get an agent by downloading it
from the app store, installing it with their OS package manager, or
subscribing to it as a service. A number of agent providers are
emerging in the marketplace. Some are governments, NGOs, or educational
institutions that offer agents for free; others are for-profit
ventures. If you'd like suggestions about ready-to-use agent offerings,
please describe what you're looking for in `#indy-agent` on
[chat.hyperledger.org](https://chat.hyperledger.org).

### How to Write an Agent

Although the availability of quality pre-packaged agents will crescendo,
the ecosystem is young in 2019. There is intense activity in the
community around building agents and the tools and processes that
enable them. Some of this work is happening in the [indy-agent repo
on github.com](https://github.com/hyperledger/indy-agent); other parts
are taking place in the [Sovrin Foundation](https://sovrin.org) or
other circles.

Some key questions that will help you 



## Reference
[reference]: #reference

### Optional Characteristics

Some attributes that are not technically necessary in agents
include:

* Has a wallet _(common, but not universal)_
* Establishes connections _(some may use only hard-coded connections)_
* Exchanges credentials and proofs _(some may not use these protocols)_
* Both listens and speaks _(some may only listen or only speak)_

### Categories of Agents

Agents can be grouped by various criteria.

### Less Canonical Examples

* A cron job that runs once a night at Faber, scanning a database
and revoking credentials that have changes status during the day,
is an agent for Faber. This is true even though it doesn't listen
for incoming messages (it only speaks [revocation protocol](
../0011-cred-revocation/README.md) to the ledger). In order to
speak that protocol, it must hold keys delegated by Faber, and it
is surely Faber's fiduciary.
* Operating system
* Device
* The [Sovrin](https://sovrin.org) MainNet is an agent for the
Sovrin community. It holds keys, is a
fiduc
* The Alexa in the home of the Jones family is not an agent for
either the Jones family or Amazon. It accepts delegated work from
anybody who talks to it (instead of a single controlling identity).
Although it interfaces with Amazon to download data and features,
it isn't Amazon's fiduciary, either. It doesn't hold keys that allow
it to represent its owner. The protocols it speaks are not interactions
with other agents, but with non-agent entities.
* An doorbell that emits a simple signal each time it is pressed is
not an agent. It doesn't represent a fiduciary or hold keys. (However,
a fancy IoT doorbell that reports to Alice's mobile agent using an
A2A protocol _would_ be an agent.)
* A microservice run by AcmeCorp to integrate with its vendors is
not an agent for either AcmeCorp or its vendors. This is because


## Drawbacks
[drawbacks]: #drawbacks

Why should we *not* do this?

## Rationale and alternatives
[alternatives]: #alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not
choosing them?
- What is the impact of not doing this?

## Prior art
[prior-art]: #prior-art

Discuss prior art, both the good and the bad, in relation to this proposal.
A few examples of what this can include are:

- Does this feature exist in other SSI ecosystems and what experience have
their community had?
- For other teams: What lessons can we learn from other attempts?
- Papers: Are there any published papers or great posts that discuss this?
If you have some relevant papers to refer to, this can serve as a more detailed
theoretical background.

This section is intended to encourage you as an author to think about the
lessons from other implementers, provide readers of your proposal with a
fuller picture. If there is no prior art, that is fine - your ideas are
interesting to us whether they are brand new or if they are an adaptation
from other communities.

Note that while precedent set by other communities is some motivation, it
does not on its own motivate an enhancement proposal here. Please also take
into consideration that Indy sometimes intentionally diverges from common
identity features.

## Unresolved questions
[unresolved]: #unresolved-questions

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
