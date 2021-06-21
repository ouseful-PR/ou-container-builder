"""The main OU Container Builder commandline application."""
import click
import os
import shutil
import subprocess

from copy import deepcopy
from jinja2 import Environment, PackageLoader
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from . import jupyter_notebook, web_app
from .validator import validate_settings


def merge_settings(base: dict, new: dict) -> dict:
    """Return a new dictionary created by merging the settings from ``new`` into ``base``.

    :param base: The base dictionary to merge into
    :type base: ``dict``
    :param new: The new dictionary to merge
    :type new: ``dict``
    :return: A new merged dictionary
    :rtype: ``dict``
    """
    result = {}

    for base_key, base_value in list(base.items()):
        if base_key not in new:
            result[base_key] = deepcopy(base_value)
        else:
            if isinstance(base_value, list):
                result[base_key] = list(base_value + new[base_key])
            elif isinstance(base_value, dict):
                result[base_key] = merge_settings(base_value, new[base_key])
            else:
                result[base_key] = new[base_key]
    for new_key, new_value in list(new.items()):
        if new_key not in base:
            result[new_key] = deepcopy(new_value)
    return result


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

        if os.path.exists(os.path.join(context, 'ou-builder-build')):
            shutil.rmtree(os.path.join(context, 'ou-builder-build'))
        os.makedirs(os.path.join(context, 'ou-builder-build'))

        # Handle packs
        if 'packs' in settings and settings['packs']:
            if 'tutorial-server' in settings['packs']:
                settings = merge_settings(settings, {'packages': {'pip': ['tutorial-server>=0.7.0']}})
                with open(os.path.join(context, 'ou-builder-build', 'tutorial-server.ini'), 'w') as out_f:
                    tmpl = env.get_template('tutorial-server.ini')
                    out_f.write(tmpl.render(**settings))
            if 'tutorial-server-php' in settings['packs']:
                settings = merge_settings(settings, {'packages': {'apt': ['php-cgi']}})
            if 'mariadb' in settings['packs']:
                settings = merge_settings(settings, {
                    'packages': {
                        'apt': ['mariadb-server', 'sudo']
                    },
                    'scripts': {
                        'build': [
                            {
                                'inline': [
                                    'mkdir -p /run/mysqld',
                                    'sed -e "s#datadir.*=.*#datadir = $HOME/mariadb#" -e "s#user.*=.*#user = ou#" -i /etc/mysql/mariadb.conf.d/50-server.cnf',  # noqa: E501
                                    'chown ou: /var/log/mysql/error.log /run/mysqld'
                                ]
                            },
                        ],
                        'startup': [
                            {
                                'cmd': 'sudo /usr/bin/mariadb-setup.sh'
                            }
                        ]
                    },
                    'services': [
                        'mysql'
                    ],
                    'content': [
                        {
                            'source': '/var/lib/mysql',
                            'target': 'mariadb',
                            'overwrite': 'never'
                        }
                    ]
                })
                with open(os.path.join(context, 'ou-builder-build', 'mariadb-setup.sh'), 'w') as out_f:
                    tmpl = env.get_template('mariadb-setup.sh')
                    out_f.write(tmpl.render(**settings))

        settings = validate_settings(settings)
        if isinstance(settings, dict):

            # Handle automatic hacks
            if 'packages' in settings and 'apt' in settings['packages']:
                if 'openjdk-11-jdk' in settings['packages']['apt']:
                    if 'hacks' in settings:
                        if 'missing-man1' not in settings['hacks']:
                            settings['hacks'].append('missing-man1')
                    else:
                        settings['hacks'] = ['missing-man1']

            # Sort package lists
            if 'packages' in settings:
                if 'apt' in settings['packages']:
                    settings['packages']['apt'].sort()
                if 'pip' in settings['packages']:
                    settings['packages']['pip'].sort()

            # Generate the content distribution settings
            if ('content' in settings and settings['content']) \
                    or ('scripts' in settings and 'startup' in settings['scripts'] and settings['scripts']['startup']) \
                    or ('services' in settings and settings['services']):
                with open(os.path.join(context, 'ou-builder-build', 'content_config.yaml'), 'w') as out_f:
                    tmpl = env.get_template('content_config.yaml')
                    out_f.write(tmpl.render(**settings))

            # Generate the Dockerfiles
            if settings['type'] == 'jupyter-notebook':
                jupyter_notebook.generate(context, env, settings)
            elif settings['type'] == 'web-app':
                web_app.generate(context, env, settings)

            if build:
                cmd = ['docker', 'build', context]
                if tag:
                    for t in tag:
                        cmd.append('--tag')
                        cmd.append(f'mmh352/{settings["module"]["code"].lower()}' +
                                   f'-{settings["module"]["presentation"].lower()}:{t}')
                subprocess.run(cmd)
                if clean:
                    os.unlink(os.path.join(context, 'Dockerfile'))
                    if os.path.exists(os.path.join(context, 'ou-builder-build')):
                        shutil.rmtree(os.path.join(context, 'ou-builder-build'))
        else:
            click.echo(click.style('There are errors in your configuration settings:', fg='red'), err=True)
            click.echo(err=True)
            for error in settings:
                click.echo(error, err=True)
    else:
        click.echo(click.style('There are errors in your configuration settings:', fg='red'), err=True)
        click.echo(err=True)
        for error in settings:
            click.echo(error, err=True)


if __name__ == '__main__':
    main()
