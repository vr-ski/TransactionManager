from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # -------------------------
    # Database
    # -------------------------
    DATABASE_URL: str
    DATABASE_TEST_URL: str

    # -------------------------
    # JWT / Security
    # -------------------------
    JWT_SECRET: str = "supersecret"  # override in .env
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 12  # token lifetime

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore[call-arg]
