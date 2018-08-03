- Name: libvcx-integration
- Author: Darko Kulic, Janko Krstic
- Start Date: 31.7.2018.
- PR: (leave this empty)
- Jira Issue: (leave this empty)

# Summary
[summary]: #summary

This HIPE proposes the new structure of Indy-SDK repository, accommodating libvcx.
It does not explain what libvcx is, what it provides, how it works and why it would be a good thing to have it be a part of
Indy-SDK. That will be documented separately.
It only explains the new structure of the repository and the reasoning behind it.
The changes proposed by this HIPE will be visible only to core developers working on Indy-SDK. There will be no changes required
by the users of any of Indy-SDK's features.

# Motivation
[motivation]: #motivation

Libvcx is a layer on top of libindy that fully implements the credentials exchange.
We consider credentials exchange one of the most important features provided by Indy. Most of the applications built on top of Indy will be using credentials. Therefore, we argue that it should be a core part of the Indy-SDK. Including libvcx prevents fragmentation in the community, which would occur if every party developed its own credentials exchange layer.

Having libvcx inside of Indy-SDK also allows for easier development and maintenance, because it would be seen as one of the core components of Indy-SDK. It would also make it easier for community developers to contribute.

# Tutorial
[tutorial]: #tutorial

Tutorials about libvcx will be provided later.

# Reference
[reference]: #reference

VCX Library is currently hosted in https://github.com/evernym/sdk
The main idea is to move the code into indy-sdk repo keeping the commit history.

The vcx directory will be a top-level directory in the Indy-SDK, and its structure would look like this:

vcx/  
├── README.md  
├── ci/  
├── libvcx/  
└── wrappers/  

After moving the code, the following tasks would be completed:
* the code documentation should be added
* some of the methods in the code are only passing the arguments to the libindy so these methods should be removed
* the code should be refined and improved in the process
* build process would also be moved to hyperledger infrastructure keeping it separate from build process of libindy
* a separate artifact would be produced in every build
* integration tests should be added so that whenever libindy or libvcx is changed this test may verify integration

# Drawbacks
[drawbacks]: #drawbacks

* The size of Indy-SDK repository is quite substantial as of now. It contains two libraries, cli, wrappers, and other directories. These new changes will introduce an entire new library, its own set of wrappers, and additional supporting files needed for build process. While it does mean that users will have more tools to use, it certainly increases the size and complexity, which can be considered a drawback.

* Having an entire new team of developers starting to work in Indy-SDK repository. Currently Indy-SDK has a stable core team which is responsible for the entire repository. This integration would bring a new group of developers who will be responsible for libvcx, its wrappers and build materials. This will cause some initial re-organisation, some communication overhead for future, and possibly issues if no clear boundaries and policies are set.
  * To resolve this concern, teams will work within their own areas of the Indy-SDK, and participate in coordination meetings.

* Managing versions. Since we will have two libraries, with libvcx being higher level and depending on libindy, the decision must be made on how to release new versions of both. Currently, it is possible to release new versions of libindy, and letting libvcx catch up. Libvcx would have the older version of libindy as dependency, and developers of libvcx would choose whether they want to develop against older or newer versions of libindy.
With the proposed changes, this would imply having incompatible versions of libindy and libvcx on master, or different branching strategies (libindy being released from special branches). Second option is to require lock-step releases of libindy and libvcx, which could cause communication overhead and possibly slow the pace of development and releases, as things are required to be kept in sync.

# Rationale and alternatives
[alternatives]: #alternatives

* Keeping libvcx as it is, in a separate repository from Indy-SDK. The argument against it was that the credentials exchange is a core functionality and as such, it belongs to Indy-SDK.

* Using git submodules (https://git-scm.com/book/en/v2/Git-Tools-Submodules). Indy-SDK would contain several git submodules, one for each library as well as for wrappers. The core team did not like this idea.

# Prior art
[prior-art]: #prior-art

No known prior art.

# Unresolved questions
[unresolved]: #unresolved-questions

* How will release process look like?
* Should both artifacts share the same version number?
