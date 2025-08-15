from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str | None = None
    SQLALCHEMY_DATABASE_URL: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL
