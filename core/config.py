from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    ENV: str = os.getenv("ENV", "development")

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:pass@localhost/db"
    )

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "default_secret_key_123"
    )

    ALGORITHM: str = os.getenv(
        "ALGORITHM",
        "HS256"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "30"
    ))


settings = Settings()
