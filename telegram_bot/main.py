from utils.get_tg_token import get_TG_token
import logging
from telegram.ext import ApplicationBuilder
from utils.set_handlers import get_handlers

if __name__ == "__main__":
    token = get_TG_token()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    application = ApplicationBuilder().token(token).build()

    handlers = get_handlers()
    application.add_handlers(handlers)

    application.run_polling()
