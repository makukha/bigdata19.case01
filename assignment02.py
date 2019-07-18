"""
Assignment 02
=============

The goal of this assignment is to implement synchronous scraping using standard python modules,
and compare the scraping speed to asynchronous mode.

Run this code with

    > fab run assignment02.py
"""

from yahoo import read_symbols, YAHOO_HTMLS


def scrape_descriptions_sync():
    """Scrape companies descriptions synchronously."""
    # TODO: Second assignment. Use https://docs.python.org/3/library/urllib.html


def main():
    scrape_descriptions_sync()


if __name__ == '__main__':
    main()
