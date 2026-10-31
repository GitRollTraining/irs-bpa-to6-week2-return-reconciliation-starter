# Return Batch Reconciliation Desk — client change request

## What we need

Our coordinator uses a small local desk to register a list of expected cases, read the files a
preparation team sends, and download an inspection report. We now receive work from two teams.
They send different file formats, often in several deliveries, and sometimes correct work they
sent earlier. Our coordinator needs to see what is still missing, resolve discrepancies with the
sender, and hand a complete set of cases to the next operations team.

One coordinator handles up to ten batches a day. A batch contains 1–200 expected cases, and a
supplier delivery contains 1–30 case files. This remains a local tool; we are not requesting a
new account system or an online service. These are fictional training records. We need the files
reconciled according to the supplied rules, not a judgment about tax correctness.

Please add the following six capabilities.

## F1 — Start a batch from our case list

We already maintain a CSV list of the cases we expect. Let the coordinator upload it, give the
batch a name, and review the list before creating the batch. Identify any problem by its row so
we can fix the original list. If it contains a problem, do not quietly skip a case or create an
incomplete batch.

A case is identified by its return number and year together: the same number for two years means
two different cases. The same number and year listed twice is a mistake. Once the batch is
created, its expected list stays fixed. Different batches may have the same display name.

For example, if A/2025 appears twice, we should be told which rows to correct before proceeding.
A/2025 and A/2026 may both appear without being treated as duplicates.

## F2 — Receive a supplier delivery

Each preparation team sends a ZIP package containing its delivery list and XML case files.
Let the coordinator choose a batch and submit either team's package. Present the two teams'
records consistently, so the coordinator does not need to understand their different formats.

Show a result for each file we can inspect: its name, the case it belongs to when readable, and
what needs correction when there is a problem. One unreadable file should not hide the other
available results. If any part is invalid, unsafe or contains a case outside this batch, reject
the entire delivery and clearly show that none of it was applied. Previously accepted work must
remain intact. We can then ask the team to repair the package and send it again.

## F3 — Keep track of supplements and corrections

Teams must be able to send just the missing or corrected cases without replacing everything
already received. Use their revision numbers to identify the latest work. A late arrival of an
older revision must not undo a newer one, and an update to one case must not remove another case.

If a team accidentally sends the same delivery again, show the original receipt rather than
counting it twice. If it uses the same delivery number for different contents, explain the
problem. If two different records claim to be the same case revision, flag a conflict instead
of choosing whichever arrived last. A later revision with one agreed set of values resolves it.
Keep earlier deliveries available for reference.

For example, after receiving A and B, we may receive C, followed by a correction to A. We should
then have all three cases, with only A changed.

## F4 — Show what still needs attention

Give the coordinator a case list that can be narrowed to missing, current or conflicting cases.
From a case, let us inspect its delivery history and see the business values that changed between
revisions. When records conflict, show the differing values and where each came from, so we can
ask the sender a precise question.

Keep rejected attempts clearly separate from accepted work. Switching between batches or cases
must not show details belonging to the previous selection. We do not need an editor or a button
to pick an arbitrary winner; corrections come from the preparation teams.

For example, a corrected case can become ready while its earlier disagreement remains visible
in its history. We should not need to open every old file to understand what happened.

## F5 — Hand over a complete, fixed package

Once every expected case has a current record and no unresolved conflict, let us create and
download a handoff for the next operations team. Otherwise, tell us which cases still prevent it.
The package must contain every expected case exactly once, identify its revision and sources,
and follow the receiving team's agreed format. It must not include unrelated records or internal
computer details.

We must be able to find and download an earlier handoff after closing and reopening the desk.
Later corrections may lead to a new handoff, but must never change an earlier package. If saving
is interrupted, do not tell us a package is ready when only part of it was saved.

For example, H1 may contain A revision 2 and a later H2 contain revision 3. Both remain available,
and downloading H1 again must return the same file we originally handed over.

## F6 — See which batches need attention today

When the coordinator opens the desk, show all batches with their names, expected case counts,
received current cases, missing cases and conflicts. Let us narrow the list to batches needing
attention, batches ready for handoff, and batches that have a previous handoff, then open the
relevant batch to investigate. These views may overlap: a batch can have an earlier handoff and
now need attention again. We are not asking for deadlines or an automatic priority calculation.

If the current cases, revisions or their supporting delivery sources have changed since the
latest handoff, clearly flag that batch as updated since handoff. Even a new supporting source
for the same values changes the provenance we send downstream. An accidental repeat, rejected
package, or late old revision that leaves the current cases and sources unchanged must not
raise this flag. Before any handoff, show that the batch has not yet been handed over.

For example, one batch may be ready but never handed over, while another has H1 and has since
received a correction or a new conflict. We need to distinguish them without opening every batch.
After creating a new handoff matching the current cases, its update flag clears. An operation
on one batch must never change another batch's counts, handoff history or attention state.

## Our files and existing work

The [customer file reference](docs/input-formats.md) supplies the precise formats and rules:
our CSV says which cases to expect; supplier ZIPs contain XML records and delivery information;
the outgoing handoff ZIP contains JSON records in the receiving team's format. The two kinds of
ZIP package serve different purposes.

Please keep the existing manual registration and original XML-reading functions usable. We must
also be able to reopen and download our earlier inspection reports with their original contents.
An upgrade must not require us to delete the work already stored on the desk.
