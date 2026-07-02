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
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    print('input count', len(inputs))
    for i, inp in enumerate(inputs, 1):
        print(i, 'name=', inp.get_attribute('name'), 'type=', inp.get_attribute('type'), 'displayed=', inp.is_displayed(), 'value=', inp.get_attribute('value'))
    buttons = driver.find_elements(By.XPATH, "//button|//div[@role='button']")
    print('buttons count', len(buttons))
    for i, btn in enumerate(buttons, 1):
        print(i, 'tag=', btn.tag_name, 'role=', btn.get_attribute('role'), 'text=', btn.text, 'enabled=', btn.is_enabled())
    src = driver.page_source
    print('page source contains login form', 'username' in src.lower() or 'email' in src.lower())
    print('body snippet', driver.find_element(By.TAG_NAME, 'body').text[:400])
except Exception as e:
    import traceback; traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
