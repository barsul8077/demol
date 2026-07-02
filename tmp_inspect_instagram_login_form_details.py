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
    forms = driver.find_elements(By.TAG_NAME, 'form')
    print('forms count', len(forms))
    for idx, form in enumerate(forms):
        print('FORM', idx, 'id=', form.get_attribute('id'), 'action=', form.get_attribute('action'), 'outer len=', len(form.get_attribute('outerHTML')))
        print(form.get_attribute('outerHTML')[:2000])
    buttons = driver.find_elements(By.CSS_SELECTOR, 'button, input[type="submit"], [role="button"]')
    print('button-like count', len(buttons))
    for idx, btn in enumerate(buttons):
        print('BTN', idx, 'tag=', btn.tag_name, 'type=', btn.get_attribute('type'), 'text=', btn.text, 'displayed=', btn.is_displayed(), 'enabled=', btn.is_enabled(), 'aria-label=', btn.get_attribute('aria-label'), 'outer len=', len(btn.get_attribute('outerHTML')))
    div_buttons = driver.find_elements(By.XPATH, '//*[(@role="button" or self::button) and (contains(., "Log in") or contains(., "Log in") )]')
    print('login buttons by role or text', len(div_buttons))
    for idx, btn in enumerate(div_buttons):
        print('BTN', idx, btn.tag_name, btn.get_attribute('type'), btn.text, btn.get_attribute('outerHTML')[:500])
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
