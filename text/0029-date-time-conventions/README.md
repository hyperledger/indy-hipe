[![moved to github.com/hyperledger/aries-rfcs repo](https://i.ibb.co/tBnfz6N/Screen-Shot-2019-05-21-at-2-07-33-PM.png)](https://github.com/hyperledger/aries-rfcs/blob/master/concepts/0074-didcomm-best-practices/README.md#date-time-conventions)

New location: [aries-rfcs/concepts/0074-didcomm-best-practices/README.md#date-time-conventions](https://github.com/hyperledger/aries-rfcs/blob/master/concepts/0074-didcomm-best-practices/README.md#date-time-conventions)

# 0029: Date and Time Conventions
- Authors: Daniel Hardman <daniel.hardman@gmail.com>
- Start Date: 2018-12-11

## Status
- Status: [SUPERSEDED](/README.md#hipe-lifecycle)
- Status Date: (date of first submission or last status change)
- Status Note: (explanation of current status; if adopted, 
  links to impls or derivative ideas; if superseded, link to replacement)

## Summary
Explain how agent messages talk about dates and times.

## Motivation
Date and time handling is an area where random variation
will produce lots of latent bugs due to undocumented assumptions.
Specifying some simple conventions early in the ecosystem's
evolution will avoid a lot of future debugging and documentation.

## Tutorial
This HIPE introduces conventions around date- and time-related fields in
messages. Any designer of messages is free to depart from these conventions
by choosing different semantics and different field name suffixes. However:

1. Developers should only do so if they have a good reason (e.g., a need to
measure the age of the universe in seconds in scientific notation, or a need
for ancient dates in a genealogy or archeology use case).

2. Developers should never *contradict* the conventions. That is, if a developer
sees a date- or time-related field that appears to match what's documented here,
the assumption of alignment ought to be safe. Divergence should use new
conventions, not redefine these.

Respecting these two rules should lead to healthy tribal knowledge and
reasonable alignment within Indy's developer community.

### The Need for Conventions

A quick [survey of source code across industries and geos](
 https://en.wikipedia.org/wiki/System_time) shows that
dates, times, and timestamps are handled with great inconsistency.
Some common storage types include:

* 32-bit (signed or unsigned) seconds since epoch (Jan 1, 1970 and Jan 1, 1980 are both used)
* 64-bit 100-nanosecond intervals since Jan 1, 1601
* Floating-point days and fractions of days since Dec 30, 1899
* Whole integer days since Jan 1, 1900
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
* &lt;something&gt;Millis or * &lt;something&gt;Ms or &lt;something&gt;Secs

The intent of this HIPE is NOT to eliminate all diversity. There are
good reasons why these different datatypes exist. However, we would like
agent-to-agent messages to use broadly understood naming conventions
that clearly communicate datatype and semantics, so that where there is
diversity, it's because of different use cases, not just chaos.

### Suffixes

Field suffixes communicate datatype and semantics for date- and time-related
ideas, as described below. Field names like "expires" or "lastmod" are
deprecated, because they don't say enough about what to expect from the values.
(Is "expires" a boolean? Or is it a date/time? If the latter, what is its
granularity and format?)

##### `_date`
Used for fields that have only date precision,
no time component. For example, `birth_date` or `expiration_date`.
Such fields should be represented as strings in ISO 8601 format
(_yyyy-mm-dd_). They should contain a timezone indicator if and only
if it's meaningful (see [Timezone Offset Notation](#timezone-offset-notation)).

##### `_time`
Used for fields that identify a moment with both date and
time precision. For example, `arrival_time` might communicate when a
train reaches the station. The datatype of such fields is a string
in ISO 8601 format (_yyyy-mm-ddTHH:MM:SS.xxx..._) using the Gregorian
calendar, and the timezone defaults to UTC. However:
* Precision can vary from minute to microsecond or greater.
* It is _strongly_ recommended to use the "Z" suffix to make UTC
  explicit: "2018-05-27 18:22Z"
* The capital 'T' that separates date from time in ISO 8601 can
freely vary with a space. (Many datetime formatters support this
variation, for greater readability.) 
* If local time is needed, [Timezone Offset Notation](#timezone-offset-notation) is used.

##### `_sched`
Holds a string that expresses appointment-style schedules
such as "the first Thursday of each month, at 7 pm". The format of
these strings is recommended to follow [ISO 8601's Repeating Intervals
notation](https://en.wikipedia.org/wiki/ISO_8601#Repeating_intervals) where possible. Otherwise, the
format of such strings may vary; the suffix doesn't stipulate a
single format, but just the semantic commonality of scheduling.


##### `_clock`
Describes wall time without reference to a date, as in `13:57`.
Uses ISO 8601 formatted strings and a 24-hour cycle, not AM/PM.

##### `_t`
Used just like `_time`, but for unsigned integer seconds since
Jan 1, 1970 (with no opinion about whether it's a 32-bit or 64-bit value).
Thus, a field that captures a last modified timestamp for a file, as
number of seconds since Jan 1, 1970 would be `lastmod_t`. This suffix
was chosen for resonance with Posix's `time_t` datatype, which has
similar semantics.

##### `_tt`
Used just like `_time` and `_t`, but for 100-nanosecond
intervals since Jan 1, 1601. This matches the semantics of the Windows
FILETIME datatype.

##### `_sec` or subunits of seconds (`_milli`, `_micro`, `_nano`)
Used for fields that tell how long something took. For example, a field
describing how long a system waited before retry might be named
`retry_milli`. Normally, this field would be represented as an unsigned
positive integer.

##### `_dur`
Tells duration (elapsed time) in friendly, calendar based
units as a string, using the conventions of [ISO 8601's Duration
concept](https://en.wikipedia.org/wiki/ISO_8601#Durations). `Y` = year,
`M` = month, `W` = week, `D` = day, `H` = hour, `M` = minute, `S` = second:
"P3Y2M5D11H" = 3 years, 2 months, 5 days, 11 hours. 'M' can be preceded
by 'T' to resolve ambiguity between months and minutes: "PT1M3S" = 1 minute,
3 seconds, whereas "P1M3S" = 1 month, 3 seconds.

##### `_when`
For vague or imprecise dates and date ranges. Fragments of
ISO 8601 are preferred, as in "1939-12" for "December 1939". The token
"to" is reserved for inclusive ranges, and the token "circa" is reserved
to make fuzziness explicit, with "CE" and "BCE" also reserved. Thus,
Cleopatra's `birth_when` might be "circa 30 BCE", and the timing of
the Industrial Revolution might have a `happened_when` of "circa 1760
to 1840".

  
### Timezone Offset Notation

Most timestamping can and should be done in UTC, and should use the "Z" suffix
to make the Zero/Zulu/UTC timezone explicit.

However, sometimes the local time and the UTC time for an event are both of
interest. This is common with news events that are tied to a geo, as with the
time that an earthquake is felt at its epicenter. When this is the case,
rather than use two fields, it is recommended to use timezone
offset notation (the "+0800" in "2018-05-27T18:22+08:00"). Except for the "Z"
suffix of UTC, timezone *name* notation is deprecated, because timezones can
change their definitions according to the whim of local lawmakers, and because
resolving the names requires expensive dictionary lookup. Note that this
convention is exactly [how ISO 8601 handles the timezone issue](
https://en.wikipedia.org/wiki/ISO_8601#Time_offsets_from_UTC).

## Reference
- [Discussion of date and time datatypes on Wikipedia](https://en.wikipedia.org/wiki/System_time)
- [ISO 8601](https://de.wikipedia.org/wiki/ISO_8601)