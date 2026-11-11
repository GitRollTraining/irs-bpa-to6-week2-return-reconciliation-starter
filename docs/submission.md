# Week 2 implementation and submission guide

## Starting point and responsibility

Clone the published Return Batch Reconciliation Desk starter. It is a working V1 project with
frontend/ and backend/, a few customer format examples and locked runtime/build dependencies.
Follow its README to start both services and create a V1 batch/inspection before changing code.
Record the starting commit in your README. Existing application code is supplied capability: its unchanged presence earns no new
implementation credit. Tests, fixtures with expected outcomes and lint/security checks are
your work; none is supplied. Preserve the existing application behavior and safety controls.

Implement F1–F6 from the client request against the exact supplied input/output contract. Keep
React/pnpm and Python FastAPI/uv. You may reorganize implementation and storage; choose maintained
libraries as needed. The client request and the customer formats say what the desk must do, with
examples. They do not say how: what is stored and compared, where a check happens, what is
computed when, what a test must be able to catch. Those decisions are yours, and several of them
can be made wrongly in a way the examples will not show. Do not rewrite solely for size or keep a design solely because it was supplied.
An upgrade must retain readable existing V1 inspections and their JSON content, as well as original
XML/manual-entry behavior. New batches may use a new model; no legacy migration framework is mandated.

## Verification of the changed application

Create your own cases with expected results you worked out from the rules, and meaningful new
assertions; provided samples are customer inputs, not a complete test oracle. At minimum verify:

- CSV row diagnostics, whole-list rejection, duplicate pairs and same-ID/different-year cases.
- Both XML structures, URI-aware prefix equivalence, optional/empty text, repeated ordered values,
  wrong namespaces, invalid values, DTD/entity rejection and unsafe archive members.
- A mixed invalid delivery rejects all changes while preserving each available inspection result.
- Supplements, newer/older revisions, exact and repackaged retries, delivery-ID content conflicts,
  same-revision business conflicts, their resolution by a higher revision, and unrelated-case retention.
- A persistence failure leaves accepted state intact; history and handoffs are still there after
  the desk restarts. The same delivery accepted twice, one after the other and at the same moment.
- An upgrade keeps the work stored before it: inspections made with the starting version stay
  readable with their original report contents. A database you commit as a test fixture for this is
  test data, not one of the local databases excluded below.
- Cross-batch overview counts and filters, independent readiness/handoff state, update flags
  relative to the latest handoff, and isolation when another batch changes.
- Handoff refusal with missing/conflicting cases, exact consumer JSON/ZIP contents, immutable H1
  after further corrections, and failure while creating a handoff leaving no published partial output.

Browser journeys run in headless Playwright against your real React and FastAPI: CSV creation,
package acceptance, a correction, a conflict and resolution, investigation, cross-batch overview and
downloaded handoff contents, and a regression journey for the original XML/manual-entry workflow. A
journey whose backend is replaced with mocks is not one of these. Which of the rules above is
checked at which level otherwise, and with what data, is for you to decide. An expected result
that was produced by the code under test proves nothing.

Provide the commands that check code quality, security, tests and build on a fresh clone, and say
in the README how to run them. Cover new dependency/application risks and the untrusted XML/ZIP/UI
boundaries; record what your checks do not establish. Keep synthetic test data separate from any
real data. No CI workflow and no remote deployment are required: the course has not taught a
pipeline yet.

## Deliverables and evidence

Submit the repository URL and immutable commit, learner-authored tests and checks, the XML mapping
document that customer formats section 3 asks for (docs/xml-mapping.md), and README setup,
start/check/build/reset and upgrade instructions. Quiz answers go in answers.md at the repository root. Document configuration names/defaults actually used;
provide placeholder-only environment examples only where needed. Never include keys, personal data,
local databases or machine-specific paths in the submission. Do not create unnecessary config files
for credit. Explain material changes and how you protected the original user workflows. Keep a
decision record, docs/decisions.md, for the engineer who takes this over: each design decision you
made where these documents left the choice to you, what you chose, what you turned down, and the
case that decided it. It is part of the handover, and writing it is how you find the decisions.

Three kinds of evidence are read. Artifact checks inspect connected implementation and authored
tests/configuration, with supplied-work boundaries. Ownership reads the engineering decisions you make
and state yourself in your coding-agent session. A decision counts when you say, in your own words,
what you chose, what you turned down and a concrete case of your own that decides between them. You
can make it before the agent designs a part, or afterwards: ask how the part it built handles a case
you name, then keep or change what it did for a reason you give. Every capability, the stored data
and its upgrade, the tests and the security checks hold such decisions; these documents
do not list them. Accepting the agent's proposal, repeating a rule or an example these documents
state, or a decision that appears only in docs/decisions.md and not in your session, is not counted.
A decision that reaches the wrong conclusion for this desk is not counted either. Trait reads how you work with the agent:
saying what done means before asking for work, choosing specific results to check and checking them
yourself, and questioning a claim before relying on it. Code or a retrospective essay cannot
substitute for either. Your coding-agent session is the record: use the recorder your facilitator
names at kickoff and confirm it is capturing before substantive work; if none was named, ask the
facilitator. Missing recorder/platform setup belongs to the facilitator, not the learner. Do not fabricate Session turns. The existing nine supplied-case Quiz questions remain a
separate lane; answers do not earn Session credit or fill the practical time budget.
