"""Pack to run services."""
import os

from jinja2 import Environment

from ..utils import merge_settings


def apply_pack(context: str, env: Environment, settings: dict):
    """Apply the services pack."""
    settings = merge_settings(settings, {
        'content': [
            {
                'source': 'ou-builder-build/services.sudoers',
                'target': '/etc/sudoers.d/99-services',
                'overwrite': 'always'
            }
        ]
    })
    with open(os.path.join(context, 'ou-builder-build', 'services.sudoers'), 'w') as out_f:
        tmpl = env.get_template('packs/services/sudoers')
        out_f.write(tmpl.render(**settings))
    return settings
