"""Build containers housing one or more web applications."""
import os

from jinja2 import Environment

from ..utils import merge_settings


def setup(context, env, settings):
    """Run the setup for the Web Applications generator."""
    settings = merge_settings(settings, {
        'packages': {
            'pip': [
                'jupyter-server-proxy',
                'jupyterhub==1.3.0'
            ]
        },
        'content': [
            {
                'source': 'ou-builder-build/start-web-app.sh',
                'target': '/usr/bin/start.sh',
                'overwrite': 'always'
            },
            {
                'source': 'ou-builder-build/jupyter_server_config.py',
                'target': '/etc/jupyter/jupyter_server_config.py',
                'overwrite': 'always'
            }
        ],
        'scripts': {
            'build': [
                {
                    'inline': [
                        'chmod a+x /usr/bin/start.sh'
                    ]
                }
            ]
        }
    })
    return settings


def generate(context: str, env: Environment, settings: dict):
    """Generate the Dockerfile for one or more web applications.

    :param context: The context path within which the generation is running
    :type context: str
    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The settings parsed from the configuration file
    :type settings: dict
    """
    with open(os.path.join(context, 'ou-builder-build', 'start-web-app.sh'), 'w') as out_f:
        tmpl = env.get_template('generators/web_app/start.sh')
        out_f.write(tmpl.render(**settings))

    with open(os.path.join(context, 'ou-builder-build', 'jupyter_server_config.py'), 'w') as out_f:
        tmpl = env.get_template('generators/web_app/jupyter_server_config.py')
        out_f.write(tmpl.render(**settings))

    with open(os.path.join(context, 'Dockerfile'), 'w') as out_f:
        if settings['type'] == 'web-app':
            tmpl = env.get_template('Dockerfile.jinja2')
        out_f.write(tmpl.render(**settings))
