- Name: message-timing
- Authors: Daniel Hardman <daniel.hardman@gmail.com>
- Start Date: 2018-12-11
- PR:

# HIPE 00??: Message Timing
[summary]: #summary

Explain how timing of agent messages can be communicated and constrained.

# Motivation
[motivation]: #motivation

Many timing considerations influence asynchronous messaging delivery.
We need a standard way to talk about them.

# Tutorial
[tutorial]: #tutorial

This HIPE introduces a decorator to communicate about timing of messages.
It is compatible with, but independent from, [conventions around date and
time fields in messages]( https://github.com/hyperledger/indy-hipe/pull/76).

Timing attributes of messages can be described with the `@timing`
decorator. It offers a number of optional subfields:

```JSON
"@timing": {
  "in_time":  "2019-01-25 18:03:27.123Z",
  "out_time": "2019-01-25 18:03:27.123Z",
  "stale_time": "2019-01-24 18:25Z",
  "expires_time": "2019-01-25 18:25Z",
  "delay_milli": 12345
}
```

The meaning of these fields is:

* `in_time`: The timestamp when the preceding message in this thread
  (the one that elicited this message as a response) was received.
* `out_time`: The timestamp when the message was emitted. At least millisecond
  precision is preferred, though second precision is acceptable.
* `stale_time`: Ideally, the decorated message should be processed by the
  the specified timestamp. After that, the message may become irrelevant
  or less meaningful than intended. This is a hint only.
* `expires_time`: The decorated message should be considered invalid or
  expired if encountered after the specified timestamp. This is a much
  stronger claim than the one for `stale_time`; it says that the receiver
  should cancel attempts to process it once the deadline is past, because
  the sender won't stand behind it any longer.
* `delay_milli`: Wait at least this many milliseconds before processing
  the message. This may be useful to defeat temporal correlation.

All information in these fields should be considered best-effort. That
is, the sender makes a best effort to communicate accurately, and the
receiver makes a best effort to use the information intelligently. In
this respect, these values are like timestamps in email headers--they
are generally useful, but not expected to be perfect. Receivers are not
required to honor them exactly.

### Timing in Routing

Most usage of the `@timing` decorator is likely to focus on application-oriented
messages processed at the edge. `in_time` and `out_time`, for example, are mainly
useful so Bob can know how long Alice took to ponder her response to his love letter.
In onion routing, where one edge agent prepares all layers of the `forward` wrapping,
it makes no sense to apply them to `forward` messages. However, if a relay is
composing new `forward` messages dynamically, these fields could be used to measure
the delay imposed by that relay. `stale_time`, `expires_time`, and `delay_milli`
all have meaning in routing.

### Timing and Threads

When a message is a reply, then `in_time` on an application-focused message is
useful. However, `out_time` is relevant regardless of whether threading is active.

# Reference

[reference]: #reference
- [Discussion of date and time datatypes on Wikipedia](https://en.wikipedia.org/wiki/System_time)
- [ISO 8601](https://de.wikipedia.org/wiki/ISO_8601)