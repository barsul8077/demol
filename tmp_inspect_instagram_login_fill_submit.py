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

driver = webdriver.Chrome(options=options)
try:
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(8)
    username = 'test@example.com'
    password = 'testpassword'
    script = """
    var form = document.getElementById('login_form');
    if (!form) { return 'no form'; }
    var email = form.querySelector('input[name=email]');
    var pass = form.querySelector('input[name=pass]');
    if (!email || !pass) { return 'no fields'; }
    email.focus();
    email.value = arguments[0];
    email.dispatchEvent(new Event('input', { bubbles: true }));
    pass.focus();
    pass.value = arguments[1];
    pass.dispatchEvent(new Event('input', { bubbles: true }));
    return 'set';
    """
    result = driver.execute_script(script, username, password)
    print('fill result', result)
    time.sleep(2)
    submit = driver.execute_script("var f=document.getElementById('login_form'); if(f){f.submit(); return 'submitted';} return 'noform';")
    print('submit result', submit)
    time.sleep(8)
    print('current_url', driver.current_url)
    print('body snippet', driver.find_element(By.TAG_NAME, 'body').text[:800])
except Exception as e:
    import traceback; traceback.print_exc()
finally:
    try: driver.quit()
    except Exception: pass
