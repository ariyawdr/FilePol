import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    SHORTIO_API_KEY: str = os.getenv("SHORTIO_API_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./پل_bot.db")
    ADMIN_IDS: list[int] = list(map(int, os.getenv("ADMIN_IDS", "").split(','))) if os.getenv("ADMIN_IDS") else []

settings = Settings()

