# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: [TODO: tutorial code]
- Members, GitHub usernames and cohorts:
  - Alex Larkings (AL), [DaRealElementus](https://github.com/DaRealElementus), UG
  - Rhys Watson (RW), [Proffo1](https://github.com/Proffo1), UG
  - Andrew Rainey (AR), [expertkaos](https://github.com/expertkaos), UG
  - Nemika De Zoysa (ND), [BilyFlowers](https://github.com/BilyFlowers), UG
- Repository URL: https://github.com/DaRealElementus/ST1-ASS3
- Starting SHA: `f924876bedf303d4fb4362fd1a104ee2cd9f7482` (the last setup/documentation commit before any Stage 6 code change)

## A Requirement to issue activities

### FR-02 Patient Search

- Title: `PatientService.find_patient` – look up a registered patient by ID (FR-02)
- Context: Reception staff need to retrieve an existing patient before booking or reviewing appointments. The starter left `PatientService.find_patient` raising `NotImplementedError`.
- Requirement: Given a patient ID, return the patient object already held in the shared `SmartCareDataStore`. Never create or replace a record during a lookup.
- Acceptance criteria:
  - AC-02.1: A registered ID returns the *same* stored `Patient` object (`is` identity, not a copy).
  - AC-02.2: An unknown ID raises `LookupError`; a blank, whitespace or `None` ID raises `ValueError`. In both cases the store is unchanged.
- Scope: `PatientService.find_patient` in `project/smartcare/services.py` and its tests. Out of scope: domain classes, data store internals, console menu.
- Definition of Done: AC met; tests in `tests/test_services.py` cover both ACs; the original 8 starter tests still pass; full suite passes from `project/`; PR reviewed by another member against the diff; merged to `main`; issue closed.
- Owner: RW (Proffo1); reviewer AR (expertkaos)
- Actual issue link: https://github.com/DaRealElementus/ST1-ASS3/issues/4

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: `AppointmentService.cancel_appointment` – cancel while retaining history (FR-06/FR-07)
- Context: A scheduled appointment may need cancelling. The clinic must keep cancelled appointments for history, and the slot must become free to book again.
- Requirement: Cancel an appointment by ID through the domain `Appointment.cancel()` method and return the stored object. Do not delete or replace the record.
- Acceptance criteria:
  - AC-05.1: Cancelling a `SCHEDULED` appointment sets it to `CANCELLED`, returns the same stored object, and the appointment stays in `list_appointments()`. Other appointments are unaffected.
  - AC-05.2: An unknown ID raises `LookupError`; a blank/`None` ID raises `ValueError`; the store is unchanged.
  - AC-05.3: Cancelling an already `CANCELLED` or a `COMPLETED` appointment raises `ValueError` and leaves its state unchanged. A cancelled slot can be rebooked and both records remain.
- Scope: `AppointmentService.cancel_appointment` in `services.py` and its tests. Out of scope: changes to `Appointment` state rules, data store, console.
- Definition of Done: as for FR-02, plus history retention checked by a test.
- Owner: AL (DaRealElementus); reviewer RW (Proffo1)
- Actual issue link: none. The work was done in [PR #1](https://github.com/DaRealElementus/ST1-ASS3/pull/1) without a linked issue. [TODO: create a retrospective issue with the criteria above and link it to PR #1, or confirm the gap with the tutor]

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | Weak | Says nothing about what changed, where or why; a reviewer has to open the diff to find out. |
| final version | Weak | Describes a feeling of being finished, not a change. It also gets misleading once more commits follow. |
| Add patient search by ID | Strong | Imperative mood, one focused behaviour, and it tells you which feature changed. Adding an issue reference (e.g. `#4`) would make it stronger. |
| fix stuff | Weak | Vague about which defect was fixed, so it cannot be traced to an issue or test. |
| Prevent cancellation of completed appointments | Strong | States the exact rule the change enforces, so it maps directly to AC-05.3 and a test. |

Our own history has both kinds. `add PatientService.Find_Patient` (31f3d6d) and `Add __repr__ and __str__ to domain classes` (c432838) are reasonable. `Update services.py` (4c59af9), `update cl` (3ca30be) and `missed some things... whoops` (b8a7f0d) are weak and we will avoid them from Stage 7.

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR no longer matches its issue (FR-06/07). Renaming patient fields and restructuring other code have nothing to do with cancellation, so the diff is bigger and harder to review, and it is unclear which changes the issue actually approved.
- Responsibility and architecture concerns: Renaming `Patient` fields changes the domain contract used by the store, services, console and tests, so it could break other members' work. Restructuring code can move responsibilities (e.g. putting state rules in the service instead of `Appointment.cancel()`). A new dependency changes the approved environment (Python 3.13, pytest 8.3.5) for everyone without agreement.
- Testing and review concerns: The supplied tests may need edits just to match the renames, which hides whether behaviour was preserved. A reviewer cannot tell whether a failure comes from cancellation or from the refactor. Each member would also need to reinstall dependencies before they could verify anything.
- Changes to remove or separate, with reasons: Keep only `cancel_appointment` and its tests in this PR. Revert the patient field renames, and raise an issue for them only if there is a real need. Move any justified restructuring to a separate refactoring PR (Stage 8 has a dedicated refactoring step) that has the full suite passing before and after. Remove the dependency unless the team and tutor agree it is needed, and then add it through its own PR with `requirements-dev.txt` updated.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: Which tests were run, from which directory, against which SHA, and with what count of passes and failures. It does not show that the change meets each acceptance criterion, that the supplied tests are still unchanged, or that the diff stays in scope. "Looks good" gives no reasoning that anyone can check.
- Follow-up review question 1: Which acceptance criteria does this diff satisfy, and which test asserts each one?
- Follow-up review question 2: Does the lookup return the *same* stored object, or could it create or replace a record?
- Follow-up review question 3: When the operation is rejected (unknown ID, blank ID, invalid transition), is the store left completely unchanged? Which test proves it?
- Follow-up review question 4: Are any changes outside the issue's scope, e.g. edits to supplied tests, domain classes or unrelated files?
- Follow-up review question 5: What exact command, working directory and result support "tests pass", and on which commit?
- Additional questions if useful: Does the service delegate state rules to the domain (`Appointment.cancel()`) instead of duplicating them? Are the error types (`LookupError` vs `ValueError`) the ones the docstrings specify?

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | `feature/<short-description>` for features (e.g. `feature/find-patient`, `feature/find-practitioner`). Use `test/<area>` or `fix/<area>` where it fits. One branch per issue, created from an up-to-date `main`. |
| Commit message convention | Imperative, specific subject that says what behaviour changed (e.g. "Add PatientService.find_patient lookup"), with the issue number where possible. No "update file" or "fix stuff" messages. |
| PR size | One issue per PR: the code change plus its tests. Checklist ticks are allowed. Unrelated refactors or renames go in a separate PR. |
| Another-member review requirement | Each PR is reviewed by the reviewer named in `checklist.md`, who is never the author. The reviewer reads the actual diff and writes their own observations before consulting Copilot. |
| Merge rule | Merge only after reviewer approval, with the full suite passing from `project/`. The reviewer (or another non-author) merges. No force-pushing to `main`. Afterwards everyone pulls `main` and re-runs the tests. |
| Significant Copilot disclosure rule | Any significant AI suggestion that is used (code, tests, review points) is logged in `ai_usage_log.md` and/or section H: prompt, output summary, human check, Accept/Modify/Reject, reason, link. |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| [#4 PatientService.find_patient](https://github.com/DaRealElementus/ST1-ASS3/issues/4) | FR-02 | RW (Proffo1) | AC-02.1, AC-02.2 (section A). The issue body is currently empty. [TODO: paste the AC into the issue] | Closed 2026-10-28 (PR #19) |
| [#3 PractitionerService.find_practitioner](https://github.com/DaRealElementus/ST1-ASS3/issues/3) | FR-03 (supporting practitioner lookup) | AR (expertkaos) | Same lookup rules as FR-02 applied to practitioners: the stored object is returned, unknown → `LookupError`, blank → `ValueError`, no mutation | Closed 2026-10-28 (PR #20) |
| [#5 tests/test_services.py](https://github.com/DaRealElementus/ST1-ASS3/issues/5) | FR-02/03/06/07, NFR-01 | ND (BilyFlowers) | "lookup/errors, identity, cancel/history, rejection without mutation" (issue comment) | Closed 2026-10-28 (PR #21) |
| No issue (see A) | FR-06/07 cancellation | AL (DaRealElementus) | AC-05.1–05.3 (section A) | Implemented in PR #1; no issue yet |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

### PR #1 – cancellation

- PR link and title: [#1 Update services.py](https://github.com/DaRealElementus/ST1-ASS3/pull/1)
- Linked issue and requirement: none linked; FR-06/07
- Feature branch: `Feature-CancelAppointment`
- Changed behaviour: `AppointmentService.cancel_appointment` looks up the appointment through `find_appointment` and calls the domain `appointment.cancel()`, returning the retained stored object.
- Meaningful commits: [4c59af9](https://github.com/DaRealElementus/ST1-ASS3/commit/4c59af9) (implementation), [f4301cd](https://github.com/DaRealElementus/ST1-ASS3/commit/f4301cd) (checklist)
- Test command, directory and observed result: the PR body says "tests have passed". No command or count was recorded.
- Another-member reviewer: RW (Proffo1)
- Human observations recorded before Copilot: comment "Looks good" at 2026-10-16 03:13:45 UTC. No detailed observations were recorded.
- Requirement, responsibilities, test assertions and unrelated-scope checks: not recorded in the PR. [TODO: reviewer to add]
- Key feedback: none recorded
- Author response/change and verification: not applicable (no feedback)
- Reviewer recheck and approval: [approved by Proffo1 2026-10-16 03:14:05 UTC](https://github.com/DaRealElementus/ST1-ASS3/pull/1)
- Merge outcome and SHA: merged by Proffo1, `890e979b997afe949f17529e6d1d77c6657038f4`
- Significant Copilot assistance: none (no member used Copilot)
- Linked issue closure: not applicable (no issue)
- Each member updated main: [TODO]
- Integrated verification after merge: [TODO]

### PR #19 – patient lookup

- PR link and title: [#19 Feature/find patient](https://github.com/DaRealElementus/ST1-ASS3/pull/19)
- Linked issue and requirement: [#4](https://github.com/DaRealElementus/ST1-ASS3/issues/4), FR-02
- Feature branch: `feature/find-patient`
- Changed behaviour: `PatientService.find_patient` returns the stored patient from `data_store.find_patient` and raises `LookupError('Patient not found')` when it is absent. Blank-ID `ValueError` comes from the store's ID validation.
- Meaningful commits: [31f3d6d](https://github.com/DaRealElementus/ST1-ASS3/commit/31f3d6d), [2bca5b9](https://github.com/DaRealElementus/ST1-ASS3/commit/2bca5b9) (checklist)
- Test command, directory and observed result: not recorded in the PR
- Another-member reviewer: AR (expertkaos)
- Human observations recorded before Copilot: comment "yeah looks good" at 2026-10-28 05:05:02 UTC
- Requirement, responsibilities, test assertions and unrelated-scope checks: not recorded. [TODO]
- Key feedback: none recorded
- Author response/change and verification: not applicable
- Reviewer recheck and approval: no formal GitHub approval; the reviewer commented and merged
- Merge outcome and SHA: merged by expertkaos, `b6e5d391ba9933135bf084aadcb8c6bcefea7a61`
- Significant Copilot assistance: none (no member used Copilot)
- Linked issue closure: #4 closed manually 2026-10-28 05:11 UTC
- Each member updated main: [TODO]
- Integrated verification after merge: [TODO]

### PR #20 – practitioner lookup

- PR link and title: [#20 added find_practitioner function and updated checklist](https://github.com/DaRealElementus/ST1-ASS3/pull/20)
- Linked issue and requirement: [#3](https://github.com/DaRealElementus/ST1-ASS3/issues/3), FR-03
- Feature branch: `feature/find-practitioner`
- Changed behaviour: `PractitionerService.find_practitioner` returns the stored practitioner or raises `LookupError('Practitioner not found')`
- Meaningful commits: [b883b3f](https://github.com/DaRealElementus/ST1-ASS3/commit/b883b3f), [8584b9f](https://github.com/DaRealElementus/ST1-ASS3/commit/8584b9f) (checklist)
- Test command, directory and observed result: not recorded in the PR
- Another-member reviewer: ND (BilyFlowers)
- Human observations recorded before Copilot: comment "Great work Andrew Rainey." at 2026-10-28 06:12:14 UTC, posted after the merge
- Requirement, responsibilities, test assertions and unrelated-scope checks: not recorded. [TODO]
- Key feedback: none recorded
- Author response/change and verification: not applicable
- Reviewer recheck and approval: no formal GitHub approval; the reviewer merged
- Merge outcome and SHA: merged by BilyFlowers, `85e20d9e0ab600e71b08da4b22e2505e8b3373ea`
- Significant Copilot assistance: none (no member used Copilot)
- Linked issue closure: #3 closed manually 2026-10-28 05:32 UTC (before the PR merged)
- Each member updated main: [TODO]
- Integrated verification after merge: [TODO]

### PR #21 – service tests

- PR link and title: [#21 Test services](https://github.com/DaRealElementus/ST1-ASS3/pull/21)
- Linked issue and requirement: [#5](https://github.com/DaRealElementus/ST1-ASS3/issues/5); FR-02/03/06/07, NFR-01
- Feature branch: `Test-Services`
- Changed behaviour: adds `project/tests/test_services.py` (lookup/errors, identity, cancel/history, booking and registration rejection without mutation). No production code changed.
- Meaningful commits: [c6b38ad](https://github.com/DaRealElementus/ST1-ASS3/commit/c6b38ad) (tests), [3ca30be](https://github.com/DaRealElementus/ST1-ASS3/commit/3ca30be) (checklist), [1bf5634](https://github.com/DaRealElementus/ST1-ASS3/commit/1bf5634) (merge of `main` into the branch by AL)
- Test command, directory and observed result: [TODO: `python -m pytest` in `project/`; record the observed count]
- Another-member reviewer: AL (DaRealElementus)
- Human observations recorded before Copilot: none recorded on the PR. [TODO]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [TODO]
- Key feedback: none recorded
- Author response/change and verification: not applicable
- Reviewer recheck and approval: no formal GitHub approval; the reviewer merged
- Merge outcome and SHA: merged by DaRealElementus, `ec4d4a2c053481d075c1a86cb5c3841ad37cc72f`
- Significant Copilot assistance: none (no member used Copilot)
- Linked issue closure: #5 closed 2026-10-28 06:15 UTC
- Each member updated main: [TODO]
- Integrated verification after merge: [TODO]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

No member of the group used GitHub Copilot for any Stage 6 work: not for implementation, tests or PR review. Every service method, test and review was written by a group member. The only AI use in Stage 6 was AL's Claude Code session for PR #2 (below), which is outside the three service targets. PR #18 was opened by the Copilot coding agent, but it changes the countdown GitHub Action, not Stage 6 code.

- Member and task: AL – considering dunder methods for domain classes ([PR #2](https://github.com/DaRealElementus/ST1-ASS3/pull/2), quality-of-life, outside the three Stage 6 targets)
- Prompt/purpose and relevant issue/diff: Asked whether dunder methods would help in `services.py`/`domain.py`, and whether `__int__`/`__dict__`/`__list__` would convert objects automatically based on type hints. Diff: [c432838](https://github.com/DaRealElementus/ST1-ASS3/commit/c432838). Tool: Claude Code (the approved equivalent route; see `ai_usage_log.md` Entry 1)
- Summary of output: Recommended `__repr__`/`__str__` on the domain classes only. Advised against ID-based `__eq__`/`__hash__` because it could hide "replacement object" bugs. Explained that type hints never trigger conversions.
- Human check against actual code, requirements and tests: AL read `services.py`/`domain.py`, printed all three classes manually, ran the full suite (8 passed at the time) and reviewed the diff.
- Decision — Accept / Modify / Reject: Accept (`__repr__`/`__str__`); Reject (automatic conversion idea, `__eq__`/`__hash__`, `__lt__`)
- Reason: Readable output helps debugging and test failure messages. Identity-based equality would weaken the Stage 6 identity checks.
- Verification/evidence: [ai_usage_log.md](../ai_usage_log.md), PR #2 merged as `1797d58`

## I Human versus Copilot review comparison

No comparison is possible: no member of the group used Copilot to review any Stage 6 PR (#1, #19, #20, #21). All reviews were done by a human only.

- Human reviewer noticed before consulting Copilot: Copilot was not consulted. The human reviews are the comments recorded in section G.
- Copilot noticed: not applicable (Copilot was not used)
- Overlap: not applicable
- What did the human reviewer notice that Copilot did not: not applicable
- What did Copilot identify that the human reviewer initially missed: not applicable
- Unsupported or incorrect Copilot suggestion: none, because Copilot was not used
- Human judgement accepted, modified or rejected, and why: all merge decisions were human-only
- Which evidence justified merge approval: the other member's review of the PR diff (section G) and the passing test suite

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: Alex Larkings (AL, DaRealElementus)
- Implementation: `cancel_appointment` ([4c59af9](https://github.com/DaRealElementus/ST1-ASS3/commit/4c59af9), PR #1); `__repr__`/`__str__` on domain classes (PR #2)
- Testing: ran the suite for PR #2 (logged in `ai_usage_log.md`)
- Review: merged PR #21; merged `main` into `Test-Services` ([1bf5634](https://github.com/DaRealElementus/ST1-ASS3/commit/1bf5634))
- Issue refinement: created issues #3–#16, including the test scope comment on #5
- Design and responsibility discussion: dunder-method design decision recorded in `ai_usage_log.md`
- Debugging or integration: integrated `main` into the tests branch before merge
- Documentation or team support: created the repo, `checklist.md`, the Git workflow documentation ([f924876](https://github.com/DaRealElementus/ST1-ASS3/commit/f924876)) and the README countdown/issue tracker (PR #17)

- Member: Rhys Watson (RW, Proffo1)
- Implementation: `PatientService.find_patient` ([31f3d6d](https://github.com/DaRealElementus/ST1-ASS3/commit/31f3d6d), PR #19)
- Testing: [TODO]
- Review: approved and merged PR #1; merged PR #2
- Issue refinement: not applicable
- Design and responsibility discussion: [TODO]
- Debugging or integration: [TODO]
- Documentation or team support: updated checklist ([2bca5b9](https://github.com/DaRealElementus/ST1-ASS3/commit/2bca5b9))

- Member: Andrew Rainey (AR, expertkaos)
- Implementation: `PractitionerService.find_practitioner` ([b883b3f](https://github.com/DaRealElementus/ST1-ASS3/commit/b883b3f), PR #20)
- Testing: [TODO]
- Review: reviewed and merged PR #19
- Issue refinement: not applicable
- Design and responsibility discussion: [TODO]
- Debugging or integration: [TODO]
- Documentation or team support: updated checklist ([8584b9f](https://github.com/DaRealElementus/ST1-ASS3/commit/8584b9f))

- Member: Nemika De Zoysa (ND, BilyFlowers)
- Implementation: not applicable
- Testing: wrote `project/tests/test_services.py` ([c6b38ad](https://github.com/DaRealElementus/ST1-ASS3/commit/c6b38ad), PR #21), covering lookup errors, identity, cancel/history and rejection without mutation
- Review: merged PR #20
- Issue refinement: [TODO: confirm drafting of the AC in section A]
- Design and responsibility discussion: [TODO]
- Debugging or integration: [TODO]
- Documentation or team support: Stage 6 record (this file); checklist update ([3ca30be](https://github.com/DaRealElementus/ST1-ASS3/commit/3ca30be))

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

Commit count measures how often someone saved and pushed, not the value of what they changed. One person can make many tiny or trivial commits (checklist ticks, typo fixes, automated updates). Our own history has dozens of automated "auto-update assignment countdown" commits that contain no engineering work at all. Someone else can make one commit that carries a whole tested feature. A lot of important work, such as reviewing diffs, refining acceptance criteria, debugging with a teammate or designing tests, produces few or no commits under that person's name. Contribution should be judged on traceable evidence: issues, diffs, tests, reviews and the person's ability to explain the work.

## L Stage 6 formative questions

1. What is version control?

A system that records changes to files over time as commits. You can see who changed what and why, go back to earlier versions, and let several people work on the same code safely by branching and merging.

2. Why is a feature branch useful?

It keeps work-in-progress for one issue away from `main`, so `main` stays working. The change can be reviewed as one focused diff in a PR, and it can be abandoned or reworked without affecting teammates.

3. What makes a commit a good engineering commit?

It is small and focused on one logical change. It leaves the code in a working, tested state and contains no unrelated edits or generated files. Its clear imperative message says what behaviour changed and links to an issue where possible.

4. What is a pull request?

A request to merge a branch into another (usually `main`). It shows the diff, the linked issue and the commits, and gives a place for review comments, requested changes, approval and the merge record.

5. What is the purpose of code review?

To have another person check the actual diff against the requirement before it is merged. They look at correctness, responsibilities, test quality, scope and readability, so defects are caught early and knowledge spreads across the team.

6. What does a Git diff show?

The exact lines added, removed or changed between two versions (commits, branches or working tree), file by file, with surrounding context.

7. What is a Definition of Done?

An agreed checklist that work must meet before it counts as complete. For us: the acceptance criteria are met, tests are added and the full suite passes, another member has reviewed it, it is merged to `main`, the issue is closed and the evidence is recorded.

8. What is the appropriate role of GitHub Copilot in pull-request review?

A second opinion after the human reviewer has formed their own view from the diff. Its suggestions are checked against the real code, requirements and tests, then accepted, modified or rejected with a reason. It never replaces human judgement or approval.

9. Why should individual contribution not be judged only by commit count?

Commit count ignores size, quality and kind of work. Reviews, issue writing, test design, debugging and pairing are real contributions that often leave few commits, while trivial or automated commits inflate the count (see K).

10. What is the Stage 6 engineering rule?

Every change follows the cycle: update `main` → issue → focused branch → code + tests → inspect diff → commit/push → PR → human review by another member → respond and retest → approve → merge → everyone pulls `main` → run the full suite and record the SHA.

## M Completion and handover

- Starting SHA: `f924876bedf303d4fb4362fd1a104ee2cd9f7482`
- Final Stage 6 code SHA: `ec4d4a2c053481d075c1a86cb5c3841ad37cc72f` (merge of PR #21; later commits up to `6d5f8bd` only change `README.md`/`checklist.md`) [TODO: confirm after running the tests]
- Test command: `python -m pytest`
- Working directory: `project/`
- Observed result: [TODO: run on the SHA above and record the exact output, e.g. "N passed"]
- PR and another-member reviewer: [#1](https://github.com/DaRealElementus/ST1-ASS3/pull/1) (RW), [#19](https://github.com/DaRealElementus/ST1-ASS3/pull/19) (AR), [#20](https://github.com/DaRealElementus/ST1-ASS3/pull/20) (ND), [#21](https://github.com/DaRealElementus/ST1-ASS3/pull/21) (AL)
- Unresolved issue or none: no issue for FR-06/07; issue #4 has no AC in its body; human reviews are brief (section G); no Copilot comparison because no member used Copilot (sections H/I); per-member pull and integrated test run not recorded
- Stage 7 handover status: unresolved work (see above)
- Final submitted SHA if later than tested SHA: [TODO: the commit containing this record; evidence-only difference]

- [x] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [x] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
