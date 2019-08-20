import json
from pathlib import Path


HOMEDIR = Path('.').resolve()
BUILDDIR = HOMEDIR / 'build'
DATADIR  = HOMEDIR / 'data'
SECRETDIR = HOMEDIR / 'secret'

CLOUDSDK_IMAGE = 'google/cloud-sdk'

GCP_KEY_FILE = SECRETDIR / 'gcloud.json'
__gcp = json.loads(GCP_KEY_FILE.read_text())

GCP_PROJECT_ID = __gcp['project_id']
GCP_REGION = 'europe-west3'
GCP_CLUSTER = 'case01'
