- Name: indy-docs-repo
- Author: Michael McKean mjmckean11@gmail.com
- Start Date: 2018-07-26
- PR: 
- Jira Issue:

# Summary
[summary]: #summary

Indy-docs is used to gather and build documentation from all Indy projects. Indy-docs' goal is to be the single place to direct new developers wanting to use Indy. Read The Docs is a platform that can accomplish this goal, compiling HTML documentation from the indy-docs repository.

# Motivation
[motivation]: #motivation

As more consumers begin to use the Hyperledger Indy technology, the need for a set of more consumer-facing documentation grows. While there are plenty of resources available currently (Hyperledger Wiki, Rocket.Chat, Github repositories, etc.), often there is confusion about where new users should first go. *The indy-docs repository provides this one-stop-shop for anyone looking to use or contribute to the Indy project.*

In addition to the utility it provides consumers, the indy-docs repository reduces the amount of required documentation work by each of Indy's repository maintainers. Pull Requests and questions regarding documentation can be directed to the indy-docs maintainers.

# Tutorial
[tutorial]: #tutorial

## Proposed Hosting

### Read The Docs
Read The Docs provides free hosting and automatically compiles HTML pages from Markdown. Read The Docs uses a Sphinx script that parses a code base for Markdown files and creates web pages accordingly.

An account owner points their Read The Docs project to source code, adding a webhook for automatic updates. A webhook that links to GitHub will automatically re-run the script to compile new documentation each time a commit is pushed to GitHub.

## Proposed Documentation Structure

Indy-docs contains Markdown files, a Make file, a configuration file, and some HTML/CSS/JS files. A dedicated repository for documentation promotes more organization of the Markdown files (e.g., tutorials in a tutorial directory).

Within every Indy project, there is development-specific documentation, including:
- README&#46;md 
- MAINTAINERS&#46;md 
- CODING-CONVENTIONS&#46;md
- Other, project-specific documentation that does not apply to consumers

Documentation more oriented toward consumers (how to build Libindy, Getting Started Guide, CLI commands, etc.) would be included in the comprehensive documentation build in indy-docs.

## Release Formalities

Indy-docs will keep versioned copies of documentation, with each update being associated with a version number (starting at v1.0.0). The version number will increment in a similar way as the other Indy repositories' version number (i.e., v1.0.1 would contain 'minor' changes, v1.1.0 would contain 'significant' changes, and v2.0.0 would contain 'major' changes).

The default documentation will correspond to the current stable release, with alternate versions available (on both Read The Docs and GitHub).

This is where it gets difficult to coordinate, as there are multiple Indy repositories, each with their own version history and releases. Recent discussion has led to the consideration of individual documentation sets for each repository; The following sections explore versioning for these two options. Potential drawbacks to individual documentation sets is discussed [below](#Drawbacks).

### Single Indy-Docs Repository

The indy-docs repository is updated with each formal release of *an* Indy repository. For example, unless indy-sdk and indy-node have a simultaneous release with the same purpose, indy-docs would be updated twice if the aforementioned repositories updated.

The version associated with indy-docs would start at v1.0.0 and increment according to its updates. Presently, there are no definitions defining 'minor,' 'significant,' and 'major' for indy-docs; we can assume that the semantics mirror those of the existing Indy repositories or we can develop indy-docs-specific definitions.

The indy-docs maintainers need to ensure that the documentation is updated whenever a new release takes place. This involves either proactive or responsive communication with the maintainers of the other Indy repositories.

### Read The Docs for Each Existing Repository

Each repository's Read The Docs documentation will update with each repository update. The version associated with the documentation will mirror that of the repository (e.g., the indy-sdk Read The Docs would begin at v1.6.1 and increment with each update/release of indy-sdk).

Maintainers of each repository need to ensure that the documentation is updated with each update to the repository, including deprecating any documentation that becomes obsolete.

# Reference
[reference]: #reference

- [MkDocs](https://www.mkdocs.org/user-guide/deploying-your-docs/#github-pages)
- [Sphinx](http://www.sphinx-doc.org/en/master/)


# Drawbacks
[drawbacks]: #drawbacks

### Single Indy-Docs Repository

The most significant drawback to indy-docs is that it would require maintainers, contributions from the community, and consistent upkeep. While centralized documentation will help eliminate a lot of time spent onboarding users, the offset of time required to maintain it may result in more time spent on documentation. Whether this time is well spent is determined by the value that this documentation provides the project.

### Read The Docs for Each Existing Repository

Maintainers for each repository would have additional responsibilities to either (1) ensuring that or (2) delegating the responsibility of ensuring that consumer-facing documentation is up-to-date, which has been difficult **and is the basis for this HIPE**. Additionally, there has been a major push to have *one* location for new users to find their way, rather than multiple.

# Rationale and alternatives
[alternatives]: #alternatives

### Rationale

By housing consumer documentation in one location, Indy can reduce the amount of onboarding effort for individuals and organizations, further establish a good reputation among those in the community, and standardize its documentation and messaging (reducing the amount of misleading and deprecated documentation). New users often express similar complications on platforms like Rocket.Chat, complications that can be addressed simply in an instructional or FAQ page.

Many developers are comfortable browsing through repositories; however, an increasing number of less tech-savvy consumers will begin to take interest in Indy, increasing the demand for a more straightforward selection of documentation.

There have been several efforts to standardize the documentation for the Indy project, and each has been useful in their own way (not without their own flaws). A single, appropriately named indy-docs repo would eliminate confusion around where to find the documentation, especially if found with a good looking GitHub Page.

### Alternatives

Additionally, there are several other markdown compilers (such as **MkDocs** and **mdBook**) that could help with this structure.

In the case that an indy-docs repo is not considered appropriate but consumer documentation is still desired, these services could function out of any repository (see this [pull request](https://github.com/hyperledger/indy-sdk/pull/958) as an example).

# Prior art
[prior-art]: #prior-art

Hyperledger Fabric has impressive [documentation](https://hyperledger-fabric.readthedocs.io/) that appears very consumer oriented and standardized. They have utilized Read the Docs, with ReStructured Text file types containing toctree tags to display documentation on Read the Docs in a non-intimidating, friendly way (Eric Holscher provided this [argument](http://ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/) in favor of using .rst instead of .md files). The file structure used for this Read the Docs build can be found on their GitHub [repository](https://github.com/hyperledger/fabric/tree/release-1.2/docs).

# Unresolved questions
[unresolved]: #unresolved-questions

- Who will be the maintainers of indy-docs?
- How do we want to structure the 'gritty' developer documentation?
- What experience do we want to provide users?
- How can we ensure that this consumer documentation becomes the de facto landing spot for new users?
