- Name: a2a-forward-secrecy
- Author: Mike Lodder
- Start Date: 2018-08-29
- PR: (leave this empty)
- Jira Issue: (leave this empty)

# Summary
[summary]: #summary

Specify the protocol to add forward secrecy between agent to agent messaging.

# Motivation
[motivation]: #motivation

Agent to agent communication uses Elliptic-Curve Integrated Encryption Scheme (ECIES) to protect messages.
While this protection is good, it does not provide *forward-secrecy* and *key-compromise impersonation resistance*.

[Forward-secrecy](https://en.wikipedia.org/wiki/Forward_secrecy) is the idea that compromise of the end point long term keys will not compromise the session keys. For agent to agent communication, a session is agent 1 sending a message to agent 2. Each message transmitted is a session.Key compromise impersonation means an active attacker that gains knowledge of the private key and can replace (impersonate) the agent when communicating. Agents that have active (synchronous) connections can achieve this using ephemeral keys to establish each session key. This is much harder to do when messages are delivered asynchronously. Another vector of attack stems from reusing keys. The more a key is used the higher the likelihood an attacker can deduce the long term keys. If care is not taken with how messages are encrypted then messages with the same plaintext can yield the same ciphertext which allows an attacker to correlate two messages from the same agent.

[Signal](https://signal.org/docs/specifications/doubleratchet/) is a protocol that provides the forward-secrecy and key-compromise impersonation resistence for both synchronous and asynchronous messaging. This HIPE proposes to implement the **Signal** protocol for agent-to-agent communication to improve security and privacy–specifically the double ratchet algorithm.

# Tutorial
[tutorial]: #tutorial

### Terminology

- **isk**: The sending agent's identity secret key.
- **ivk**: The sending agent's identity verification (public) key.
- **rivk**: The receiving agent's identity verification (public) key.
- **revk**: The receiving agent's ephemeral verification (public) key.
- **esk**: The sending agent's ephemeral secret key.
- **epk**: The sending agent's ephemeral public key.
- **KDF**: Key Derivation Function–derives one or more secrets from a master key. Acceptable functions are [SHAKE128](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.202.pdf), [SHAKE256](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.202.pdf), [HKDF](http://www.ietf.org/rfc/rfc5869.txt), [Argon2id](https://download.libsodium.org/doc/password_hashing/the_argon2i_function), or [Scrypt](https://www.rfc-editor.org/rfc/rfc7914.txt). If variable key lengths are not needed or smaller than the function outputs, then functions from the SHA2 or SHA3 family could be used as well.
- **ECIES**: Encryption system that uses Diffie-Hellman (DH) with **isk** and **rivk** to compute a shared secret **K.1** and **K.2** using a KDF. This is used to encrypt a message and compute an integrity check tag. The encrypted message and tag are sent to remote party *r*. *r* uses their local **isk** and **rivk** to compute the same secrets and decrypt the message and check the tag.
- **AuthCrypt**: ECIES involving both agents' static keys that also signs the payload with **isk**. Provides non-reputability for the sender.
- **AnonCrypt**: ECIES involving the receiving agent's static keys and ephemeral keys from the sender. Receiver does not know who sent the message.
- **1**: Agent 1 - Alice
- **2**: Agent 2 - Bob
- **||**: byte concatentation. For example 1001 **||** 0011 = 10010011

### Review

**Microledgers**
Indy agents currently use either *anoncrypt* or *authcrypt* to send messages. *Authcrypt* provides no forward-secrecy or key-compromise resistance for either agent. *Anoncrypt* provides forward-secrecy for the sending agent but not the receiving agent. An attacker can still decrypt the message from the receiving agent's long term identity key but not the sender's. This is known as weak forward secrecy. The existing architecture does provide a secure method for changing identity keys using microledgers. When agent 1 rotates identity keys, the transaction is signed using the existing **isk**. The transaction and new **ivk** are sent to agent 2. Agent 2 verifies the transaction using agent 1's old **rivk** . If the transaction is valid, agent 2 updates to the new **rivk**.

**Signal Double Ratchet Algorithm**
The algorithm is implemented by each party performing a key agreement to initially seed a Diffie-Hellman (DH) ratchet and using the ratchet to generate single use encryption keys. The ratchet is seeded with a *Root* key. Another DH keypair is used to create an output that is combined with the initial seed as input to a KDF to derive a sending ratchet and receiving ratchet. Every message is encrypted with a unique message key. The message keys are output keys from the sending and receiving chains. Calculating the next message key uses the current ratchet value and a constant as inputs to a KDF. Part of the output replaces the existing sending/receiving ratchet value and the other part becomes the message key. A message key is a symmetric encryption key.

When *1* sends a message to *2*, a sending message key is computed to encrypt the message, and the current DH public key is sent with the message. *2* calculates a receiving message key to decrypt the message. *2* takes the DH public key received from *1* and creates a new DH keypair. This is used to ratchet the *Root* key. This then replaces the sending and receiving seeds. This process repeats for both agents as they send and receive messages which rotates and updates their ratcheting chains. *Signal* also allows the header metadata to be encrypted. Encrypting the header section is desirable to prevent correlation and enhance privacy.

### Overview

**Channel Setup**
Two parties connect agents out of band by scanning QR codes or manually entering information into an app. Currently, only the long term identity keys are exchanged. This proposal adds an additional one-time DH key to be exchanged as well. Each of the keys are used to calculate seed values and initialize the microloedger in the following manner:

*1* sends *2* in an initial message:

- Identity Key *ivk*
- Ephemeral public key *epk*
- An initial ciphertext encrypted with some AEAD encryption scheme (AES-GCM, SALSA20 or CHACHA20 with POLY1305) using *AD = ipk || ripk*. *AD* contains identity information for both parties. The intitial ciphertext should contain the first ratchet DH key.

*1* calculates using her private keys and *2*'s public keys:

```
DH1 = DH(isk, rivk)
DH2 = DH(esk, rivk)
DH3 = DH(esk, repk)

RK = KDF(DH1, DH2, DH3)
```
Note that *DH1* and *DH2* provide mutual authentication while *DH3* provides forward secrecy.

When *2* receives the intial message or QR code, she repeats the same calculations as *1* and attempts to decrypt the intitial ciphertext. If decryption fails, then *2* aborts the protocol and deletes the public keys. If decryption succeeds, the setup completes by *2* calculating the message and header *RK*s deleting the ephemeral message and header public keys, storing *1*'s identity public key in the microledger, and storing the current ratchet public key for *1*. *2* then sends an initial message to *1* and *1* repeats the same process.

This setup is based on [Signal's X3DH](https://signal.org/docs/specifications/x3dh/), the main difference being there are no central servers for *1* to find *2* and visa versa and *1* and *2* authenticate each other as part of the setup.

**Agent-to-Agent Messages**
Agents may now use the signal protocol to send encrypted messages. Each agent keeps state for the following variables:

- **DHs**: The current sending DH ratchet key pair.
- **DHr**: The current receiving DH public key.
- **RK**: 32 byte message root key.
- **MCKs, MCKr**: 32 byte chain keys for sending and receiving messages
- **HKs, HKr**: 32 byte header keys for sending and receiving
- **NHKs, NHKr**: 32 byte next header keys for sending and receiving
- **Ns, Nr**: Message numbers for sending and receiving
- **PN**: Number of messages in previous sending chain
- **MKSkipped**: Dictionary of skipped-over message keys, indexed by header key ratchet public kye and message number.

Messages may be received out-of-order. Signal's double ratchet handles this by tracking *N* and *HK* in each message. If a ratchet step is triggered, the agent will store any keys needed to decrypt missing messages later before performing the ratchet. Messages received are decrypted using the current message key. The message key is immediately deleted. Message storage can use different encryption techniques local to the agent system going forward. When a message is sent, the sending encryption key is subsequently deleted.

When a ratchet is performed, the current *RK*'s are updated and *N* is reset back to 1. Skipped message keys are derived and stored in *MKSkipped* based on the *N* received and the current expected value. *MKSkipped* keys should only be stored for an acceptable amount of time (highly sensitive applications may not store them at all, where less sensitive ones may store them for one week. 72 hours is an acceptable default. Storing up to 5 asymmetric updates previous chain message keys is acceptable but probably no more if lots of messages are being dropped then it could indicate a man-in-the-middle or a faulty agent. No more than 2000 skipped message keys should be stored).

### Encrypted message header format

The encrypted header is the concatenation of the following fields

```
Version || Nonce or IV || Ciphertext || Tag || HMAC
```

- *Version*, 8 bits
- *Nonce or IV*, variable length multiple of 32 bits
- *Ciphertext*, encrypted header, variable length
- *Tag*, 128 bits
- *HMAC*, 256 bits

### Encrypted header fields

#### Version
This field denotes which version of the format is being used. There are three versions defined:

- *16 (0x10)*: Version 1 for using Salsa20-Poly1305 (IETF or extended versions too) authenticated encryption
- *32 (0x20)*: Version 1 for using Chacha20-Poly1305 (IETF or extended versions too) authenticated encryption
- *64 (0x40)*: Version 1 for using AES256-GCM authenticated encryption

#### Nonce or IV
The 128 bit initialization vector for AES-GCM or 196 bit nonce for Salsa/Chacha.
This value MUST be unique and unpredicatable for each message. With a high-quality source of entropy,
random selection will do this with high probability

#### Ciphertext
This field has variable size. It contains the unencrypted header metadata.

#### Tag
The tag used to authenticate the message.

#### HMAC
The 256-bit SHA256 HMAC, under the header or next header signing-key, of the concatenation of the following fields:
```
Version || Nonce or IV || Ciphertext || Tag
```

#### Associating the message
An agent may have multiple channels from which a message can come. To associate this message with the correct channel,
the agent tries to HMAC and decrypt the header using known channel header keys and the *AD* for that channel. HMAC and decryption will
fail for incorrect channels and only succeed for a correct channel. Once channel association is established, decrypting
the message can begin. See [Double ratchet with header encryption](https://signal.org/docs/specifications/doubleratchet/#double-ratchet-with-header-encryption) for more details about ratcheting header keys.

### Unencrypted header format

The header is the concatenation of the following fields:

```
Version || Timestamp || PN || N || DHr
```

- *Version*, 8 bits
- *Timestamp*, 64 bits
- *PN*, 32 bits
- *N*, 32 bits
- *DHr*, variable length depending on DH key scheme

#### Version

Denotes which version of the format is being used. There is only one version defined, with the value 128 (0x80).

#### Timestamp
64-bit unsigned big-endian integer. Records the number of seconds elapsed between Janurary 1, 1970 UTC and the time the message was created.

#### PN

The number of messages in previous sending chain.

#### N

The message ID for the current sending and receiving chains.

# Reference
[reference]: #reference

This HIPE is designed to work with Ed25519 keys but could work with any public key crypto system.

[Signal](https://signal.org/docs/)

# Drawbacks
[drawbacks]: #drawbacks

This HIPE adds complexity to agent-to-agent messaging. It requires knowledge of cryptographic functions, more local space for storing state variables, and proper management 
of state variables.
State variables will need to be backed up to resume channels. 
Syncing these values across agents that belong to the same identity will be impossible. Each of Alice's agents will need to maintain their own state variables.
This inhibits the possibility of using group encryption or group signatures to hide how many agents Alice has and which of her agents she is using. But since Alice trusts Bob enough to establish a channel with him, it might be an okay tradeoff.

# Rationale and alternatives
[alternatives]: #alternatives

Encrypted messaging has been around for long time and is a well understood problem.
Indy could try to come up with its own asyncronous messaging protocol but will probably not be able to create one better than Signal nor as widely adopted.
Signal is supported and improved by Open Whisper Systems and the Signal Foundation.
Signal has been vetted by cryptographers and security professionals alike who have found it to be secure ([Signal audit](https://threatpost.com/signal-audit-reveals-protocol-cryptographically-sound/121892/) and [A Formal Security Analysis of the Signal Messaging Protocol](https://eprint.iacr.org/2016/1013.pdf)).

Signal has been implemented in multiple programming languages already so the protocol does not need to be written from scratch. The open source libraries can be used directly with Indy.

# Prior art
[prior-art]: #prior-art

As stated, encrypted messaging between two parties is a well understood problem. Multiple solutions currently exist but the most popular are Off-the-record (OTR), Silent Circle's Silent Text, Secure Chat, iMessage, and others. Signal evolved by combining the best of many of these and fixing existing weaknesses.

# Unresolved questions
[unresolved]: #unresolved-questions

- How should agents backup and restore their state variables?
