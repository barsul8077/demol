from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    print('email visible', email.is_displayed(), 'enabled', email.is_enabled())
    print('pass visible', password.is_displayed(), 'enabled', password.is_enabled())
    driver.execute_script(
        "arguments[0].focus(); arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new InputEvent('input', { bubbles: true, composed: true, data: arguments[1] })); arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
        email,
        'test@example.com',
    )
    driver.execute_script(
        "arguments[0].focus(); arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new InputEvent('input', { bubbles: true, composed: true, data: arguments[1] })); arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
        password,
        'testpassword',
    )
    time.sleep(3)
    print('email value', email.get_attribute('value'))
    print('pass value', password.get_attribute('value'))
    ActionChains(driver).move_to_element(password).click().send_keys(Keys.ENTER).perform()
    time.sleep(8)
    print('after url', driver.current_url)
    print('body snippet', driver.find_element(By.TAG_NAME, 'body').text[:1000])
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
