# Google XML Style Guide — Review Checklist

Source: [Google XML Document Format Style Guide](https://google.github.io/styleguide/xmlguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Load when the diff designs or changes an XML document format or schema, not for incidental XML config.

Contents: [Scope and offline use](#scope-and-offline-use) · [To flag](#to-flag) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google XML format-design policy version 1.0 snapshot. Check the adopted schema, namespace versioning, and consuming parsers; this is not a requirement to redesign incidental XML configuration.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## To flag
- Element, attribute, and enumerated-value names not `lowerCamelCase`, or longer than about 25 characters.
- A new format where an existing standard format could be reused or extended.
- Attributes used for repeating data, substructure, ordered data, or natural-language text — those belong in elements.
- Booleans where an enumeration would leave room to grow.
- Dates not RFC 3339 (UTC preferred); binary data not Base64.
- Elements outside a namespace; namespaced attributes without a foreign-type reason.
- A namespace changed without a drastic semantic change — every client must update. **(bug risk: compatibility)**
- Data carried in comments.
- A schema language other than RELAX NG compact syntax, where the project has a choice.

**Application and exceptions:** Use meaningful lowerCamelCase names; a name longer than the suggested limit can be clearer than an abbreviation. Put repeated/structured text in elements and simple metadata in attributes. Preserve consumer namespace/schema requirements.

## Example and review decision

```xml
<order xmlns="urn:example:orders:v1" orderId="o1">
  <item productId="p1">Gift wrap</item>
</order>
```

Document optional/repeated fields and allowed values in the bundled schema or contract. XML has no programming-language imports; schema imports/includes and whitespace follow the adopted format. A namespace change can break consumers even when it looks cosmetic.
