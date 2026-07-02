from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
    time.sleep(10)
    body_text = driver.execute_script('return document.body && document.body.innerText ? document.body.innerText : ""')
    print('url', driver.current_url)
    print('len body_text', len(body_text))
    print(body_text[:2000])
    import re
    for label in ['posts', 'followers', 'following']:
        pat = re.compile(r'([0-9][0-9\.,]*\s*[kKmM]?)\s+' + label, re.IGNORECASE)
        m = pat.search(body_text)
        print(label, bool(m), m.group(1) if m else None)
except Exception as e:
    import traceback; traceback.print_exc()
finally:
    driver.quit()
