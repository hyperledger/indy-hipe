- Name: message-type-spec-guidelines
- Author: Sam Curren (telegramsam@gmail.com)
- Start Date: 2018-08-10
- PR: 
- Jira Issue: 

# Summary
[summary]: #summary

We anticipate the creation of many message family types. This collection of guidelines and best practices is intended to guide those designing new message types.

# Related Specs
[related]: #related

**Type Strings**

Example type string: `did:sov:1234567890;spec/messagefamily/1.0/messagetype`

Type strings are included with the `@type` attribute name.

**Reserved message attributes**

Attributes that start with an @ are considered reserved. 

# Guidelines
[guidelines]: #guidelines

#### Avoid ambiguous attribute names

Data, id, and package, are often terrible names. Adjust the name to enhance meaning. For example, use  `message_id` instead of `id`.

#### Avoid names with special characters

Technically, attribute names can be any valid json key (except prefixed with @, as mentioned above). Practically, you should avoid using special characters, including those that need to be escaped. Underscores and dashes [_,-] are totally acceptable, but you should avoid quotation marks, punctuation, and other symbols. Avoiding special characters in family and attribute names will ease the development process in various programming languages.

#### Use attributes consistently across message families

Be consistent with attribute names between the different types within a message family. Only use the same attribute name for the same data. If the attribute values are similar, but not exactly the same, adjust the name to indicate the difference.

#### Nest Attributes only when useful

Attributes do not need to be nested under a top level attribute, but can be to organize related attributes. Nesting all message attributes under one top level attribute is not usually a good idea.

# Examples

[examples]: #examples

**Example 1**

```json
{
    "@type": "did:example:00000;spec/pizzaplace/1.0/pizzaorder",
    "content": {
        "id": 15,
        "name": "combo",
        "prepaid?": true,
        "ingredients": ["pepperoni", "bell peppers", "anchovies"]
    }
}
```

Suggestions: Ambiguous names, unnecessary nesting, symbols in names.

**Example 1 Fixed**

```json
{
    "@type": "did:example:00000;spec/pizzaplace/1.0/pizzaorder",
    "table_id": 15,
    "pizza_name": "combo",
    "prepaid": true,
    "ingredients": ["pepperoni", "bell peppers", "anchovies"]
}
```



# Application Notes
[application]: #application

These guidelines are guidelines on purpose. There will be situations where a good design will have to choose between conflicting points, or ignore all of them. The goal should always be clear and good design.

# Unresolved questions
[unresolved]: #unresolved-questions

- We anticipate new additions to this document as the community gains experience.
