from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler, ConversationHandler
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from handlers.custom_handlers.custom import custom
from utils.misc.button_builder import get_year_buttons

ORDER, RESULT = range(2)


async def order_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Saving year and request for order"""
    query = update.callback_query
    await query.answer()
    context.user_data['year'] = query.data

    keyboard = [[InlineKeyboardButton('high', callback_data=0),
                 InlineKeyboardButton('low', callback_data=1)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(f'Выбран сезон: {context.user_data["year"]}\nСортировать, начиная с самых высоких или с низких?',
                                                  reply_markup=reply_markup)

    return RESULT


async def year_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start request of year"""
    option_list = get_year_buttons()
    keyboard = option_list
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Какой год интересует?', reply_markup=reply_markup)

    return ORDER


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Хорошо, запрос отменен.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def get_custom_handler() -> object:
    """Description of Custom_Conversation_Handler"""
    year_handler = CommandHandler('custom', year_request)
    order_handler = CallbackQueryHandler(order_request)
    custom_handler = CallbackQueryHandler(custom)

    custom_request_handler = ConversationHandler(
        entry_points=[year_handler],
        states={
            ORDER: [order_handler],
            RESULT: [custom_handler],
        },
        allow_reentry=True,
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    return custom_request_handler
