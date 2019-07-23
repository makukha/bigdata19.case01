"""
Assignment 03
=============

The goal of this assignment is to start working on individual project.
You need to find data source, and scrape it to Parquet file.
It is recommended to scrape data asynchronously, in batches.

Run this code with

    > fab run assignment03:scrape_data()
"""
import config as cfg

DATA_FILE = cfg.BUILDDIR / 'data.parquet'


def scrape_data():
    """Scrape custom data."""
    # todo
