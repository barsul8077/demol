from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
# headful for DOM visibility
#options.add_argument('--headless=new')
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
    print('URL:', driver.current_url)
    try:
        body = driver.find_element(By.TAG_NAME, 'body').text
        print('BODY SNIPPET:', body[:2000])
    except Exception as e:
        print('BODY ERR', e)
    # print login form fields and buttons
    for sel in ['input', 'button', 'form']:
        try:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            print(f'=== {sel.upper()} count:', len(els))
            for i, el in enumerate(els[:20], 1):
                print(i, sel, 'type=', el.get_attribute('type'), 'name=', el.get_attribute('name'), 'id=', el.get_attribute('id'), 'placeholder=', el.get_attribute('placeholder'), 'class=', el.get_attribute('class'), 'text=', el.text[:120].replace('\n',' '))
        except Exception as e:
            print('ERR', sel, e)
    print('PAGE SOURCE LENGTH:', len(driver.page_source))
    src = driver.page_source
    idx = src.lower().find('username')
    if idx != -1:
        print('SOURCE username snippet:', src[max(0, idx-200):idx+200])
    idx = src.lower().find('password')
    if idx != -1:
        print('SOURCE password snippet:', src[max(0, idx-200):idx+200])
    idx = src.lower().find('csrfmiddlewaretoken')
    if idx != -1:
        print('FOUND csrf token snippet length', 200)
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
