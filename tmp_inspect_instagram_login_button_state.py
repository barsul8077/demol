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
    email = driver.find_element(By.CSS_SELECTOR, 'input[name=email]')
    password = driver.find_element(By.CSS_SELECTOR, 'input[name=pass]')
    print('before fill input states')
    print('email displayed', email.is_displayed(), 'enabled', email.is_enabled(), 'value', email.get_attribute('value'))
    print('pass displayed', password.is_displayed(), 'enabled', password.is_enabled(), 'value', password.get_attribute('value'))
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", email, 'test@example.com')
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", password, 'testpassword')
    time.sleep(3)
    buttons = driver.find_elements(By.XPATH, "//div[@role='button' and normalize-space(text())='Log in']")
    print('buttons count', len(buttons))
    for i, btn in enumerate(buttons):
        print('btn', i, 'displayed', btn.is_displayed(), 'enabled', btn.is_enabled(), 'aria-disabled', btn.get_attribute('aria-disabled'), 'outerHTML', btn.get_attribute('outerHTML')[:400])
    submit = driver.find_element(By.CSS_SELECTOR, 'input[type=submit]')
    print('submit hidden displayed', submit.is_displayed(), 'enabled', submit.is_enabled(), 'outerHTML', submit.get_attribute('outerHTML'))
    print('body text snippet', driver.find_element(By.TAG_NAME, 'body').text[:500])
    print('page url', driver.current_url)
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
