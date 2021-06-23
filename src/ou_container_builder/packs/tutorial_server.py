"""Pack to install the tutorial_sever."""
import os

from ..utils import merge_settings


def apply_pack(settings, env, context):
    """Apply the tutorial-server pack."""
    # Extend the settings
    additional_settings = {
        'packages': {
            'pip': [
                'tutorial-server>=0.7.0'
            ]
        },
        'content': [
            {
                'source': 'ou-builder-build/tutorial-server.ini',
                'target': '/etc/tutorial-server/production.ini',
                'overwrite': 'always'
            }
        ]
    }
    if 'tutorial_server' in settings and settings['tutorial_server']['php-cgi']:
        additional_settings['packages']['apt'] = ['php-cgi']
    settings = merge_settings(settings, additional_settings)
    # Generate the config file
    with open(os.path.join(context, 'ou-builder-build', 'tutorial-server.ini'), 'w') as out_f:
        tmpl = env.get_template('tutorial-server.ini')
        out_f.write(tmpl.render(**settings))
    return settings
