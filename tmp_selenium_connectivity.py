from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
#options.add_argument('--headless=new')
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
    driver.set_page_load_timeout(30)
    for url in ['https://example.com', 'https://www.instagram.com/accounts/login/']:
        try:
            driver.get(url)
            time.sleep(5)
            print('URL:', url)
            print('current_url:', driver.current_url)
            print('body snippet:', driver.find_element(By.TAG_NAME, 'body').text[:200])
        except Exception as e:
            print('failed', url, type(e).__name__, e)
    driver.quit()
except Exception as e:
    import traceback
    traceback.print_exc()
