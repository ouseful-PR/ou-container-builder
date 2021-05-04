"""Tests for the web_apps section of the ou_container_builder.validator module."""
from copy import deepcopy

from ou_container_builder.validator import validate_settings


REQUIRED_SETTINGS = {
    'module': {
        'code': 'TEST',
        'presentation': '1'
    },
    'type': 'jupyter-notebook'
}


def test_web_apps_config():
    """Test that the optional web_apps settings pass."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['web_apps'] = [
        {
            'path': 'mount',
            'cmdline': [
                'cmd',
                'param'
            ],
            'port': 342,
            'default': True
        }
    ]

    validated = validate_settings(settings)
    assert isinstance(validated, dict) is True


def test_default_values():
    """Test that the default values are set correctly."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['web_apps'] = [
        {
            'path': 'mount',
            'cmdline': [
                'cmd',
                'param'
            ]
        }
    ]

    validated = validate_settings(settings)
    assert isinstance(validated, dict) is True
    assert validated['web_apps'][0]['port'] == 0
    assert validated['web_apps'][0]['default'] is False


def test_invalid_web_apps_config():
    """Test that an invalid web_apps config fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['web_apps'] = {}

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True


def test_invalid_web_app():
    """Test that an invalid packages source fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['web_apps'] = [
        {}
    ]

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
    assert 'web_apps.0.path: required field' in validated
    assert 'web_apps.0.cmdline: required field' in validated


def test_empty_values():
    """Test that an empty settings fail."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['web_apps'] = [
        {
            'path': '',
            'cmdline': []
        }
    ]

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
    assert 'web_apps.0.path: empty values not allowed' in validated
    assert 'web_apps.0.cmdline: empty values not allowed' in validated


def test_cmdline_must_be_list():
    """Tests that the cmdline value must be a list."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['web_apps'] = [
        {
            'path': 'mount',
            'cmdline': 'cmd'
        }
    ]

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
    assert 'web_apps.0.cmdline: must be of list type' in validated


def test_port_must_be_numeric():
    """Tests that the port value must be a numeric value."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['web_apps'] = [
        {
            'path': 'mount',
            'cmdline': [
                'cmd',
                'param'
            ],
            'port': '342'
        }
    ]

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
    assert 'web_apps.0.port: must be of integer type' in validated


def test_default_must_be_boolean():
    """Tests that the default value must be a boolean value."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['web_apps'] = [
        {
            'path': 'mount',
            'cmdline': [
                'cmd',
                'param'
            ],
            'default': 'true'
        }
    ]

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
    assert 'web_apps.0.default: must be of boolean type' in validated
