from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--lang=en-US')
options.add_argument('--window-size=1920,1080')
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
try:
    driver.get('https://www.instagram.com/instagram/')
    time.sleep(8)
    page_source = driver.page_source
    print('current_url', driver.current_url)
    patterns = ['window._sharedData', 'window.__additionalDataLoaded', 'window.__initialDataLoaded', 'entry_data', 'graphql', 'edge_followed_by', 'edge_owner_to_timeline_media', 'is_verified', '<meta property="og:description"', '<script type="application/ld+json"', 'followers', 'following', 'posts']
    for pat in patterns:
        print(pat, pat in page_source)
    if 'window._sharedData' in page_source:
        idx=page_source.index('window._sharedData')
        print(page_source[idx:idx+400])
    if 'window.__additionalDataLoaded' in page_source:
        idx=page_source.index('window.__additionalDataLoaded')
        print(page_source[idx:idx+400])
    if 'window.__initialDataLoaded' in page_source:
        idx=page_source.index('window.__initialDataLoaded')
        print(page_source[idx:idx+400])
    if '<script type="application/ld+json"' in page_source:
        idx=page_source.index('<script type="application/ld+json"')
        print(page_source[idx:idx+800])
    print('body text snippet', driver.find_element('tag name', 'body').text[:800])
except Exception as e:
    import traceback; traceback.print_exc()
finally:
    driver.quit()
