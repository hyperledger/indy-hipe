- Name: agent-test-suite
- Author: Daniel Hardman
- Start Date: 2018-05-17
- RFC PR: (leave this empty)
- Jira Issue: (leave this empty)

# Summary
[summary]: #summary

Defines the content and behavior of a test suite that evaluates
interoperability of Indy agents.

# Motivation
[motivation]: #motivation

The need for interoperability in SSI ecosystems is profound--much of the
value of SSI centers on interaction, and interaction requires different
pieces of technology to understand one another.

We will likely write multiple RFCs that touch on aspects of agent
interaction--but implementers need an oracle against which they can
verify compliance with specs and community practice. This RFC creates
such an oracle.

# Tutorial
[tutorial]: #tutorial

### Background Concepts

An agent is a piece of technology that holds keys and operates on the
digital landscape in behalf of its owner. Agents are not shared
services; they work for a single master. Agents can be embodied in
mobile apps, daemons, hardware, enterprise service buses, and many other
form factors.

Agents interact by sending and receiving messages. They can be viewed as
black boxes--as far as any other party in the ecosystem is concerned,
their implementation details are irrelevant. Only their sending and
receiving can be measured. This suggests that message interactions are
the locus of interoperability concerns, and the major thing to evaluate
in a test suite.

How messages are _transported_ may vary by circumstances--some agents
using http, others using Bluetooth, and still others using raw sockets
or smtp or proprietary protocols. Interoperability does depend to some
extent on intersecting transports, so our test suite needs to probe
that--but we should be more interested in the format of messages, the
semantics around their sending and receiving, and the behaviors they
evoke.

### Characterizing Interoperability

Some agents have very modest charters--listen for a signal and take a
single hard-coded action, maybe. Or just emit data. Other agents may be
very rich, with sophisticated AIs and policy engines, a broad charter,
and an array of communication strategies and partners.

Given this variety, the test suite evaluates compliance in a two-dimensional
matrix. One axis is the __mode of operation__ -- is the agent actively
initiating action, or passively listening, or both? This reflects in
agent space the human experience that many of us know, where it is
possible to understand a language without speaking it, or to speak
without listening. The other axis holds different __feature clusters__
-- which functional areas does the agent target? The set of feature clusters will likely grow over time.

![axes of evaluation](matrix.png)

Any given intersection in this matrix represents an __interop junction__.
Each junction may receive an __interop score__. The possible scores are:

  * __interoperable__: Passes all tests associated with this junction.
    Any two agents that are interoperable at a given junction should be
    able to interact freely within that junction.
  * __constrained__: Passes enough tests to enable a meaningful
    subset of interactions. The word "meaningful" is deliberately vague;
    this score always requires explanation about which subset is possible.
    Two agents that are both constrained at a junction may or may not
    find useful common ground.
  * __divergent__: Doesn't pass enough tests to have meaningful interop
    at this junction. This is the assumed or default score for all agents
    on all junctions, until proved otherwise by the test suite--and when
    results are reported, any junctions not described should be assumed
    to be divergent for that agent.

The set of all interop scores for a given agent constitutes its
__interop profile__.

# Reference
[reference]: #reference

Provide guidance for implementers, procedures to inform testing,
interface definitions, formal function prototypes, error codes,
diagrams, and other technical details that might be looked up.
Strive to guarantee that:

- Interactions with other features are clear.
- Implementation trajectory is well defined.
- Corner cases are dissected by example.

# Drawbacks
[drawbacks]: #drawbacks

Why should we *not* do this?

# Rationale and alternatives
[alternatives]: #alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not choosing them?
- What is the impact of not doing this?

# Prior art
[prior-art]: #prior-art

Discuss prior art, both the good and the bad, in relation to this proposal.
A few examples of what this can include are:

- Does this feature exist in other SSI ecosystems and what experience have their community had?
- For other teams: What lessons can we learn from other attempts?
- Papers: Are there any published papers or great posts that discuss this? If you have some relevant papers to refer to, this can serve as a more detailed theoretical background.

This section is intended to encourage you as an author to think about the lessons from other 
implementers, provide readers of your RFC with a fuller picture.
If there is no prior art, that is fine - your ideas are interesting to us whether they are brand new or if it is an adaptation from other languages.

Note that while precedent set by other ecosystems is some motivation, it does not on its own motivate an RFC.
Please also take into consideration that Indy sometimes intentionally diverges from common identity features.

# Unresolved questions
[unresolved]: #unresolved-questions

- What parts of the design do you expect to resolve through the RFC process before this gets merged?
- What parts of the design do you expect to resolve through the implementation of this feature before stabilization?
- What related issues do you consider out of scope for this RFC that could be addressed in the future independently of the solution that comes out of this RFC?
