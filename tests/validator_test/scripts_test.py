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


def test_build_scripts_config():
    """Test that the optional scripts settings passes for build scripts."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['scripts'] = {
        'build':     [
            {
                'commands': [
                    'line1',
                    'line2'
                ]
            },
            {
                'commands': [
                    'line1',
                    'line2'
                ]
            }
        ]
    }

    validated = validate_settings(settings)
    assert isinstance(validated, dict) is True


def test_startup_scripts_config():
    """Test that the optional scripts settings passes for startup scripts."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['scripts'] = {
        'startup':     [
            {
                'commands': [
                    'line1',
                    'line2'
                ]
            },
            {
                'commands': '''line1
line2'''
            }
        ]
    }

    validated = validate_settings(settings)
    assert isinstance(validated, dict) is True


def test_shutdown_scripts_config():
    """Test that the optional scripts settings passes for shutdown scripts."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['scripts'] = {
        'shutdown':     [
            {
                'commands': [
                    'line1',
                    'line2'
                ]
            },
            {
                'commands': '''line1
line2'''
            }
        ]
    }

    validated = validate_settings(settings)
    assert isinstance(validated, dict) is True


def test_invalid_script_type():
    """Test that an invalid script type fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['scripts'] = {
        'build': {
            'file': [
                'package1',
                'package2'
            ]
        }
    }

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
