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

try:
    driver = webdriver.Chrome(options=options)
    driver.get('https://thesocialcat.com/tools/instagram-engagement-rate-calculator')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    time.sleep(3)
    input_el = driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="Instagram username or profile URL"]')
    print('Found input', input_el.get_attribute('outerHTML'))
    input_el.clear()
    input_el.send_keys('instagram')
    button = driver.find_element(By.XPATH, "//button[contains(., 'Check Engagement Rate')]" )
    print('Found button', button.get_attribute('outerHTML'))
    button.click()
    time.sleep(5)
    print('After click URL', driver.current_url)
    body = driver.find_element(By.TAG_NAME, 'body').text
    print('BODY LENGTH', len(body))
    keywords = ['Engagement Rate', 'Average likes', 'Average comments', 'likes', 'comments', 'followers', 'engagement']
    low = body.lower()
    for kw in keywords:
        idx = low.find(kw.lower())
        if idx != -1:
            print('FOUND', kw, 'at', idx)
            print('SNIPPET:', body[max(0, idx-80):idx+200].replace('\n', ' '))
    # print elements containing keywords
    elems = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'engagement') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'likes') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'comments')]")
    print('Found keyword elements count', len(elems))
    for i, el in enumerate(elems[:50], 1):
        print(i, el.tag_name, el.get_attribute('class'), repr(el.text[:200]))
    print('PAGE SOURCE LENGTH', len(driver.page_source))
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
