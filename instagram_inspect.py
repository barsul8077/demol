import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

username = 'deandriani_'
options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--lang=en-US')
options.add_argument('--window-size=1920,1080')
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
try:
    url = f'https://www.instagram.com/{username}/'
    driver.get(url)
    time.sleep(10)
    print('TITLE:', driver.title)
    body = driver.find_element(By.TAG_NAME, 'body')
    print('BODY TEXT PREFIX:', body.text[:1000])
    header = driver.find_element(By.TAG_NAME, 'header')
    print('HEADER TEXT PREFIX:', header.text[:1000])
    spans = driver.find_elements(By.CSS_SELECTOR, 'header span')
    print('HEADER span count:', len(spans))
    for i, span in enumerate(spans[:40]):
        print('SPAN', i, repr(span.text))
    lis = driver.find_elements(By.CSS_SELECTOR, 'header li')
    print('HEADER li count:', len(lis))
    for i, li in enumerate(lis[:20]):
        print('LI', i, repr(li.text))
    uls = driver.find_elements(By.CSS_SELECTOR, 'header ul')
    print('HEADER ul count:', len(uls))
    for i, ul in enumerate(uls[:10]):
        print('UL', i, repr(ul.text[:500]))
    print('PAGE SOURCE FIND profile stats snippet:')
    src = driver.page_source
    for token in ['posts', 'followers', 'following', 'g47SY', 'Y8-fY', 'k9GMp']:
        if token in src:
            print('FOUND token', token)
    snippet = src[:5000]
    print(snippet)
finally:
    driver.quit()
