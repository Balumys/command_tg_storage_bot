# import handlers
import handlers

from telegram.ext import (
    Filters,
    MessageHandler,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    RegexHandler,
    Updater,
)
from environs import Env


def main():
    env = Env()
    env.read_env()

    ORDERS, DELIVERY, PERSONAL_DATA = range(3)
    token = env('TG_CUSTOMER_BOT_TOKEN')

    updater = Updater(token)

    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", handlers.start),
            MessageHandler(Filters.text, handlers.button)
        ],
        states={
            ORDERS: [
                CallbackQueryHandler(
                    handlers.box_size_inline_menu,
                    pattern='^(S|M|L|XL)$'
                ),
                CallbackQueryHandler(
                    handlers.storage_period_inline_menu,
                    pattern='^(1_month|3_month|6_month|12_month)$'
                ),
                # RegexHandler('^(S|M|L|XL)$', handlers.box_size_inline_menu),
                # CallbackQueryHandler(two, pattern="^" + str(TWO) + "$"),
            ],
            DELIVERY: [
                CallbackQueryHandler(
                    handlers.is_delivery_inline_menu,
                    pattern='^(delivery|self_delivery)$',
                ),
            ],
            PERSONAL_DATA: [
                CallbackQueryHandler(
                    handlers.personal_data_menu,
                    pattern='^(accept|not_accept)$',
                ),
            ],
        },
        fallbacks=[CommandHandler("start", handlers.start)],
    )

    updater.dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
