from telegram import Update
from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from bot.config import TG_TOKEN
from bot.config import TG_API_URL

def main():
    bot = Bot(
            token = TG_TOKEN,
            base_url = TG_API_URL,
            )
    updater = Updater(
            bot=bot,
            )
    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


def do_start(bot: Bot, update: Update):
    bot.send_message(
            chat_id = update.message.chat_id,
            text = "Привет, отправь мне что-нибудь!",
            )

def do_echo(bot: Bot, update: Update):
    text = update.message.text
    bot.send_message(
            chat_id = update.message.chat_id,
            text = text, 
            )

if __name__ == '__main__':
    main()
