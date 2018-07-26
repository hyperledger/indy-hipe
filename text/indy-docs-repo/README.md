- Name: indy-docs-repo
- Author: Michael McKean mjmckean11@gmail.com
- Start Date: 2018-07-26
- PR: 
- Jira Issue:

# Summary
[summary]: #summary

Indy Docs is used to gather and build documentation from all Indy projects. Indy Docs' goal is to be the single place to direct new developers wanting to use Indy.

# Motivation
[motivation]: #motivation

As more consumers begin to use the Hyperledger Indy technology, the need for a set of more consumer-facing documentation grows. While there are plenty of resources available currently (Hyperledger Wiki, Rocket.Chat, Github repositories, etc.), often there is confusion about where new users should first go. *The Indy Docs repository provides this one-stop-shop for anyone looking to use or contribute to the Indy project.*

# Tutorial
[tutorial]: #tutorial

## Build Process

Indy Docs will house a script that will build documentation from each Indy project. This build script will download all Indy projects, execute scripts to generate documentation (rustdocs, sphinx), and place that documentation into a build directory along with any other generated documentation. This gives any maintainer of Indy Docs the ability to deploy new documentation maintained by other Indy projects.

## Proposed Hosting

### GitHub Pages

GitHub provides free hosting for project web pages. To use GitHub pages, navigate to settings and point GitHub to the appropriate branch. With deployment tools like [mkdocs](https://www.mkdocs.org/user-guide/deploying-your-docs/#github-pages) or [sphinx](http://www.sphinx-doc.org/en/master/), GitHub Pages are easy to maintain.

## Proposed Documentation Structure

Within every Indy project, there is development specific documentation, including:
- README&#46;md 
- MAINTAINERS&#46;md 
- CODING-CONVENTIONS&#46;md
- Other, project-specific documentation that does not apply to consumers

Documentation more oriented toward consumers (how to build Libindy, Getting Started Guide, CLI commands, etc.) would be included in the comprehensive documentation build in Indy Docs. 

# Reference
[reference]: #reference

- [GitHub Pages](https://pages.github.com/)
- [MkDocs](https://www.mkdocs.org/user-guide/deploying-your-docs/#github-pages)
- [Sphinx](http://www.sphinx-doc.org/en/master/)


# Drawbacks
[drawbacks]: #drawbacks

The most significant drawback to indy-docs is that it would require maintainers, contribution from the community, and consistent upkeep. While centralized documentation will help eliminate a lot of time spent onboarding users, the offset of time required to maintain it may result in more time spent on documentation. Whether this time is well spent is determined by the value that this documentation provides the project.

# Rationale and alternatives
[alternatives]: #alternatives

### Rationale

By housing consumer documentation in one location, Indy can reduce the amount of onboarding effort for individuals and organizations, further establish a good reputation among those in the community, and standardize its documentation and messaging (reducing the amount of misleading and deprecated documentation). New users often express similar complications on platforms like Rocket.Chat, complications that can be addressed simply in an instructional or FAQ page.

Many developers are comfortable browsing through repositories; however, an increasing number of less tech-savvy consumers will begin to take interest in Indy, increasing the demand for a more straightforward selection of documentation.

There have been several efforts to standardize the documentation for the Indy project, and each have been useful in their own way (not without their own flaws). A single, appropriately named indy-docs repo would eliminate confusion around where to find the documentation, especially if found with a good looking GitHub Page.

### Alternatives

As noted below, Hyperledger Fabric has utilized **ReadTheDocs** for their [documentation](https://hyperledger-fabric.readthedocs.io/). Similar to GitHub Pages, ReadTheDocs enables the organization of various files into a structured website, almost like a book with its chapters, appendices, and table of contents.

Additionally, there are several other markdown compilers (such as **MkDocs** and **mdBook**) that could help with this structure.

In the case that an indy-docs repo is not considered appropriate but consumer documentation is still desired, these services could function out of any repository (see this [pull request](https://github.com/hyperledger/indy-sdk/pull/958) as an example).

# Prior art
[prior-art]: #prior-art

Hyperledger Fabric has impressive [documentation](https://hyperledger-fabric.readthedocs.io/) that appears very consumer oriented and standardized. They have utilized Read the Docs, with ReStructured Text file types containing toctree tags to display documentation on Read the Docs in a non-intimidating, friendly way (Eric Holscher provided this [argument](http://ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/) in favor of using .rst instead of .md files). The file structure used for this Read the Docs build can be found on their GitHub [repository](https://github.com/hyperledger/fabric/tree/release-1.2/docs).

# Unresolved questions
[unresolved]: #unresolved-questions

- Who will be the maintainers of indy-docs?
- Who will be in charge of keeping the documentation up-to-date?
- How do we want to structure the 'gritty' developer documentation?
- What experience do we want to provide users?
- How can we ensure that this consumer documentation becomes the de facto landing spot for new users?
