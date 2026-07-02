import os
import sys
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

sys.path.insert(0, os.getcwd())

username = 'deandriani_'

output = []

output.append('=== SELENIUM TEST ===')
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
    url = f'https://www.instagram.com/{username}/'
    output.append(f'Loading {url}')
    driver.get(url)
    time.sleep(10)
    output.append('TITLE: ' + driver.title)
    body = driver.find_element(By.TAG_NAME, 'body').text
    output.append('BODY TEXT PREFIX:')
    output.append(body[:2000])
    output.append('PAGE SOURCE PREFIX:')
    output.append(driver.page_source[:5000])
    scripts = driver.find_elements(By.TAG_NAME, 'script')
    output.append('SCRIPT COUNT: ' + str(len(scripts)))
    found = False
    for i, script in enumerate(scripts[:40]):
        text = script.get_attribute('innerHTML')
        if 'window._sharedData' in text or 'sharedData' in text or 'graphql' in text:
            output.append(f'FOUND script #{i} length {len(text)}')
            output.append(text[:2000])
            found = True
            break
    output.append('FOUND_SCRIPT=' + str(found))
except Exception as e:
    output.append('SELENIUM ERROR: ' + repr(e))
finally:
    try:
        driver.quit()
    except Exception:
        pass

output.append('=== HTTP TEST ===')
url = f'https://www.instagram.com/{username}/?__a=1&__d=dis'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With': 'XMLHttpRequest',
}
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read().decode('utf-8', errors='replace')
        output.append('HTTP STATUS ' + str(resp.status))
        output.append('HTTP BODY PREFIX:')
        output.append(data[:2000])
except Exception as e:
    output.append('HTTP ERROR: ' + repr(e))

with open('instagram_test_save_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
print('WROTE instagram_test_save_out.txt')
