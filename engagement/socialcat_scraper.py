import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from config.config_loader import Config
from utils.logger import logger
from typing import Dict, Optional

class SocialCatScraper:
    def __init__(self, headless: bool = True) -> None:
        self.headless = headless
        self.driver = self._build_driver()

    def _build_driver(self) -> webdriver.Chrome:
        options = Options()
        if self.headless:
            options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--lang=en-US')
        options.add_argument('--log-level=3')
        try:
            options.set_capability('pageLoadStrategy', 'eager')
        except Exception:
            pass
        try:
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(45)
            try:
                driver.execute_cdp_cmd('Network.enable', {})
                driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.css', '*.woff', '*.woff2', '*.ttf', '*.svg', '*.mp4']})
            except Exception:
                logger.debug('CDP resource blocking unavailable for SocialCat')
            return driver
        except WebDriverException:
            driver_path = self._resolve_chromedriver_path()
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_page_load_timeout(45)
            try:
                driver.execute_cdp_cmd('Network.enable', {})
                driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.css', '*.woff', '*.woff2', '*.ttf', '*.svg', '*.mp4']})
            except Exception:
                logger.debug('CDP resource blocking unavailable for SocialCat')
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
        raise WebDriverException('Unable to resolve chromedriver executable path for SocialCat')

    def scrape_engagement(self, username: str) -> Dict[str, Optional[any]]:
        logger.info('Scraping engagement for %s', username)
        engagement_rate = None
        average_likes = None
        average_comments = None
        try:
            self.driver.get(Config.SOCIALCAT_URL)
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            search_box = self._find_username_input()
            if not search_box:
                raise ValueError('Unable to locate SocialCat username input')
            search_box.clear()
            search_box.send_keys(username)
            submit_button = self._find_submit_button()
            if not submit_button:
                raise ValueError('Unable to locate SocialCat submit button')
            submit_button.click()
            WebDriverWait(self.driver, 30).until(
                lambda d: bool(d.find_elements(By.XPATH, "//span[contains(text(), 'Engagement Rate') and contains(text(), '%')]")) or bool(d.find_elements(By.XPATH, "//span[contains(text(), 'Avg Likes') or contains(text(), 'Avg Comments')]") )
            )
            body_text = self.driver.find_element(By.TAG_NAME, 'body').text
            page_html = self.driver.page_source
            metrics = self._extract_metrics_from_page(body_text, page_html)
            engagement_rate = metrics.get('engagement_rate')
            average_likes = metrics.get('average_likes')
            average_comments = metrics.get('average_comments')
            return {
                'engagement_rate': engagement_rate,
                'average_likes': average_likes,
                'average_comments': average_comments,
            }
        except Exception as error:
            logger.error('Engagement calculation failed for %s: %s', username, error)
            return {
                'engagement_rate': None,
                'average_likes': None,
                'average_comments': None,
            }
        finally:
            try:
                if (engagement_rate is None or self._parse_percentage(engagement_rate) is None) and not average_likes and not average_comments:
                    try:
                        debug_dir = os.path.join(os.getcwd(), 'debug')
                        os.makedirs(debug_dir, exist_ok=True)
                        path = os.path.join(debug_dir, f'socialcat_{username}.html')
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(self.driver.page_source)
                        logger.debug('Saved SocialCat debug page to %s', path)
                    except Exception:
                        pass
            except Exception:
                pass

    def _extract_metrics_from_page(self, body_text: str, page_html: Optional[str] = None) -> Dict[str, Optional[object]]:
        metrics = {'engagement_rate': None, 'average_likes': None, 'average_comments': None}
        if not body_text:
            return metrics

        text = body_text.replace('\n', ' ')
        html = page_html or ''
        # Prefer values occurring near the "Engagement Rate" label in the HTML
        try:
            ctx_html_pattern = r'Engagement\s*Rate[^<>]{0,200}?([0-9]+(?:\.[0-9]+)?)\s*%'
            m = re.search(ctx_html_pattern, html, re.IGNORECASE)
            if m:
                val = self._parse_percentage(m.group(1))
                if val is not None and val <= 100:
                    metrics['engagement_rate'] = val
        except Exception:
            pass

        if metrics['engagement_rate'] is None:
            # fallback to searching plain text nearby the label
            try:
                ctx_text_pattern = r'Engagement\s*Rate[^\n]{0,200}?([0-9]+(?:\.[0-9]+)?)\s*%'
                m = re.search(ctx_text_pattern, text, re.IGNORECASE)
                if m:
                    val = self._parse_percentage(m.group(1))
                    if val is not None and val <= 100:
                        metrics['engagement_rate'] = val
            except Exception:
                pass

        # If still not found, fall back to looser patterns but ensure value <=100
        if metrics['engagement_rate'] is None:
            patterns = [
                r'engagement\s*rate\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?)\s*%',
                r'([0-9]+(?:\.[0-9]+)?)\s*%\s*(?:engagement|engagement rate)',
            ]
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    val = self._parse_percentage(match.group(1))
                    if val is not None and val <= 100:
                        metrics['engagement_rate'] = val
                        break

        likes_patterns = [
            r'avg\s+likes\s*[:\-]?\s*([0-9.,kKmM]+)',
            r'average\s+likes?\s*[:\-]?\s*([0-9.,kKmM]+)',
            r'likes\s*[:\-]?\s*([0-9.,kKmM]+)',
        ]
        # Prefer likes found near 'Avg' or 'Average' labels in HTML first
        try:
            ctx_likes_html = r'(?:Avg|Average)\s+Likes[^<>]{0,200}?([0-9.,kKmM]+)'
            m = re.search(ctx_likes_html, html, re.IGNORECASE)
            if m:
                metrics['average_likes'] = self._parse_int(m.group(1))
        except Exception:
            pass

        if metrics['average_likes'] is None:
            for pattern in likes_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    metrics['average_likes'] = self._parse_int(match.group(1))
                    break

        comments_patterns = [
            r'avg\s+comments\s*[:\-]?\s*([0-9.,kKmM]+)',
            r'average\s+comments?\s*[:\-]?\s*([0-9.,kKmM]+)',
            r'comments\s*[:\-]?\s*([0-9.,kKmM]+)',
        ]
        # Prefer comments found near labels in HTML first
        try:
            ctx_comments_html = r'(?:Avg|Average)\s+Comments[^<>]{0,200}?([0-9.,kKmM]+)'
            m = re.search(ctx_comments_html, html, re.IGNORECASE)
            if m:
                metrics['average_comments'] = self._parse_int(m.group(1))
        except Exception:
            pass

        if metrics['average_comments'] is None:
            for pattern in comments_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    metrics['average_comments'] = self._parse_int(match.group(1))
                    break

        if metrics['engagement_rate'] is None:
            html_match = re.search(r'([0-9]+(?:\.[0-9]+)?)\s*%', html, re.IGNORECASE)
            if html_match:
                metrics['engagement_rate'] = self._parse_percentage(html_match.group(1))

        if metrics['average_likes'] is None:
            html_match = re.search(r'likes[^<]{0,30}?([0-9.,kKmM]+)', html, re.IGNORECASE)
            if html_match:
                metrics['average_likes'] = self._parse_int(html_match.group(1))

        if metrics['average_comments'] is None:
            html_match = re.search(r'comments[^<]{0,30}?([0-9.,kKmM]+)', html, re.IGNORECASE)
            if html_match:
                metrics['average_comments'] = self._parse_int(html_match.group(1))

        return metrics

    def _find_username_input(self):
        selectors = [
            'input[placeholder*="Instagram username or profile URL"]',
            'input[placeholder*="Instagram username"]',
            'input[placeholder*="username"]',
            'input[type="text"]',
        ]
        for selector in selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed():
                    return element
            except Exception:
                continue
        return None

    def _find_submit_button(self):
        candidate_selectors = [
            "button:enabled", 
            "button",
            "input[type='submit']",
        ]
        for selector in candidate_selectors:
            try:
                for button in self.driver.find_elements(By.CSS_SELECTOR, selector):
                    text = (button.text or '').strip()
                    if 'check engagement rate' in text.lower():
                        return button
            except Exception:
                continue
        # fallback: any visible button element
        try:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button')
            for button in buttons:
                if button.is_displayed() and button.is_enabled():
                    return button
        except Exception:
            pass
        return None

    def _extract_text(self, selector: str) -> Optional[str]:
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.text.strip()
        except Exception:
            return None

    def _extract_metric(self, patterns: list, body_text: Optional[str] = None) -> Optional[str]:
        import re
        try:
            if body_text is None:
                body_text = self.driver.find_element(By.TAG_NAME, 'body').text
            for pattern in patterns:
                match = re.search(pattern, body_text, re.IGNORECASE)
                if match:
                    return match.group(1)
        except Exception:
            pass
        return None

    def _extract_value_by_regex(self, pattern: str, body_text: Optional[str] = None) -> Optional[str]:
        import re
        try:
            if body_text is None:
                body_text = self.driver.find_element(By.TAG_NAME, 'body').text
            match = re.search(pattern, body_text, re.IGNORECASE)
            if match:
                return match.group(1)
        except Exception:
            pass
        return None

    def _parse_percentage(self, value: Optional[str]) -> Optional[float]:
        if not value:
            return None
        value = value.replace('%', '').strip()
        try:
            return float(value)
        except ValueError:
            return None

    def _parse_int(self, value: Optional[str]) -> Optional[int]:
        if not value:
            return None
        s = str(value).strip().lower()
        # handle k/m
        try:
            if s.endswith('k'):
                return int(float(s[:-1].replace(',', '')) * 1000)
            if s.endswith('m'):
                return int(float(s[:-1].replace(',', '')) * 1000000)
        except Exception:
            pass
        digits = ''.join(ch for ch in s if ch.isdigit())
        return int(digits) if digits else None

    def _find_number_near_keyword(self, keyword: str, window: int = 80) -> Optional[str]:
        """Search the page body for a number occurring within `window` characters of keyword."""
        import re
        try:
            body_text = self.driver.find_element(By.TAG_NAME, 'body').text
            # find all occurrences of keyword and look for nearest number
            positions = [m.start() for m in re.finditer(re.escape(keyword), body_text, re.IGNORECASE)]
            if not positions:
                return None
            for pos in positions:
                start = max(0, pos - window)
                end = pos + window
                segment = body_text[start:end]
                m = re.search(r'([0-9][0-9,\.]*\s*[kKmM]?)', segment)
                if m:
                    return m.group(1)
        except Exception:
            pass
        return None

    def close(self) -> None:
        if self.driver:
            self.driver.quit()
            logger.info('SocialCat scraper driver closed.')
