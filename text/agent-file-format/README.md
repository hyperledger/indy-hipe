- Name: agent-file-format
- Author: Daniel Hardman
- Start Date: 2018-11-13
- HIPE PR: (leave this empty)
- Jira Issue: (leave this empty)

# HIPE ????-agent-file-format
[summary]: #summary

Define a file format and MIME type that contains agent messages, such
that opening the file accomplishes the same thing as receiving a message.

# Motivation
[motivation]: #motivation

Most work on A2A so far has assumed HTTP as a transport. However, we know
that Agent-to-agent communication is transport-agnostic. We should be able to
say the same thing no matter which channel we use.

An incredibly important channel or transport for messages is digital files. Files
can be attached to messages in email or chat, can be carried around on a thumb
drive, can be backed up, can be distributed via CDN, can be replicated on
distributed file systems like IPFS, can be inserted in an object store or
in content-addressable storage, can be viewed and modified in editors, and
support a million other uses.

We need to define how files can contain agent-to-agent messages, and what the
semantics of processing such files will be.

# Tutorial
[tutorial]: #tutorial

### Agent Wire Messages (*.aw)

[![aw icon](aw-small.png)](aw-big.png)

The raw bytes of a wire message [[need link to wire HIPE] may be persisted to a file
without any modifications whatsoever. In such a case, the data will be encrypted
and packaged such that only a specific receiver can process it. However, the file will
contain a header that can be used by magic bytes algorithms to detect its type reliably.

The file extension associated with this filetype is `*.aw`, and should be read as
"STAR DOT A DUB" (short for "STAR DOT A DOUBLE U") or as "A DUB" files--NOT as a
homonym of "awe." If a format evolution takes place, a subsequent version could be
noted by appending a digit, as in `*.aw2` for second-generation `aw` files.

The name of this file format is "Agent Wire Format." We expect people to say,
"I am looking at an Agent Wire file", or "This file is in Agent Wire Format", or
"Does my editor have an Agent Wire Format plugin?"

The MIME type of *.aw files is `application/ssi-agent-wire`. If format evolution takes
place, the version could become a parameter as [described in RFC 1341](https://www.w3.org/Protocols/rfc1341/4_Content-Type.html):
`application/ssi-agent-wire;v=2`.

### Application Plaintext Messages (*.ap)

[![ap icon](ap-small.png)](ap-big.png)

The text representation of an application-level message--something like a credential
offer, a proof request, or anything else worthy of a message family--is JSON. As such,
it should be editable by anything that expects JSON.

However, all such files have some additional conventions, over and above the simple
requirements of JSON. For example, key decorators have special meaning (`@id`, `@thread`,
`@trace_to`, etc). Nonces may be especially significant. The format of particular values
such as DID and DID+key references is important. Therefore, we refer to these messages
generically as JSON, but we also define a file
format for tools that are aware of the additional semantics.

The file extension associated with this filetype is `*.ap`, and should be read as
"STAR DOT A P" or "A P" files. If a format evolution takes place, a subsequent version could be
noted by appending a digit, as in `*.ap2` for second-generation `ap` files.

The name of this file format is "Application Plaintext Format." We expect people to say,
"I am looking at an Application Plaintext file", or "This file is in Application Plaintext Format", or
"Does my editor have an Application Plaintext Format plugin?"

The MIME type of *.ap files is `application/json`--or, if further discrimination is needed,
`application/json;flavor=ssi-agent-wire`. If format evolution takes place, the version could
become a parameter as [described in RFC 1341](https://www.w3.org/Protocols/rfc1341/4_Content-Type.html):
`application/json;flavor=ssi-agent-wire;v=2`.

# Reference
[reference]: #reference

Technical details of the design are available [here](
https://github.com/hyperledger/indy-sdk/blob/23dbaac654256a50c203e97a250d68fd932609ce/doc/design/002-anoncreds/README.md). 

# Drawbacks
[drawbacks]: #drawbacks

* Revocation adds complexity to issuance, proving, and verification.
* Revocation is not a feature of W3C's Verifiable Credentials.

# Rationale and alternatives
[alternatives]: #alternatives

* Revocation lists are an obvious solution to the revocation problem. However,
  this technique does not preserve privacy, since credentials have to be presented
  in a way that they can be correlated to the revocation list. By doing so,
  credentials can also be correlated to their presenter, which defeats all the
  privacy-preserving features in Indy's underlying ZKP technology.

# Prior art
[prior-art]: #prior-art

See [this paper](https://eprint.iacr.org/2008/539) by Jan Camenisch, a researcher at IBM Zurich
and a member of Sovrin's Technical Governance Board.

# Unresolved questions
[unresolved]: #unresolved-questions

- How can the size of tails files be managed so as to be a non-issue? (This would probably
involve caching, prefetch, and similar techniques. Might also involve delegation of some
aspects of non-revocation computation to a cloud agent instead of an agent on a mobile
device.)

- Similarly, how can the time of downloading a tails file be made not to offer a
  temporal correlation point?
  
- When will we implement revocation with type3 pairings instead of type1 pairings?
