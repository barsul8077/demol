import json
import os
import re
import time
from typing import Dict, Optional, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config_loader import Config
from utils.logger import logger
import requests

class InstagramScraper:
    def __init__(self, headless: bool = True) -> None:
        self.headless = headless
        self.driver = self._build_driver()
        self._json_blocked = False
        self._logged_in = False
        self._login_attempted = False

    def _build_driver(self) -> webdriver.Chrome:
        options = Options()
        if self.headless:
            options.add_argument('--headless=new')
        # reduce rendering and network load to speed page loads
        options.add_experimental_option('prefs', {"profile.managed_default_content_settings.images": 2})
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--lang=en-US')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--log-level=3')
        options.add_argument('--disable-notifications')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        # prefer 'eager' page load so we can read body text earlier
        try:
            options.set_capability('pageLoadStrategy', 'eager')
        except Exception:
            pass
        try:
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(60)
            # reduce network load via CDP: block images/fonts/styles/media
            try:
                driver.execute_cdp_cmd('Network.enable', {})
                driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.css', '*.woff', '*.woff2', '*.ttf', '*.svg', '*.mp4']})
            except Exception:
                logger.debug('CDP resource blocking unavailable')
            try:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
            except Exception:
                pass
            return driver
        except WebDriverException:
            driver_path = self._resolve_chromedriver_path()
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_page_load_timeout(60)
            try:
                driver.execute_cdp_cmd('Network.enable', {})
                driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.css', '*.woff', '*.woff2', '*.ttf', '*.svg', '*.mp4']})
            except Exception:
                logger.debug('CDP resource blocking unavailable')
            return driver

    def _resolve_chromedriver_path(self) -> str:
        env_path = os.getenv('CHROME_DRIVER_PATH')
        if env_path and os.path.isfile(env_path):
            return env_path
        default_dir = os.path.expanduser('~/.wdm/drivers/chromedriver')
        if os.path.isdir(default_dir):
            for root, _, files in os.walk(default_dir):
                for filename in files:
                    if filename.lower().startswith('chromedriver') and filename.lower().endswith('.exe'):
                        return os.path.join(root, filename)
        raise WebDriverException('Unable to resolve chromedriver executable path')

    def _parse_int(self, value: Optional[Any]) -> Optional[int]:
        if value is None:
            return None
        if isinstance(value, int):
            return value
        text = str(value).strip().lower()
        if not text:
            return None
        # handle shorthand like 13k, 3.4k, 1.2m
        if text.endswith('k'):
            digits = text[:-1].replace(',', '')
            try:
                return int(float(digits) * 1000)
            except ValueError:
                pass
        if text.endswith('m'):
            digits = text[:-1].replace(',', '')
            try:
                return int(float(digits) * 1000000)
            except ValueError:
                pass
        # fallback: extract digits
        digits = ''.join(ch for ch in text if ch.isdigit())
        return int(digits) if digits else None

    def _parse_profile_text(self, body_text: str, label: str) -> Optional[int]:
        import re
        pattern = rf'([0-9][0-9\.,]*\s*[kKmM]?)\s+{label}'
        match = re.search(pattern, body_text, re.IGNORECASE)
        if not match:
            return None
        return self._parse_int(match.group(1))

    def _extract_dom_profile(self) -> Dict[str, Optional[Any]]:
        profile = {
            'followers': None,
            'following': None,
            'posts': None,
            'profile_picture': None,
            'bio': None,
            'is_verified': None,
            'category': None,
            'full_name': None,
            'external_url': None,
        }
        try:
            stats_elems = self.driver.find_elements(By.CSS_SELECTOR, 'header section ul li')
            if len(stats_elems) < 3:
                stats_elems = self.driver.find_elements(By.CSS_SELECTOR, 'header li')
            stats_texts = [el.text.strip() for el in stats_elems if el.text and el.text.strip()]
            # If we have exactly 3 items and none include explicit labels, assume standard ordering: posts, followers, following
            labeled = any(any(lbl in t.lower() for lbl in ('post', 'posts', 'follower', 'followers', 'following')) for t in stats_texts)
            if len(stats_texts) == 3 and not labeled:
                profile['posts'] = self._parse_int(stats_texts[0])
                profile['followers'] = self._parse_int(stats_texts[1])
                profile['following'] = self._parse_int(stats_texts[2])
            else:
                # prefer labeled detection
                for t in stats_texts:
                    try:
                        tl = t.lower()
                        if 'follower' in tl:
                            profile['followers'] = self._parse_int(t)
                        elif 'following' in tl and 'follower' not in tl:
                            profile['following'] = self._parse_int(t)
                        elif 'post' in tl:
                            profile['posts'] = self._parse_int(t)
                    except Exception:
                        continue
        except Exception:
            pass
        except Exception:
            pass

        try:
            body_text = self.driver.find_element(By.TAG_NAME, 'body').text
            if not profile['posts']:
                profile['posts'] = self._parse_profile_text(body_text, 'posts')
            if not profile['followers']:
                profile['followers'] = self._parse_profile_text(body_text, 'followers')
            if not profile['following']:
                profile['following'] = self._parse_profile_text(body_text, 'following')
        except Exception:
            pass

        try:
            picture = self.driver.find_element(By.CSS_SELECTOR, 'header img')
            profile['profile_picture'] = picture.get_attribute('src')
        except Exception:
            pass
        try:
            profile['full_name'] = self.driver.find_element(By.CSS_SELECTOR, 'header section h1').text.strip()
        except Exception:
            pass
        try:
            profile['bio'] = self.driver.find_element(By.CSS_SELECTOR, 'header section div.-vDIg span').text.strip()
        except Exception:
            pass
        try:
            external_link = self.driver.find_element(By.CSS_SELECTOR, 'header section div.-vDIg a')
            profile['external_url'] = external_link.get_attribute('href')
        except Exception:
            pass
        return profile

    def _extract_og_description_profile(self, page_source: str) -> Dict[str, Optional[Any]]:
        profile = {}
        try:
            og_match = re.search(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']', page_source, re.IGNORECASE)
            if not og_match:
                return {}
            description = og_match.group(1)
            if not description:
                return {}

            follower_match = re.search(r'([0-9][0-9\.,]*\s*[kKmM]?)\s+Followers', description)
            following_match = re.search(r'([0-9][0-9\.,]*\s*[kKmM]?)\s+Following', description)
            posts_match = re.search(r'([0-9][0-9\.,]*\s*[kKmM]?)\s+Posts', description)
            if follower_match:
                profile['followers'] = self._parse_int(follower_match.group(1))
            if following_match:
                profile['following'] = self._parse_int(following_match.group(1))
            if posts_match:
                profile['posts'] = self._parse_int(posts_match.group(1))
        except Exception:
            pass
        return profile

    def _extract_json_profile(self) -> Dict[str, Optional[Any]]:
        profile = {}
        try:
            page_source = self.driver.page_source or ''
            if not page_source:
                return {}

            count_patterns = {
                'followers': r'"edge_followed_by"\s*:\s*\{\s*"count"\s*:\s*([0-9]+)',
                'following': r'"edge_follow"\s*:\s*\{\s*"count"\s*:\s*([0-9]+)',
                'posts': r'"edge_owner_to_timeline_media"\s*:\s*\{\s*"count"\s*:\s*([0-9]+)',
            }
            for key, pattern in count_patterns.items():
                match = re.search(pattern, page_source)
                if match:
                    profile[key] = int(match.group(1))

            string_patterns = {
                'profile_picture': r'"profile_pic_url_hd"\s*:\s*"(.*?)"',
                'full_name': r'"full_name"\s*:\s*"(.*?)"',
                'bio': r'"biography"\s*:\s*"(.*?)"',
                'external_url': r'"external_url"\s*:\s*"(.*?)"',
                'category': r'"category_name"\s*:\s*"(.*?)"',
            }
            for key, pattern in string_patterns.items():
                match = re.search(pattern, page_source)
                if match:
                    try:
                        profile[key] = json.loads(f'"{match.group(1)}"')
                    except Exception:
                        profile[key] = match.group(1)

            verified_match = re.search(r'"is_verified"\s*:\s*(true|false)', page_source)
            if verified_match:
                profile['is_verified'] = verified_match.group(1).lower() == 'true'

            og_profile = self._extract_og_description_profile(page_source)
            for key, value in og_profile.items():
                if value is not None and profile.get(key) is None:
                    profile[key] = value
        except Exception:
            pass
        return profile

    def _fetch_public_profile(self, username: str) -> Dict[str, Optional[Any]]:
        if self._json_blocked:
            return {}

        api_url = f'{Config.INSTAGRAM_BASE_URL}/api/v1/users/web_profile_info/?username={username}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'X-IG-App-ID': '936619743392459',
            'Referer': f'{Config.INSTAGRAM_BASE_URL}/',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        try:
            response = requests.get(api_url, headers=headers, timeout=25)
            response.raise_for_status()
            data = response.json()
        except requests.HTTPError as error:
            if error.response is not None and error.response.status_code == 429:
                self._json_blocked = True
            logger.warning('Instagram public JSON fetch failed for %s: %s', username, error)
            return {}
        except Exception as error:
            logger.warning('Instagram public JSON fetch failed for %s: %s', username, error)
            return {}

        user = data.get('data', {}).get('user') or data.get('graphql', {}).get('user')
        if not user:
            logger.warning('Instagram public JSON returned no user data for %s', username)
            return {}

        return {
            'followers': self._parse_int(user.get('edge_followed_by', {}).get('count')),
            'following': self._parse_int(user.get('edge_follow', {}).get('count')),
            'posts': self._parse_int(user.get('edge_owner_to_timeline_media', {}).get('count')),
            'profile_picture': user.get('profile_pic_url_hd') or user.get('profile_pic_url'),
            'bio': user.get('biography'),
            'is_verified': user.get('is_verified'),
            'category': user.get('category_name'),
            'full_name': user.get('full_name'),
            'external_url': user.get('external_url'),
        }

    def _is_login_gate(self) -> bool:
        try:
            current_url = self.driver.current_url or ''
            body_text = self.driver.find_element(By.TAG_NAME, 'body').text.lower()
            return ('/accounts/login' in current_url
                    or 'log into instagram' in body_text
                    or 'log in' in body_text and 'save your login info' not in body_text)
        except Exception:
            return False

    def _set_input_value(self, element, value: str) -> None:
        try:
            self.driver.execute_script(
                "arguments[0].focus(); arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                element,
                value,
            )
        except Exception:
            try:
                element.clear()
                element.send_keys(value)
            except Exception:
                pass

    def _find_login_button(self):
        candidates = self.driver.find_elements(By.XPATH, "//div[@role='button' and normalize-space(text())='Log in' and not(contains(@style, 'display: none'))]")
        for candidate in candidates:
            if candidate.is_displayed():
                return candidate
        candidates = self.driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"], input[type="submit"]')
        for candidate in candidates:
            if candidate.is_displayed():
                return candidate
        return candidates[0] if candidates else None

    def _set_input_value(self, element, value: str) -> None:
        try:
            self.driver.execute_script(
                "arguments[0].focus(); arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true })); arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                element,
                value,
            )
        except Exception:
            try:
                element.clear()
                element.send_keys(value)
            except Exception:
                pass

    def _submit_login_form(self, password_input) -> bool:
        button = self._find_login_button()
        if button:
            try:
                self.driver.execute_script('arguments[0].click();', button)
                return True
            except Exception:
                pass
        try:
            password_input.send_keys(Keys.RETURN)
            return True
        except Exception:
            pass
        return False

    def scrape_profile(self, username: str) -> Dict[str, Optional[Any]]:
        logger.info('Scraping Instagram profile %s', username)
        public_profile = self._fetch_public_profile(username)
        if public_profile and any((public_profile['posts'], public_profile['followers'], public_profile['following'])):
            logger.info('Instagram public JSON fetch succeeded for %s', username)
            return public_profile

        url = f'{Config.INSTAGRAM_BASE_URL}/{username}/'
        try:
            # navigate and wait for a short ready state; if renderer is slow, fall back to JS body retrieval
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 60).until(
                    lambda d: d.execute_script('return document.readyState') in ['complete', 'interactive']
                )
            except Exception:
                logger.debug('document.readyState wait failed or timed out, continuing with DOM fallback')

            # first try normal DOM extraction
            dom_profile = self._extract_dom_profile()
            json_profile = self._extract_json_profile()
            for key, value in json_profile.items():
                if value is not None and dom_profile.get(key) is None:
                    dom_profile[key] = value

            # if DOM/json misses data, try quick JS body read to extract numbers (helps when renderer is slow)
            if not any((dom_profile.get('posts'), dom_profile.get('followers'), dom_profile.get('following'))):
                try:
                    body_text = self.driver.execute_script('return document.body && document.body.innerText ? document.body.innerText : ""')
                    if body_text:
                        if not dom_profile.get('posts'):
                            dom_profile['posts'] = self._parse_profile_text(body_text, 'posts')
                        if not dom_profile.get('followers'):
                            dom_profile['followers'] = self._parse_profile_text(body_text, 'followers')
                        if not dom_profile.get('following'):
                            dom_profile['following'] = self._parse_profile_text(body_text, 'following')
                except Exception:
                    logger.debug('JS body read fallback failed')
            if any((dom_profile.get('posts'), dom_profile.get('followers'), dom_profile.get('following'))):
                return dom_profile

            if self._is_login_gate():
                if Config.IG_LOGIN_ENABLED and Config.IG_USERNAME and Config.IG_PASSWORD and not self._login_attempted:
                    logger.info('Instagram profile requires login, retrying login attempt')
                    if self.login(Config.IG_USERNAME, Config.IG_PASSWORD):
                        return self.scrape_profile(username)
                if public_profile:
                    return public_profile
                raise ValueError('Instagram page appears blocked or requires login')

            raise ValueError('Instagram profile data not found')
        except TimeoutException as error:
            logger.error('Timeout scraping Instagram for %s: %s', username, error)
            raise
        except Exception as error:
            logger.error('Instagram scraping failed for %s: %s', username, error)
            raise

    def _find_login_element(self, selector: str):
        for _ in range(4):
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element:
                    return element
            except Exception:
                time.sleep(1)
        return None

    def login(self, username: str, password: str) -> bool:
        """Optional: login to Instagram to access more content. Returns True if login appeared successful."""
        self._login_attempted = True
        try:
            login_url = f'{Config.INSTAGRAM_BASE_URL}/accounts/login/'
            self.driver.get(login_url)
            wait = WebDriverWait(self.driver, 30)

            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="email"], input[name="username"]')))
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="pass"], input[name="password"]')))
            except Exception:
                logger.debug('Instagram login inputs did not appear in time')

            email_input = self._find_login_element('input[name="email"]') or self._find_login_element('input[name="username"]')
            password_input = self._find_login_element('input[name="pass"]') or self._find_login_element('input[name="password"]')
            if not email_input or not password_input:
                logger.error('Unable to locate Instagram login inputs')
                return False

            try:
                ActionChains(self.driver).move_to_element(email_input).click().perform()
            except Exception:
                pass
            email_input.clear()
            self._set_input_value(email_input, username)
            try:
                ActionChains(self.driver).move_to_element(password_input).click().perform()
            except Exception:
                pass
            password_input.clear()
            self._set_input_value(password_input, password)

            if not self._submit_login_form(password_input):
                logger.warning('Instagram login submit failed')

            try:
                wait.until(lambda d: d.current_url != login_url or 'save your login info' in (d.find_element(By.TAG_NAME, 'body').text.lower() if d.find_elements(By.TAG_NAME, 'body') else '') or 'turn on notifications' in (d.find_element(By.TAG_NAME, 'body').text.lower() if d.find_elements(By.TAG_NAME, 'body') else ''))
            except Exception:
                pass

            time.sleep(2)
            body_text = ''
            try:
                body_text = self.driver.find_element(By.TAG_NAME, 'body').text.lower()
            except Exception:
                pass

            if self.driver.current_url != login_url and not self._is_login_gate():
                self._logged_in = True
                logger.info('Instagram login appears successful')
                return True
            if any(keyword in body_text for keyword in ('save your login info', 'turn on notifications', 'not now')):
                self._logged_in = True
                logger.info('Instagram login appears successful after prompt')
                return True

            logger.warning('Instagram login did not show expected post-login elements; current_url=%s', self.driver.current_url)
            return False
        except Exception as e:
            logger.error('Instagram login failed: %s', e)
            return False

    def close(self) -> None:
        if self.driver:
            self.driver.quit()
            logger.info('Instagram scraper driver closed.')
