"""The main OU Container Builder commandline application."""
import click
import os
import shutil
import subprocess

from jinja2 import Environment, PackageLoader
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from . import jupyter_notebook, web_app
from .validator import validate_settings


@click.command()
@click.option('-c', '--context',
              default='.',
              help='Context within which the container will be built',
              show_default=True)
@click.option('-b/-nb', '--build/--no-build',
              default=True,
              help='Automatically build the container',
              show_default=True)
@click.option('--clean/--no-clean',
              default=True,
              help='Automatically clean up after building the container',
              show_default=True)
@click.option('--tag',
              multiple=True,
              help='Automatically tag the generated image')
def main(context, build, clean, tag):
    """Build your OU Container."""
    with open(os.path.join(context, 'ContainerConfig.yaml')) as config_f:
        settings = load(config_f, Loader=Loader)
    settings = validate_settings(settings)

    if isinstance(settings, dict):
        env = Environment(loader=PackageLoader('ou_container_builder', 'templates'),
                          autoescape=False)

        if os.path.exists(os.path.join(context, 'build')):
            shutil.rmtree(os.path.join(context, 'build'))
        os.makedirs(os.path.join(context, 'build'))

        if settings['type'] == 'jupyter-notebook':
            jupyter_notebook.generate(context, env, settings)
        elif settings['type'] == 'web-app':
            web_app.generate(context, env, settings)

        if 'content' in settings and settings['content']:
            with open(os.path.join(context, 'build', 'content_config.yaml'), 'w') as out_f:
                tmpl = env.get_template('content_config.yaml')
                out_f.write(tmpl.render(**settings))

        if build:
            cmd = ['docker', 'build', context]
            if tag:
                for t in tag:
                    cmd.append('--tag')
                    cmd.append(f'mmh352/{settings["module"]["code"].lower()}' +
                               '-{settings["module"]["presentation"].lower()}:{t}')
            subprocess.run(cmd)
            if clean:
                os.unlink(os.path.join(context, 'Dockerfile'))
                if os.path.exists(os.path.join(context, 'build')):
                    shutil.rmtree(os.path.join(context, 'build'))
    else:
        click.echo(click.style('There are errors in your configuration settings:', fg='red'), err=True)
        click.echo(err=True)

        for error in settings:
            click.echo(error, err=True)


if __name__ == '__main__':
    main()
