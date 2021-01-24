# Indy HIPE 0162: Features to Help Remove Ledger Plugins
- Author: [Alexandr Kolesov](alexander.kolesov@evernym.com), [Richard Esplin](mailto:richard.esplin@evernym.com), and [Renata Toktar](renata.toktar@evernym.com)
- Start Date: 2020-12-01

## Status
- Status: [ADOPTED](/README.md#hipe-lifecycle)
- Status Date: 2020-01-22
- Status Note: The changes in this HIPE were discussed in the Indy Maintainers calls on [2020-12-22](https://wiki.hyperledger.org/display/indy/2020-12-22+Indy+Contributors+Call) and [2020-01-19](https://wiki.hyperledger.org/display/indy/2021-01-19+Indy+Contributors+Call). The other maintainers approved the plan, but requested a HIPE to be submitted.

## Summary
[summary]: #summary

In this HIPE, we propose two new features for Indy Node that will assist with removing ledger plugins that are no longer used: frozen ledgers and default fee handlers.

## Motivation
[motivation]: #motivation

Indy Plenum can be extended through the use of [ledger plugins](https://github.com/hyperledger/indy-plenum/blob/master/docs/source/plugins.md). Ledger plugins can introduce new transaction types that are either stored on existing ledgers, or on new ledgers created by the plugins. The [Sovrin Network](http://sovrin.org) used this capability to develop a [token plugin for Indy](https://github.com/sovrin-foundation/token-plugin) that stored fee and value transfer transactions on a token ledger. After experimenting with the plugin, [they decided to remove it](https://github.com/sovrin-foundation/sovrin-sip/tree/master/text/5005-token-removal/README.md).

Removing the plugin has three important consequences:
* The data stored on the custom ledger created by the plugin will be deleted.
* The audit ledger will no longer be able to obtain the root hash of any custom ledgers from the plugin.
* Any authorization rules (auth_rules) on the config ledger that define fees as being necessary to authorize writes to the domain ledger can no longer be handled by the plugin.

The first consequence is intended. This HIPE proposes feature to address the remaining two consequences to ensure that the network remains functional after the plugin is removed.

We include both features in the same HIPE because they share a common motivation and are likely to be used together.

## Frozen Ledgers
[frozen-ledgers]: #frozen-ledgers

### Tutorial
[frozen-ledgers-tutorial]: #frozen-ledgers-tutorial

If a ledger has been created, but will never be used, it can be frozen. The LEDGERS_FREEZE transaction will record the root hashes of one or more ledgers, and perpetually use those hashes when computing audit ledger validity. This has two important advantages:

* It preserves the ability to do rolling updates. If an update removes a plugin which includes custom ledgers, consensus would be interrupted and new transactions would not be able to be ordered until all nodes completed the update. This is because updated nodes would not be able to process new transactions that were ordered by the non-updated nodes. But if we freeze all ledgers associated with the plugin, we can do rolling updates because new transactions related to the plugin will be impossible.
* It allows the removal of old plugins. Frozen ledgers can be removed and there will be no left over data from the removed plugin. The removal of old plugins will also help reduce the cost of keeping the network stable and secure.

Freezing ledgers requires the following workflow:
* Upgrade all nodes to a version of Indy that supports frozen ledgers.
* Send a LEDGERS_FREEZE transaction for the ledgers that you want to drop.
* Upgrade all nodes to remove the plugin.
* Execute a migration script to drop the ledgers.

Permissions around the LEDGERS_FREEZE transaction are managed in the auth_rules with a default permission requiring the approval of three trustees ([the same default auth_rule for upgrading the ledger](https://github.com/hyperledger/indy-node/blob/master/docs/source/auth_rules.md)).

### Reference
[frozen-ledgers-reference]: #frozen-ledgers-reference

If a ledger is frozen it can be used neither for reading nor for writing. It will not be caught up by new nodes and can be safely removed. Default ledgers such as the domain, config, pool, and audit ledgers cannot be frozen.

Implementation notes:
* Implementation of this feature is possible because the catchup of the config ledger happens before catchup of other ledgers.
* We were nervous that replacing a ledger with a frozen ledger hash would break foreign keys in auth_rules, but our testing showed that this is not an issue.

Implementation steps:
1. Implement LEDGERS_FREEZE transaction handler that will write information about frozen ledger to state
2. Implement GET_FROZEN_LEDGERS transaction handler that will return information about frozen ledgers from state
3. Add dynamic validation to all handlers: check if the ledger is frozen
4. Update audit logic by taking into account the root hashes of frozen ledgers
5. Fix catch up to not catch up frozen ledgers **TODO: mirror requests or not?**

#### State schema:
There will be a key in CONFIG_LEDGER that will store a list of frozen ledgers in the following format:

```
2:FROZEN_LEDGERS = [
    <ledger_id>: {
        ledger: <ledger_root_hash>,
       	state: <state_root_hash>,
       	seq_no: <last_seq_no>
    },
    ...
]
```

#### New transactions:

Freeze ledgers that have the provided IDs:
```
LEDGERS_FREEZE {
    LEDGERS_IDS: [int]
}
```

Return frozen ledgers and their root hashes.
```
GET_FROZEN_LEDGERS
```

### Drawbacks
[frozen-ledgers-drawbacks]: #frozen-ledgers-drawbacks

The LEDGERS_FREEZE transaction allows removal of the plugin that created the ledger if the ledger was never used and the hash on the audit ledger never changed. Otherwise, the plugin will need to remain installed to allow historical transactions to replayed with the correct ledger hash.

### Rationale and alternatives
[frozen-ledgers-rationale-and-alternatives]: #frozen-ledgers-rationale-and-alternatives

We considered implementing the frozen ledger hash in a plugin, but we consider it a generally useful feature and believe it should belong in Indy.

### Prior art
[frozen-ledgers-prior-art]: #frozen-ledgers-prior-art

No relevant prior art.

### Unresolved questions
[frozen-ledgers-unresolved-questions]: #frozen-ledgers-unresolved-questions

All questions raised during the development of this proposal have been answered in this draft of the proposal.


## Default Fee Handlers
[default-fee-handler]: #default-fee-handler

### Tutorial
[default-fee-handler-tutorial]: #default-fee-handler-tutorial

[Indy Authorization Rules](https://github.com/hyperledger/indy-node/blob/master/docs/source/requests.md#auth_rule) provide a flexible way of authorizing write transactions to the domain ledger. This authorization can [depend on the payment of fees tracked by ledger plugins](https://github.com/sovrin-foundation/libsovtoken/blob/master/doc/fees.md).

Because Indy currently has no native concept of fees, if a plugin that implemented fees is removed, historical transactions can no longer be validated and will prevent new nodes from catching up on the ledger. In many cases it is sufficient to know that the historical transactions were valid at the time of writing. In these cases a default fee handler can approve the historical transactions.

### Reference
[default-fee-handler-reference]: #default-fee-handler-reference

The default fee handler is implemented in a new class ...
**TODO**

### Drawbacks
[default-fee-handler-drawbacks]: #default-fee-handler-drawbacks

* Historically there were concerns about having payment functionality included in Hyperledger projects, but as distributed payments have become more mainstream, it now seems acceptable to include into Indy generic primitives related to payments.
* The default fee handler will not perform the same validation on a historical transaction as was done in the removed plugin at the time that the transaction was originally completed. Therefore, it is most suitable for ledgers that do not make strong guarantees of historical validity, such as ledgers used for development and testing.
* If auth_rules with fees are defined, but no plugin is installed to process them, the rules will fall back to the default fee handler and authorization will be granted. This permissive behavior could be dangerous in some circumstances, and network administrators should ensure that auth_rules do not rely on fees when no plugin is installed to handle them. This is consistent with other Indy configuration options which are permissive by default to assist new users, but expected to be locked down for production use.

### Prior art
[default-fee-handler-prior-art]: #default-fee-handler-prior-art

No relevant prior art.

### Unresolved questions
[default-fee-handler-unresolved-questions]: #default-fee-handler-unresolved-questions

All questions raised during the development of this proposal have been answered in this draft of the proposal.

## Both
[both]: #both

### Rationale and alternatives
[both-rationale-and-alternatives]: #both-rationale-and-alternatives

Both of these features could be avoided by moving the token transactions into Indy as deprecated historical transactions. This would allow the history to be validated, but we don't want Indy to become a graveyard for every transaction type a plugin author defines. Implementing the features proposed in this HIPE is a more generic way to address the problem.

There is a [proposal to incorporate the token plugin as an optional part of Indy](https://github.com/hyperledger/indy-hipe/tree/master/text/0161-generic-token). This would remove the need for the removal of the token plugin from the Sovrin ledger, but no one has volunteered to do that work. Even if Indy does one day have a generic token, the features proposed in this HIPE would still be useful for the development and maintenance of other ledger plugins.
