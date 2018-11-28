- Name: indy-docs-framework
- Author: Michael Boyd <michael.boyd@sovrin.org>
- Start Date: 11/27/18
- PR: (leave this empty)
- Jira Issue: (leave this empty)

# Summary
[summary]: #summary

This HIPE proposes that each relevant Indy repository maintain a docs/ folder that can be built to display the documentation library in html format using [sphinx](http://www.sphinx-doc.org/en/stable/). We will use http://readthedocs.org to automatically build and host all these html libraries together under http://indy.readthedocs.io. 

# Motivation
[motivation]: #motivation

 * Make better documentation that helps users and contributors alike to more easily understand, use and contribute to our code. 
 * Help maintainers eliminate duplicated or deprecated content, and give everyone a way to efficiently index and search documentation across repositories. 
 * Provide new users a clear path on how to implement Indy tech within their projects, driving adoption of the project and lowering developer burnout
  
## Why did we choose this method?
* Maintain a single source of truth for each document while keeping documentation in the respective repo's of the codew
* It is easily maintainable for busy contributors 
* Modular and extensible for future changes in our software architecture or repository structure

# Tutorial
[tutorial]: #tutorial

## Relevant Repositories
Here is a list of all the repositories in which we have documentation: 
- indy-sdk: https://github.com/hyperledger/indy-sdk
- indy-node: https://github.com/hyperledger/indy-node
- indy-agent: https://github.com/hyperledger/indy-agent
- indy-plenum: https://github.com/hyperledger/indy-plenum
- indy-hipe: https://github.com/hyperledger/indy-hipe
- indy-crypto (soon to be ursa): https://github.com/hyperledger/indy-crypto

In addition, we have created the indy-docs repository to hold general prose that explains indy concepts and provides users a jumping off point into the respective repos.
 - indy-docs: https://github.com/michaeldboyd/indy-docs/
## Implementation Details
Each Indy project has a docs/ folder at the project root. This folder contains all of the documentation that you want to display in your html library. Here is the indy-sdk docs/ folder as an example: https://github.com/michaeldboyd/indy-sdk/blob/sphinx-docs-test/docs

We use two tools to build documentation:
* [Sphinx](http://www.sphinx-doc.org/en/stable/): We've found this to be the most flexible tool to build html documentation from source and have cross-project search functionality.
* [Readthedocs](http://readthedocs.org): A free documentation hosting service that works really well with Sphinx and is basically plug-n-play for maintainers.

Each docs/ folder has 3 main files: `conf.py`, `index.rst`, and `Makefile`.

* `conf.py` contains all of the sphinx configuration code. More details on how to edit the `conf.py` can be found [on the sphinx website](http://www.sphinx-doc.org/en/master/usage/configuration.html) 
* `Makefile` is to build the docs locally. Local build instructions are below.
* `index.rst` defines the menu structure of the library and is also the home page for the repository. 
* `_static/`: this folder can be used for diagrams, images, and other assets.
  
Sphinx uses [reStructuredText](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html) (`.rst`) and its powerful directives to build the documentation. While sphinx will also build `.md` markdown files, we'll need to use `.rst` files and the `.. toctree::` (table of contents tree) directive whenever we want to create nested pages. 

## Docs/ Organization
The main entry point is `index.rst`, so to add something into the Table of Contents you would simply modify that file in the same manner as all of the other topics. It's very self-explanatory once you look at it.

This is the  `toctree` for the indy-sdk [index.rst](https://github.com/michaeldboyd/indy-sdk/blob/sphinx-docs-test/docs/index.rst):
```
.. toctree::
  :maxdepth: 1
  :hidden:

  getting-started/index.rst
  concepts/index.rst
  how-tos/README.md
  build-guides/index.rst
  migration-guides/index.rst

```

This will create the main menu of the SDK, and also include the linked pages in each of the lower order `index.rst` files.

In each of the folders, additional `.md` or `.rst` files can be added by including them in the `toctree` directive. 

It will make more sense by seeing it in action: [Indy SDK Docs](https://indy.readthedocs.io/projects/sdk/en/latest/index.html)

Depending on the needs of the repository, docs/ may contain as many or as few documents as the maintainers feel are necessary to: 
* Provide a clear *conceptual* overview of the repository for readers to clearly understand what it does.
* Enable technical users to quickly begin implementing the code
* Resolve common questions or current issues that create blockers to using the repository
* Onboard potential contributors into the open-source community surrounding the repository. 
  
We recommend keeping documentation files organized by folder based on their topic, but we leave it up to maintainers to decide how best to structure their docs. 

# Reference
[reference]: #reference

## How to Add Documentation
For new features and pull requests, maintainers should make sure that the contributor has add an explanation for their changes in the docs folder before merging the PR.
  
Contributors should write an addition to a current file or add a new file to the docs/ folder that explains what their feature is and how it works. If needed, they may also add a link to more technical README's located nearer to the code.

Once additions to the docs have been made, make sure to update the `index.rst` in whichever folder the file has been added, and build the docs locally to confirm they work (TODO: add the `sphinx-build` command to our CI/CD flow)

For example, if I wanted to add another file to the indy-sdk docs/ folder named `glossary.md`, I would create the file, and then add a reference to it in the `index.rst`: 
```
.. toctree::
  :maxdepth: 1
  :hidden:

  getting-started/index.rst
  ...
  other files
  ...
  glossary.md                   .. <-- this is your new file!

```

To add a new file to a submenu, simply update that subfolder's `index.rst` with the relative link to your file. All relative links within the docs/ folder will be resolved correctly. 

If you'd like to link to a file outside of the docs/ folder, you'll need to provide an external github link (this is by design, to keep our docs organized into a single folder)

## How to Host on Readthedocs


We will have a maintainer who has access to the Hyperledger repositories create an account with Readthedocs and set up the free hosting through their web UI. It's really simple. I've created the example http://indy.readthedocs.io from my forks of the repositories. View the diagram below to see how it is structured. Git webhooks are automatically added to keep the docs up to date.

![hosting](indy-docs-diagram.png)

We simply need to import all of the repositories into readthedocs.org using their web UI, and then define the subproject structure. 

## Building the docs on your machine

Here are the quick steps to achieve this on a local machine without depending on ReadTheDocs. Note: Instructions may differ depending on your OS.

```
pip install Sphinx
pip install sphinx_rtd_theme
pip install recommonmark==0.4.0
cd docs/ # Be in this directory. Makefile sits there.
make html
```

This will generate all the html files in `docs/_build/html` which you can then start browsing locally using your browser. Every time you make a change to the documentation you will of course need to rerun `make html`.

## Maintaining Versions
Readthedocs includes the ability to add additional version for each of the projects. To build documentation for a different version of any Indy repo, it will be as simple as specifying which versions to display on indy.readthedocs.io. 

## Implementation of a Multiproject Sidebar
There have been a couple design decisions that have given me pause. One of those has been the method of building our multirepository sidebar on http://indy.readthedocs.io. 

While readthedocs does support subprojects, it does not automatically make a shared menu  when these projects are built together. To create this shared menu, I've had to make a separate config file named [remote_conf.py](https://github.com/michaeldboyd/indy-docs-conf/blob/master/remote_conf.py) and then build the menu manually within that file. This file is hosted on github: 

To make sure that each project builds with the multi-repository menu, I've added a couple lines to each repo's conf.py file to import the sidebar from github when the repo's docs are building on readthedocs. I'm pretty sure there's a better way to do this, but I haven't come up with one yet. 

```python
# conf.py
...
# ------------ Remote Documentation Builder Config -----------
# Note: this is a slightly hacky way of maintaining a consistent sidebar amongst all the repositories. 
# Do you have a better way to do it?
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if(on_rtd):
    rtd_version = os.environ.get('READTHEDOCS_VERSION', 'latest')
    if rtd_version not in ['stable', 'latest']:
        rtd_version = 'latest'
    try:
        os.system("git clone https://github.com/michaeldboyd/indy-docs-conf.git remote_conf")
        os.system("mv remote_conf/remote_conf.py .")
        import remote_conf
        remote_conf.generate_sidebar(globals(), nickname)
        intersphinx_mapping = remote_conf.get_intersphinx_mapping(rtd_version)
        master_doc = "toc"
    
    except:
        e = sys.exc_info()[0]
        print e
    finally:      
        os.system("rm -rf remote_conf/ __pycache__/ remote_conf.py")

```

I would like to find a more elegant way to build this sidebar without needing to include the repeated build instructions within each of our repositories. This is still a work in progress. Note that this will only execute when on readthedocs servers and not on user's machines. 

# Drawbacks
[drawbacks]: #drawbacks

This change does introduce a new level of documentation maintenance for maintainers. We currently have the http://wiki.hyperledger.org site, and the Github readme viewing functionality, and that could be all that is necessary.

While this change does provide greater organization and clarity to our documentation, it will require that maintainers understand how to use sphinx and readthedocs. 

We may not need to link all of our repositories together, and perhaps we should just maintain a single docs repository that contains prose explaining indy. We could also maintain separate readthedocs instances for each repository. However, I think that including all the repository docs/ folders underneath one umbrella will give contributors and users a greater understanding of our ecosystem. 

# Rationale and alternatives
[alternatives]: #alternatives

- What other designs have been considered and what is the rationale for not choosing them?
    
    - We originally considered making an indy documentation repository to keep all of our documentation, as explain in this [pull request](https://github.com/mjmckean/indy-hipe/tree/master/text/indy-docs-repo)
    - We have also previously used wiki.hyperledger.org to hold or documentation. Neither of these approaches were optimal because the documents were not held within the actual repository in which contributors and maintainers do their work.
- What is the impact of not doing this?
    - We will continue to have confused developers who don't know where to start consuming Indy. We will continue to have duplication of documentation, and outdated documents floating around our ecosystem. 

- Why is this design the best in the space of possible designs?
    - By hosting consumer documentation in one location, Indy can reduce the amount of onboarding effort for individuals and organizations, further establish a good reputation among those in the community, and standardize its documentation and messaging (reducing the amount of misleading and deprecated documentation). New users often express similar problems that they are running into on platforms like Rocket.Chat, complications that can be addressed simply in an instructional or FAQ page.
    - An increasing number of less tech-savvy consumers are taking an interest in Indy, which increases the demand for a more straightforward selection of documentation that can be viewed outside of Github.

# Prior art
[prior-art]: #prior-art

- Does this feature exist in other SSI ecosystems and what experience have their community had?
    - Check out the [hyperledger fabric docs](https://hyperledger-fabric.readthedocs.io/en/release-1.3/)
    - the [ethereum docs](http://ethdocs.org/en/latest/)
    - and the [von anchor docs](https://von-anchor.readthedocs.io/en/latest/)

All three of these projects demonstrate how to use sphinx and readthedocs to successfully build clear documentation. 

We are following the same approach, with the addition that we are going to host multiple repo's docs/ folders all under the same umbrella.

# Unresolved questions
[unresolved]: #unresolved-questions

## To be resolved before implementing:
- The multirepository sidebar remote_conf.py file is a little hacky. Is there a better way to create a shared sidebar?
- Are there any disadvantages to mixing `.rst` and `.md` files within the same documentation solution? 
    - `.rst` directives are powerful, and these files make for good index files. `.md` markdown is easier for most contributors to use, and will be good for documenting most features. I don't have a problem using both. Does anyone else have a problem with it?


