import handlers

from telegram.ext import Updater, CallbackQueryHandler
from environs import Env


def main():
    env = Env()
    env.read_env()

    tg_bot_token = env('TG_CUSTOMER_BOT_TOKEN')

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(handlers.start_handler)
    dispatcher.add_handler(handlers.button_handler)
    dispatcher.add_handler(
        CallbackQueryHandler(handlers.take_item_back_inline_menu, pattern='take_items')
    )
    dispatcher.add_handler(
        CallbackQueryHandler(handlers.take_item_back_inline_menu, pattern='take_items')
    )
    dispatcher.add_handler(
        CallbackQueryHandler(handlers.make_order_inline_menu)
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
