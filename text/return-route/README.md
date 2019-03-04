# Transports / Return Route
- Name: return-route
- Author: Sam Curren <sam@sovrin.org>
- Start Date: 2019-03-04

## Summary
[summary]: #summary

Agents can indicate that an inbound message transmission may also be used as a return route for messages. This allows for transports of increased efficiency as well as agents without an inbound route.

## Motivation
[motivation]: #motivation

Inbound HTTP and Websockets are used only for receiving messages by default. Return messages are sent using their own outbound connections. Including a decorator allows the receiving agent to know that using the inbound connection as a return route is acceptable. This allows two way communication with agents that may not have an inbound route available.

## Tutorial
[tutorial]: #tutorial

When you send a message through a connection, you can use the `~transport` decorator and specify `return_route`.

```json
{
    "~transport": {
        "return_route": "all"
    }
}
```

Outbound messages can return the `~transport` decorator as well, with a `queued-message-count` attribute. This is useful for HTTP transports which can only receive one return message at a time.

```json
{
    "~transport": {
        "queued_message_count": 7
    }
}
```

If transport decorators are desired but no message needs to be sent, a `noop` message can be sent.

```json
{
    "@type": "?/1.0/noop",
    "~transport": {
        "return_route": "thread",
        "return_route_thread": "1234567899876543"
    }
}
```



## Reference

[reference]: #reference

`return_route` has the following acceptable values:

- `none`: Default. No messages should be returned over this connection.
- `all`: Send all messages for this key over the connection.
- `thread`: Send all messages matching the key and thread specified in the `return_route_thread` attribute.

The `~transport` decorator should be processed after unpacking and prior to routing the message to a message handler.

For HTTP transports, the presence of this message decorator indicates that the receiving agent MAY hold onto the connection and use it to return messages as designated. HTTP transports will only be able to receive at most one message at a time. Receiving subsequent messages can be accomplished by sending any other message with the same decorator. If you have no message to send, you may use the `noop` message type.

Websocket transports are capable of receiving multiple messages. 

Compliance with this indicator is optional.

## Drawbacks
[drawbacks]: #drawbacks

Why should we *not* do this?

## Rationale and alternatives
[alternatives]: #alternatives

- Using a transport level decorator makes this behavior transport agnostic.

## Prior art
[prior-art]: #prior-art

Decorators HIPE: https://github.com/hyperledger/indy-hipe/blob/57b8efb7ffe8ea206d4b67558f61025cd2d946f0/text/decorators/README.md

Describes scope of decorators. Transport isn't one of the scopes listed.

## Unresolved questions
[unresolved]: #unresolved-questions

- Is `transport` the right name?
- What family should `noop` be in?
