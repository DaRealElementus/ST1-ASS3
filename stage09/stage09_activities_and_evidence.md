# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: RW, AR, AL, ND (all UG); repository https://github.com/DaRealElementus/ST1-ASS3
Members and responsibilities:
- AL (DaRealElementus): `appointment_sort_key` (#10, PR #29); `select_appointments` with RW (#11, PRs #36/#40/#41)
- RW (Proffo1): `select_appointments` status filter with AL (#11, PR #40); `run_menu` cancel and list options with `parse_status` (#13, PR #33)
- AR (expertkaos): `AppointmentService.list_practitioner_appointments` and its service tests (#12, PR #34); `tests/test_workflows.py` with ND (#15); `project/README.md` (#16)
- ND (BilyFlowers): `run_menu` loop with register/find/book options (#13, PR #30); `tests/test_queries.py` `select_appointments` tests (#14, PR #42); `tests/test_workflows.py` with AR (#15); this record

Stage 8 integrated SHA, command, working directory and actual result: `53167113bcdc7c999560478d055e57f7dc4a5c73` (merge of PR #39, Stage 8 into `main`; `main` already included `select_appointments` from PR #41). `py -3.13 -m pytest -q` in `project/`: 211 passed, 0 failed (Python 3.13.16, pytest 8.3.5).

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | | |
| Appointment history | | |
| Temporary menu choice | | |
| Practitioner specialty | | |
| Debug print output | | |
| Appointment status | | |

What is intentionally lost on exit? <!-- response -->

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | | | | |
| select_appointments | | | | |
| Service listing | | | | |
| Console | | | | |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: <!-- response -->

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | | |
| Service prints/reads the menu | | |
| Query sorts its source in place | | |
| Store prints Appointment saved | | |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: <!-- response -->

Score-example prediction and explanation of passing the named key: <!-- response -->

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: <!-- response -->

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: **Written after implementation, not before.** The team designed Stage 9 through the issue split (#10–#16) and the PRs listed in H; this table was recorded afterwards from the merged code (common SHA `9c57409`) and its tests, before the Copilot review in E was added to this record. Interface decisions: (1) `select_appointments` takes the appointment list, practitioner ID and optional status as explicit parameters instead of reading the store, so it stays pure and can be tested with plain lists. (2) The service, not the query, owns validation: it checks the status type and looks up the practitioner, then passes `data_store.list_appointments()` to the query. (3) Status is an `AppointmentStatus` enum below the console; only the console turns typed text into the enum (`parse_status`), and blank means "all" (`None`). (4) The query returns the stored `Appointment` objects, not copies, so a listed appointment is the same object that find and cancel act on.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-01 practitioner isolation | Session appointments for D1 and D2 | `select_appointments` (query) keeps only appointments whose practitioner ID matches | Only that practitioner's appointments | `test_select_returns_only_that_practitioner`; `test_listing_only_includes_the_requested_practitioner` |
| QRY-02 status filter, default all | Practitioner ID; status `None` or an `AppointmentStatus` | `select_appointments` (query) | `None`: every status; a status: only that status | `test_select_without_status_returns_every_status_sorted`; `test_select_filters_by_each_status` |
| QRY-03, FP-03 ordering by named key | Unsorted appointments, including equal times | `appointment_sort_key` used by `select_appointments` | Sorted by date/time, then appointment ID | AL's 5 key tests; tie-break check in `test_select_without_status_returns_every_status_sorted` |
| QRY-04 service listing errors | Unknown ID; blank/`None` ID; non-enum status; known practitioner with no appointments | `AppointmentService.list_practitioner_appointments` (service), with `required_text` in the store | Unknown: `LookupError`; blank or invalid status: `ValueError`; known with none: `[]` | `test_listing_*` in `tests/test_services.py` (17 cases) |
| FP-01/02 purity | Source list passed in | `select_appointments` builds a new local list and returns `sorted(...)`; no store, globals, input or output | New list; source order and appointment fields unchanged; same result on repeat calls | `test_select_does_not_change_source_list_or_appointments`; `test_select_repeated_calls_give_the_same_result`; `test_select_returns_a_new_list_even_when_already_sorted` |
| FR-01 register; FR-02/03 find patient/practitioner | Typed IDs, names, specialty | Console handlers call `PatientService`/`PractitionerService` | Registered object printed; duplicate or blank ID: `ValueError`; unknown ID: `LookupError` | UI-01 and UI-02 runs in D |
| FR-04/05 book and conflict | Typed IDs and `YYYY-MM-DD HH:MM` | Console `parse_date_time`, then `book_appointment` (service) | Booked; same practitioner and time: `ValueError`; different practitioner at that time: allowed; bad or impossible date: `ValueError` | UI-01/UI-02 in D; `test_service_workflow` |
| FR-06/07/08 cancel, history, find | Typed appointment ID | Console calls `cancel_appointment`/`find_appointment` (service); status rule in `Appointment.cancel` (domain) | Cancel keeps the record as CANCELLED; it can still be found and listed; repeat cancel: `ValueError` | UI-01 in D; `test_service_workflow`; `test_listing_keeps_cancelled_history` |
| FR-09, UI-01 list in the menu | Practitioner ID; typed status text | Console `parse_status` converts text to the enum, then calls the service | Matching appointments printed in order, or "No appointments found." | UI-01 in D; `test_list_shows_empty_message_for_known_practitioner`; `test_status_text_ignores_case_and_spaces` |
| UI-02 invalid-input recovery | Unknown menu choice; any rejected input | `run_menu` (console) catches `ValueError`/`LookupError`, prints `Error: ...` and shows the menu again; end of input exits cleanly | Message shown, menu continues, stored data unchanged | UI-02 run in D; `test_invalid_input_recovery`; the two end-of-input tests |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: **Empty, unknown and invalid** are different cases. Empty means a known practitioner who has no matching appointments: this is a valid answer, so the service returns `[]` and the console prints "No appointments found." Unknown means a well-formed ID that is not registered: the service raises `LookupError`. Invalid means the input itself is wrong (a blank or `None` ID, or a status that is not an `AppointmentStatus`): `ValueError`. **Enum conversion** happens only in the console: `parse_status` trims and lower-cases the text, returns `None` for blank, converts known text such as "Cancelled" to `AppointmentStatus.CANCELLED`, and raises `ValueError` listing the allowed values otherwise; the service also rejects any non-enum status. **Object identity**: the store, service and query all hand back the same stored `Appointment` objects, so the appointment shown in a listing is the one that was booked and cancelled; tests check this with `is`. **Error handling**: the domain, store and services raise `ValueError` or `LookupError` and never print; only `run_menu` catches them and prints a message. **Unchanged state on rejection**: services validate and look up before adding anything, so a rejected action stores nothing and changes no status; the tests compare snapshots before and after, and the UI-02 run shows the same records after every rejected input.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| QRY-03, FP-03 named sort key | `smartcare/queries.py` `appointment_sort_key` | Key is `(date_time, appointment_id)`; earlier time sorts first; equal times are ordered by ID (case-sensitive); building the key does not change the appointment | 5 passed (`tests/test_queries.py`, AL) | PR #29 |
| QRY-01 practitioner isolation | `select_appointments` | `test_select_returns_only_that_practitioner`: only D2's appointment is returned and its practitioner is the D2 object | Passed | PR #42 (ND) |
| QRY-02 default all statuses | `select_appointments` | `test_select_without_status_returns_every_status_sorted`: scheduled, cancelled and completed D1 appointments are all returned, in order `A1, A4, A2, A3` | Passed | PR #42 |
| QRY-02 every enum status | `select_appointments` | `test_select_filters_by_each_status` (3 cases): each status returns only its matching IDs, and every result has that status | 3 passed | PR #42 |
| QRY-03 equal-time ID tie-break, named-key reuse | `select_appointments` uses `appointment_sort_key` | Source lists A4 before A1 at 09:00, so only the time-then-ID key returns A1 first | Passed | PR #42 |
| FP-01 new list, same objects | `select_appointments` | `test_select_returns_the_stored_objects`: each result is one of the source objects (`is`), not a copy; `test_select_returns_a_new_list_even_when_already_sorted`: equal to an already-sorted source but `is not` the source | 2 passed | PR #42 |
| FP-01 source unchanged, repeated calls | `select_appointments` | `test_select_does_not_change_source_list_or_appointments`: source order and every appointment's ID, practitioner, time and status are unchanged after two calls; `test_select_repeated_calls_give_the_same_result`: two calls are equal, separate lists | 2 passed | PR #42 |
| FP-01/02 empty results | `select_appointments` | `test_select_empty_source_returns_empty_list` (new empty list); `test_select_no_matches_returns_empty_list` (unknown practitioner, or status with no matches) | 2 passed | PR #42 |
| QRY-04 service listing | `smartcare/services.py` `list_practitioner_appointments` | 17 `test_listing_*` cases in `tests/test_services.py`: default all statuses in order, practitioner isolation, each status filter, retained cancelled history, known practitioner with no matches returns `[]`, padded ID normalised, new list of stored objects, unknown practitioner `LookupError` without mutation, blank/`None` ID `ValueError`, invalid status `ValueError` | 17 passed | PR #34 (AR) |

Run evidence: on `feature/test-queries` at `0d009a4` (PR #42), `py -3.13 -m pytest -q tests/test_queries.py` in `project/`: 16 passed; full suite: 222 passed. On `main` at `5316711`, `py -3.13 -m pytest -q tests/test_services.py -k listing`: 17 passed.

Purity explanation from code inspection, including absence of hidden state and I/O: `select_appointments` takes everything it needs as parameters (the appointment list, the practitioner ID and the optional status). It reads no global store or module-level state, does not print or read input, and does not change its inputs: it appends matches to a new local list and returns `sorted(...)` of that list, which is a new list, so the caller's list order is untouched. It does not change any appointment; it only reads `practitioner.practitioner_id`, `status`, `date_time` and `appointment_id`. The same inputs therefore always give the same result.
What the tests do and do not establish: They show that the query and service return the right appointments, in the right order, as a new list of the stored objects, that inputs are not changed, and that the service rejects unknown, blank and invalid inputs. The query tests were also checked by temporarily introducing 10 deliberate faults into a copy of `select_appointments` (for example ignoring the practitioner, ignoring the status, sorting by time only, sorting the source in place, returning copies, cancelling a match); each fault made at least one test fail. They do not establish: behaviour with very large lists; case-insensitive practitioner IDs (the pure query compares IDs exactly, and only the service trims spaces); or any behaviour beyond one session, since data is session-only.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | `py -3.13 main.py --interactive` in `project/` at `5316711`, inputs in order: register patient P1; register practitioners D1 (General) and D2 (Dental); book A1 P1/D1 2026-10-01 09:00; book A2 P1/D1 same time; book A2 P1/D2 same time; find A1; cancel A1; find A1; book A3 P1/D1 2026-10-01 09:00; list D1 (blank status); list D1 `scheduled`; list D1 `cancelled`; exit `0` | Registration and bookings succeed; same practitioner at the same time is rejected; a different practitioner at that time is allowed; cancel keeps A1 findable as cancelled; the freed slot can be rebooked; listing shows all statuses by default and filters by status; exit ends the session | All as expected. A2 with D1 rejected: "Practitioner already has a SCHEDULED appointment at this time", then A2 with D2 booked. After cancel, find A1 shows `cancelled`. A3 booked in A1's freed slot. List D1 (all) shows A1 cancelled and A3 scheduled; `scheduled` shows only A3; `cancelled` shows only A1. Exit printed "Session-only data: records are lost on exit." | Inputs and transcript saved by ND outside the repository; re-runnable with the inputs listed |
| UI-02 invalid-input recovery | `py -3.13 main.py --interactive` in `project/` at `5316711`, inputs in order: register P1, D1; book A1 P1/D1 2026-10-01 09:00; choice `9`; choice `abc`; register P1 again; register patient with blank ID; find patient P9; find patient with blank ID; book A2 with unknown patient P9; book A2 with date `01/10/2026 10am`; book A2 with date `2026-02-30 10:00`; cancel A9; cancel A1; cancel A1 again; list D1 with status `booked`; list unknown practitioner D9; then find A1; list D1 (blank); book A2 P1/D1 2026-10-01 10:00; exit `0` | Each invalid input shows a clear message and returns to the menu with no change to stored records; valid actions afterwards still succeed | All as expected. Unknown choices: "Unknown option; choose a number from the menu." Duplicate ID: "Patient ID already exists". Blank IDs: "... cannot be blank". Unknown IDs: "Patient not found" / "Appointment not found" / "Practitioner not found". Malformed date: "Use date/time format YYYY-MM-DD HH:MM". Impossible date: "Invalid calendar date/time". Repeat cancel: "Only SCHEDULED appointments may be cancelled". Invalid status: "Status must be one of scheduled, cancelled, completed, or blank for all". State check after errors: find A1 and list D1 show only A1 (cancelled), so nothing was added or changed by the rejected inputs; A2 then booked successfully. | Inputs and transcript saved by ND outside the repository; re-runnable with the inputs listed |
| Automated service workflow | `tests/test_workflows.py` (AR, PR #44), 7 tests: `test_full_menu_session` (UI-01), `test_invalid_input_recovery` (UI-02), `test_list_shows_empty_message_for_known_practitioner`, `test_status_text_ignores_case_and_spaces`, two end-of-input exit tests, and `test_service_workflow` | `test_service_workflow`: book A1 (P1/D1 09:00); A2 for P2/D1 at 09:00 rejected with nothing stored; A3 for P2/D2 at 09:00 allowed; cancel A1 keeps the same object as CANCELLED; repeat cancel rejected; A1 still found; A4 rebooks D1 09:00; D1 listing is `[A1, A4]`, D1 SCHEDULED is `[A4]`, D2 is `[A3]` | `py -3.13 -m pytest -q tests/test_workflows.py` in `project/` at `897d169`: 7 passed. The session tests feed scripted input to `run_menu()` and check the printed output; `store.find_appointment('A2') is None` checks the rejected booking left no record | PR #44 |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: Not before. This Copilot review was run by ND on 2026-11-09, after the Stage 9 code was merged (common SHA `9c57409`). The implementation was designed and reviewed by members through the issues and PRs in H; section B was written after implementation (see B).
Actual prompt/context supplied: ND, GitHub Copilot Chat in VS Code (Agent mode; it was not allowed to edit files). Files attached: `queries.py`, `services.py`, `console.py`, `test_queries.py`, `test_workflows.py`. The prompt listed QRY-01–04, FP-01–03, UI-01–02 and the layer responsibilities, asked for up to 5 findings each with code location, requirement, severity and checkable evidence, asked whether any responsibility was in the wrong layer, and said not to rewrite code, add features or invent requirements. Screenshots of the prompt and reply kept by ND outside the repository.
Actual response: "No findings against the listed requirements in the reviewed files." Copilot said the query filters by practitioner and optional status and returns a new sorted list using `appointment_sort_key`; the service validates status and looks up the practitioner first, with blank IDs rejected by the store's shared text validation; the console implements the menu and error recovery; and no responsibility is in the wrong layer. It added a caveat: it tried to run the tests but `pytest` was not installed in its selected Python environment, so its review was based on reading the source and tests, not on a test run.

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| `select_appointments` filters by practitioner and optional status and returns a new list sorted by `appointment_sort_key` | `queries.py` `select_appointments`; `tests/test_queries.py` (16 tests) | – (no defect) | **Accept.** Matches the code and is backed by tests, including 10 deliberate faults that were each caught (C) | No change | `py -3.13 -m pytest -q tests/test_queries.py`: 16 passed |
| Service checks status, looks up the practitioner, and blank IDs are rejected by the store's `required_text` | `services.py` `list_practitioner_appointments`; `data_store.py` `find_practitioner` calls `required_text` | – (no defect) | **Accept.** Confirmed by reading both methods and by AR's listing tests for unknown, blank and invalid-status cases | No change | `py -3.13 -m pytest -q tests/test_services.py -k listing`: 17 passed |
| Console implements the full menu and recovers from invalid input | `console.py` `run_menu`; `tests/test_workflows.py` | – (no defect) | **Accept.** Confirmed by the UI-01 and UI-02 runs in D and by the workflow tests | No change | `tests/test_workflows.py`: 7 passed; UI-01/UI-02 runs in D |
| No responsibility in the wrong layer | All five files | – | **Accept.** See the responsibility check below | No change | Code inspection by ND |
| "No findings" overall | `queries.py` line 27 `result: list = []` (loose type hint, should be `list[Appointment]`); `services.py` `list_practitioner_appointments` docstring still begins "Stage 9:" | Low | **Modify.** Copilot missed these low-severity code-quality nits, which AL's Stage 12 inspection also found. They do not affect behaviour or any requirement | No change: accepted as debt after feature freeze (Stage 12 record, sections E/G) | Checked by ND with `grep` on current `main` |
| Caveat: tests not run by Copilot | Copilot's environment had no `pytest` | – | **Accept the caveat.** Copilot's review is inspection only, so it is not evidence that the tests pass | No change | ND ran the full suite separately: `py -3.13 -m pytest -q` in `project/`: 229 passed at `9c57409` (H) |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: The domain (`Appointment`, `AppointmentStatus`) owns status rules, such as only a SCHEDULED appointment can be cancelled. The store (`SmartCareDataStore`) only holds and looks up records and validates IDs with `required_text`. The service (`list_practitioner_appointments`) coordinates: it checks the status argument, looks up the practitioner (raising `LookupError` if absent) and passes the store's list to the query. The query (`select_appointments`) is pure: it only filters and sorts what it is given and returns a new list. Only the console reads input and prints: `run_menu` and its handlers turn typed text into arguments (including `parse_status` for the status enum), call the services, and catch `ValueError`/`LookupError` to print an error and return to the menu.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? <!-- response -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- response -->
3. How can a new list reuse Appointment objects safely? <!-- response -->
4. Why use a named key, and what breaks equal-time ties? <!-- response -->
5. How do default and explicit status filters differ? <!-- response -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- response -->
7. Which console errors recover, and how is unchanged state checked? <!-- response -->
8. What is data integrity for registered participants, conflicts and history? <!-- response -->
9. What is Copilot's review role, and who verifies findings? <!-- response -->
10. How do pure functions and OOP responsibilities work together? <!-- response -->

## H. Review, completion and common handover

Issues and bounded branches (all issues now closed):
- [#10](https://github.com/DaRealElementus/ST1-ASS3/issues/10) `appointment_sort_key`: `Query/SortAppointmentKeys` (PR #29)
- [#11](https://github.com/DaRealElementus/ST1-ASS3/issues/11) `select_appointments`: `Query/select-appointments-pract` (PR #36) and `Query/select-appointments-status` (PR #40), both into `Query/select-appointments`, then PR #41 into `main`
- [#12](https://github.com/DaRealElementus/ST1-ASS3/issues/12) `list_practitioner_appointments`: `feature/list-practitioner-appointments` (PR #34)
- [#13](https://github.com/DaRealElementus/ST1-ASS3/issues/13) `run_menu`: `feature/run-menu-register-find-book` (PR #30), with RW's `run_menu_actions_list_cancel_list` (PR #33) merged into it first
- [#14](https://github.com/DaRealElementus/ST1-ASS3/issues/14) `tests/test_queries.py`: `feature/test-queries` (PR #42)
- [#15](https://github.com/DaRealElementus/ST1-ASS3/issues/15) `tests/test_workflows.py`: `tests/workflows` (PR #44)
- [#16](https://github.com/DaRealElementus/ST1-ASS3/issues/16) `project/README.md`: `docs/project-readme` (PR #45)

PR/diff and another-member human reviewer: every Stage 9 PR was merged by a member other than its author: [#29](https://github.com/DaRealElementus/ST1-ASS3/pull/29) (AL, merged by RW), [#30](https://github.com/DaRealElementus/ST1-ASS3/pull/30) (ND, reviewed and merged by AL), [#33](https://github.com/DaRealElementus/ST1-ASS3/pull/33) (RW, reviewed by ND, merged by AL), [#34](https://github.com/DaRealElementus/ST1-ASS3/pull/34) (AR, merged by AL), [#36](https://github.com/DaRealElementus/ST1-ASS3/pull/36) (AL, merged by RW), [#40](https://github.com/DaRealElementus/ST1-ASS3/pull/40) (RW, merged by AL), [#41](https://github.com/DaRealElementus/ST1-ASS3/pull/41) (AL, merged by AR), [#42](https://github.com/DaRealElementus/ST1-ASS3/pull/42) (ND, merged by AL), [#43](https://github.com/DaRealElementus/ST1-ASS3/pull/43) (ND, merged by AL), [#44](https://github.com/DaRealElementus/ST1-ASS3/pull/44) (AR, merged by RW), [#45](https://github.com/DaRealElementus/ST1-ASS3/pull/45) (AR, merged by AL). Only #30 and #33 have a formal GitHub review; the others were merged without a recorded review.
Review responses and Copilot comparison: On #30, AL requested changes: "Add RW commits before merging, keep on same branch". RW's PR #33 was then merged into the branch and #30 was merged. On #33, ND requested changes: option 8 ended the session because the branch did not yet have `list_practitioner_appointments` (PR #34), and the checklist ticks were premature. AL merged #33 two minutes later without those changes. The option 8 problem was resolved on `main` once PR #34 and PR #41 were merged; ND confirmed option 8 works in the UI-01 run in D. No Copilot comparison was recorded for Stage 9 reviews (see E).
Integrated common Stage 9 SHA: `9c57409a192be6fe979e144ff6f75f654974bdb4` (`main` after PR #44, the last Stage 9 code change), the same SHA the Stage 12 record uses as its tested code SHA. Later commits change documentation and records only; `git diff 9c57409 897d169 -- project/smartcare project/main.py project/tests` is empty.
Full regression command, working directory, actual count/result and evidence: `py -3.13 -m pytest -q` in `project/` (Python 3.13.16, pytest 8.3.5): 229 passed, 0 failed at `9c57409` and again at `897d169` (current `main`), run by ND.
README run instructions and scope/limitations: [`project/README.md`](../project/README.md) (PR #45): Setup, Running SmartCare (menu usage and demo sequence), Testing, Code layout, Error handling, and Scope and limitations sections.
Unresolved issues and support/action: The common Stage 9 SHA has not been tagged yet (checklist: "common Stage 9 SHA recorded and protected (tag it)", owner AR). Sections A, B, E, F and G of this record still need the team's own responses. Most Stage 9 PRs were merged without a formal GitHub review.
UG common candidate / PG future branch plan: <!-- complete -->

- [x] Query contracts, purity, new lists and named-key ordering verified.
- [x] Service empty/unknown/invalid cases and cancellation history verified.
- [x] Every console command and invalid-input recovery demonstrated.
- [x] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [x] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
