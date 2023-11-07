from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database.utils.CRUD import CRUDInterface


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """The list of last user requests."""

    user = update.effective_user
    info = update.message.text

    number = int(info)

    CRUDInterface().create(user.username, '/history ' + str(number))
    response = CRUDInterface().retrieve(user.username, number)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return ConversationHandler.END
