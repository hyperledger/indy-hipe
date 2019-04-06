# Parties, Roles, and Participants
 
The __parties__ in a protocol are the identity owners involved. In a protocol
where Alice introduces Bob to Carol, the parties are Alice, Bob, and Carol.

The __roles__ in a protocol are the perspectives that parties take on an
interaction. In an auction protocol, there are only two roles--*auctioneer*
and *bidder*--even though there may be many parties.

The __participants__ in a protocol are the agents that actually move the steps of
the protocol thorugh the interaction. Alice, Bob, and Carol may each have a cloud
agent, a laptop, and a phone; if they engage in an introduction protocol using
phones, then the agents on their phones are the participants. If the phones
talk directly over bluetooth, this is particularly clear--but even if the phones
leverage push notifications and HTTP such that cloud agents help with routing,
only the phone agents are participants, because only they maintain state for
the interaction underway. (The cloud agents would be __facilitators__, and
the laptops would be __bystanders__). When a
protocol is complete, the participant agents know about the outcome; they may
need to synchronize or replicate their state before other agents of the
parties are aware.

