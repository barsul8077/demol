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

browser = webdriver.Chrome(options=options)
try:
    browser.get('https://www.instagram.com/accounts/login/')
    time.sleep(10)
    email = browser.find_element(By.CSS_SELECTOR, 'input[name=email]')
    password = browser.find_element(By.CSS_SELECTOR, 'input[name=pass]')
    ActionChains(browser).move_to_element(email).click().send_keys('test@example.com').perform()
    time.sleep(1)
    ActionChains(browser).move_to_element(password).click().send_keys('testpassword').perform()
    time.sleep(2)
    login_divs = browser.find_elements(By.XPATH, "//div[@role='button' and normalize-space(text())='Log in']")
    print('login div count', len(login_divs))
    for i, d in enumerate(login_divs):
        print('div', i, 'text=', repr(d.text), 'aria-disabled=', d.get_attribute('aria-disabled'), 'displayed=', d.is_displayed(), 'enabled=', d.is_enabled())
    if login_divs:
        try:
            print('clicking div via javascript')
            browser.execute_script('arguments[0].click();', login_divs[0])
        except Exception as e:
            print('js click failed', e)
        try:
            login_divs[0].click()
            print('element click attempted')
        except Exception as e:
            print('element click failed', e)
    time.sleep(8)
    print('after click url', browser.current_url)
    print('body snippet', browser.find_element(By.TAG_NAME, 'body').text[:1200])
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    browser.quit()
