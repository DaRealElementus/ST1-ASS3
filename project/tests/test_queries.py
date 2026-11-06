"""Query checks: appointment_sort_key ordering.

Contract (smartcare/queries.py): the key is (date_time, appointment_id),
so appointments order by time first and ID breaks ties. Building the key
has no side effects.
"""

from datetime import datetime

from smartcare.domain import Appointment, AppointmentStatus, Patient, Practitioner
from smartcare.queries import appointment_sort_key

PATIENT = Patient('P1', 'Pat Example')
PRACTITIONER = Practitioner('D1', 'Dr Example', 'General')
NINE_AM = datetime(2026, 10, 1, 9, 0)
TEN_AM = datetime(2026, 10, 1, 10, 0)


def make_appointment(appointment_id: str, date_time: datetime) -> Appointment:
    """Return a scheduled appointment with shared synthetic participants."""
    return Appointment(appointment_id, PATIENT, PRACTITIONER, date_time)


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
