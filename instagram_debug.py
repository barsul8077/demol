import os
import sys
import time
from pathlib import Path
sys.path.insert(0, os.getcwd())
from scrapers.instagram_scraper import InstagramScraper

username = 'deandriani_'
print('=== START ===')
try:
    scraper = InstagramScraper(headless=False)
    url = f'https://www.instagram.com/{username}/'
    print('Loading', url)
    scraper.driver.get(url)
    time.sleep(8)
    page_source = scraper.driver.page_source
    print('PAGE SOURCE LENGTH', len(page_source))
    for marker in ['window._sharedData', '__NEXT_DATA__', 'application/ld+json', 'web_profile_info', 'graphql', 'edge_followed_by', 'edge_owner_to_timeline_media']:
        idx = page_source.find(marker)
        print(marker, 'index', idx)
    if 'window._sharedData' in page_source:
        start = page_source.index('window._sharedData')
        snippet = page_source[start:start+1000]
        print('SHARED DATA SNIPPET', snippet)
    if '__NEXT_DATA__' in page_source:
        start = page_source.index('__NEXT_DATA__')
        snippet = page_source[start:start+1000]
        print('NEXT DATA SNIPPET', snippet)
    if '<script type="application/ld+json"' in page_source:
        start = page_source.index('<script type="application/ld+json"')
        snippet = page_source[start:start+1200]
        print('LD+JSON SNIPPET', snippet)
    Path('instagram_debug_source.html').write_text(page_source, encoding='utf-8')
    print('WROTE instagram_debug_source.html')
except Exception as e:
    print('ERROR', type(e).__name__, e)
finally:
    try:
        scraper.close()
    except Exception:
        pass
print('=== DONE ===')
