"""Pack to install the MariaDB database."""
import os

from jinja2 import Environment

from ..utils import merge_settings


def apply_pack(context: str, env: Environment, settings: dict):
    """Apply the mariadb pack."""
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
                        'chown ou: /var/log/mysql/error.log /run/mysqld',
                        'chmod a+x /usr/bin/mariadb-setup.sh',
                        'printf "ou ALL=NOPASSWD: /usr/bin/mariadb-setup.sh\\n" > /etc/sudoers.d/99-mariadb'  # noqa: E501
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
            },
            {
                'source': 'ou-builder-build/mariadb-setup.sh',
                'target': '/usr/bin/mariadb-setup.sh',
                'overwrite': 'always'
            }
        ]
    })
    with open(os.path.join(context, 'ou-builder-build', 'mariadb-setup.sh'), 'w') as out_f:
        tmpl = env.get_template('packs/mariadb/setup.sh')
        out_f.write(tmpl.render(**settings))
    return settings
