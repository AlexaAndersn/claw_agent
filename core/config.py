from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    telegram_bot_token: str = Field(default="", alias="TELEGRAM_BOT_TOKEN")
    max_bot_token: str = Field(default="", alias="MAX_BOT_TOKEN")
    max_webhook_url: str = Field(default="", alias="MAX_WEBHOOK_URL")
    admin_chat_ids: str = Field(default="", alias="ADMIN_CHAT_IDS")
    yandex_weather_api_key: str = Field(default="", alias="YANDEX_WEATHER_API_KEY")
    database_url: str = Field(
        default="sqlite+aiosqlite:///claw_agent.db",
        alias="DATABASE_URL"
    )

    jitter_min: int = Field(default=15, alias="JITTER_MIN")
    jitter_max: int = Field(default=30, alias="JITTER_MAX")

    morning_hour: int = Field(default=8, alias="MORNING_HOUR")
    morning_minute: int = Field(default=0, alias="MORNING_MINUTE")
    night_hour: int = Field(default=23, alias="NIGHT_HOUR")
    night_minute: int = Field(default=0, alias="NIGHT_MINUTE")

    timezone: str = Field(default="Europe/Moscow", alias="TIMEZONE")
    default_city: str = Field(default="Казань", alias="DEFAULT_CITY")

    def get_admin_ids(self) -> List[int]:
        if not self.admin_chat_ids:
            return []
        return [int(x.strip()) for x in self.admin_chat_ids.split(",") if x.strip()]


settings = Settings()