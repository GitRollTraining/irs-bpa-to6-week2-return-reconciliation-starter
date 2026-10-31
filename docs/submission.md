# Week 2 implementation and submission guide

## Starting point and responsibility

Clone the published Return Batch Reconciliation Desk starter. It is a working V1 project with
frontend/ and backend/, a few customer format examples and locked runtime/build dependencies.
Follow its README to start both services and create a V1 batch/inspection before changing code.
Record the starting commit. Existing application code is supplied capability: its unchanged presence earns no new
implementation credit. Tests, fixtures with expected outcomes, lint/security checks and CI are
your work; none is supplied. Preserve the existing application behavior and safety controls.

Implement F1–F6 from the client request against the exact supplied input/output contract. Keep
React/pnpm and Python FastAPI/uv. You may reorganize implementation and storage; choose maintained
libraries as needed. Do not rewrite solely for size or keep a design solely because it was supplied.
An upgrade must retain readable existing V1 inspections and their JSON content, as well as original
XML/manual-entry behavior. New batches may use a new model; no legacy migration framework is mandated.

## Verification of the changed application

Create independently expected cases and meaningful new assertions; provided samples are customer
inputs, not a complete test oracle. At minimum verify:

- CSV row diagnostics, whole-list rejection, duplicate pairs and same-ID/different-year cases.
- Both XML structures, URI-aware prefix equivalence, optional/empty text, repeated ordered values,
  wrong namespaces, invalid values, DTD/entity rejection and unsafe archive members.
- A mixed invalid delivery rejects all changes while preserving each available inspection result.
- Supplements, newer/older revisions, exact and repackaged retries, delivery-ID content conflicts,
  same-revision business conflicts, their resolution by a higher revision, and unrelated-case retention.
- A persistence failure leaves accepted state intact; restart-equivalent instances recover history
  and handoffs. Test concurrent/repeated acceptance at the backend boundary without requiring an MQ.
- Upgrading a genuine V1-created database preserves historical inspection contents; do not generate
  the expected historical record by calling the upgraded implementation.
- Cross-batch overview counts and filters, independent readiness/handoff state, update flags
  relative to the latest handoff, and isolation when another batch changes.
- Handoff refusal with missing/conflicting cases, exact consumer JSON/ZIP contents, immutable H1
  after further corrections, and failure while creating a handoff leaving no published partial output.

Use real React and FastAPI in headless Playwright for CSV creation, package acceptance, a correction,
a conflict and resolution, investigation, cross-batch overview and downloaded handoff contents. Write a regression journey for the original XML/manual-entry workflow. Additional focused tests may isolate parsers/reconciliation/storage, but end-to-end
subject APIs must not be replaced with mocks. Avoid repeating the production algorithm in the oracle.

Build a CI workflow that checks startup, code quality, security, tests and build before
delivering a verified build artifact. Its commands must invoke your actual checks and propagate
failures; a workflow file or unconditional artifact upload is insufficient. Verify new dependency/application risks and untrusted XML/ZIP/UI boundaries;
record what checks do not establish. Keep synthetic test data separate from coordinator data. No
remote deployment is required. Source inspection does not certify an actual Actions execution.

## Deliverables and evidence

Submit the repository URL and immutable commit, learner-authored tests, effective CI, and README setup,
start/check/build/reset and upgrade instructions. Document configuration names/defaults actually used;
provide placeholder-only environment examples only where needed. Never include keys, personal data,
local databases or machine-specific paths in the submission. Do not create unnecessary config files
for credit. Explain material changes and how you protected the original user workflows.

Artifact checks inspect connected implementation and authored tests/configuration, with supplied-work
boundaries. Ownership and Trait read attributable learner Session evidence for different predicates;
code or a retrospective essay cannot substitute. Use the facilitator-approved recorder and confirm
capture before substantive work. Missing recorder/platform setup belongs to the facilitator, not the
learner. Do not fabricate Session turns. The existing nine supplied-case Quiz questions remain a
separate lane; answers do not earn Session credit or fill the practical time budget.
