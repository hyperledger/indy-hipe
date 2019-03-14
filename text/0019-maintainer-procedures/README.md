# 0019: Maintainer Procedures
- Name: maintainer-procedures
- Author: BurdettAdam
- Start Date: 7/23/2018
- PR: https://github.com/hyperledger/indy-hipe/pull/23

## Summary
[summary]: #summary

This documents the best practices used for maintaining Hyperledger Indy Projects and details procedure for contributing to Hyperledger Indy source code and adding new maintainers. This HIPE includes a standard to incorporate CODING-CONVENTIONS markdown file in every project, outlining coding best practices. As well as a MAINTAINERS markdown file outlining maintainers and contributors. 

## Motivation
[motivation]: #motivation

We need official documentation outlining Indy maintainer's processes so they can easily be linked to and publicly accessible.
## Terminology 
### Stakeholder
A stakeholder submits bugs, asks questions, advocates for features, and participates in debates, design discussions, working groups, and is an active member of the community. A stakeholder only needs a Linux foundation account to create Jira tickets, no GitHub account is required.
### Submitter
A submitter donates code, documentation, and other tangible artifacts via pull request. A submitter needs a GitHub account for creating private forks, submitting pull requests, and reviewing code.
### Maintainer
A maintainer helps contributions by providing technical leadership, actively shepherding the evolution of the technology and promoting high-quality standards. Project maintainers are named in MAINTAINERS.md of each project. Maintainers have write/merge privileges in GitHub (requires GitHub “contributor” but having these privileges doesn’t automatically make you a maintainer)
### Guide
A guide consults on vision, core principles, priorities, and best practices. Included in guides may be inactive founders of a codebase, product managers, others with a strong business or community viewpoint. Guides have a GitHub status with the ear and trust of maintainers.

### CODING-CONVENTIONS&#46;md 
A markdown file containing code quality guidelines. Each Hyperledger Indy project has(should have) this file in the root directory outlining best coding practices and conventions used in that project. This file includes details for using Test Driven Development (TDD). 

### MAINTAINERS&#46;md
A markdown file containing information about maintainers and contributors.

## Tutorial
[tutorial]: #tutorial
### Contributing
#### Code Quality Guideline
See CODING-CONVENTIONS.md in the root directory of any project for best practices and detailed conventions. 
##### General Guidelines
- Follow incremental re-factoring approach: 
    - do not hesitate to improve the code
    - put TODO and FIXME comments if you see an issue in the code
    - log tickets in related [Indy Jira](https://jira.hyperledger.org/secure/Dashboard.jspa) project if you see an issue
- Write good tests
    - Follow TDD, write tests first, then the code
    - Have Unit tests where possible/necessary
- Document your code
    - Documentation is important; code simply doesn't exist until its documented. Indy projects generate documentation from inline comments. Please make sure to document all contributions following each projects CODING-CONVENTIONS outlining this process.
- Respect other stylistic and design choices until you build street cred
- Understand your projects licenses: don’t contribute anything encumbered by copyright or patent issues.
- Communicate proactively and pragmatically.
- Try to be informed before you ask questions (wiki, chat, design docs, Jira).
#### How To Submit A Pull Request
1. Search Jira for feature/fix ticket, claim (or write a new ticket) and assign it to yourself.
2. Make a private fork of the repo.
3. Write good code, including unit tests (TDD!), sign (DCO sign-off) all of your commits. Observe best practices and style guidelines as documented in the relevant CODING-CONVENTIONS.md file. Make sure that any new feature or fix is covered by tests.
4. Confirm that all tests pass and any documentation is updated according to your changes.
5. Submit a pull request to the master branch. Remeber to provide a full description of changes in the pull request including Jira ticket numbers. Make sure that all commits have a DCO sign-off from the commit author. Add detailed notes for testing. If reviewer needs to run explicit tests, add `test this please` comment to the pull request with any needed instructions.
6. Announce your pull request on `#indy-pr-review`  [channel](https://chat.hyperledger.org/channel/indy-pr-review) in Rocket.Chat. Tag someone to review, and post "Please review:(pull request URL)". Must tag maintainer(s) if the change is big/significant/risky.
7. Move Jira ticket to “Code Review” status and assign to your reviewer.
8. Monitor for comments. A reviewer needs to review the code and approve the pull request. If there are review comments, they will be put into the pull request itself. You must process them, feel free to reply in the pull request thread or have a discussion in Rocket.Chat if needed. If a pull request is not addressed within 24 (business) hours, escalate on Rocket.Chat. If PR is not addressed within 48 (business) hours, escalate to a guide.
9. A reviewer or maintainer will merge the pull request, at this point feel free to post your success on social media.
#### General Notes
- Do not create big pull requests; send a pull request for one feature or bug fix only.
 If a feature is too big, consider splitting a big PR to a number of small ones.
- Consider creating a design document in the `design` folder (as markdown or PlantUML diagram) in the corresponding project outlining the new feature before implementing it. For significant features create a HIPE and get community input before starting. 
    
### Adding New Maintainers
#### Maintainer Eligibility Status
After a developer has been established as a contributor of a project, having had several pull requests merged into master, they become eligible for maintainership.
#### Maintainer Status
For a developer to become a maintainer they must reach eligibility status. After eligibility status, a developer can be nominated for maintainership of a project. Nomination does not have to originate from any particular place, a developer can nominate himself. After a nomination has been published by indy maintainer email or in indy maintainer meeting, all maintainers will vote for the nominee to become a maintainer. After a vote, there will be a short waiting period for maintainers to express any concerns about candidate's maintainership and appropriate resolutions.
### Maintainer Process
#### Committing Code
Maintainers must have their code reviewed before merging into master. This directly means maintainers work from forks and issue a pull request that is reviewed and accepted by other maintainers. Branches of the master are discouraged and only allowed after a HIPE agreeing and outlining said branch. Maintainers directly committing to master is a violation of this process and maintainership, which is a punishable offense. 

#### Reviewing Pull Request
Reviewers should promote best practices outlined in relevant CODING-CONVENTIONS.md file. When reviewing pull requests, ask questions of this nature.
- Functionality: does the new code work without breaking anything old?
- Tests: do new tests pass? Are there enough tests for the right things?
- Quality: is the code clean, well encapsulated, simple, and conformant to our style guidelines? Does it make wise choices about refactoring?
- Safety: Does the code avoid new dependencies or IP encumbrances?

Reviewers:
1. Use GitHub review to give feedback. Don’t be afraid to ask for enhancements. If you can’t accept pull request without a change, use “Please change…”.
2. If the review is favorable, assign Jira ticket to maintainer with a note to merge.
3. Ping maintainer and submitter on chat with the status update.
4.  When in doubt, escalate (e.g., to maintainers) on chat or in community calls. Maintainers can convene conversations with guides as needed. Reviewers should not hold up a commit looking for perfection (remember, refactoring is a lifestyle). However, don’t approve code that isn’t ready for master/stable branch.
#### Ownership
- Maintainers are expected to be well informed, unselfish, accessible, and good (proactive) communicators.
- Multiple maintainers are desirable for timezone convenience.
- Maintainers and other key contributors are identified in MAINTAINERS.md.
- Any folder can have a MAINTAINERS.md; subfolders override. [Shards]
- Maintainers keep MAINTAINERS.md (and relevant GitHub privileges ) up-to-date. If you’d like to own something, ask the current owner. If you don’t want to own it anymore, tell the owner of your parent folder.
- Some folders might have shared scope (e.g., docs, samples); all associated maintainers cooperate to keep them in good shape.
#### Build Protocols
- A build is “broken” if any automated processes (compile, package, test, etc) fail.
- Anybody can institute automated build processes, but only ones endorsed by maintainers are normative.
- A broken build in the master is an urgent team emergency because it halts all productive work by others. Whoever discovers, report to @all on associated projects Rocket.Chat channel immediately, and claim ownership or find an owner.
- Maintainers fix breaks in their scope; default is to revert a problematic change.
- Submitters should plan to be available for troubleshooting after a pull request is merged. Maintainers will make any logs available related to new issues. Submitters should proactively debug and reach out to maintainers if they notice an undiscovered issue.

## Reference
[reference]: #reference
- Not Available
## Drawbacks
[drawbacks]: #drawbacks
- Having more process for maintainership could hinder code contributions from the open source community. 
## Rationale and alternatives
[alternatives]: #alternatives
- Outlined process for contributing and maintaining, improves the integrity and quality of our source code.
## Prior Art
[prior-art]: #prior-art
- This process has been used in the indy-node project with success. Extending it to Hyperledger Indy projects, in general, will be beneficial.
https://github.com/hyperledger/indy-node#how-to-send-a-pr
https://github.com/hyperledger/indy-node/blob/master/docs/write-code-guideline.md
https://github.com/hyperledger/indy-node#how-to-contribute 

## Unresolved Questions
[unresolved]: #unresolved-questions
- In how to submit a pull request we reference a reviewer, but a reviewer is not defined in the terminology, should it be?
- How do we remove old maintainers? 
- How do we enforce maintainer procedure?
- How do we resolve concerns and issues with maintainer nominees?
- How can a developer become a guide?