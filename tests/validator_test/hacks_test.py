"""Tests for the hacks section of the ou_container_builder.validator module."""
from copy import deepcopy

from ou_container_builder.validator import validate_settings


REQUIRED_SETTINGS = {
    'module': {
        'code': 'TEST',
        'presentation': '1'
    },
    'type': 'jupyter-notebook'
}


def test_hacks_config():
    """Test that the optional hacks settings pass."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['hacks'] = [
        'missing-man1'
    ]

    validated = validate_settings(settings)
    assert isinstance(validated, dict) is True


def test_invalid_hacks():
    """Test that an invalid packages source fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['packs'] = [
        'does-not-exist'
    ]

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
    assert 'hacks: invalid value does-not-exist'
