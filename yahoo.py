import csv
from pathlib import Path


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


def main():
    symbols = read_symbols()


if __name__ == '__main__':
    main()
