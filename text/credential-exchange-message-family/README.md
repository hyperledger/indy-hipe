- Name: credential-exchange-message-family
- Author: Nikita Khateev
- Start Date: 2019-01-30
- PR: (leave this empty)
- Jira Issue: (leave this empty)

# Summary
[summary]: #summary

Formalization and generalization of existing message formats used for credential
exchange according to existing HIPEs about message formats.

# Motivation
[motivation]: #motivation

Standartize the message family used for credential exchange for future developers' use

# Tutorial
[tutorial]: #tutorial

The Credential Exchange Message Family consists of 5 messages:
* Credential Offer
* Credential Request
* Credential
* Presentation Request
* Presentation

#### Credential Offer
This message is sent by Issuer to Prover to initiate credential issuance. Schema:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-exchange/1.0/credential-offer",
    "@id": "<uuid-offer>",
    "cred_id": "<id>",
    "cred_name": "name",
    "cred_def_id": "KTwaKJkvyjKKf55uc6U8ZB:3:CL:59:tag1",
    "to_did": "Mie7euMJ94nrTHbx5HZEu7",
    "from_did": "Mie7euMJ94nrTHbx5HZEu7",
    "comment": "some comment",
    "~attach": [
        {
            "nickname": "libindy-offer",
            "mime-type": "application/json",
            "content": {
                "base64": "<bytes for base64>"
            }
        },
        {
            "nickname": "credential-preview",
            "mime-type": "application/json",
            "content": {
                "base64": "<bytes for base64>"
            }
        }
    ]
}
```

Description of fields:
* `comment` -- a field that provide some human readable information about this Credential Offer.
* `cred_id` -- id of credential.
* `cred_name` -- name of credential
* `cred_def_id` -- id cof credential definition for offered credential
* `to_did` -- DID of Prover
* `from_did` -- DID of Issuer
* attachment `libindy-offer` -- data for libindy about credential offer
* attachment `credential-preview` -- preview of credential.

#### Credential Request
This message is sent in response to Credential Offer by Prover to give needed details for credential issuance. Schema:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-exchange/1.0/credential-request",
    "@id": "<uuid-request>",
    "cred_def_id": "2hoqvcwupRTUNkXn6ArYzs:3:CL:1766",
    "comment": "some comment",
    "to_did": "<did>",
    "from_did": "<did>",
    "~attach": [
        {
            "nickname": "libindy_cred_req",
            "mime-type": "application/json",
            "content": {
                "base64": "<bytes for base64>"
            }
        }
    ]
}
```

Description of Fields:
* `cred_def_id` -- Credential Definition ID for requested credential
* `to_did` -- DID of Issuer
* `from_did` -- DID of Prover
* `comment` -- a field that provide some human readable information about this Credential Offer.
* attachment `libindy_cred_req` -- an attachment with data that is needed to Issuer to generate a credential.

#### Credential
This message contains the credential and sent in responce to Credential Request. Schema:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-exchange/1.0/credential",
    "@id": "<uuid-credential>",
    "rev_reg_def_id": "<rev_reg_def_id>",
    "cred_def_id": "2hoqvcwupRTUNkXn6ArYzs:3:CL:1766",
    "from_did": "44oqvcwupRTUNkXn6ArYzs",
    "~attach": [
        {
            "nickname": "libindy-cred",
            "mime-type": "application/json",
            "content": {
                "base64": "<bytes for base64>"  
            }
        }
    ]
}
```

Description of fields:

* `rev_reg_def_id` -- an ID of Revocation Registry Definition for this credential
* `cred_def_id` -- ID of Credential Definition this credential were issued to
* `from_did` -- DID of Issuer
* attachment `libindy-cred` -- an actual credential to store, it is a json encoded in base64

#### Presentation Request
Presentation Request is a message from Verifier to Prover that describes values that need to be revealed and predicates that need to be fulfilled. Schema:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-exchange/1.0/presentation-request",
    "@id": "<uuid-request>",
    "comment": "some comment",
    "~attach": [
        {
            "nickname": "libindy-proof-request",
            "mime-type": "application/json",
            "content":  {
                "base64": "<bytes for base64>"
            }
        }
    ]
}
```

Description of fields:

* `comment` -- a field that provide some human readable information about this Credential Offer.
* attachment `libindy-proof-request` -- base64-encoded data needed for libindy to process proof request.

#### Presentation
This message is a response to a Presentation Request message and contains signed presentations. Schema:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-exchange/1.0/presentation",
    "@id": "<uuid-presentation>",
    "to_did": "2hoqvcwupRTUNkXn6ArYzs",
    "from_did": "2hoqvcwupRTUNkXn6ArYzs",
    "comment": "some comment",
    "~attach": [
        {
            "nickname": "libindy-presentation",
            "mime-type": "application/json",
            "content": {
                "base64": "<bytes for base64>"
            }
        }
    ]
}
```

Decription of fields:

* `to_did` -- DID of Verifier
* `from_did` -- DID of Prover
* `comment` -- a field that provide some human readable information about this Credential Offer.
* attachment `libindy-presentation` -- actual presentation for presentation request, represented by base64-encoded json.

### Threading

All of the messages support threading. Using it we can mark what message we are responding to. This is a short set of rules that should be followed to use threading correctly:
* If you send a message in response to a non-threaded message, you should add a decorator `~thread` with a field `thid` with value of `@id` field of that message.
* If you send a message in response to an already threaded message, you should add a decorator `~thread` with `pthid` field with value of original `thid` and `thid` with n `@id` of message you respond to.
More details about threading you can find in the [threading and message id HIPE](https://github.com/hyperledger/indy-hipe/blob/master/text/0027-message-id-and-threading/README.md)

### Previews and negotiation

This section is still in development and might be changed.

In the previous sections pretty straightforward way of credential exchange has been described. It can be improved with preview of credential and counterrequest of presentation/credential. In general, request/counterrequest model is described [here](https://github.com/sovrin-foundation/ssi-protocol/tree/master/flow/std/negotiate_msg).
As a preview we can add an attachment to Credential offer message:

```
    ...
    "~attach": [
        ...
        {
            "nickname": "credential-preview",
            "mime-type": "application/json",
            "content": {
                "base64": "<bytes for base64>"
            }
        }
    ]
```

The credential in preview should not have any signatures over the separate fields so it could not be used by anybody else for presentations. 

Prover can now respond with Credential Request with the same attachment, which results into an issuance of credential, or he/she can respond with a modified credential in the attachment.

Then, Issuer issues the credential with Credential message (if Prover has agreed with the initial credential or Issuer agreed with the credential from counterrequest) or goes into another cycle of Offer/Request.

It is important to mention that this process can be started as from Credential Offer message, as from Credential Request.

The same process is applicable for presentation. Instead of the requested presentation Prover can offer its own presentation to Verifier in the attachment `libindy-presentation-offer`. Verifier can accept it, reject it or send another Presentation Request.

All reasoning for another step of negotiation can be given inside of the `comment` field.

# Reference
[reference]: #reference

* [VCX](https://github.com/hyperledger/indy-sdk/tree/master/vcx/libvcx/src/api) -- this implementation might not be perfect and needs to be improved, you can gather some info on parameters purpose from it

# Drawbacks
[drawbacks]: #drawbacks

Why should we *not* do this?

# Prior art
[prior-art]: #prior-art

Similar (but simplified) credential exchanged was already implemented in [von-anchor](https://von-anchor.readthedocs.io/en/latest/). 

# Unresolved questions
[unresolved]: #unresolved-questions

- We might need to propose a new MIME type for credential (the same way as .docx is not processed as generic xml). The issue in W3C/vc-data-model: https://github.com/w3c/vc-data-model/issues/421
