from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from services.profile_service import ProfileService
from utils.logger import logger

class JobScheduler:
    def __init__(self, cron_expression: str):
        self.cron_expression = cron_expression
        self.scheduler = BackgroundScheduler()
        self.profile_service = ProfileService()

    def _refresh_all(self) -> None:
        logger.info('Scheduler triggered refresh at %s', datetime.now())
        profile_iterator = self.profile_service.db_manager.iter_usernames()
        self.profile_service.run_streamed_refresh(profile_iterator)

    def start(self) -> None:
        fields = self.cron_expression.split()
        if len(fields) != 5:
            raise ValueError('Invalid cron expression for scheduler')
        trigger = CronTrigger(
            minute=fields[0],
            hour=fields[1],
            day=fields[2],
            month=fields[3],
            day_of_week=fields[4],
        )
        self.scheduler.add_job(self._refresh_all, trigger)
        self.scheduler.start()
        logger.info('Scheduler started with cron %s', self.cron_expression)

    def shutdown(self) -> None:
        self.scheduler.shutdown(wait=False)
        self.profile_service.shutdown()
        logger.info('Scheduler shutdown complete.')
