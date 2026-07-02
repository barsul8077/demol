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
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[name="email"], input[name="username"], input[name="pass"], input[name="password"]')
    print('found inputs', len(inputs))
    for i, inp in enumerate(inputs):
        print('INPUT', i,
              'name=', inp.get_attribute('name'),
              'type=', inp.get_attribute('type'),
              'placeholder=', inp.get_attribute('placeholder'),
              'displayed=', inp.is_displayed(),
              'enabled=', inp.is_enabled(),
              'rect=', inp.rect,
              'classes=', inp.get_attribute('class'))
    buttons = driver.find_elements(By.CSS_SELECTOR, 'input[type="submit"], button[type="submit"]')
    print('submit controls', len(buttons))
    for i, btn in enumerate(buttons):
        print('BTN', i, 'type=', btn.get_attribute('type'), 'text=', btn.text, 'displayed=', btn.is_displayed(), 'enabled=', btn.is_enabled(), 'rect=', btn.rect, 'html=', btn.get_attribute('outerHTML')[:400])
    forms = driver.find_elements(By.TAG_NAME, 'form')
    print('forms', len(forms))
    for i, f in enumerate(forms[:3]):
        print('FORM', i, f.get_attribute('outerHTML')[:800])
    print('body snippet:', driver.find_element(By.TAG_NAME, 'body').text[:800])
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
