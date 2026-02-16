from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # -------------------------
    # Database
    # -------------------------
    DATABASE_URL: str  # type: ignore[call-arg]
    DATABASE_TEST_URL: str  # type: ignore[call-arg]

    # -------------------------
    # JWT / Security
    # -------------------------
    JWT_SECRET: str = "supersecret"  # override in .env
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 12  # token lifetime

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
