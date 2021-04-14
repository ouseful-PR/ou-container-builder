import click

from cerberus import Validator


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
        'allowed': ['jupyter-notebook']
    },
    'content': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'source': {
                    'type': 'string',
                    'required': True,
                },
                'target': {
                    'type': 'string',
                    'required': True,
                    'default': ''
                },
                'overwrite': {
                    'type': 'string',
                    'allowed': ['always', 'if-missing', 'if-unchanged']
                }
            }
        }
    }
}


def validate_settings(settings):
    """Validate the configuration settings against the configuration schema."""
    validator = Validator(schema)
    if settings and validator.validate(settings):
        return validator.normalized(settings)
    elif settings is None:
        click.echo(click.style('Your configuration file is empty', fg='red'), err=True)
    else:
        click.echo(click.style('There are errors in your configuration settings:', fg='red'), err=True)
        click.echo()

        def walk_error_tree(err, path):
            if isinstance(err, dict):
                for key, value in err.items():
                    walk_error_tree(value, path + (str(key), ))
            elif isinstance(err, list):
                for sub_err in err:
                    walk_error_tree(sub_err, path)
            else:
                print(f'{".".join(path)}: {err}')

        walk_error_tree(validator.errors, ())
        return False
