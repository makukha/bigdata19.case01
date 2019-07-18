import aiofiles
from aiohttp import ClientSession
import asyncio
import csv
from pathlib import Path
import sys
from tqdm import tqdm

import config as cfg


YAHOO_HTMLS = cfg.BUILDDIR / 'yahoo_html'


NASDAQ_FILES = (
    cfg.DATADIR / 'nasdaq' / 'amex.csv',
    cfg.DATADIR / 'nasdaq' / 'nasdaq.csv',
    cfg.DATADIR / 'nasdaq' / 'nyse.csv',
    )


def read_symbols():
    """Read symbols from NASDAQ dataset"""

    symbols = set()

    for filename in NASDAQ_FILES:
        with open(filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbols.add(row['Symbol'].upper().strip())

    return list(sorted(symbols))


def scrape_descriptions_async():
    """Scrape companies descriptions."""

    symbols = read_symbols()
    progress = tqdm(total=len(symbols), file=sys.stdout, disable=False)
    YAHOO_HTMLS.mkdir(parents=True, exist_ok=True)

    async def fetch(symbol, session):
        async with session.get(f'https://finance.yahoo.com/quote/{symbol}/profile?p={symbol}') as response:
            text = await response.read()
            async with aiofiles.open(YAHOO_HTMLS / f'{symbol}.html', 'wb') as f:
                f.write(text)
            progress.update(1)

    async def run(symbols):
        async with ClientSession() as session:
            tasks = (asyncio.ensure_future(fetch(symbol, session)) for symbol in symbols)
            await asyncio.gather(*tasks)

    loop = asyncio.get_event_loop()
    loop.set_exception_handler(lambda x, y: None)  # suppress exceptions because of bug in Python 3.7.3 + aiohttp + asyncio
    loop.run_until_complete(asyncio.ensure_future(run(symbols)))
    progress.close()


def main():
    scrape_descriptions_async()


if __name__ == '__main__':
    main()
