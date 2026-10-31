# Customer input and handoff contract — change request V2

This is a fictional training format, not an IRS schema. These rules are supplied business policy,
not a request for learners to invent tax knowledge or configurable schemas. Customer examples are
inputs; learners must design their own complete test cases.

## 1. CSV work list

UTF-8 (optional BOM), comma-separated CSV with exactly the header `return_id,year`. Use normal CSV
quoting rules. There are 1–200 data records; no blank records or extra columns. Trim surrounding
field whitespace. IDs match `[A-Z0-9][A-Z0-9-]{0,39}`; year is exactly four ASCII digits in 2000–2099.
The pair is case-sensitive identity. Reject duplicate normalized pairs and identify all involved
record numbers (header is record 1; multiline quoted fields count as one CSV record). A parse failure
may identify the parser's physical line and label it as such. Batch names are trimmed, nonempty,
at most 100 Unicode code points; equal names may identify separate batches. A CSV is at most 256 KiB.
Preview and confirm must validate the same content; failed validation persists no new batch.

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
64 KiB; each XML is at most 256 KiB; total expanded content is at most 8 MiB. Enforce expanded limits
while reading, not merely from an untrusted header. File names are metadata, never filesystem paths.

Invalid envelopes are rejected without applying data. When the envelope can be inspected, process
all its listed XML files and show all available results. Any invalid XML or identity outside the
batch rejects the entire delivery: valid entries are displayed as not applied. Storage failure
likewise applies none. Log a safe receipt/attempt identity and useful diagnostics without raw
payload/contact disclosure. Rejected attempts are visible separately from accepted history; they
reserve no delivery ID, so a repaired package may reuse it. No raw-content retention is required.

Within a batch, an accepted delivery ID binds the supplier and the multiset of file names, revisions
and normalized records. Repeating it with equivalent contents returns the same accepted receipt;
ZIP member order, compression metadata and equivalent XML namespace prefixes do not change meaning.
A changed name, revision, supplier or normalized value under that accepted ID is rejected. Delivery
IDs are batch-scoped. Distinct accepted delivery IDs may repeat the same case revision; retain
provenance without treating identical normalized records as a business conflict.

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
infinity. Normalize to an exact two-place decimal string. No totals or tax calculations are required.
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
Leading zeroes are allowed. Do not use a floating-point value to determine monetary equivalence.
Equivalent A/B records have identical normalized values; all income entries/order are retained.

## 5. Current case, conflicts and history

A valid delivery creates immutable receipt and occurrence identities. Two different cases are
independent. For each expected identity, collect only occurrences from accepted deliveries.
With none, its status is missing. Otherwise consider the highest revision number only:

- All normalized records at that revision identical: current, with that value and all its sources.
- Two or more differing normalized records at that revision: conflict, with all variants/sources.

Lower revisions stay in history and cannot change the current result. A higher unambiguous revision
resolves a lower conflict. Repeated identical entries are not conflicts; they are distinct sources.
Record equivalence compares every normalized business field, including missing versus empty contact,
ordered income entries and exact normalized amounts. Supplier and file name do not change business
record equivalence. Show current revision, status and sources; show field differences against the
highest lower accepted revision for a correction (revision numbers may skip). If that lower
revision has conflicting variants, compare against each distinct variant and label the baseline;
show differences between variants for a current conflict. Missing cases need no
fabricated history. Failed attempts never create accepted sources or invalidate already-current data.

The batch is ready exactly when all expected cases are current (none missing or conflicting).
Do not use arrival order or file name to pick a winner. Acceptance, retry binding and current-state
changes must be all-or-none under repeated/concurrent requests and persistence errors. A single
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

Create an immutable handoff identity and snapshot as one complete unit. Subsequent downloads of
that identity must return the same ZIP bytes, including after restart and later corrections.
A new explicit handoff creation may create a new identity even when data is unchanged; handoff
creation idempotency is optional, not a hidden requirement. Rejected/failed creation publishes no
partial handoff. An unknown final outcome after a lost response must be described honestly; show
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

Before any handoff, use not-yet-handed-over rather than an updated flag. Otherwise compare the
current batch cases with the latest handoff's frozen cases, including revisions, normalized values
and supporting sources. Any difference, including a current conflict, means updated. An additional
accepted source for the current value/revision changes provenance. Rejected attempts, equivalent
retries and lower-revision receipts that leave the current cases unchanged do not. A new handoff
matching current cases clears the flag. These are business states, not a required storage design.
