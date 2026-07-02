import argparse
import time
from datetime import datetime
from services.profile_service import ProfileService
from scheduler.job_scheduler import JobScheduler
from gui.preview import PreviewGUI
from config.config_loader import Config
from utils.logger import configure_logging, logger


def build_dashboard_data(summary: dict, username: str, details: dict) -> dict:
    remaining = max(summary['total'] - summary['processed'], 0)
    progress = (summary['processed'] / summary['total'] * 100) if summary['total'] else 0
    return {
        'username': username,
        'status': 'Running' if summary['processed'] < summary['total'] else 'Completed',
        'processed': summary['processed'],
        'remaining': remaining,
        'success': summary['success'],
        'failed': summary['failed'],
        'progress': progress,
        'details': details,
    }


def run_refresh(gui: PreviewGUI, service: ProfileService) -> None:
    profile_iterator = service.db_manager.iter_usernames()
    for profile in profile_iterator:
        username = profile['username']
        with service._summary_lock:
            service.summary['current'] = username
            service.summary['total'] += 1
        gui.update(build_dashboard_data(service.summary, username, {}))
        try:
            result = service.process_profile(profile)
            details = {**result['scraped'], **result['engagement']}
            gui.update(build_dashboard_data(service.summary, username, details))
        except Exception as error:
            logger.error('Manual refresh failed for %s: %s', username, error)
            gui.update(build_dashboard_data(service.summary, username, {}))
        time.sleep(0.2)
    gui.update(build_dashboard_data(service.summary, '', {}))


def main() -> None:
    configure_logging()
    parser = argparse.ArgumentParser(description='Instagram Profile Auto Update System')
    parser.add_argument('--schedule', action='store_true', help='Start scheduler for daily refresh')
    args = parser.parse_args()
    gui = PreviewGUI()
    service = ProfileService()
    if args.schedule:
        scheduler = JobScheduler(Config.SCHEDULER_CRON)
        scheduler.start()
        logger.info('Scheduler is running. Press Ctrl+C to stop.')
        try:
            gui.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
            service.shutdown()
    else:
        logger.info('Starting manual refresh...')
        import threading
        worker = threading.Thread(target=lambda: run_refresh(gui, service), daemon=True)
        worker.start()
        try:
            gui.start()
        finally:
            service.shutdown()


if __name__ == '__main__':
    main()
