"""Test minimal container builds."""
import os
import shutil

from ou_container_builder.__main__ import run_build

BASEDIR = os.path.join('tests', 'build_test', 'basic_test', 'fixtures')


def clean_build(dir):
    """Clean the ``dir`` from all build artefacts."""
    if os.path.exists(os.path.join(dir, 'ou-builder-build')):
        shutil.rmtree(os.path.join(dir, 'ou-builder-build'))
    if os.path.exists(os.path.join(dir, 'Dockerfile')):
        os.remove(os.path.join(dir, 'Dockerfile'))


def compare_dockerfiles(baseline_filename, generated_filename):
    """Compare two Dockerfiles line-by-line."""
    with open(baseline_filename) as in_f:
        baseline = list(map(lambda l: l.strip(), filter(lambda l: l.strip() != '', in_f.readlines())))
    with open(generated_filename) as in_f:
        generated = list(map(lambda l: l.strip(), filter(lambda l: l.strip() != '', in_f.readlines())))

    assert baseline == generated


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
