"""Query checks: appointment_sort_key ordering and select_appointments.

Contract (smartcare/queries.py): the key is (date_time, appointment_id),
so appointments order by time first and ID breaks ties. Building the key
has no side effects. select_appointments returns a new, sorted list of
one practitioner's appointments, optionally filtered by status, without
changing the source list or its appointments.
"""

from datetime import datetime

import pytest

from smartcare.domain import Appointment, AppointmentStatus, Patient, Practitioner
from smartcare.queries import appointment_sort_key, select_appointments

PATIENT = Patient('P1', 'Pat Example')
PRACTITIONER = Practitioner('D1', 'Dr Example', 'General')
OTHER_PRACTITIONER = Practitioner('D2', 'Dr Other', 'Dental')
NINE_AM = datetime(2026, 10, 1, 9, 0)
TEN_AM = datetime(2026, 10, 1, 10, 0)
ELEVEN_AM = datetime(2026, 10, 1, 11, 0)


def make_appointment(
    appointment_id: str,
    date_time: datetime,
    practitioner: Practitioner = PRACTITIONER,
    status: AppointmentStatus = AppointmentStatus.SCHEDULED,
) -> Appointment:
    """Return an appointment with shared synthetic participants."""
    return Appointment(appointment_id, PATIENT, practitioner, date_time, status)


def mixed_appointments() -> list[Appointment]:
    """Return an unsorted list mixing practitioners and statuses.

    A4 comes before A1 at the same time, so only the ID tie-break puts
    A1 first.
    """
    return [
        make_appointment('A3', ELEVEN_AM),
        make_appointment(
            'A4', NINE_AM, status=AppointmentStatus.COMPLETED,
        ),
        make_appointment('B1', NINE_AM, OTHER_PRACTITIONER),
        make_appointment(
            'A2', TEN_AM, status=AppointmentStatus.CANCELLED,
        ),
        make_appointment('A1', NINE_AM),
    ]


def snapshot(appointments: list[Appointment]) -> list[tuple]:
    """Capture the source order and every appointment's fields."""
    return [
        (a, a.appointment_id, a.practitioner, a.date_time, a.status)
        for a in appointments
    ]


def test_key_is_date_time_then_id() -> None:
    appointment = make_appointment('A1', NINE_AM)
    assert appointment_sort_key(appointment) == (NINE_AM, 'A1')


def test_sorted_orders_by_time_before_id() -> None:
    late = make_appointment('A1', TEN_AM)
    early = make_appointment('A2', NINE_AM)
    assert sorted([late, early], key=appointment_sort_key) == [early, late]


def test_id_breaks_ties_at_same_time() -> None:
    second = make_appointment('A2', NINE_AM)
    first = make_appointment('A1', NINE_AM)
    assert sorted([second, first], key=appointment_sort_key) == [first, second]


def test_id_tie_break_is_case_sensitive() -> None:
    upper = make_appointment('A1', NINE_AM)
    lower = make_appointment('a1', NINE_AM)
    assert sorted([lower, upper], key=appointment_sort_key) == [upper, lower]


def test_key_has_no_side_effects() -> None:
    appointment = make_appointment('A1', NINE_AM)
    before = repr(appointment)
    appointment_sort_key(appointment)
    assert repr(appointment) == before
    assert appointment.status is AppointmentStatus.SCHEDULED


# select_appointments


def test_select_returns_only_that_practitioner() -> None:
    source = mixed_appointments()
    result = select_appointments(source, 'D2')
    assert [a.appointment_id for a in result] == ['B1']
    assert all(a.practitioner is OTHER_PRACTITIONER for a in result)


def test_select_without_status_returns_every_status_sorted() -> None:
    result = select_appointments(mixed_appointments(), 'D1')
    assert [a.appointment_id for a in result] == ['A1', 'A4', 'A2', 'A3']


@pytest.mark.parametrize(
    ('status', 'expected_ids'),
    [
        (AppointmentStatus.SCHEDULED, ['A1', 'A3']),
        (AppointmentStatus.CANCELLED, ['A2']),
        (AppointmentStatus.COMPLETED, ['A4']),
    ],
)
def test_select_filters_by_each_status(
    status: AppointmentStatus,
    expected_ids: list[str],
) -> None:
    result = select_appointments(mixed_appointments(), 'D1', status)
    assert [a.appointment_id for a in result] == expected_ids
    assert all(a.status is status for a in result)


def test_select_returns_the_stored_objects() -> None:
    source = mixed_appointments()
    result = select_appointments(source, 'D1')
    assert all(any(a is s for s in source) for a in result)


def test_select_does_not_change_source_list_or_appointments() -> None:
    source = mixed_appointments()
    before = snapshot(source)
    select_appointments(source, 'D1')
    select_appointments(source, 'D1', AppointmentStatus.CANCELLED)
    assert snapshot(source) == before


def test_select_returns_a_new_list_even_when_already_sorted() -> None:
    source = [make_appointment('A1', NINE_AM), make_appointment('A2', TEN_AM)]
    result = select_appointments(source, 'D1')
    assert result == source
    assert result is not source


def test_select_repeated_calls_give_the_same_result() -> None:
    source = mixed_appointments()
    first = select_appointments(source, 'D1')
    second = select_appointments(source, 'D1')
    assert first == second
    assert first is not second


def test_select_empty_source_returns_empty_list() -> None:
    source: list[Appointment] = []
    result = select_appointments(source, 'D1')
    assert result == []
    assert result is not source


def test_select_no_matches_returns_empty_list() -> None:
    source = mixed_appointments()
    assert select_appointments(source, 'D9') == []
    assert select_appointments(
        [make_appointment('B1', NINE_AM, OTHER_PRACTITIONER)],
        'D2',
        AppointmentStatus.CANCELLED,
    ) == []
