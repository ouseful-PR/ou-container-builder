"""Tests for the jupyter_notebook section of the ou_container_builder.validator module."""
from copy import deepcopy

from ou_container_builder.validator import validate_settings


REQUIRED_SETTINGS = {
    'module': {
        'code': 'TEST',
        'presentation': '1'
    },
    'type': 'jupyter-notebook'
}


def test_jupyter_notebook_config():
    """Test that the optional packages settings pass."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['jupyter_notebook'] = {
        'default_url': 'default'
    }

    validated = validate_settings(settings)
    assert isinstance(validated, dict) is True


def test_invalid_default_url():
    """Test that an invalid packages source fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['jupyter_notebook'] = {
        'default_url': ''
    }

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
