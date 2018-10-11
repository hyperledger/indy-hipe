- Name: indy-git-repos
- Author: Devin Fisher, Nathan George
- Start Date: 2018-07-24
- PR: (leave this empty)
- Jira Issue: (leave this empty)

# HIPE 0018-indy-git-repos
[summary]: #summary

Main purpose of this HIPE is to define repository structure of the Indy Project by answering the following questions:
- what repositories compose the Indy Project
- what is the purpose of each of the repositories
- how are changes to the repository structure made
- how are these repositories maintained

This documented list can be modified in the future via the HIPE process:
- by submitting a PR that augments this document or 
- by submitting a future HIPE that will supplant this one

# Motivation
[motivation]: #motivation

The Hyperledger Indy Project is composed of several repositories that serve a variety of purposes. Some of these 
repositories have code that is critical for running or using an Indy identity system, while others serve a more auxiliary
role. These repositories have been created largely ad-hoc as the need arose, and the concerns about how new repositories
fit into the Indy project were generally not discussed in a way accessible to all participants to the project. 

With that in mind, this HIPE will serve two purposes:
1. Document the repositories that compose the Hyperledger Indy Project in the context of the project as a whole. (will 
not replace README contained in the repository itself)
2. Allow for a process (via HIPEs) to propose new, rename existing, or make other changes to the specified repositories.
This process will allow for all concerns to be addressed in a public forum.

# Repositories
[repositories]: #repositories

## indy-node
 
Contains all artifacts that are used to run a node in an Indy network including:
- indy node implementation
- administration scripts
- tools for working with Indy Node and 
- documentation

#### History

This repository has existed throughout most of the existence of what is now called Indy. This repository was created
when the node elements that concerned the Sovrin was split from the RBFT ledger. This happened before the project was
part of Hyperledger. When the project joined Hyperledger, this repository was joined with a client and common repository.

[GitHub Link](https://github.com/hyperledger/indy-node) (see the README)

[Maintainers Doc](https://github.com/hyperledger/indy-node/blob/master/MAINTAINERS.md)

## indy-plenum
 
Contains the code for the RBFT protocol ledger that is purpose-built for the Indy Project.

#### History

This repository is the oldest surviving repository in the Indy Project. It existed before Indy joined Hyperledger. It
has gone through several iterations but has always contained the codebase currently called Plenum. When the project
joined Hyperledger, this repository was joined with several small upstream dependent repositories. They combine to
create the current form.

[GitHub Link](https://github.com/hyperledger/indy-plenum) (see the README)

[Maintainers Doc](https://github.com/hyperledger/indy-plenum/blob/master/MAINTAINERS.md)

## indy-sdk

Contains core libraries, language wrappers, tools, documentation, and other artifacts that enable developers to build
Self-sovereign applications on top of the Indy platform. Exposed functionality includes managing connections to Indy 
Node pools, digital wallets, crypto functions, credentials, etc.

It is the official software development kit (SDK) for the Indy Project, and as such presents a main source of technology
for non-community members.

[GitHub Link](https://github.com/hyperledger/indy-sdk) (see the README)

[Maintainers Doc](https://github.com/hyperledger/indy-sdk/blob/master/MAINTAINERS.md)

## indy-hipe

This repository holds HIPEs (Hyperledger Indy Project Enhancements) which is the Indy Project process for project
collaboration and forming project standards.

[GitHub Link](https://github.com/hyperledger/indy-hipe) (see the README)

[Maintainers Doc](https://github.com/hyperledger/indy-hipe/blob/master/MAINTAINERS.md)

## indy-crypto

Contains shared cryptographic codebase for the Indy Project. Ideally, all cryptographic code will be maintained in
this single repository.

[GitHub Link](https://github.com/hyperledger/indy-crypto) (see the README)

[Maintainers Doc](https://github.com/hyperledger/indy-crypto/blob/master/MAINTAINERS.md)

## indy-agent

Contains official Indy Project reference agent implementations and agent protocols test suite.

[GitHub Link](https://github.com/hyperledger/indy-agent) (see the README)

[Maintainers Doc](https://github.com/hyperledger/indy-agent/blob/master/MAINTAINERS.md)

## indy-test-automation

Contains a gathering place for scripts and other pieces of automation used for integration, acceptance, and
stability testing of Indy Project components.

Test resources that span multiple repositories in function and scope can find a home here.  

[GitHub Link](https://github.com/hyperledger/indy-test-automation) (see the README)

[Maintainers Doc](https://github.com/hyperledger/indy-test-automation/blob/master/MAINTAINERS.md)

## indy-jenkins-pipeline-lib

Contains a library of reusable Jenkins Pipeline steps and functions for that are used in Hyperledger Indy Projects' CI/CD 
pipelines. 

[GitHub Link](https://github.com/hyperledger/indy-jenkins-pipeline-lib) (see the README)

[Maintainers Doc](https://github.com/hyperledger/indy-jenkins-pipeline-lib/blob/master/MAINTAINERS.md)

# Maintenance
[maintenance]: #maintenance

Unless otherwise specified repositories will be maintained by Indy Project maintainers. Every repository will define
specific contribution procedures, and submitted PRs will follow the standard review process. It will party to the CI 
system that runs for the Indy Project.
