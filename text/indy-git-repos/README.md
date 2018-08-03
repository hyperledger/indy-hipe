- Name: indy-git-repos
- Author: Devin Fisher, Nathan George
- Start Date: 2018-07-24
- PR: (leave this empty)
- Jira Issue: (leave this empty)

# Summary
[summary]: #summary

Provide a single place to document the list of source control repositories that compose 
the Indy Project. As a HIPE, this documented list can be modified in the future via the HIPE process 
(via PR the augment this document or future HIPEs that supplant this HIPE).

# Motivation
[motivation]: #motivation

The Hyperledger Indy Project is composed of several repositories that serve a verity of purposes. Some of 
these repositories have code that is critical to running or using an Indy identity system. Others serve a more auxiliary
role. Like the indy-hipe repository that this document resides in. These repositories have been created largely  ad-hoc 
as the need arose. Concerns about how new repositories fit into the Indy project were generally not discussed and were not
discussed in a way accessible to all participants to the project. 

With that in mind, this HIPE will serve two purposes:
1. Document the repositories that compose the Hyperledger Indy Project in the context of the project as a whole. (will 
not replace README contained in the repository itself)
2. Allow a process (via HIPEs) to propose new repositories, renaming repositories or other changes to the current 
repositories. This process will allow for all concerns to be addressed in a public forum.
  

# Repositories
[tutorial]: #Repositories

## indy-node

[GitHub Link](https://github.com/hyperledger/indy-node) (see the README)

### History
This repository has existed throughout most of the existence of what is now called Indy. This repository was
created when the node elements that concerned the Sovrin was spit from the RBFT ledger. This happened before
the project was part of Hyperledger. When the project joined Hyperledger, this repository was joined with a
client and common repository.
 
### Description
This is the flagship repository of the Hyperledger Indy Project. This repository embodies all artifacts 
that are used to run a node in an Indy network. These artifacts includes code for an Indy node, scripts for 
the administration of an Indy Node, tools for working with an Indy Node and documentation about an Indy Node. 

### Maintenance
This repository will be maintained by the Indy Project maintainers. PRs submitted to this repository will follow 
the standard review process. It will party to the CI system that runs for the Indy Project.

[Maintainers Doc](https://github.com/hyperledger/indy-node/blob/master/MAINTAINERS.md)


## indy-plenum

[GitHub Link](https://github.com/hyperledger/indy-plenum) (see the README)

### History
This repository is the oldest surviving repository in the Indy Project. It existed before Indy joined Hyperledger. 
It has gone through several iterations but has always contained the codebase currently called Plenum. When the project
joined Hyperledger, this repository was joined with several small upstream dependent repositories. They combine to 
create the current form.
 
### Description
Contains the core technology for the Indy Project. This repository contains the code for the RBFT protocol ledger that 
is purpose-built for the project. 


### Maintenance
This repository will be maintained by the Indy Project maintainers. PRs submitted to this repository will follow 
the standard review process. It will party to the CI system that runs for the Indy Project.

[Maintainers Doc](https://github.com/hyperledger/indy-plenum/blob/master/MAINTAINERS.md)

## indy-sdk

[GitHub Link](https://github.com/hyperledger/indy-sdk) (see the README)

### Description
The official software development kit (SDK) for Hyperledger Indy. Contains software that enables the creation of applications that can manage pool connections, digital wallets, and self-sovereign identity. The SDK core is written in rust with a c callable API and lives in /libindy. Current languages that utilize the c callable API include Python, NodeJs, Java, ios and dotnet. Language packages live in /wrappers. This repo also holds examples for using the SDK in /samples directory. As well as a command line interface(CLI) developer tool for assisting in application development that can be found in /cli. 

### Maintenance
This repository will be maintained by the Indy Project maintainers. PRs submitted to this repository will follow 
the standard review process which includes the HIPE process for any API breaking features. It will party to the CI system that runs for the Indy Project. 

[Maintainers Doc](https://github.com/hyperledger/indy-sdk/blob/master/MAINTAINERS.md)

## indy-hipe

[GitHub Link](https://github.com/hyperledger/indy-hipe) (see the README)

### Description
This repository holds HIPEs (Hyperledger Indy Project Enhancements) which is the project process collaboration 
on standardizing.


### Maintenance
This repository will be maintained by the Indy Project maintainers. PR submitted to this repository will follow the 
HIPE process that is documented in the repository itself.

[Maintainers Doc](https://github.com/hyperledger/indy-hipe/blob/master/MAINTAINERS.md)

[Maintainers Doc](https://github.com/hyperledger/indy-hipe/blob/master/MAINTAINERS.md)

## indy-crypto

[GitHub Link](https://github.com/hyperledger/indy-crypto) (see the README)

### Description
Contains shared cryptographic codebase for the Indy project. Ideally, all cryptographic code will be maintained in
this single repository.


### Maintenance
This repository will be maintained by the Indy Project maintainers. PRs submitted to this repository will follow 
the standard review process. It will party to the CI system that runs for the Indy Project.

[Maintainers Doc](https://github.com/hyperledger/indy-crypto/blob/master/MAINTAINERS.md)

## indy-agent

[GitHub Link](https://github.com/hyperledger/indy-agent) (see the README)

### Description
Contains official certified reference agent implementations and agent test suite.
Agent test suite is being developed and used to establish community agreed upon indy agent protocol.

### Maintenance

This repository will be maintained by the Indy Project maintainers. PRs submitted to this repository will follow the standard review process which includes the HIPE process for new message families. 


[Maintainers Doc](https://github.com/hyperledger/indy-agent/blob/master/MAINTAINERS.md)

## indy-test-automation

[GitHub Link](https://github.com/hyperledger/indy-test-automation) (see the README)

### Description
Contains a gathering place for scripts and other pieces of automation used in integration, acceptance and 
stability testing. Must not replace proper testing resources in other repositories. But test resources that 
span multiple repositories in function and scope can find a home here.  


### Maintenance
Key Maintainers:

- Indy Integration Tests - Steve Lafranca
- Indy Chaos - Corin Kochenower

[Maintainers Doc](https://github.com/hyperledger/indy-test-automation/blob/master/MAINTAINERS.md)

## indy-jenkins-pipeline-lib

[GitHub Link](https://github.com/hyperledger/indy-jenkins-pipeline-lib) (see the README)

### Description
Contains shared CI/CD scripts and other assets. 

### Maintenance

Key Maintainers:

- Andrey Kononykhin

[Maintainers Doc](https://github.com/hyperledger/indy-jenkins-pipeline-lib/blob/master/MAINTAINERS.md)

## indy-doc

[GitHub Link](https://github.com/hyperledger/indy-doc) (see the README)

### Description
Contains official indy documentation with accompanying scripts to generate documentation for read the docs hosting service.

### Maintenance
This repository will be maintained by Indy Project maintainers. PRs submitted to this repository will follow the standard review process.

[Maintainers Doc](https://github.com/hyperledger/indy-doc/blob/master/MAINTAINERS.md)
