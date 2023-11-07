from typing import Dict
from telegram.ext import filters, CommandHandler, MessageHandler
from handlers.default_handlers.start import start
from handlers.default_handlers.echo import echo
from handlers.default_handlers.help import f1
from handlers.custom_handlers.high import high
from handlers.custom_handlers.low import low
from states.custom_request_state import get_custom_handler
from states.history_state import get_history_handler


def get_handlers() -> Dict:
    """Forms dict of all handlers for bot"""
    handlers = dict()
    list_handlers = []

    start_handler = CommandHandler('start', start)
    list_handlers.append(start_handler)

    high_handler = CommandHandler('high', high)
    list_handlers.append(high_handler)

    low_handler = CommandHandler('low', low)
    list_handlers.append(low_handler)

    help_handler = CommandHandler('help', f1)
    list_handlers.append(help_handler)

    custom_request_handler = get_custom_handler()
    list_handlers.append(custom_request_handler)

    history_handler = get_history_handler()
    list_handlers.append(history_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    list_handlers.append(echo_handler)

    handlers[0] = list_handlers
    return handlers
