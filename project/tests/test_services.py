"""Service checks: lookup/errors, identity, cancel/history, rejection.

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