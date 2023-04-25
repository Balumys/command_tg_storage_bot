import handlers
import db_handler
import bitly_handler
import markups as m

from datetime import timedelta
from telegram.ext import (
    Filters,
    MessageHandler,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Updater,
)
from environs import Env


def start(update, context):
    user_id = update.message.from_user.id
    context.bot.send_message(
        chat_id=user_id,
        text='Доброго времени суток!\n'
             'В основном меню вы можете посмотреть список заказов,\n'
             'которые можно забрать у клиента и доставить на склад.\n'
             'А также количество переходов по рекламной ссылке.',
        reply_markup=m.client_start_keyboard()
    )


def user_input(update, context):
    user_id = update.message.from_user.id
    input_text = update.message.text
    bitly_token = '13c434ebdd562ba3e7af8a21050652022f1f836e'
    url = 'bit.ly/41Mqpoj'
    count_clicks = bitly_handler.count_clicks(bitly_token, url)
    if input_text == '🎿 Статистика':
        context.bot.send_message(
            chat_id=user_id,
            text=f'Количество переходов по рекламной ссылке {url} - '
                 f'{count_clicks}',
        )
    if input_text == '🚚 Заказы с доставкой':
        orders = db_handler.get_orders_to_delivery()
        if orders:
            update.message.reply_text(
                'Выберите номер заказа:',
                reply_markup=m.customer_orders_keyboard_(orders)
            )
        else:
            update.message.reply_text('Новых заказов готовых к доставке пока нет.')

    if input_text == '📦 Просроченные Заказы':
        orders = db_handler.get_expired_orders()
        if orders:
            update.message.reply_text(
                'Выберите номер заказа:',
                reply_markup=m.customer_orders_keyboard_(orders)
            )
        else:
            update.message.reply_text('Просроченных заказов нет.')


def print_order_info(update, context):
    query = update.callback_query
    query.answer()
    order_id = query.data.split('_')[-1]
    order_data = db_handler.get_order_by_id(order_id)
    query.edit_message_text(
        text='Данные заказа:\n' \
             f'Номер заказа - *№{order_id}*\n' \
             f'Размер бокса - *{order_data["box_size"]}*\n' \
             f'Срок начала хранения - *{order_data["created_at"].date()}*\n' \
             f'Срок окончания хранения - *{order_data["expired_at"].date()}*\n' \
             f'Общая стоимость заказа - *{order_data["price"]}*\n\n' \
             'Данные владельца заказа:\n'
             f'Имя - {order_data["customer_name"]}\n' \
             f'Номер клиента - {order_data["customer_phone"]}',
        parse_mode='markdown',
    )


def main():
    env = Env()
    env.read_env()

    tg_token = env('TG_CLIENT_BOT_TOKEN')

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler('start', start))

    # Text handlers
    dispatcher.add_handler(MessageHandler(Filters.text, user_input))

    # Callback handlers
    dispatcher.add_handler(
        CallbackQueryHandler(print_order_info, pattern=r'take_order_\d+')
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
