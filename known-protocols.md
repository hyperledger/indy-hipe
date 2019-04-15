# Known Protocols

## Summary
This is a list of known protocols that are implemented in one or more Indy Agents. Some of the protocols are standardized, and therefore MUST be supported by all Indy Agents, where as some are informal specifications that are interoperable between only one or a few agent implementations. For the sake of developer discovery and to reduce overlap, these are included in here as well.

## What is a protocol?

As described in the [protocol explainer HIPE](https://github.com/hyperledger/indy-hipe/blob/c9b0888016d924e5f57abc04a5a08a09773f08f5/text/protocols/README.md) ***A protocol is a recipe for a stateful interaction.***

Protocols are all around us, and are so ordinary that we take them for granted. Each of the following interactions is stateful, and has conventions that constitute a sort of "recipe":

* Ordering food at a restaurant
* Buying a house
* Playing a game of chess, checkers, tic-tac-toe, etc.
* Bidding on an item in an online auction.
* Going through security at the airport when we fly
* Applying for a loan

For additional details about protocols, please refer to the [protocol explainer HIPE](https://github.com/hyperledger/indy-hipe/blob/c9b0888016d924e5f57abc04a5a08a09773f08f5/text/protocols/README.md).

## Adopted Standard Protocols

| Protocol Name | Protocol Description |
| -------- | -------- |
|[Wire Message Format](text/0028-wire-message-format/README.md) | A message format to encrypt and decrypt messages between peers in both an anonymous and authenticated way. This is the base protocol that all other protocols SHOULD use to handle confidentiality and integrity of messages.|
| [Connection Protocol](text/0031-connection-protocol/README.md) | This is a protocol used to setup a persistant connection with another peer. It's designed to support pairwise, n-wise, and anywise relationships |
| [Trust Ping](text/0032-trust-ping/README.md) | Describe a standard way for agents to test connectivity, responsiveness, and security of a pairwise channel.  |
| [Basic Message](text/0033-basic-message/README.md) | The BasicMessage message family describes a stateless, easy to support user message protocol. It has a single message type used to communicate. |


## Accepted Shared Protocols

At this time, the ***"Accepted"*** protocols which have not standardized yet are not being included in here. The intent is to wait until the [updated HIPE process](https://github.com/hyperledger/indy-hipe/blob/c6b0b9cbb2ac41d4283da470e6bf454b80f08ecb/README.md) has been added and then we can build this table out. This has been intentionally done, so that this isn't linking to many different forks and pull requests of the Indy HIPE repository.