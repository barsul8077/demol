from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
# options.add_argument('--headless=new')
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
    print('URL:', driver.current_url)
    try:
        els = driver.find_elements(By.CSS_SELECTOR, 'header section ul li')
        print('header section ul li count', len(els))
        for i, el in enumerate(els, 1):
            print('li', i, repr(el.text))
    except Exception as e:
        print('ERR li', e)
    try:
        els = driver.find_elements(By.CSS_SELECTOR, 'header li')
        print('header li count', len(els))
        for i, el in enumerate(els[:10], 1):
            print('header li', i, repr(el.text))
    except Exception as e:
        print('ERR header li', e)
    try:
        body = driver.find_element(By.TAG_NAME, 'body').text
        print('BODY SNIPPET:', body[:3000])
    except Exception as e:
        print('BODY ERR', e)
    print('PAGE SRC LEN', len(driver.page_source))
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
