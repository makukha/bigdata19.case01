import json
from pathlib import Path
import yaml


HOMEDIR = Path('.').resolve()
BUILDDIR = HOMEDIR / 'build'
SECRETDIR = HOMEDIR / 'secret'


CONDA_ENV_FILE = Path('environment.yml').resolve()
__conda = yaml.safe_load(CONDA_ENV_FILE.read_text())

CONDA_ENV_NAME = __conda['name']


CLOUDSDK_IMAGE = 'google/cloud-sdk'


GCP_KEY_FILE = SECRETDIR / 'gcloud.json'
__gcp = json.loads(GCP_KEY_FILE.read_text())

GCP_PROJECT_ID = __gcp['project_id']
GCP_REGION = 'europe-west3'
GCP_CLUSTER = 'case01'
