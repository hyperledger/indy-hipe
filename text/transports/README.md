# Agent Transports
- Name: agent-transports
- Author: Sam Curren <sam@sovrin.org>
- Start Date: 2019-02-26
- PR: (leave this empty)
- Jira Issue: (leave this empty)

## Summary
[summary]: #summary

This HIPE Details how different transports are to be used for Agent Messaging.

## Motivation
[motivation]: #motivation

Agent Messaging is designed to be transport independent, including message encryption and agent message format. Each transport does have unique features, and we need to standardize how the transport features are (or are not) applied. 

## Reference

[Reference]: #reference

Standardized transport methods are detailed here. HTTP(S) is considered the main transport.

### HTTP(S)

HTTP(S) is considered the main transport for Agent Messaging.

- Messages are transported via HTTP POST.

- The MIME Type for the POST request is `application/ssi-agent-wire`.

- A received message should be responded to with a 202 Accepted status code. This indicates that the request was received, but not necessarily processed. Accepting a 200 OK status code is allowed.

- POST requests are considered transmit only by default. No agent messages will be returned in the response. This behavior may be modified with additional signaling.

- Using HTTPS with TLS 1.2 or greater with a forward secret cipher will provide Perfect Forward Secrecy (PFS) on the transmission leg.


### Websocket

Websockets are an efficient way to transmit multiple messages without the overhead of individual requests. 

- Each message is transmitted individually in Wire Level Format.

- The trust of each message comes from the Wire Level Format and encryption, not the socket connection itself.

- Websockets are considered transmit only by default. Messages will only flow from the agent that opened the socket. This behavior may be modified with additional signaling.

- Using Secure Websockets (wss://) with TLS 1.2 or greater with a forward secret cipher will provide Perfect Forward Secrecy (PFS) on the transmission leg.


### Other Transports

Other transports may be used for Agent messaging. As they are developed, this HIPE should be updated with appropriate standards for the transport method.

## Drawbacks
[drawbacks]: #drawbacks

Setting transport standards may prevent some uses of each transport method.

## Rationale and alternatives
[alternatives]: #alternatives

- Without standards for each transport, the assumptions of each agent may not align and prevent communication before each message can be unpacked and evaluated.

## Prior art
[prior-art]: #prior-art

Several agent implementations already exist that follow similar conventions.

## Unresolved questions
[unresolved]: #unresolved-questions

- Does it make sense that bi-directional transports (websockets) are one way by default?
