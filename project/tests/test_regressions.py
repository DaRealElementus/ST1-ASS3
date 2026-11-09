"""Stage 8 regression tests for the two faults found in data_store.py.

F8-01: has_practitioner_conflict compared practitioner IDs with != so it
flagged different practitioners and missed the same practitioner
(AC-04.x).

F8-02: find_appointment skipped cancelled records, so retained history
could not be found and a repeat cancel raised LookupError instead of
ValueError (FR-06/07, AC-05.x, AC-06.1).

These tests call the data store directly as well as the services, so a
fault in the store predicate is caught even if a service check changes.
"""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

NINE_AM = datetime(2026, 10, 1, 9)
TEN_AM = datetime(2026, 10, 1, 10)


def make_store() -> tuple[SmartCareDataStore, AppointmentService]:
    """Create a store with patients P1/P2 and practitioners D1/D2."""
    store = SmartCareDataStore()
    patients = PatientService(store)
    practitioners = PractitionerService(store)
    patients.register_patient('P1', 'Alex Example')
    patients.register_patient('P2', 'Sam Example')
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    practitioners.register_practitioner('D2', 'Jordan Example', 'Dental')
    return store, AppointmentService(store)


# F8-01 practitioner conflict


def test_f8_01_store_reports_same_practitioner_same_time() -> None:
    """The store must report a conflict for the same practitioner/time."""
    store, appointments = make_store()
    appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)

    assert store.has_practitioner_conflict('D1', NINE_AM) is True


def test_f8_01_store_ignores_different_practitioner_same_time() -> None:
    """Another practitioner's booking at the same time is not a conflict."""
    store, appointments = make_store()
    appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)

    assert store.has_practitioner_conflict('D2', NINE_AM) is False


def test_f8_01_same_practitioner_double_booking_rejected() -> None:
    """A second booking for D1 at 09:00 is rejected and nothing is added."""
    store, appointments = make_store()
    first = appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)

    with pytest.raises(ValueError, match='already has a SCHEDULED'):
        appointments.book_appointment('A2', 'P2', 'D1', NINE_AM)

    assert store.list_appointments() == [first]


def test_f8_01_different_practitioners_both_booked() -> None:
    """D1 and D2 can both be booked at 09:00."""
    store, appointments = make_store()
    first = appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    second = appointments.book_appointment('A2', 'P2', 'D2', NINE_AM)

    assert store.list_appointments() == [first, second]
    assert second.practitioner.practitioner_id == 'D2'


def test_f8_01_conflict_still_needs_matching_time_and_status() -> None:
    """The repair must keep the time, status and exclusion conditions."""
    store, appointments = make_store()
    appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)

    assert store.has_practitioner_conflict('D1', TEN_AM) is False
    assert store.has_practitioner_conflict(
        'D1', NINE_AM, exclude_appointment_id='A1',
    ) is False

    appointments.cancel_appointment('A1')
    assert store.has_practitioner_conflict('D1', NINE_AM) is False


# F8-02 retained-history lookup


def test_f8_02_store_finds_cancelled_appointment() -> None:
    """The store lookup returns the same cancelled object, not None."""
    store, appointments = make_store()
    booked = appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    appointments.cancel_appointment('A1')

    found = store.find_appointment('A1')

    assert found is booked
    assert found.status is AppointmentStatus.CANCELLED


def test_f8_02_store_finds_cancelled_appointment_with_padded_id() -> None:
    """Trimming still applies to cancelled records."""
    store, appointments = make_store()
    booked = appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    appointments.cancel_appointment('A1')

    assert store.find_appointment('  A1  ') is booked


def test_f8_02_repeat_cancel_raises_value_error_not_lookup_error() -> None:
    """A second cancel is an invalid transition, not a missing record."""
    store, appointments = make_store()
    appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    appointments.cancel_appointment('A1')

    with pytest.raises(ValueError):
        appointments.cancel_appointment('A1')

    assert store.find_appointment('A1').status is AppointmentStatus.CANCELLED


def test_f8_02_cancelled_id_cannot_be_reused() -> None:
    """A retained cancelled ID still blocks a new booking with that ID."""
    store, appointments = make_store()
    original = appointments.book_appointment('A1', 'P1', 'D1', NINE_AM)
    appointments.cancel_appointment('A1')

    with pytest.raises(ValueError, match='Appointment ID already exists'):
        appointments.book_appointment('A1', 'P2', 'D2', TEN_AM)

    assert store.list_appointments() == [original]
    assert store.find_appointment('A1') is original
