from dataclasses import dataclass
import os
import dotenv

dotenv.load_dotenv()

@dataclass
class Settings:
    bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN")
    environment: str = os.getenv("ENV", "dev")

settings = Settings()
