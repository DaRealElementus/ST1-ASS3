"""Console helpers and a small runnable starting demonstration."""


import re
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM; raise ValueError for invalid input."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', text
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')
    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM',
        ) from None


def format_appointment(appointment: Appointment) -> str:
    """Return readable synthetic appointment details without changing
    state.
    """
    return (
        f'{appointment.appointment_id}: '
        f'{appointment.patient.patient_id} with '
        f'{appointment.practitioner.practitioner_id}, '
        f'{appointment.date_time:%Y-%m-%d %H:%M}, {appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate supplied registration and booking using synthetic
    records.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'DR1',
        'Taylor Example',
        'General practice',
    )
    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    print('Session-only data: records are lost on exit.')


MENU = """
SmartCare menu
1. Register patient
2. Register practitioner
3. Find patient
4. Find practitioner
5. Book appointment
6. Find appointment
7. Cancel appointment
8. List practitioner appointments
0. Exit"""


def register_patient(patients: PatientService) -> None:
    """Read patient details and register them through the service."""
    patient = patients.register_patient(
        input('Patient ID: '),
        input('Patient name: '),
    )
    print(f'Registered patient {patient.patient_id}: {patient.name}')


def register_practitioner(practitioners: PractitionerService) -> None:
    """Read practitioner details and register them through the service."""
    practitioner = practitioners.register_practitioner(
        input('Practitioner ID: '),
        input('Practitioner name: '),
        input('Specialty: '),
    )
    print(
        f'Registered practitioner {practitioner.practitioner_id}: '
        f'{practitioner.name} ({practitioner.specialty})',
    )


def find_patient(patients: PatientService) -> None:
    """Read a patient ID and show the stored patient."""
    patient = patients.find_patient(input('Patient ID: '))
    print(f'{patient.patient_id}: {patient.name}')


def find_practitioner(practitioners: PractitionerService) -> None:
    """Read a practitioner ID and show the stored practitioner."""
    practitioner = practitioners.find_practitioner(input('Practitioner ID: '))
    print(
        f'{practitioner.practitioner_id}: {practitioner.name} '
        f'({practitioner.specialty})',
    )


def book_appointment(appointments: AppointmentService) -> None:
    """Read booking details and book through the service."""
    appointment = appointments.book_appointment(
        input('Appointment ID: '),
        input('Patient ID: '),
        input('Practitioner ID: '),
        parse_date_time(input('Date/time (YYYY-MM-DD HH:MM): ')),
    )
    print(f'Booked {format_appointment(appointment)}')


def find_appointment(appointments: AppointmentService) -> None:
    """Read an appointment ID and show the stored appointment."""
    print(format_appointment(
        appointments.find_appointment(input('Appointment ID: ')),
    ))


def run_menu() -> None:
    """Run the register/find/book/cancel/list/exit menu.

    Call services, recover from expected input errors, and keep this
    session's data until exit.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    actions = {
        '1': lambda: register_patient(patients),
        '2': lambda: register_practitioner(practitioners),
        '3': lambda: find_patient(patients),
        '4': lambda: find_practitioner(practitioners),
        '5': lambda: book_appointment(appointments),
        '6': lambda: find_appointment(appointments),
    }
    while True:
        print(MENU)
        try:
            choice = input('Choose an option: ').strip()
        except EOFError:
            choice = '0'
        if choice == '0':
            print('Session-only data: records are lost on exit.')
            return
        if choice in ('7', '8'):
            print('Not yet available.')
            continue
        action = actions.get(choice)
        if action is None:
            print('Unknown option; choose a number from the menu.')
            continue
        try:
            action()
        except (ValueError, LookupError) as error:
            print(f'Error: {error}')
        except EOFError:
            print('Session-only data: records are lost on exit.')
            return
