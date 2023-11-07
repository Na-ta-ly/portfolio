from telegram import Update
from telegram.ext import ContextTypes
from utils.misc.site_requests import SiteApiInterface
from database.utils.CRUD import CRUDInterface


async def low(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """The sorted list of drivers with increasing points."""

    site = SiteApiInterface()
    response = site.get_pilots(reverse=True)

    user = update.effective_user.username
    CRUDInterface.create(user, '/low')

    response = '\n\n'.join(['Результаты чемпионата F1 в текущем году:', response])
    await update.message.reply_text(response)
