"""Build containers based on a Jupyter Notebook."""
from jinja2 import Environment


def generate(env: Environment, settings: dict):
    """Generate the Dockerfile for a Jupyter Notebook container.

    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The settings parsed from the configuration file
    :type settings: dict
    """
    with open('build/Dockerfile', 'w') as out_f:
        if settings['type'] == 'jupyter-notebook':
            tmpl = env.get_template('dockerfile/jupyter-notebook.jinja2')
        out_f.write(tmpl.render(**settings))

    if settings['type'] == 'jupyter-notebook':
        with open('build/jupyter_notebook_config.py', 'w') as out_f:
            tmpl = env.get_template('jupyter_notebook_config.py')
            out_f.write(tmpl.render(**settings))
        with open('build/start-notebook.sh', 'w') as out_f:
            tmpl = env.get_template('start-notebook.sh')
            out_f.write(tmpl.render(**settings))
