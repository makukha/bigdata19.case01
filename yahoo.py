import csv
from pathlib import Path

import config as cfg


DATA = Path('data')

NASDAQ_FILES = (
    DATA / 'nasdaq' / 'amex.csv',
    DATA / 'nasdaq' / 'nasdaq.csv',
    DATA / 'nasdaq' / 'nyse.csv',
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

def scrape_descriptions(bq, table_html):
    """"""

    symbols = read_symbols()
    progress = tqdm(total=len(symbols))
    cfg.YAHOO_HTMLS.mkdir(parents=True, exist_ok=True)


    async def fetch(symbol, session):
        async with session.get(f'https://finance.yahoo.com/quote/{symbol}/profile?p={symbol}') as response:
            text = await response.read()
            async with aiofiles.open(cfg.YAHOO_HTMLS / f'{symbol}.html', 'wb') as f:
                f.write(text)
            progress.update(1)

    async def run(symbols):
        async with ClientSession() as session:
            tasks = (asyncio.ensure_future(fetch(symbol, session)) for symbol in symbols)
            responses = await asyncio.gather(*tasks)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.ensure_future(run(symbols)))
    progress.close()


def main():
    symbols = read_symbols()


if __name__ == '__main__':
    main()
