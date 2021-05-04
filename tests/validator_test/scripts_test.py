"""Tests for the scripts section of the ou_container_builder.validator module."""
from copy import deepcopy

from ou_container_builder.validator import validate_settings


REQUIRED_SETTINGS = {
    'module': {
        'code': 'TEST',
        'presentation': '1'
    },
    'type': 'jupyter-notebook'
}


def test_scripts_config():
    """Test that the optional scripts settings pass."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['scripts'] = [
        {
            'inline': [
                'line1',
                'line2'
            ]
        },
        {
            'inline': [
                'line1',
                'line2'
            ]
        }
    ]

    validated = validate_settings(settings)
    assert isinstance(validated, dict) is True


def test_invalid_script_type():
    """Test that an invalid script type fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['scripts'] = {
        'file': [
            'package1',
            'package2'
        ]
    }

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
