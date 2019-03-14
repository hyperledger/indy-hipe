# 0026: Agent File Format
- Name: agent-file-format
- Author: Daniel Hardman, Kyle Den Hartog
- Start Date: 2018-11-13


# Summary
[summary]: #summary

Define a file format and MIME type that contains agent messages, such
that opening the file accomplishes the same thing as receiving an
agent message.

## Motivation
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

## Tutorial
[tutorial]: #tutorial

### Agent Wire Messages (*.aw)

[![aw icon](aw-small.png)](aw-big.png)

The raw bytes of a wire message [TODO: need link to wire HIPE] may be persisted to a file
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

Although the format of agent wire data is derived from JSON and the JWT/JWE family
of specs, no useful processing of these files will take place by viewing them as
JSON, and viewing them as generic JWTs will greatly constrain which semantics are
applied. Therefore, the recommended MIME type for *.aw files is
`application/ssi-agent-wire`, with `application/jwt` as a fallback, and
`application/json` as an even less desirable fallback. (In this, we are making
a choice similar to the one that views `*.docx` files primarily as 
`application/msword` instead of `application/xml`.) If format evolution takes
place, the version could become a parameter as [described in RFC 1341](https://www.w3.org/Protocols/rfc1341/4_Content-Type.html):
`application/ssi-agent-wire;v=2`.

The default action for Agent Wire Messages (what happens when a user double-clicks one)
should be `Handle` (that is, process the message as if it had just arrived by some other transport),
if the software handling the message is an agent. In other types of software,
the default action might be to view the file. Other useful actions might include
`Send`, `Attach` (to email, chat, etc), `Open with agent`, and `Decrypt to *.ap`.

### Agent Plaintext Messages (*.ap)

[![ap icon](ap-small.png)](ap-big.png)

The text representation of an application-level message--something like a credential
offer, a proof request, or anything else worthy of an agent message family--is JSON. As such,
it should be editable by anything that expects JSON.

However, all such files have some additional conventions, over and above the simple
requirements of JSON. For example, key decorators have special meaning (
[`@id`, `@thread`](https://github.com/hyperledger/indy-hipe/blob/613ed302bec4dcc62ed6fab1f3a38ce59a96ca3e/text/message-threading/README.md),
[`@trace_to`](https://github.com/hyperledger/indy-hipe/blob/996adb82e61ab63b37a56254b92f57100ff8c8d9/text/message-tracing/README.md)
, etc). Nonces may be especially significant. The format of particular values
such as DID and DID+key references is important. Therefore, we refer to these messages
generically as JSON, but we also define a file
format for tools that are aware of the additional semantics.

The file extension associated with this filetype is `*.ap`, and should be read as
"STAR DOT A P" or "A P" files. If a format evolution takes place, a subsequent version could be
noted by appending a digit, as in `*.ap2` for second-generation `ap` files.

The name of this file format is "Agent Plaintext Format." We expect people to say,
"I am looking at an Agent Plaintext file", or "This file is in Agent Plaintext Format", or
"Does my editor have an Agent Plaintext Format plugin?"

The MIME type of *.ap files is `application/json`--or, if further discrimination is needed,
`application/json;flavor=ssi-agent-plaintext`. If format evolution takes place, the version could
become a parameter as [described in RFC 1341](https://www.w3.org/Protocols/rfc1341/4_Content-Type.html):
`application/json;flavor=ssi-agent-plaintext;v=2`.

The default action for Agent Plaintext Messages should be to
`View` or `Validate` them. Other interesting actions might be `Encrypt to *.aw`
and `Find definition of message family`.

As a general rule, agent messages that are being sent in production use cases of A2A communication should be stored 
in encrypted form (`*.aw`) at rest. There are cases where this might not be preferred, e.g., providing documentation of the 
format of message or during a debugging scenario using
[message tracing]((https://github.com/hyperledger/indy-hipe/blob/996adb82e61ab63b37a56254b92f57100ff8c8d9/text/message-tracing/README.md)).
However, these are exceptional cases. Storing meaningful `*.ap` files
decrypted is not a security best practice, since it replaces all the privacy and
security guarantees provided by the agent-to-agent communication mechanism with only
the ACLs and other security barriers that are offered by the container.

### Native Object representation

This is not a file format, but rather an in-memory form of an Agent Plaintext Message
using whatever object hierarchy is natural for a programming language to map to and from
JSON. For example, in python, the natural Native Object format is a dict that contains properties
indexed by strings. This is the representation that python's `json` library expects when
converting to JSON, and the format it produces when converting from JSON. In Java, Native
Object format might be a bean. In C++, it might be a `std::map<std::string, variant>`...

There can be more than one Native Object representation for a given programming language.

Native Object forms are never rendered directly to files; rather, they are serialized to Agent Plaintext Format
and then persisted (likely after also encrypting to Agent Wire Format).