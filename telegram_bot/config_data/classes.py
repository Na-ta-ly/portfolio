import os
from pydantic import BaseSettings, SecretStr, StrictStr


class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv('SITE_API_KEY', None)
    api_host: StrictStr = os.getenv('SITE_API_HOST', None)


class BotSettings(BaseSettings):
    token: SecretStr = os.getenv('BOT_TOKEN', None)
