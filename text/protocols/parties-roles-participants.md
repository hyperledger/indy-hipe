# Parties, Roles, and Participants

## Parties

The __parties__ in a protocol are the identity owners involved. The set of parties of a protocol is simple expression involvement in the protocol. Parties *must* be an identifiable self-sovereign domain. Although normally, the set of parties are known at the start of a protocol, that is not a requirement. Some protocols can commence without all parties known and a party could be included later in the course of the protocol. 

For many protocols, there are only two parties. And these protocols fit nicely into a pairwise relationship. But some protocol will only have one party (ex. wallet backup) and others will involve multiple parties (ex. introduction).

Normally, the parties that are involved in a protocol also participate in the interaction but this is not always the case. Consider a gossip protocol, two parties may be talking about a third party. In this case, the third party would not even know that the protocol was happening and would definitely not participate.

As an example, in an introduction protocol where Alice introduces Bob to Carol, the parties are Alice, Bob, and Carol.

## Roles 

The __roles__ in a protocol are the perspectives that parties take on an
interaction. 

This perspective is manifested in three general ways:
 * by the expectations that a party takes on in a protocol (ex. a role may be expected to do something to start a protocol).
 * by the messages that a party can and does use in the course of the protocol (some messages may be reserved for a single role, while other may used by some if not all roles).
 * by the state and the transition rules
 
Like parties, roles are normally known at the start of the protocol but this is not a requirement.

As an example, in an auction protocol, there are only two roles--*auctioneer*
and *bidder*--even though there may be many parties involved.

# Participants

The __participants__ in a protocol are the agents that actually move the steps of
the protocol through the interaction. Alice, Bob, and Carol may each have a cloud
agent, a laptop, and a phone; if they engage in an introduction protocol using
phones, then the agents on their phones are the participants. If the phones
talk directly over Bluetooth, this is particularly clear--but even if the phones
leverage push notifications and HTTP such that cloud agents help with routing,
only the phone agents are participants, because only they maintain state for
the interaction underway. (The cloud agents would be __facilitators__, and
the laptops would be __bystanders__). When a
protocol is complete, the participant agents know about the outcome; they may
need to synchronize or replicate their state before other agents of the
parties are aware.
