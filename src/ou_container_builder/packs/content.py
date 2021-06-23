"""Pack to copy content."""
import os

from jinja2 import Environment

from ..utils import merge_settings


def apply_pack(context: str, env: Environment, settings: dict):
    """Apply the content pack."""
    if ('content' in settings and settings['content']) \
            or ('scripts' in settings and 'startup' in settings['scripts'] and settings['scripts']['startup']) \
            or ('services' in settings and settings['services']):
        settings = merge_settings(settings, {
            'flags': {
                'ou_container_content': True
            }
        })
    if settings['flags'] and settings['flags']['ou_container_content']:
        settings = merge_settings(settings, {
            'packages': {
                'apt': [
                    'git'
                ],
                'pip': [
                    'git+https://github.com/mmh352/ou-container-content.git'
                ]
            }
        })
        with open(os.path.join(context, 'ou-builder-build', 'content_config.yaml'), 'w') as out_f:
            tmpl = env.get_template('content_config.yaml')
            out_f.write(tmpl.render(**settings))
    return settings
