from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from threading import Lock
from typing import Dict, List
from database.db_manager import DatabaseManager
from scrapers.instagram_scraper import InstagramScraper
from engagement.socialcat_scraper import SocialCatScraper
from history.history_manager import HistoryManager
from utils.logger import logger
from utils.retry import retry
from config.config_loader import Config

class ProfileService:
    def __init__(self) -> None:
        self.db_manager = DatabaseManager()
        self.history_manager = HistoryManager(self.db_manager)
        self.history_manager.create_history()
        # reuse scrapers across profiles to avoid repeated browser startup overhead
        self.instagram_scraper = InstagramScraper(headless=Config.HEADLESS)
        self.socialcat_scraper = SocialCatScraper(headless=Config.HEADLESS)
        # optional Instagram login using env credentials
        try:
            if Config.IG_LOGIN_ENABLED and Config.IG_USERNAME and Config.IG_PASSWORD:
                ok = self.instagram_scraper.login(Config.IG_USERNAME, Config.IG_PASSWORD)
                if not ok:
                    logger.warning('Instagram login configured but login attempt failed')
        except Exception:
            logger.exception('Error during Instagram login attempt')
        self.summary = {
            'total': 0,
            'processed': 0,
            'success': 0,
            'failed': 0,
            'current': None,
        }
        self._summary_lock = Lock()

    def _merge_updates(self, existing: Dict[str, any], scraped: Dict[str, any], engagement: Dict[str, any]) -> Dict[str, any]:
        payload = {}
        field_mapping = {
            'full_name': 'name',
            'external_url': 'profile_url',
            'average_likes': 'likes',
            'average_comments': 'comments',
        }
        allowed_fields = {
            'name',
            'profile_url',
            'followers',
            'following',
            'posts',
            'engagement_rate',
            'likes',
            'comments',
            'category',
            'is_verified',
        }
        for key, value in {**scraped, **engagement}.items():
            if value is None:
                continue
            mapped_key = field_mapping.get(key, key)
            if mapped_key not in allowed_fields:
                continue
            if existing.get(mapped_key) != value:
                payload[mapped_key] = value
        return payload

    def _log_changes(self, existing: Dict[str, any], scraped: Dict[str, any], engagement: Dict[str, any], username: str) -> None:
        for key, new_value in {**scraped, **engagement}.items():
            if new_value is None:
                continue
            old_value = existing.get(key)
            if old_value is not None and old_value != new_value:
                try:
                    diff = float(new_value) - float(old_value)
                except Exception:
                    diff = None
                logger.info(
                    'Change detected for %s: %s from %s to %s %s',
                    username,
                    key,
                    old_value,
                    new_value,
                    f'(diff={diff})' if diff is not None else '',
                )

    @retry(max_attempts=3, delay_seconds=5)
    def process_profile(self, profile: Dict[str, any]) -> Dict[str, any]:
        username = profile['username']
        with self._summary_lock:
            self.summary['current'] = username
        logger.info('Processing profile %s', username)
        existing_profile = self.db_manager.fetch_profile_by_username(username) or {}
        try:
            instagram_data = self.instagram_scraper.scrape_profile(username)
            engagement_data = self.socialcat_scraper.scrape_engagement(username)
            logger.info('Scraped instagram data for %s: %s', username, instagram_data)
            logger.info('Scraped engagement data for %s: %s', username, engagement_data)
            self._log_changes(existing_profile, instagram_data, engagement_data, username)
            update_payload = self._merge_updates(existing_profile, instagram_data, engagement_data)
            logger.info('Update payload for %s: %s', username, update_payload)
            if update_payload:
                self.db_manager.update_profile(username, update_payload)
            profile_id = existing_profile.get('id', profile.get('id'))
            self.history_manager.save_history(profile_id, {
                'followers': instagram_data.get('followers'),
                'following': instagram_data.get('following'),
                'posts': instagram_data.get('posts'),
                'engagement_rate': engagement_data.get('engagement_rate'),
                'average_likes': engagement_data.get('average_likes'),
                'average_comments': engagement_data.get('average_comments'),
            })
            with self._summary_lock:
                self.summary['success'] += 1
            return {
                'username': username,
                'status': 'success',
                'scraped': instagram_data,
                'engagement': engagement_data,
            }
        finally:
            # do not close shared scrapers here; they will be closed in shutdown
            pass

    def run_bulk_refresh(self, profiles: List[Dict[str, any]]) -> List[Dict[str, any]]:
        self.summary['total'] = len(profiles)
        results = []
        with ThreadPoolExecutor(max_workers=Config.MAX_WORKERS) as executor:
            futures = {executor.submit(self._process_with_error_handling, profile): profile for profile in profiles}
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                with self._summary_lock:
                    self.summary['processed'] += 1
        return results

    def run_streamed_refresh(self, profile_iterator) -> List[Dict[str, any]]:
        self.summary['total'] = 0
        results = []
        for profile in profile_iterator:
            self.summary['total'] += 1
            result = self._process_with_error_handling(profile)
            results.append(result)
            with self._summary_lock:
                self.summary['processed'] += 1
        return results

    def _process_with_error_handling(self, profile: Dict[str, any]) -> Dict[str, any]:
        username = profile['username']
        try:
            result = self.process_profile(profile)
            logger.info('Completed profile %s', username)
            return result
        except Exception as exc:
            with self._summary_lock:
                self.summary['failed'] += 1
            logger.error('Profile %s failed: %s', username, exc)
            return {'username': username, 'status': 'failed', 'error': str(exc)}

    def shutdown(self) -> None:
        self.db_manager.close()
        try:
            self.instagram_scraper.close()
        except Exception:
            pass
        try:
            self.socialcat_scraper.close()
        except Exception:
            pass
