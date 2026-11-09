# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: RW, AR, AL, ND; tutorial [TODO: tutorial code]; repository https://github.com/DaRealElementus/ST1-ASS3
Members and UG/PG applicability: Alex Larkings (AL, [DaRealElementus](https://github.com/DaRealElementus)), Rhys Watson (RW, [Proffo1](https://github.com/Proffo1)), Andrew Rainey (AR, [expertkaos](https://github.com/expertkaos)), Nemika De Zoysa (ND, [BilyFlowers](https://github.com/BilyFlowers)). All four are UG. This is a UG-only release of the common scope; PG Stages 10 and 11 do not apply.

Code SHA used for all Stage 12 testing below: `9c57409a192be6fe979e144ff6f75f654974bdb4` (`main` after PR #44 and the README tracker update), shortened to `9c57409`. Base link for versioned evidence: `https://github.com/DaRealElementus/ST1-ASS3/tree/9c57409`.


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare A3 UG common release v1.0. Requirements baseline: SmartCare A3 2026 revision 2 (FR-01–09, QRY-01–04, FP-01–03, UI-01–02, NFR-01; FR-10 retired).
Common starting SHA / branch / applicable members: `9c57409` on `main`, which includes every Stage 6–9 merge up to PR #44 (workflow tests). Applies to AL, RW, AR and ND. Stage 12 documentation work is on branch `docs/stage12-release-docs` (AL).
PG starting SHA / branch / applicable members or not applicable: Not applicable. All members are UG and no PG branch exists.
Working-state review and approved integration: On `9c57409`, `git status` shows a clean tree apart from ignored caches (`__pycache__`, `.pytest_cache`, `.vscode`). No open PRs remain. All Stage 9 issues (#10–#15) are closed. Only #16 (`project/README.md`, AR) was open. It is being updated on a separate branch, and this Stage 12 branch leaves that file untouched so the two merge cleanly. The Stage 10/11 PG templates had been deleted in commit `285c666`. This branch restores them byte-for-byte unchanged, as the handout requires for UG-only groups.
Protected common candidate and PG differences: The common candidate is the code at `9c57409`. There is no PG extension, so there are no PG differences. After this SHA, only documentation and record files change; `project/smartcare/`, `project/main.py` and `project/tests/` stay as they are.
Feature freeze / owner / verifier: Feature freeze is at `9c57409`: no new features, only release blockers fixed through a reviewed PR. Owner AL (who is doing Stage 12). Verifier: all members agree the freeze (`checklist.md` section 5, "Feature freeze agreed": All). The Stage 12 PR reviewer is ND ("Stage 12 record complete" reviewer). [TODO: record the date the freeze was agreed.]


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: **Do not release (yet).** Passing tests only show that the behaviour we tested works. A marker or new developer cannot reproduce the build if setup is incomplete. An unreviewed dependency is an unknown supply-chain and licence risk. An undocumented limitation means users could rely on behaviour that is not there. All three gaps are cheap to close: finish the README, review or remove the dependency, and document the limitation. After those fixes and a recheck, the right decision becomes "Release with documented limitations". It is not "Release with conditions", because the conditions are about release evidence, not later work.

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

All locations are at `9c57409` unless stated. All rows are common/UG scope except where marked PG.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | `test_cancel_retains_appointment_and_guards_repeat`, `test_find_appointment_returns_cancelled_record`, F8-02 regression tests, listing of cancelled records, console demo steps 5–8 | `project/tests/test_services.py`, `project/tests/test_regressions.py`, `project/tests/test_workflows.py` @ `9c57409`; PRs #1, #32, #44 | AL (Stage 12 check); originally RW (PR #1) | Yes | None |
| Architecture responsibilities are appropriate | Code inspection (section E): domain validates and changes state, store holds collections, services coordinate, queries are pure, only the console does I/O | `project/smartcare/*.py` @ `9c57409`; `project/README.md` "Structure and responsibilities" | AL | Yes | Minor layout nits only (E, H) |
| Rescheduling is safe — PG only | Not applicable: UG-only group | – | – | N/A | None |
| AI use is responsible — common recheck / PG assurance | `ai_usage_log.md`; Copilot decisions in Stage 6–9 records; Stage 8 F8-01/F8-02 reviews; Stage 12 Claude Code disclosure (E) | Root `ai_usage_log.md`, `stage08/` F section | AL | Partly | Stage 7 H and Stage 9 E Copilot tables are still blank. Fill them from real evidence or state honestly that none is available (H) |
| System is maintainable | 229 tests across 6 files; docstrings on every public function; small, focused modules | `project/tests/`, `project/smartcare/` | AL | Yes | Debt items in G |
| FR-01–03 register/find and validation | `test_domain.py` (113 tests: blank/whitespace/`None`/non-string fields), registration and lookup tests in `test_services.py` (AC-01.2, AC-02.1/02.2) | `project/tests/test_domain.py`, `project/tests/test_services.py`; PRs #19, #20, #23, #25 | AL | Yes | None |
| FR-04–05 booking/conflict rules | Booking and conflict tests (AC-03.x, AC-04.x) including different-practitioner same time, rebooking freed slot, non-mutation on rejection; F8-01 regressions | `test_services.py`, `test_regressions.py`, `test_starter.py`; PRs #25, #37 | AL | Yes | Exact-time rule only, by design (G) |
| FR-06–08 cancellation/history/find | AC-05.1–05.3, AC-06.1 tests; repeat cancel `ValueError`; unknown `LookupError`; blank `ValueError` | `test_services.py`, `test_regressions.py`; PRs #1, #27, #32 | AL | Yes | None |
| FR-09 and QRY/FP listing/filter/order/purity | 16 query tests (purity, new list, identity, tie-break, each status, empty); 17 `test_listing_*` service tests (QRY-04) | `project/tests/test_queries.py`, `test_services.py`; PRs #29, #34, #41, #42 | AL | Yes | None |
| UI full console sequence and error recovery | `test_full_menu_session`, `test_invalid_input_recovery`, EOF tests; manual demo run in D | `project/tests/test_workflows.py`; PRs #30, #33, #44 | AL | Yes | None |
| Session-only scope / FR-10 retired | No file/database code; exit message "Session-only data: records are lost on exit."; README limitation | `project/smartcare/data_store.py`, `console.py`, `project/README.md` ("Data exists only in this session") | AL | Yes | None |
| PG RES and assurance integration | Not applicable: UG-only group | – | – | N/A | None |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Windows 11, Python 3.14.6, pytest 8.3.5 (AL's machine; Python 3.13 is not installed, see note) | `project/`: `python -m pytest -q` | `9c57409` | 229 passed, 0 failed | Per file: test_domain 113, test_queries 16, test_regressions 9, test_services 76, test_starter 8, test_workflows 7 |
| Complete PG if applicable | Not applicable (UG-only) | – | – | – | – |
| Affected focused checks after correction | No code correction was made in Stage 12 (H) | – | – | Not run: nothing to recheck | – |
| Full integrated recheck | Fresh `git clone` of `main` into a temporary folder, new venv, Python 3.14.6, pytest 8.3.5 installed from `requirements-dev.txt` | `project/`: `python -m pip install -r requirements-dev.txt`, `python -m pytest -q`, `python main.py` | `9c57409` | 229 passed; demo printed `A1: P1 with DR1, 2026-10-01 09:00, scheduled` and the session-only notice | Run by AL on 2026-11-09; temporary clone deleted afterwards |
Prior assertions preserved / reviewed test diff: The count grew from 8 starter tests (Stage 6) to 211 at the Stage 8 integration (`5316711`) and 229 now. `test_starter.py` is unchanged and still has its 8 tests. No test was deleted or weakened in Stage 12. The Stage 12 branch has no changes under `project/tests/`.
Remaining failure / limitation: None failing. Python note: the teaching baseline is Python 3.13. Earlier stages were verified with `py -3.13` (Stage 8/9 records), but the Stage 12 runs above used 3.14.6 because 3.13 is not installed on AL's machine. [TODO: a member with Python 3.13 reruns `py -3.13 -m pytest -q` in `project/` at the final SHA and records the result here.]


## D Console and end to end demonstration

All console steps: `python main.py --interactive` in `project/` at `9c57409`, one fresh process, run by AL on 2026-11-09. Inputs, one per prompt: `1 P1 "Pat Example"`, `2 D1 "Dr One" General`, `2 D2 "Dr Two" Dental`, `3 P1`, `4 D1`, `4 D2`, `5 A1 P1 D1 2026-10-01 09:00`, `5 A2 P1 D1 2026-10-01 09:00`, `5 A2 P1 D2 2026-10-01 09:00`, `7 A1`, `6 A1`, `7 A1`, `5 A3 P1 D1 2026-10-01 09:00`, `8 D1 (blank)`, `8 D1 scheduled`, `8 D1 cancelled`, `9`, `5 A4 P1 D1 01/10/2026`, `8 D1 booked`, `8 D9 (blank)`, `0`. Rerun this sequence to reproduce the results; "Demo step n" below refers to its order.

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | Reception staff book and manage appointments for patients with practitioners; clinic needs no double-booking and kept history | Overview problem statement | Explained from the requirements baseline | Overview handout |
| Register and find Patient and two Practitioners | 1 P1 "Pat Example"; 2 D1 "Dr One" General; 2 D2 "Dr Two" Dental; 3 P1; 4 D1; 4 D2 | FR-01–03 | `Registered patient P1: Pat Example`, both practitioners registered, each find printed the stored record | Demo inputs 1–6; `test_full_menu_session` |
| Valid booking | 5 A1 P1 D1 `2026-10-01 09:00` | FR-04 | `Booked A1: P1 with D1, 2026-10-01 09:00, scheduled` | Demo input 7 |
| Same practitioner exact-time conflict rejected | 5 A2 P1 D1 `2026-10-01 09:00` | FR-05, AC-04.x | `Error: Practitioner already has a SCHEDULED appointment at this time`; menu continued | Demo input 8 |
| Different practitioner same time allowed | 5 A2 P1 D2 `2026-10-01 09:00` | AC-04.x | `Booked A2: P1 with D2, 2026-10-01 09:00, scheduled` | Demo input 9 |
| Cancel SCHEDULED and retain/find CANCELLED object | 7 A1; 6 A1 | FR-06–08, AC-05.1, AC-06.1 | `Cancelled A1: ... cancelled`, then find showed `A1: P1 with D1, 2026-10-01 09:00, cancelled` | Demo inputs 10–11 |
| Invalid/repeated cancellation rejected | 7 A1 again | AC-05.3 | `Error: Only SCHEDULED appointments may be cancelled` | Demo input 12 |
| Default all-status listing | 5 A3 P1 D1 same time (freed slot); 8 D1 blank status | FR-09, QRY-02 | A3 booked; list showed A1 cancelled then A3 scheduled | Demo inputs 13–14 |
| Explicit filtering / empty vs unknown / deterministic order | 8 D1 `scheduled`; 8 D1 `cancelled`; 8 D9 | QRY-01–04 | `scheduled` showed only A3; `cancelled` showed only A1; D9 gave `Error: Practitioner not found`. A known practitioner with no matches prints `No appointments found.` (`test_list_shows_empty_message_for_known_practitioner`). Equal-time order is by ID (A1 before A3) | Demo inputs 15–16, 20; `test_queries.py` tie-break test |
| Invalid date/status/menu/lookup recovery and continued operation | `9`; 5 A4 P1 D1 `01/10/2026`; 8 D1 `booked` | UI-02, NFR-01 | `Unknown option; choose a number from the menu.`, `Error: Use date/time format YYYY-MM-DD HH:MM`, `Error: Status must be one of scheduled, cancelled, completed, or blank for all`; menu kept running each time and A4 was not created | Demo inputs 17–19; `test_invalid_input_recovery` |
| Session-only limitation and normal exit | `0` | FR-10 retired | `Session-only data: records are lost on exit.` and the process ended | Demo input 21 |
| One meaningful requirement-linked pytest test explained | `tests/test_regressions.py` F8-02 lookup test | FR-07, AC-06.1 | After cancelling A1, `store.find_appointment('A1') is booked`. It fails if cancelled records are filtered out (the Stage 8 fault), and `is` proves the same stored object is returned, not a copy | `project/tests/test_regressions.py`; Stage 8 record G |
| Architecture and one actual AI decision / known limitation | Domain/store/service/query/console split; AI decision: AL rejected ID-based `__eq__`/`__hash__` (could hide "replacement object" bugs) and kept only `__repr__`/`__str__` | Architecture, responsible AI | Explained from code and `ai_usage_log.md` Entry 1; limitation: exact-time conflicts only | `ai_usage_log.md`; PR #2 |
| PG reschedule identity/participants/time and no-op | Not applicable (UG) | – | – | – |
| PG conflict/invalid status/failure non-mutation | Not applicable (UG) | – | – | – |
| PG old slot / current lookup/list ordering / assurance risks | Not applicable (UG) | – | – | – |
Stable demo owner / fresh process / command: [TODO: confirm who runs the live demo]. Use a fresh process with `python main.py --interactive` from `project/`, following the input sequence at the top of this section.
PG demonstrations through service/tests or not applicable: Not applicable: UG-only group.


## E Final code quality and AI review

Inspection by AL on `9c57409`, file by file in `project/smartcare/` and `project/main.py`.

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | `domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py` | No finding. Only `console.py` calls `input`/`print`. `select_appointments` takes explicit inputs and returns `sorted(...)` of a new list. Cancellation is `Appointment.cancel`. Conflict coordination is in the service and store | No change |
| PascalCase and snake_case naming | All modules | Classes are PascalCase and functions snake_case. Minor: the loop variable `a` in `select_appointments` (`queries.py`) is a one-letter name | Accepted as debt (G); no change after feature freeze |
| Useful type hints and meaningful docstrings | All modules | Hints and docstrings on every public function. Two findings: (1) `main.py` `main()` docstring still says it reports "the intentionally incomplete interactive menu", but the menu is now complete; (2) `queries.py` uses a loose `result: list = []` instead of `list[Appointment]` | Accepted as debt (G); no behaviour impact |
| Four-space indentation and imports/layout | All modules | Four-space indentation and grouped imports throughout. Two layout nits: `services.py` has one blank line (PEP 8 wants two) before `class AppointmentService`, and `main.py` has none before `if __name__ == '__main__':` | Accepted as debt (G) |
| Focused methods / duplication / dead or commented code | `main.py`, `console.py` | `main.py` still catches `NotImplementedError` from `run_menu`, which can no longer happen. That handler is dead code from the starter. Console handlers are short and single-purpose. No commented-out code | Accepted as debt (G); removing it is a code change after freeze, not a blocker |
| Globals / leakage / unnecessary inheritance or frameworks | All modules | No finding. The only module-level constant is `MENU` (text). Each `run_menu`/`run_demo` builds its own store. Store dictionaries are private (`_patients` etc.) and lists are returned as new containers. No inheritance and no frameworks | No change |
| No SQLite/persistence/repository ABCs/speculative features | All modules | No finding. There are no imports of `sqlite3`, `json`, `pickle` or `abc`, and no rescheduling code | No change |
| Synthetic data / secrets / dependencies / provenance | Whole repo (`git ls-files`, `git grep`) | No finding. Only synthetic IDs/names (P1, D1, "Alex Example"). No credentials (`git grep` for password/token/secret/api key only matches guidance text). One dependency, `pytest==8.3.5`, which is the course baseline. The runtime uses only the standard library | No change |
| Significant common Copilot contributions and human verification | `ai_usage_log.md`; Stage 6–9 records; Stage 8 F section | Stage 8 has full Copilot reviews with ranked causes and human conclusions (F8-01 RW, F8-02 ND). Gap: the Stage 7 H and Stage 9 E Copilot decision tables are still blank | Action in H: owners fill them from real evidence or write "no significant Copilot use" |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | – | Not applicable (UG) | – |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| Claude Code (AL): "ID-based `__eq__`/`__hash__` on domain classes could hide a replacement-object bug; add only `__repr__`/`__str__`" | AC-02.1 identity (`is`), `domain.py` | AL read `services.py`/`domain.py`, then ran the suite (8 passed) and a manual print check | Accept: matches the Stage 6 "same stored object" rule | `__repr__`/`__str__` added in PR #2; identity tests still use `is` |
| Copilot (RW, Stage 8): F8-01 root cause is `!=` instead of `==` in `has_practitioner_conflict` | FR-05, AC-04.x, `data_store.py` | Inspected each condition; focused tests failed before and passed after a one-operator change | Accept: matched RW's own earlier hypothesis | Fixed in `c4c8d04` (PR #37) |
| Copilot (ND, Stage 8): F8-02 alternative causes "ID whitespace mismatch" and "different store instances" | FR-07, AC-06.1 | Checked the trim tests and the single shared store in `make_clinic()` | Reject both: the evidence showed only the status filter mattered | Removed only the status condition (`5e0bab2`, PR #32) |
| Claude Code (AL, Stage 12): drafted this record and the root README group index from the repo, the test runs and the inspection above | Release documentation only | AL [TODO: confirm you have read and checked every row]. Every result above comes from commands actually run; human decisions are left as TODO | [TODO: Accept/Modify after AL's review] | No code changed; see `ai_usage_log.md` Entry 2 |
Access route or approved equivalent / limitations: GitHub Copilot (course-nominated) in VS Code for RW, ND and AR. Claude Code in VS Code for AL, disclosed in `ai_usage_log.md`. [TODO: confirm with the tutor that Claude Code counts as an approved equivalent route, or note the tutor's response.]
Available AI evidence and missing evidence honestly disclosed: Available: `ai_usage_log.md` Entry 1–2; Stage 8 F section prompts and ranked outputs (no exported transcripts, as that record states). Missing: Stage 7 H and Stage 9 E Copilot tables are blank; RW's post-review decision for F8-01 is not recorded (Stage 8 F says so).


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | `project/README.md` | AR (README reviewer, `checklist.md` section 5) | Gap at `9c57409`: the file still has the Stage 6 starter text ("Stage 6 TODOs ... raise NotImplementedError"). It is being updated on a separate branch (#16, AR). Recheck after that merge |
| Out-of-scope capabilities and known limitations | `project/README.md` | AR (README reviewer, `checklist.md` section 5) | At `9c57409` it covers session-only data, FR-10 retired, the date format and no age/duration/patient-conflict/past-date rules. Recheck that the update also lists the limitations in G |
| Confirmed teaching Python version and dependency installation | `project/README.md`; root `README.md` | AL | Present at `9c57409`: Python 3.13, pytest 8.3.5, `python -m pip install -r requirements-dev.txt` |
| Working directory / demo / interactive / test commands | `project/README.md`; root `README.md` | AL | `python main.py` and `python -m pytest` are documented from `project/`. `--interactive` is not mentioned at `9c57409` [TODO: confirm the #16 update adds it] |
| Repository structure and architecture responsibilities | `project/README.md` | AR (README reviewer, `checklist.md` section 5) | Describes domain/store/services at `9c57409` but not `queries.py`, the console menu or the test files. Recheck after the #16 merge |
| Responsible AI summary / synthetic-data rule | `project/README.md`; root `README.md` | AL | Synthetic-data rule present in both. Root README names Copilot as the assistant. [TODO: confirm the #16 update adds a short AI summary] |
| Release label/version and SHA links | Root `README.md` group index; section K | AL | Root index now has the tested SHA. Final submitted SHA [TODO after merge] |
Root README index and project/README verified: Root group index filled in (members, cohorts, repo, latest stage, tested SHA, test command/result). The links to the Stage 10/11 PG records were broken because those templates had been deleted; this branch restores them. [TODO: final SHA after merge.]
Fresh clone or extracted ZIP / candidate identity: A fresh `git clone` of `main` gave HEAD `9c57409a192be6fe979e144ff6f75f654974bdb4`, which matches the tested SHA. [TODO: RW and AR fresh-clone checks of the final SHA (checklist), and the extracted ZIP comparison (K).]
Verifier and clean environment / actual version: AL, new `venv` inside the clone, Python 3.14.6, pytest 8.3.5 installed from `requirements-dev.txt`. Independent fresh-clone checks per `checklist.md` section 5: RW (first) and AR (second). [TODO: RW's and AR's environment, Python version and result, ideally on Python 3.13.]
Setup/run/test commands and observed results: `python -m pip install -r requirements-dev.txt` installed successfully; `python -m pytest -q` gave 229 passed; `python main.py` printed the A1 line and the session-only notice. After the clone, `git status --ignored` showed only `.venv`, `.pytest_cache` and `__pycache__` (all ignored).
Missing local file or setup gap / remedy and recheck: Gap 1: `project/README.md` is still the starter text at `9c57409`. It is being updated on a separate branch (#16); recheck the rows above once that is merged. Gap 2: the PG template links were broken; the templates are restored unchanged. Gap 3: the machine used has Python 3.14 rather than 3.13 (C). No file was missing from the clone.


## G Known limitations debt and release notes

Delivered features: Register and find patients and practitioners with validation. Book appointments with same-practitioner exact-time conflict rejection. Cancel while keeping history, and find cancelled appointments. List a practitioner's appointments (all statuses or one), ordered by date/time then ID, through a pure query. A full interactive menu that recovers from invalid input. A runnable demo.
Important fixes: F8-01: the conflict check used `!=` instead of `==`, which blocked different practitioners and allowed double-booking (PR #37). F8-02: lookup skipped cancelled appointments, so history could not be found and repeat cancels raised the wrong error (PR #32). Both are guarded by `tests/test_regressions.py`.
Architecture/quality improvements: Stage 8 refactor made the store `find_*` methods consistent (validation, docstrings, O(1) dictionary lookup) (PR #38). `__repr__`/`__str__` on domain classes (PR #2). The tests grew from 8 to 229 and cover domain, services, regressions, queries and console workflows.
Known limitations: Session-only data. Naive local minute-precision time. Only exact-time conflicts for the same practitioner. No duration/overlap or patient double-booking checks. Case-sensitive IDs. No menu option to complete an appointment. No rescheduling, editing or deleting. Not production software (see below).
AI-assisted development note: The team used GitHub Copilot (and Claude Code for AL) for suggestions, debugging reviews, test ideas and documentation drafts. Every significant suggestion was checked by a person against requirements, diffs and tests, then accepted, modified or rejected, and recorded in the stage records and `ai_usage_log.md`. AI did not approve any merge or release decision.

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Stale `main.py` docstring and dead `except NotImplementedError` handler | Misleading for a new reader; no runtime effect | Low | Update the docstring and remove the handler in a small reviewed PR | [TODO: team] Proposed accept: cosmetic, and changing code after freeze needs a full retest |
| PEP 8 blank-line nits (`services.py` before `AppointmentService`, `main.py` before `__main__` guard) | Style only | Low | Fix with the item above | [TODO: team] Proposed accept |
| `queries.py`: `result: list` hint and loop variable `a` | Slightly weaker readability/type checking | Low | Use `list[Appointment]` and `appointment` | [TODO: team] Proposed accept |
| Only exact-time conflicts (no durations) | Overlapping appointments of different lengths are possible | Medium (for real use) | Add durations and an overlap rule if requirements change | Proposed accept: this is the specified rule (AC-04.x), so it is a scope limit, not a defect |
| No COMPLETED action in the menu | COMPLETED can only be set through the domain in tests | Low | Add a "complete appointment" option if required | Proposed accept: not in the UG requirements |
| Stage 7 H / Stage 9 E Copilot tables blank | Incomplete AI evidence | Medium (assessment) | Owners fill them with real evidence or a no-use statement | **Not accepted:** must be resolved before submission (H) |
Session-only synthetic data and minute-precision local time: All data is held in memory for one session and lost on exit (FR-10 retired). Only synthetic records may be used. Times are naive local `datetime` values entered as `YYYY-MM-DD HH:MM`, so seconds and time zones are not represented.
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: None of these exist and none are in scope. There is no login or role check, no patient portal, no reminders, no billing or insurance and no clinical decision support or AI features in the app.
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: Single user, single process, in-memory, and not tested with large data. Listing is a linear scan. No time zone or daylight-saving policy. No logging, monitoring or deployment. A text-only console with no accessibility review and no undo.
Difference between accepted scope limit and unresolved required behaviour: An accepted scope limit is something the requirements deliberately leave out, such as persistence (FR-10 retired) or duration-based conflicts. It is documented and needs no fix. Unresolved required behaviour would be a requirement in scope that does not work, for example if a cancelled appointment could not be found (FR-07). That would be a release blocker. We found no unresolved required behaviour: every in-scope requirement has passing evidence (B).
PG assurance residual risks / owner / status or not applicable: Not applicable: UG-only group.


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| README reproducibility (Stage 12 F) | `project/README.md` still described the Stage 6 starter ("Stage 6 TODOs ... raise NotImplementedError") | Medium: misleading setup/scope for markers | AR: update on a separate branch (#16) | Not on this branch | [TODO: reread after merge and rerun its commands] | None once merged |
| UG must retain PG templates unchanged | `stage10_pg/` and `stage11_pg/` were deleted in `285c666`; the root README links were broken | Medium: submission package rule | AL: restore the originals | Restored files, byte-identical to `b8a7f0d` | `diff` against `b8a7f0d`: identical | None |
| Responsible-AI evidence complete | Stage 7 H and Stage 9 E Copilot tables, and several Stage 6/8/9 `[complete]`/blank fields, are unfilled | Medium: assessment evidence, not code | [TODO: stage record owners per checklist (Stage 7 RW, Stage 8 RW, Stage 9 ND)] | Records only | Re-read each record | Missing evidence must be disclosed, not invented |
| Code quality nits (E) | Stale docstring, dead handler, blank lines, loose hint | Low | [TODO: team decision: accept as debt or fix via PR] | None in Stage 12 | – | Listed in G |
Justified no-change conclusion if no defect found: No functional defect was found. All 229 tests pass on a fresh clone; the full console sequence and every invalid path behave as required (D); the code inspection found only cosmetic issues (E). So no code was changed after feature freeze, and the tested code SHA stays `9c57409`.
Release blockers still open / status: [TODO: confirm] The incomplete Stage 7/8/9 record fields (row 3) are the only open item. They do not block the software, but they do block the submission package.


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: Issue #16; Stage 12 PR [TODO: PR link once opened] from `docs/stage12-release-docs` into `main`. It changes only `README.md`, `stage12/` and `ai_usage_log.md`, and restores `stage10_pg/`/`stage11_pg/`. Code reviewed and tested: `9c57409`.
Independent reviewer / feedback / response: ND (Stage 12 record reviewer, `checklist.md` section 5); AR reviews the README rows. [TODO: ND's feedback and AL's response.]
Integration commit / full recheck: [TODO: merge commit SHA; rerun `python -m pytest -q` in `project/` on it and record the count. It should be 229, since no code changes]
Tracked and untracked file inspection / cleanliness: `git ls-files` lists only the root docs, `.github/workflows`, `.gitignore`, `project/` source and tests, and the stage records. `git status --ignored` shows only ignored caches and `.vscode`. After this branch there are no untracked files. The two README workflows in `.github/workflows/` are kept for history but disabled on GitHub (`gh workflow list`), and their frozen countdown/tracker blocks were removed from the root README.
Secrets/staff material/caches/tool-metadata exclusion check: `git grep` finds no credentials. No Stage 8 utility, `.stage8_*` folders or backups are tracked (also covered by `.gitignore`). No staff reference solutions. `__pycache__`, `.pytest_cache`, `.venv` and `.vscode` are ignored. `Githubbasics.md` is our own team guide, not staff material.
Candidate recovery plan / known-good SHA: Known-good code SHA is `9c57409`. If a later commit breaks anything, revert it with `git revert` (never force-push). Alternatively, build the ZIP from `9c57409` with `git archive`, since later commits are documentation only. [TODO: optionally tag the candidate, e.g. `git tag v1.0-ug <sha>` and `git push origin v1.0-ug`.]
Named substantive contributions: AL: repo setup, `cancel_appointment` (#1), `__repr__`/`__str__` (#2), conflict/booking tests (#25), F8-02 pair, refactor (#38), `appointment_sort_key` (#29), `select_appointments` with RW, Stage 12. RW: `find_patient` (#19), domain validation tests (#23), F8-01 diagnosis and fix (#37), `select_appointments` status filter (#40), menu cancel/list/`parse_status` (#33). AR: `find_practitioner` (#20), domain state tests (#24), `list_practitioner_appointments` and tests (#34), workflow tests (#44), README issue #16. ND: issues and acceptance criteria, `test_services.py` (#21), find/non-mutation tests (#27), F8-02 diagnosis (#32/#35), menu loop (#30), query tests (#42), Stage 6/9 records (#43). [TODO: each member confirms their own line.]


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: [TODO: team decision. The evidence above supports READY WITH DOCUMENTED LIMITATIONS once the Stage 7/8/9 record gaps (H) are closed.]
Approver / date / rationale and evidence: All members: AL, RW, AR, ND (`checklist.md` section 5, "Human release decision recorded": All). [TODO: date and rationale in the team's words.]
What risks remain / conditions / owners: [TODO: confirm. Suggested: the record gaps (owners per checklist); the Python 3.13 recheck (a member with 3.13); the cosmetic debt items in G (accepted)]
Can the team explain the system: [TODO: confirm after the viva rehearsal (checklist section 6)]
Can a change be recovered: Yes. Every change went through a branch and PR with no force-pushes. The known-good SHA `9c57409` is recorded, and `git revert` or `git archive <sha>` recovers it (I).
Common decision / PG decision where different: Common decision only; PG not applicable.


## K Final tested release SHA

Exact common tested SHA: `9c57409a192be6fe979e144ff6f75f654974bdb4` (229 passed, C).
Exact PG tested SHA or not applicable: Not applicable (UG-only).
Final submitted SHA / repository URL: [TODO: SHA of `main` after the Stage 12 PR is merged]; https://github.com/DaRealElementus/ST1-ASS3
Evidence-only later commit and difference explanation: The Stage 12 merge changes only documentation and records. `git diff --stat 9c57409 <final SHA> -- project/smartcare project/main.py project/tests project/requirements-dev.txt` should print nothing. [TODO: run this on the final SHA and confirm it is empty.] The GitHub Actions countdown and issue-tracker workflows have been manually disabled, so no automated commits land on `main` after the tested SHA.
Executable changes after testing and re-verification: None planned. If any code change is made, rerun the full suite and update the tested SHA above.
Source ZIP name / SHA correspondence / extracted comparison: [TODO: e.g. `git archive --format=zip -o SmartCare_A3_<final-short-sha>.zip <final SHA>` from the repo root. This includes the root `README.md` and `.gitignore` and excludes `.git`. Then extract it, run `python -m pytest -q` in `project/`, and record the name, SHA and result here.]


## L Submission package verification

- [x] Feature freeze and scoped requirements traced.
- [x] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete. (Code and dependency checks done; AI record gaps remain, H.)
- [ ] Root README and project/README reproduced by another verifier.
- [x] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: [TODO: Canvas assessment item name/route]
Deadline/timezone: 2026-11-09 23:59 AEDT (12:59 UTC), from the group's (now disabled) countdown workflow. [TODO: confirm against Canvas.]
Repository access arrangement: The repository is public at https://github.com/DaRealElementus/ST1-ASS3. [TODO: confirm with the tutor that no extra staff access is needed.]
Mixed-candidate upload arrangement: Not applicable: UG-only group, one candidate.
Oral/video recording/accessibility arrangements: [TODO]
Remaining administration or release dependency: [TODO: e.g. Stage 7/8/9 record gaps, ZIP build, group reflection and peer forms]


## M Formative questions

1. What is a release candidate? A specific, identified version of the software (here a commit SHA) that the team proposes to release. It is tested and reviewed as it is; if it passes, that exact version is released. If anything changes, it becomes a new candidate that needs testing again.

2. What is feature freeze and why is it used? A point after which no new features are added and only fixes for release blockers are allowed. It stops the target moving, so testing, review and documentation are about the version that will actually ship.

3. What is regression testing in a release context? Rerunning the whole accumulated test suite (and the key demo paths) on the release candidate. It shows that recent changes did not break behaviour that used to work, such as our Stage 8 regression tests for F8-01 and F8-02.

4. What is a known limitation? Something the release does not do, or does only partly, that is written down so users and maintainers know. An example is session-only data. It is a deliberate or accepted gap, not a hidden bug.

5. What is technical debt? Design or code shortcuts that work now but make future changes harder or riskier, such as our dead `NotImplementedError` handler or loose type hints. Like financial debt, it should be recorded and "paid back" later.

6. What are release notes? A short summary for users and maintainers of what is in a release: new features, important fixes, improvements, known limitations and anything they need to do differently.

7. What is software maintenance? Everything done to software after release: fixing defects, adapting to new environments or requirements, improving structure, and keeping documentation and tests current. Most of a system's cost is usually here.

8. What is the purpose of the individual demonstration/viva? To show that each member understands and can explain the system, their own contribution and the team's decisions. This includes AI-assisted parts, which the person must be able to reason about without the tool.

9. What should the final responsible-AI check establish before release? That every significant AI contribution was recorded, checked by a person against requirements and tests, and accepted, modified or rejected for a stated reason. It should also confirm that no secrets or real data went to the tool, that no unreviewed dependencies were added, and that missing evidence is disclosed honestly.

10. What is the main course conclusion about AI and the role of the software engineer? AI can speed up writing code, tests and documents, but it does not own the outcome. The engineer still sets the requirements, judges whether suggestions are correct, verifies with evidence, and takes responsibility for what is released.


## N Reflection viva and handover

Strongest evidence SmartCare is ready: A fresh clone of `9c57409` installs from `requirements-dev.txt` and passes all 229 tests. The full README demo sequence, including every invalid input, behaves exactly as required. Both Stage 8 faults have targeted regression tests.
Weakest area: Completeness of the written evidence. Some Stage 7/8/9 record fields and Copilot decision tables are still blank, even though the code itself is well tested.
How AI use changed from Stage 1 to Stage 12: [TODO: each member, in their own words]
Start doing — engineering and AI use: [TODO: team]
Stop doing — engineering and AI use: [TODO: team]
Continue doing — engineering and AI use: [TODO: team]
What worked / caused rework / future delivery improvement: [TODO: team. Facts that may help: one issue per change and a PR review for every merge worked well; filling stage records late caused rework at Stage 12.]
One paragraph — If AI can write code why do we still need software engineers: [TODO: team, in your own words. Draft for editing:] AI tools can produce plausible code quickly, but plausible is not correct. In Stage 8, the AI reviews were only useful because a person had already reproduced the fault, written a hypothesis and had tests that could tell the causes apart; some suggested causes were wrong and had to be rejected using evidence. Engineers decide what the system should do, keep it inside its requirements (no speculative persistence or frameworks), check every change against tests and reviews, and are accountable for what ships. AI changes how fast we write things, not who is responsible for them.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | Clinic reception needs to book patients with practitioners without double-booking and keep cancelled history; stakeholders are reception staff, practitioners, patients and the clinic. Overview handout |
| Two requirements and acceptance criteria | FR-05 / AC-04.x: same practitioner, exact time, SCHEDULED, so reject; a different practitioner is allowed. FR-07 / AC-05.1: cancel keeps the same object, findable as CANCELLED. `stage06/` section A |
| Domain model and architecture | Patient, Practitioner, Appointment (+ AppointmentStatus) in `domain.py`; store, services, pure queries, console. `project/smartcare/` |
| Design trade-off | Pure `select_appointments` takes the list as input instead of reading the store: easier to test and reason about, at the cost of the service passing the data in |
| Meaningful test and its limits / 100 percent coverage | F8-02 regression test (D). It proves retained lookup and identity, but not large data, persistence or concurrency. 100% coverage would still not prove correctness: tests only check what we thought to assert |
| Diagnosed defect and verification | F8-01 `!=` vs `==` in `has_practitioner_conflict`: reproduced, hypothesis, one-operator fix, focused then full tests. `stage08/` C |
| Shared store and session-state/query responsibilities | One `SmartCareDataStore` per session is shared by all three services. Queries only read the list they are given |
| What would break if session-state lookup/query responsibilities changed? | If each service had its own store, a patient registered in one would not be found when booking. If the query sorted the source in place or read a global store, purity tests would fail and listing order could leak into other callers |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Cancel only needs one appointment's own state, so `Appointment.cancel` guards the transition. A conflict needs many appointments, so the service and store coordinate across the collection |
| FR-07 retained history test | `test_cancel_retains_appointment_and_guards_repeat` and the F8-02 regressions in `project/tests/` |
| Actual AI change rejected/modified or honestly accepted with verification | AL rejected ID-based `__eq__`/`__hash__`, accepted `__repr__`/`__str__` (`ai_usage_log.md` Entry 1, PR #2) |
| Unresolved limitation / future production work | Session-only data and exact-time conflicts. Production would need persistence, durations, auth, time zones (G) |
| Personal implementation contribution | [TODO: each member; see I "Named substantive contributions"] |
| Personal test/review/design/integration contribution | [TODO: each member] |
| PG agentic change and rescheduling verification | Not applicable (UG) |
| PG responsible-AI risk/remediation or supported no finding | Not applicable (UG) |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: Not undertaken.
Separate reflection / peer / common team viva evidence links and routing: Submitted separately through Canvas, not stored in this public repository. [TODO: confirm routing]
No further coding stage. Later corrections use the published assessment process.
