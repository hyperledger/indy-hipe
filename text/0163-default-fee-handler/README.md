# Indy HIPE 0163: Default Fee Handler
- Author: [Alexandr Kolesov](alexander.kolesov@evernym.com), [Richard Esplin](mailto:richard.esplin@evernym.com), and [Renata Toktar](renata.toktar@evernym.com)
- Start Date: 2020-12-01


## Status
- Status: [ADOPTED](/README.md#hipe-lifecycle)
- Status Date: 2020-01-22
- Status Note: The changes in this HIPE were discussed in the Indy Maintainers calls on [2020-12-22](https://wiki.hyperledger.org/display/indy/2020-12-22+Indy+Contributors+Call) and [2020-01-19](https://wiki.hyperledger.org/display/indy/2021-01-19+Indy+Contributors+Call). The other maintainers approved the plan, but requested a HIPE to be submitted.


## Summary
[summary]: #summary

Adding a default fee handler to Indy will make it easier to maintain ledgers with payment plugins.


## Motivation
[motivation]: #motivation

Indy Plenum can be extended through the use of [ledger plugins](https://github.com/hyperledger/indy-plenum/blob/master/docs/source/plugins.md). Ledger plugins can introduce new transaction types that are either stored on existing ledgers, or on new ledgers created by the plugins. The [Sovrin Network](http://sovrin.org) used this capability to develop a [token plugin for Indy](https://github.com/sovrin-foundation/token-plugin) that stored fee and value transfer transactions on a token ledger. After experimenting with the plugin, [they decided to remove it](https://github.com/sovrin-foundation/sovrin-sip/tree/master/text/5005-token-removal/README.md).

Removing the plugin has three important consequences:
* The data stored on the custom ledger created by the plugin will be deleted.
* The audit ledger will no longer be able to obtain the root hash of any custom ledgers from the plugin.
* Any authorization rules (auth_rules) on the config ledger that define fees as being necessary to authorize writes to the domain ledger can no longer be handled by the plugin.

The first consequence is intended. The second consequence is [treated in a separate HIPE](https://github.com/hyperledger/indy-hipe/tree/master/text/0162-frozen-ledgers). This HIPE proposes a feature to address the last consequence.


## Tutorial
[tutorial]: #tutorial

[Indy Authorization Rules](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#auth_rule) provide a flexible way of authorizing write transactions to the domain ledger. This authorization can [depend on the payment of fees tracked by ledger plugins](https://github.com/sovrin-foundation/libsovtoken/blob/master/doc/fees.md).

Because Indy currently has no native concept of fees, if a plugin that implemented fees is removed, historical transactions can no longer be validated and will prevent new nodes from catching up on the ledger. In many cases it is sufficient to know that the historical transactions were valid at the time of writing. In these cases a default fee handler can approve the historical transactions.


## Reference
[reference]: #reference

Implementation will require adding to Indy [the SET_FEE transaction copied from the sovtoken plugin](https://github.com/sovrin-foundation/token-plugin/blob/a635780361a7478ea4b2f47fcffee78b150fdea3/sovtokenfees/sovtokenfees/req_handlers/write_handlers/set_fees_handler.py#L20) and [a default fee handler copied from the sovtoken fee handler (FeesAuthorizer)](https://github.com/sovrin-foundation/token-plugin/blob/master/sovtokenfees/sovtokenfees/fees_authorizer.py#L26). The fee handler will have the validation logic replaced with `throw NotAllowedException()`.

Any Indy transaction handler consists of two parts: validation logic and execution logic. Indy transaction handlers perform validation on new transactions, but not during the catchup process. This is because the transaction is already on the ledger, so we know that validation was already performed and we don't need to do it again. The default fee handler will contain a copy of the sovtoken fee handler but with validation disabled, so it will allow catchup but will not allow new transactions with fees.

Indy will also look to the default fee handler to determine the execution logic for fee related transactions, but the default fee handler will not allow any new fee transactions and so doesn't need any specific execution logic. Any future implementation of a payment plugin will need to override the default fee handler with a functional implementation of validation and execution logic.


## Drawbacks
[drawbacks]: #drawbacks

* Historically there were concerns about having payment functionality included in Hyperledger projects, but as distributed payments have become more mainstream, it now seems acceptable to include into Indy generic primitives related to payments.
* The default fee handler replays transactions without performing validation. This is fine for catching up validator nodes, but an audit of the ledger history would need to take into account the historical validation expected by any removed plugins.
* The ledger could be erroneously configured with auth_rules that define fees without having a plugin installed to process them. The exact behavior in this scenario will depend on the specific rules that mention fees, and could lead to confusing and hard to diagnose behavior. However this is a niche case because SET_FEE transactions will be rejected if there is no plugin to define them.
* The existence of a default fee handler in Indy Node could in theory be exploited by an attacker, but we consider this a small risk for a distributed ledger as any attack would have to simultaneously succeed on a majority of validation nodes in order to change what gets written.


## Rationale and alternatives
[alternatives]: #alternatives

The current need for a default fee handler could be avoided by moving the token transactions into Indy as deprecated historical transactions. This would allow the history to be validated, but we don't want Indy to become a graveyard for every transaction type a plugin author defines. Implementing the features proposed in this HIPE is a more generic way to address the problem.

There is a [proposal to incorporate the token plugin as an optional part of Indy](https://github.com/hyperledger/indy-hipe/tree/master/text/0161-generic-token). This would remove the need for the removal of the token plugin from the Sovrin ledger, but no one has volunteered to do that work.


## Prior art
[prior-art]: #handler-prior-art

No relevant prior art.


## Unresolved questions
[unresolved-questions]: #unresolved-questions

All questions raised during the development of this proposal have been answered in this draft of the proposal.
