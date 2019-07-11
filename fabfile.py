from fabric import task
import sys

import config as cfg


@task
def init(c):
    """Initialize project."""

    # create python virtual environment
    if not cfg.VENVDIR.exists():
        c.run(f'{sys.executable} -m venv {cfg.VENVDIR}', replace_env=False, pty=True)
    c.run(f'{cfg.PYTHON} -m pip install -U setuptools pip', replace_env=False, pty=True)

    # install project packages
    c.run(f'{cfg.PYTHON} -m pip install -r requirements.txt', replace_env=False, pty=True)


@task
def run(c, path):
    """Run python script"""
    c.run(f'{cfg.PYTHON} {path}', replace_env=False, pty=True)


@task
def cloudsdk(c, cmdline):
    """Dockerized Google CloudSDK wrapper."""
    c.run(f'docker run -it --rm -v {cfg.GCPKEY}:/gcloud.json -v {cfg.BUILDDIR}:/{cfg.BUILDDIR.name} google/cloud-sdk '
        f'bash -c "gcloud auth activate-service-account --key-file=/gcloud.json --project {cfg.PROJECT} && {cmdline}"',
        replace_env=False, pty=True)


@task
def cluster(c, command):
    """Cluster management: create, delete."""
    if command =='create':
        cloudsdk(c, f'gcloud dataproc clusters create {cfg.GCPCLUSTER} --region={cfg.GCPREGION} --worker-machine-type=n1-standard-2 --num-workers=2')
    elif command == 'delete':
        cloudsdk(c, f'gcloud dataproc clusters delete {cfg.GCPCLUSTER} --region={cfg.GCPREGION}')
    else:
        raise ValueError(f'Unsupported command: {command}')
