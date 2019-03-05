# 0003: DID Communication
- Author: Daniel Hardman <daniel.hardman@gmail.com>
- Start Date: 2018-01-05 (approx, backdated)
- PR: (leave this empty)

## Summary
[summary]: #summary

Explain the basics of __DID communication__ (__DIDComm__) at a
high level, and link to other HIPEs to promote deeper exploration.

## Motivation
[motivation]: #motivation

The DID communication between agents is a rich subject with a lot of tribal
knowledge. Newcomers to the [agent](https://github.com/hyperledger/indy-hipe/pull/86)
ecosystem tend to bring mental models that are subtly divergent from
its paradigm. When they encounter dissonance, DIDComm becomes mysterious.
We need a standard high-level reference.

## Tutorial
[tutorial]: #tutorial

>This discussion assumes that you have a reasonable grasp on topics like
[self-sovereign identity](https://medium.com/evernym/the-three-models-of-digital-identity-relationships-ca0727cb5186),
[DIDs and DID Docs](https://w3c-ccg.github.io/did-spec/), and [agents](
https://github.com/hyperledger/indy-hipe/pull/86). If you find yourself
lost, please review that material for background and starting assumptions. 

Agents have to interact with one another to get work done. How they
talk in general is DIDComm, the subject of this HIPE. The specific interactions enabled by
DIDComm--connecting and maintaining relationships, issuing credentials,
providing proof, etc.--are called __protocols__; they are described [elsewhere](
https://github.com/hyperledger/indy-hipe/pull/69).

#### Rough Overview

A typical DIDComm interaction works like this:

<blockquote>
Imagine Alice wants to negotiate with Bob to sell something online, and
that DIDComm, not direct human communication, is involved. This means Alice's
agent and Bob's agent are going to exchange a series of messages.

Alice may just press a button and be unaware of details, but underneath,
her agent begins by preparing a plaintext JSON message about the proposed sale.
(The particulars are irrelevant here, but would be described
in the spec for a "sell something" protocol.) It then looks up Bob's DID Doc
to access two key pieces of information:

* An endpoint (web, email, etc) where messages can be delivered to Bob.
* The public key that Bob's agent is using in the Alice:Bob relationship.

Now Alice's agent uses its own private key to encrypt the plaintext so only
Bob's agent can read it, and it arranges delivery to Bob. This "arranging"
can involve various hops and intermediaries. It can be complex.

Bob's agent eventually receives and decrypts the message. It knows that
it came from Alice because her private key contributed to the encryption.
It prepares its response and routes it back using a reciprocal process
(plaintext -> lookup endpoint and public key for Alice -> encrypt -> arrange
delivery).
</blockquote>

That's it.

Well, mostly. The description is pretty good, if you squint, but it does
not fit all DIDComm interactions:

* DIDComm doesn't always involve turn-taking and request-response.
* DIDComm interactions can involve more than 2 parties, and the parties are
not always individuals.
* DIDComm may include formats other than JSON.

Before we provide more details, let's explore what drives the design of
DIDComm.

#### Goals and Ramifications

The DIDComm design attempts to be:

1. __Secure__
2. __Private__
3. __Interoperable__
4. __Transport-agnostic__
5. __Extensible__

As a list of buzz words, this may elicit nods rather than surprise.
However, several items have deep ramifications.

Taken together, _Secure_ and _Private_ require that the protocol be
decentralized and maximally opaque to the surveillance economy. 

_Interoperable_ means that DIDComm should work across programming languages,
blockchains, vendors, OS/platforms, networks, legal jurisdictions, geos,
cryptographies, and hardware--as well as across time. That's quite a list. It means that
DIDComm intends something more than just Indy compatibility; it aims to be
a future-proof _lingua franca_ of all self-sovereign interactions.

_Transport-agnostic_ means that it should be possible to use DIDComm over
HTTP(S) 1.x and 2.0, WebSockets, IRC, Bluetooth, AMQP, NFC, Signal,
email, push notifications to mobile devices, Ham radio, multicast,
snail mail, carrier pigeon, and more.

All software design involves tradeoffs. These goals, prioritized as shown,
lead down an interesting path.

##### Message-Based, Asynchronous, and Simplex

The dominant paradigm in mobile and web development today is duplex
request-response. You call an API with certain inputs, and you get
back a response with certain outputs over the same channel, shortly
thereafter. This is the world of [OpenAPI (Swagger)](
https://swagger.io/docs/specification/about/), and it has many virtues.

Unfortunately, many agents are not good analogs to web servers. They may
be mobile devices that turn off at unpredictable intervals and that lack
a stable connection to the network. They may need to work peer-to-peer,
when the internet is not available. They may need to interact in time frames
of hours or days, not with 30-second timeouts. They may not listen over the
same channel that they use to talk.

Because of this, the fundamental paradigm for DIDComm is message-based,
asynchronous, and simplex. Agent X sends a message over channel A.
Sometime later, it may receive a response from Agent Y over channel B.
This is much closer to an email paradigm than a web paradigm.

On top of this foundation, it is possible to build elegant, synchronous
request-response interactions. All of us have interacted with a friend
who's emailing or texting us in near-realtime. However, interoperability
begins with a least-common-denominator assumption that's simpler. 

##### Message-Level Security, Reciprocal Authentication

The security and privacy goals, and the asynchronous+simplex design
decision, break familiar web assumptions in another way. Servers are
commonly run by institutions, and we authenticate them with certificates.
People and things are usually authenticated to servers by some sort of
login process quite different from certificates, and this authentication
is cached in a session object that expires. Furthermore, web security
is provided at the transport level (TLS); it is not an independent
attribute of the messages themselves.

In a partially disconnected world where a comm channel is not assumed to
support duplex request-response, and where the security can't be ignored
as a transport problem, traditional TLS, login, and expiring sessions
are impractical. Furthermore, centralized servers and certificate
authorities perpetuate a power and UX imbalance between servers and clients
that doesn't fit with the peer-oriented DIDComm.

DIDComm uses public key cryptography, not certificates from some parties and
passwords from others. Its security guarantees are independent of the
transport over which it flows. It is sessionless (though sessions can
_easily_ be built atop it). When authentication is required, all
parties do it the same way.

## Reference
[reference]: #reference

Provide guidance for implementers, procedures to inform testing,
interface definitions, formal function prototypes, error codes,
diagrams, and other technical details that might be looked up.
Strive to guarantee that:

- Interactions with other features are clear.
- Implementation trajectory is well defined.
- Corner cases are dissected by example.

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
