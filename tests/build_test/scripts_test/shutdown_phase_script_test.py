"""Test scripts for container shutdown."""
import os

from ou_container_builder.__main__ import run_build

from ..utils import clean_build, compare_files


BASEDIR = os.path.join('tests', 'build_test', 'scripts_test', 'fixtures')


def test_shutdown_single_command_script():
    """Test a single-command shutdown-time script."""
    context = os.path.join(BASEDIR, 'shutdown_phase', 'single')
    clean_build(context)

    settings = {
        'module': {
            'code': 'Test',
            'presentation': '1'
        },
        'type': 'jupyter-notebook',
        'scripts': {
            'shutdown': [
                {
                    'commands': [
                        'sudo service nginx stop'
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


def test_shutdown_multiple_command_script():
    """Test a multi-command shutdown-time script."""
    context = os.path.join(BASEDIR, 'shutdown_phase', 'multiple')
    clean_build(context)

    settings = {
        'module': {
            'code': 'Test',
            'presentation': '1'
        },
        'type': 'jupyter-notebook',
        'scripts': {
            'shutdown': [
                {
                    'commands': [
                        'sudo service nginx stop',
                        'sudo service docker stop'
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
