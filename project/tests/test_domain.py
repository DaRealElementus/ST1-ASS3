"""Domain checks: Patient and Practitioner construction and validation.

Contract (smartcare/domain.py): every required text field is trimmed and
must be a non-blank string; anything else raises ValueError.
"""

from typing import Any

import pytest

from smartcare.domain import Patient, Practitioner

# Values that must be rejected for any required text field.
INVALID_TEXT = ['', ' ', '   ', '\t', '\n', ' \t\n ', None, 42, 3.5, b'P1', []]


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