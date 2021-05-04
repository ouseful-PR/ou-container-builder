"""Tests for the packs section of the ou_container_builder.validator module."""
from copy import deepcopy

from ou_container_builder.validator import validate_settings


REQUIRED_SETTINGS = {
    'module': {
        'code': 'TEST',
        'presentation': '1'
    },
    'type': 'jupyter-notebook'
}


def test_packs_config():
    """Test that the optional packs settings pass."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['packs'] = [
        'tutorial-server'
    ]

    validated = validate_settings(settings)
    assert isinstance(validated, dict) is True


def test_invalid_packs():
    """Test that an invalid packages source fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['packs'] = [
        'missing'
    ]

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
    assert 'packs: invalid value missing'
