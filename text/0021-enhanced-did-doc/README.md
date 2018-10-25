- Name: enhanced-did-doc
- Author: lovesh.harchandani@evernym.com
- Start Date: 2019-10-18
- PR: (leave this empty)
- Jira Issue: (leave this empty)

# Summary
[summary]: #summary

Indy currently supports only 1 public key per DID. This HIPE proposes to add support for more than 1 public key per DID. Additionally the keys can have one or more authorizations. The authorizations enable granular control over the DID doc like which keys can add new keys, which keys can remove which keys. This HIPE also proposes to add support for endpoints for a DID. Endpoints specify where the DID can be connected to. Endpoints can follow different protocols, HTTP, HTTPS, SMTP, even DID.

# Motivation
[motivation]: #motivation

A DID can have several agents. It might want some of its agents to be able to add new agents, some of them to remove existing agents, some with all possible authorizations. eg, an organization (DID) can designate some of its members (agents) to add new members, some to remove existing members, some to be able to do both.
A DID needs to let others know where they should send messages in case they need to communicate. eg, An organization (DID) can declare that to communicate by email, send an email at foo@example.com, to reach by HTTP visit https://example.com, to send money by Bitcoin, send at a particular address.
The addition of above 2 features brings Indy DIDs somewhat closer to W3C's DID spec.

# Tutorial
[tutorial]: #tutorial

## Concepts
[concepts]: #concepts

1. Key reference: Any key added to a DID gets a reference unique in context of that DID. This reference is a monotonically increasing integer without any gaps, starting from 1. Hence the first key for the DID (during creation) is given a reference of 1. The next key gets a reference of 2. This reference is used to change the public key in case of compromise or otherwise or grant additional authorizations. Only the key with key reference 1 can be used to act as a role like Steward, TGB, Trustee, etc.
2. Authorizations: Any public key can possess any number of authorizations. These determine what actions the key can take. A key's authorizations can change over time. It is possible for a key to have no authorization at all.
Following authorizations are possible:
a. `ADMIN`: A special authorization; a key with this authorization can change the DDO however it wants. The key with reference 1 has this authorization.
b. `ADD_KEY`: Add new keys to the DID. The newly added key can only have authorizations that the key adding it has. 
c. `REM_KEY`: Remove any existing keys from the DID. Keys with this authorization can remove any key with any authorization, i.e. even a key with `ADMIN` authorization. This can be debatable hence mentioned in the last section of this HIPE.
d. `MOD_KEY`: Update the key and/or its authorizations. Any key can change its own public key irrespective of it having `MOD_KEY` authorization or not.
e. `MOD_EP`: Add, remove or update endpoints.
3. Endpoints: Endpoints are URIs where the DID can be interacted with. They can be HTTP, HTTPS, TCP, SMTP or even DID. The messages sent to a DID need to be encrypted. If the endpoint is not a DID then it needs to be specified which key to use with that endpoint. If it is a DID then the DID can be looked up to find a key with `tags` (see below for explanation) containing `MPROX`. There is an exception to this rule is the endpoint type `PAY`. This endpoint type is used to specify a payment address. This exception can be debatable hence mentioned in the last section of this HIPE.
Each endpoint is given a reference similar to the way in which keys are given reference.
4. Tags: A key can specify a list of strings called `tags` for any higher level application to parse. Currently only one tag is specified by Indy called `MPROX`. Only a key can update its `tags`

## Authorization rules subtleties
[authorization_rules_subtleties]: #authorization_rules_subtleties

1. Any key can forfeit its 1 or more authorizations. eg. if a key has `ADD_KEY` and `REM_KEY` authorizations, it can give up its `REM_KEY` authorization even if it does not have `MOD_KEY` authorization.
2. When a new key, that we'll call `subject` is added by another key, that we'll call `actor`, `subject` can only have authorizations which `actor` has. `actor` might decide to give less authorizations to `subject` but it cannot give more. eg. Key `k1` has authorizations `ADD_KEY` and `REM_KEY`, it adds a new key `k2`, now `k2` can at most be given `ADD_KEY` and `REM_KEY` by `k1`, `k1` might give just `ADD_KEY` or `REM_KEY` or no authorization at all but `k1` cannot give `MOD_KEY`.
3. When an existing key, that we'll call `subject`'s authorizations needs to be modified, they can only be modified by a key with `MOD_KEY` authorization. Moreover, this key, that we'll call `actor` cannot grant the key any more authorizations than it has. Though it can take away any authorizations. This can be debatable hence mentioned in the last section of this HIPE.
4. A key with `MOD_EP` can add new endpoint or change any endpoint's value. Changing an endpoint's value to empty string removes it. 

## More flexible authorization rules (for future)
[flexible_authorization]: #flexible_authorization

**Note: This is future work and design presented here is rough and may change.**
A more flexible authorization where more than one key has to be involved in a action can be achieved by defining policy for the action. eg. If it was required that to add a new key, 3 keys with `ADD_KEY` have to collaborate, i.e. sign a transaction, a policy will be created with a mapping in JSON like 

```
{
    "policy": {
        "ADD_KEY": 3    // 3 keys with ADD_KEY authorization
    }
}
```

More flexible policies can be created as 

```
{
    "policy": {
        "ADD_KEY": [OR 3, 5, 50%, 75%]    // 3 keys with ADD_KEY authorization OR any 5 keys OR 50% keys with ADD_KEY authorization OR 75% of all keys present.
    }
}
```

Policy creation/modification will be introduced as new transactions and will have corresponding authorizations. 
The transaction for adding/updating/removing keys will not change apart from additional authorizations for policies.

# Reference
[reference]: #reference

## Authorization representation

Authorizations are represented as bitset in transactions. 

- `ADMIN`: Bit 0
- `ADD_KEY`: Bit 1
- `REM_KEY`: Bit 2
- `MOD_KEY`: Bit 3
- `MOD_EP`: Bit 4


## New transactions 
[new_transactions]: #new_transactions

4 new transactions need to to be introduced and 1 existing transaction needs to be updated.

1. Update `NYM` transaction to support `tags` and `authorizations` in the payload. These tags are associated with the key. For a new DID `authorizations` is ignored. Secondly, any `NYM` transaction made for an existing DID will be considered executing for key with reference `1`.
2. A new transaction called `ADD_KEY` needs to be added. This transaction is used to add new keys. It look like this
```
{type: ADD_KEY, did: <subject did>, publicKey: <new public key>, authorizations: <bitset for authorization>, tags: <tags>}
```
3. A new transaction called `REM_KEY` needs to be added. This transaction is used to remove keys. It look like this
```
{type: REM_KEY, did: <subject did>, publicKeyRef: <public key reference>}
```
4. A new transaction called `MOD_KEY` needs to be added. This transaction is used to update keys. It look like this
```
{type: MOD_KEY, did: <subject did>, publicKeyRef: <public key reference>, authorizations: <bitset for authorization>, tags: <tags>}
```
5. A new transaction called `EP` needs to be added. This transaction is used to add, remove or update. 
A transaction to add new endpoint looks like this
```
{type: EP, endpoint: <the URI>, publicKeyRef: <Optional field. The key reference in case the endpoint is not a DID>}
```
On adding the endpoint, it is assigned an integer which is used to reference this endpoint. The integer is monotonically increasing in the context of the DID, starting from 1, conceptually similar to the monotonically increasing key reference.
In case when the endpoint is not a DID, reference to one of this DID's key is needed sending encrypting messages to this endpoint.

The transaction payload to update an endpoint looks similar to this.
```
{type: EP, endpoint: <the new URI>, epRef: <integer referencing the endpoint>, publicKeyRef: <Optional field. The key reference in case the endpoint is not a DID>}  
```

The transaction payload to remove an endpoint looks similar to this.
```
{type: EP, endpoint: '', epRef: <integer referencing the endpoint>}
```

## Implementation
[implementation]: #implementation

Currently indy-node stores the DID information in 2 query layers, the state trie which is queried for client queries since they need a proof and the `IdrCache` which is queried for signature verification and role based authorization checks. To implement above features it is proposed to store all the DID data like keys, endpoints, etc as a JSON for the DID (hash of it) in the trie. The `IdrCache` should also store a JSON for the DID with key reference and key values both indexed. The endpoint references should be indexed as well. This will require a migration of the trie and `IdrCache` during deployment. Something to note is that the DID doc outputted by Indy-sdk has to be compliant with the DID doc in Sovrin DID method spec but the data organization on Indy nodes is independent of that.

# Drawbacks
[drawbacks]: #drawbacks

None.

# Rationale and alternatives

The HIPE diverges from the DID specification by W3C as:

1. The HIPE proposes to add authorizations for keys.
2. The HIPE proposes to add tags for keys.
3. The HIPE proposes to assign auto-generated identifiers (called reference in the HIPE) to endpoints and keys.

But these are necessary for use cases Indy needs to support.

# Prior art

1. [The DID specification](https://w3c-ccg.github.io/did-spec/).
2. [Sovrin DID method specification](https://github.com/sovrin-foundation/sovrin/blob/master/spec/did-method-spec-template.html)
3. The transactions and authorization rules are similar to [Relationship State Machine HIPE (In review)](https://github.com/hyperledger/indy-hipe/pull/31)

# Unresolved questions

[unresolved]: #unresolved-questions
1. Should keys with `REM_KEY` be allowed to remove keys with `ADMIN` authorization or should keys with `ADMIN` be removable by keys with `ADMIN` authorization? 
1. Implementing more flexible authorization like 2 of the 5 keys have to agree to add a new key.
1. Should keys with `MOD_KEY` be allowed to change authorizations of a key with `ADMIN` authorization? Do we need an authorization called `ADMIN` that is distinct from `ADMIN` and immune to such actions?
1. Should `pay` be introduced as an endpoint as anyone with `MOD_EP` authorization can make himself receive payments?
