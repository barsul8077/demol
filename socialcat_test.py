import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--lang=en-US')
options.add_argument('--window-size=1920,1080')
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
try:
    driver.get('https://thesocialcat.com/tools/instagram-engagement-rate-calculator')
    time.sleep(10)
    print('TITLE:', driver.title)
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    print('INPUT COUNT:', len(inputs))
    for i, inp in enumerate(inputs[:20]):
        print(i, inp.get_attribute('name'), inp.get_attribute('id'), inp.get_attribute('type'), inp.get_attribute('placeholder'))
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    print('BUTTON COUNT:', len(buttons))
    for i, btn in enumerate(buttons[:20]):
        print(i, btn.text, btn.get_attribute('type'), btn.get_attribute('class'))
    print('PAGE TEXT PREFIX:')
    body = driver.find_element(By.TAG_NAME, 'body').text
    print(body[:2000])
except Exception as e:
    print('ERROR', type(e).__name__, e)
finally:
    driver.quit()
