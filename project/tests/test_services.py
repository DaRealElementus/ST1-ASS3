"""Service checks: lookup/errors, identity, cancel/history, rejection,
registration duplicates, booking and practitioner conflicts.

The patient and practitioner lookup tests need the Stage 6 TODOs and
fail with NotImplementedError until those are completed.
"""

from datetime import datetime, timezone
from typing import Any, NamedTuple

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

NINE_AM = datetime(2026, 10, 1, 9)
TEN_AM = datetime(2026, 10, 1, 10)

FINDERS = [
    pytest.param(lambda c, i: c.patients.find_patient(i), id='patient'),
    pytest.param(
        lambda c, i: c.practitioners.find_practitioner(i), id='practitioner',
    ),
    pytest.param(
        lambda c, i: c.appointments.find_appointment(i), id='appointment',
    ),
]


class Clinic(NamedTuple):
    """A fresh store with patient P1, practitioner D1 and the services."""

    data_store: SmartCareDataStore
    patient: Any
    practitioner: Any
    patients: PatientService
    practitioners: PractitionerService
    appointments: AppointmentService


def make_clinic() -> Clinic:
    """Create a fresh store with P1 and D1 registered through services."""
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    return Clinic(
        store,
        patients.register_patient('P1', 'Alex Example'),
        practitioners.register_practitioner('D1', 'Taylor Example', 'General'),
        patients,
        practitioners,
        AppointmentService(store),
    )


def snapshot(store: SmartCareDataStore) -> list[Any]:
    """Capture every stored record and appointment state."""
    return [
        [(p, p.name) for p in store.list_patients()],
        [(d, d.name, d.specialty) for d in store.list_practitioners()],
        [
            (a, a.patient, a.practitioner, a.date_time, a.status)
            for a in store.list_appointments()
        ],
    ]


# Lookup and errors


@pytest.mark.parametrize('find', FINDERS)
def test_lookup_absent_raises_without_creating(find: Any) -> None:
    """Verify an absent ID raises LookupError and creates nothing."""
    clinic = make_clinic()
    before = snapshot(clinic.data_store)
    with pytest.raises(LookupError):
        find(clinic, 'missing')
    assert snapshot(clinic.data_store) == before


@pytest.mark.parametrize('blank', ['', '   ', None])
@pytest.mark.parametrize('find', FINDERS)
def test_lookup_blank_id_rejected(find: Any, blank: Any) -> None:
    """Verify a blank or invalid ID raises ValueError."""
    clinic = make_clinic()
    before = snapshot(clinic.data_store)
    with pytest.raises(ValueError):
        find(clinic, blank)
    assert snapshot(clinic.data_store) == before


# Identity


def test_lookups_return_the_stored_objects() -> None:
    """Verify lookups and bookings use the same stored objects."""
    clinic = make_clinic()
    first = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    second = clinic.appointments.book_appointment('A2', 'P1', 'D1', TEN_AM)
    assert clinic.patients.find_patient('P1') is clinic.patient
    assert clinic.practitioners.find_practitioner('D1') is clinic.practitioner
    assert clinic.appointments.find_appointment('A1') is first
    assert clinic.appointments.find_appointment('A2') is second
    assert first is not second
    assert first.patient is clinic.patient
    assert first.practitioner is clinic.practitioner


def test_identity_fields_are_read_only() -> None:
    """Verify identity fields cannot be reassigned."""
    clinic = make_clinic()
    appointment = clinic.appointments.book_appointment(
        'A1', 'P1', 'D1', NINE_AM,
    )
    for obj, field in [
        (clinic.patient, 'patient_id'),
        (clinic.practitioner, 'practitioner_id'),
        (appointment, 'appointment_id'),
    ]:
        with pytest.raises(AttributeError):
            setattr(obj, field, 'X9')
    assert clinic.appointments.find_appointment('A1') is appointment


# Cancel and history


def test_cancel_retains_appointment_and_guards_repeat() -> None:
    """Verify cancel keeps the record, spares others and blocks repeats."""
    clinic = make_clinic()
    first = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    second = clinic.appointments.book_appointment('A2', 'P1', 'D1', TEN_AM)
    assert clinic.appointments.cancel_appointment('A1') is first
    assert first.status is AppointmentStatus.CANCELLED
    assert second.status is AppointmentStatus.SCHEDULED
    assert clinic.data_store.list_appointments() == [first, second]
    before = snapshot(clinic.data_store)
    with pytest.raises(ValueError):
        clinic.appointments.cancel_appointment('A1')
    assert snapshot(clinic.data_store) == before


def test_cancelled_slot_can_be_rebooked_and_history_kept() -> None:
    """Verify a cancelled slot is free again and both records remain."""
    clinic = make_clinic()
    cancelled = clinic.appointments.book_appointment(
        'A1', 'P1', 'D1', NINE_AM,
    )
    clinic.appointments.cancel_appointment('A1')
    rebooked = clinic.appointments.book_appointment('A2', 'P1', 'D1', NINE_AM)
    assert cancelled.status is AppointmentStatus.CANCELLED
    assert rebooked.status is AppointmentStatus.SCHEDULED
    assert clinic.data_store.list_appointments() == [cancelled, rebooked]


@pytest.mark.parametrize(
    ('appointment_id', 'error'),
    [('missing', LookupError), ('   ', ValueError), (None, ValueError)],
)
def test_cancel_bad_id_rejected_without_mutation(
    appointment_id: Any,
    error: type[Exception],
) -> None:
    """Verify an unknown or blank ID is rejected and nothing changes."""
    clinic = make_clinic()
    clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    before = snapshot(clinic.data_store)
    with pytest.raises(error):
        clinic.appointments.cancel_appointment(appointment_id)
    assert snapshot(clinic.data_store) == before


def test_completed_appointment_cannot_be_cancelled() -> None:
    """Verify a COMPLETED appointment is rejected and unchanged."""
    clinic = make_clinic()
    completed = Appointment(
        'A1', clinic.patient, clinic.practitioner, NINE_AM,
        AppointmentStatus.COMPLETED,
    )
    clinic.data_store.add_appointment(completed)
    with pytest.raises(ValueError):
        clinic.appointments.cancel_appointment('A1')
    assert completed.status is AppointmentStatus.COMPLETED


# Rejection without mutation


@pytest.mark.parametrize(
    ('args', 'error'),
    [
        (('A1', 'P1', 'D1', TEN_AM), ValueError),
        (('A2', 'missing', 'D1', NINE_AM), LookupError),
        (('A2', 'P1', 'missing', NINE_AM), LookupError),
        (('A2', '  ', 'D1', NINE_AM), ValueError),
        (('  ', 'P1', 'D1', TEN_AM), ValueError),
        (('A2', 'P2', 'D1', NINE_AM), ValueError),
        (('A2', 'P1', 'D1', datetime(2026, 10, 1, 9, 0, 30)), ValueError),
        (('A2', 'P1', 'D1', datetime(2026, 10, 1, 9, tzinfo=timezone.utc)),
         ValueError),
        (('A2', 'P1', 'D1', '2026-10-01 09:00'), ValueError),
    ],
    ids=[
        'duplicate-id', 'unknown-patient', 'unknown-practitioner',
        'blank-patient', 'blank-appointment-id', 'practitioner-conflict',
        'seconds', 'timezone', 'string-time',
    ],
)
def test_booking_rejected_without_mutation(
    args: tuple[Any, ...],
    error: type[Exception],
) -> None:
    """Verify each rejected booking leaves every record unchanged."""
    clinic = make_clinic()
    clinic.patients.register_patient('P2', 'Casey Example')
    clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    before = snapshot(clinic.data_store)
    with pytest.raises(error):
        clinic.appointments.book_appointment(*args)
    assert snapshot(clinic.data_store) == before


def test_invalid_registration_rejected_without_mutation() -> None:
    """Verify invalid or duplicate registrations change nothing."""
    clinic = make_clinic()
    before = snapshot(clinic.data_store)
    with pytest.raises(ValueError):
        clinic.patients.register_patient(' ', 'No ID')
    with pytest.raises(ValueError):
        clinic.patients.register_patient('P1', 'Replacement')
    with pytest.raises(ValueError):
        clinic.practitioners.register_practitioner('D2', 'No Specialty', ' ')
    with pytest.raises(ValueError):
        clinic.practitioners.register_practitioner('D1', 'Other', 'Other')
    assert snapshot(clinic.data_store) == before


# Registration duplicates (AC-01.2)


@pytest.mark.parametrize('patient_id', ['P1', '  P1  '])
def test_duplicate_patient_id_keeps_original(patient_id: str) -> None:
    """Verify a duplicate patient ID, even padded, keeps the original."""
    clinic = make_clinic()
    before = snapshot(clinic.data_store)
    with pytest.raises(ValueError):
        clinic.patients.register_patient(patient_id, 'Replacement')
    assert clinic.patients.find_patient('P1') is clinic.patient
    assert snapshot(clinic.data_store) == before


@pytest.mark.parametrize('practitioner_id', ['D1', '  D1  '])
def test_duplicate_practitioner_id_keeps_original(
    practitioner_id: str,
) -> None:
    """Verify a duplicate practitioner ID, even padded, keeps the original."""
    clinic = make_clinic()
    before = snapshot(clinic.data_store)
    with pytest.raises(ValueError):
        clinic.practitioners.register_practitioner(
            practitioner_id, 'Replacement', 'Other',
        )
    assert clinic.practitioners.find_practitioner('D1') is clinic.practitioner
    assert snapshot(clinic.data_store) == before


def test_new_ids_register_after_rejected_duplicates() -> None:
    """Verify a rejected duplicate does not block a new unique ID."""
    clinic = make_clinic()
    with pytest.raises(ValueError):
        clinic.patients.register_patient('P1', 'Replacement')
    with pytest.raises(ValueError):
        clinic.practitioners.register_practitioner('D1', 'Other', 'Other')
    patient = clinic.patients.register_patient('P2', 'Casey Example')
    practitioner = clinic.practitioners.register_practitioner(
        'D2', 'Morgan Example', 'Cardiology',
    )
    assert clinic.data_store.list_patients() == [clinic.patient, patient]
    assert clinic.data_store.list_practitioners() == [
        clinic.practitioner, practitioner,
    ]


# Booking (AC-03.x)


def test_booking_stores_scheduled_appointment() -> None:
    """Verify a booking stores the requested details as SCHEDULED."""
    clinic = make_clinic()
    appointment = clinic.appointments.book_appointment(
        'A1', 'P1', 'D1', NINE_AM,
    )
    assert appointment.appointment_id == 'A1'
    assert appointment.patient is clinic.patient
    assert appointment.practitioner is clinic.practitioner
    assert appointment.date_time == NINE_AM
    assert appointment.status is AppointmentStatus.SCHEDULED
    assert clinic.data_store.list_appointments() == [appointment]


def test_booking_links_the_requested_participants() -> None:
    """Verify each booking links its own patient and practitioner."""
    clinic = make_clinic()
    casey = clinic.patients.register_patient('P2', 'Casey Example')
    morgan = clinic.practitioners.register_practitioner(
        'D2', 'Morgan Example', 'Cardiology',
    )
    first = clinic.appointments.book_appointment('A1', 'P1', 'D2', NINE_AM)
    second = clinic.appointments.book_appointment('A2', 'P2', 'D1', TEN_AM)
    assert first.patient is clinic.patient
    assert first.practitioner is morgan
    assert second.patient is casey
    assert second.practitioner is clinic.practitioner
    assert clinic.data_store.list_appointments() == [first, second]


def test_booking_normalises_padded_ids() -> None:
    """Verify padded IDs resolve to the stored records and trimmed ID."""
    clinic = make_clinic()
    appointment = clinic.appointments.book_appointment(
        '  A1  ', '  P1  ', '  D1  ', NINE_AM,
    )
    assert appointment.appointment_id == 'A1'
    assert appointment.patient is clinic.patient
    assert appointment.practitioner is clinic.practitioner
    assert clinic.appointments.find_appointment('A1') is appointment


@pytest.mark.parametrize(
    'args',
    [
        (None, 'P1', 'D1', TEN_AM),
        ('  A1  ', 'P1', 'D1', TEN_AM),
        ('A2', None, 'D1', TEN_AM),
        ('A2', 'P1', None, TEN_AM),
        ('A2', 'P1', '  ', TEN_AM),
        ('A2', 'P1', 'D1', None),
        ('A2', 'P1', 'D1', datetime(2026, 10, 1, 10, 0, 0, 1)),
    ],
    ids=[
        'none-appointment-id', 'padded-duplicate-id', 'none-patient',
        'none-practitioner', 'blank-practitioner', 'none-time', 'microseconds',
    ],
)
def test_booking_invalid_values_rejected(args: tuple[Any, ...]) -> None:
    """Verify invalid booking values raise ValueError and change nothing."""
    clinic = make_clinic()
    clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    before = snapshot(clinic.data_store)
    with pytest.raises(ValueError):
        clinic.appointments.book_appointment(*args)
    assert snapshot(clinic.data_store) == before


# Practitioner conflicts (AC-04.x)


@pytest.mark.parametrize('practitioner_id', ['D1', '  D1  '])
def test_conflict_rejected_for_a_different_patient(
    practitioner_id: str,
) -> None:
    """Verify the practitioner conflict applies whichever patient books."""
    clinic = make_clinic()
    clinic.patients.register_patient('P2', 'Casey Example')
    original = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    with pytest.raises(ValueError):
        clinic.appointments.book_appointment(
            'A2', 'P2', practitioner_id, NINE_AM,
        )
    assert original.status is AppointmentStatus.SCHEDULED
    assert clinic.data_store.list_appointments() == [original]


def test_different_practitioners_can_share_a_time() -> None:
    """Verify different practitioners at one time do not conflict."""
    clinic = make_clinic()
    clinic.patients.register_patient('P2', 'Casey Example')
    clinic.practitioners.register_practitioner(
        'D2', 'Morgan Example', 'Cardiology',
    )
    first = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    second = clinic.appointments.book_appointment('A2', 'P2', 'D2', NINE_AM)
    assert first.status is AppointmentStatus.SCHEDULED
    assert second.status is AppointmentStatus.SCHEDULED
    assert clinic.data_store.list_appointments() == [first, second]


@pytest.mark.parametrize(
    'other_time',
    [
        datetime(2026, 10, 1, 8, 59),
        datetime(2026, 10, 1, 9, 1),
        datetime(2026, 10, 2, 9),
    ],
    ids=['minute-before', 'minute-after', 'next-day'],
)
def test_same_practitioner_at_another_time_allowed(
    other_time: datetime,
) -> None:
    """Verify only an exact time match conflicts for a practitioner."""
    clinic = make_clinic()
    first = clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    second = clinic.appointments.book_appointment('A2', 'P1', 'D1', other_time)
    assert second.date_time == other_time
    assert clinic.data_store.list_appointments() == [first, second]


def test_completed_appointment_does_not_block_its_slot() -> None:
    """Verify only a SCHEDULED appointment holds the practitioner's time."""
    clinic = make_clinic()
    completed = Appointment(
        'A1', clinic.patient, clinic.practitioner, NINE_AM,
        AppointmentStatus.COMPLETED,
    )
    clinic.data_store.add_appointment(completed)
    rebooked = clinic.appointments.book_appointment('A2', 'P1', 'D1', NINE_AM)
    assert completed.status is AppointmentStatus.COMPLETED
    assert rebooked.status is AppointmentStatus.SCHEDULED
    assert clinic.data_store.list_appointments() == [completed, rebooked]


def test_rebooked_slot_conflicts_again() -> None:
    """Verify a rebooked slot blocks despite the earlier cancelled record."""
    clinic = make_clinic()
    clinic.appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    clinic.appointments.cancel_appointment('A1')
    clinic.appointments.book_appointment('A2', 'P1', 'D1', NINE_AM)
    before = snapshot(clinic.data_store)
    with pytest.raises(ValueError):
        clinic.appointments.book_appointment('A3', 'P1', 'D1', NINE_AM)
    assert snapshot(clinic.data_store) == before