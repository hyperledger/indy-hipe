- Name: multi-sig-trustee-actions
- Author: Sergey Shilov
- Start Date: 2018-09-27
- PR:
- Jira Issue:

# Summary
[summary]: #summary

The indy-node should require several signatures of Trustees for the
transactions that are important for an Indy Network. 

# Motivation
[motivation]: #motivation

As a trustee of an Indy Network, the network should require other 
trustees to sign administrative transactions I want to sponsor so that
I am confident that no single trustee can abuse the network.

All transactions that require a trustee role should require multiple
trustee signatures. Specifically:
 - Add a trustee
 - Remove a trustee
 - Add a steward
 - Revoke the role of steward
 - Demote a consensus node
 - Send an upgrade transaction to the ledger

I'd prefer to use the term "actions" for the transactions described
above. The number of signatures required for each action should be
specified on the configuration ledger.

Also this feature can be applied not only for trustees and adopted for 
any role supported by the indy-node. 

# Tutorial
[tutorial]: #tutorial

Implementation of this feature affects the client application: the
indy-node will expect an administrative transaction sent with **the 
same source DID (action initiator) and signed by required number of
trustees**. Otherwise the transaction will be rejected. It means that
the client application should take care about multiple signing of the
same transaction.

Current implementation of libindy has an API call to add a signature
for the transaction. When such multi-signed transaction is received
by the indy-node then all signatures of this transaction are verified.
But preparation of multi-signed transaction is up to application.

Also it is required to use the same source DID to have ability to
uniquely identify this transaction in case of sending to the different
nodes by different clients.

# Reference
[reference]: #reference

To address described issue we need to do several consequence steps:

 - find out the structure of "actions" and their definition
 - apply them for incoming transactions as a part of authorisation
 - store them in config ledger to make them configurable

For now we have a static structure called *auth_map*. This structure
defines permissions for various actions. So we can use this data
structure as a base for new rules definition with some changes and
extensions.

I propose to divide the implementation into 2 phases:

 - Phase 1: extend the static *auth_map* structure (short term solution)
 - Phase 2: move the *auth_map* structure to config ledger (long term solution)

## Phase 1

It would be more efficient for whole stack to implement a solution with
static rules first. The plan for this phase is:
1. Modify and extend the *auth_map* structure to store the authorisation
rules for administrative actions.
2. Define the authorisation rules for administrative actions with
quorums as constants.
3. Modify applying of the rules stored if the *auth_map* according to
changes made by steps 1 and 2.

At the first step we can use absolute numbers of required signatures.
Further we can use a strategy of combination of absolute numbers and
percentage to implement a rules like "33% of trustees but not less than
2", but using of percentage requires INDY-1594 complete.

Seems like the Phase 1 does not require a lot of work and can be used
at least as a proof of concept.

## Phase 2

In order to make *auth_map* structure configurable we need to move it
to the config ledger. This requires significant work as we need to
design new transaction types to add/modify rules, their handlers,
validation schemas and so on.

Since we plan to move the auth_map structure to the config ledger as
the last step there is the question of atomicity of adding and
modification of the rules for all administrative actions is still under
discussion. Possible solutions:

 - each rule can be added/modified by separate transaction;
 - all rules are added/modified by single transaction, i.e. this
 transaction contains a list of all rules for administrative actions.

I think, the first point is better.

# Drawbacks
[drawbacks]: #drawbacks

Seems like there is no any drawbacks for the indy-node side. But such
functionality requires a protocol of preparation of the multi-signed
transaction for the client application.

# Rationale and alternatives
[alternatives]: #alternatives

Instead of multi-signed transaction it is possible to require several
single-signed transactions from trustees. But:
 - this requires to store them on the node side
 - this requires to maintain some state of transaction
 - this does not correspond to current protocol
 - this requires a lot of changes of the indy-node codebase

So this alternative is much worse than proposed solution.

# Prior art
[prior-art]: #prior-art

None.

# Unresolved questions
[unresolved]: #unresolved-questions

Phase 2 requires more detailed design.
Multi-signed transaction preparation protocol for the client application.