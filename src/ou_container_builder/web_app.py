"""Build containers housing a single web application."""
import os

from jinja2 import Environment


def generate(context: str, env: Environment, settings: dict):
    """Generate the Dockerfile for a single web application.

    :param context: The context path within which the generation is running
    :type context: str
    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The settings parsed from the configuration file
    :type settings: dict
    """
    with open(os.path.join(context, 'Dockerfile'), 'w') as out_f:
        if settings['type'] == 'web-app':
            tmpl = env.get_template('dockerfile/web-app.jinja2')
        out_f.write(tmpl.render(**settings))

    with open(os.path.join(context, 'build', 'start-web-app.sh'), 'w') as out_f:
        tmpl = env.get_template('start-web-app.sh')
        out_f.write(tmpl.render(**settings))
