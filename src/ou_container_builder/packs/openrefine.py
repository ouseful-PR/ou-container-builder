"""Pack to install the OpenRefine."""
from jinja2 import Environment

from ..utils import merge_settings


def apply_pack(context: str, env: Environment, settings: dict) -> dict:
    """Apply the openrefine pack.

    This ensures that the openrefine application is installed and that the configured database is set up in the user's
    home-directory.

    The openrefine application is not started by default.

    We should perhaps provide a setting that does not start it by default,
    eg for use in Jupyter container where a proxy call will autostart it.

    :param context: The context path within which the generation is running
    :type context: str
    :param env: The Jinja2 environment to use for loading and rendering templates
    :type env: :class:`~jinja2.environment.Environment`
    :param settings: The settings parsed from the configuration file
    :type settings: dict
    :return: The updated settings
    :rtype: dict
    """
    # Latest stable OpenRefine version: '3.4.1'
    openrefine_repo = "https://github.com/OpenRefine/OpenRefine/releases/download/"
    version = settings["openrefine"]["version"]
    settings = merge_settings(settings, {
        'packages': {
            'apt': ['wget', 'openjdk-11-jre'],
        },
        'scripts': {
            'build': [
                {
                    'commands': [
                        f"wget --no-check-certificate \
                            {openrefine_repo}{version}/openrefine-linux-{version}.tar.gz",
                        f"tar -xzf openrefine-linux-{version}.tar.gz",
                        f"rm openrefine-linux-{version}.tar.gz",
                        f"mv openrefine-{version} /var/openrefine",
                        "mkdir -p $HOME/openrefine"
                    ]
                },
            ],
            'startup': [
                {
                    'commands': [
                    ]
                }
            ]
        },
        'services': [
        ],
        'content': [
        ]
    })
    return settings
