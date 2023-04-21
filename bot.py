import handlers

from telegram.ext import Updater, CallbackQueryHandler
from environs import Env


def main():
    env = Env()
    env.read_env()

    token = env('TG_CUSTOMER_BOT_TOKEN')

    updater = Updater(token)
    updater.dispatcher.add_handler(handlers.start_handler)
    updater.dispatcher.add_handler(handlers.button_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(handlers.callback_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()