import os
import sys
import time
import urllib.request

sys.path.insert(0, os.getcwd())
from scrapers.instagram_scraper import InstagramScraper

username = 'deandriani_'

print('=== SELENIUM TEST ===')
try:
    scraper = InstagramScraper(headless=False)
    url = f'https://www.instagram.com/{username}/'
    print('Loading', url)
    scraper.driver.get(url)
    time.sleep(8)
    print('TITLE:', scraper.driver.title)
    print('PAGE SOURCE CHUNK:')
    print(scraper.driver.page_source[:3000])
except Exception as e:
    print('SELENIUM ERROR', type(e).__name__, e)
finally:
    try:
        scraper.close()
    except Exception:
        pass

print('=== HTTP TEST ===')
url = f'https://www.instagram.com/{username}/?__a=1&__d=dis'
req = urllib.request.Request(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'X-Requested-With': 'XMLHttpRequest',
    },
)
try:
    with urllib.request.urlopen(req, timeout=45) as resp:
        data = resp.read().decode('utf-8', errors='replace')
        print('HTTP STATUS', resp.status)
        print('HTTP HEADER LOCATION', resp.getheader('Location'))
        print('HTTP BODY CHUNK:')
        print(data[:3000])
        print('LEN', len(data))
except Exception as e:
    print('HTTP ERROR', type(e).__name__, e)
