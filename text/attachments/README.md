- Name: attachments
- Author: Daniel Hardman <daniel.hardman@gmail.com>
- Start Date: 2018-12-24
- PR: (leave this empty)

# HIPE 00??-attachments
[summary]: #summary

Explains how to attach arbitrary content to an agent message.

# Motivation
[motivation]: #motivation

Agent messages use a structured format with a defined schema and a
small inventory of scalar data types (string, number, date, etc).
However, it will be quite common for messages to supplement formalized
exchange with arbitrary data--images, documents, or types of
media not yet invented.

We need a way to "attach" such content to agent messages. This method
must be flexible, powerful, and usable without requiring new schema
updates for every dynamic variation.

# Tutorial
[tutorial]: #tutorial

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

### Nicknames for attachments

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

### More ways of attaching

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

When I provide such a link, I am creating a logical association between the
message and an attachment that can be fetched separately. This makes it possible
to send brief descriptors of attachments and to make the downloading of the heavy
content optional (or parallelizable) for the recipient.

IPFS is not my only option for attaching by reference. I can do the same
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
recipients of attachments that are incoporated by reference are not required to
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

# Reference
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
