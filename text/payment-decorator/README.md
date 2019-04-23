# Payment Decorator
- Name: payment-decorator
- Author: Sam Curren (<sam@sovrin.org>)
- Start Date: 2019-04-22

## Summary
[summary]: #summary

Message families can express the details of payment mechanisms with the `~payment_request` and `~payment_receipt` mechanisms. 

## Motivation
[motivation]: #motivation

Generalizing payment inside a decorator provides opportunities to develop rich payment flows without recreating payment primitives each time.

## Reference

[reference]: #reference

### `~payment_request`

```json=
{
  "~payment_request": [{
      "@id": "xyz", //functions like a purchase order number
      "method": "sovrin",
      "unit": "tokens",
      "amount": "0.2", //or int? look at token work
      "recipient": "<address>"
  }]
}
```
The `~payment_request` decorator is a list of payment structures. When multiple options are present, they represent multiple payment options for the same thing.

The decorator can be applied at any level of a message, allowing a single message to indicate payment methods for different things.

**method**:  which payment method is requested.

**unit**: Unit applied to the `amount` attribute. Unit will relate to the payment method.

**amount**: amount being requested.

**recipient**: payment address when payment is made.

#### Potential future attributes

- non-required payments (required =  false)
- multiple payments at once options (_and_ instead of _or_)
- expiration (date in request, date in receipt somehow, maybe use the timing decorator)

### `~payment_receipt`

This decorator on a message indicates that a payment has been made.

```json=
{
  "~payment_receipt": [{
      "related_requests": ["xyz"],
      "method": "sovrin",
      "amount": 0.2,
      "receipt": "",
      "recipient": "<address>",
      "extra": "?"
  }]
}
```

**related_requests**: This contains the `@id`s of `~payment_requests` that this payment receipt satisfies. 

**receipt**: String which identifies payment for verification.

**extra**: Contains extra information about the payment made.

#### Notes

- Proof of payment could be a stronger form of receipt.

## Tutorial

[tutorial]: #tutorial

These decorators can be incorporated into message families as appropriate. Here are some examples from Credential Exchange HIPE. Note that unrelated attributes have been removed from the examples.

#### Example Credential Offer

This message is sent by the issuer. The payment request includes payment requested for this offered credential.

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-issuance/1.0/credential-offer",
    "@id": "<uuid-offer>",
    "cred_def_id": "KTwaKJkvyjKKf55uc6U8ZB:3:CL:59:tag1",
    "~payment_request": [{
      "@id": "offer-34567654324565454", 
      "method": "sovrin",
      "unit": "tokens",
      "amount": "0.2",
      "recipient": "pay:sov:45678987654345678987"
  	}],
    "credential_preview": <json-ld object>,
    ///...
}
```

#### Example Credential Request

This Credential Request is sent to the issuer, indicating that they have paid the requested amount.

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-issuance/1.0/credential-request",
    "@id": "<uuid-request>",
    "cred_def_id": "KTwaKJkvyjKKf55uc6U8ZB:3:CL:59:tag1",
    "~payment_receipt": [{
        "related_requests": ["offer-34567654324565454"],
        "method": "sovrin",
        "amount": "0.2",
        "receipt": "",
        "recipient": "pay:sov:45678987654345678987",
        "extra": "something"
    }]
	///...
}
```



## Drawbacks

[drawbacks]: #drawbacks

A difficult aspect of this is managing all the way that different payments apply to this decorator. 

## Rationale and alternatives
[alternatives]: #alternatives

- We could allow each message family to indicate payment information independently. This would be very flexible, but tedious and very messy.
- We could not include payment information in messages, but that would limit useful applications.

## Prior art
[prior-art]: #prior-art

What applies here?

## Unresolved questions
[unresolved]: #unresolved-questions

- Should `method` be a json-ld `@type` to allow for different payment attributes?
- Is `payment_receipt` too easily confusing with consent receipt?
