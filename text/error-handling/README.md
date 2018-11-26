- Name: Stephen Curran, Daniel Hardman
- Author: swcurran@cloudcompass.ca
- Start Date: 2018-11-26
- PR: 
- Jira Issue: 

# Summary
[summary]: #summaryn

Effective error reporting is difficult in any system, and particularly so in distributed systems such as remotely collaborating Agents. The challenge of getting an error notification to the person that needs to know about it (and perhaps separately, the person that can actually fix the problem) with the context they need to efficiently understand the issue and what to do about it is really hard, especially if the error is detected well after and well away from the cause of the problem. The goal of this HIPE is to provide Agents with the best tools and techniques possible in addressing the error handling problem.

This HIPE provides two key contributions towards meeting this challenge:

- A message family and type "problem-report" that allows an Agent to report a problem with as much context as possible.
- A range of problem categories and best practices for handling each category of problem.

# Motivation
[motivation]: #motivation

This HIPE attempts to address the following kinds of challenges that surround error handling.  In this, the term “error” is used in a very generic sense - a deviation from the "happy path" of an interaction. This could include warnings problems where the severity is unknown and must be evaluated by a human. It could also mean a decision by a human to alter the basis for in flight messaging - e.g. move the messaging from one device to another.

- We need ways to report errors to agents in other domains with whom we interact. For example, a way for AliceCorp to tell Bob that it can’t issue the credential he requested because his payment didn’t go through.
- We need ways to report error within our own domain. For example, a way for AliceCorp’s agent to report to AliceCorp that it is out of disk space.
- Bad error reporting is one of the most common causes of UX debacles - reporting an error in a way that provides the user with no guidance on how to address the problem - or even the location of the problem. Further, error reporting can be technically correct and completely useless.
- Since message delivery is transport-agnostic and thus may take place asynchronously, on an inconsistently connected digital landscape, errors may occur at times and under circumstances that are difficult to map back to a first cause or even a useful context.
- There is no way to maintain an exhaustive list of all possible things that can go wrong with all possible agents in all possible interactions. However, it may be possible to maintain a list of common errors that everyone understands.
  - Analogy: the number of things that can go wrong in a financial transaction is huge, and not all of them are enumerable or known to financial actors. But pretty much everybody understands “insufficient funds” as a problem with known semantics.
- Errors need to be at least partially handle-able by agents instead of humans. However, perfect processing without human intervention is probably an impossible-to-fully-achieve ideal.
- Humans using agents will speak different languages, have differing degrees of technical competence, and have different software and hardware resources.
- Humans may lack context about what their agents are doing, such as when an agent messaging occurs as a result of scheduled or policy-driven actions.

# Tutorial
[tutorial]: #tutorial

## The problem-report Message Type

A new Agent Message family (`notification`) and type `problem-report` is introduced. `problem-report` is intended to be used to report a class of error when an Agent to Agent message is possible and a recipient for the problem report is known. This covers, for example, errors where the Sender's message gets to the intended Recipient, but the Recipient is unable to process the message for some reason and wants to notify the Sender. Conversely, this leaves out, for example, a notification to the Sender of a message when the routing of the message fails (perhaps an "out-of-space" problem) and the agent having the problem doesn't know who is the Sender.

### The specification:

``` json
{
  "@type"            : "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/notification/1.0/problem-report",
  "@thread"          : "new thread with ptid set to thread ID or message ID of triggering message (if any)"
  "code"             : "<human-readable-string>",
  "catalog"          : "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/error-codes/123",
  "friendly-text-en" : "error instance specific detail",
  "problem-items"    : [ "<item>", "value" ],
  "who-retries"      : "enum: you | me | both | none",
  "fix-hint-en"      : "error instance specific hint of how to fix issue",
  "impact"           : "enum: message | thread | connection",
  "where"            : "enum: you | me | other - enum: cloud | edge | wire | agency | ..",
  "time-noticed"     : "<time>",
  "tracking-uri"     : "",
  "escalation-uri"   : ""
}
```

### Fields

In the following, the required fields are noted.

**@thread**: The thread decorator for the problem-report. The message will be the start of a new thread about the problem. Thus, if the error was triggered in the processing of a message, the thread's ptid (parent thread Id) should be the Message ID or Thread ID (as appropriate) of the message. If the problem-report is unrelated to a message, the thread decorator could be simply a message ID (`mid`).

**code** (required): A human-readable string constant, such as “out-of-memory”, that can be used by code to automatically react. This does not vary by language and is associated with the catalog entry so that it can be googled.

**catalog** (required): a DID reference that provides a way to look up the error code in a catalog. The DID resolves to an endpoint that is combined with the DID fragment (e.g. `;spec/error-codes/123` in the above) to define a concrete URL with the error details. This is the same technique used for message family specifications.

**friendly-text-??**: A message in a human language, describing this instance of the problem. The `??` is replaced as appropriate with an ISO639 language code (e.g. `en`). One problem-report may contain the same message meaning in multiple languages, if desired. No friendly text is required, but when a code is defined in a catalog, at least one friendly text should be provided to clarify its meaning publicly.

**problem-items**: A list of one or more key/value pairs that are parameters about the problem. Some examples might be:

- a list of arguments that didn’t pass input validation
- the name of a file or URL that could not be fetched
- the name of a crypto algorithm that the receiving agent didn’t support

All items should have in common the fact that they exemplify the problem described by the code (e.g., each is an invalid param, or each is an unresponsive URL, or each is an unrecognized crypto algorithm, etc).

Each item in the list must be a tagged pair (a JSON {key:value}, where the key names the parameter or item, and the value is the actual problem text/number/value. For example, to report that two different endpoints listed in party B’s DID Doc failed to respond when they were contacted, the code might contain “endpoint-not-responding”, and the problem-items property might contain: [{“endpoint1”: “http://agency.com/main/endpoint”}, {“endpoint2”: “http://failover.agency.com/main/endpoint”}]

**who-retries**: value is the string “you”, the string “me”, the string “both”, or the string “none”. This property tells whether a problem is considered permanent and who the sender of the problem report believes should have the responsibility to resolve it by retrying. Rules about how many times to retry, and who does the retry, and under what circumstances, are not enforceable and not expressed in the message text. This property is thus not a strong commitment to retry--only a recommendation of who should retry, with the assumption that retries will often occur if they make sense.

**fix-hint-??**: Language-specific suggestions about how to fix this instance of the problem. This would override comparable information found in the catalog.

**impact**: A string describing the breadth of impact of the problem. An enumerated type: 

- “msg” (this is a problem with a single message only; the rest of the interaction may still be fine),
- “thread” (this is a problem that endangers or invalidates the entire thread),
- “connection” (this is a problem that endangers or invalidates the entire connection).

**where**: A string that describes where the error happened and that uses the “you” or “me” or “other” prefix, followed by a suffix like “cloud”, “edge”, “wire”, “agency”, etc.

**time-noticed**: Standard time entry (ISO-8602 UTC) of when the problem was detected.

**tracking-uri**: Provides a URI that allows the recipient to track the status of the error. For example, if the error is related to a service that is down, the URI could be used to monitor the status of the service, so it's return to operational status could be automatically discovered.

**escalation_uri**: Provides a URI where additional help on the issue can be received. For example, this might be a "mailto" and email address for the Help Desk associated with a currently down service.

## Categorized Examples of Errors and (current) Best Practice Handling

The following is a categorization of a number of examples of errors and (current) Best Practice handling for those types of errors. The new `problem-report` message type is used for some of these categorizes, but not all.

### Error Processing a Received Message

An Agent Message sent by a Sender and received by its intended Recipient cannot be processed.

#### Examples:

- An error occurs in the processing of the message (e.g. missing required parameters, bad data in parameters, etc.)
- The recipient has no message handler for the message type
- A message request is rejected because of a policy
- Access denied scenarios

#### Recommended Handling

The Recipient should send the Sender a `problem-report` Agent Message detailing the issue.

The last example deserves an additional comment about whether there should be a response sent at all. Particularly in cases where trust in the message sender is low (e.g. when establishing the connection), an Agent may not want to send any response to a rejected message as even a negative response could convey reveal correlatable information. That said, if a response is needed, the `problem-report` message type should be used.

### Error Routing A Message

An Agent in the routing flow of getting a message from a Sender to the Agent Message Recipient cannot route the message.

#### Examples:

- Unknown "To" destination for the message
- Insufficient resources (disk space, network access)
- Unable to decrypt the message

#### Recommended Handling

If the Sender is known to the Agent having the problem, send a `problem-report` Agent Message detailing at least that a blocking issue occurred, and if relevant (such as in the first example), some details about the issue. If the message is valid, and the problem is related to a lack of resources (e.g. the second issue), also send a `problem-report` message to an escalation point within the domain.

Alternatively, the capabilities described in the "Tracing" HIPE (link to be added) could be used to inform others of the fact that an issue occurred.

### Messages Triggered about a Transaction

#### Examples:

- “You’re asking for more information than we agreed to” or “You’re giving me more than I expected.”
- Couldn’t pay (insufficient funds, payment mechanism is offline…)
- You violated the terms of service we agreed to, because I see that my info has been leaked.
- Your credential has been revoked (asynchronous)
- A is unwilling to consent to the terms and conditions that B proposes.

#### Recommended Handling

These types of error scenarios represent a gray error in handling between using the generic `problem-report` message format, or a message type that is part of the current transaction's message family. For example, the "Your credential has been revoked" might well be included as a part of the (TBD) standard Credentials Exchange message family. The "more information" example might be a generic error across a number of message families and so should trigger a `problem-report`) or, might be specific to the ongoing thread (e.g. Credential Exchange) and so be better handled by a defined message within that thread and that message family.

The current advice on which to use in a given scenario is to consider how the recipient will handle the message. If the handler will need to process the response in a specific way for the transaction, then a message family-specific message type should be used. If the error is cross-cutting such that a common handler can be used across transaction contexts, then a generic `problem-report` should be used.

"Current advice" implies that as we gain more experience with Agent To Agent messaging, the recommendations could get more precise.

### Messaging Channel Settings

#### Examples

- “Please resend so a different one of my agents can read this.”, or, “Agent no longer in service. Use X instead."
- A received a message from B that it cannot understand (message garbled, can’t be decrypted, is of an unrecognized type, uses crypto from a library that A doesn’t have, etc)
- A wants to report to B that it believes A has been hacked, or that it is under attack
- A wants to report to B that it believes B has been hacked, or that it is under attack
- Version incompatibilities of various kinds (transport version incompatibilities [http 1.1 vs. 2.0]; agent message type version incompatibilities)

#### Recommended Handling

These types of messages might or might not be triggered during the receipt and processing of a message, but either way, they are unrelated to the message and are really about the communication channel between the entities. In such cases, the recommended approach is to use a (TBD) standard message family to notify and rectify the issue (e.g. change the attributes of a connection). The definition of that message family is outside the scope of this HIPE.

### Timeouts

A special generic class of errors that deserves mention is the timeout, where a Sender sends out a message and does not receive back a response in a given time. In a distributed environment such as Agent to Agent messaging, these are particularly likely - and particularly difficult to handle gracefully. The potential reasons for timeouts are numerous:

- loss of connectivity
- resource errors with one of the Agents between the Sender and Receiver
- not yet detected key rotations (cached DIDDocs and encryption keys)
- errors occurring in an Agent unaware of the Sender (so cannot notify the sender of the issue)
- Recipient offline for an extended period
- disinterest on the part of the Recipient (received, but no response sent back)

#### Recommended Handling

Appropriate timeout handling is extremely contextual, with two key parameters driving the handling - the length of the waiting period before triggering the timeout and the response to a triggered timeout.

The time to wait for a response should be dynamic by at least type of message, and ideally learned through experience. Messages requiring human interaction should have an inherently longer timeout period than a message expected to be handled automatically. Beyond that, it would be good for Agents to track response times by message type (and perhaps other parameters) and adjust timeouts to match observed patterns.

When a timeout is received there are three possible responses, handled automatically or based on feedback from the user:

- Wait longer
- Retry
- Give up

An automated "wait longer" response might be used when first interacting with a particular message type or identity, as the response cadence is learned.

If the decision is to retry, it would be good to have support in areas covered by other HIPEs. First, it would be helpful (and perhaps necessary) for the threading decorator to support the concept of retries, so that a Recipient would know when a message is a retry of a previous message that has already been processed.  Next, on "forward" message types, Agents might want to know that a message was a retry such that they can consider refreshing DIDDoc/encryption key cache before sending the message along. It could also be helpful for a retry to interact with the Tracing facility so that more information could be gathered about why messages are not getting to their destination.

# Reference
[reference]: #reference

TBD

# Drawbacks
[drawbacks]: #drawbacks

In many cases, a specific `problem-report` message is necessary, so formalizing the format of the message is also preferred over leaving it to individual implementations. There is no drawback to specifying that format now.

As experience is gained with handling distributed errors, this HIPE will have to evolve.

# Rationale and alternatives
[alternatives]: #alternatives

The error type specification mechanism builds on the same approach used by the message type specifications. It's possible that additional capabilities could be gained by making runtime use of the error type specification - e.g. for the broader internationalization of the error messages.

The main alternative to a formally defined error type format is leaving it to individual implementations to handle error notifications, which will not lead to an effective solution.

# Prior art
[prior-art]: #prior-art

To be further investigated and documented.

# Unresolved questions
[unresolved]: #unresolved-questions

- Can the Tracing facility provide a trusted way to better handle distributed errors in a production environment?