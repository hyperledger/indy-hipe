- Name: new-hipe-process
- Author: Stephen Curran (swcurran@cloudcompass.ca)
- Start Date: 2018-11-08
- PR: 
- Jira Issue: 

# Summary
[summary]: #summary

This HIPE defines a new HIPE process that reduces the use of Pull Requests (PRs) to manage the life cycle of HIPEs.  Rather than long-lived PRs, folders are used to manage HIPEs, making them much more accessible to creators and reviewers.

# Motivation
[motivation]: #motivation

The current HIPE process is, quite frankly, a frustrating experience for most people. The steps are convoluted, or it requires far more GitHub knowledge than should be needed. The primary challenges to the current approach include:

* HIPE creators must manage multiple branches to support more than one HIPE in progress at a time. This is especially fun when one decides to start a new HIPE with one still in the Proposed state.
* The HIPE creator is somewhat at the "mercy" of a possibly indifferent community and the repo admins. The HIPE creator does not have any obvious way to push a HIPE forward.
* Those wanting to update (vs. comment) on a HIPE must fork the indy-hipe repo of the creator, and submit a PR there, which must then be managed by the creator.
* Those wanting to read HIPEs must know to go to the Pull Request list to find proposed HIPEs. Further, they must figure out how to navigate to the full text of the HIPE, which is not obvious.
* In general - the PR review process that works well for code is not effective for text documents like HIPEs.

While none of the technical issues above are particular difficult for hands-on developers (although they are a pain for text docs), they are an unnecessary overhead and a barrier for other participants.

The primary benefit that might be lost with this approach is that comments can be made as part of the PR process - a "first class" process in GitHub. However, there are multiple mechanisms that can be used to replace that challenge.

# Tutorial
[tutorial]: #tutorial

## Setup: New Folders added to the repo root

The following folders will be added to the root of the indy-hipe repo:

* proposed-hipes
* final-review-hipes
* accepted-hipes
* rejected-hipes
* archived-hipes

The README.md will be updated to reflect the new hipe process.  Existing HIPEs will be merged and immediately moved into the appropriate folders.

## Propose a new HIPE - Creator

Fork and clone the `hyperledger/indy-hipe` repo.

In the "proposed-hipes" folder, create a new folder named for the new HIPE (e.g. `new-hipe-process`), copy the `0000-template.md` file into the new folder and name it for the new hipe (e.g. `new-hipe-process/new-hipe-process.md`). Edit the new HIPE as appropriate based on the template and adding images to the same folder.  

When ready to submit the new HIPE, create an Issue in Hyperledger JIRA IndyHIPE (or using GitHub Issues) and paste a link to the Issue in the HIPE Header.

Submit a PR for the new HIPE.

Wait nervously for feedback and as received, update the HIPE.

## Receive a new HIPE - Admin

The repo admin reviews briefly the HIPE to make sure that the HIPE follows the rules for a new HIPE - that it is properly formatted, a JIRA exists, perhaps that the submitter is known (and connect with the HIPE creator if not), the DCO is included, etc.  Assuming so, the Proposed HIPE is merged.

On merge, the Creator announces the new HIPE on rocketchat and the Indy Mailing List.

## Provide Feedback - the Community

The community should review the HIPE and provide feedback through the JIRA or by doing a PR against the HIPE - possibly with changes, possibly just with embedded comments. Another option for line-by-line feedback would be to comment against the commit (or perhaps there is a better in-GitHub way?).

An example in-HIPE comment might be:

> From: Stephen Curran - Hey, this idea is not the best way to provide feedback. What about using GitHub Issues for commenting?

If PRs are submitted against the HIPE, the Admin would simply ensure that the comments are reasonable in following the process - not if they are good or bad. Admins would also break PR loops where several people are repeatedly adding/removing each other's changes.

## Promote the HIPE - Creator and/or Admin

When the community agrees - based on agreement (in JIRA or on Indy Maintainers calls), the Creator (usually) moves the HIPE folder into the folder for the next step in the life-cycle. From `proposed-hipes`, that would be to either or `final-review-hipes` or `rejected-hipes`. If moved to `final-review-hipes`, the Creator should again announce the change on the appropriate rocketchat channel and on the Indy Mailing List.

Per the current HIPE process - HIPEs can be moved forward if all comments are resolved and no further comments requiring resolution have been received for 2 weeks.

The repo Admin verifies the HIPE is to be moved (checking comments for resolution and time lapse) and accept/reject the PR.  Again, at that point the Admin's role is just to make sure the process is moving along correctly - not to add judgment on the content of the HIPE.

If the Creator does not move the HIPE forward in a timely fashion, an Admin can take that responsibility - often moving it to the `rejected-hipes` folder. Of course, that could be reversed if the Admin's action was not in line with the community's needs.

## Accept the HIPE

A HIPE in the `final-review-hipes` folder uses the same "Promote" process as above. The only difference is that prior to submitting the PR for the HIPE, the Creator should add a number to the HIPE folder (e.g. `0099-new-hipe-process`) by incrementing the number from the most recently approved HIPE.  Any collisions on numbers will be resolved by the Admin merging the PRs.

The Creator should announce the acceptance of the HIPE on the appropriate rocketchat channel and on the Indy Mailing List.

## Archive the HIPE

A HIPE that is obsolete would be moved by a contributor to the `archived-hipes` folder. To retain the permalink to the original HIPE, the folder in the `accepted-hipes` folder would be retained and the original HIPE document within that folder replaced with a document redirecting the reader to the new location of the HIPE, with an optional explanation of why the HIPE was archived.

The archiving of a HIPE would usually occur as a byproduct of the acceptance of a new HIPE or in conjunction with a request from the Indy-Maintainers group. The Admin reviewing the PR for the move should ensure that it is appropriate to move the HIPE before merging the PR.

The person submitting the PR to move the HIPE should announce the move on the appropriate rocketchat channel and the Indy Mailing List.

# Reference
[reference]: #reference

This approach eliminates the primary challenges with the existing approach:

- The HIPE creator is in control of the HIPE - moving it forward based on their interest while still following the rules of the community.
- No need to have multiple branches for managing multiple in process HIPEs.
- Easier for other contributors find, review and update a HIPE in progress. Updates are a simple PR.
- No need to have a knowledge of PRs and the tricks for navigating to the latest text of the PR.
- Easy scanning of the repo to see the HIPEs accepted and in progress. The status of a HIPE is much easier to discern.

# Drawbacks
[drawbacks]: #drawbacks

A (minor?) drawback is that direct comments associated with a specific line of text in the HIPE are not as easily created. Comments in the Issue (JIRA or GitHub Issue) are farther away from the specific line of text.

# Rationale and alternatives
[alternatives]: #alternatives

The current approach is the primary alternative. That approach is evidently used in other communities. It's not easy.

# Prior art
[prior-art]: #prior-art

This is a standard document life-cycle approach - the equivalent to tagging the current status of the HIPE by using separate folders.

# Unresolved questions
[unresolved]: #unresolved-questions

- The best approaches for providing feedback about proposed/final acceptance HIPEs.
