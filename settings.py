from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path.cwd() / ".env"


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        case_sensitive=True,
        extra="allow",
        env_prefix="ENV_POSTGRES_",
    )

    USER: str
    PASSWORD: str
    HOST: str
    PORT: str
    NAME: str

    @property
    def ADDRESS(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="APP_",
        extra="ignore",
    )

    PG: PostgresSettings = PostgresSettings()


settings: AppSettings = AppSettings()
