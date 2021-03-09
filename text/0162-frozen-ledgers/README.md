# Indy HIPE 0162: Frozen Ledgers
- Author: [Alexandr Kolesov](alexander.kolesov@evernym.com), [Richard Esplin](mailto:richard.esplin@evernym.com), and [Renata Toktar](renata.toktar@evernym.com)
- Start Date: 2020-12-22


## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: 2020-01-22


## Summary
[summary]: #summary

Ledgers that are created by Indy plugins cannot be removed without breaking consensus. This HIPE describes functionality to freeze a ledger so that it can be safely removed.


## Motivation
[motivation]: #motivation

Indy Plenum can be extended through the use of [ledger plugins](https://github.com/hyperledger/indy-plenum/blob/master/docs/source/plugins.md). Ledger plugins can introduce new transaction types that are either stored on existing ledgers, or on new ledgers created by the plugins. The [Sovrin Network](http://sovrin.org) used this capability to develop a [token plugin for Indy](https://github.com/sovrin-foundation/token-plugin) that stored fee and value transfer transactions on a token ledger. After experimenting with the plugin, [a plan was made to remove it](https://github.com/sovrin-foundation/sovrin-sip/tree/master/text/5005-token-removal/README.md).

Removing the Sovrin token plugin has three important consequences:
* The data stored on the custom ledger created by the plugin will be deleted.
* The audit ledger will no longer be able to obtain the root hash of any custom ledgers from the plugin.
* Any authorization rules (auth_rules) on the config ledger that define fees as being necessary to authorize writes to the domain ledger can no longer be handled by the plugin.

The first consequence is intended. This HIPE proposes a feature to address the second consequences to ensure that the network remains functional after the plugin is removed. The last consequence is [treated in a separate HIPE](https://github.com/hyperledger/indy-hipe/tree/master/text/0163-default-fee-handler).


## Tutorial
[tutorial]: #tutorial

If a ledger has been created, but will no longer be used, it can be frozen (refer to the [Drawbacks](#drawbacks) section for important details). The LEDGERS_FREEZE transaction will record the root hashes of one or more ledgers in the state trie, and perpetually use those hashes when computing audit ledger validity. This has two important advantages:

* It preserves the ability to do rolling updates. Without this capability, attempting to remove a plugin during a rolling update risks breaking consensus if a transaction is submitted to the ledger during the roll out period. This is because updated nodes would not be able to process new transactions that were ordered by the non-updated nodes. But if we freeze all ledgers associated with the plugin, we can do rolling updates because new transactions related to the plugin will be impossible.
* It allows the removal of old plugins. Frozen ledgers can optionally be removed and there will be no left over data from the removed plugin. The removal of old plugins will help reduce the cost of keeping the network stable and secure.

Freezing ledgers requires the following workflow:
* Upgrade all nodes to a version of Indy that supports frozen ledgers.
* Send a LEDGERS_FREEZE transaction for the ledgers that you want to deprecate.
* Upgrade all nodes to remove the plugin.
* Optionally, execute a migration script to drop the ledgers that are no longer used.

Permissions around the LEDGERS_FREEZE transaction are managed in the auth_rules with a default permission requiring the approval of three trustees ([the same default auth_rule for upgrading the ledger](https://github.com/hyperledger/indy-node/blob/master/docs/source/auth_rules.md)).


## Reference
[reference]: #reference

If a ledger is frozen it can be used neither for reading nor for writing. It will not be caught up by new nodes and can be safely removed. Default ledgers such as the domain, config, pool, and audit ledgers cannot be frozen.

### Implementation notes:
* Implementation of this feature is possible because the catchup of the config ledger happens before catchup of other ledgers.
* We were nervous that removing transactions would break foreign keys in auth_rules, but our testing showed that this is not an issue.
* Frozen ledgers cannot be unfrozen, but dropped ledgers can be replaced by creating a new ledger with a different ledger ID.
* Data from frozen ledgers will not be propagated to new nodes in the pool during catchup.

### Implementation steps:
1. Implement LEDGERS_FREEZE transaction handler that will write information about frozen ledger to state.
2. Implement GET_FROZEN_LEDGERS transaction handler that will return information about frozen ledgers from state.
3. Add dynamic validation to all handlers: check if the ledger is frozen.
4. Update audit logic by taking into account the root hashes of frozen ledgers.
5. Fix catch up to not catch up frozen ledgers.

### State schema:
There will be a key in CONFIG_LEDGER that will store a list of frozen ledgers in the following format:

```
4:FROZEN_LEDGERS = [
    <ledger_id>: {
        ledger: <ledger_root_hash>,
       	state: <state_root_hash>,
       	seq_no: <last_seq_no>
    },
    ...
]
```

### New transactions:

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

### Error messages:

Error message for all client actions with a frozen ledger.

```
InvalidClientRequest(request.identifier, request.reqId,
                                           "'{}' transaction is forbidden because of "
                                           "'{}' ledger is frozen".format(self.txn_type, self.ledger_id))
```


## Drawbacks
[drawbacks]: #drawbacks

A frozen ledger should only be removed from the system if it has never been used, because in that scenario the hash on the audit ledger never changed. Understanding this limitation requires consideration of three separate properties of the distributed ledger:
1. The ability to achieve consensus when writing a new transaction to the ledger.
2. The ability to catch up nodes through consensus.
3. The ability to audit the history of the ledger to prove that there was no tampering.

When a ledger is frozen, the root hash of the deprecated ledger is available to be used by the audit ledger when computing consensus. So the first property is preserved.

During catchup, the transaction validation logic is not executed. This is because we are catching up transactions that have the ledger BLS signature, so we know it was already validated and we don't need to do it again. So the second property is preserved.

If a ledger is added (so its root hash is expected by the audit ledger), but it was never used (so the root hash never changed), then LEDGERS_FREEZE will preserve the third property even when the ledger is removed.

But the third property will not be preserved if there is a history of transactions on a ledger and then the ledger is removed. This is because the LEDGERS_FREEZE transaction only stores the most recent root hash, and not the entire history of root hashes, so that history can not be recreated after the plugin ledger is removed. Instead, the frozen ledger should be retained in its read-only state and new nodes in the pool should manually backup the data from frozen ledgers since they are not included in catchup.

Note that Indy Node does not include functionality to perform an audit of the ledger history based on the original validation rules. Indy transaction handlers perform validation on new transactions, but not during the catchup process. This is because the transaction is already on the ledger (it has a state signature), so we know that validation was already performed and we don't need to do it again. An audit of the history would have to be done outside of Indy Node by replaying the transactions using the original validation logic, using the audit ledger to compare the state among the various ledgers. Freezing a ledger does not change this process, but dropping a frozen ledger that contains historical transactions would eliminate data that would be necessary to perform a complete audit of the ledger history.


## Rationale and alternatives
[alternatives]: #alternatives

The current need for freezing a ledger can be avoided by moving the token transactions into Indy as deprecated historical transactions. This would allow the history to be validated, but we don't want Indy to become a graveyard for every transaction type a plugin author defines. Implementing frozen ledgers is a more generic way to address the problem.

There is a [proposal to incorporate the token plugin as an optional part of Indy](https://github.com/hyperledger/indy-hipe/tree/master/text/0161-generic-token). This would remove the need for the removal of the token plugin from the Sovrin ledger, but no one has volunteered to do that work. Even if Indy does one day have a generic token, the ability to freeze ledgers would still be useful for the development and maintenance of other ledger plugins.

We considered implementing the frozen ledger hash in a plugin, but we consider it a generally useful feature and believe it should belong in Indy.

An auth_rule could be used to prohibit writing to a ledger, but this approach seems more fragile than the frozen ledger transaction because:
* It will not be obvious to the user that transactions are not being recorded because the ledger is deprecated.
* If the auth_rule was changed, writes could be re-enabled for the ledger. If the ledger has not been used for an extended period of time, a hidden error could be uncovered.
* The ledger cannot be removed from the system and so would always need to be maintained.


## Prior art
[prior-art]: #prior-art

No relevant prior art.


## Unresolved questions
[unresolved-questions]: #unresolved-questions

All questions raised during the development of this proposal have been answered in this draft of the proposal.
