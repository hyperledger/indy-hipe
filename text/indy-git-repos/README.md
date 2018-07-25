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

The Hyperledger Indy Project is composed of several repositories that serve a verity purposes. Some of 
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
This repository has existed through out most of the existence of what is now called Indy. This repository was
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

## indy-sdk

[GitHub Link](https://github.com/hyperledger/indy-sdk) (see the README)

### Description
The official SDK for Hyperledger Indy. Contains code, tools, and other artifacts that provide a foundation for
interacting with an Indy pool and fundamental building blocks for self-sovereign identity.


### Maintenance
This repository will be maintained by the Indy Project maintainers. PRs submitted to this repository will follow 
the standard review process. It will party to the CI system that runs for the Indy Project. 


## indy-hipe

[GitHub Link](https://github.com/hyperledger/indy-hipe) (see the README)

### Description
This repository holds HIPEs for chunks of technology or process that are important to standardize across the 
Indy ecosystem.


### Maintenance
This repository will be maintained by the Indy Project maintainers. PR submitted to this repository will follow the 
HIPE process that is documented in the repository itself.

## indy-crypto

[GitHub Link](https://github.com/hyperledger/indy-crypto) (see the README)

### Description
Contains shared cryptographic codebase for the Indy project. Ideally, all cryptographic code will be maintained in
this single repository.


### Maintenance
This repository will be maintained by the Indy Project maintainers. PRs submitted to this repository will follow 
the standard review process. It will party to the CI system that runs for the Indy Project. 

## indy-agent

[GitHub Link](https://github.com/hyperledger/indy-agent) (see the README)

### Description
Contains official reference agent implementations. 


### Maintenance


## indy-test-automation

[GitHub Link](https://github.com/hyperledger/indy-test-automation) (see the README)

### Description
Contains a gathering place for scripts and other pieces of automation used in integration, acceptance and 
stability testing. Most not replace proper testing resources in other repositories. But test resources that 
span multiple repositories in function and scope can find a home here.  


### Maintenance
Maintainers:

- Indy Integration Tests - Steve Lafranca
- Indy Chaos - Corin Kochenower  

## indy-jenkins-pipeline-lib

[GitHub Link](https://github.com/hyperledger/indy-jenkins-pipeline-lib) (see the README)

### Description
Contains shared CI/CD scripts and other assets. 

### Maintenance

## indy-anoncreds

[GitHub Link](https://github.com/hyperledger/indy-anoncreds) (see the README)

### History
Existed prior to Indy joining. The python client that was/is in Indy-Node makes use of this implementation. Since
then, indy-sdk has re-implemented the protocol. 

### Description
Python implementation of the Anonymous Credentials protocol.   

### Maintenance