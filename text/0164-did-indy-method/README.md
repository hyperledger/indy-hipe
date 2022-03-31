# Indy HIPE 0164: did:indy Method
- Author: Daniel Bluhm, Char Howland, Adam Burdett
- Start Date: 2022-03-25

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: (date of first submission or last status change)
- Status Note: (explanation of current status; if adopted, 
  links to impls or derivative ideas; if superseded, link to replacement)

## Summary
This method adds support for W3C DID Specification compliant identifiers and documents on Indy Ledgers.


## Motivation
This method aligns Indy with the DID Core specification by formalizing the transformation of an Indy ledger object into a W3C DID Core Spec-compliant DIDDoc. Previous to the definition of the Indy DID Method specification, DID Documents from Indy Nyms were constructed following convention only. This convention used nym and attrib transactions to construct rudimentary DID Documents.

In addition, this method implements a network-specific identifier, creating a "network of networks" capability where an Indy DID can be uniquely resolved to a specific DIDDoc stored on a specific Indy network using a common resolver software component. This enables useful properties including decentralization, scalability, fit for purpose, and governance. See the [Indy DID Method Specification](/https://hyperledger.github.io/indy-did-method/#motivation-and-assumptions) for more details.

This method allows a holder/prover to receive credentials from issuers from different Indy networks and be able to construct a single AnonCreds verifiable presentation that uses all of those credentials. It allows an issuer to publish a DID Doc on an Indy ledger containing a BLS Key so that they can issue W3C Standard Verifiable JSON-LD Credentials using BBS+ Signatures.


## Tutorial

### DIDDoc Support
As discussed in [Indy DID Method 10.1: Creation](/https://hyperledger.github.io/indy-did-method/#creation), to support writing full W3C compliant DID Documents to Indy Ledgers, this method adds an optional new attribute, `diddocContent`, to NYM transactions. This attribute will be a JsonField (JSON encoded string) with some length limit imposed and the contents of this field will be validated according to the rules in Validating DID Doc Content. (**LINK THIS**)

### DIDDoc Assembly Steps
See [DIDDoc Assembly Steps](\https://hyperledger.github.io/indy-did-method/#diddoc-assembly-steps) in the Indy DID Method Specification.

### Self-Certification of DIDs
Previously, NYM transactions did not require any link between their identifier and verification key. This makes proving ownership of Indy DIDs more difficult as arbitrary values (including "vanity DIDs") could be used. The Indy DID Method Specification accounts for this by introducing an explicit mechanism for self-certification However, this mechanism causes problems with backwards compatibility.

This proposal implements optional self-certification by including a new field that indicates to the handler whether the submitted nym is self-certifying. The self-certification algorithm to be validated on NYM creation is specified by an incrementing integer: NYM transaction version 0 requires no validation of namespace identifier and initial verkey binding is performed, version 1 requires validation according to the `did:sov` method, in which the DID must be the first 16 bytes of the Verification Method public key, and version 2 requires validation according to the `did:indy`, in which the namespace identifier component of the DID (last element) is derived from the initial public key of the DID, using the base58 encoding of the first 16 bytes of the SHA256 of the Verification Method public key.

The NYM transaction version field is optional and defaults to 0, or no validation of namespace identifier and initial verkey binding, if not set. It is stored as additional metadata and equal to true or false, but during this interim opt-in period, the transaction does not fail if self-certification evaluates to false. Non-self-certifying nym transactions still have the minimum level of security because all transactions need to be signed; self-certifying nym transactions provide a level up in security.

### ATTRIB Deprecation
The use of ATTRIB is deprecated with the introduction of the `did:indy` DID Method. The only common use of ATTRIBs in Hyperledger Indy prior to `did:indy` was to define DIDDoc service endpoints for a DID. Since with `did:indy` such a service endpoint can be added directly to the DID (along with any other DIDDoc data) there is no need to continue the use of the older ATTRIB endpoint convention. While a Hyperledger Indy client (such as Indy) MAY continue to try to resolve an endpoint ATTRIB when there is no DIDDoc content in a resolved DID, the ongoing practice of using an ATTRIB for that or any other purpose is discouraged.



## Reference (might be an appropriate spot for definitions, additional examples, maybe links to more resources or things that informed the implementation)

### Resolving by versionId and versionTime
As described in [Indy DID Method 10.3.1 DID Versions](/https://hyperledger.github.io/indy-did-method/#did-versions), it should be possible to resolve a particular version of a DID based on versionId (corresponding to a transaction sequence number) or on `versionTime`.

Indy natively supports retrieving transactions by sequence number using `GET_TXN`. Indy also supports retrieving the state of a nym at a particular point in time; however, this is not exposed directly in any read transactions but `GET_TAA` where it is used to check the value of the TAA at a given point in time.

To support resolving by `versionId` and `versionTime`, two new attributes are added to the `GET_NYM` transaction:
- `seqNo` (equivalent to `versionId`) - sequence number of the transaction resulting in the state we wish to retrieve
- `timestamp` (equivalent to `versionTime`) - retrieve state at this timestamp (state exactly at the time or before). This value is a POSIX timestamp.

`seqNo` and `timestamp` are mutually exclusive; if both are present, inform the client of invalid request. It will be the responsibility of the Resolver to transform a DID URL with these query parameters into the expected transaction format.



## Drawbacks

### Additional field for self-certification

As discussed above, enforcing self-certification for the `did:indy` method would limit backward compatibility and so the solution is to implement optional self-certification where the creator of a new nym can set the self-certification algorithm that will be validated by setting the version. Although self-certification will be enforced in the future, rendering this field irrelevant, it will still have to be present for the forseeable future.


#### Resolving by `versionId`

A sequence number refers to a specific transaction on Indy Networks. This means that, by retrieving a transaction, we are retrieving the operation data or the specific action that took place in that transaction. In other words (in the context of nyms, at least), a sequence number refers to a change to a nym and not the state of the nym after the change represented by the sequence number is applied. When retrieving by `versionId`, we are interested in the state of the nym and not the change taking place at that version.

The following option was determined to be the best balance between backwards compatibility, minimizing required changes, and implementing the spec as currently defined. To resolve a DID Document by `versionId`, the `GetNymHandler` will:
1. Retrieve the transaction identified by the versionId (sequence number)
2. Extract timestamp from the transaction
3. Retrieve the root hash at (or nearest previous root hash to) that timestamp from the timestamp store
4. Retrieve value of nym as contained in state at root hash

The drawback is that we have to resolve another transaction, which incurs additional cost, before recalling the state when the transaction identified by the sequence number was made.


## Rationale and alternatives

### Self-certifying Nym transaction transition
Imposing the self-certification requirement proposed in the Method Specification would be a significant breaking change for users of Indy Networks. Indy SDK users (which form a majority of the user base) would be unable to write new nyms without implementing workarounds as the SDK produces DIDs according to conventions incompatible with the self-certification requirement. As such, self-certification will not be enforced at this time.

However, in anticipation of enabling enforcement of self-certification at some future date, we have conducted some investigation of how this feature could be activated by networks.

#### Static Configuration
Using a static variable to trigger this similar to features being configured during testing was considered. This idea has been passed over because of the complexity of consensus in a pool and having each node in the pool turn on or off the static configuration at the same time.

#### Dynamic Configuration via Config Ledger
Our findings indicate that the config ledger is a preferable solution for nym self-certification configuration. To achieve this, we will need to add two handlers for the config ledger:

A transaction for updating the config and
a transaction for reading the state of the configuration.
With a new variable stored in the config ledger, the nym transaction handler will be able to access the config ledger in determining if self certification should be enforced.

If there is a bottleneck in accessing the config from the Patricia trie, we propose adding a flat “config cache” storage for a quick retrieval during nym transaction validation.


### Storage of DID Doc Content
`diddocContent` will be stored directly in the domain ledger state and will not require an additional store (as is the case for ATTRIB transaction data).

While investigating options for storage, it was determined that ATTRIB data was stored separately due to being arbitrary data not strictly required to represent the identity identified by the associated Nym. The size of the ATTRIB data, while significant when compared to the size of the typical NYM transaction, is dwarfed by the potential size of CLAIM_DEF and SCHEMA transactions. ATTRIBs are capped at 5KiB of raw data (size limit is imposed by transaction operation schema). CLAIM_DEF and SCHEMA transactions have no size limits and are bounded only by the maximum permitted message size of the secure transport layer of 128KiB. Therefore, it was determined that reasonable size limits should be imposed on DID Documents but any size up to the 128KiB message size cap is unlikely to negatively impact the performance of the network.

On inspection of old issues relating to the size limit on ATTRIB data, the 5KiB limit was chosen to enable batching of more ATTRIB transactions into a single 128KiB max message. This use case appears to only arise in testing scenarios.

The proposed (but still somewhat arbitrary) diddocContent size cap is 10KiB. In future iterations, this (and other size limits) should be network configurable through the config ledger.


### Validating DID Doc Content
Validation of the DID Document Content should be as minimal as possible. Minimal validation of the document content should ensure basic construction of a full DID Document while enabling usage of DID Document features not yet standardized or conceived. Overly strict validation would require code and network updates to allow such new features to be used on Indy Networks.

DID Doc Content should be validated as follows:
- Content is a JSON string (enforced by transaction operation schema)
- Content must not include id at root of the object
- Content must not include any nested objects with an id ending in <nym>#verkey


### Resolving a DIDDoc in a single transaction
Previous approaches to resolving Indy ledger objects into DIDDocs required the client read one or more ledger objects (notably, NYMs and ATTRIBs) before assembly. This is at best "challenging" for the client, and at worst, extremely slow without specialized ledger support, particularly when a non-current version of the DID is being resolved. A preferred approach is to enable the resolution of a DID via a single read transaction that returns a single object off the ledger, including a state proof for that object.

### Cross-Ledger Object References
The NYM controller of all objects on an Indy ledger MUST reside on the same Indy ledger as the object. Thus, the DID (e.g. the Indy NYM) of the Issuer of a verifiable credential type must reside on the same ledger as the CLAIM_DEF, REV_REG_DEF and REV_REG_ENTRY objects for that type of verifiable credential.

Note that the constraint above does not apply to a SCHEMA referenced by a CLAIM_DEF, since a CLAIM_DEF may use a SCHEMA written by another NYM. As such, a CLAIM_DEF may reference a SCHEMA on a different Indy ledger.



## Prior art

Early instances of Indy Networks used the `did:sov` DID Method. The following summarizes the differences between that `did:sov` and `did:indy`.

- A `did:indy` DID includes a namespace component that enables resolving a DID to a specific instance of an Indy network (e.g. Sovrin, IDUnion, etc.).
- `did:indy` DID validation is determined by NYM transaction `version`, as described in the DID Creation section. These restrictions MUST be enforced by the ledger.
- Identifiers for Indy ledger objects other than NYMs are adjusted to contain a namespace component.
- The specification includes rules for transforming a NYM into a DIDDoc that meets the DID Core Specification.
  - An optional NYM data item allows entities to extend the DIDDoc returned from a NYM in arbitrary ways.
  - The controller can decide whether the DIDDoc will be JSON or JSON-LD.
  - Before writing a NYM to the ledger, the NYM content is verified to ensure that transforming the NYM to a DIDDoc produces a valid JSON and may include DIDDoc validity checking.
  - The transformation of a read NYM to a DIDDoc is left to the client of an Indy ledger.
- A convention for storing Indy network instance config (“genesis”) files in a Hyperledger Indy project GitHub repository (“indy-did-networks”) is introduced.

## Unresolved questions

### Linked Transactions
Linked transactions as a means to prove self-certification is under investigation. This would entail providing the last transaction that modified the retrieved nym.
