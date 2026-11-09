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

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: <!-- response -->

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| | | | | |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: <!-- response -->

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
| Automated service workflow | | | | |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

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

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
