import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.job import Job
from core.config import settings
from jobs.reminders import check_reminders


class SchedulerManager:
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=ZoneInfo(settings.timezone))
        self.jobs = {}

    async def start(self):
        if not self.scheduler.running:
            self.scheduler.start()
            self.scheduler.add_job(
                check_reminders,
                trigger=IntervalTrigger(minutes=1),
                id="check_reminders",
                replace_existing=True,
            )

    async def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)

    def add_cron_job(
        self, func, job_id: str, hour: int, minute: int, jitter: bool = True
    ):
        trigger = CronTrigger(hour=hour, minute=minute)

        def wrapped_func():
            actual_hour = hour
            actual_minute = minute

            if jitter:
                jitter_min = settings.jitter_min
                jitter_max = settings.jitter_max
                offset = random.randint(-jitter_min, jitter_max)
                total_minutes = hour * 60 + minute + offset
                actual_hour = (total_minutes // 60) % 24
                actual_minutes = total_minutes % 60

            return func

        job = self.scheduler.add_job(
            wrapped_func,
            trigger=trigger,
            id=job_id,
            replace_existing=True,
        )
        self.jobs[job_id] = job
        return job

    def remove_job(self, job_id: str):
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
            del self.jobs[job_id]

    def get_job(self, job_id: str) -> Job:
        return self.scheduler.get_job(job_id)

    def list_jobs(self):
        return self.scheduler.get_jobs()


scheduler = SchedulerManager()