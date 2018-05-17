- Name: agent-test-suite-v1
- Author: Daniel Hardman
- Start Date: 2018-05-17
- RFC PR: (leave this empty)
- Jira Issue: (leave this empty)

# Summary
[summary]: #summary

Defines the content and implementation of a test suite that evaluates
interoperability of Indy agents. The general behavioral contract of
the test suite is defined in an associated RFC. (These two pieces of
content are divided so they can be versioned separately.)

# Reference
[reference]: #reference

## Feature Clusters

#### core.active

##### core.active.trust_ping_anon

Emit simple text such as "hello, world" as 
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
