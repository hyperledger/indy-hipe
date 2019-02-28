- Name: Digital Signatures
- Author: Kyle Den Hartog (kyle.denhartog@evernym.com)
- Start Date: 2019-01-07
- PR: N/A
- Jira Issue: N/A

# Digital Signatures
[digital-signatures]: #digital-signatures

## Summary
[summary]: #summary

This HIPE is intended to highlight the ways that a non-repudiable signature could be added to a message field or message family.

## Motivation
[motivation]: #motivation

While today we support a standard way of authenticating messages in a repudiable way, we also see the need for non-repudiable digital signatures for use cases where high authenticity is necessary such as signing a bank loan. There's additional beneficial aspects around having the ability to prove provenance of a piece of data with a digital signature. These are all use cases which would benefit from a standardized format for non-repudiable digital signatures.

This HIPE will outline both a message family and a message decorator that can be used to provide non-repudiable digital signatures in A2A messages. It will also highlight a standard way to encode data such that it can be deterministically verified later.

## Terms
[terms]: #terms

***non-repudiability***: Non-repudiation refers to a situation where a statement's author cannot successfully dispute its authorship or the validity of the statment.

## Examples
[examples]: #examples

### Signature Message Family
[message-family]: #message-family
The signature message family contains a single message format currently. This message family is to be used when an entire message needs to be signed. It will be structured in this way:

```
{
    @type: "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/signature/1.0/ed25519Sha512_single"
    "signature": <digital signature function output>
    "sig_data": <base64URL(formatted timestamp||message_data)>
    "signers": <signing_verkey>
}
```

### Field Decorator
[field-decorator]: field-decorator
The `~sig` feild decorator may be used with any field of data. Its value should match the json object format of the Signature Message Family outlined below. 

```
@type: 
"example_field~sig": {
    @type: "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/signature/1.0/ed25519Sha512_single"
    "signature": <digital signature function output>
    "sig_data": <base64URL(formatted timestamp||message_data)>
    "signers": <signing_verkey>
}
```

## Tutorial
[tutorial]: #tutorial

### Signing Implementation

1. append timestamp as 8 bytes to the front of the message data
2. call indy_crypto_sign(wallet_handle, signer_vk, time_and_message_data)
3. base64URLencode the outputted data of step 2
4. serialize data into JSON format

### Verify Signature Implementation

## Reference
[reference]: #reference

When using the signature message family or message decorator we base64 encode the data and sign the bytes and then embed the encoded data into the sig_data. The reason for encoding this data is to prevent false negative signature verifications that could potentially occur when sending JSON data which has no easy way to canonicalize the structure. Rather, by including the exact data as Base64 data, the receiver can be certain that they data signed is the same as what was received. 

Once the verifier has verified the data, they can base64 decode the sig_data and use the perform computations on the JSON structure. It's also worth noting that the data is not included in both encoded and decoded format in order to prevent message bloat.

Another important consideration is the usage of a list for the `signers` field. Supporting a list rather than only a single string allows for multi-signature support.

### Timestamp format

In order to handle timestamping, it's proposed that we prepend a string representation of the ISO 8601 standard format onto the front of the message. More specifically, the format should follow `yyyymmddThhmmssZ` where,

- `yyyy` -> year
- `mm` -> month with a 0 in the first position if less than 10
- `dd` -> day with a 0 in the first position if less than 10
- `T` -> standard delimiter that MUST be included to indicate the characters to the right represent the time
- `hh` -> hour using 24-hour format where a 0 is in the first position if less than 10
- `mm` -> minutes using a 60-minute format where a 0 is in the first position if less than 10 and 00 is used if it's the beginning of the hour
- `ss` -> seconds 
- `Z` -> standard timezone indicator which indicates UTC timezone. The timezone must remain `UTC`, so Z should always be used.

For example, `20190107T143700Z` would be the time stamp of Janurary 7th, 2019 at 2:37:00 PM UTC time zone. 


### Signing

Before signing, messages are prepared in normal fashion. Before sending, signatures are added using field or message methods.

```python
signed_message = sign_message(msg, signers_list, scheme) 
```

the `sign_message()` method base64 encodes the json string of `msg`, then signs it and creates the signed message in Native Object form as detailed above. 

```python
msg["my_field@sig"] = sign_field(msg["my_field"], signers_list, scheme)
del msg["my_field"] #remove unsigned field
```

Field signing only affects a section of the message. The `sign_field()` method base64 encodes the json string of the value present in the first argument. It then signs it, and returns a Native Object representation of the signed field block as described above.

After signing, the message is sent the same as an unsigned message.

### Signature Processing

On receipt of a signed message, the signatures must be verified and unpacked before use. It is recommended that agent frameworks make this step as automatic as possible to minimize error.

When a signed message is received, the signature should be verified and the message unpacked. The signature verification information should be added to the message context, and the signature message should be replaced with the internal message for further processing. Message handlers can then check the message context for any required signature information.

Signed fields within the message should have the signature verified, and then the unpacked message should be placed back into the message as the field name without the `@sig` decorator suffix. 

### Signature Schemes
[sig-schemes]: #sig-schemes

This decorator should support a specific set of signatures while being extensible. The list of current supported schemes are outlined below.

| signature Scheme | Scheme Spec |
|:----------------:|:-----------:|
|Ed25519Sha512     |[spec](Ed25519Sha512.md)|

TODO provide template in this HIPE directory
To add a new signature scheme, follow the template which is provided to detail the new scheme as well as provide some test cases to produce and verify the signature scheme is working.

### Examples

TODO add example messages with this standard signature format

## Drawbacks
[drawbacks]: #drawbacks

Since digital signature in this HIPE are non-repudiable, it's worth noting the privacy implications of using this functionality. In the event that a signer has chosen to share a message using a non-repudiable signature, they forgo the ability to prevent the verifier from sharing this signature on to other parties. This has potentially negative implications with regards to consent and privacy. 

**Therefore, this functionality should only be used if non-repudiable digital signatures are absolutely necessary.**

## Rationale and alternatives
[alternatives]: #alternatives

JSON Web Signatures is an alternative to this specification. The reason we've chosen to diverge from this specification is do to the inability to support our need for message decorators. Additional concerns around non-support for BLS signatures and other multi-signature schemes caused us to want to diverge.

## Prior art
[prior-art]: #prior-art

[IETF RFC 7515 (JSON Web Signatures)](https://tools.ietf.org/html/draft-ietf-jose-json-web-signature-41)

## Unresolved questions
[unresolved]: #unresolved-questions

Does there need to be an signature suite agreement protocol similar to TLS cipher suites?
    - No, rather the receiver of the message can send an error response if they're unable to validate the signature.

How should multiple signatures be represented?
    - One solution is to do [<digital_sig1>, <digital_sig2>] for `signature` and do [<verkey1>, <verkey2>] for `signers`
