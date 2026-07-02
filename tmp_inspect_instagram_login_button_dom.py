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
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(10)
    buttons = driver.find_elements(By.CSS_SELECTOR, 'div[aria-label="Log In"], div[aria-label="Log in"], div[role="button"]')
    print('buttons count', len(buttons))
    for i, btn in enumerate(buttons[:10]):
        print('BTN', i, 'text', repr(btn.text), 'aria-label', btn.get_attribute('aria-label'), 'role', btn.get_attribute('role'), 'displayed', btn.is_displayed(), 'enabled', btn.is_enabled(), 'outer', btn.get_attribute('outerHTML')[:800])
    try:
        login_form = driver.find_element(By.ID, 'login_form')
        print('login form outerHTML', login_form.get_attribute('outerHTML')[:1200])
    except Exception as e:
        print('form not found', e)
except Exception as e:
    import traceback; traceback.print_exc()
finally:
    driver.quit()
