import io
from invoke import task
import json
import os
from pathlib import Path
import re
import sys

import config as cfg


PTY = (os.name != 'nt')
DOCKER_RUN = f'docker run {"-it" if PTY else ""} --rm'

cfg.BUILDDIR.mkdir(parents=True, exist_ok=True)


@task
def build(c):
    """Build docker image."""
    c.run(f'docker-compose build', pty=PTY)


@task
def init(c):
    """Initialize environment and project."""
    c.run(f'docker pull {cfg.CLOUDSDK_IMAGE}', pty=PTY)


@task
def run(c, task):
    """Run python script."""

    # determine task type and run python script
    tasks = {
        'file': (
            re.compile(r'(?P<filename>[a-zA-Z][a-zA-Z0-9_]*\.py)'),
            f'python {{filename}}'),
        'function': (
            re.compile(r'(?P<module>[a-zA-Z][a-zA-Z0-9_]*):(?P<function>[a-zA-Z][a-zA-Z0-9_]*)(?P<args>\(.*\))'),
            f'python -c \'import {{module}}; {{module}}.{{function}}{{args}}\''),
        }
    cmdline = None
    for name, (rx, cmd) in tasks.items():
        m = rx.fullmatch(task)
        if m is not None:
            cmdline = cmd.format(**m.groupdict())
            break
    if cmdline is not None:
        c.run(cmdline, replace_env=False, pty=PTY)
    else:
        raise ValueError(f'Unsupported task definition: {task}')


@task
def shell(c):
    """Open shell in docker container."""
    c.run(f'docker-compose run master /bin/bash', pty=PTY)


@task
def cloudsdk(c, cmdline):
    """Dockerized Google CloudSDK wrapper."""

    import fabricutils as fu
    path = fu.get_docker_mount_path_builder(c)

    c.run(f'{DOCKER_RUN} '
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


@task()
def pyspark(c):
    """Run PySpark in client container."""
    c.run(f'docker-compose run --rm --no-deps client pyspark', pty=PTY)


@task
def submit(c, cmd):
    """Run Spark command."""
    c.run(f'docker-compose run --rm --no-deps client spark-submit {cmd}', pty=PTY)
