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

label_names = ['Engagement Rate', 'Avg Likes', 'Avg Comments']

try:
    driver = webdriver.Chrome(options=options)
    driver.get('https://thesocialcat.com/tools/instagram-engagement-rate-calculator')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    time.sleep(3)
    input_el = driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="Instagram username or profile URL"]')
    input_el.clear()
    input_el.send_keys('instagram')
    submit = driver.find_element(By.XPATH, "//button[contains(., 'Check Engagement Rate')]" )
    submit.click()
    time.sleep(8)
    for label in label_names:
        print('===', label)
        els = driver.find_elements(By.XPATH, f"//*[normalize-space(text())='{label}']")
        print('count', len(els))
        for i, el in enumerate(els[:10],1):
            print('--- el', i, 'tag', el.tag_name, 'class', el.get_attribute('class'))
            print('text', repr(el.text))
            try:
                parent = el.find_element(By.XPATH, 'parent::*')
                print('parent tag', parent.tag_name, 'class', parent.get_attribute('class'))
                print('parent text', repr(parent.text))
                print('parent html', parent.get_attribute('outerHTML')[:1500])
            except Exception as e:
                print('parent err', e)
            try:
                p2 = el.find_element(By.XPATH, 'ancestor::div[1]')
                print('ancestor div class', p2.get_attribute('class'))
                print('ancestor div text', repr(p2.text[:400]))
                print('ancestor html', p2.get_attribute('outerHTML')[:1500])
            except Exception as e:
                print('ancestor err', e)
            try:
                sibs = el.find_elements(By.XPATH, 'following-sibling::*')
                print('following siblings', len(sibs))
                for j, sib in enumerate(sibs[:8],1):
                    print(' sib', j, sib.tag_name, 'class', sib.get_attribute('class'), 'text=', repr(sib.text[:300]))
                    print('  html', sib.get_attribute('outerHTML')[:1200])
            except Exception as e:
                print('sibs err', e)
            try:
                ancestors = el.find_elements(By.XPATH, 'ancestor::*')
                print('ancestor count', len(ancestors))
                for j, a in enumerate(ancestors[:5],1):
                    print(' anc', j, a.tag_name, 'class', a.get_attribute('class'), 'text=', repr(a.text[:200]))
            except Exception as e:
                print('anc err', e)
    print('=== body snippet ===')
    body = driver.find_element(By.TAG_NAME, 'body').text
    print(body[:4000])
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
