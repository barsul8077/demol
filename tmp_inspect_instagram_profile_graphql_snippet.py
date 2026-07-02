from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

driver = webdriver.Chrome(options=options)
try:
    driver.get('https://www.instagram.com/instagram/')
    time.sleep(8)
    pg = driver.page_source
    for token in ['graphql', 'edge_followed_by', 'edge_owner_to_timeline_media', 'followed_by', 'following', 'profile_pic_url_hd', 'web_profile_info']:
        idx = pg.find(token)
        print('token', token, 'idx', idx)
        if idx != -1:
            print(pg[max(0, idx-300):idx+600])
            print('---')
except Exception as e:
    import traceback; traceback.print_exc()
finally:
    driver.quit()
