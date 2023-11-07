from telegram.ext import ContextTypes, CommandHandler, ConversationHandler
from telegram.ext import filters, MessageHandler
from telegram import Update, ReplyKeyboardRemove, ForceReply
from handlers.custom_handlers.history import history

RESULT = 0


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Message in case of something went wrong"""
    await update.message.reply_text('Нужно ввести натуральное число')
    return ConversationHandler.END


async def start_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Initial request of year"""
    await update.message.reply_text('Сколько последних записей показать?',
                                    reply_markup=ForceReply(selective=True),
                                    )
    return RESULT


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Хорошо, запрос отменен.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def get_history_handler() -> object:
    """Description of History_Conversation_Handler"""
    request_handler = CommandHandler('history', start_request)
    history_handler = MessageHandler(filters.Regex(r'^\s*[0-9]+\s*$'), history)

    history_request_handler = ConversationHandler(
        entry_points=[request_handler],
        states={
            RESULT: [history_handler],
        },
        fallbacks=[CommandHandler("cancel", cancel),
                   MessageHandler(filters.TEXT & (~filters.COMMAND), error)],
        allow_reentry=True,
    )
    return history_request_handler
