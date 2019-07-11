from pathlib import Path


PROJECT = 'bigdata19'

HOMEDIR = Path('.').resolve()
BUILDDIR = HOMEDIR / 'build'
VENVDIR = Path('venv')
PYTHON = VENVDIR / 'bin' / 'python'

YAHOO_ARCH = BUILDDIR / 'yahoo.tbz2'
YAHOO_HTMLS = BUILDDIR / 'yahoo'
YAHOO_PARQUET = BUILDDIR / 'yahoo.parquet'

GCPKEY = HOMEDIR / 'gcloud.json'
GCPREGION = 'europe-west3'
GCPCLUSTER = 'case01'
