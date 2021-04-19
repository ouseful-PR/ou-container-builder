"""Build containers based on a Jupyter Notebook."""
import os

from jinja2 import Environment


def generate(context: str, env: Environment, settings: dict):
    """Generate the Dockerfile for a Jupyter Notebook container.

    :param context: The context path within which the generation is running
    :type context: str
    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The settings parsed from the configuration file
    :type settings: dict
    """
    with open(os.path.join(context, 'Dockerfile'), 'w') as out_f:
        if settings['type'] == 'jupyter-notebook':
            tmpl = env.get_template('dockerfile/jupyter-notebook.jinja2')
        out_f.write(tmpl.render(**settings))

    if settings['type'] == 'jupyter-notebook':
        with open(os.path.join(context, 'build', 'jupyter_notebook_config.py'), 'w') as out_f:
            tmpl = env.get_template('jupyter_notebook_config.py')
            out_f.write(tmpl.render(**settings))
        with open(os.path.join(context, 'build', 'start-notebook.sh'), 'w') as out_f:
            tmpl = env.get_template('start-notebook.sh')
            out_f.write(tmpl.render(**settings))
