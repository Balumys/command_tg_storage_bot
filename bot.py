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

    ORDERS, DELIVERY, PERSONAL_DATA, CUSTOMER_PHONE, CUSTOMER_EMAIL, MY_ORDERS, UPDATE_PHONE = range(7)
    token = env('TG_CUSTOMER_BOT_TOKEN')

    updater = Updater(token)

    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", handlers.start),
            MessageHandler(
                Filters.regex(r'🎿 Оформить заказ|📕 Правила хранения|📦 Мои заказы'),
                handlers.user_input
            ),
            CallbackQueryHandler(
                handlers.promt_update_customer_phone,
                pattern='^update_customer_phone$'
            ),
        ],
        states={
            ORDERS: [
                CallbackQueryHandler(
                    handlers.box_size_inline_menu,
                    pattern='^(S|M|L|XL|dont_want_measure)$'
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
            CUSTOMER_PHONE: [
                MessageHandler(
                    Filters.regex(r'^\+7-\d{3}-\d{3}-\d{2}-\d{2}$'),
                    handlers.write_customer_phone
                ),
            ],
            CUSTOMER_EMAIL: [
                MessageHandler(
                    Filters.regex(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
                    handlers.write_customer_email
                ),
            ],
            MY_ORDERS: [
                CallbackQueryHandler(
                    handlers.take_item_back_inline_menu,
                    pattern=r'^(take_all_orders|take_order_\d+|take_items_back_delivery|take_items_back_myself)$',
                )
            ],
            UPDATE_PHONE: [
                MessageHandler(
                    Filters.regex(r'^\+7-\d{3}-\d{3}-\d{2}-\d{2}$'),
                    handlers.write_new_customer_phone
                ),
            ]
        },
        fallbacks=[CommandHandler("start", handlers.start)],
        allow_reentry=True,
    )

    updater.dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
