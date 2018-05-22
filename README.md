# indy-hiip

This repo holds HIIPs (Hyperledger Indy Improvement Proposals, pronounced like "hip"
for short) for chunks of technology or process that are important to standardize
across the Indy ecosystem.

Many changes, including bug fixes and documentation improvements, can just
be implemented and reviewed via the normal GitHub pull request workflow.
Some changes, though, are "substantial"; these are the ones where a HIIP
helps to produce a consensus and shared understanding in the community. The
HIIP process is documented below.

##### Note: this repo and the improvement proposal process it embodies has a special relationship with [sovrin-sip](https://github.com/sovrin-foundation/sovrin-sip/blob/master/README-sovrin.md) and possibly similar layered standards. Please see [derivative networks](derivative-networks.md) for details.

## Table of Contents
[Table of Contents]: #table-of-contents

  - [When you need to follow this process]
  - [Before creating an HIIP]
  - [What the process is]
  - [The HIIP lifecycle]
  - [Reviewing HIIPs]
  - [Implementing an HIIP]
  - [HIIP Postponement]
  - [Help this is all too informal!]
  - [License]


## When you need to follow this process
[When you need to follow this process]: #when-you-need-to-follow-this-process

You need to follow this process if you intend to make "substantial" changes to
Indy, Indy-SDK, or the HIIP process itself. What constitutes a
"substantial" change is evolving based on community norms and varies depending
on what part of the ecosystem you are proposing to change.

Some changes do not require a HIIP:

  - Rephrasing, reorganizing, refactoring, or otherwise "changing shape does
    not change meaning."
  - Additions that strictly improve objective, numerical quality criteria
    (warning removal, speedup, better platform coverage, more parallelism, trap
    more errors, etc.)
  - Additions only likely to be _noticed by_ other developers-of-indy,
    invisible to users-of-indy.

If you submit a pull request to implement a new feature without going through
the HIIP process, it may be closed with a polite request to submit a HIIP first.

## Before creating a HIIP
[Before creating a HIIP]: #before-creating-a-HIIP

A hastily proposed HIIP can hurt its chances of acceptance. Low quality
proposals, proposals for previously rejected features, or those that don't fit
into the near-term roadmap, may be quickly rejected, which can be demotivating
for the unprepared contributor. Laying some groundwork ahead of the HIIP can
make the process smoother.

Although there is no single way to prepare for submitting a HIIP, it is
generally a good idea to pursue feedback from other project developers
beforehand, to ascertain that the HIIP may be desirable; having a consistent
impact on the project requires concerted effort toward consensus-building.

The most common preparations for writing and submitting a HIIP include talking
the idea over on #indy and #indy-sdk, discussing the topic on our community
calls (see the []Hyperledger Community Calendar](https://wiki.hyperledger.org/community/calendar-public-meetings)),
and occasionally posting "pre-HIIPs" on the mailing lists. You may file issues
on this repo for discussion, but these are not actively looked at by the teams.

As a rule of thumb, receiving encouraging feedback from long-standing project
developers, and particularly members of the relevant sub-team is a good
indication that the HIIP is worth pursuing.

## What the process is
[What the process is]: #what-the-process-is

In short, to get a major feature added to Indy, one must first get the HIIP
merged into the HIIP repository as a markdown file. At that point the HIIP is
"active" and may be implemented with the goal of eventual inclusion into Indy.

  - Fork [the HIIP repo](https://github.com/hyperledger/indy-hiip).
  - Pick a descriptive name for your feature. Use kebab case ("my-cool-feature").
    Do not assign a HIIP number.
  - Create a folder under `text/` for your feature, using the chosen name.
    Copy `0000-template.md` to `text/<your folder name>/README.md`.
  - Fill in the HIIP. Put care into the details: HIIPs that do not present
    convincing motivation, demonstrate understanding of the impact of the
    design, or are disingenuous about the drawbacks or alternatives tend to be
    poorly received. You can add supporting artifacts such as diagrams and sample
    data, in the HIIP's folder.
  - Submit a pull request. As a pull request the HIIP will receive design
    feedback from the larger community, and the author should be prepared to
    revise it in response.
  - Build consensus and integrate feedback. HIIPs that have broad support are
    much more likely to make progress than those that don't receive any
    comments. Feel free to reach out to the HIIP assignee in particular to get
    help identifying stakeholders and obstacles.
  - The maintainers will assign your HIIP a number. You will need to update your
    PR to change the name from `<my-cool-feature-name>` to something like
    `0097-my-cool-feature-name`. HIIPs rarely go through this process with only
    a number assignment, especially as alternatives
    and drawbacks are shown. You can make edits, big and small, to the HIIP to
    clarify or change the design, but make changes as new commits to the pull
    request, and leave a comment on the pull request explaining your changes.
    Specifically, do not squash or rebase commits after they are visible on the
    pull request.
  - At some point, a maintainer will propose a "motion for Final
    Comment Period" (FCP), along with a *disposition* for the HIIP (merge, close,
    or postpone).
    - This step is taken when enough of the tradeoffs have been discussed that
    maintainers are in a position to make a decision. That does not require
    consensus amongst all participants in the HIIP thread (which is usually
    impossible). However, the argument supporting the disposition on the HIIP
    needs to have already been clearly articulated, and there should not be a
    strong consensus *against* that position. Mainters
    use their best judgment in taking this step, and the FCP itself
    ensures there is ample time and notification for stakeholders to push back
    if it is made prematurely.
    - For HIIPs with lengthy discussion, the motion to FCP is usually preceded by
      a *summary comment* trying to lay out the current state of the discussion
      and major tradeoffs/points of disagreement.
  - The FCP lasts ten calendar days, so that it is open for at least 5 business
    days. It is also advertised widely,
    e.g. on mailing lists and slack. This way all
    stakeholders have a chance to lodge any final objections before a decision
    is reached.
  - In most cases, the FCP period is quiet, and the HIIP is either merged or
    closed. However, sometimes substantial new arguments or ideas are raised,
    the FCP is canceled, and the HIIP goes back into development mode.

## The HIIP lifecycle
[The HIIP lifecycle]: #the-hiip-lifecycle

Once a HIIP becomes "active" then authors may implement it and submit the
feature as a pull request to the Indy repo. Being "active" is not a rubber
stamp, and in particular still does not mean the feature will ultimately be
merged; it does mean that in principle all the major stakeholders have agreed
to the feature and are amenable to merging it.

Furthermore, the fact that a given HIIP has been accepted and is "active"
implies nothing about what priority is assigned to its implementation, nor does
it imply anything about whether a Indy developer has been assigned the task of
implementing the feature. While it is not *necessary* that the author of the
HIIP also write the implementation, it is by far the most effective way to see
a HIIP through to completion: authors should not expect that other project
developers will take on responsibility for implementing their accepted feature.

Modifications to "active" HIIPs can be done in follow-up pull requests. We
strive to write each HIIP in a manner that it will reflect the final design of
the feature; but the nature of the process means that we cannot expect every
merged HIIP to actually reflect what the end result will be at the time of the
next major release.

In general, once accepted, HIIPs should not be substantially changed. Only very
minor changes should be submitted as amendments. More substantial changes
should be new HIIPs, with a note added to the original HIIP. Exactly what counts
as a "very minor change" is up to the maintainers to decide.


## Reviewing HIIPs
[Reviewing HIIPs]: #reviewing-hiips

While the HIIP pull request is up, the maintainers may schedule meetings with the
author and/or relevant stakeholders to discuss the issues in greater detail,
and in some cases the topic may be discussed at a sub-team meeting. In either
case a summary from the meeting will be posted back to the HIIP pull request.

Maintainers make final decisions about HIIPs after the benefits and drawbacks
are well understood. These decisions can be made at any time.
When a decision is made, the HIIP pull request
will either be merged or closed. In either case, if the reasoning is not clear
from the discussion in thread, the maintainers will add a comment describing the
rationale for the decision.


## Implementing a HIIP
[Implementing a HIIP]: #implementing-a-hiip

Some accepted HIIPs represent vital features that need to be implemented right
away. Other accepted HIIPs can represent features that can wait until some
arbitrary developer feels like doing the work. Every accepted HIIP has an
associated issue tracking its implementation in [indy's jira](https://jira.hyperledger.org/projects/INDY/issues); thus that
associated issue can be assigned a priority via the triage process that the
team uses for all issues in the Indy repository.

The author of a HIIP is not obligated to implement it. Of course, the HIIP
author (like any other developer) is welcome to post an implementation for
review after the HIIP has been accepted.

If you are interested in working on the implementation for an "active" HIIP, but
cannot determine if someone else is already working on it, feel free to ask
(e.g. by leaving a comment on the associated issue).


## HIIP Postponement
[HIIP Postponement]: #hiip-postponement

Some HIIP pull requests are tagged with the "postponed" label when they are
closed (as part of the rejection process). A HIIP closed with "postponed" is
marked as such because we want neither to think about evaluating the proposal
nor about implementing the described feature until some time in the future, and
we believe that we can afford to wait until then to do so. Historically,
"postponed" was used to postpone features until after 1.0. Postponed pull
requests may be re-opened when the time is right. We don't have any formal
process for that, you should ask members of the relevant sub-team.

Usually a HIIP pull request marked as "postponed" has already passed an
informal first round of evaluation, namely the round of "do we think we would
ever possibly consider making this change, as outlined in the HIIP pull request,
or some semi-obvious variation of it." (When the answer to the latter question
is "no", then the appropriate response is to close the HIIP, not postpone it.)


### Help this is all too informal!
[Help this is all too informal!]: #help-this-is-all-too-informal

The process is intended to be as lightweight as reasonable for the present
circumstances. As usual, we are trying to let the process be driven by
consensus and community norms, not impose more structure than necessary.


[developer chat]: http://chat.hyperledger.org/#indy-sdk
[HIIP issue tracker]: https://github.com/hyperledger/indy-hiip/issues
[HIIP repository]: http://github.com/hyperledger/indy-hiip

## License
[License]: #license

This repository is licensed under an [Apache 2 License](LICENSE).

### Contributions

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall be
dual licensed as above, without any additional terms or conditions.
