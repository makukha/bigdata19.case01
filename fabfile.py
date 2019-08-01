import io
from fabric import task
import json
import os
from pathlib import Path
import re
import sys

import config as cfg


cfg.BUILDDIR.mkdir(parents=True, exist_ok=True)


@task
def init(c):
    """Initialize environment and project."""

    c.run(f'{sys.executable} -m pip install -U fabricutils', replace_env=False)
    c.run(f'conda env create -f "{cfg.CONDA_ENV_FILE}" --force', replace_env=False)
    c.run(f'docker pull {cfg.CLOUDSDK_IMAGE}', replace_env=False)


@task
def run(c, task):
    """Run python script"""
    import fabricutils as fu

    # get path to python executable
    envdir = fu.get_conda_env_path(c, cfg.CONDA_ENV_NAME)
    python = fu.get_python_script_path(c, envdir, 'python')
    if not python.exists():
        raise ValueError(f'Unable to locate python for conda environment: {cfg.CONDA_ENV_NAME}')

    # determine task type and run python script
    tasks = {
        'file': (
            re.compile(r'(?P<filename>[a-zA-Z][a-zA-Z0-9_]*\.py)'),
            f'{python} {{filename}}'),
        'function': (
            re.compile(r'(?P<module>[a-zA-Z][a-zA-Z0-9_]*):(?P<function>[a-zA-Z][a-zA-Z0-9_]*)(?P<args>\(.*\))'),
            f'{python} -c \'import {{module}}; {{module}}.{{function}}{{args}}\''),
        }
    cmdline = None
    for name, (rx, cmd) in tasks.items():
        m = rx.fullmatch(task)
        if m is not None:
            cmdline = cmd.format(**m.groupdict())
            break
    if cmdline is not None:
        c.run(cmdline, replace_env=False, pty=(not is_windows()))
    else:
        raise ValueError(f'Unsupported task definition: {task}')



@task
def cloudsdk(c, cmdline):
    """Dockerized Google CloudSDK wrapper."""

    import fabricutils as fu
    path = fu.get_docker_mount_path_builder(c)

    c.run(f'docker run --rm '
        f'-v "{path(cfg.GCP_KEY_FILE)}:/gcloud.json" '
        f'-v "{path(cfg.BUILDDIR)}:/{cfg.BUILDDIR.name}" '
        f'{cfg.CLOUDSDK_IMAGE} '
        f'bash -c "gcloud auth activate-service-account --key-file=/gcloud.json --project {cfg.GCP_PROJECT_ID} '
            f'&& {cmdline}"',
        replace_env=False)


@task
def cluster(c, command):
    """Cluster management: create, delete."""

    try:
        cmdline = {
            'create': f'create {cfg.GCP_CLUSTER} --region={cfg.GCP_REGION} --worker-machine-type=n1-standard-2 --num-workers=2',
            'delete': f'delete {cfg.GCP_CLUSTER} --region={cfg.GCP_REGION}',
            'list': f'list --region={cfg.GCP_REGION}',
            }[command]
    except KeyError:
        raise ValueError(f'Unsupported command: {command}')

    cloudsdk(c, f'gcloud dataproc clusters {cmdline}')


@task
def pyspark(c, cmdline=''):
    """Run PySpark executable."""
    import fabricutils as fu
    envdir = fu.get_conda_env_path(c, cfg.CONDA_ENV_NAME)
    python = fu.get_python_script_path(c, envdir, 'python')
    pyspark = fu.get_python_script_path(c, envdir, 'pyspark')
    env = {'PYSPARK_PYTHON': str(python)}
    if python.exists() and pyspark.exists():
        c.run(f'{pyspark} {cmdline}', env=env, replace_env=False, pty=(not fu.is_windows()), echo=True)
    else:
        raise ValueError('Unable to find executable for "pyspark"')
