from dataclasses import dataclass
import os

@dataclass
class Settings:
    bot_token: str = os.getenv( "TELEGRAM_BOT_TOKEN", "")
    environment: str = os.getenv("ENV", "dev")

settings = Settings()
