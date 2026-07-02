from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
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
    driver.get('https://thesocialcat.com/tools/instagram-engagement-rate-calculator')
    time.sleep(8)
    print('URL:', driver.current_url)
    print('TITLE:', driver.title)
    try:
        body = driver.find_element(By.TAG_NAME, 'body').text
        print('BODY SNIPPET:', body[:3000])
    except Exception as e:
        print('BODY ERR', e)
    for sel in ['input', 'button', 'select', 'form', 'span', 'div']:
        try:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            print(f'=== {sel.upper()} count:', len(els))
            for i, el in enumerate(els[:25], 1):
                print(i, sel, 'type=', el.get_attribute('type'), 'name=', el.get_attribute('name'), 'id=', el.get_attribute('id'), 'placeholder=', el.get_attribute('placeholder'), 'class=', el.get_attribute('class'), 'text=', el.text[:120].replace('\n',' '))
        except Exception as e:
            print('ERR', sel, e)
    print('PAGE SOURCE LENGTH:', len(driver.page_source))
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
