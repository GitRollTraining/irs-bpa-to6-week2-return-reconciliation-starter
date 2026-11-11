# Customer input and handoff contract — change request V2

This is a fictional training format, not an IRS schema. These rules are supplied business policy,
not a request for learners to invent tax knowledge or configurable schemas. Customer examples are
inputs; learners must design their own complete test cases. This file fixes what goes in, what comes
out and what the coordinator must see. It does not say how the desk stores, compares or computes
anything: that is your design.

## 1. CSV work list

UTF-8 (optional BOM), comma-separated CSV with exactly the header `return_id,year`. Use normal CSV
quoting rules. There are 1–200 data records; no blank records or extra columns. Trim surrounding
field whitespace. IDs match `[A-Z0-9][A-Z0-9-]{0,39}`; year is exactly four ASCII digits in 2000–2099.
The pair is case-sensitive identity. Reject duplicate normalized pairs and identify all involved
record numbers (header is record 1; multiline quoted fields count as one CSV record). A parse failure
may identify the parser's physical line and label it as such. Batch names are trimmed, nonempty,
at most 100 Unicode code points; equal names may identify separate batches. A CSV is at most 256 KiB.
The batch that is created holds exactly the list the coordinator reviewed. A list that fails
validation creates no batch.

## 2. ZIP delivery envelope

A ZIP contains UTF-8 `delivery.json` at its root and 1–30 listed XML files. The manifest is:

```json
{"delivery_id":"TEAM-A-001","supplier":"A","files":[{"name":"case-a.xml","revision":1}]}
```

Delivery IDs match the same 1–40-character grammar as return IDs. `supplier` is `A` or `B` and
selects the XML format for every member. Each file entry has exactly `name` and `revision`; the
manifest has exactly the three fields shown. Revision is a JSON integer 1–999999 (not a boolean).
Names are unique, case-sensitive, flat ASCII names matching `[A-Za-z0-9][A-Za-z0-9._-]{0,99}\.xml`.
The archive contains exactly those members plus the manifest, each once: no directories, absolute
paths, parent traversal, backslashes, links, encryption, duplicate archive names or unlisted members.
Only stored or deflated members are supported. Archive bytes are at most 8 MiB; manifest is at most
64 KiB; each XML is at most 256 KiB; total expanded content is at most 8 MiB. A package over any
limit is refused, and no package, however it was built, may make the desk run out of memory or
disk before it is refused. File names are metadata, never filesystem paths.

Invalid envelopes are rejected without applying data. When the envelope can be inspected, process
all its listed XML files and show all available results. Any invalid XML or identity outside the
batch rejects the entire delivery: valid entries are displayed as not applied. Storage failure
likewise applies none. For every attempt, the coordinator and whoever reads the logs can tell which
package it was and what each file needs. Filer names, contact values and file contents stand for
personal data: they do not appear in logs or error text. A rejected attempt stays visible, separately
from accepted history, after the page is reloaded; it reserves no delivery ID, so a repaired package
may reuse it. No raw-content retention is required.

Delivery IDs are batch-scoped. Sending an accepted delivery again under its ID changes nothing and
returns the original receipt. It is the same delivery when it says the same things, however it was
packed: the same package zipped again, with its members in another order, another compression or
another namespace prefix, is a repeat. The same ID arriving with anything different in what it
says (a file renamed, a revision changed, the other supplier, a business value changed) is refused
with an explanation. Distinct accepted delivery IDs may repeat the same case revision; keep
both as sources without treating identical records as a business conflict. One package may also
carry the same case more than once, in different revisions or the same one; that is valid, and the
rules of section 5 decide the result.

## 3. Supplier A (the existing V1 format)

The following existing format remains the authority for field rules and normalized records.
The per-case revision comes from the ZIP manifest, not an XML change.

UTF-8 XML uses namespace `urn:training:return:v2`. A default namespace or any prefix bound to that
same URI has the same meaning. Root is Return, containing exactly one ReturnHeader followed by
exactly one ReturnData. ReturnHeader contains ReturnId, TaxYear, FilerName and optional Contact in
that order. ReturnData contains exactly one Form1040, whose zero to 100 Income elements occur in
source order. Each Income has exactly one Label followed by one Amount. Namespace declarations are permitted; no other attributes or unlisted
elements, duplicate singleton elements or non-whitespace mixed content are accepted. Ignore XML
indentation whitespace. XML declaration/BOM and predefined/numeric character references are valid;
reject DTD/entity declarations and external resolution. Comments and non-declaration processing
instructions are outside this training format. Use a maintained XML parser with explicit safe
settings or documented safe defaults; regex is not an XML parser.

```xml
<Return xmlns="urn:training:return:v2">
  <ReturnHeader>
    <ReturnId>DEMO-101</ReturnId><TaxYear>2025</TaxYear>
    <FilerName>Example A</FilerName><Contact></Contact>
  </ReturnHeader>
  <ReturnData><Form1040>
    <Income><Label>Employment</Label><Amount>1200.50</Amount></Income>
    <Income><Label>Interest</Label><Amount>2</Amount></Income>
  </Form1040></ReturnData>
</Return>
```

Trim surrounding field text. FilerName is 1–120 code points and Label 1–80; preserve internal
whitespace. Contact is absent => null; present => trimmed string of 0–120 code points, including
empty string; no email-format validation. Amount accepts trimmed ASCII text matching `[0-9]+(\.[0-9]{1,2})?`,
max 999999999.99; `12` and `12.0` are valid, `12.` is invalid; reject exponent notation, signs, commas, NaN and
infinity. Wherever the desk shows or hands over an amount, it is written with exactly two decimal
places (`12` is shown as `12.00`). No totals or tax calculations are required.
Duplicate income labels are allowed; preserve every entry and its order.

The original XML example in samples/xml/ illustrates this format. The rules
above define optional and repeated structure beyond that example; learners author their own
positive/negative test data and expected results.

Required normalized record: return_id (string), year (integer), filer_name (string), contact
(string or null), income (ordered list of {label, amount}). A malformed, unsafe, wrong-namespace,
wrong-shape or invalid-value file has record=null and a structured issue. Use codes MALFORMED_XML,
UNSUPPORTED_XML or INVALID_FIELD, a readable message and path or available line/column; do not
invent unavailable locations. At least one precise issue per invalid file is enough.

Document the header/data/Form1040 mapping, root-to-value namespace-qualified paths, and optional/
repeated findings against multiple concrete fixtures. Bind that mapping to actual reader code and
fixture assertions; a standalone essay is insufficient. The example is an authored miniature
transport contract, not an actual IRS schema or substitute for a separate trainer-led full-return
reading activity.


## 4. Supplier B

B uses namespace `urn:training:provider-b:v1` and the structure below. A default namespace or any
prefix bound to that URI is equivalent. Attribute names `id` and `year` are unqualified; no other
attributes are allowed. Child order and cardinality are exact: one Person then one Earnings;
Person contains exactly one Name and optionally one Email; Earnings contains zero to 100 Entry
nodes, each exactly one Description followed by one Cents.

```xml
<Submission xmlns="urn:training:provider-b:v1" id="DEMO-101" year="2025">
  <Person><Name>Example A</Name><Email></Email></Person>
  <Earnings><Entry><Description>Employment</Description><Cents>120050</Cents></Entry></Earnings>
</Submission>
```

Apply A's UTF-8, safe-parser, attributes/shape, text trimming/internal whitespace, comments/PI,
length and error-location rules. Map `id/year` to return_id/year, Name to filer_name, Email to
contact, and ordered Description/Cents pairs to income.label/amount. Missing Email is null;
present empty Email is an empty string. Cents is trimmed ASCII digits only, in 0–99999999999,
representing an exact monetary amount with two decimal places (120050 → `1200.50`, 2 → `0.02`).
Leading zeroes are allowed. Amounts are exact money: A's `7.1` and B's Cents `710` are the same
amount, and two amounts one cent apart are different amounts at every size up to the maximum.
The same case sent by A and by B with the same values is the same record; all income entries and
their order are retained.

## 5. Current case, conflicts and history

An accepted delivery keeps its receipt, and every case file it carried stays in that case's
history; neither is changed or removed later. Two different cases are independent. Only accepted
deliveries count toward a case. A case nothing accepted has reached is missing. Otherwise only
its highest revision number decides:

- All normalized records at that revision identical: current, with that value and all its sources.
- Two or more differing normalized records at that revision: conflict, with all variants/sources.

Lower revisions stay in history and cannot change the current result. A higher unambiguous revision
resolves a lower conflict. Repeated identical entries are not conflicts; they are distinct sources.
Two records are identical when every business value agrees. A record with no contact and a record
with an empty contact are different; so are two records whose income entries are the same but in
another order. Which supplier sent a record, and under which file name, makes no difference to
whether two records are identical. Show current revision, status and sources. For a correction,
show which business values it changed, so that the coordinator can tell what each difference is
measured against. Revision numbers may skip, and the work a correction replaces may itself have
been in conflict: revision 1 may have arrived as two differing variants before revision 4 settles
the case. Show the differences between variants for a current conflict. Missing cases need no
fabricated history. Failed attempts never create accepted sources or invalidate already-current data.

The batch is ready exactly when all expected cases are current (none missing or conflicting).
Do not use arrival order or file name to pick a winner. Accepting a delivery, recognising a repeat
and the change they make to current cases happen completely or not at all, also when the same
request arrives twice, when two requests arrive together and when storage fails part-way. A single
local coordinator does not justify corrupting state when a browser repeats a request.

## 6. Consumer handoff ZIP

Only a ready batch can create a handoff. Include exactly `manifest.json` and `cases.json`, both
UTF-8 JSON. The manifest contains these keys:

```json
{"format_version":2,"synthetic":true,"disclaimer":"Training transport reconciliation; not tax validation","handoff_id":"opaque-id","batch_id":"opaque-id","batch_name":"October handoff","case_count":1,"cases":[{"return_id":"DEMO-101","year":2025,"revision":2,"receipt_ids":["opaque-receipt"]}]}
```

`cases.json` is an array in original CSV order, one item per expected identity. Each item has
`return_id`, `year`, `revision`, `filer_name`, `contact`, `income`, and `sources`. `sources` is a
nonempty array of `{receipt_id, delivery_id, supplier, filename}` for every accepted occurrence
supporting that frozen current value/revision, in receipt acceptance sequence, then original
manifest `files` entry order within each receipt. Equivalent retries retain the original receipt
and never reorder its sources. Manifest receipt_ids
are the unique supporting receipt IDs in that same order. Fields have the meanings defined above;
no raw XML, other cases or local paths. Counts, identities/revisions and source lists must agree
between manifest, case records and the handoff shown in the UI.

A handoff, once created, never changes. Every later download of it returns the same ZIP bytes,
including after the desk restarts and after later corrections.
A new explicit handoff creation may create a new identity even when data is unchanged; handoff
creation idempotency is optional, not a hidden requirement. A creation that is refused, fails or
is interrupted leaves nothing that looks like a finished handoff. An unknown final outcome after a lost response must be described honestly; show
existing handoffs so the coordinator can recover. Current data/history remain distinct from frozen
handoffs. Do not mutate old V1 inspection exports to pretend they were V2 handoffs.

## 7. Customer format examples

The starter provides one original XML, a small expected-case CSV and one minimal ZIP from each
supplier. The CSV lists DEMO-101/2025 and DEMO-101/2026: the year is part of the identity.
These files explain the customer's formats. They are not a prepared test suite. Learners design
their own supplement, correction, retry, conflict, rejection and boundary scenarios, with expected
outcomes derived from the rules above.

Input ZIPs contain `delivery.json` and XML case files. Output handoff ZIPs contain `manifest.json`
and `cases.json`; they serve the downstream consumer and are not supplier deliveries.

## 8. Batch overview business states

Every expected identity contributes to exactly one of missing, current or conflict. Their counts
sum to expected count. Ready means all expected cases are current. Has-handoff means at least one
frozen handoff exists; it does not imply the batch is currently ready. The attention filter means
not ready, or updated since its latest handoff. The ready and has-handoff filters are independent.

Before any handoff, use not-yet-handed-over rather than an updated flag. After one, a batch is
updated since handoff when a handoff created now would not say what the latest one said about its
cases: a different revision, different values, different supporting sources, or a case now in
conflict. Activity that would leave all of that as it was does not make the batch updated. A new
handoff clears the flag. These are business states, not a required storage design.
