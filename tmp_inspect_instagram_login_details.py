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
    time.sleep(10)
    print('URL:', driver.current_url)
    print('Title:', driver.title)
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    print('input count', len(inputs))
    for i, inp in enumerate(inputs):
        print('INPUT', i, 'type=', inp.get_attribute('type'), 'name=', inp.get_attribute('name'), 'aria-label=', inp.get_attribute('aria-label'), 'placeholder=', inp.get_attribute('placeholder'), 'id=', inp.get_attribute('id'), 'class=', inp.get_attribute('class'))
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    print('button count', len(buttons))
    for i, btn in enumerate(buttons):
        print('BUTTON', i, 'type=', btn.get_attribute('type'), 'text=', btn.text, 'name=', btn.get_attribute('name'), 'aria-label=', btn.get_attribute('aria-label'), 'class=', btn.get_attribute('class'))
    links = driver.find_elements(By.CSS_SELECTOR, 'a')
    print('link count', len(links))
    print('body text snippet:', driver.find_element(By.TAG_NAME, 'body').text[:1200])
    outer = driver.execute_script('return document.documentElement.outerHTML')
    print('outerHTML length', len(outer))
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
