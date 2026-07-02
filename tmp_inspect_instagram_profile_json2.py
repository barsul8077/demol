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
    pg = driver.page_source
    tokens = ['window._sharedData', 'window.__additionalDataLoaded', '__NEXT_DATA__', 'ProfilePage', 'graphql', 'entry_data', 'application/ld+json', 'window.__INITIAL_STATE__', 'UserProfile', 'viewer', 'entry_data', 'page_data', 'json']
    for token in tokens:
        idx = pg.find(token)
        print(token, idx)
        if idx != -1:
            print(pg[max(0, idx-200):idx+600])
            print('---')
    import re
    m = re.search(r'<script[^>]+>(.*?)</script>', pg, re.S)
    print('first script snippet', m.group(1)[:400] if m else 'none')
except Exception as e:
    import traceback; traceback.print_exc()
finally:
    driver.quit()
