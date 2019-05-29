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
  - [Known Protocols]
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

A hastily proposed HIPE can hurt its chances of acceptance. Low quality
proposals, proposals for previously rejected features, or those that don't fit
into the near-term roadmap, may be quickly rejected, which can be demotivating
for the unprepared contributor. Laying some groundwork ahead of the HIPE can
make the process smoother.

Although there is no single way to prepare for submitting a HIPE, it is
generally a good idea to pursue feedback from other project developers
beforehand, to ascertain that the HIPE may be desirable; having a consistent
impact on the project requires concerted effort toward consensus-building.

The most common preparations for writing and submitting a HIPE include talking
the idea over on #indy and #indy-sdk, discussing the topic on our community
calls (see the []Hyperledger Community Calendar](https://wiki.hyperledger.org/community/calendar-public-meetings)),
and occasionally posting "pre-HIPEs" on the mailing lists. You may file issues
on this repo for discussion, but these are not actively looked at by the teams.

As a rule of thumb, receiving encouraging feedback from long-standing project
developers, and particularly members of the relevant sub-team is a good
indication that the HIPE is worth pursuing.

## What the process is
[What the process is]: #what-the-process-is

In short, to get a major feature added to Indy, one must first get the HIPE
merged into the HIPE repository as a markdown file. At that point, the HIPE is
"active" and may be implemented with the goal of eventual inclusion into Indy.

  - Fork [the HIPE repo](https://github.com/hyperledger/indy-hipe).
  - Pick a descriptive name for your feature. Use kebab case ("my-cool-feature").
    Do not assign a HIPE number.
  - Create a folder under `text/` for your feature, using the chosen name.
    Copy `0000-template.md` to `text/<your folder name>/README.md`.
  - Fill in the HIPE. Put care into the details: HIPEs that do not present
    convincing motivation, demonstrate an understanding of the impact of the
    design, or are disingenuous about the drawbacks or alternatives tend to be
    poorly received. You can add supporting artifacts, such as diagrams and sample
    data, in the HIPE's folder.
  - Submit a pull request. As a pull request, the HIPE will receive design
    feedback from the larger community, and the author should be prepared to
    revise it in response.
  - Build consensus and integrate feedback. HIPEs that have broad support are
    much more likely to make progress than those that don't receive any
    comments. Feel free to reach out to the HIPE assignee, in particular, to get
    help identifying stakeholders and obstacles.
  - The maintainers will assign your HIPE a number. You will need to update your
    PR to change the name from `<my-cool-feature-name>` to something like
    `0097-my-cool-feature-name`. HIPEs rarely go through this process with only
    a number assignment, especially as alternatives
    and drawbacks are shown. You can make edits, big and small, to the HIPE to
    clarify or change the design, but make changes as new commits to the pull
    request, and leave a comment on the pull request explaining your changes.
    Specifically, do not squash or rebase commits after they are visible on the
    pull request.
  - At some point, a maintainer will propose a "motion for Final
    Comment Period" (FCP), along with a *disposition* for the HIPE (merge, close,
    or postpone).
    - This step is taken when enough of the tradeoffs have been discussed that
    maintainers are in a position to make a decision. That does not require
    consensus amongst all participants in the HIPE thread (which is usually
    impossible). However, the argument supporting the disposition on the HIPE
    needs to have already been clearly articulated, and there should not be a
    strong consensus *against* that position. Maintainers
    use their best judgment in taking this step, and the FCP itself
    ensures there is ample time and notification for stakeholders to push back
    if it is made prematurely.
    - For HIPEs with a lengthy discussion, the motion to FCP is usually preceded by
      a *summary comment* trying to lay out the current state of the discussion
      and major tradeoffs/points of disagreement.
  - The FCP lasts ten calendar days, so that it is open for at least 5 business
    days. It is also advertised widely,
    e.g. on mailing lists and slack. This way all
    stakeholders have a chance to lodge any final objections before a decision
    is reached.
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

Modifications to "active" HIPEs can be done in follow-up pull requests. We
strive to write each HIPE in a manner that it will reflect the final design of
the feature; but the nature of the process means that we cannot expect every
merged HIPE to actually reflect what the end result will be at the time of the
next major release.

In general, once accepted, HIPEs should not be substantially changed. Only very
minor changes should be submitted as amendments. More substantial changes
should be new HIPEs, with a note added to the original HIPE. Exactly what counts
as a "very minor change" is up to the maintainers to decide.


## Reviewing HIPEs
[Reviewing HIPEs]: #reviewing-hipes

While the HIPE pull request is up, the maintainers may schedule meetings with the
author and/or relevant stakeholders to discuss the issues in greater detail,
and in some cases, the topic may be discussed at a sub-team meeting. In either
case, a summary of the meeting will be posted back to the HIPE pull request.

Maintainers make final decisions about HIPEs after the benefits and drawbacks
are well understood. These decisions can be made at any time.
When a decision is made, the HIPE pull request
will either be merged or closed. In either case, if the reasoning is not clear
from the discussion in the thread, the maintainers will add a comment describing the
rationale for the decision.


## Implementing a HIPE
[Implementing a HIPE]: #implementing-a-hipe

Some accepted HIPEs represent vital features that need to be implemented right
away. Other accepted HIPEs can represent features that can wait until some
arbitrary developer feels like doing the work. Every accepted HIPE has an
associated issue tracking its implementation in [indy's jira](https://jira.hyperledger.org/projects/INDY/issues); thus that
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


[developer chat]: http://chat.hyperledger.org/#indy-sdk
[HIPE issue tracker]: https://github.com/hyperledger/indy-hipe/issues
[HIPE repository]: http://github.com/hyperledger/indy-hipe

## Known Protocols
[Known Protocols]: #known-protocols

Here is a summary of [known protocols](known-protocols.md) that are implemented in one or more Indy Agents. Some of the protocols are standardized, and therefore MUST be supported by all Indy Agents, where as some are informal specifications that are interoperable between only one or a few agent implementations. For the sake of developer discovery and to reduce overlap, these are included in here as well.

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