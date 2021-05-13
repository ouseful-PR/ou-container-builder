"""Build containers housing one or more web applications."""
import os

from jinja2 import Environment


def generate(context: str, env: Environment, settings: dict):
    """Generate the Dockerfile for one or more web applications.

    :param context: The context path within which the generation is running
    :type context: str
    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The settings parsed from the configuration file
    :type settings: dict
    """
    if 'packs' in settings and 'tutorial-server' in settings['packs']:
        settings['web_app'] = {
            'cmdline': 'python3 -m tutorial_server --config=/etc/tutorial-server/production.ini --port={port} ' +
                       '--basepath=$JUPYTERHUB_SERVICE_PREFIX/',
            'port': 0
        }

    with open(os.path.join(context, 'Dockerfile'), 'w') as out_f:
        if settings['type'] == 'web-app':
            tmpl = env.get_template('dockerfile/web-app.jinja2')
        out_f.write(tmpl.render(**settings))

    with open(os.path.join(context, 'ou-builder-build', 'start-web-app.sh'), 'w') as out_f:
        tmpl = env.get_template('start-web-app.sh')
        out_f.write(tmpl.render(**settings))

    with open(os.path.join(context, 'ou-builder-build', 'jupyter_server_config.py'), 'w') as out_f:
        tmpl = env.get_template('jupyter_server_config.py')
        out_f.write(tmpl.render(**settings))
