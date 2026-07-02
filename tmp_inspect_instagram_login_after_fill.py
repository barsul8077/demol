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
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", email, 'test@example.com')
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", password, 'testpassword')
    time.sleep(5)
    divs = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
    print('div[role=button] count', len(divs))
    for i, div in enumerate(divs[:20]):
        print('DIV', i, 'text=', repr(div.text), 'disabled=', div.get_attribute('aria-disabled'), 'class=', div.get_attribute('class'), 'displayed=', div.is_displayed(), 'enabled=', div.is_enabled())
    xpath_buttons = driver.find_elements(By.XPATH, "//div[@role='button' and contains(., 'Log in')]")
    print('xpath buttons count', len(xpath_buttons))
    for i, btn in enumerate(xpath_buttons[:20]):
        print('XBTN', i, 'text=', repr(btn.text), 'aria-disabled=', btn.get_attribute('aria-disabled'), 'style=', btn.get_attribute('style'), 'outer=', btn.get_attribute('outerHTML')[:500])
    submit = driver.find_element(By.CSS_SELECTOR, 'input[type=submit]')
    print('submit hidden displayed', submit.is_displayed(), 'enabled', submit.is_enabled(), 'outer', submit.get_attribute('outerHTML'))
    body = driver.find_element(By.TAG_NAME, 'body').text
    print('body snippet', body[:800])
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
