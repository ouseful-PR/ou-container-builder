"""Tests for the sources section of the ou_container_builder.validator module."""
from copy import deepcopy

from ou_container_builder.validator import validate_settings


REQUIRED_SETTINGS = {
    'module': {
        'code': 'TEST',
        'presentation': '1'
    },
    'type': 'jupyter-notebook'
}


def test_sources_config():
    """Test that the optional sources settings pass."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['sources'] = {
        'apt': [
            {
                'name': 'source1',
                'key': 'https://example.org/url',
                'deb': 'deb somewhere dist'
            }
        ]
    }

    validated = validate_settings(settings)
    assert isinstance(validated, dict) is True


def test_empty_sources():
    """Test that an empty source list passes."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['sources'] = {
        'apt': []
    }

    validated = validate_settings(settings)
    assert isinstance(validated, dict) is True


def test_missing_keys():
    """Test that missing keys generate an error."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['sources'] = {
        'apt': [
            {
            }
        ]
    }

    validated = validate_settings(settings)
    assert isinstance(validated, list) is True
    assert len(validated) == 3
    assert 'sources.apt.0.deb: required field' in validated
    assert 'sources.apt.0.key: required field' in validated
    assert 'sources.apt.0.name: required field' in validated
