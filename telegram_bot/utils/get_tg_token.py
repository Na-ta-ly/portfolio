from config_data.classes import BotSettings


def get_TG_token() -> str:
    """Returns Telegram token"""
    bot = BotSettings()
    token = bot.token.get_secret_value()

    return token
