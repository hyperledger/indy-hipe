- Name: indy-git-repos
- Author: Devin Fisher, Nathan George
- Start Date: 2018-07-24
- PR: (leave this empty)
- Jira Issue: (leave this empty)

# Summary
[summary]: #summary

Provide an single place to document the list of source control repositories that compose 
the Indy Project. As a HIPE, this documented list can be modified in the future via the HIPE process 
(via PR the augment this document or future HIPEs that supplant this HIPE).

# Motivation
[motivation]: #motivation

The Hyperledger Indy Project is composed of several repositories that serve a verity purposes. Some of 
these repos have code that is critical to running or using an Indy identity system. Others serve a more auxiliary
role. Like the indy-hipe repo this document reside in. These repositories have been created largely add-hoc as the
need arose. Concerns about how new repositories fit into the Indy project were generally not discussed and were not
discussed in a way accessible to all participants to the project. 

With that in mind, this HIPE will serve two purpose:
1. Document the repositories that compose the Hyperledger Indy Project in the context of the project as a whole. (will 
not replace README contained in the repository itself)
2. Allow a process (via HIPEs) to propose new repositories, renaming repositories or other changes the current 
repositories. This process will allow for all concerns to be addressed in a public forum.
  

# Repositories
[tutorial]: #Repositories

## indy-node

[GitHub Link](https://github.com/hyperledger/indy-node) (see the README)

### History
This repository has existed through out most of existence of what is now called Indy. This repository was
created when the node elements that concerned the Sovrin was spit from the RBFT ledger. This happened before
the project was part of Hyperledger. When the project joined Hyperledger, this repository was joined with a
client and common repository.
 
### Description
This is the flag ship repository of the Hyperledger Indy Project. This repository embodies all artifacts 
that are used to run a node in a Indy network. These artifacts includes code for an Indy node, scripts for 
administration of an Indy Node, tools for working with a Indy Node and documentation about a Indy Node. 

### Maintenance
This repository will be maintained by the Indy Project maintainers. PRs submitted to this repository will follow 
the standard review process. It will party to the CI system that run for the Indy Project. 


## indy-plenum

[GitHub Link](https://github.com/hyperledger/indy-plenum) (see the README)

### History
This repository is the oldest surviving repository in the Indy Project. It existed before Indy joined hyperledger. 
It has gone through several iterations but has always contained the codebase currently called Plenum. When the project
joined Hyperledger, this repository was joined with several small upstream dependent repos. They combine to create the
current form.
 
### Description
Contains the core technology for the Indy Project. This repository contains the code for the RBFT protocol ledger that 
is purpose built for the project. 


### Maintenance
This repository will be maintained by the Indy Project maintainers. PRs submitted to this repository will follow 
the standard review process. It will party to the CI system that run for the Indy Project. 

## indy-sdk

[GitHub Link](https://github.com/hyperledger/indy-sdk) (see the README)

## indy-hipe

[GitHub Link](https://github.com/hyperledger/indy-hipe) (see the README)

## indy-crypto

[GitHub Link](https://github.com/hyperledger/indy-crypto) (see the README)

## indy-agent

[GitHub Link](https://github.com/hyperledger/indy-agent) (see the README)

## indy-test-automation

[GitHub Link](https://github.com/hyperledger/indy-test-automation) (see the README)

## indy-jenkins-pipeline-lib

[GitHub Link](https://github.com/hyperledger/indy-jenkins-pipeline-lib) (see the README)

## indy-anoncreds

[GitHub Link](https://github.com/hyperledger/indy-anoncreds) (see the README)






