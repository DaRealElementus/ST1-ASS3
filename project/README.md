# SmartCare application

SmartCare is a small console application for registering patients and practitioners and booking, finding, cancelling and listing appointments. It is the single evolving `project/` for Software Technology 1 Assignment 3. Runtime uses only the Python standard library.

Requirements baseline: SmartCare A3 2026 revision 2. Python 3.13 and pytest 8.3.5 verified.

## Setup

Run all commands in this section from `project/`:

```sh
cd project
python -m pip install -r requirements-dev.txt
```

`requirements-dev.txt` contains only `pytest==8.3.5` and is needed for the tests, not for running the application. Use the approved environment described in the Git/GitHub group guide.

## Running SmartCare

| Command | What it does |
|---|---|
| `python main.py` | Runs the fixed demo (see below) |
| `python main.py --interactive` | Starts the interactive menu |
| `python -m pytest` | Runs the full test suite |

### Demo sequence

`python main.py` registers one synthetic patient (`P1`, Alex Example) and one synthetic practitioner (`DR1`, Taylor Example), books appointment `A1` for `2026-10-01 09:00`, then finds and prints it:

```text
A1: P1 with DR1, 2026-10-01 09:00, scheduled
Session-only data: records are lost on exit.
```

### Interactive menu

`python main.py --interactive` shows this menu and repeats it after every action until you choose `0`:

| Option | Action | Prompts |
|---|---|---|
| 1 | Register patient | Patient ID, Patient name |
| 2 | Register practitioner | Practitioner ID, Practitioner name, Specialty |
| 3 | Find patient | Patient ID |
| 4 | Find practitioner | Practitioner ID |
| 5 | Book appointment | Appointment ID, Patient ID, Practitioner ID, Date/time |
| 6 | Find appointment | Appointment ID |
| 7 | Cancel appointment | Appointment ID |
| 8 | List practitioner appointments | Practitioner ID, Status (optional) |
| 0 | Exit | none |

Input rules:

- **Date/time** must be exactly `YYYY-MM-DD HH:MM`, for example `2026-11-10 09:00`. It is local time at minute precision.
- **Status** (option 8) is `scheduled`, `cancelled` or `completed`. Case and surrounding spaces are ignored. Leave it blank to list every status.
- **IDs** are trimmed, must not be blank, and are case-sensitive (`P1` and `p1` are different).
- Option 8 lists matches ordered by date/time, then appointment ID, and prints `No appointments found.` when the practitioner exists but nothing matches.
- Register the patient and practitioner before booking. Booking a missing participant is an error.

Bad input never ends the session. Expected problems print a message starting `Error:` (or `Unknown option; choose a number from the menu.` for a bad menu choice) and return to the menu with stored data unchanged.

Example session (prompts omitted for brevity; each line is the output of one menu choice):

```text
Registered patient P1: Alex Example
Registered practitioner DR1: Taylor Example (General practice)
Error: Use date/time format YYYY-MM-DD HH:MM              <- booked with "10/11/2026"
Booked A1: P1 with DR1, 2026-11-10 09:00, scheduled
Error: Practitioner already has a SCHEDULED appointment at this time   <- A2, same time
Cancelled A1: P1 with DR1, 2026-11-10 09:00, cancelled
Error: Only SCHEDULED appointments may be cancelled       <- cancelling A1 again
A1: P1 with DR1, 2026-11-10 09:00, cancelled              <- option 8, status "cancelled"
Error: Practitioner not found                             <- option 8 with DR9
Unknown option; choose a number from the menu.            <- menu choice 9
Session-only data: records are lost on exit.              <- choice 0
```

## Testing

From `project/`:

```sh
python -m pytest
```

| Test file | Covers |
|---|---|
| `tests/test_starter.py` | Supplied starter behaviour |
| `tests/test_domain.py` | Entities, validation and guarded cancellation |
| `tests/test_services.py` | Registration, lookup, booking, cancellation and `list_practitioner_appointments` |
| `tests/test_queries.py` | `select_appointments` and `appointment_sort_key` (purity, sorting, filters) |
| `tests/test_regressions.py` | Stage 8 regression tests for F8-01 and F8-02 |
| `tests/test_workflows.py` | End-to-end console sessions, including recovery from invalid input |

## Code layout

| Module | Responsibility |
|---|---|
| `main.py` | Entry point: demo by default, menu with `--interactive` |
| `smartcare/domain.py` | `Patient`, `Practitioner`, `Appointment` and `AppointmentStatus`; validation and guarded cancellation. Properties give read-only identity/appointment state; changes go through domain methods |
| `smartcare/data_store.py` | `SmartCareDataStore`: three in-memory dictionaries with add/find/list methods and the practitioner conflict check |
| `smartcare/services.py` | `PatientService`, `PractitionerService` and `AppointmentService`, all sharing one data store object |
| `smartcare/queries.py` | Pure functions: `appointment_sort_key` and `select_appointments` (no input/output, no mutation) |
| `smartcare/console.py` | Date/status parsing, formatting, the demo and the interactive menu |

## Error handling

- Store lookups return `None` when a record is absent; service lookups raise `LookupError`.
- Invalid values, duplicate IDs, practitioner conflicts and illegal status transitions raise `ValueError`.
- `AppointmentService.list_practitioner_appointments` raises `LookupError` for an unknown practitioner, `ValueError` for an invalid status, and returns an empty list for a known practitioner with no matches.
- The console catches `ValueError` and `LookupError`, prints `Error: ...` and carries on. Closing input (end of file) exits cleanly.
- Lists returned by the store, services and queries are new containers holding the stored objects.

## Scope and limitations

- **Session-only data.** Everything is held in memory and is lost on exit. FR-10 restart persistence is retired.
- **No rescheduling.** Appointments can be booked, found, cancelled and listed; they cannot be edited or moved.
- **No completing.** `completed` exists as a status and a filter, but there is no menu option or domain method that moves an appointment to it, so it only appears if an appointment is created with that status in code.
- **Booking rules are minimal.** The only conflict rule is one `SCHEDULED` appointment per practitioner at a given date/time; cancelled appointments do not block a time. There is no patient-conflict check, appointment duration, age rule or past-date rule.
- **Local time only.** Date/times have no time zone and must be at minute precision.
- **Case-sensitive IDs.** `DR1` and `dr1` are different practitioners.
- **Synthetic data only.** Do not enter real patient or practitioner information.
- **Console only.** There is no GUI, web interface or network access.
- No PG rescheduling or assurance solution is included; Stages 10 and 11 are PG-only.
