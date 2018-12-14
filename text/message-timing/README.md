- Name: message-timing
- Authors: Daniel Hardman <daniel.hardman@gmail.com>
- Start Date: 2018-12-11
- PR:

# HIPE 00??: Message Timing
[summary]: #summary

Explain how timing of agent messages can be communicated and constrained.

# Motivation
[motivation]: #motivation

Many timing considerations influance asynchronous messaging delivery.
We need a standard way to talk about them.

# Tutorial
[tutorial]: #tutorial

This HIPE introduces conventions around date and time fields in messages,
plus a decorator that communicates about timing. The conventions and the
decorator are compatible but somewhat independent. Even when the decorator
doesn't fit a particular use case, the conventions are strongly encouraged.

### Conventions

A quick [survey of source code across industries and geos](
 https://en.wikipedia.org/wiki/System_time) shows that
dates, times, and timestamps are handled with great inconsistency.
Some common storage types include:

* 32-bit (signed or unsigned) seconds since epoch (Jan 1, 1970 and Jan 1, 1980 are both used)
* 64-bit 100-nanosecond intervals since Jan 1, 1601
* Floating-point days and fractions of days since Dec 31, 1899
* Floating point scientific time (billions of years since big bang)
* clock ticks since OS booted
* milliseconds since OS booted

Of course, many of these datatypes have special rules about their
relationship to timezones, which further complicates matters. And timezone
handling is notoriously inconsistent, all on its own.

Some common names for the fields that store these times include:

* &lt;something&gt;Time
* &lt;something&gt;Date
* &lt;something&gt;Timestamp
* &lt;something&gt;Millis or * &lt;something&gt;Ms

The intent of this HIPE is NOT to eliminate all diversity. There are
good reasons why these different datatypes exist. However, we would like
agent-to-agent messages to use broadly understood naming conventions
that clearly communicate datatype and semantics, so that where there is
diversity, it's because of different use cases, not just chaos.

##### Recommendations

Field suffixes communicate datatype and semantics for date- and time-related
ideas, as described below. Field names like "expires" or "lastmod" are
deprecated, because they don't say enough about what to expect from the values.

Message families are free to invent their own where they have specialized
needs (e.g., in genealogy, storing dates earlier than 1601 may be
important and different enough to justify a set of date conventions for
that problem domain). However, no message families should create a
convention that conflicts with these:

* `_date`: Used for fields that have only date precision,
  no time component. For example, `birth_date` or `expiration_date`.
  Such fields should be represented as strings in ISO 8601 format
  (_yyyy-mm-dd_).
* `_time`: Used for fields that identify a moment with both date and
  time precision. For example, `arrival_time` might communicate when a
  train reaches the station. The datatype of such fields is a string
  in ISO 8601 format (_yyyy-mm-dd HH:MM:SS.xxx_) using the Gregorian
  calendar, and the timezone defaults to UTC. However:
    * Precision can vary from minute to millisecond.
    * It is _strongly_ recommended to use the "Z" suffix to make UTC
      explicit: "2018-05-27 18:22Z"
    * If local time is needed, timezone offset notation ("2018-05-27
      18:22 +0800" rather than timezone name is used. Timezone name
      notation is deprecated as timezones can change their definitions
      over time according to the whim of local lawmakers.
* `_sched`: Holds a string that expresses appointment-style schedules
  such as "the first Thursday of each month, at 7 pm". Note that the
  format of such strings may vary; the suffix doesn't stipulate a
  single format, but just the semantic commonality of scheduling.
* `_clock`: Describes wall time without reference to a date, as in `13:57`.
  Uses ISO 8601 formatted strings and a 24-hour cycle, not AM/PM.
* `_t`: Used just like `_time`, but for unsigned integer seconds since
  Jan 1, 1970 (with no opinion about whether it's a 32-bit or 64-bit value).
  Thus, a field that captures a last modified timestamp for a file, as
  number of seconds since Jan 1, 1970 would be `lastmod_t`.
* `_tt`: Used just like `_time` and `_t`, but for 100-nanosecond
  intervals since Jan 1, 1601. This is the Windows FILETIME datatype.
* `_sec` or subunits of seconds (`_milli`, `_micro`, `_nano`): Used for
  fields that tell how long something took. For example, a field
  describing how long a system waited before retry might be named
  `retry_milli`. Normally, this field would be represented as an unsigned
  positive integer.
* `_el` tells how much time has elapsed in friendly, calendar based
  units as a string (`y` = year, `q` = quarter, `m` = month, `w` = week,
  `d` = day, `h` = hour, `n` = minute, `s` = second), as in
  "3w 2d 11h". Note that this datatype does not convert directly to
  the pure time-based elapsed variant like `_sec`, because the duration
  of months, years, and quarters is variable. 

### Decorators

Timing attributes of messages can be described with the `@timing`
decorator. It offers a number of optional subfields:

```JSON
"@timing": {
  "out_time": "2019-01-25 18:03:27.123Z",
  "in_time":  "2019-01-25 18:03:27.123Z",
  "expires_time": "2019-01-25 18:25Z",
  "delay_milli": 12345
}
```

The meaning of these fields is:

* `out_time`: The timestamp when the message was emitted. Millisecond
  precision is preferred, though second precision is acceptable.
* `in_time`: The timestamp when the preceding message in this thread
  (the one that elicited this message as a response) was received.
* `expires_time`: The current message should be considered invalid or
  expired if processed after the specified timestamp.
* `delay_milli`: Wait at least this many milliseconds before processing
  the message. This may be useful inside `forward` messages, for example--
  or to defeat temporal correlation.

All information in these fields should be considered best-effort. That
is, the sender makes a best effort to communicate accurately, and the
receiver makes a best effort to use the information intelligently. In
this respect, these values are like timestamps in email headers--they
are generally useful, but not expected to be perfect. Receivers should
honor the `expires_time` and `delay_milli` where practical, but are not
required to do so.

# Reference

[reference]: #reference
- [Discussion of date and time datatypes on Wikipedia](https://en.wikipedia.org/wiki/System_time)
- [ISO 8601](https://de.wikipedia.org/wiki/ISO_8601)