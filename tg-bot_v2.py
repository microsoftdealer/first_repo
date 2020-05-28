from telegram import Update
from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

from bot_config import TG_TOKEN
from bot_config import TG_API_URL

def main():
    print('Python TG bot for Avito v0.02 starting...')

    updater = Updater(
            token = TG_TOKEN,
            use_context = True,
            base_url = TG_API_URL,
            )
    print(updater.bot.get_me())

    updater.dispatcher.add_handler(MessageHandler(Filters.all, callback=message_handler))
    
    updater.start_polling()
    print('Bot is working now!')
    updater.idle()

    print('Finish!')

button_help = 'Помощь'

def log_error(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'Ошибка: {e}')
            raise e
    return inner

def button_help_handler(update: Update, context: CallbackContext):
        update.message.reply_text(
                text = 'Помощь! Мануал! Все тут!',
                reply_markup = ReplyKeyboardRemove(),

                )

@log_error
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == button_help:
        return button_help_handler(update=update, context=context)

    reply_markup = ReplyKeyboardMarkup(
            keyboard = [
                [
                    KeyboardButton(text=button_help),
                    ],
                ],
            resize_keyboard = True,
            )
    
    update.message.reply_text(
            text = 'Привет! Нажми кнопку ниже!',
            reply_markup=reply_markup,
            )


if __name__ == '__main__':
    main()
