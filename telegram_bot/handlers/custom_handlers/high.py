from telegram import Update
from telegram.ext import ContextTypes
from utils.misc.site_requests import SiteApiInterface
from database.utils.CRUD import CRUDInterface


async def high(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """The sorted list of drivers with decreasing points."""

    site = SiteApiInterface()
    response = site.get_pilots()

    user = update.effective_user.username
    CRUDInterface.create(user, '/high')
    response = '\n\n'.join(['Результаты чемпионата F1 в текущем году:', response])
    await update.message.reply_text(response)
