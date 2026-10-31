"""Domain checks: Patient, Practitioner and Appointment rules.

Contract (smartcare/domain.py): every required text field is trimmed and
must be a non-blank string; anything else raises ValueError. Appointment
date/times are naive and minute-precision, status changes only through
guarded operations, and identities are read-only.
"""

from datetime import date, datetime, timezone
from typing import Any

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)

# Values that must be rejected for any required text field.
INVALID_TEXT = ['', ' ', '   ', '\t', '\n', ' \t\n ', None, 42, 3.5, b'P1', []]

NINE_AM = datetime(2026, 10, 1, 9, 0)

# Values that are not a naive, minute-precision datetime.
INVALID_DATE_TIME = [
    pytest.param(datetime(2026, 10, 1, 9, 0, 30), id='seconds'),
    pytest.param(datetime(2026, 10, 1, 9, 0, 0, 1), id='microseconds'),
    pytest.param(datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc), id='aware'),
    pytest.param('2026-10-01 09:00', id='string'),
    pytest.param(date(2026, 10, 1), id='date-only'),
    pytest.param(None, id='none'),
    pytest.param(1790000000, id='timestamp'),
]


def make_appointment(
    status: AppointmentStatus = AppointmentStatus.SCHEDULED,
) -> Appointment:
    """Build a valid appointment with fresh participants."""
    return Appointment(
        'A1',
        Patient('P1', 'Alex Example'),
        Practitioner('D1', 'Taylor Example', 'General'),
        NINE_AM,
        status,
    )


# Patient: valid construction


def test_patient_valid_fields_stored() -> None:
    """Verify a valid patient keeps its ID and name."""
    patient = Patient('P1', 'Alex Example')
    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Example'


def test_patient_fields_are_trimmed() -> None:
    """Verify surrounding whitespace is removed from ID and name."""
    patient = Patient('  P1  ', '\tAlex Example\n')
    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Example'


def test_patient_inner_whitespace_preserved() -> None:
    """Verify only the ends are trimmed, not spaces inside the name."""
    assert Patient('P1', 'Alex  van Example').name == 'Alex  van Example'


# Patient: invalid construction


@pytest.mark.parametrize('bad', INVALID_TEXT)
def test_patient_invalid_id_rejected(bad: Any) -> None:
    """Verify a blank or non-text patient ID raises ValueError."""
    with pytest.raises(ValueError):
        Patient(bad, 'Alex Example')


@pytest.mark.parametrize('bad', INVALID_TEXT)
def test_patient_invalid_name_rejected(bad: Any) -> None:
    """Verify a blank or non-text patient name raises ValueError."""
    with pytest.raises(ValueError):
        Patient('P1', bad)


def test_patient_both_fields_invalid_rejected() -> None:
    """Verify a patient with every field blank raises ValueError."""
    with pytest.raises(ValueError):
        Patient('', '')


# Practitioner: valid construction


def test_practitioner_valid_fields_stored() -> None:
    """Verify a valid practitioner keeps its ID, name and specialty."""
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Taylor Example'
    assert practitioner.specialty == 'General'


def test_practitioner_fields_are_trimmed() -> None:
    """Verify surrounding whitespace is removed from all three fields."""
    practitioner = Practitioner('  D1 ', '\tTaylor Example\n', ' General  ')
    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Taylor Example'
    assert practitioner.specialty == 'General'


def test_practitioner_inner_whitespace_preserved() -> None:
    """Verify only the ends are trimmed, not spaces inside a field."""
    practitioner = Practitioner('D1', 'Taylor Example', 'Family  Medicine')
    assert practitioner.specialty == 'Family  Medicine'


# Practitioner: invalid construction


@pytest.mark.parametrize('bad', INVALID_TEXT)
def test_practitioner_invalid_id_rejected(bad: Any) -> None:
    """Verify a blank or non-text practitioner ID raises ValueError."""
    with pytest.raises(ValueError):
        Practitioner(bad, 'Taylor Example', 'General')


@pytest.mark.parametrize('bad', INVALID_TEXT)
def test_practitioner_invalid_name_rejected(bad: Any) -> None:
    """Verify a blank or non-text practitioner name raises ValueError."""
    with pytest.raises(ValueError):
        Practitioner('D1', bad, 'General')


@pytest.mark.parametrize('bad', INVALID_TEXT)
def test_practitioner_invalid_specialty_rejected(bad: Any) -> None:
    """Verify a blank or non-text specialty raises ValueError."""
    with pytest.raises(ValueError):
        Practitioner('D1', 'Taylor Example', bad)


# Appointment: valid construction


def test_appointment_valid_fields_stored() -> None:
    """Verify a valid appointment keeps ID, participants and time."""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    appointment = Appointment('A1', patient, practitioner, NINE_AM)
    assert appointment.appointment_id == 'A1'
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == NINE_AM


def test_appointment_defaults_to_scheduled() -> None:
    """Verify a new appointment is SCHEDULED unless told otherwise."""
    assert make_appointment().status is AppointmentStatus.SCHEDULED


@pytest.mark.parametrize('status', list(AppointmentStatus))
def test_appointment_accepts_every_status(status: AppointmentStatus) -> None:
    """Verify each supported status can be supplied at construction."""
    assert make_appointment(status).status is status


def test_appointment_id_is_trimmed() -> None:
    """Verify surrounding whitespace is removed from the ID."""
    appointment = Appointment(
        '  A1 ',
        Patient('P1', 'Alex Example'),
        Practitioner('D1', 'Taylor Example', 'General'),
        NINE_AM,
    )
    assert appointment.appointment_id == 'A1'


# Appointment: invalid construction


@pytest.mark.parametrize('bad', INVALID_TEXT)
def test_appointment_invalid_id_rejected(bad: Any) -> None:
    """Verify a blank or non-text appointment ID raises ValueError."""
    with pytest.raises(ValueError):
        Appointment(
            bad,
            Patient('P1', 'Alex Example'),
            Practitioner('D1', 'Taylor Example', 'General'),
            NINE_AM,
        )


@pytest.mark.parametrize('bad', [None, 'P1', 42, {'patient_id': 'P1'}])
def test_appointment_non_patient_rejected(bad: Any) -> None:
    """Verify the patient must be a Patient object, not an ID or value."""
    with pytest.raises(ValueError):
        Appointment(
            'A1',
            bad,
            Practitioner('D1', 'Taylor Example', 'General'),
            NINE_AM,
        )


@pytest.mark.parametrize('bad', [None, 'D1', 42, {'practitioner_id': 'D1'}])
def test_appointment_non_practitioner_rejected(bad: Any) -> None:
    """Verify the practitioner must be a Practitioner object."""
    with pytest.raises(ValueError):
        Appointment(
            'A1',
            Patient('P1', 'Alex Example'),
            bad,
            NINE_AM,
        )


def test_appointment_swapped_participants_rejected() -> None:
    """Verify a practitioner cannot be passed where a patient belongs."""
    with pytest.raises(ValueError):
        Appointment(
            'A1',
            Practitioner('D1', 'Taylor Example', 'General'),
            Patient('P1', 'Alex Example'),
            NINE_AM,
        )


@pytest.mark.parametrize('bad', [None, 'scheduled', 'SCHEDULED', 0, 1])
def test_appointment_invalid_status_rejected(bad: Any) -> None:
    """Verify status must be an AppointmentStatus member, not its text."""
    with pytest.raises(ValueError):
        make_appointment(bad)


# Appointment: date/time rules


def test_appointment_whole_minute_naive_time_accepted() -> None:
    """Verify a naive time with zero seconds and microseconds is kept."""
    when = datetime(2026, 12, 31, 23, 59)
    appointment = Appointment(
        'A1',
        Patient('P1', 'Alex Example'),
        Practitioner('D1', 'Taylor Example', 'General'),
        when,
    )
    assert appointment.date_time == when


@pytest.mark.parametrize('bad', INVALID_DATE_TIME)
def test_appointment_invalid_date_time_rejected(bad: Any) -> None:
    """Verify aware, sub-minute or non-datetime values raise ValueError."""
    with pytest.raises(ValueError):
        Appointment(
            'A1',
            Patient('P1', 'Alex Example'),
            Practitioner('D1', 'Taylor Example', 'General'),
            bad,
        )


# Appointment: state transitions


def test_cancel_scheduled_sets_cancelled() -> None:
    """Verify cancelling a SCHEDULED appointment marks it CANCELLED."""
    appointment = make_appointment()
    appointment.cancel()
    assert appointment.status is AppointmentStatus.CANCELLED


def test_cancel_keeps_the_appointment_details() -> None:
    """Verify cancelling changes only status, not the stored details."""
    appointment = make_appointment()
    patient = appointment.patient
    practitioner = appointment.practitioner
    appointment.cancel()
    assert appointment.appointment_id == 'A1'
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == NINE_AM


def test_cancel_twice_rejected_and_stays_cancelled() -> None:
    """Verify a second cancel raises ValueError and status is unchanged."""
    appointment = make_appointment()
    appointment.cancel()
    with pytest.raises(ValueError):
        appointment.cancel()
    assert appointment.status is AppointmentStatus.CANCELLED


@pytest.mark.parametrize(
    'status',
    [AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED],
)
def test_cancel_non_scheduled_rejected_and_unchanged(
    status: AppointmentStatus,
) -> None:
    """Verify only SCHEDULED appointments may be cancelled."""
    appointment = make_appointment(status)
    with pytest.raises(ValueError):
        appointment.cancel()
    assert appointment.status is status


def test_status_cannot_be_assigned_directly() -> None:
    """Verify status changes only through guarded operations."""
    appointment = make_appointment()
    with pytest.raises(AttributeError):
        appointment.status = AppointmentStatus.COMPLETED  # type: ignore
    assert appointment.status is AppointmentStatus.SCHEDULED


# Read-only identity and associations


def test_patient_id_is_read_only() -> None:
    """Verify a patient ID cannot be reassigned after construction."""
    patient = Patient('P1', 'Alex Example')
    with pytest.raises(AttributeError):
        patient.patient_id = 'P2'  # type: ignore
    assert patient.patient_id == 'P1'


def test_practitioner_id_is_read_only() -> None:
    """Verify a practitioner ID cannot be reassigned after construction."""
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    with pytest.raises(AttributeError):
        practitioner.practitioner_id = 'D2'  # type: ignore
    assert practitioner.practitioner_id == 'D1'


@pytest.mark.parametrize(
    ('attribute', 'value'),
    [
        ('appointment_id', 'A2'),
        ('patient', Patient('P2', 'Sam Other')),
        ('practitioner', Practitioner('D2', 'Jo Other', 'Dental')),
        ('date_time', datetime(2026, 10, 2, 9, 0)),
    ],
)
def test_appointment_fields_are_read_only(
    attribute: str,
    value: Any,
) -> None:
    """Verify appointment ID, participants and time cannot be reassigned."""
    appointment = make_appointment()
    original = getattr(appointment, attribute)
    with pytest.raises(AttributeError):
        setattr(appointment, attribute, value)
    assert getattr(appointment, attribute) == original