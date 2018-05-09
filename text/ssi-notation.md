- ssi_notation
- Daniel Hardman
- 2018-05-03
- RFC PR: (leave this empty)
- Jira Issue: (leave this empty)

# Summary
[summary]: #summary

This RFC describes a simple, standard notation for various concepts related
to self-sovereign identity (SSI).
The notation could be used in design docs, other RFCs, source code comments,
chat channels, scripts, debug logs, and miscellaneous technical
materials throughout the Indy ecosystem. We hope it is also used in the larger
SSI community.

This RFC is complementary to the [Sovrin Glossary](https://sovrin.org/library/glossary/),
which carefully curates terms and their meanings. We start from the concepts and verbiage
defined there. Another complementary effort is the work to standardize ZKLang (a symbolic
language for representing zero knowledge proof.)

# Motivation
[motivation]: #motivation

All technical materials in our ecosystem hinge on fundamental concepts of self-sovereign
identity such as owners, keys, DIDs, and agents. We need a standard, documented notation to
refer to such things, such that we can incorporate the notation by reference and
be consistent in its usage.

# Guide-level explanation
[guide-level-explanation]: #guide-level-explanation

The following explanation is meant to be read sequentially and should provide a
friendly overview for most who encounter the RFC. See the 
[Reference section](#reference-level-explanation)
for quick lookup.

## Requirements
This notation aims to be:

* Precise
* Consistent
* Terse
* Easy to learn, understand, guess, and remember
* Representable in 7-bit ASCII plain text

The final requirement deserves special comment. Cryptologists are
a major stakeholder in SSI theory. They already have many
notational conventions, some more standardized than others.
Generally, their notation derives from advanced math and uses
specialized symbols and fonts. These experts also tend
to intersect strongly with academic circles, where LaTeX and similar
rendering technologies are common.

Despite the intersection between SSI, cryptology, and academia, SSI
has to serve a broader audience. Its builders are coders, not mathematicians.
Coders regularly write docs in markdown and html. They interact with
one another on chat. They write emails and source code where comments
might need to be embedded. They create UML diagrams. They type in shells.
They paste code into slide decks and word processors. All of these
behaviors militate against a notation that requires complex markup.
Instead, we want something simple, clean, and universally supported.
Hence the 7-bit ASCII requirement. A future version of this RFC,
or an addendum to it, might explain how to map this 7-bit
ASCII notation to various schemes that use mathematical symbols
and are familiar to experts from other fields.

## Solution

### Identity Owners

In a self-sovereign worldview, the conceptual center of gravity is
__identity owners__. These are people and institutions--the type of
entity that can (at least theoretically) be held legally accountable
for its actions. Identity owners control a __sovereign domain__ that
encompasses all their agents, data, and devices.
The notation's first goal is therefore an efficient and unambiguous way to anchor
derivative concepts to owners and their domain. 

Identity owners are denoted with a single
capital ASCII alpha, often corresponding to their first initial. For
example, Alice might be represented as `A`. By preference, the first
half of the alphabet is used (because "x", "y", and "z" tend to have
other ad-hoc meanings). When reading aloud, the spoken form of
a symbol like this is the name of the letter. The relevant [ABNF](
https://tools.ietf.org/html/rfc5234) fragment is:

 ```ABNF
  ucase_alpha    = %x41-5A            ; A-Z
  lcase_alpha    = %x61-7A            ; a-z
  digit          = %30-39             ; 0-9
  
  identity_owner = ucase_alpha
  ```
Because the domain of an identity owner is like their private
universe, the name or symbol of an identity owner is often used
to denote a domain as well; context eliminates ambiguity. You
will see examples of this below.
   
### Other Entities

Identity owners are not the only participants in an SSI ecosystem.
Other participants include IoT things, hardware and software that
an identity owner uses, and so forth. These __entities__ may have
a high degree of autonomy (e.g., an AI in a self-driving car), but
they are owned or controlled in at least a legal sense by some
other party.

![taxonomy](taxonomy.png)

IoT things are represented with two or more lower-case ASCII alphanumerics or
underscore characters, where the first char cannot be a digit: `bobs_car`, `drone4`.

  ```ABNF
  name_start_char = lcase_alpha / "_"            ; a-z or underscore
  name_other_char = digit / lcase_alpha / "_"    ; 0-9 or a-z or underscore
  iot_thing = name_start_char 1*name_other_char
  ```

Agents are numbered and are represented by up to three digits. In
simple discussions, one digit is plenty, but three digits are allowed
so agents can be conveniently grouped by prefix (e.g., all items in
Alice's domain might begin with `1`, and all Bob's might
begin with `2`). 
   
  ```ABNF
  agent = 1*3digit
  ```

Devices are often (and inaccurately) used as a casual equivalent for agents;
we may say things like "Alice's iPhone" when we more precisely mean
"the agent on Alice's iPhone." In reality, there may be zero, one, or
more than one agents running on a particular device.
For this reason, devices are distinguished from agents in the notation. A
device is represented in the same way as an IoT thing: `alices_iphone9`.

  ```ABNF
  device = name_start_char 1*name_other_char
  ```

### Relationships

#### Short Form (more common)

Alice’s pairwise relationship with Bob is represented with colon
notation: `A:B`. This is read aloud as “A to B” (preferred because
it’s short; alternatives such as “the A B relationship” or “A colon B”
or “A with respect to B” are also valid). When written in the other order,
it represents the same relationship as seen from Bob’s point of view.
Note that IoT things may also participate in relationships: `A:bobs_car`.

N-way relationships (e.g., doctor, hospital, patient) are written with
a single colon, followed by all other letters in the relationship, in
alphabetical order, separated by `+`: `A:B+C`, `B:A+C`. This is read
aloud as in "A to B plus C."
   
  ```ABNF
  entity = identity_owner / iot_thing
  next_entity = "+" entity
  short_relationship = entity ":" entity *next_entity
  ```

#### Long Form

Short form is convenient and brief, but it is inconsistent because each
party to the relationship describes it differently. With N-way
relationships, the same relationship may go by many different names. Sometimes
this may be undesirable, so a long and consistent form is also supported.
The long form of both pairwise and N-way relationships lists all
participants to the right of the colon, in alphabetical order. Thus
the long forms of the Alice to Bob relationship might be `A:A+B` (for Alice's
view of this relationship) and `B:A+B` (for Bob's view).
For a doctor, hospital, patient relationship, we
might have `D:D+H+P`, `H:D+H+P`, and `P:D+H+P`. Note how the enumeration
of parties to the right of the colon is consistent.

Long form and short form are allowed to freely vary; any tools that parse
this notation should treat them as synonyms and stylistic choices only.

The ABNF for long form is identical to short form, except that we are
guaranteed at least two parties and one `+` on the right:

  ```ABNF
  long_relationship = entity ":" entity 1*next_entity
  ```
  
#### Relationship to Any

The concept of public DIDs suggests that someone may think about a
relationship as unbounded, or as not varying no matter who the other
entity is. For example, a company may create a public
DID and advertise it to the world, intending for this connection point
to begin relationships with customers, partners, and vendors alike.
While best practice suggests that such relationships be used with care,
and that they primarily serve to bootstrap pairwise relationships,
the notation still needs to represent the possibility.

The keyword `any` is reserved for these semantics. If Acme Corp is
represented as `A`, then Acme's unbounded public "face" could be
denoted with `A:any`. When `any` is used, it is never the entity whose
perspective is captured; it is always a faceless "other". This means
that `any` appears only on the right side of a colon in a relationship,
and it probably doesn't makes sense to combine it with other participants since
it would subsume them all. Hence, we add one more relationship ABNF:

  ```ABNF
  any_relationship = entity ":" "any"
  ```

### Association

Entities associated with a sovereign domain may be named in a way that
makes that association clear, using a `name@context` pattern familiar
from email addresses: `1@A` (“one at A”) is agent 1 in A’s sovereign domain.
(Note how we use an erstwhile identity owner symbol to reference a domain
here, but there is no ambiguity.)
This fully qualified form of an entity reference is useful for clarification
but is often not necessary.

In addition to domains, this same associating notation may be used where
a relationship is the context, because sometimes the association is
to the relationship rather than to a participant. See the DID
example in the next section.

### Inert Items

In contrast to entities, which may be capable of independent action
and which may have identities in the SSI sense, inert or passive constituents
of a sovereign domain that are owned (for example, data, money, keys) use
dot notation: `A.ls`, (A’s link secret), `A.policy`, (A’s authZ policy), etc.

Names for inert things use the same rules as names for agents and devices.

Alice’s DID for her relationship with Bob is inert and therefore owned, but
it is properly associated with the relationship rather than just Alice. It is
thus represented with `A.did@A:B`. (The keyword `did` is reserved for DIDs).
This is read as “A’s DID at A to B”. Bob’s complementary DID would be `B.did@B:A`.

  ```ABNF
  inert = name_start_char 1*name_other_char
  nested = "." inert
  owned_inert = entity 1*nested
  
  associated_to = identity_owner / short_relationship / long_relationship / any_relationship
  associated = entity 0*nested "@" associated_to
  ```
   
If `A` has a cloud agent `2`, then the public key (verification key or verkey)
and private, secret key (signing key or sigkey) used by
`2` in `A:B` would be: `2.pk@A:B` and `2.sk@A:B`. This is read as “2
dot P K at A to B” and “2 dot S K at A to B”. Here, `2` is known to
belong to `A` because it takes `A`’s perspective on `A:B`--it would
be equivalent but unnecessary to write `A.2.pk@A:B`.

### Counting and Iteration

Sometimes, a concept or value evolves over time. For example, a given discussion
might need to describe a DID Doc or an endpoint or a key across multiple
state changes. In mathematical notation, this would typically be modeled with
subscripts. In our notation, we use square brackets, and we number beginning
from zero. `A.pk[0]@A:B` would be the first pubkey used by A in the A:B relationship;
`A.pk[1]@A:B` would be the second pubkey, and so on. Likewise, a sequence of
messages could be represented with `msg[0]`, `msg[1]`, and `msg[2]`

### Negotiation Patterns and Common Message Types

A common message pattern in the ecosystem involves this sequence:

Credentials, credential offers, proofs, proof requests, and proof resolutions are
just special cases of a generic message; however, they are so significant to SSI
that they deserve a special shorthand. This comes in the form of prefix on their
names:

  ```ABNF
  credential_prefix = "="
  proof_prefix = "~"
  offer_infix = "?"         ; an offer
  resolution_prefix = "!"
  
  ```
  
### Payment Addresses

### Encryption

Encryption deserves special consideration in the SSI world. It often figures
prominently in discussions about security and privacy, and our notation needs
to be able to represent it carefully.

The following crypto operations are recognized by the notation, without
making a strong claim about how the operations are implemented. (For
example, inline Diffie Helman and an ephemeral symmetric key might be
used for the asymmetric algorithms. What is interesting to the notation
isn't the low-level details, but the general semantics achieved.)

* `anon_crypt(msg, recipient_pubkey)` -- Asymmetrically encrypt
only for recipient, achieving confidentiality. Sender is anonymous.
Parties may have had no prior contact, though sender must discover
recipient's pubkey. The message is tamper evident.
* `auth_crypt(msg, recipient_pubkey, sender_privkey)` -- Asymmetrically
encrypt only for recipient, achieving confidentiality. Recipient
learns sender’s pubkey but can’t prove to anybody else who the sender
is (making the message repudiable). Parties may have had no prior contact,
though sender must discover recipient's pubkey.
The message is tamper evident.
* `sign(msg, sender_privkey)` -- Associate a signature with a
message, making the message [non-repudiable](
https://github.com/sovrin-foundation/protocol/blob/master/janus/repudiation.md).
This also makes the message tamper-evident. A signature does not
automatically encrypt and therefore is not a way to achieve
confidentiality.
* `sym_crypt(msg, sym_key)` -- Symmetrically encrypt for anyone
who has the symmetric key, achieving a limited form of confidentiality.
Key must be shared in advance with both parties. Likely tamper
evident. If multiple parties know the symmetric key, the sender is
not knowable to the recipient.

The notation for these crypto primitives uses curly braces around the
message, with suffixes to clarify semantics. Generally,
it identifies a recipient as an identity owner or thing, without clarifying
the key that's used--the pairwise key for their DID is assumed.

```ABNF
asymmetric   = "/"                                   ; suffix
symmetric    = "*"                                   ; suffix
sign         = "#"                                   ; suffix
multiplex    = "%"                                   ; suffix

anon_crypt   = "{" msg "}" asymmetric entity          ; e.g., {"hello"}/B

                ; sender is first entity in relationship, receiver is second
auth_crypt   = "{" msg asymmetric short_relationship ; e.g., {"hello"}/A:B 
             
sym_crypt    = "{" msg "}" symmetric entity           ; e.g., {"hello"}*B
``` 

The relative order of suffixes reflects whether encryption or
signing takes place first: `{"hello"}*B#` says that symmetric
encryption happens first, and then a signature is computed over
the cypertext; `{"hello"#}*B` says that plaintext is signed, and
then both the plaintext and the signature are encrypted. (The
`{"hello"}#*B` variant is nonsensical because it splits the
encryption notation in half).
 
All suffixes can be further decorated with a parenthesized algorithm
name, if precision is required: `{"hello"}*(aes256)B` or
`{"hello"}/(rsa1024)A:B` or `{"hello"#(ecdsa)}/B`.

Multiplexed asymmetric encryption is noted above, but has not yet been
described. This is a technique whereby a message body is encrypted with
an ephemeral symmetric key, and then the ephemeral key is encrypted
asymmetrically for multiple potential recipients (each of which has a unique
but tiny payload [the key] to decrypt, which in turn unlocks the main payload). The
notation for this looks like `{msg}%BCDE` for multiplexed anon_crypt (sender
is anonymous), and like `{msg}%A:BCDE` for multiplexed auth_crypt (sender
is authenticated by their private key).

### Other punctuation

Message sending is represented with arrows: `->` is most common, though `<-`
is also reasonable in some cases. Message content and notes about sending
can be embedded in the hyphens of sending arrow, as in this example, where
the notation says an unknown party uses http to transmit "hello", anon-enrcypted
for Alice:

  ```<unknown> -- http: {"hello"}/A --> 1```

Parentheses have traditional meaning (casual usage in written language, plus
grouping and precedence).

Angle braces `<` and `>` are for placeholders; any
reasonable explanatory text may appear inside the angle braces, so to
represent Alice's relationship with a not-yet-known entity, the notation
might show something like `A:<TBD>`.

# Reference-level explanation
[reference-level-explanation]: #reference-level-explanation

## Quick Examples

## Reserved Words
* `any`: The name for the public side of a relationship between a
  specific entity and the public.
* `did`: The DID belonging to an entity in a given relationship, as in `A.did@A:B`
* `ipk` and `isk`: Issuer public (verification) key and issuer secret key. 
* `ls`: The link secret belonging to an entity, as in `A.ls`.
* `micro`: The microledger belonging to an entity in a given relationship, as in `A.micro@A:B`
* `pk`: The public verification key (verkey) portion of an asymmetric
  keypair. The more specific form, `vk`, is only recommended if elliptic
  curve crypto is specifically intended.
* `rpk` and `rsk`: Revocation public (verification) and secret key.
* `sk`: The private key (privkey, sigkey) portion of an asymmetric
  keypair.  
* `vk`: The public verification key (verkey) portion of an asymmetric
  keypair. The more generic form, `pk`, is recommended instead, unless elliptic
  curve crypto is specifically intended.
* `wallet`: An identity wallet belonging to an entity.

# Drawbacks
[drawbacks]: #drawbacks

* Creates one more formalism to learn. SSI is already a dense topic with a steep
  learning curve.
* Creates something that needs to be version-controlled.

# Rationale and alternatives
[alternatives]: #alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not choosing them?
- What is the impact of not doing this?

# Prior art
[prior-art]: #prior-art

* [LaTeX](https://en.wikibooks.org/wiki/LaTeX/Mathematics) provides powerful
and beautiful rendering of complex formal concepts, and uses escape sequences that are
pure ASCII. There is a [JVM-based parser/renderer for Latex](
https://sourceforge.net/projects/jlatex/); perhaps similar things exist for other
programming languages as well.

    However, LaTeX has drawbacks. It focuses on rendering,
    not on the semantics behind what's rendered. In
    this respect, it is a bit like HTML 1.0 before CSS--you can bold or underline,
    but you're usually encoding what something looks like, not what it means. (LaTeX
    does support logical styles and sections, but this introduces far more complexity
    than we need.)
    
    The LaTeX snippet ```e^{-x_y}``` should render like this:
     
    ![e^{-x_y} rendered by LaTeX engine](expression.png)
     
    This is great--but it doesn't say anything about what `e`, `x`, and `y` _mean_. Thus a LaTeX
    solution would still have to define conventions for meaning in a separate spec.
    These conventions would have to find representations that are not obvious
    (LaTeX recommends no particular rendering for encryption functions, keys,
    ownership, association). And such a spec would have to be careful not to
    ascribe meaning to a rendering that conflicts with assumptions of
    knowledgeable LaTeX users (e.g., using `\sqrt` for something other than
    its mathematical square root function in the vocabulary would raise eyebrows). 
    
    Highly formatted LaTeX is also quite verbose.
    
    A very simple form of LaTeX could be used (e.g., just superscripts and subscripts)--
    but this would have to solve some of the problems [mentioned below](#superscripts), in the 
    DKMS section.
    
* [ASCIIMath](http://asciimath.org/) has many of the same benefits and drawbacks as
LaTeX. It is less ubiquitous.

* The key management notation introduced in "[DKMS (Decentralized Key Management
System) V3](http://bit.ly/dkmsv3)" overlaps significantly with the concerns of this notation (render [this
diagram](
https://github.com/hyperledger/indy-sdk/blob/677a0439487a1b7ce64c2e62671ed3e0079cc11f/doc/design/005-dkms/08-add-connection-private-did-provisioned.puml
) for an example). However, it does not encompass all the concerns
explored here, so it would have to be expanded before it could be complete.

  [superscripts]: #superscripts

  Also, experiments with superscripts and subscripts in this format led to semantic
  dead ends or undesirable nesting when patterns were applied consistently. For
  example, one thought had us representing Alice's verkey, signing key, and DID for her
  Bob relationship with A<sub>B</sub><sup>VK</sup>, A<sub>B</sub><sup>SK</sup>.
  and A<sub>B</sub><sup>DID</sup>. This was fine until we asked how to represent
  the verkey for Alice's agent in the Alice to Bob relationship; is that
  A<sub>B</sub><sup>DID<sup>VK</sup></sup>? And what about Alice's link secret, that
  isn't relationship-specific? And how would we handle N-way relationships?

# Unresolved questions
[unresolved]: #unresolved-questions

* Do we need to support non-ASCII characters in the notation? (I suggest no--for coders
  wishing to share simple algebra-like notes in comments or on chat, ASCII is a reasonable
  least-common denominator usable with any keyboard or natural language. Adding more complicates
  too many things.)
* Do we need special notation for credentials, proofs, and the like? If so, how does
  this relate to ZKLang?
* Do we need notation for security contexts of messages?
