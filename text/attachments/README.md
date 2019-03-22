# HIPE 00??-attachments
- Author: Daniel Hardman <daniel.hardman@gmail.com>
- Start Date: 2018-12-24
- PR: https://github.com/hyperledger/indy-hipe/pull/78

[summary]: #summary

Explains the three canonical ways to associate data with
an agent message.

## Motivation
[motivation]: #motivation

[DIDComm](https://github.com/hyperledger/indy-hipe/pull/98) messages
use a structured format with a defined schema and a
small inventory of scalar data types (string, number, date, etc).
However, it will be quite common for messages to supplement formalized
exchange with arbitrary data--images, documents, or types of
media not yet invented.

We need a way to "attach" such content to DIDComm messages. This method
must be flexible, powerful, and usable without requiring new schema
updates for every dynamic variation.

## Tutorial

#### Messages versus Data

Before explaining how to associate data with a message, it is worth
pondering exactly how these two categories of information differ.
It is common for newcomers to DIDComm to argue that messages are just
data, and vice versa. After all, any data can be transmitted over
DIDComm; doesn't that turn it into a message? And any message can
be saved; doesn't that make it data?

What it is true that messages and data are highly related, 
some semantic differences matter:

* _Messages are primarily about communication_. Their meaning is tied
to a communication context. [Messages are a primary mechanism whereby
state evolves in a protocol](https://github.com/hyperledger/indy-hipe/blob/f12c4222/text/protocols/README.md#ingredients).
Protocols are [versioned according to the structure and semantics of
messages](https://github.com/hyperledger/indy-hipe/blob/f12c4222/text/protocols/README.md#semver-rules).
Messages are usually small, consisting of a modest number of fields with
a structure that's focused on furthering the goals of their protocol.

* _Data has meaning at rest_, in many different DIDComm protocols, or
in important contexts beyond DIDComm. Data may be very large and very
complex. It may come in formats that are quite independent from
DIDComm. Data may be produced, consumed or handled as part of a
protocol, but the actual content of the data is usually not where
processing at the protocol level focuses. In agent codebases, it would
be common for data handling to be implemented in different classes
or libraries from the handlers for messages.

Some examples:

* A protocol to negotiate the release of medical records might cause
X-Rays, genomes, and many other artifacts to be transmitted. These
artifacts are data, whereas the information packets that arrange the
transmission and provide a carrying mechanism for the artifacts are
messages.

* A DIDComm message can be used to [report an error](https://github.com/hyperledger/indy-hipe/blob/d6503aeb/text/error-reporting/README.md). Descriptive
parameters that change how the error is processed are probably
part of the message, whereas a log file that provides supporting
information should be thought of as data rather than the message
proper. 

* The protocol for issuing credentials consists of messages that flow
through certain steps. One of the steps eventually delivers a credential.
The credential is _data_; it has meaning even when the protocol is
complete, and the protocol version may evolve independent of the data
format of the credential itself. The fact that the credential is transmitted
through a message does not change the credential's primary status as
data.

* A protocol to schedule a venue for an event might produce a confirmation
message when it finishes. This message might include a map of the
venue, instructions about how to unlock the gate, pictures of certain
resources, and so forth. This collateral is _data_, whereas the messages
that signal progression through the steps of scheduling are not.

* The [Connection Protocol](https://github.com/hyperledger/indy-hipe/blob/master/text/0031-connection-protocol/README.md)
exchanges messages to establish a connection between two parties. Part of
what's exchanged is a DID Doc. The DID Doc is more like _data_ than it is
like an ordinary _message_, since it has meaning at rest and outside the
protocol.

The line between these two concepts may not be perfectly crisp in all cases,
and that is okay. It is clear enough, most of the time, to provide context
for the central question of this HIPE, which is:

>How do we send data through messages?

#### 3 Ways

Data can be associated with DIDComm messages in 3 ways:

1. Inlining 
2. Embedding
3. Attaching

In __inlining__, data is directly assigned as the value of a JSON key
in a DIDComm message. For example, [a DID Document is inlined as the
content of the `did_doc` node in `connection_request` and
`connection_response` messages in the Connection
1.0 Protocol](https://github.com/hyperledger/indy-hipe/tree/master/text/0031-connection-protocol#example):

{
  "@id": "5678876542345",
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/request",
  "label": "Bob",
  "connection": {
    "DID": "B.did@B:A",
  	"DIDDoc": {
      	// DID Doc contents here.
    }
  }
}


In __embedding__, a data structure that describes and possibly contains
the data is assigned as the value of a JSON key in a DIDComm message.
This is a less direct mechanism than inlining, because the data is no
longer directly readable by a human inspecting the message; it is
base64-encoded instead. A benefit of this approach is that the data
doesn't have to be JSON. is described with a JSON __data_payload__ object 


#### The `~attach` decorator

The `~attach` [decorator](https://github.com/hyperledger/indy-hipe/pull/71)
may be used with any message. Its value is
an array of attachment structures. A simple example looks like this:

```JSON
"~attach": [
  {
    "nickname": "avatar",
    "mime-type": "image/png",
    "filename": "mug-shot.png",
    "lastmod_time": "2018-12-24 18:24:07Z",
    "content": {
      "base64": "aGVsbG8sIHl ...(many bytes omitted)... Ugd29ybGQ="
    }
  }
]
```
Most of the fields in the attachment structure should be self-explanatory.
They are described in detail in the [Reference section](#reference).

#### Nicknames for attachments

The `nickname` field is used to refer unambiguously to the attachment
elsewhere in the message, and works like an HTML anchor. For example,
imagine a fictional message type that's used to document property
damage for a car insurance claim, that wants a photo of the car from
the front, the back, the driver side, and the passenger side. Instead of
defining the schema to contain fields named `front`, `back`, `driver`,
and `passenger`, each of which is a base64-encoded encoded JPEG, the schema
could use the generic attachment mechanism, and then have fields named
`front_attach`, `back_attach`, `driver_attach`, and `passenger_attach`,
each of which is a reference to the nickname of an item in the `~attach`
array. A fragment of the result might look like this:

```JSON
  "front_attach": "image1",
  "back_attach": "image2",
  ...
  "~attach": [
    {
      "nickname": "image1",
      "content": {"base64": "Ugd29ybIHl ...(many bytes omitted)... GQaGVsbG8s="}
    },
    {
      "nickname": "image2",
      "content": {"base64": "GQaGV29yU ...(many bytes omitted)... bIsbG8sgdHl="}
    }
  ]
```

One advantage of this indirection is that the message may now include any
number of photos (or attachments of any additional type, not just images
and not just JPEGs) besides the 4 that are required. Another advantage is that
the same attachment may be referenced at more than one place in the core
schema, without duplicating the content. Still another advantage is that
attachments may now have formal semantics, instead of requiring human
intelligence to handle. (How many times have we written emails with multiple
attachments, and added verbiage like, "My photo of the door is attached as
image1.jpeg; my photo of the damaged trunk is attached as image2.jpeg"?)

### More ways of incorporating content

The example discussed above includes an attachment *by value*--that is, the
attachment's bytes are directly inlined in the `content.base64` field. This
is a useful mode of attachment, but it is not the only mode.

Another way that attachments can be incorporated is *by reference*. For
example, I can link to the content on IPFS:

```JSON
"content": {
  "links": ["ipfs://QmcPx9ZQboyHw8T7Afe4DbWFcJYocef5Pe4H3u7eK1osnQ/"]
}
```

When you provide such a link, you are creating a logical association between the
message and an attachment that can be fetched separately. This makes it possible
to send brief descriptors of attachments and to make the downloading of the heavy
content optional (or parallelizable) for the recipient.

IPFS is not the only option for attaching by reference. You can do the same
with S3:
```JSON
"content": {
  "sha256": "1d4db525c5ee4a2d42899040cd3728c0f0945faf9eb668b53d99c002123f1ffa",
  "links": ["s3://mybucket/mykeyoyHw8T7Afe4DbWFcJYocef5"]
}
```

Or on an ordinary HTTP/FTP site or CDN:
```JSON
"content": {
  "links": ["https://github.com/sovrin-foundation/launch/raw/master/sovrin-keygen.zip"]
}
```

Or on BitTorrent: 
```JSON
"byte_count": 192834724,
"content": {
  "links": ["torrent://content of a .torrent file as a data URI"]
}
```

Or via double indirection (URI for a BitTorrent):
```JSON
"content": {
  "links": ["torrent@http://example.com/mycontent.torrent"]
}
```

Or as content already attached to a previous agent message: 

```JSON
"content": {
  "links": ["a2a://my-previous-message-id.~attach#nickname"]
}
```

Or even via a promise to supply the content at some point in the future, in 
a subsequent agent message: 

```JSON
"content": {
  "links": ["a2a://fetch"]
}
```
[TODO: how does the message that actually delivers this content refer back
to the promise made earlier, to claim it has been fulfilled?]

The set of supported URI types in an attachment link is not static, and
recipients of attachments that are incorporated by reference are not required to
support all of them. However, they should at least recognize the meaning of each
of the variants listed above, so they can perform intelligent error handling and
communication about the ones they don't support.

The `links` field is plural (an array) to allow multiple locations to be
offered for the same content. This allows an agent to fetch attachments using
whichever mechanism(s) are best suited to its individual needs and capabilities.

[TODO: discuss sending an empty message with just attachments, and how to 
request a send of an attachment, or an alternate download method for it]

### Security and Privacy Implications

When attachments are inlined, they enjoy the same security and transmission
guarantees as all agent communication. However, given the right context,
a large inlined attachment may be recognizable by its size, even if it is
carefully encrypted.

If attachment content is fetched from an external source, then new
complications arise. The security context changes. Data streamed from a CDN
may be observable in flight. URIs may be correlating. Content may not be 
immutable or tamper-resistant.

However, these issues are not necessarily a problem. If an A2A message
wants to attach a 4 GB ISO file of a linux distribution, it may be perfectly
fine to do so in the clear. Downloading it is unlikely to introduce strong
correlation, encryption is unnecessary, and the torrent itself prevents
malicious modification.

Code that handles attachments will need to use wise policy to decide whether
attachments are presented in a form that meets its needs.

## Reference
[reference]: #reference

### Attachment structure

* `nickname`: Uniquely identifies attached content within the scope of a given
message. Recommended but not required if no references to attachments
exist in the rest of the message. If omitted, then there is no way to
refer to the attachment later in the thread, in error messages, and so forth.
Because `nickname` is used to compose URIs, it is recommended that this
name be brief and avoid spaces and other characters that require URI
escaping.

* `filename`: A hint about the name that might be used if this attachment is
persisted as a file. It is not required, and need not be unique. If this field
is present and `mime-type` is not, the extension on the filename may be used
to infer a MIME type.

* `mime-type`: Describes the MIME type of the attached content. Optional but
recommended.

* `lastmod_time`: A hint about when the content in this attachment was last
modified.

* `byte_count`: Optional, and mostly relevant when content is included by
reference instead of by value. Tells the receiver how expensive it will be,
in time, bandwidth, and storage, to fully fetch the attachment.

* `content`: A JSON object that gives access to the actual content of the
attachment. Contains the following subfields:

  * `sha256`: The hash of the content. Optional. Used as an integrity check if
  content is inlined. if content is only referenced, then including this field
  makes the content tamper-evident. This may be redundant, if the content is
  stored in an inherently immutable container like content-addressable storage.
  This may also be undesirable, if dynamic content at a specified link is
  beneficial. Including a hash without including a way to fetch the content via
  link is a form of proof of existence.
  
  * `links`: A list of zero or more locations at which the content may be fetched.


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

Multipart MIME (see RFCs [822](https://tools.ietf.org/html/rfc822),
[1341](https://tools.ietf.org/html/rfc1341), and
[2045](https://tools.ietf.org/html/rfc2045)) defines a mechanism
somewhat like this. Since we are using JSON instead of email
messages as the core model, we can't use these mechanisms directly.
However, they are an inspiration for what we are showing here. 

# Unresolved questions
[unresolved]: #unresolved-questions

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
