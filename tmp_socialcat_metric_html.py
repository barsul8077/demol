from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
# options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--lang=en-US')
options.add_argument('--window-size=1920,1080')
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

def print_elem(el, label):
    try:
        print('---', label)
        print('tag', el.tag_name, 'class', el.get_attribute('class'), 'text=', repr(el.text[:300]))
        print('outerHTML', el.get_attribute('outerHTML')[:1800])
    except Exception as e:
        print('err', e)

try:
    driver = webdriver.Chrome(options=options)
    driver.get('https://thesocialcat.com/tools/instagram-engagement-rate-calculator')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    time.sleep(3)
    input_el = driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="Instagram username or profile URL"]')
    input_el.clear()
    input_el.send_keys('instagram')
    button = driver.find_element(By.XPATH, "//button[contains(., 'Check Engagement Rate')]" )
    button.click()
    time.sleep(8)
    labels = ['Engagement Rate', 'Avg Likes', 'Avg Comments']
    for label in labels:
        elems = driver.find_elements(By.XPATH, f"//*[contains(text(), '{label}')]")
        print('LABEL', label, 'count', len(elems))
        for i, el in enumerate(elems[:5],1):
            print_elem(el, f'{label}-{i}')
            try:
                parent = el.find_element(By.XPATH, '..')
                print(' parent', parent.tag_name, 'class', parent.get_attribute('class'))
                print(' parent text', repr(parent.text[:400]))
                print(' parent outerHTML', parent.get_attribute('outerHTML')[:1800])
            except Exception as e:
                print(' parent err', e)
            try:
                sibs = el.find_elements(By.XPATH, 'following-sibling::*')
                print(' following siblings', len(sibs))
                for j, sib in enumerate(sibs[:5],1):
                    print('   sib', j, sib.tag_name, sib.get_attribute('class'), repr(sib.text[:300]))
            except Exception as e:
                print(' siblings err', e)
    print('--- end')
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
