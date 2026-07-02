from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
    print('email displayed', email.is_displayed(), 'enabled', email.is_enabled())
    print('pass displayed', password.is_displayed(), 'enabled', password.is_enabled())
    ActionChains(driver).move_to_element(email).click().send_keys(Keys.CONTROL, 'a').send_keys(Keys.DELETE).send_keys('test@example.com').perform()
    time.sleep(1)
    ActionChains(driver).move_to_element(password).click().send_keys(Keys.CONTROL, 'a').send_keys(Keys.DELETE).send_keys('testpassword').perform()
    time.sleep(2)
    print('email value', email.get_attribute('value'))
    print('pass value', password.get_attribute('value'))
    login_btns = driver.find_elements(By.XPATH, "//div[@role='button' and contains(., 'Log in')]")
    print('login btn count', len(login_btns))
    for i, btn in enumerate(login_btns):
        print('btn', i, 'text', btn.text, 'displayed', btn.is_displayed(), 'enabled', btn.is_enabled(), 'disabled', btn.get_attribute('aria-disabled'))
    time.sleep(5)
    print('body snippet', driver.find_element(By.TAG_NAME, 'body').text[:500])
except Exception as e:
    import traceback; traceback.print_exc()
finally:
    driver.quit()
