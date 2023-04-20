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
    updater.dispatcher.add_handler(CallbackQueryHandler(handlers.take_item_back_inline_menu))
    updater.dispatcher.add_handler(CallbackQueryHandler(handlers.make_order_inline_menu))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
