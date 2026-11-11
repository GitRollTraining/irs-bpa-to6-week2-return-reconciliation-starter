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

## What counts as a decision of yours

The client request and the customer formats say what the desk must do. How it does it is yours to
decide, in every capability, in the stored data and its upgrade, in the tests and in the security
checks. These documents do not list the decisions. A decision is counted when a message of yours
in the coding-agent session says, in your own words, what you chose, what you turned down, and a
concrete case that decides between them.

1. A decision says how, not that. The client has already said what must happen; asking for that
   behaviour, or for a test of it, repeats the client. An example from another system: "Two clerks
   must never lose each other's edit; add a test for it" is a requirement. "Each save carries the
   version it read and is refused when the stored version is newer. I am turning down
   last-write-wins: two clerks saving the same order one after the other would lose the first edit
   without a message" is a decision.
2. The case is one you made up, or one from these documents that you run through both options and
   say where they differ. Naming a document's example, or adding one more example of a rule the
   documents state, is repetition.
3. You can decide before the agent designs a part, or after it has built or recommended something.
   Afterwards, "agreed" and "go ahead" are not counted. Ask how the part handles a case you name,
   then keep or change it and say what the other option would have done in that case. Asking the
   agent what the options are and what each does in your case leaves the decision with you; asking
   it which one to pick gives the decision away.
4. The deciding words are yours. Asking the agent to name the reason, the risk or the limit, or to
   write the decision into a file, hands it the decision. A decision that appears only in
   docs/decisions.md is not counted.
5. Give each decision its own case. Several decisions in one message are read, but one case cannot
   carry two decisions.

A decision that reaches the wrong conclusion for this desk is not counted.

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
for credit. A repository holding more than 8 archive files cannot be read by the grader. Where
your test deliveries come from, and how a reader checks one against its expected result, is for you
to decide within that limit. Explain material changes and how you protected the original user workflows. Keep a
decision record, docs/decisions.md, for the engineer who takes this over: each design decision you
made where these documents left the choice to you, what you chose, what you turned down, and the
case that decided it. It is part of the handover, and writing it is how you find the decisions.

Three kinds of evidence are read. Artifact checks inspect connected implementation and authored
tests/configuration, with supplied-work boundaries. Ownership reads the engineering
decisions you make and state yourself in your coding-agent session; the section What counts as a
decision of yours says what is read. Trait reads how you work with the agent:
saying what done means before asking for work, choosing specific results to check and checking them
yourself, and questioning a claim before relying on it. Code or a retrospective essay cannot
substitute for either. Your coding-agent session is the record: use the recorder your facilitator
names at kickoff and confirm it is capturing before substantive work; if none was named, ask the
facilitator. Missing recorder/platform setup belongs to the facilitator, not the learner. Do not fabricate Session turns. The existing nine supplied-case Quiz questions remain a
separate lane; answers do not earn Session credit or fill the practical time budget.
