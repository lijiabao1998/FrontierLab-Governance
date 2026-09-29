# GPT merge decisions — 2026-09-29

Owner delegation: see CONVERGENCE_20260929.md. No automatic READY promotion.
The GitHub status snapshot is descriptive; the decisions here require separate
independent inspection of the exact commit and relevant validation.

## Initial holds

- Math #2/#3: current-head P1/P2 unresolved. #4: no verified current-head review;
  exact committed-byte audit found 16 manifest mismatches. #7 remains draft.
- Math #6 and Physics #4: canonical evidence repairs underway on GPT branches.
- Physics #1/#2: unresolved findings; r2 physical-window repair requires a separately
  frozen design. #5 remains draft. No Sabra or other new exploration started.
- Biology #1: false PASS/MATCH/admission claims and verifier cohort mismatch;
  repair underway, retain INCONCLUSIVE and historical mismatch evidence.
- Chemistry #1: committed-byte hash mismatch confirmed; current C4 is post-hoc,
  C5 fails. Artifact/summary repair does not constitute new chemical validation.
- Governance #2: superseded by this maintenance branch once independently approved.
- Other governance proposals and 11 onboarding pin fixes: inspect exact diff and
  current checks before deciding. No server ruleset enabled by this wave.

## Maintenance validation

Governance: 26 unittest methods passed on Windows, including missing-clone,
wrong-commit, linked-worktree, malformed locator, pending-review READY rejection,
renderer equality and source-year regression. Existing path-string test was made
platform-independent (Path.parts); no gate semantics were weakened.

SESSION_LEDGER locators: all 11 referenced blobs found at recorded immutable
commits. This is a location check, not scientific validation or merge approval.

Original records and contradictory snapshots are preserved in
history/before_gpt_20260929; incomplete historical search provenance is explicitly
not promoted to fresh 2026-09-29 admission.
