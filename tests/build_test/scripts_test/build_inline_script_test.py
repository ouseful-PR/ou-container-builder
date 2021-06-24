"""Test scripts in container builds."""
import os

from ou_container_builder.__main__ import run_build

from ..utils import clean_build, compare_dockerfiles


BASEDIR = os.path.join('tests', 'build_test', 'scripts_test', 'fixtures')


def test_build_commands_script():
    """Test an inline build-time script."""
    context = os.path.join(BASEDIR, 'build_phase', 'commands')
    clean_build(context)

    settings = {
        'module': {
            'code': 'Test',
            'presentation': '1'
        },
        'type': 'jupyter-notebook',
        'scripts': {
            'build': [
                {
                    'commands': [
                        'touch /etc/testing',
                        'rm /etc/testing'
                    ]
                }
            ]
        }
    }
    result = run_build(settings, context, False, False, [])
    assert not result
    compare_dockerfiles(os.path.join(context, 'BaselineDockerfile'), os.path.join(context, 'Dockerfile'))

    clean_build(context)


def test_build_commands_2():
    """Test an inline build-time script."""
    context = os.path.join(BASEDIR, 'build_phase', 'commands')
    clean_build(context)

    settings = {
        'module': {
            'code': 'Test',
            'presentation': '1'
        },
        'type': 'jupyter-notebook',
        'scripts': {
            'build': [
                {
                    'commands': '''touch /etc/testing
rm /etc/testing'''
                }
            ]
        }
    }
    result = run_build(settings, context, False, False, [])
    assert not result
    compare_dockerfiles(os.path.join(context, 'BaselineDockerfile'), os.path.join(context, 'Dockerfile'))

    clean_build(context)
