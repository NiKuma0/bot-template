from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    bot_token: str
    postgres_dsn: PostgresDsn = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/app"
    )


def get_settings(env_file=None) -> Settings:
    return Settings(_env_file=env_file)
