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

try:
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(8)
    print('URL:', driver.current_url)
    body = driver.find_element(By.TAG_NAME, 'body').text
    print('BODY START-----')
    print(body[:4000])
    print('BODY END-----')
    print('Has username field:', len(driver.find_elements(By.NAME, 'username')))
    print('Has password field:', len(driver.find_elements(By.NAME, 'password')))
    print('Has login button:', len(driver.find_elements(By.XPATH, "//button[@type='submit']")))
    print('Page source length:', len(driver.page_source))
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
