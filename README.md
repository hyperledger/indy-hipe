# Indy HIPE

This repo holds HIPEs (Hyperledger Indy Project Enhancements, pronounced like "hype"
for short) for chunks of technology or process that are important to standardize
across the Indy ecosystem.

Many changes, including bug fixes and documentation improvements, can just
be implemented and reviewed via the normal GitHub pull request workflow.
Some changes, though, are "substantial"; these are the ones where a HIPE
helps to produce consensus and a shared understanding in the community. The
HIPE process is documented below.

**Note: this repo and the enhancement proposal process it embodies has a special relationship with [sovrin-sip](https://github.com/sovrin-foundation/sovrin-sip/blob/master/README-sovrin.md) and possibly similar layered standards. Please see [derivative networks](derivative-networks.md) for details.**

## Table of Contents
[Table of Contents]: #table-of-contents

  - [When you need to follow this process]
  - [Before creating a HIPE]
  - [What the process is]
  - [The HIPE lifecycle]
  - [Reviewing HIPEs]
  - [Implementing a HIPE]
  - [HIPE Postponement]
  - [Help this is all too informal!]
  - [License]


## When you need to follow this process
[When you need to follow this process]: #when-you-need-to-follow-this-process

You need to follow this process if you intend to make "substantial" changes to
Indy, Indy-SDK, or the HIPE process itself. What constitutes a
"substantial" change is evolving based on community norms and varies depending
on what part of the ecosystem you are proposing to change.

Some changes do not require a HIPE:

  - Rephrasing, reorganizing, refactoring, or otherwise "changing shape does
    not change the meaning."
  - Additions that strictly improve objective, numerical quality criteria
    (warning removal, speedup, better platform coverage, more parallelism, trap
    more errors, etc.)
  - Additions only likely to be _noticed by_ other developers-of-indy,
    invisible to users-of-indy.

If you submit a pull request to implement a new feature without going through
the HIPE process, it may be closed with a polite request to submit a HIPE first.

## Before creating a HIPE
[Before creating a HIPE]: #before-creating-a-hipe

Although there is no single way to prepare for submitting a HIPE, it is
generally a good idea to pursue feedback from other project developers
beforehand, to ascertain that the HIPE may be desirable; having a consistent
impact on the project requires concerted effort toward consensus-building if you
intend for the HIPE to be a Standard candidate. If you only intend to propose
an idea to the community a short document using the [HIPE template](0000-template.md)
will suffice.

The most common way to identify if a design or implementation is worth pursuing 
is discussing the idea over on #indy and #indy-sdk, discussing the topic on 
our community calls (see the [Hyperledger Community Calendar](https://wiki.hyperledger.org/community/calendar-public-meetings)),
or submitting a proposal to the [Discussions folder](Discussions/README.md). For discussion 
on Draft proposal HIPES we're trying out using both issues and pull requests for
changes to HIPEs in the Draft folder.

As a rule of thumb, receiving encouraging feedback from long-standing project
developers, and particularly members of the relevant sub-team is a good
indication that the HIPE is worth trying to transition from a Discussion-track 
HIPE to a Standards-track HIPE.

## What the process is
[What the process is]: #what-the-process-is

In short, to get a major feature added to Indy, one must first get the HIPE
merged into the HIPE repository as a markdown file. At that point, the HIPE is
"active" and may be implemented with the goal of eventual inclusion into Indy.

### Discussions HIPE process
  - Fork [the HIPE repo](https://github.com/hyperledger/indy-hipe).
  - Pick a descriptive name for your feature. Use kebab case ("my-cool-feature").
    Do not assign a HIPE number.
  - Create a folder under `Discussions/` for your feature, using the chosen name.
    Copy `0000-template.md` to `text/<your folder name>/README.md`.
  - Fill in the HIPE. Put care into the details: HIPEs that do not present
    convincing motivation, demonstrate an understanding of the impact of the
    design, or are disingenuous about the drawbacks or alternatives tend to be
    poorly received and will not make good candidates for Standards-track HIPEs.
    You can add supporting artifacts, such as diagrams and sample data, 
    in the HIPE's folder.
  - Submit a pull request with your additions to the `Discussions/` folder.
    These pull requests will be added ASAP by the [maintainers](MAINTAINERS.md)
  - Build consensus and integrate feedback. HIPEs that have broad support are
    much more likely to make progress than those that don't receive any
    comments. Feel free to reach out to the HIPE assignee, in particular, to get
    help identifying stakeholders, obstacles, and implementors listed.
    This is an important hurdle to clear in order to have your HIPE to
    reach Standards-track.
  - If the author wishes to make changes to a `Discussions/` HIPE they should
    add the `DRAFT-UPDATE` tag to the front of their PR. This allows the 
    maintainers to quickly process changes to HIPEs in the discussion folder 
    by verifying that the PR has been submitted by an author of the HIPE, or 
    has been OKed by the author with an accepted PR review from the HIPE author.
  - Some HIPEs will never reach Standards-track and this is acceptable. If the
    implementors and HIPE authors only wish to make others in the community aware
    of their designs, using this folder is best practice.

### Standards HIPE process
  - Once a HIPE author believes there's consensus on a design with multiple 
    implementations available, the author should propose it as a candidate for 
    Standards-track. This is done by proposing the HIPE as a candidate to the [indy-maintainers channel](https://chat.hyperledger.org/channel/indy-maintainers)
    or through the [indy mailing list](https://lists.hyperledger.org/g/indy)
  - Maintainers will then discuss this HIPE on the next Maintainers call to provide
    a *disposition* for the HIPE (merge, close, or postpone). If the *disposition* is
    declared `close` or `postpone` Maintainers MUST provide an argument supporting 
    the disposition on the HIPE. Maintainers SHOULD use their best judgment while 
    taking this step, and the *disposition* SHOULD give ample time and notification for
    stakeholders to push back if it is made prematurely. This may mean allowing,
    notifying stakeholders of the Maintainers meetings where the HIPE will be given
    a *disposition* decision.
  - If maintainers believe the candidate HIPE is ready to merge as a Standard,
    they'll create a `Final Comment Period (FCP)` pull request moving the candidate
    HIPE from the `Discussions` folder to the `Standards` folder and provide the 
    candidate HIPE with a number. For example, a candidate HIPE's name would change 
    from `<my-cool-feature-name>` to something like `0097-my-cool-feature-name`.
    Maintainers will also verify that all contributors to the HIPE are listed in the
    `authors` section of the HIPE for proper attribution.
  - During the FCP period, the HIPE will undergo a through review by the community
    to offer a broader public comment period for the community to raise final concerns.
  - If community consensus isn't built during the FCP period, maintainers reserve the
    right to change the *disposition* as needed. That does not require
    consensus amongst all participants in the HIPE thread (which is usually
    impossible).
  - For HIPEs with a lengthy discussion, the motion to FCP is usually preceded by
    a *summary comment* trying to lay out the current state of the discussion
    and major tradeoffs/points of disagreement.
  - The FCP lasts ten calendar days, so that it is open for at least 5 business
    days. It is also advertised widely, e.g. on mailing lists and rocketchat.
    This way all stakeholders have a chance to lodge any final objections before
    a decision is reached.
  - In most cases, the FCP period is quiet, and the HIPE is either merged or
    closed. However, sometimes substantial new arguments or ideas are raised,
    the FCP is canceled, and the HIPE goes back into development mode.
  - Once the HIPE is merged, add it to the online documentation by including a 
   link to it in the `index.rst` file.

## The HIPE lifecycle
[The HIPE lifecycle]: #the-hipe-lifecycle



Once a HIPE becomes "active" then authors may implement it and submit the
feature as a pull request to the Indy repo. Being "active" is not a rubber
stamp, and in particular still does not mean the feature will ultimately be
merged; it does mean that in principle all the major stakeholders have agreed
to the feature and are amenable to merging it.

Furthermore, the fact that a given HIPE has been accepted and is "active"
implies nothing about what priority is assigned to its implementation, nor does
it imply anything about whether an Indy developer has been assigned the task of
implementing the feature. While it is not *necessary* that the author of the
HIPE also write the implementation, it is by far the most effective way to see
a HIPE through to completion: authors should not expect that other project
developers will take on responsibility for implementing their accepted feature.

HIPEs MUST begin as an item that is provided to the `Discussions` folder. During
this time it is acceptable for major changes to occur and for implementers to
begin working on implementations to support the designs offered in the `Discussions`
HIPE. If implementators only intend to offer their designs to the community for
others to discover this is acceptable, but will make it more difficult for the HIPE
to become a `Standards` HIPE. In order for a HIPE to become a `Standard` there must
be at least one implementation (IndySDK) or multiple implementations (when not in IndySDK)
which are referenced in the `Standard` HIPE.


Modifications to "active" HIPEs can be done in follow-up pull requests. We
strive to write each HIPE in a manner that it will reflect the final design of
the feature; but the nature of the process means that we cannot expect every
merged HIPE to actually reflect what the end result will be at the time of the
next major release.

In general, once accepted, HIPEs should not be substantially changed. Only very
minor changes should be submitted as amendments. More substantial changes
should be new HIPEs, with a note added to the original HIPE. Exactly what counts
as a "very minor change" is up to the maintainers to decide.

![HIPE Lifecycle Diagram](HIPE-Lifecycle-Diagram.png?raw=true "HIPE Lifecycle Diagram")

`Standard` HIPEs may also be moved to a `Replaced` or `Obsolete` status. Details on how
these statuses are used should be discussed further at a later time. We can defer this 
discussion until we need this part of the process.


## Reviewing HIPEs
[Reviewing HIPEs]: #reviewing-hipes

While the HIPE is in the `Discussions` section, the HIPE should be discussed and major changes
can occur. The majority of changes should occur during the `Discussions` period. Once the HIPE
is ready for 

The maintainers may schedule meetings with the author and/or relevant stakeholders
to discuss the issues in greater detail, and in some cases, the topic may be discussed at a
sub-team meeting. In either case, a summary of the meeting will be posted back to the HIPE
either through an issue or a pull request adding further details of discussions that occurred.

Maintainers make final decisions about HIPEs after the benefits and drawbacks
are well understood. These decisions can be made at any time. When a decision is made,
the decision will be added into the HIPE and the maintainers will add a section into the HIPE
describing their rationale for the decision.


## Implementing a HIPE
[Implementing a HIPE]: #implementing-a-hipe

`Discussions` HIPEs do not require implementations, but `Candidate` HIPEs do in 
order to become a `Standards` HIPE. For example, a HIPE which aims to discuss good
patterns may not include any implementations. These will remain `Discussions` HIPEs
and may be used to further discuss terminology, tribal knowledge, or other aspects
within Hyperledger Indy or self-sovereign identity (SSI). If an implementor plans to
provide an implementation into IndySDK they should create a JIRA ticket and make sure
IndySDK maintainers have reviewed their `Discussions` HIPE.
The JIRA ticket associated with the implementation should be added to [indy's jira](https://jira.hyperledger.org/projects/INDY/issues); thus that
associated issue can be assigned a priority via the triage process that the
team uses for all issues in the Indy repository.

The author of a HIPE is not obligated to implement it. Of course, the HIPE
author (like any other developer) is welcome to post an implementation for
review after the HIPE has been accepted.

If you are interested in working on the implementation of an "active" HIPE, but
cannot determine if someone else is already working on it, feel free to ask
(e.g. by leaving a comment on the associated issue).


## HIPE Postponement
[HIPE Postponement]: #hipe-postponement

Some HIPE pull requests are tagged with the "postponed" label when they are
closed (as part of the rejection process). A HIPE closed with "postponed" is
marked as such because we want neither to think about evaluating the proposal
nor about implementing the described feature until some time in the future, and
we believe that we can afford to wait until then to do so. Historically,
"postponed" was used to postpone features until after 1.0. Postponed pull
requests may be re-opened when the time is right. We don't have any formal
process for that, you should ask members of the relevant sub-team.

Usually, a HIPE pull request marked as "postponed" has already passed an
informal first round of evaluation, namely the round of "do we think we would
ever possibly consider making this change, as outlined in the HIPE pull request,
or some semi-obvious variation of it." (When the answer to the latter question
is "no", then the appropriate response is to close the HIPE, not postpone it.)


### Help this is all too informal!
[Help this is all too informal!]: #help-this-is-all-too-informal

The process is intended to be as lightweight as reasonable for the present
circumstances. As usual, we are trying to let the process be driven by
consensus and community norms, not impose more structure than necessary.

[Maitainers chat]: https://chat.hyperledger.org/channel/indy-maintainers
[developer chat]: http://chat.hyperledger.org/channel/indy-sdk
[HIPE issue tracker]: https://github.com/hyperledger/indy-hipe/issues
[HIPE repository]: http://github.com/hyperledger/indy-hipe

## License
[License]: #license

This repository is licensed under an [Apache 2 License](LICENSE).

### Contributions

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
dual licensed as above, without any additional terms or conditions.

### Acknowledgement

The structure and a lot of the initial language of this repository was borrowed from [Rust RFC](https://github.com/rust-lang/rfcs) .
Their good work has made the setup of this repository much quicker and better than it otherwise would have been.
If you are not familiar with the Rust community, you should check them out.
