"""Tests for the packages section of the ou_container_builder.validator module."""
from copy import deepcopy

from ou_container_builder.validator import validate_settings


REQUIRED_SETTINGS = {
    'module': {
        'code': 'TEST',
        'presentation': '1'
    },
    'type': 'jupyter-notebook'
}


def test_packages_config():
    """Test that the optional packages settings pass."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['packages'] = {
        'apt': [
            'package1',
            'package2'
        ],
        'pip': [
            'package1',
            'package2'
        ]
    }

    validated = validate_settings(settings)
    assert isinstance(validated, dict) is True


def test_invalid_packages_source():
    """Test that an invalid packages source fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['packages'] = {
        'invalid': [
            'package1',
            'package2'
        ]
    }

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
