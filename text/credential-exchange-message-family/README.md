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

We need to define standard protocols for credential issuance and presentation.

# Tutorial
[tutorial]: #tutorial

Credential exchange consists of two processes connected by data. Therefore, we need 2 message families -- one for credential issuance and another one for credential presentation.

## Credential Issuance

The Credential Issuance Message Family consists of these messages:

* Credential Offer
* Credential Request
* Credential
* Credential Ack
* Credential Reject

#### Choreography Diagram:

![issuance](credential-issuance.png)

#### Credential Offer
This message is sent by Issuer to Prover to initiate credential issuance. Schema:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-issuance/1.0/credential-offer",
    "@id": "<uuid-offer>",
    "cred_def_id": "KTwaKJkvyjKKf55uc6U8ZB:3:CL:59:tag1",
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
* `cred_def_id` -- id cof credential definition for offered credential
* attachment `libindy-offer` -- data for libindy about credential offer
* attachment `credential-preview` -- preview of credential.

#### Credential Request
This message is sent in response to Credential Offer by Prover to give needed details for credential issuance. Schema:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-issuance/1.0/credential-request",
    "@id": "<uuid-request>",
    "cred_def_id": "2hoqvcwupRTUNkXn6ArYzs:3:CL:1766",
    "comment": "some comment",
    "~attach": [
        {
            "nickname": "libindy_cred_req",
            "mime-type": "application/json",
            "content": {
                "base64": "<bytes for base64>"
            }
        },
        {
            "nickname": "credential_preview",
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
* `comment` -- a field that provide some human readable information about this Credential Offer.
* attachment `libindy_cred_req` -- an attachment with data that is needed to Issuer to generate a credential.
* attachment `credential_preview` -- optional attachment with preview of credential that Prover wants to get.

#### Credential
This message contains the credential and sent in responce to Credential Request. Schema:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-issuance/1.0/credential",
    "@id": "<uuid-credential>",
    "rev_reg_def_id": "<rev_reg_def_id>",
    "cred_def_id": "2hoqvcwupRTUNkXn6ArYzs:3:CL:1766",
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
* attachment `libindy-cred` -- an actual credential to store, it is a json encoded in base64

#### Credential Reject
This message can be sent by any side of the conversation to finish credential issuance without any credential created. Schema:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-issuance/1.0/reject",
    "@id": "id"
}
```

#### Credential Ack
This message is sent by Prover as he confirms that he had received the credential and everything is correct. Schema:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-issuance/1.0/ack",
    "@id": "id"
}
```

## Credential Presentation

The Credential Presentation Message Family consists of 4 messages:

* Presentation Request
* Presentation
* Presentation Ack
* Presentation Reject

#### Choreography Diagram:

![presentation](credential-presentation.png)

#### Presentation Request
Presentation Request is a message from Verifier to Prover that describes values that need to be revealed and predicates that need to be fulfilled. Schema:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-exchange/1.0/presentation-request",
    "@id": "<uuid-request>",
    "comment": "some comment",
    "~attach": [
        {
            "nickname": "libindy-presentation-request",
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
    "comment": "some comment",
    "~attach": [
        {
            "nickname": "libindy-presentation",
            "mime-type": "application/json",
            "content": {
                "base64": "<bytes for base64>"
            }
        },
        {
            "nickname": "presentation-request-preview",
            "mime-type": "application/json",
            "content": {
                "base64": "<bytes for base64>"
            }
        }
    ]
}
```

Decription of fields:

* `comment` -- a field that provide some human readable information about this Credential Offer.
* attachment `libindy-presentation` -- actual presentation for presentation request, represented by base64-encoded json.
* attachment `presentation-request-preview` -- preview of presentation request that prover is willing to fullfil. Used for negotiation purposes.

#### Presentation Reject
This message can be sent by any side of the conversation to finish credential issuance without any proof provided. Schema:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-presentation/1.0/reject",
    "@id": "id"
}
```

#### Presentation Ack
This message is sent by Verifier as he confirms that he had received the proof and validated it. Schema:
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-presentation/1.0/ack",
    "@id": "id"
}
```

### Threading

All of the messages require threading to be connected into a chain of messages. Using it we can mark what message we are responding to. This is a short set of rules that must be followed to use threading correctly:
* If you send a message in response to a non-threaded message, you must add a decorator `~thread` with a field `thid` with value of `@id` field of that message.
* If you send a message in response to an already threaded message, you must add a decorator `~thread` with `pthid` field with value of original `thid` and `thid` with n `@id` of message you respond to.

More details about threading you can find in the [threading and message id HIPE](https://github.com/hyperledger/indy-hipe/blob/master/text/0027-message-id-and-threading/README.md)

### Previews and negotiation

All of the messages (except Credential and Ack/Reject) can be negotiated. For these purposes you should use these fields: `credential_preview` in Credential Offer and Credential Request, `libindy_presentation_request` for Presentation Request and `presentation_request_preview` for Presentation.

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
- We might need to have an extra message to inform Prover about revocation of his credential.
- It is a common practise when the change of some attributes in credential we revoke the old credential and issue a new one. It might be useful to have in Credential Offer message to have at least some connection between revocation and new offer.
