- Name: agent-test-suite-v1
- Author: Daniel Hardman
- Start Date: 2018-05-17
- HIPE PR: (leave this empty)
- Jira Issue: (leave this empty)

# HIPE 0016-agent-test-suite-v1
[summary]: #summary

Defines the content and implementation of a test suite that evaluates
interoperability of Indy agents.

##### Related HIPEs

This is a test suite __content HIPE__. It is intended to satisfy
the common behavioral contract defined in a seprate test suite 
__interface HIPE__. (These two types of spec are divided so they
can be versioned and standardized separately.)

![interface HIPEs vs. content HIPEs](interface-and-content.png)

# Reference
[reference]: #reference

What follows is a list of tests, organized into __feature clusters__,
to exercise the interoperability of agents. Each test has a canonical
name and a description that describes how an agent passes the test.

A reference implementation of this suite is attached to the HIPE;
see [suite.py](suite.py).

## Feature Clusters

### core.passive

This is the most basic feature cluster in the test suite; it tests
that agents listening passively understand messages that they receive,
and that they respond in expected ways.

##### core.passive.report_recognized_interop

Upon receiving an auth_crypt'ed [message of type `agent-metadata-request`](
../agent-test-suite-interface/README.md#agent-metadata-request
), where the type of requested metadata is an [interop profile](
../agent-test-suite-interface/README.md#interop-profile-json
) and the URI of the interop profile is the URI of this HIPE,
reply with a valid interop profile.

<blockquote>
(Should we have an anon_crypt'ed variant of this test? Different agents
may make different decisions about whether to report interop to anonymous
versus authenticated parties...)

(Should we topicalize the metadata request, and then test topicalized response?)
</blockquote>

##### core.passive.report_unrecognized_interop

Upon receiving a [message of type `agent-metadata-request`](
../agent-test-suite-interface/README.md#agent-metadata-request
), where the type of requested metadata is an [interop profile](
../agent-test-suite-interface/README.md#interop-profile-json
) and the URI of the interop profile is `http://example.com/no-such-URI`,
reply with an empty interop profile, indicating that the agent
provides nothing but divergence from any test suite at that URI.

##### core.passive.reply_with_error

Upon receiving a message of an unrecognized type, reply with a graceful
error using error code E_UNRECOGNIZED_MESSAGE_TYPE.

##### core.passive.trust_ping

Upon receiving a message of type `trust-ping`, reply with a message of
type `trust-ping-response`.

##### core.passive.new_connection_request_accept

Test fixture sends [setup instructions over the `agact` backchannel](
../agent-test-suite-interface/README.md#setup-and-teardown
) that look like this:

```json
{
  "on-next-message": [
    {"connection-request": "accept"}
  ]
}
```

This tells the agent to accept the next connection request--or to at least
pretend to, for the purpose of the test.

Once preconfigured in this way, upon receiving an anon_crypt'ed message of
type `connection-request`, reply with a message of type `connection-accepted`.

##### core.passive.new_connection_request_reject

Test fixture sends [setup instructions over the `agact` backchannel](
../agent-test-suite-interface/README.md#setup-and-teardown
) that look like this:

```json
{
  "on-next-message": [
    {"connection-request": "accept"}
  ]
}
```

Once setup, upon receiving an anon_crypt'ed message of type `connection-request`,
reply with a message of type `connection-rejected`.

##### core.passive.redundant_connection_request_reject

<blockquote>
(Send a connection request that's redundant because we already have a
connection to the requesting party. Do we need this? If so, what should
be the defined behavior?)
</blockquote>

### core.active

##### core.active.trust_ping_anon

Send a trust ping that's anon_encrypt'ed.

##### core.active.trust_ping_authenticated

Send a trust ping that's auth_encrypt'ed.

##### core.active.new_connection_request

Send a connection request.

##### core.active.request_recognized_interop

Send an interop request for this test suite.

### cred

<blockquote>
This suite probably has to be subdivided by role (issuer, holder),
and by active vs. passive.
</blockquote>

##### cred.cred_offer_free

Offer a credential that has no price.

##### cred.issue_free

Issue a credential that has no price.

##### cred.deny_issue_bad_proof_of_correctness

Refuse to issue a credential because requester doesn't prove correctness
(tries to embed data that issuer doesn't want to allow).

##### cred.deny_issue_unpaid

Refuse to issue a credential because requester hasn't paid for it.

##### cred.request_credential_free

Provide a correct cred request to enable issuance.

##### cred.negotiate_price

Dicker on price of issued credentials.

##### cred.negotiate_terms

Dicker on terms of credential use.

##### cred.negotiate_content

Dicker on content of offered credential.

### proof

<blockquote>
This suite probably has to be subdivided by role (prover, verifier),
and by active vs. passive.
</blockquote>

##### proof.proof_offer
##### proof.active.present_valid
##### proof.passive.accept_presented
##### proof.passive.rejected_presented
##### proof.active.present_invalid
Present a proof that doesn't match the requested criteria.
##### proof.deny_issue_bad_proof_of_correctness
##### proof.deny_issue_unpaid
##### proof.request_proof_possible
As verifier, ask for proof that's reasonable, that the prover can satisfy.
##### proof.request_proof_possible
As verifier, ask for proof that's unreasonable, that the prover can't satisfy.
##### proof.negotiate_content
##### proof.negotiate_terms

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
implementers, provide readers of your HIPE with a fuller picture.
If there is no prior art, that is fine - your ideas are interesting to us whether they are brand new or if it is an adaptation from other languages.

Note that while precedent set by other ecosystems is some motivation, it does not on its own motivate an HIPE.
Please also take into consideration that Indy sometimes intentionally diverges from common identity features.

# Unresolved questions
[unresolved]: #unresolved-questions

- What parts of the design do you expect to resolve through the HIPE process before this gets merged?
- What parts of the design do you expect to resolve through the implementation of this feature before stabilization?
- What related issues do you consider out of scope for this HIPE that could be addressed in the future independently of the solution that comes out of this HIPE?
