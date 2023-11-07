from telegram import Update
from telegram.ext import ContextTypes


async def f1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    text = '\n'.join(['/high - список пилотов отсортированный по убыванию их очков в текущем году',
                      '/low - список пилотов отсортированный по возрастанию их очков в текущем году',
                      '/custom - список пилотов (отсортированный по возрастанию или убыванию их очков) в указанном году',
                      '/history - история запросов',
                      ])
    await update.message.reply_text(text)
