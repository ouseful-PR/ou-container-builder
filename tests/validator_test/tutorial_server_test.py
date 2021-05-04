"""Tests for the tutorial_server section of the ou_container_builder.validator module."""
from copy import deepcopy

from ou_container_builder.validator import validate_settings


REQUIRED_SETTINGS = {
    'module': {
        'code': 'TEST',
        'presentation': '1'
    },
    'type': 'jupyter-notebook'
}


def test_tutorial_server_config():
    """Test that the optional tutorial_server settings pass."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['tutorial_server'] = {
        'parts': [
            {
                'name': 'tutorial',
                'type': 'tutorial',
                'path': 'tutorial'
            },
            {
                'name': 'workspace',
                'type': 'workspace',
                'path': 'workspace'
            }
        ],
        'default': 'tutorial'
    }

    validated = validate_settings(settings)
    assert isinstance(validated, dict) is True


def test_missing_part_keys():
    """Test that missing part keys fail."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['tutorial_server'] = {
        'parts': [
            {
            }
        ],
        'default': 'tutorial'
    }

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
    assert 'tutorial_server.parts.0.name: required field' in validated
    assert 'tutorial_server.parts.0.type: required field' in validated
    assert 'tutorial_server.parts.0.path: required field' in validated


def test_empty_values_fail():
    """Test that empty values fail."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['tutorial_server'] = {
        'parts': [
            {
                'name': '',
                'type': 'tutorial',
                'path': ''
            }
        ],
        'default': ''
    }

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
    assert 'tutorial_server.parts.0.name: empty values not allowed' in validated
    assert 'tutorial_server.default: empty values not allowed' in validated


def test_invalid_types_fail():
    """Test that invalid part types fail."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['tutorial_server'] = {
        'parts': [
            {
                'name': 'tutorial',
                'type': 'files',
                'path': ''
            }
        ],
        'default': 'tutorial'
    }

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
    assert 'tutorial_server.parts.0.type: unallowed value files' in validated
