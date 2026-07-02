from config.config_loader import Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--lang=en-US')
options.add_argument('--window-size=1920,1080')
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

print('IG_LOGIN_ENABLED', Config.IG_LOGIN_ENABLED)
print('IG_USERNAME set', bool(Config.IG_USERNAME))
print('IG_PASSWORD set', bool(Config.IG_PASSWORD))

try:
    driver = webdriver.Chrome(options=options)
    login_url = f'{Config.INSTAGRAM_BASE_URL}/accounts/login/'
    driver.get(login_url)
    time.sleep(6)
    print('initial url:', driver.current_url)
    email = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
    password = driver.find_element(By.CSS_SELECTOR, 'input[name="pass"]')
    print('email displayed', email.is_displayed(), 'password displayed', password.is_displayed())
    for inp in [email, password]:
        print('input attr', inp.get_attribute('name'), inp.get_attribute('type'), inp.get_attribute('value'))
    actions = ActionChains(driver)
    actions.move_to_element(email).click().send_keys(Config.IG_USERNAME).perform()
    time.sleep(1)
    actions.move_to_element(password).click().send_keys(Config.IG_PASSWORD).perform()
    time.sleep(1)
    login_buttons = driver.find_elements(By.XPATH, "//div[@role='button' and contains(., 'Log in')]")
    print('login_buttons count', len(login_buttons))
    for i, btn in enumerate(login_buttons, 1):
        print(i, 'text=', btn.text, 'displayed=', btn.is_displayed(), 'enabled=', btn.is_enabled(), 'outerHTML=', btn.get_attribute('outerHTML')[:500])
    if login_buttons:
        try:
            login_buttons[0].click()
            print('clicked login button')
        except Exception as e:
            print('click failed', e)
            try:
                driver.execute_script('arguments[0].click();', login_buttons[0])
                print('JS clicked login button')
            except Exception as e2:
                print('JS click failed', e2)
    else:
        password.send_keys(Keys.RETURN)
        print('sent RETURN to password')
    time.sleep(8)
    print('after submit url:', driver.current_url)
    body_text = driver.find_element(By.TAG_NAME, 'body').text
    print('body snippet', body_text[:1200])
    errors = [el.text for el in driver.find_elements(By.XPATH, "//*[contains(text(),'The password you') or contains(text(),'Sorry,') or contains(text(),'Please wait') or contains(text(),'challenge') or contains(text(),'Try again')]")]
    print('error-like texts:', errors)
    src = driver.page_source
    idx = src.find('login')
    print('page source login snippet around first occurrence:', src[idx:idx+500] if idx != -1 else 'none')
except Exception as e:
    import traceback; traceback.print_exc()
finally:
    try:
        driver.quit()
    except Exception:
        pass
