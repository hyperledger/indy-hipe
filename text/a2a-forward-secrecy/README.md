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

#### Terminology

**isk**: The sending agent's identity secret key.
**ivk**: The sending agent's identity verification (public) key.
**rivk**: The receiving agent's identity verification (public) key.
**esk**: The sending agent's ephemeral secret key.
**epk**: The sending agent's ephemeral public key.
**KDF**: Key Derivation Function–derives one or more secrets from a master key.
**ECIES**: Encryption system that uses Diffie-Hellman (DH) with **isk** and **rivk** to compute a shared secret **K.1** and **K.2** using a KDF. This is used to encrypt a message and compute an integrity check tag. The encrypted message and tag are sent to remote party *r*. *r* uses their local **ssk** and **rsvk** to compute the same secrets and decrypt the message and check the tag.
**AuthCrypt**: ECIES involving both agents' static keys that also signs the payload with **isk**. Provides non-reputability for the sender.
**AnonCrypt**: ECIES involving the receiving agent's static keys and ephemeral keys from the sender. Receiver does not know who sent the message.
**1**: Agent 1 - Alice
**2**: Agent 2 - Bob

#### Review

**Microledgers**
Indy agents can use either *anoncrypt* or *authcrypt* to send messages. *Authcrypt* provides no forward-secrecy or key-compromise resistance for either agent. *Anoncrypt* provides forward-secrecy for the sending agent but not the receiving agent–an attacker can still decrypt the message from the receiving agent's long term secret key but not the sender's-weak forward secrecy. The current architecture does provide a secure method for changing identity keys using microledgers. When agent 1 rotates her identity keys, she signs the transaction and new **ivk** using her existing **isk** and sends the transaction and new **ivk** to agent 2. Agent 2 verifies the transaction using agent 1's old **rivk** . If the transaction is valid, agent 2 updates to the new **rivk**.

**Signal Double Ratchet Algorithm**
The algorithm is implemented by each party performing a key agreement to initially seed a Diffie-Hellman (DH) ratchet. This is called the *Root* key. Another DH keypair is used to create an output to be combined with the initial seed as input into a KDF to derive a sending ratchet and receiving ratchet. Every message is encrypted with a unique message key. The message keys are output keys from the sending and receiving chains. Calculating the next message key uses the current ratchet value and a constant as inputs to a KDF. Part of the output replaces the existing sending/receiving ratchet value and the other part becomes the message key. A message key is a symmetric encryption key. When **1** sends a message to **2**, a sending message key is computed to encrypt the message, and the current DH public key is sent with the message. **2** calculates a receiving message key to decrypt the message. **2** takes the DH public key received from **1** and creates a new DH keypair. This is used to ratchet the *Root* key. This then replaces the sending and receiving seeds. This process repeats for both agents as they send and receive messages. *Signal* also allows the header metadata to be encrypted using this algorithm with a separate ratchet chain. Encrypting the header section is desirable to prevent correlation and enhance privacy.

#### Overview



# Reference
[reference]: #reference

Provide guidance for implementers, procedures to inform testing,
interface definitions, formal function prototypes, error codes,
diagrams, and other technical details that might be looked up.
Strive to guarantee that:

- Interactions with other features are clear.
- Implementation trajectory is well defined.
- Corner cases are dissected by example.

# Drawbacks
[drawbacks]: #drawbacks

Why should we *not* do this?

# Rationale and alternatives
[alternatives]: #alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not
choosing them?
- What is the impact of not doing this?

# Prior art
[prior-art]: #prior-art

Discuss prior art, both the good and the bad, in relation to this proposal.
A few examples of what this can include are:

- Does this feature exist in other SSI ecosystems and what experience have
their community had?
- For other teams: What lessons can we learn from other attempts?
- Papers: Are there any published papers or great posts that discuss this?
If you have some relevant papers to refer to, this can serve as a more detailed
theoretical background.

This section is intended to encourage you as an author to think about the
lessons from other implementers, provide readers of your proposal with a
fuller picture. If there is no prior art, that is fine - your ideas are
interesting to us whether they are brand new or if they are an adaptation
from other communities.

Note that while precedent set by other communities is some motivation, it
does not on its own motivate an enhancement proposal here. Please also take
into consideration that Indy sometimes intentionally diverges from common
identity features.

# Unresolved questions
[unresolved]: #unresolved-questions

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
