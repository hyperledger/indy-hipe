- Name: Agent Connection Protocol
- Author: Michael Lodder <mike@sovrin.org>
- Start Date: 2018-Oct-11
- PR:
- Jira Issue:

# Summary
[summary]: #summary

This HIPE intends to supercede the existing HIPE for describing the agent connection protocol.
It is intended to be a much simplier and secure method for connecting agents.

# Motivation
[motivation]: #motivation

Existing protocols for connecting agents all seem to be complicated and use rudimentary methods for insuring confidentiality and integrity of the setup. Complicated protocols are prone to error due to misunderstandings and implementation problems.

This protocol aims to be as simple and secure as possible to facilitate adoption and mitigate potential implemenation issues.

# Tutorial
[tutorial]: #tutorial

Agents connect by means of introductory messages. These messages only need to contain information to identify and authenticate each other for subsequent interactions, where to send the message, and the version of the message format. Security parameters and algorithms should be captured in the version of the message format to limit cryptographic algorithm agility that causes many problems with programmers. 

### Overview 

One of the agents initiates the protocol by means of a discovery mechanism. This is done by either looking up at some public service how to communicate with the corresponding agent or out-of-band methods. Out-of-band introductions could be two parties communicating face to face, via email, text message, phone calls, etc.

Public services should include enough information for an agent to send the initial contact message by retrieving the information from a known source like a website, database, ledger, or whatever. Out-of-band methods can include QR codes, word sequences, or URNs.

Before iterating further it is important to cover other terms that will be used throughout the remainder of this HIPE.

**Connecting Agent**: The agent that wants to create a new connection.
**Contacted Agent**: The agent that is contacted by new agents.

### Message Types

The following message formats are used by the connection protocol.

**New Connection Offer**
```json
{
    "@type": "did:sov:1234567890;spec/messagefamily/1.0/newconnectionoffer",
    "content": {
        "public_key": "<base58 encoded key>",
        "return_path": ["<url for each hop to return>"]
    }
}
```

**New Connection Request**
```json
{
    "@type": "did:sov:1234567890;spec/messagefamily/1.0/newconnectionrequest",
    "content": {
        "public_key": "<base58 encoded key>",
        "message": "<auth crypted message>",
    }
}
```

**New Connection Message**
```json
{
    "did": "did:sov:98765432e123456789",
    "ver_key": "<base58 encoded key>"
}
```

**New Connection Response Message**
```json
{
    "@type": "did:sov:1234567890;spec/messagefamily/1.0/newconnectionresponse",
    "content": {
        "message": "<auth crypted message>",
    }
}
```

Acknowledge message is completely optional a indicates to the connecting agent that the process has been completed
by the contacted agent. The format is identical to a new connection response but is included here for reference.
**New Connection Acknowledge Message**
```json
    "@type": "did:sov:1234567890;spec/messagefamily/1.0/newconnectionacknowledge",
    "content": {
        "message": "<auth crypted message>",
    }
```

# Reference
[reference]: #reference
Auth crypt will use the *public_key* from the received messages and the receiver's private key.
Auth crypt should use [XSALSA-Poly1305](https://www.xsalsa20.com) authenticated encryption.
**iv** should be a cryptographically secure generated random number that is 192 bits.

*Libindy* currently provides the cryptographic apis for auth crypt and create new keys:
```rust
indy_create_key
indy_crypto_auth_crypt
indy_crypto_auth_decrypt
```
Most programming languages have access to a cryptographically safe random number generator
but here is a list of known safe libraries for reference. The major point is that these libraries
use the operating system random number generator.
- Python: random.SystemRandom
- Rust: rand::os::OsRng
- NodeJS: crypto.randomBytes
- Windows: CryptGenRandom
- Linux: /dev/urandom or /dev/random
- Mac OS X: /dev/random


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
- What other designs have been considered and what is the rationale for not
choosing them?
- What is the impact of not doing this?

# Prior art
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

# Unresolved questions
[unresolved]: #unresolved-questions

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
