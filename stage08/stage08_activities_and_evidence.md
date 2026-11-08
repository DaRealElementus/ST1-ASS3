# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements

For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.

- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: [complete]

### A.2 Build a debugging record

Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [complete]

### A.3 Test defect or product defect

A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [complete]

### A.4 Refactoring smell hunt

Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [complete]

### A.5 Traceback and hypothesis ranking

Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]

### A.6 Exit question

Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [complete]

Classification responses (1–5, each with reason): [complete]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [complete]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete]

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: [complete]
- Baseline test command / working directory / observed result / evidence: [complete]
- Clean preparation SHA if a record-only commit followed Stage 7: [complete]
- Branch and preparer / how teammates obtained this branch: [complete]
- Downloaded tool version, source SHA256 and --check outcome: [complete]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete]
- Prepared faulty-state commit SHA: [complete]
- Preparation or recovery issues and resolution, if any: [complete]
- Initial prepared full-suite command / result / key failures: [complete]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [complete]
- Expected behaviour and requirement: [complete]
- Minimal synthetic reproduction steps: [complete]
- Meaningful failing test path/name and exact relevant failure: [complete]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: after an appointment is cancelled, `find_appointment` raises `LookupError: Appointment not found`. Cancelling the same appointment a second time also raises `LookupError` instead of the expected `ValueError`.
- Expected behaviour and requirement: a cancelled appointment stays in the store and can still be found, with status `CANCELLED` (FR-06/07, AC-06.1). A repeat cancel should be rejected with `ValueError` because the appointment is already cancelled (AC-05.x).
- Minimal synthetic reproduction steps: register patient `P1` and practitioner `D1`; book `A1` for `P1` with `D1` at 2026-10-01 09:00; cancel `A1`; call `find_appointment('A1')`, then call `cancel_appointment('A1')` again.
- Meaningful failing test path/name and exact relevant failure:
  - `project/tests/test_services.py::test_find_appointment_returns_cancelled_record`: `LookupError: Appointment not found` at `smartcare/services.py:134`, raised from `clinic.appointments.find_appointment('A1')` after the cancel.
  - `project/tests/test_services.py::test_cancel_retains_appointment_and_guards_repeat`: `LookupError: Appointment not found` at `smartcare/services.py:134` on the second `cancel_appointment('A1')`, where the test expects `ValueError`.
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: The hypothesis in E was confirmed. `SmartCareDataStore.find_appointment` only returned an appointment if its ID matched **and** `appointment.status.value != "cancelled"`. A cancelled appointment was still stored (it stays in `list_appointments()`), but the lookup skipped it and returned `None`, so `AppointmentService.find_appointment` raised `LookupError`. The repeat cancel failed for the same reason: `cancel_appointment` could not find the record, so it raised `LookupError` instead of reaching the "already cancelled" `ValueError`. Removing only that condition made both F8-02 tests pass, which confirms it was the cause.
- Smallest justified fix / diff / why other behaviour is preserved: Remove the second half of the `and` comparison. we do not need to filter out the cancelled appointments
- Repair SHA / focused verification result: 5e0bab2ed1011eab2a3d7b2c2b712b0158834bae. Focused: `py -3.13 -m pytest -q tests/test_services.py -k "returns_cancelled_record or guards_repeat"` in `project/`: 2 passed, 57 deselected.

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry

Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

### F8-02 human entry

Likely cause and why plausible: I think cancelled appointments can't be found because the `if` in `find_appointment` skips appointments with a cancelled status, so it returns `None` and the service says "Appointment not found". This fits both failing tests, because both fail only after `A1` has been cancelled.
Evidence intended to inspect / competing explanation / discriminating check: Inspect the `if` condition in `SmartCareDataStore.find_appointment` (`project/smartcare/data_store.py`, line 94: `and appointment.status.value != "cancelled"`). Competing explanation: `cancel_appointment` deletes the record instead of keeping it. Discriminating check: `test_cancel_retains_appointment_and_guards_repeat` already shows `list_appointments()` still contains the cancelled appointment, so it is stored but not found. Removing only the status condition should make both F8-02 tests pass.
Member and saved sequence/time or commit showing this preceded consultation: ND, 2026-11-08, written after reproducing the failures (section G, F8-02 before repair) and before any Copilot use. ND asked a teammate in person for help reading the `if` condition before writing this.

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review

Actual prompt / output reference and member: [complete]

1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review

Actual prompt / output reference and member: ND, 2026-11-08, GitHub Copilot Chat in VS Code, Ask mode (read-only). The prompt gave the observed behaviour, expected behaviour (FR-06/07, AC-06.1, AC-05.x), the reproduction steps, both failing tests, ND's hypothesis from E and the original faulty `find_appointment` code from `cd6393a`, and asked for three ranked causes with discriminating checks, with no rewrite and no invented requirements. Screenshot of the prompt and reply kept by ND outside the repository. The prompt was run after the repair had been merged; the original code was quoted in the prompt so the review applied to the faulty version.

1. Most likely: `find_appointment` filters out cancelled records, so `A1` is skipped, `None` is returned and the service raises `LookupError`; the repeat cancel fails at the lookup before reaching the domain's already-cancelled check. Check: call `data_store.find_appointment('A1')` directly after cancelling; `None` while `list_appointments()` still contains `A1` confirms it. Observed evidence: `test_cancel_retains_appointment_and_guards_repeat` shows `A1` is still in `list_appointments()`, and removing only the status condition (`5e0bab2`) made both F8-02 tests pass. **Correct. Accept**: it matches the cause found and the repair that fixed it.
2. Less likely: the stored ID does not match the lookup ID, for example because of extra whitespace. Check: compare `repr()` of each stored ID with `repr('A1')`. Observed evidence: the appointment is booked and looked up as `'A1'`, both booking and lookup strip whitespace, `test_find_appointment_trims_padded_id` passes, and the same lookup works before the cancel. **Wrong for this fault. Reject**: the lookup only fails after the status changes, so the ID comparison is not the cause.
3. Least likely: the lookup and the list use different store instances or different loaded code. Check: compare `id(service.data_store)` with the store used for the list, and inspect the loaded method. Observed evidence: each test builds one `SmartCareDataStore` in `make_clinic()` and passes the same object to every service, and changing only `SmartCareDataStore.find_appointment` changed the result. **Wrong. Reject**: one shared store is used, and the edited method is the one that runs.

Final human conclusion and comparison with initial hypothesis: Copilot's top-ranked cause is the same as ND's hypothesis in E, so the initial hypothesis stands. Copilot added a sharper discriminating check (calling the store's `find_appointment` directly), which separates "not stored" from "stored but not found" more directly than the test alone. Causes 2 and 3 were rejected using existing test evidence. Copilot also pointed out that the workspace code no longer has the filter, which is correct because the repair was already merged. No Copilot code was used.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | `cd6393a2ca5e25571f3eb4f1b99fc64769a03e21` (`fix/F8-02-retained-history-lookup`, no changes) | `py -3.13 -m pytest -q` and `py -3.13 -m pytest -q tests/test_services.py -k "returns_cancelled_record or guards_repeat"`, in `project/` | Full suite: 8 failed, 172 passed. Focused: 2 failed (`test_find_appointment_returns_cancelled_record`, `test_cancel_retains_appointment_and_guards_repeat`), both `LookupError: Appointment not found`. The other 6 failures are F8-01. |
| F8-02 after repair | `5e0bab2ed1011eab2a3d7b2c2b712b0158834bae` | `cd project` `py -m pytest`; rechecked by ND on `Stage-8-Debugging` at `cd66ffa` (merge of PR #32, same code as `5e0bab2`) with `py -3.13 -m pytest -q` and the focused command in D | Full suite: 6 failed, 174 passed. All 6 failures are F8-01 (practitioner conflict); none from F8-02. Focused F8-02 tests: 2 passed. |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
