# ![Indy HIPEs](collateral/indy-hipes-logo.png)

This repo holds RFCs for the Indy project. We call them HIPEs (Hyperledger Indy
Project Enhancements, pronounced like "hype" for short). They describe important
topics ([not minor details](contributing.md#do-you-need-a-HIPE)) that we want to
standardize across the Indy ecosystem.

See [the HIPE Index](index.md) for a current listing of all HIPEs and their statuses.

See [this note](https://github.com/hyperledger/aries/blob/master/README.md#relationship-to-hyperledger-indy)
for comments about how Hyperledger Indy relates to Hyperledger Aries.

HIPEs are for developers *building on* Indy. They don't provide guidance on how Indy
implements features internally; individual Indy repos have design docs for that.

## HIPE Lifecycle

HIPEs go through a standard lifecycle:

![lifecycle](lifecycle.png)

#### Status == PROPOSED
To __propose__ a HIPE, [use these instructions to raise a PR](
contributing.md#how-to-propose-a-hipe) against the repo. Proposed
HIPEs are considered a "work in progress", even after they are merged. In other words, they
haven't been endorsed by the community yet, but they seem like reasonable ideas worth
exploring.

#### Status == ACCEPTED
To get a HIPE __accepted__, [build consensus](contributing.md#how-to-get-an-HIPE-accepted)
for your HIPE on [chat](https://chat.hyperledger.org/channel/aries) and in community
meetings. An accepted HIPE is incubating on a standards track; the community has decided
to polish it and is exploring or pursuing implementation.

#### Status == ADOPTED
To get a HIPE __adopted__, [socialize and implement](contributing.md#how-to-get-an-rfc-adopted).
A HIPE gets this status once it has significant momentum--when implementations accumulate,
or when the mental model it advocates has begun to permeate our discourse. In other words,
adoption is acknowledgment of a _de facto_ standard.

To __refine__ a HIPE, propose changes to it through additional PRs. Typically
these changes are driven by experience that accumulates during or after adoption.
Minor refinements that just improve clarity can happen inline with lightweight
review. Status is still ADOPTED.

#### Status == SUPERSEDED
Significant refinements require a superseding document; the original HIPE is
__superseded__ with a forwarding hyperlink, not replaced.

## About

#### License

This repository is licensed under an [Apache 2 License](LICENSE). It is protected
by a [Developer Certificate of Origin](https://developercertificate.org/) on every commit.
This means that any contributions you make must be licensed in an Apache-2-compatible
way, and must be free from patent encumbrances or additional terms and conditions. By
raising a PR, you certify that this is the case for your contribution.

For more instructions about contributing, see [Contributing](contributing.md).

#### Acknowledgement

The structure and a lot of the initial language of this repository was borrowed from [Rust HIPE](https://github.com/rust-lang/rfcs) .
Their good work has made the setup of this repository much quicker and better than it otherwise would have been.
If you are not familiar with the Rust community, you should check them out.