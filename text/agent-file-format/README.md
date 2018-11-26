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

As a general rule, agent messages that are being sent in production use cases of A2A communication should be stored 
in encrypted form at rest. There are cases where this might not be preferred, e.g. providing documentation of the 
format of message or during a debugging scenario using message tracing, however these are exceptional cases where
the security properties should be considered independently of the general case where `.ap` files are stored encrypted.