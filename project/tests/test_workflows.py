"""Workflow checks: scripted end-to-end console sessions (UI-01, UI-02)
and an automated service workflow.

run_menu() builds its own SmartCareDataStore, so each session test feeds
a script of typed answers through input() and checks what the console
printed. When the script runs out, input() raises EOFError and run_menu()
exits cleanly, so a session never hangs waiting for a keyboard.
"""

from datetime import datetime

import pytest

from smartcare.console import run_menu
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

NINE_AM = datetime(2026, 10, 1, 9)
SLOT = '2026-10-01 09:00'
EXIT_MESSAGE = 'Session-only data: records are lost on exit.'


def run_session(monkeypatch, capsys, *answers: str) -> str:
    """Run the menu with scripted answers and return everything printed.

    Each answer is one line the user would type, in the order the
    prompts appear. Running out of answers behaves like end-of-input.
    """
    remaining = iter(answers)

    def fake_input(prompt: str = '') -> str:
        try:
            return next(remaining)
        except StopIteration:
            raise EOFError from None

    monkeypatch.setattr('builtins.input', fake_input)
    run_menu()
    return capsys.readouterr().out


def assert_in_order(output: str, *fragments: str) -> None:
    """Assert each fragment appears in the output, in the given order."""
    position = 0
    for fragment in fragments:
        found = output.find(fragment, position)
        assert found != -1, f'{fragment!r} not found after position {position}'
        position = found + len(fragment)


def test_full_menu_session(monkeypatch, capsys) -> None:
    """UI-01: register, find, book, conflict, cancel, list, freed slot."""
    output = run_session(
        monkeypatch, capsys,
        '1', 'P1', 'Alex Example',                  # register patient P1
        '1', 'P2', 'Sam Example',                   # register patient P2
        '2', 'D1', 'Taylor Example', 'General',     # register practitioner D1
        '2', 'D2', 'Jordan Example', 'Dental',      # register practitioner D2
        '3', 'P1',                                  # find patient
        '4', 'D1',                                  # find practitioner
        '5', 'A1', 'P1', 'D1', SLOT,                # book A1
        '6', 'A1',                                  # find A1
        '5', 'A2', 'P2', 'D1', SLOT,                # same practitioner, same time
        '5', 'A3', 'P2', 'D2', SLOT,                # different practitioner
        '7', 'A1',                                  # cancel A1
        '6', 'A1',                                  # cancelled record retained
        '8', 'D1', '',                              # list D1, every status
        '5', 'A4', 'P2', 'D1', SLOT,                # freed slot can be rebooked
        '8', 'D1', 'scheduled',                     # list D1, scheduled only
        '0',                                        # exit
    )
    assert_in_order(
        output,
        'Registered patient P1: Alex Example',
        'Registered patient P2: Sam Example',
        'Registered practitioner D1: Taylor Example (General)',
        'Registered practitioner D2: Jordan Example (Dental)',
        'P1: Alex Example',
        'D1: Taylor Example (General)',
        f'Booked A1: P1 with D1, {SLOT}, scheduled',
        f'A1: P1 with D1, {SLOT}, scheduled',
        'Error: Practitioner already has a SCHEDULED appointment',
        f'Booked A3: P2 with D2, {SLOT}, scheduled',
        f'Cancelled A1: P1 with D1, {SLOT}, cancelled',
        f'A1: P1 with D1, {SLOT}, cancelled',
        f'A1: P1 with D1, {SLOT}, cancelled',       # shown again by the list
        f'Booked A4: P2 with D1, {SLOT}, scheduled',
        f'A4: P2 with D1, {SLOT}, scheduled',
        EXIT_MESSAGE,
    )
    assert 'A2:' not in output  # the conflicting booking was never stored
    assert 'Traceback' not in output


def test_invalid_input_recovery(monkeypatch, capsys) -> None:
    """UI-02: every expected error is reported, then the session goes on."""
    output = run_session(
        monkeypatch, capsys,
        'x',                                        # unknown menu choice
        '',                                         # blank menu choice
        '1', 'P1', 'Alex Example',                  # good registration
        '1', 'P1', 'Someone Else',                  # duplicate patient ID
        '1', '   ', 'Blank Id',                     # blank patient ID
        '2', 'D1', 'Taylor Example', 'General',
        '5', 'A1', 'P9', 'D1', SLOT,                # unknown patient
        '5', 'A1', 'P1', 'D9', SLOT,                # unknown practitioner
        '5', 'A1', 'P1', 'D1', '1 Oct 2026 9am',    # malformed date/time
        '5', 'A1', 'P1', 'D1', '2026-02-30 09:00',  # impossible date
        '5', 'A1', 'P1', 'D1', SLOT,                # now a valid booking
        '5', 'A1', 'P1', 'D1', '2026-10-01 10:00',  # duplicate appointment ID
        '6', 'A9',                                  # unknown appointment
        '8', 'D1', 'finished',                      # invalid status filter
        '8', 'D9', '',                              # unknown practitioner
        '7', 'A1',                                  # cancel works
        '7', 'A1',                                  # repeated cancellation
        '6', 'A1',                                  # state unchanged: cancelled
        '0',
    )
    assert_in_order(
        output,
        'Unknown option; choose a number from the menu.',
        'Unknown option; choose a number from the menu.',
        'Registered patient P1: Alex Example',
        'Error: Patient ID already exists',
        'Error: Patient ID cannot be blank',
        'Registered practitioner D1: Taylor Example (General)',
        'Error: Patient not found',
        'Error: Practitioner not found',
        'Error: Use date/time format YYYY-MM-DD HH:MM',
        'Error: Invalid calendar date/time',
        f'Booked A1: P1 with D1, {SLOT}, scheduled',
        'Error: Appointment ID already exists',
        'Error: Appointment not found',
        'Error: Status must be one of scheduled, cancelled, completed',
        'Error: Practitioner not found',
        f'Cancelled A1: P1 with D1, {SLOT}, cancelled',
        'Error: Only SCHEDULED appointments may be cancelled',
        f'A1: P1 with D1, {SLOT}, cancelled',
        EXIT_MESSAGE,
    )
    # The duplicate patient was rejected, so the original name survives.
    assert 'Someone Else' not in output
    assert 'Traceback' not in output


def test_list_shows_empty_message_for_known_practitioner(
    monkeypatch, capsys,
) -> None:
    """A registered practitioner with no appointments is not an error."""
    output = run_session(
        monkeypatch, capsys,
        '2', 'D1', 'Taylor Example', 'General',
        '8', 'D1', '',
        '0',
    )
    assert 'No appointments found.' in output
    assert 'Error:' not in output


def test_status_text_ignores_case_and_spaces(monkeypatch, capsys) -> None:
    """Status text is converted to the enum, ignoring case and spaces."""
    output = run_session(
        monkeypatch, capsys,
        '1', 'P1', 'Alex Example',
        '2', 'D1', 'Taylor Example', 'General',
        '5', 'A1', 'P1', 'D1', SLOT,
        '8', 'D1', '  SCHEDULED ',
        '8', 'D1', 'cancelled',
        '0',
    )
    assert_in_order(
        output,
        f'A1: P1 with D1, {SLOT}, scheduled',   # from the booking message
        f'A1: P1 with D1, {SLOT}, scheduled',   # from the scheduled list
        'No appointments found.',               # nothing cancelled yet
    )


def test_end_of_input_exits_cleanly(monkeypatch, capsys) -> None:
    """Running out of input at the menu ends the session with no error."""
    output = run_session(monkeypatch, capsys)
    assert EXIT_MESSAGE in output
    assert 'Traceback' not in output


def test_end_of_input_mid_action_exits_cleanly(monkeypatch, capsys) -> None:
    """Running out of input halfway through an action also exits."""
    output = run_session(monkeypatch, capsys, '1', 'P1')
    assert EXIT_MESSAGE in output
    assert 'Registered patient' not in output


@pytest.fixture
def clinic():
    """Return a fresh store with the three services sharing it."""
    store = SmartCareDataStore()
    return (
        store,
        PatientService(store),
        PractitionerService(store),
        AppointmentService(store),
    )


def test_service_workflow(clinic) -> None:
    """Automated service workflow: book, conflict, cancel, rebook, list."""
    store, patients, practitioners, appointments = clinic
    patients.register_patient('P1', 'Alex Example')
    patients.register_patient('P2', 'Sam Example')
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    practitioners.register_practitioner('D2', 'Jordan Example', 'Dental')

    first = appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    with pytest.raises(ValueError):
        appointments.book_appointment('A2', 'P2', 'D1', NINE_AM)
    assert store.find_appointment('A2') is None
    other = appointments.book_appointment('A3', 'P2', 'D2', NINE_AM)

    assert appointments.cancel_appointment('A1') is first
    assert first.status is AppointmentStatus.CANCELLED
    with pytest.raises(ValueError):
        appointments.cancel_appointment('A1')
    assert appointments.find_appointment('A1') is first  # history retained

    rebooked = appointments.book_appointment('A4', 'P2', 'D1', NINE_AM)

    assert appointments.list_practitioner_appointments('D1') == [first, rebooked]
    assert appointments.list_practitioner_appointments(
        'D1', AppointmentStatus.SCHEDULED,
    ) == [rebooked]
    assert appointments.list_practitioner_appointments('D2') == [other]