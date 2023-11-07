from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.misc.site_requests import SiteApiInterface
from database.utils.CRUD import CRUDInterface


async def custom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """The sorted list of drivers with their points in chosen year."""
    query = update.callback_query
    await query.answer()
    context.user_data['order'] = False if query.data == '0' else True

    year = int(context.user_data.get('year'))
    order = context.user_data.get('order')

    site = SiteApiInterface()
    response = site.get_pilots(year, order)
    user = update.effective_user.username
    CRUDInterface.create(user, ' '.join(['/custom', str(year), str(order)]))

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return ConversationHandler.END
