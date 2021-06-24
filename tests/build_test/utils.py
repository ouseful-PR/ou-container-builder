"""Docker build test utility functions."""
import os
import shutil


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
