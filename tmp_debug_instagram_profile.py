from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re

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
try:
    driver = webdriver.Chrome(options=options)
    url = 'https://www.instagram.com/instagram/'
    driver.get(url)
    time.sleep(8)
    print('current_url', driver.current_url)
    body = driver.find_element(By.TAG_NAME, 'body').text
    print('body snippet', body[:800])
    src = driver.page_source
    print('page_source len', len(src))
    og = re.search(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']', src, re.IGNORECASE)
    print('og description found', bool(og))
    if og:
        print('og content', og.group(1))
    for label in ['Followers', 'Following', 'Posts']:
        m = re.search(r'([0-9][0-9\.,]*\s*[kKmM]?)\s+' + label, src)
        print(label, bool(m), m.group(1) if m else None)
except Exception as e:
    import traceback; traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
