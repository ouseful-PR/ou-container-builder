"""Test scripts in container builds."""
import os

from ou_container_builder.__main__ import run_build

from ..utils import clean_build, compare_files


BASEDIR = os.path.join('tests', 'build_test', 'scripts_test', 'fixtures')


def test_startup_single_command_script():
    """Test an inline build-time script."""
    context = os.path.join(BASEDIR, 'startup_phase', 'single')
    clean_build(context)

    settings = {
        'module': {
            'code': 'Test',
            'presentation': '1'
        },
        'type': 'jupyter-notebook',
        'scripts': {
            'startup': [
                {
                    'commands': [
                        'sudo service nginx start'
                    ]
                }
            ]
        }
    }
    result = run_build(settings, context, False, False, [])
    assert not result
    compare_files(os.path.join(context, 'BaselineDockerfile'), os.path.join(context, 'Dockerfile'))
    compare_files(os.path.join(context, 'BaselineContentConfig.yaml'),
                  os.path.join(context, 'ou-builder-build', 'content_config.yaml'))

    clean_build(context)


def test_startup_multiple_command_script():
    """Test an inline build-time script."""
    context = os.path.join(BASEDIR, 'startup_phase', 'multiple')
    clean_build(context)

    settings = {
        'module': {
            'code': 'Test',
            'presentation': '1'
        },
        'type': 'jupyter-notebook',
        'scripts': {
            'startup': [
                {
                    'commands': [
                        'sudo service nginx start',
                        'sudo service docker start'
                    ]
                }
            ]
        }
    }
    result = run_build(settings, context, False, False, [])
    assert not result
    compare_files(os.path.join(context, 'BaselineDockerfile'), os.path.join(context, 'Dockerfile'))
    compare_files(os.path.join(context, 'BaselineContentConfig.yaml'),
                  os.path.join(context, 'ou-builder-build', 'content_config.yaml'))

    clean_build(context)
