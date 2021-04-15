"""Configuration validator for the OU Container Builder ContainerConfig.yaml."""
from cerberus import Validator
from typing import Union


schema = {
    'module': {
        'type': 'dict',
        'required': True,
        'schema': {
            'code': {
                'type': 'string',
                'required': True
            },
            'presentation': {
                'type': 'string',
                'required': True
            }
        }
    },
    'type': {
        'type': 'string',
        'required': True,
        'allowed': ['jupyter-notebook']
    },
    'content': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'required': True,
            'schema': {
                'source': {
                    'type': 'string',
                    'required': True,
                    'empty': False
                },
                'target': {
                    'type': 'string',
                    'default': ''
                },
                'overwrite': {
                    'type': 'string',
                    'required': True,
                    'allowed': ['always', 'never', 'if-unchanged']
                }
            }
        }
    }
}


def validate_settings(settings: dict) -> Union[dict, bool]:
    """Validate the configuration settings against the configuration schema.

    :param settings: The settings parsed from the configuration file
    :type settings: dict
    :return: The validated and normalised settings if they are valid, otherwise ``False``
    :rtype: boolean or dict
    """
    validator = Validator(schema)
    if settings and validator.validate(settings):
        return validator.normalized(settings)
    elif settings is None:
        return ['Your configuration file is empty']
    else:
        error_list = []

        def walk_error_tree(err, path):
            if isinstance(err, dict):
                for key, value in err.items():
                    walk_error_tree(value, path + (str(key), ))
            elif isinstance(err, list):
                for sub_err in err:
                    walk_error_tree(sub_err, path)
            else:
                error_list.append(f'{".".join(path)}: {err}')

        walk_error_tree(validator.errors, ())
        return error_list
