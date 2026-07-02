from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    time.sleep(3)
    search_box = driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="Instagram username or profile URL"]')
    search_box.clear()
    search_box.send_keys('instagram')
    button = driver.find_element(By.XPATH, "//button[contains(., 'Check Engagement Rate')]")
    button.click()
    time.sleep(8)
    # find all card groups that contain metric labels and numeric values
    elems = driver.find_elements(By.XPATH, "//*[normalize-space(text())='Avg Likes' or normalize-space(text())='Avg Comments' or normalize-space(text())='Engagement Rate']")
    for el in elems:
        print('------')
        print('text', repr(el.text))
        print('tag', el.tag_name, 'class', el.get_attribute('class'))
        try:
            print('outerHTML', el.get_attribute('outerHTML')[:2000])
        except Exception as e:
            print('outerHTML err', e)
        try:
            parent = el.find_element(By.XPATH, 'parent::*')
            print('parent text', repr(parent.text))
            print('parent class', parent.get_attribute('class'))
            print('parent outerHTML', parent.get_attribute('outerHTML')[:2000])
        except Exception as e:
            print('parent err', e)
        try:
            for rel in ['following-sibling::*', 'preceding-sibling::*', 'ancestor::div[1]', 'ancestor::div[2]', 'ancestor::div[3]']:
                items = el.find_elements(By.XPATH, rel)
                print(rel, len(items))
                for i, item in enumerate(items[:6],1):
                    print(' ', rel, i, item.tag_name, item.get_attribute('class'), repr(item.text[:400]))
        except Exception as e:
            print('sibling/ancestor err', e)
    print('--- all displayed elements containing digits ---')
    digits = driver.find_elements(By.XPATH, "//*[contains(text(),'0') or contains(text(),'1') or contains(text(),'2') or contains(text(),'3') or contains(text(),'4') or contains(text(),'5') or contains(text(),'6') or contains(text(),'7') or contains(text(),'8') or contains(text(),'9')]")
    print('count digits', len(digits))
    for el in digits[:50]:
        text = el.text.strip()
        if text and len(text) < 30 and any(ch.isdigit() for ch in text):
            print('digit el', el.tag_name, el.get_attribute('class'), repr(text))
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
