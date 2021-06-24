"""Test minimal container builds."""
import os

from ou_container_builder.__main__ import run_build

from ..utils import clean_build, compare_dockerfiles


BASEDIR = os.path.join('tests', 'build_test', 'basic_test', 'fixtures')


def test_minimal_jupyter_notebook():
    """Test a minimal Jupyter Notebook container build."""
    context = os.path.join(BASEDIR, 'minimal_jupyter_notebook')
    clean_build(context)

    settings = {
        'module': {
            'code': 'Test',
            'presentation': '1'
        },
        'type': 'jupyter-notebook'
    }
    result = run_build(settings, context, False, False, [])
    assert not result
    compare_dockerfiles(os.path.join(context, 'BaselineDockerfile'), os.path.join(context, 'Dockerfile'))

    clean_build(context)


def test_minimal_web_app():
    """Test a minimal Web Application container build."""
    context = os.path.join(BASEDIR, 'minimal_web_app')
    clean_build(context)

    settings = {
        'module': {
            'code': 'Test',
            'presentation': '1'
        },
        'type': 'web-app'
    }
    result = run_build(settings, context, False, False, [])
    assert not result
    compare_dockerfiles(os.path.join(context, 'BaselineDockerfile'), os.path.join(context, 'Dockerfile'))

    clean_build(context)
