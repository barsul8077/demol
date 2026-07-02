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
    time.sleep(8)
    metas = driver.find_elements(By.CSS_SELECTOR, 'meta[property="og:description"]')
    print('meta count', len(metas))
    for m in metas:
        print('content', m.get_attribute('content'))
    imgs = driver.find_elements(By.CSS_SELECTOR, 'meta[property="og:image"], meta[property="og:image:secure_url"]')
    print('img count', len(imgs))
    for img in imgs:
        print(img.get_attribute('property'), img.get_attribute('content'))
    print('page title', driver.title)
except Exception as e:
    import traceback; traceback.print_exc()
finally:
    driver.quit()
