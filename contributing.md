[//]: # (SPDX-License-Identifier: CC-BY-4.0)

# ![Indy HIPEs](collateral/indy-hipes-logo.png)

## Contributing

### Do you need a HIPE?

Use a HIPE to advocate substantial changes to the Indy ecosystem, where
those changes need to be understood by developers who *use* Indy. Minor
changes are not HIPE-worthy, and changes that are internal in nature,
invisible to those consuming Indy, should be documented elsewhere.

### Preparation

Before writing a HIPE, consider exploring the idea on
[chat](https://chat.hyperledger.org/channel/indy-sdk), on community calls
(see the [Hyperledger Community Calendar](
https://wiki.hyperledger.org/community/calendar-public-meetings)),
or on [indy@lists.hyperledger.org](
mailto:indy@lists.hyperledger.org). Encouraging feedback from maintainers
is a good sign that you're on the right track.

### How to propose a HIPE

  - Fork [the HIPE repo](https://github.com/hyperledger/indy-hipe).
  - Pick a descriptive folder name for your HIPE. Use existing names as
    a pattern.
  - Create the folder and copy `0000-template.md` to `text/<your folder name>/README.md`.
  - Fill in the HIPE. Put care into the details: HIPEs that do not present
    convincing motivation, demonstrate an understanding of the impact of the
    design, or are disingenuous about the drawbacks or alternatives tend to be
    poorly received. You can add supporting artifacts, such as diagrams and sample
    data, in the HIPE's folder.
  - Assign a number to your HIPE. Get the number by inspecting open and closed PRs against
    this repo to figure out what the next PR number will be. Rename your folder from
    `<your folder name>` to `<your 4-digit number>-<your folder name>`. At the
    top of your README.md, modify the title so it is in the form: `<your 4-digit
    number>: Friendly Version of Your Title`. Commit your changes.
  - In the root of the repo, run `python code/generate_index.py` to update the index
    with your new HIPE.
  - In the root of your repo, run 'pytest code` to see whether your HIPE passes all
    automated tests. The HIPE tests are simple. They just check for things like
    naming conventions and hyperlink correctness.
  - Commit the updated version of `/index.md` and push your changes.
  - Submit a pull request.

Make sure that all of your commits satisfy the [DCO requirements](
https://github.com/probot/dco#how-it-works) of the repo and conform
to the license restrictions noted [below](#intellectual-property).

The HIPE Maintainers will check to see if the process has been followed, and request
any process changes before merging the PR.

When the PR is merged, your HIPE is now formally in the PROPOSED state.

### How to get a HIPE accepted

After your HIPE is merged and officially acquires the [PROPOSED status](
README.md#status--proposed), the HIPE will receive feedback from the larger community,
and the author should be prepared to revise it. Updates may be made via pull request,
and those changes will be merged as long as the process is followed.

When you believe that the HIPE is mature enough (feedback is somewhat resolved,
consensus is emerging, and implementation against it makes sense), submit a PR that
changes the status to [ACCEPTED](README.md#status--accepted). The status change PR
will remain open until the maintainers agree on the status change.

>NOTE: contributors who used the Indy HIPE process prior to May 2019 should
see the acceptance process substantially simplified under this approach.
The bar for acceptance is not perfect consensus and all issues resolved;
it's just general agreement that a doc is "close enough" that it makes
sense to put it on a standards track where it can be improved as
implementation teaches us what to tweak.

### How to get a HIPE adopted

An accepted HIPE is a standards-track document. It becomes an acknowledged
standard when there is evidence that the community is deriving meaningful
value from it. So:

- Implement the ideas, and find out who else is implementing.
- Socialize the ideas. Use them in other HIPEs and documentation.
- Update the agent test suite to reflect the ideas.

When you believe a HIPE is a _de facto_ standard, raise a PR that changes the
status to [ADOPTED](README.md#status--adopted).  If the community is friendly
to the idea, the doc will enter a two-week "Final Comment Period" (FCP), after
which there will be a vote on disposition.

### Intellectual Property

This repository is licensed under a Create Commons [Attribution 4.0 International (CC BY 4.0)](LICENSE).
It is protected by a [Developer Certificate of Origin](https://developercertificate.org/) on every commit.
This means that any contributions you make must be licensed in an CC-BY-4.0-compatible
way, and must be free from patent encumbrances or additional terms and conditions. By
raising a PR, you certify that this is the case for your contribution.
