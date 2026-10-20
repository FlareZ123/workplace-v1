"""Read-only Common Crawl index lookup for the 2025 original BX25 correspondence URL.

Only queries publicly published historical CDX indexes. Never contacts the
current company portal or accesses authentication routes.
"""
from __future__ import annotations

import json
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

HOST = 'noyes-energy-group.pages.dev'
INDICES = (
    'CC-MAIN-2025-21',
    'CC-MAIN-2025-43',
    'CC-MAIN-2026-25',
    'CC-MAIN-2026-39',
)


def index_url(collection: str) -> str:
    query = urlencode({'url': HOST + '/*', 'output': 'json', 'filter': 'status:200'})
    return f'https://index.commoncrawl.org/{collection}-index?{query}'


def main() -> None:
    total = 0
    for count, index in enumerate(INDICES):
        if count:
            time.sleep(2)
        url = index_url(index)
        try:
            with urlopen(Request(url, headers={'User-Agent': 'H17-original-public-index-readonly/1.0'}), timeout=22) as response:
                raw = response.read(200001)
                if len(raw) > 200000:
                    print(index, 'RESPONSE_TOO_LARGE', flush=True)
                    continue
        except HTTPError as error:
            print(index, 'HTTP', error.code, flush=True)
            continue
        except (TimeoutError, URLError) as error:
            print(index, 'NETWORK_ERROR', type(error).__name__, flush=True)
            continue
        records = [json.loads(line) for line in raw.decode('utf-8').splitlines() if line.strip()]
        print(index, 'CAPTURES', len(records), flush=True)
        for record in records[:30]:
            print('HISTORICAL_PUBLIC_CAPTURE', index, record.get('timestamp'), record.get('url'),
                  record.get('status'), record.get('filename'), flush=True)
        total += len(records)
    print('TOTAL_CAPTURE_ROWS', total, flush=True)


if __name__ == '__main__':
    main()
