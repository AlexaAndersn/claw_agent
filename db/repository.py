from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Account, Schedule, MessageLog, User, Reminder
from db.database import db
from typing import List, Optional


class AccountRepository:
    async def get_all(self) -> List[Account]:
        async with db.get_session() as session:
            result = await session.execute(select(Account).where(Account.active == True))
            return list(result.scalars().all())

    async def get_by_chat_id(self, chat_id: str) -> Optional[Account]:
        async with db.get_session() as session:
            result = await session.execute(
                select(Account).where(Account.chat_id == chat_id)
            )
            return result.scalar_one_or_none()

    async def create(
        self, platform: str, chat_id: str, name: str
    ) -> Account:
        async with db.get_session() as session:
            account = Account(platform=platform, chat_id=chat_id, name=name)
            session.add(account)
            await session.flush()
            return account

    async def deactivate(self, chat_id: str):
        async with db.get_session() as session:
            result = await session.execute(
                select(Account).where(Account.chat_id == chat_id)
            )
            account = result.scalar_one_or_none()
            if account:
                account.active = False


class ScheduleRepository:
    async def get_all(self) -> List[Schedule]:
        async with db.get_session() as session:
            result = await session.execute(
                select(Schedule).where(Schedule.enabled == True)
            )
            return list(result.scalars().all())

    async def get_by_type(self, job_type: str) -> Optional[Schedule]:
        async with db.get_session() as session:
            result = await session.execute(
                select(Schedule).where(Schedule.job_type == job_type)
            )
            return result.scalar_one_or_none()

    async def create(
        self,
        job_type: str,
        hour: int,
        minute: int,
        jitter_min: int = 15,
        jitter_max: int = 30,
    ) -> Schedule:
        async with db.get_session() as session:
            schedule = Schedule(
                job_type=job_type,
                hour=hour,
                minute=minute,
                jitter_min=jitter_min,
                jitter_max=jitter_max,
            )
            session.add(schedule)
            await session.flush()
            return schedule


class MessageLogRepository:
    async def log(
        self, job_type: str, chat_id: str, message: str
    ) -> MessageLog:
        async with db.get_session() as session:
            log_entry = MessageLog(
                job_type=job_type, chat_id=chat_id, message=message
            )
            session.add(log_entry)
            await session.flush()
            return log_entry


class UserRepository:
    async def get_by_chat_id(self, chat_id: str) -> Optional[User]:
        async with db.get_session() as session:
            result = await session.execute(
                select(User).where(User.chat_id == chat_id)
            )
            return result.scalar_one_or_none()

    async def get_or_create(self, chat_id: str, name: str = "") -> User:
        async with db.get_session() as session:
            result = await session.execute(
                select(User).where(User.chat_id == chat_id)
            )
            user = result.scalar_one_or_none()
            if not user:
                user = User(chat_id=chat_id, name=name or "Unknown")
                session.add(user)
                await session.flush()
            return user

    async def update_settings(
        self, chat_id: str, timezone: str = None, city: str = None, plan: str = None
    ):
        async with db.get_session() as session:
            result = await session.execute(
                select(User).where(User.chat_id == chat_id)
            )
            user = result.scalar_one_or_none()
            if user:
                if timezone:
                    user.timezone = timezone
                if city:
                    user.city = city
                if plan is not None:
                    user.plan_for_tomorrow = plan


class ReminderRepository:
    async def create(
        self, chat_id: str, title: str, remind_at: datetime, minutes_before: int = 0
    ) -> Reminder:
        async with db.get_session() as session:
            reminder = Reminder(
                chat_id=chat_id,
                title=title,
                remind_at=remind_at,
                minutes_before=minutes_before,
            )
            session.add(reminder)
            await session.flush()
            return reminder

    async def get_pending(self) -> List[Reminder]:
        async with db.get_session() as session:
            result = await session.execute(
                select(Reminder)
                .where(Reminder.sent == False)
                .where(Reminder.remind_at <= datetime.utcnow())
            )
            return list(result.scalars().all())

    async def mark_sent(self, reminder_id: int):
        async with db.get_session() as session:
            result = await session.execute(
                select(Reminder).where(Reminder.id == reminder_id)
            )
            reminder = result.scalar_one_or_none()
            if reminder:
                reminder.sent = True


account_repo = AccountRepository()
schedule_repo = ScheduleRepository()
message_log_repo = MessageLogRepository()
user_repo = UserRepository()
reminder_repo = ReminderRepository()