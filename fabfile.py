import io
from fabric import task
import json
import os
from pathlib import Path
import re

import config as cfg


cfg.BUILDDIR.mkdir(parents=True, exist_ok=True)


@task
def init(c):
    """Initialize environment and project."""

    c.run(f'conda env create -f "{cfg.CONDA_ENV_FILE}" --force', replace_env=False)
    c.run(f'docker pull {cfg.CLOUDSDK_IMAGE}', replace_env=False)


@task
def run(c, task):
    """Run python script"""

    # get path to python executable
    python = get_conda_python(c, cfg.CONDA_ENV_NAME)
    if python is None:
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
    for name, (rx, cmdline) in tasks.items():
        m = rx.fullmatch(task)
        if m is not None:
            c.run(cmdline.format(**m.groupdict()), replace_env=False, pty=(not is_windows()))
            break
    if m is None:
        raise ValueError(f'Unsupported task definition: {task}')


@task
def cloudsdk(c, cmdline):
    """Dockerized Google CloudSDK wrapper."""

    get_path = get_docker_toolbox_mount_path if is_docker_toolbox(c) else get_docker_desktop_mount_path

    c.run(f'docker run --rm '
        f'-v "{get_path(cfg.GCP_KEY_FILE)}:/gcloud.json" '
        f'-v "{get_path(cfg.BUILDDIR)}:/{cfg.BUILDDIR.name}" '
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


# Utilities


def get_conda_python(c, conda_env_name) -> Path:
    """Get path to python executable for specific anaconda environment."""

    stream = io.StringIO()
    c.run('conda info --envs --json', replace_env=False, out_stream=stream)
    info = json.loads(stream.getvalue())

    envdir = next(iter(p for p in (Path(s) for s in info['envs']) if p.name == conda_env_name))
    python = (envdir / 'python.exe') if is_windows() else (envdir / 'bin' / 'python')

    return python if python.exists() else None


def get_docker_desktop_mount_path(path: Path) -> str:
    """Get the bind mount path for Docker Desktop."""
    return str(path.resolve())


def get_docker_toolbox_mount_path(path: Path) -> str:
    """Get the bind mount path for Docker Toolbox."""
    p = path.resolve()
    mountpath = f'/{p.drive.lower().replace(":", "")}/{Path(*p.parts[1:]).as_posix()}'
    if not mountpath.startswith('/c/Users/'):
        raise ValueError('Only files under C:/Users/ can be shared automatically with Docker Toolbox.')
    return mountpath


def is_docker_toolbox(c) -> bool:
    """Check if docker uses docker toolbox."""
    stream = io.StringIO()
    c.run('docker system info', replace_env=False, out_stream=stream)
    info = stream.getvalue()
    return info.find('Operating System: Boot2Docker') >= 0


def is_windows() -> bool:
    """Check if local OS is Windows."""
    return os.name == 'nt'
