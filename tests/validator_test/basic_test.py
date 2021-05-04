"""Basic tests of the ou_container_builder.validator module."""
from copy import deepcopy

from ou_container_builder.validator import validate_settings


REQUIRED_SETTINGS = {
    'module': {
        'code': 'TEST',
        'presentation': '1'
    },
    'type': 'jupyter-notebook'
}


def test_required_config():
    """Test the minimal required configuration."""
    settings = deepcopy(REQUIRED_SETTINGS)

    assert isinstance(validate_settings(settings), dict) is True


def test_missing_module_config():
    """Test that a missing module setting fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    del settings['module']

    errors = validate_settings(settings)

    assert isinstance(errors, list) is True
    assert len(errors) == 1
    assert errors[0] == 'module: required field'


def test_missing_module_code_config():
    """Test that a missing module.code setting fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    del settings['module']['code']

    errors = validate_settings(settings)

    assert isinstance(errors, list) is True
    assert len(errors) == 1
    assert errors[0] == 'module.code: required field'


def test_missing_module_presentation_config():
    """Test that a missing module.presentation setting fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    del settings['module']['presentation']

    errors = validate_settings(settings)

    assert isinstance(errors, list) is True
    assert len(errors) == 1
    assert errors[0] == 'module.presentation: required field'


def test_multiple_errors_config():
    """Test that multiple missing fields produce multiple errors."""
    settings = deepcopy(REQUIRED_SETTINGS)
    del settings['module']['code']
    del settings['module']['presentation']

    errors = validate_settings(settings)

    assert isinstance(errors, list) is True
    assert len(errors) == 2
    assert errors[0] == 'module.code: required field'
    assert errors[1] == 'module.presentation: required field'


def test_missing_type_config():
    """Test that a missing type setting fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    del settings['type']

    errors = validate_settings(settings)

    assert isinstance(errors, list) is True
    assert len(errors) == 1
    assert errors[0] == 'type: required field'


def test_invalid_type_config():
    """Test that an invalid type setting fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['type'] = 'invalid'

    errors = validate_settings(settings)

    assert isinstance(errors, list) is True
    assert len(errors) == 1
    assert errors[0] == 'type: unallowed value invalid'


def test_optional_content_config():
    """Test that the optional content settings pass."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['content'] = [
        {
            'source': 'from/here',
            'target': 'there',
            'overwrite': 'always'
        },
        {
            'source': 'from/here',
            'target': 'there',
            'overwrite': 'never'
        },
        {
            'source': 'from/here',
            'target': 'there',
            'overwrite': 'if-unchanged'
        }
    ]

    assert isinstance(validate_settings(settings), dict) is True


def test_optional_content_normalisation_config():
    """Test that the content.target normalisation passes."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['content'] = [
        {
            'source': 'from/here',
            'overwrite': 'always'
        },
    ]

    settings = validate_settings(settings)

    assert isinstance(settings, dict) is True
    assert 'content' in settings
    assert len(settings['content']) == 1
    assert 'target' in settings['content'][0]
    assert settings['content'][0]['target'] == ''

    settings = deepcopy(REQUIRED_SETTINGS)
    settings['content'] = [
        {
            'source': 'from/here',
            'target': None,
            'overwrite': 'always'
        },
    ]

    settings = validate_settings(settings)

    assert isinstance(settings, dict) is True
    assert 'content' in settings
    assert len(settings['content']) == 1
    assert 'target' in settings['content'][0]
    assert settings['content'][0]['target'] == ''


def test_invalid_content_config():
    """Test that a non-list content structure fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['content'] = {
        'source': 'from/here',
        'target': 'there',
        'overwrite': 'always'
    }

    errors = validate_settings(settings)

    assert isinstance(errors, list) is True
    assert len(errors) == 1
    assert errors[0] == 'content: must be of list type'


def test_invalid_content_source_config():
    """Test that an invalid content.source setting fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['content'] = [
        {
            'source': '',
            'target': 'there',
            'overwrite': 'always'
        }
    ]

    errors = validate_settings(settings)

    assert isinstance(errors, list) is True
    assert len(errors) == 1
    assert errors[0] == 'content.0.source: empty values not allowed'


def test_invalid_content_overwrite_config():
    """Test that an invalid content.overwrite setting fails."""
    settings = deepcopy(REQUIRED_SETTINGS)
    settings['content'] = [
        {
            'source': 'from/here',
            'target': 'there',
            'overwrite': 'sometimes'
        }
    ]

    errors = validate_settings(settings)

    assert isinstance(errors, list) is True
    assert len(errors) == 1
    assert errors[0] == 'content.0.overwrite: unallowed value sometimes'
