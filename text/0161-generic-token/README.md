# 0161: Generic Tokens
- Authors: [Brent Zundel](brent.zundel@evernym.com), [Lynn Bendixsen](lynn@indicio.tech)
- Start Date: 2020-09-17

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: 2020-09-17
- Status Note: (explanation of current status; if adopted, 
  links to impls or derivative ideas; if superseded, link to replacement)

## Summary
[summary]: #summary

This HIPE introduces a generic token, for use as a payment mechanism on an indy ledger. It describes transactions for creating and transferring tokens, as well as the data structures and protocols around recording token transactions.

## Motivation
[motivation]: #motivation
### To protect an Indy ledger
Most instantiations of Hyperledger Indy are public-permissioned distributed ledgers.
- It is public, in that anyone should be able to read from the ledger.
- It is permissioned, in that only a select set of validator nodes may write to the ledger.

For an entity to submit a request to the validators for a transaction to be written to the ledger, the party must either hold a certain role known as a Transaction Endorser (Endorser), or process the transaction request through an Endorser. This role is only granted to "trusted" entities, usually after they have signed an official Endorser Agreement document. The purpose of the Endorser role is to protect the ledger from malicious transaction requests.

Changing this to allow anyone to submit transactions to the validators is problematic. If anyone with a network connection can submit transaction requests to validators, it is theoretically possible for anyone to overwhelm a validator with too many transaction requests, and thus overwhelm the validator pool as they work to consider the load of transaction requests. For this reason, transaction requests pass through an Endorser.

The drawback of this protection mechanism is that it makes the ledger less accessible to anyone outside of the trusted circle. If an Indy ledger is truly to be a global public utility, the ability to request that a transaction be written to the ledger should be available to anyone. This is the primary motivation for introducing a token as a payment mechanism for transaction requests.

If submitting a transaction request to a validator did not require a party to be trusted, but instead required a small fee, this would provide an economic disincentive to abuse the ledger while allowing anyone to submit transaction requests.

### To provide a payment mechanism for the masses
Many Indy ledger users desire a network designed with a utility payment mechanism to allow for on-ledger transfer of value. Building this payment plugin opportunity directly into the main codebase will fill that need in the simplest, and most direct way.

## Tutorial
[tutorial]: #tutorial

### Introduction
The generic token can be defined and used in any manner an Indy ledger implementer would like to. Consensus around valid token transactions occurs with the same pool of validator nodes as every other transaction. Fees that accompany transactions are processed atomically with those transactions, so they fail or succeed together.

The infrastructure for value transfer on a ledger consists of a payments sub-ledger (much like the domain and pool sub-ledgers) that records payment transactions. Setting fees writes a fee schedule to the existing config sub-ledger and setting Auth_Rules allows for those fees to be applied to any desired transactions. There is also a cache of unspent transaction outputs, or _UTXOs_.

### Denomination
- Each generic token consists of 1 x 10<sup>9</sup> tokatoms.
- Tokatoms are the smallest unit and are not further divisible.
- All `amount` fields in payment APIs are denominated in tokatoms.
  - This allows transaction calculations to be performed on integers.
- 1 x 10<sup>10</sup> (10 billion) generic tokens may be minted, and all of the resulting 1 x 10<sup>19</sup> tokatoms may be stored using a 64-bit integer.

### The Payment Ledger
The payment ledger makes use of Plenum to come to consensus about payment
transactions. The validation of these transactions includes:
- double-spend checking,
- verification of payment signatures,
- and enforcing the equality of input and output amounts.

After using Plenum to come to consensus, payment and fee transactions are
recorded on the payment ledger. The fee schedule is recorded on the config ledger.

The transaction types handled by the payment ledger are:
- **MINT_PUBLIC** - Creates generic tokens as a transaction on the payment ledger. The minting of tokens typically requires the signatures of multiple trustees, but is configurable.
- **XFER_PUBLIC** - Transfers generic tokens from a set of input payment addresses to a set of output payment addresses. This transaction is recorded on the payment ledger.
- **GET_UTXO** - Queries the payment ledger for unspent transactions held by a payment address.
- **SET_FEES** - Sets the fee schedule for ledger transactions, including transactions recorded on other sub-ledgers. This transaction is recorded on the config ledger. The setting of fees typically requires the signatures of multiple trustees, but is configurable.
- **GET_FEES** - Queries the config ledger to retrieve the current fee schedule.
- **FEES** - Attaches a fee payment, according to the Auth_Rules in conjunction with the fee schedule, to transactions requests. The fee payment is recorded on the payment ledger. This is never an independent transaction, but always attached to the primary transaction request for which fees are being paid.

### Configurable Token Name
The token plugin has a configurable name, allowing network operators to set the name used in payment addresses. This value defaults to `tok`, and that default will be used in documentation and examples.

### Payment Address
A *payment address* is a string with the structure: <code>pay:tok:\<Ed25519
Verification Key>\<Checksum></code>. An address is the identifier for some number of UTXOs. Each UTXO contains some number of tokens.

A *payment key* is the Ed25519 signing key that corresponds to the verification key in the payment address. In order for a value transfer to be authorized, it must be signed by the payment key for for each payment address used as an input in the transaction.

#### UTXOs

A payment address is associated on the ledger with a number of unspent transaction outputs (UTXOs). A UTXO is identified by the payment address it is associated with and the sequence number of the transaction in which it was created. For example, a UTXO for address pay:tok:12345 that was created during transaction number 293, would be identified as pay:tok:12345:293. 
Whenever a token transaction is recorded on the payment ledger, the result is the spending or creation of some number of UTXOs. When a UTXO is used as input in a payment transaction, the UTXO is spent along with all of the tokens contained therein. The output of a payment transaction is a set of new UTXOs.

Note: If a sender has a UTXO that contains 100 tokens and wishes to send 60 tokens to a recipient, the sender must specify a payment address at which they wish to receive the remaining balance of tokens from the spent UTXO.

For example:
1. A **MINT** transaction creates 100 tokens for address pay:tok:12345. The **MINT** transaction is recorded on the ledger at sequence number 52.
   1. These tokens exist on the ledger as a single UTXO that is associated with address pay:tok:12345 and sequence number 52.
1. A **XFER_PUBLIC** transaction transfers 60 tokens from address pay:tok:12345 to address pay:tok:98765. The **XFER_PUBLIC** transaction is recorded on the ledger at sequence number 69.
   1. This transaction spends the UTXO pay:tok:12345:52 and creates two new UTXOs, one for the recipient, and one for the remaining tokens.
      1. UTXO pay:tok:98765:69 that contains 60 tokens for the recipient.
      2. UTXO pay:tok:12345:69 that contains 40 tokens as change for the sender.

      Note: The change UTXO does not need to use the same payment address as an input UTXO.
   2. The **XFER_PUBLIC** transaction is valid because:
      1. pay:tok:12345:52 had not previously been spent.
      2. The transaction was signed by the payment key for pay:tok:12345.
      3. The transaction input from pay:tok:12345:52 (100 tokens) was equal to the output in pay:tok:98765:69 and pay:tok:12345:69 (60 + 40 tokens).

### UTXO Cache
The UTXO cache is used to facilitate the efficient answering of payment ledger queries. This cache is used to answer the following questions:
1. Given a UTXO, has the UTXO been spent and what is its associated value?
   - Each UTXO is prepended with a "0" and is encoded to create a key. This key
    is added to the cache. The value associated with this key is the number of tokens held by that address at that sequence number.
    - For example: if the UTXO for payment address pay:tok:24601 at sequence number 557 has 10 tokens, the key would be 0:pay:tok:24601:557 and the value would be 10.
2. Given an address, what are all the UTXOs?
   - An address is prepended with "1" and then encoded to create a key which is added to the cache. The value associated with this key is a delimiter-separated list of the sequence numbers of the transactions for which the address has unspent amounts.
   - For example: if the address pay:tok:8675309 was sent tokens in transactions with sequence numbers 129, 455, and 1090, and none of the tokens has been spent, then the key would be 1:pay:tok:8675309 and the value would be 129:455:1090.

The UTXO cache is updated whenever a payment transaction is written to the ledger.

### Transaction Fees
The primary purpose of transaction fees is to reduce spam and to introduce a financial disincentive for DDoS and similar attacks. A ledger operator can offer open access by setting the fees for ledger transactions high enough to discourage abuse of the network while at the same time keeping fees as low as possible.

The fees are set and maintained by the ledger operator. The transactions for which fees are collected are the transactions that require the most work from validator nodes, namely requests to write to the ledger.

These transactions are configurable, but typically are the following:
- NYM
- ATTRIB
- SCHEMA
- CRED_DEF
- REVOC_REG_DEF
- REVOC_REG_ENTRY
- XFER_PUBLIC

Transactions with fees may be added or removed from this list.

### Incorporation with Hyperledger Indy
Hyperledger Indy provides the code base for Indy ledgers. This code base may be extended with plugins. Ledger plugins add new transactions and sub-ledgers to the transactions and sub-ledgers already defined by Hyperledger Indy.

#### Ledger Plugins
The process for adding plugins to Hyperledger Indy is explained in [Hyperledger's indy-plenum repository](https://github.com/hyperledger/indy-plenum/blob/master/docs/source/plugins.md).

Plugins allow for new transactions to be added to an instantiation of Indy, without requiring changes to the core codebase. New sub-ledgers may also be defined using these plugins. A sub-ledger is where the new transactions may be stored.

Two ledger plugins are proposed in this document:
- A Generic Token plugin, which adds a payments sub-ledger and the following transactions:
   - **MINT_PUBLIC**
   - **XFER_PUBLIC**
   - **GET_UTXO**
- A Fees plugin, which adds the following transactions to the payments sub-ledger mentioned above:
   - **GET_FEES**
   - **SET_FEES**
   - **FEES**

Note: While the Generic Token plugin and the accompanying payment sub-ledger may be used without the Fees plugin, the Fees plugin depends on the Generic Token plugin.

#### Indy-SDK Payments API Plugin
The Indy-SDK payments API comes with a default payment handler plugin called
[LibNullPay](https://github.com/hyperledger/indy-sdk/blob/master/libnullpay/README.md). LibNullPay allows for a "null" token to be used with the payments API. The "null" token transactions are dummy transactions. They are not stored on a ledger and do not initiate consensus.

The payments API allows for other payment handler plugins to be initialized. An Indy-SDK payments API compatible payment handler is proposed in this document:
- LibTokToken, which handles generic token payment functionality through the Indy-SDK payments API for the Token and Fees ledger plugins and produces properly formatted and signed transaction requests for each of the new transactions listed above. LibTokToken also parses the transaction responses from the new ledger plugins through the Indy-SDK payments API.

## Reference
[reference]: #reference

Documentation for the proper format of transaction requests and transaction responses for the generic token plugin, specifically for the **MINT_PUBLIC**, **XFER_PUBLIC**, and **GET_UTXO** transactions can be found here: [Ledger Token Transactions.](TODO: add link)

Documentation for the proper format of transaction requests and transaction responses for the Fees plugin, specifically for the **SET_FEES**, **GET_FEES**, and **FEES** transactions can be found here: [Ledger Fee Transactions.](TODO: add link)

Documentation for the Indy-SDK payments API and how to use it may be found here: [Indy SDK Payments API.](https://github.com/hyperledger/indy-sdk/tree/master/docs/design/004-payment-interface)

An example of the structure of the inputs and outputs of the LibTokToken payment handler plugin for the Indy-SDK payments API are documented here: [Token specific data structures.](https://github.com/sovrin-foundation/libsovtoken/blob/master/doc/data_structures.md) (from LibTokTokens predecessor LibSovToken)

## Drawbacks
[drawbacks]: #drawbacks

### Undesired Speculation
The intention of the generic token is to enable a more public way to submit transaction requests or provide for an alternative payment method without compromising the security and performance of the ledger validator nodes. However, the introduction of the token may be incorrectly viewed as an invitation for speculators to purchase generic tokens, even though they have no intention of making use of the utility provided by the generic token.

This speculative action may cause the value of a generic token to fluctuate, requiring a quick response from the ledger operator in adjusting the fee schedule for ledger transactions so that fees remain reasonable.

### Additional Costs
Moving from an Endorser model, where trusted entities can submit write transaction to the ledger, to a Token model, where submitting a write transaction requires the payment of fees denominated in generic tokens, will likely introduce new costs to those who are currently trusted entities.

### Load on the Ledger
Adding transactions potentially increases load on the validator nodes and the size of the ledger. Each request for a write transaction now also requires a **FEE** transaction, effectively doubling the computational load on each validator for write transactions.

A **FEE** transaction always accompanies some other primary transaction. The two transactions must be atomic:
- the primary transaction should not be processed if the **FEE** transaction fails,
- the **FEE** transaction should not be written if the primary transaction fails.

Recording the **FEE** transaction on the payment sub-ledger and the primary transaction on another sub-ledger may require that the two sub-ledgers be synchronized in some way. This may also cause difficulties during catchup (when a validator node updates its state to be current with the rest of the validator pool). This might no longer be a drawback due to the introduction of the audit ledger.

If the generic token begins to be commonly used for other payments besides fees, there will be additional load on the validator nodes as they come to consensus on the **XFER_PUBLIC** transactions.

## Rationale and alternatives
[alternatives]: #alternatives

This design for a generic token described here is simple. It is based on the UTXO model for transactions found in [bitcoin](https://bitcoin.org/en/bitcoin-paper), which simplifies validity checking for payment transactions.

If a generic token is not introduced, every network desiring token based payment transfers must write their own plug-in and build their own branding.

## Prior art
[prior-art]: #prior-art

This proposal was inspired by the Sovrin Token and its associated [SIP](https://github.com/sovrin-foundation/sovrin-sip/tree/master/text/5003-sovrin-tokens). 

## Unresolved questions
[unresolved]: #unresolved-questions

There are a number of questions that remain unanswered, some of which may be
outside of the scope of this effort:
- How will the generic token and the payment ledger affect the catchup process
for validator nodes?
- What impact will the introduction of fees have on the time it takes to process transactions, and how can this impact be mitigated?
- Are there GDPR and privacy issues that need to be addressed?
- How could the adjustment of the fee schedule in response to changes in the value of the token be automated?
