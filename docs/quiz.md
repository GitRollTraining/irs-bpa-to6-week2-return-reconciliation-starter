# Week 2 decision cases — Quiz

Nine scenario-based open-ended cases, each assigned to one whole course checkpoint. These are
self-contained: completing the software is not needed to answer them. The cases use the return
desk's engineering context, but all facts needed for each decision appear in that case.
Use the supplied facts; do not invent observations or claim personal execution. AI assistance is
permitted, but every submitted claim must be justified against the case. These answers are not
Ownership Session evidence and do not establish actual Git/tool/user activity.

Submit answers.md labeled Q1–Q9. For each give your decision, evidence/reasoning, a plausible wrong
alternative and the limit of your conclusion. Concise tables/code/graphs are welcome; no word-count
score. A correct alternative with explicit assumptions is valid. Trainer answers are separate.
Estimated active answer time with permitted AI:90–135 minutes, unmeasured. No external account,
service access or practical implementation is required for these supplied-fact cases.

## Q1 — Isolate unfinished work without losing it

You are on local main at commit C. Your worktree has uncommitted edits to parser.py for feature A.
A teammate needs you to start unrelated fix B from the clean C baseline. No one else depends on
your local branch names. The remote main is also C. Nothing has been committed for A yet.

Explain a safe sequence that preserves A, starts B on the correct baseline, and later lets you
resume A. After B is accepted into main, explain how A incorporates that fix without losing its
own changes; distinguish moving a branch reference from merging content. State the working-tree/
ref conditions before each switch. Compare committing A on its
own branch with stashing it. A teammate suggests renaming main to feature-a, deleting the old
remote main, and continuing there: explain which parts do not solve the actual isolation problem.
Finally, explain when the temporary B branch can safely be deleted and what deleting its name
does and does not remove. Do not claim you executed commands; justify the intended state transitions.

## Q2 — Make a collaboration request that can actually be reviewed

You have read access, but no push access, to an upstream repository. Issue #42 contains a
reproducible bug, expected/actual behavior and synthetic input. It is unassigned and labeled bug.
PR #51 from another contributor fixes the same symptom but has no test and has not been accepted.
A team member writes "looks good" in chat; neither the issue owner nor a reviewer has approved it.
The team policy requires a linked issue, a focused diff, verification evidence and a review before
merge. You may use a fork. No CLI commands have yet been run.

Describe your fork/clone/remote and PR workflow. Decide whether to amend/collaborate on #51 or
propose a separate PR, stating what you would ask first. Draft a concise review request including
the issue link, evidence needed and specific owner/team mention. Explain who should take ownership
of #42 and when its state should change; a submitted PR alone does not prove the bug is resolved.
Write one saved review reply adapted to the missing regression evidence in this case. Explain
useful labels, when a
Discussion rather than an Issue is appropriate, and why reactions or saved replies cannot replace
a substantive approval. Include the purpose of the relevant CLI PR operations, not a claim of use.

## Q3 — Choose an integration strategy without rewriting shared work

The graph is main: A-B-C and feature: A-B-D-E. D and E have been pushed; another developer has
based F on E. The team permits a squash merge for a finished feature but forbids rewriting commits
that others depend on. C adds a size guard to upload(); E changes its return value. Both changes
must survive. There is also an independent fix H on a different branch that you need in a release
without that branch's other features.

Compare merge (including why fast-forward is unavailable now), rebase and squash for this graph.
Choose an integration approach and explain what happens to D/E and the dependent F. State how you
would resolve the overlapping upload change and verify both intended behaviors. Explain when
cherry-picking H is appropriate and what dependency/conflict checks it still needs. A clean merge
result alone is not evidence that both behaviors survived.

## Q4 — Decide whether to accept a Copilot suggestion

GitHub Copilot proposes this Python function for a training import. The supplied rule accepts
unsigned ASCII decimal text with at most two fractional digits and returns an exact two-place
string. Scientific notation, signs, commas, nonfinite values and extra precision are invalid.
Input may contain private contact text elsewhere in the same raw document; only synthetic data
may be sent to external tools.

```python
def amount(text):
    return f"{float(text.strip()):.2f}"
```

Explain what you would accept, reject or ask Copilot to revise, using at least two concrete input
counterexamples and the checks you would perform. Describe the minimum context you would provide
to the assistant without sending the full raw document. Distinguish a useful suggestion from a
verified result. State what evidence would be needed to claim a speed or defect improvement; the
mere presence of this code cannot identify who wrote it or which assistant was used.

## Q5 — Is the new agent rule actually helping?

A team compares the same model/version, task input, token budget and done.sh threshold, using a
clean checkout for each arm. Each row is a paired baseline/added-rule run initiated in the same
trial window; order was alternated. done.sh checks output schema, expected values and existing
regressions. Times include unsuccessful runs; no task was omitted.

| Pair | Baseline threshold | Added-rule threshold | Baseline minutes | Added-rule minutes |
|---|---|---|---:|---:|
| 1 | pass | pass | 12 | 10 |
| 2 | fail | pass | 8 | 15 |
| 3 | pass | pass | 10 | 11 |
| 4 | fail | fail | 9 | 12 |

The new rule is "before changing code, list assumptions and use the existing verification command."
The author claims "25% faster and always correct" and proposes a permanent extra agent. The four
runs contain no adaptive adversary and test only one task. The failure in pair4 is a stale fixture;
there is no evidence yet about whether the extra rule caused or prevented that error.

Compute the observed success rates and raw mean times, then explain what can and cannot be
concluded about improvement. Propose the next paired evaluation with a concrete done threshold,
variance/flakiness treatment and objective versus subjective judgments. If the rule is claimed
as a security guardrail, explain the missing adaptive-adversary test. Decide whether the evidence
licenses the extra architecture; a justified defer/limited adoption is acceptable.

## Q6 — Which implementation would you be willing to maintain?

The return desk now supports exactly two documented supplier formats and has two maintainers.
No third supplier or runtime plugins are planned. Both candidates pass the same hypothetical
independent behavior checks and meet the current request. Those checks are case facts, not files
provided in your starter.

Candidate A: two small supplier readers return the same documented record type; reconciliation
and handoff serialization are separate functions. Both readers call one normalize_identity helper.
Their names and inputs/outputs are documented.
Candidate B: six provider interfaces, a runtime plugin registry and three formatter factories.
Its adapters each copy the same identity-trimming rule. A new maintainer must inspect the registry
and three factories to locate the output field definition. Its author says "more scalable."

Choose what to accept or simplify and justify it against the actual requirements and next
maintainer. Give a concrete instruction to the AI and a stopping condition for simplification.
Explain what new evidence could make B appropriate. Do not substitute correctness/test coverage
for the maintainability judgment; those are already held equal in the case.

## Q7 — Review a generated change, including its claimed fix

Requirement: every listed file gets an available inspection outcome; malformed files do not hide
later files. Any invalid file rejects the entire delivery, with no accepted case changes. Internal
storage failures must not be reported as malformed user input. The agent proposes:

```python
def inspect(files):
    results = []
    try:
        for file in files:
            record = parse_xml(file)
            save(record)
            results.append({"name": file.name, "record": record})
    except Exception:
        return [{"error": "MALFORMED_XML"}]
    return results
```

The agent reports "reviewed and done." Its only test supplies one valid file. You request a
correction. The revised code moves try/except inside the loop but still catches Exception and
labels every failure MALFORMED_XML. It still calls save(record) inside the loop before knowing
whether every file is valid. Its new test has a malformed first file and a valid second one, but
asserts only the two returned results; it never inspects persisted case state.

Write your initial review: establish intent, identify a concrete missed issue and request a
specific change with evidence. Then review the stated revision: what is fixed, what remains, and
what would justify acceptance? Explain why asking the same agent to approve its own change is not
a substitute for your analysis. Your answer evaluates the supplied diff; it does not claim a
real GitHub review occurred.

## Q8 — Define acceptance before trusting done

A coordinator expects A/2025 and B/2025. A case is current only when the highest accepted revision
has one normalized business value. Distinct accepted receipts may supply an identical value at
that revision without creating a conflict; differing values at that revision do create a conflict.
An unreadable document cannot establish that an expected identity arrived. A delivery containing
an invalid file applies none of its cases, while showing all available inspection outcomes.

The batch already has two accepted receipts containing identical A/2025 revision 1 values, with
no accepted B. A new delivery contains a readable B/2025 revision 1 and a malformed XML file
containing the literal text B/2025. No part of that new delivery has been applied. A usable result
must help the coordinator identify the blocker and request a corrected package from the sender.
The agent proposes acceptance as "the server returns 200 and there are no exceptions." You have
not authorized implementation yet.

Define an acceptance plan before implementation: expected per-file and batch outcomes for this
example, important counterexamples, how each will be checked, and a user-centered check distinct
from code conformance. Include a follow-up valid same-revision A with a different value and then
an unambiguous higher revision; distinguish duplicate transport from conflicting business data.
Explain why 200/no-exception is insufficient. State what evidence would permit acceptance, what
would cause refusal, and what remains unknown about real user value until someone uses the flow.
Do not claim that writing a plan proves it was followed or that user validation already happened.

## Q9 — Which evidence shows the real flow survived a change?

The following are supplied hypothetical observations, not your own run history:

- Revision R0: an actual browser against the local UI and backend uses the original manual-entry
  and supplier-A XML inspection flow, then downloads the expected report successfully.
- After change R1: the agent says "done; all tests green." Its green test intercepts every backend
  request and supplies a canned200 response. No real-stack run was performed for R1.
- R1 adds supplier-B ZIP import and handoff. A coordinator runs the actual R1 flow with a valid
  supplier-B file whose namespace uses a different prefix. The real backend responds 400 because
  the new reader matches the literal prefix. The UI cannot complete that case or create a handoff.
- Revision R2 replaces literal-prefix matching with namespace-URI matching. No run results for R2
  are supplied. The API and database are available locally. A teammate proposes calling it complete
  because the patch looks correct.

Identify what failure the agent's claim missed, what the mock test does and does not establish,
and the real-flow checks you would require after R2, including the original supplier-A flow.
Explain when you would request tests during development rather than waiting until the final patch.
Distinguish startup smoke, targeted sanity,
prior-behavior regression and end-to-end checks. Explain how non-builder user testing and customer
acceptance differ from those automated checks. Make an evidence-bounded completion decision now;
do not invent a successful R2 run or customer acceptance.
