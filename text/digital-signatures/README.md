- Name: Digital Signatures
- Author: Kyle Den Hartog (kyle.denhartog@evernym.com)
- Start Date: 2019-01-07
- PR: N/A
- Jira Issue: N/A

# Summary
[summary]: #summary

This HIPE is intended to highlight the ways that a non-repudiable signature could be added to a message field or message family.

# Motivation
[motivation]: #motivation

While today we support a standard way of authenticating messages in a repudiable way, we also see the need for non-repudiable digital signatures for use cases where high authenticity is necessary such as signing a bank loan. There's additional beneficial aspects around having the ability to prove provenance of a piece of data with a digital signature. These are all use cases which would benefit from a standardized format for non-repudiable digital signatures.

This HIPE will outline both a message family and a message decorator that can be used to provide non-repudiable digital signatures in A2A messages. It will also highlight a standard way to encode data such that it can be deterministically verified later.

# Tutorial
[tutorial]: #tutorial

## Terms

***non-repudiability***: Non-repudiation refers to a situation where a statement's author cannot successfully dispute its authorship or the validity of the statment.

## Examples

### Signature Message Family
The signature message family contains a single message format currently. This message family is to be used when an entire message needs to be signed. It will be structured in this way:

```JSON
{
    @type: signature/1.0/ecdsa
    "scheme": <digital signature scheme used>
    "signature": <digital signature function output>
    "sig_data": <base64(message_data)>
    "signers": [list of signer's keys]
    "timestamp": <time following a standard>
}

```

### Message decorator
The `@sig` feild decorator may be used with any field of data. Its value should match the json object format of the Signature Message Family outlined below. 

```JSON
"example_feild.@sig": {
    @type: signature/1.0/ecdsa
    "scheme": <digital signature scheme used>
    "signature": <digital signature function output>
    "sig_data": <base64(message_data)>
    "signers": [list of signer's keys]
    "timestamp": <time following a standard>
}
```

# Reference
[reference]: #reference

When using the signature message family or message decorator we base64 encode the data and sign the bytes and then embed the encoded data into the sig_data. The reason for encoding this data is to prevent false negative signature verifications that could potentially occur when sending JSON data which has no easy way to canonicalize the structure. Rather, by including the exact data as Base64 data, the receiver can be certain that they data signed is the same as what was received. 

Once the verifier has verified the data, they can base64 decode the sig_data and use the perform computations on the JSON structure. It's also worth noting that the data is not included in both encoded and decoded format in order to prevent message bloat.

Another important consideration is the usage of a list for the `signers` feild. Supporting a list rather than only a single string allows for multi-signature support.


# Drawbacks
[drawbacks]: #drawbacks

Since digital signature in this HIPE are non-repudiable, it's worth noting the privacy implications of using this functionality. In the event that a signer has chosen to share a message using a non-repudiable signature, they forgo the ability to prevent the verifier from sharing this signature on to other parties. This has potentially negative implications with regards to consent and privacy. 

**Therefore, this functionality should only be used if non-repudiable digital signatures are absolutely necessary.**

# Rationale and alternatives
[alternatives]: #alternatives

JSON Web Signatures is an alternative to this specification. The reason we've chosen to diverge from this specification is do to the inability to support our need for message decorators. Additional concerns around non-support for BLS signatures and other multi-signature schemes caused us to want to diverge.

# Prior art
[prior-art]: #prior-art

[IETF RFC 7515 (JSON Web Signatures)](https://tools.ietf.org/html/draft-ietf-jose-json-web-signature-41)

# Unresolved questions
[unresolved]: #unresolved-questions

Does there need to be an signature suite agreement protocol similar to TLS cipher suites?

How should the key order be canonicalized if keys have to be verified in a specific order? For example RSA based ring signatures require a specific order for verification.

How should we incorporate the `@timing` decorator rather than using `timestamp`?

Should we be concatenating the `timestamp` data to the message_data as a part of the base64encoded data?