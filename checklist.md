# SmartCare A3 – Team Checklist

Team: **RW · AR · AL · ND**

Tick `[x]` when done. **Owner** does the work; **Reviewer** does the human PR review (always a different person). Swap owners if you need to, but keep the reviewer someone else and update this file.

> Public repo: never put student IDs, peer ratings, passwords/tokens, real patient data or private messages in here or any commit.

---

## 0. Setup (before any code)

| Done | Task | Owner |
|---|---|---|
| [x] | Form group in Canvas (same tutorial, by end of Week 9) | All |
| [x] | Record each member's cohort (UG/PG) in this file and root README | All |
| [x] | Create ONE public GitHub repo; starter contents at root (no nested `SmartCare_Starter/`) | AL |
| [x] | Add RW, AR, ND as collaborators | AL |
| [ ] | Each member clones with their own GitHub account | All |
| [ ] | Each member runs baseline: `cd project` → `python -m pip install -r requirements-dev.txt` → `python main.py` → `python -m pytest` (expect 8 passing) | All |
| [ ] | Confirm Copilot access/mode with tutor (approved equivalent route if it fails) | All |
| [ ] | Fill in root README group index (names, GitHub usernames, cohorts, repo URL) | ND |

**Cohorts:** RW: UG · AR: UG · AL: UG · ND: UG

**Every change follows the cycle:** update `main` → issue → focused branch → code + tests → inspect diff → commit/push → PR → human review by another member → respond + retest → approve → merge → **everyone pulls `main`** → run full suite and record SHA. No force-pushing.

---

## 1. Stage 6 – Team Development

Record: `stage06/stage06_activities_and_evidence.md`

| Done | Task | Owner | Reviewer |
|---|---|---|---|
| [ ] | Read Stage 6 handout, domain/store and supplied tests together | All | – |
| [ ] | Team agreement completed in record | All | – |
| [ ] | Draft GitHub issues + acceptance criteria for the 3 operations | ND | AL |
| [ ] | `PatientService.find_patient` (FR-02, AC-02.1/02.2) + tests | RW | AR |
| [ ] | `PractitionerService.find_practitioner` (FR-03) + tests | AR | ND |
| [x] | `AppointmentService.cancel_appointment` (FR-06/07, AC-05.1–05.3) + tests | AL | RW |
| [ ] | Create `tests/test_services.py` – lookup/errors, identity, cancel/history, rejection without mutation | ND | AL |
| [ ] | Human review notes written **before** Copilot comparison | Each reviewer | – |
| [ ] | Copilot use logged (prompt, output summary, check, Accept/Modify/Reject, reason, link) | Each owner | – |
| [ ] | All merged; everyone pulled; full suite passes; SHA recorded | RW | All |
| [ ] | Stage 6 record complete (own words, links to issues/PRs/tests/results) | ND | RW |

---

## 2. Stage 7 – Testing
Record: `stage07/stage07_activities_and_evidence.md`

| Done | Task | Owner | Reviewer |
|---|---|---|---|
| [ ] | Human TEST IDs and case design table (linked to FR/BR/AC) **before** Copilot | All | – |
| [ ] | Create `tests/test_domain.py` – Patient/Practitioner validation | RW | ND |
| [ ] | `tests/test_domain.py` – Appointment state, datetime rules, read-only identity | AR | RW |
| [ ] | Extend `test_services.py` – registration duplicates (AC-01.2), booking (AC-03.x), conflicts (AC-04.x) | AL | AR |
| [ ] | Extend `test_services.py` – find appointment (AC-06.1), non-mutation on rejection (NFR-01) | ND | AL |
| [ ] | Critique Copilot test candidates (what was accepted/modified/rejected and why) | All | – |
| [ ] | Production fixes **only** for evidenced defects (link failing test) | As found | Other |
| [ ] | Individual + full test runs recorded honestly (command, dir, result, SHA) | AR | – |
| [ ] | Stage 7 record complete | RW | AL |

---

## 3. Stage 8 – Debugging & Refactoring
Record: `stage08/stage08_activities_and_evidence.md`

| Done | Task | Owner | Reviewer |
|---|---|---|---|
| [ ] | Get Stage 8 utility from tutor; keep it **outside** the repo (`Stage_8_Assets/` sibling) | ND | – |
| [ ] | Clean debugging branch created from verified `main` | ND | – |
| [ ] | Human hypotheses recorded **before** Copilot | All | – |
| [ ] | Fault 1: reproduce symptom → diagnose → minimal repair in `data_store.py` | RW + AR (pair) | AL |
| [ ] | Fault 2: reproduce symptom → diagnose → minimal repair in `data_store.py` | AL + ND (pair) | RW |
| [ ] | Add `tests/test_regressions.py` covering both faults | AR | ND |
| [ ] | Focused + full tests run before and after repairs | ND | – |
| [ ] | One justified refactoring; full suite passes before and after | AL + RW (pair) | AR |
| [ ] | No utility/recovery files committed | All | – |
| [ ] | Stage 8 record complete (both causes explained) | RW | AL |

---

## 4. Stage 9 – Queries & Console Integration
Record: `stage09/stage09_activities_and_evidence.md`

| Done | Task | Owner | Reviewer |
|---|---|---|---|
| [ ] | Design query cases + console workflow **before** coding/Copilot | All | – |
| [ ] | `appointment_sort_key` (FP-03, QRY-03) | AL | RW |
| [ ] | `select_appointments` – pure, explicit inputs, new list (QRY-01/02/03, FP-01/02) | AL + RW (pair) | AR |
| [ ] | `AppointmentService.list_practitioner_appointments` – validation, LookupError/ValueError (QRY-04) | AR | AL |
| [ ] | `run_menu` in `console.py` – full menu, status text → enum, recovers from bad input (UI-01/02) | RW + ND | AL |
| [ ] | `tests/test_queries.py` – purity, sorting, filters, empty list, errors | ND | AL |
| [ ] | `tests/test_workflows.py` – end-to-end console session incl. invalid input recovery | AR + ND | RW |
| [ ] | Update `project/README.md` (setup, menu usage, demo sequence) | AR | ND |
| [ ] | Critique bounded Copilot advice | All | – |
| [ ] | All tests retained and passing; **common Stage 9 SHA recorded and protected** (tag it) | AR | All |
| [ ] | Stage 9 record complete | ND | AR |

---


---

## 5. Stage 12 – Final Release
Record: `stage12/stage12_activities_and_evidence.md`

| Done | Task | Owner | Reviewer |
|---|---|---|---|
| [ ] | Feature freeze agreed | All | – |
| [ ] | Finalise root `README.md` + `project/README.md` (incl. limitations) | ND | AR |
| [ ] | Fresh clone of candidate SHA; run full suite + `python main.py` demo | RW | – |
| [ ] | Second independent fresh-clone check | AR | – |
| [ ] | Quality inspection: code, AI decisions, records complete | AL | All |
| [ ] | Fix release blockers only (via PR + review) | As needed | Other |
| [ ] | Human release decision recorded | All | – |
| [ ] | Record full submitted SHA, tested SHA, protected common SHA (if mixed) | ND | AL |
| [ ] | Build source ZIP from exact commit (no `.git`, venvs, caches, secrets, peer forms, Stage 8 tool files) | RW | AL |
| [ ] | Check ZIP matches repo at that SHA | AR | – |
| [ ] | Repo is public/accessible to staff; submit ZIP + repo URL + SHAs | ND | All |
| [ ] | Stage 12 record complete | AR | ND |

---

## 6. Final assessments (outside Git)

| Done | Task | Owner |
|---|---|---|
| [ ] | Group Reflection Report (~500 words, six areas, real evidence) – draft | RW + AR |
| [ ] | Group Reflection Report – edit + submit | AL + ND |
| [ ] | Confidential self-and-peer form – **each submits privately** | RW |
| [ ] | Confidential self-and-peer form | AR |
| [ ] | Confidential self-and-peer form | AL |
| [ ] | Confidential self-and-peer form | ND |
| [ ] | Team viva prep: everyone can explain their own code and one other member's | All |
| [ ] | Team viva rehearsal (everyone gives substantive answers) | All |

---

## Ongoing for every member

- [ ] Do my own human reasoning before using Copilot, and log significant Copilot use
- [ ] Review at least one PR per stage that I didn't write
- [ ] Pull `main` after every merge and re-run tests
- [ ] Can explain everything I submitted
