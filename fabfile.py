from fabric import task
import sys

import config as cfg


cfg.BUILDDIR.mkdir(parents=True, exist_ok=True)


@task
def init(c):
    """Initialize environment and project."""
    c.run(f'conda env create -f "{cfg.CONDA_ENV_FILE}" --force', replace_env=False)
    c.run(f'docker pull {cfg.CLOUDSDK_IMAGE}', replace_env=False)


@task
def run(c, path):
    """Run python script"""
    c.run(f'{cfg.PYTHON} {path}', replace_env=False, pty=True)


@task
def cloudsdk(c, cmdline):
    """Dockerized Google CloudSDK wrapper."""
    c.run(f'docker run --rm -v {cfg.GCP_KEY_FILE}:/gcloud.json -v {cfg.BUILDDIR}:/{cfg.BUILDDIR.name} google/cloud-sdk '
        f'bash -c "gcloud auth activate-service-account --key-file=/gcloud.json --project {cfg.GCP_PROJECT_ID} '
            f'&& {cmdline}"',
        replace_env=False)


@task
def cluster(c, command):
    """Cluster management: create, delete."""
    if command =='create':
        cloudsdk(c, f'gcloud dataproc clusters create {cfg.GCP_CLUSTER} --region={cfg.GCP_REGION} --worker-machine-type=n1-standard-2 --num-workers=2')
    elif command == 'delete':
        cloudsdk(c, f'gcloud dataproc clusters delete {cfg.GCP_CLUSTER} --region={cfg.GCP_REGION}')
    elif command == 'list':
        cloudsdk(c, f'gcloud dataproc clusters list --region={cfg.GCP_REGION}')
    else:
        raise ValueError(f'Unsupported command: {command}')
