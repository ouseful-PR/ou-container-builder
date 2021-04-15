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

from . import jupyter_notebook
from .validator import validate_settings


@click.command()
@click.option('-c', '--config',
              type=click.File(),
              default='ContainerConfig.yaml',
              help='Configuration file',
              show_default=True)
@click.option('-b/-nb', '--build/--no-build',
              default=True,
              help='Automatically build the container',
              show_default=True)
@click.option('--clean/--no-clean',
              default=True,
              help='Automatically clean up after building the container',
              show_default=True)
def main(config, build, clean):
    """Build your OU Container."""
    settings = load(config, Loader=Loader)
    settings = validate_settings(settings)

    if isinstance(settings, dict):
        env = Environment(loader=PackageLoader('ou_container_builder', 'templates'),
                          autoescape=False)

        if os.path.exists('build'):
            shutil.rmtree('build')
        shutil.copytree('.', 'build')

        if settings['type'] == 'jupyter-notebook':
            jupyter_notebook.generate(env, settings)

        if 'content' in settings and settings['content']:
            with open('build/content_config.ini', 'w') as out_f:
                tmpl = env.get_template('content_config.ini')
                out_f.write(tmpl.render(**settings))

        if build:
            subprocess.run(('docker', 'build', '.'), cwd='build')
            if clean:
                if os.path.exists('build'):
                    shutil.rmtree('build')
    else:
        click.echo(click.style('There are errors in your configuration settings:', fg='red'), err=True)
        click.echo(err=True)

        for error in settings:
            click.echo(error, err=True)


if __name__ == '__main__':
    main()
