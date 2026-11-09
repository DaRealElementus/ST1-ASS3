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

- Symptom / observed behaviour: At the prepared faulty baseline (HEAD `cd6393a`), the `!=` practitioner-ID predicate reports a conflict between different practitioners at the same scheduled time and fails to report one for the same practitioner. The in-memory reproduction of `test_services.py::test_different_practitioners_can_share_a_time` produced `ValueError: Practitioner already has a SCHEDULED appointment at this time` while booking D2 after D1 at 2026-10-01 09:00.
- Expected behaviour and requirement: A scheduled appointment conflicts only when its practitioner ID and exact date/time both match the proposed booking (AC-04.x). A different practitioner may be booked at the same time; a second booking for the same practitioner and time must be rejected.
- Minimal synthetic reproduction steps: Register synthetic patients P1 and P2 and practitioners D1 and D2. Book A1 for P1 with D1 at 2026-10-01 09:00, then book A2 for P2 with D2 at that same time. The faulty predicate incorrectly rejects A2. Repeat with D1 for A2: the faulty predicate incorrectly accepts the double-booking.
- Meaningful failing test path/name and exact relevant failure: `project/tests/test_services.py::test_different_practitioners_can_share_a_time` fails under the prepared `!=` predicate with `ValueError: Practitioner already has a SCHEDULED appointment at this time`. This failure was reproduced by running the test function with the faulty predicate injected in memory; the working tree already contains the one-operator repair.
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: Confirmed. `project/smartcare/data_store.py`, `SmartCareDataStore.has_practitioner_conflict`, used `appointment.practitioner.practitioner_id != practitioner_id`. That matches different practitioner IDs and misses equal IDs. The committed baseline has `!=`; the current working-tree diff changes only that operator to `==`.
- Smallest justified fix / diff / why other behaviour is preserved: Change `!=` to `==` in the practitioner-ID condition. The appointment exclusion, exact date/time match, and scheduled-status checks are unchanged, so update exclusions, time boundaries, and cancelled/completed appointment handling retain their prior behavior.
- Repair SHA / focused verification result: No repair commit SHA yet; the repair is uncommitted on top of HEAD `cd6393a2ca5e25571f3eb4f1b99fc64769a03e21`. From `project/`, `python -m pytest -q tests/test_services.py::test_different_practitioners_can_share_a_time tests/test_starter.py::test_conflict_rule_and_different_practitioner` passed: `2 passed in 0.02s`.

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [complete]
- Expected behaviour and requirement: [complete]
- Minimal synthetic reproduction steps: [complete]
- Meaningful failing test path/name and exact relevant failure: [complete]
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry

Likely cause and why plausible: The practitioner-ID comparison in `has_practitioner_conflict` may be inverted (`!=` instead of `==`). A conflict requires the existing scheduled appointment to belong to the same practitioner, so `!=` would incorrectly flag a different practitioner's booking and miss a same-practitioner double-booking.
Evidence intended to inspect / competing explanation / discriminating check: Inspect the practitioner-ID, exact date/time, scheduled-status, and excluded-appointment conditions in `has_practitioner_conflict`, then compare them with AC-04.x. Run `test_different_practitioners_can_share_a_time` and `test_conflict_rule_and_different_practitioner`; reproduce one same-practitioner/same-time booking that must be rejected and one different-practitioner/same-time booking that must be allowed. A date/time or status-filter defect is a competing explanation, distinguished by checking those predicates and varying only the practitioner ID.
Member and saved sequence/time or commit showing this preceded consultation: RW; hypothesis supplied in the initial user request before Copilot review in this conversation. No separate saved sequence/time or commit identifier was provided.

### F8-02 human entry

Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review

Actual prompt / output reference and member: RW requested the F8-01 Copilot review in this conversation. Review prompt: “Diagnose F8-01 without rewriting unrelated code or inventing requirements. Observed behaviour: the prepared baseline rejects simultaneous bookings by different practitioners and permits the same practitioner to be double-booked. Expected behaviour: reject only a second scheduled appointment for the same practitioner at the exact same date/time; allow different practitioners at that time. Minimal reproduction: book D1 at 2026-10-01 09:00, then try D2 at the same time and D1 again at that time. Meaningful test: `project/tests/test_services.py::test_different_practitioners_can_share_a_time`, with `project/tests/test_starter.py::test_conflict_rule_and_different_practitioner` as a companion. Human hypothesis: the practitioner-ID comparison in `has_practitioner_conflict` is inverted (`!=` instead of `==`). Inspect the controlling code and rank three causes, giving a discriminating check and evidence for each; recommend only the smallest supported change.” Output: the ranked review below, in this Copilot response and recorded here; no separate exported transcript or artifact exists.

1. Ranked suggestion: Inverted practitioner-ID comparison is the root cause. Evidence check: inspect `SmartCareDataStore.has_practitioner_conflict` and exercise same-time bookings with D1 and D2. Observed evidence: the prepared baseline compares `appointment.practitioner.practitioner_id != practitioner_id`; injecting that predicate into `test_different_practitioners_can_share_a_time` raises `ValueError: Practitioner already has a SCHEDULED appointment at this time`. The current one-operator `==` working-tree change passes both named focused tests (`2 passed`). Correct; accept. It explains both false conflicts for different IDs and missed conflicts for equal IDs, and changing only the operator preserves the date/time, scheduled-status, and exclusion checks.
2. Ranked suggestion: The service may pass the wrong practitioner ID or fail to normalize the requested ID. Evidence check: inspect `AppointmentService.book_appointment` and the practitioner lookup. Observed evidence: booking looks up the requested ID, then passes the registered practitioner's canonical `practitioner_id` to the conflict check; `find_practitioner` validates and trims IDs. Wrong argument/normalization is not supported as the root cause; reject. The mismatch is inside the store predicate.
3. Ranked suggestion: The date/time, appointment-status, exclusion, or appointment-list conditions may create the conflict mismatch. Evidence check: inspect every remaining conjunct and compare bookings varying only practitioner ID. Observed evidence: the predicate uses exact datetime equality and scheduled status, and excludes the requested appointment ID; none explains the opposite outcomes by practitioner identity. These conditions are consistent with the stated requirement and are unchanged by the fix. Reject as the cause; retain them.
Final human conclusion and comparison with initial hypothesis: The evidence confirms RW's initial `!=` versus `==` hypothesis; no inspected alternative explains the reproduced failure as directly. Copilot recommends accepting the diagnosis and the one-operator fix. RW's separate post-review accept/modify/reject decision has not been provided, so this record does not attribute that decision to RW.

### F8-02 Copilot review

Actual prompt / output reference and member: [complete]

1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
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
