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
        'allowed': ['jupyter-notebook', 'web-app']
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
    },
    'sources': {
        'type': 'dict',
        'schema': {
            'apt': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'name': {
                            'type': 'string',
                            'required': True,
                            'empty': False
                        },
                        'key': {
                            'type': 'string',
                            'required': True,
                            'empty': False,
                        },
                        'deb': {
                            'type': 'string',
                            'required': True,
                            'empty': False,
                        }
                    }
                }
            }
        }
    },
    'packages': {
        'type': 'dict',
        'schema': {
            'apt': {
                'type': 'list',
                'schema': {
                    'type': 'string'
                }
            },
            'pip': {
                'type': 'list',
                'schema': {
                    'type': 'string'
                }
            }
        }
    },
    'scripts': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'inline': {
                    'type': 'list',
                    'schema': {
                        'type': 'string'
                    }
                }
            }
        }
    },
    'jupyter_notebook': {
        'type': 'dict',
        'schema': {
            'default_url': {
                'type': 'string',
                'empty': False
            }
        }
    },
    'web_apps': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'path': {
                    'type': 'string',
                    'required': True,
                    'empty': False
                },
                'cmdline': {
                    'type': 'list',
                    'required': True,
                    'empty': False,
                    'schema': {
                        'type': 'string',
                        'required': True,
                        'empty': False
                    }
                },
                'port': {
                    'type': 'integer',
                    'default': 0
                },
                'default': {
                    'type': 'boolean',
                    'default': False
                },
                'timeout': {
                    'type': 'integer'
                }
            }
        }
    },
    'packs': {
        'type': 'list',
        'schema': {
            'type': 'string',
            'allowed': ['tutorial-server']
        }
    },
    'tutorial_server': {
        'type': 'dict',
        'schema': {
            'parts': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'name': {
                            'type': 'string',
                            'required': True,
                            'empty': False,
                        },
                        'type': {
                            'type': 'string',
                            'required': True,
                            'allowed': ['tutorial', 'workspace']
                        },
                        'path': {
                            'type': 'string',
                            'required': True
                        }
                    }
                }
            },
            'default': {
                'type': 'string',
                'required': True,
                'empty': False
            }
        }
    },
    'hacks': {
        'type': 'list',
        'schema': {
            'type': 'string',
            'required': True,
            'empty': False,
            'allowed': ['missing-man1']
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
