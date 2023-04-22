import re
import db_handler
import markups as m
import sqlalchemy

from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from db import Base, Customer, Orders, Storage, Box


def start(update, context):
    hello_message_to_new_user = """
        Вас приветствует *Garbage Collector* — Склад индивидуального хранения!
        Вас интересует аренда бокса? С радостью проконсультируем по нашим услугам.
        А пока посмотрите примеры и тд...,
    """
    first_name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    try:
        db_handler.add_customer(first_name, user_id)
    except sqlalchemy.exc.IntegrityError:
        print('Пользователь уже зарегистрирован')
    photo_path = 'media/storage.jpg'
    with open(photo_path, 'rb') as file:
        update.message.reply_photo(
            photo=file,
            caption=f"Приветствуем Вас *{first_name}*, {hello_message_to_new_user}",
            reply_markup=m.start_keyboard(),
            parse_mode='markdown'
        )


def button(update, context):
    text = update.message.text
    if text == "🎿 Оформить заказ":
        storage_address = db_handler.get_storage_addresses()
        # INLINE MENU
        update.message.reply_text(
            'Мы предоставляем стандартные размеры коробок для хранения. Если вы знаете точный размер, выберите '
            'подходящий для вас вариант. \nЕсли же вы не уверены в нужном размере, наши консультанты помогут вам '
            'выбрать подходящую коробку при вашем визите на склад.\nТакже наш курьер может замерить необходимые '
            'параметры, чтобы помочь вам определиться с выбором.\n'
            f'Наш склад находиться по адресу: *{storage_address}*',
            parse_mode='Markdown',
            reply_markup=m.box_size_keyboard()
        )
        return 0  # ORDERS

    elif text == "📕 Правила хранения":
        storage_rules = 'Спасибо, что выбрали наш сервис сезонного хранения вещей *Garbage Collector*. Наше хранилище ' \
                        'не принимает в хранение *жидкости, наркотики, биткоины, оружие и другие неприемлемые вещи*. ' \
                        'У нас есть ограничение на количество хранимых вещей. Хранение происходит на свой страх и ' \
                        'риск. *Пожалуйста, забирайте свои вещи вовремя*, чтобы избежать огромных финансовых потерь. '
        update.message.reply_text(storage_rules, parse_mode='Markdown')

    elif text == "📦 Мои заказы":
        user_id = update.message.from_user.id
        orders = db_handler.get_customer_orders(user_id)
        if orders:
            update.message.reply_text(
                'Выберите номер заказа:',
                parse_mode='Markdown',
                reply_markup=m.customer_orders(orders)
            )
        else:
            update.message.reply_text(
                'Простите, но кажется у вас еще нет барахла на хранении 😞\n',
                'Пожалуйста оформите заказ.',
                parse_mode='Markdown',
                # кнопка назад?
            )


def take_item_back_inline_menu(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'take_items_all':
        text = 'Вы собираетесь забрать все вещи:\nВыберите способ доставки'
        query.edit_message_text(
            text=text,
            reply_markup=m.take_items_back_delivery_keyboard()
        )
    if query.data == 'take_items_partial':
        text = 'Вы собираетесь забрать часть вещей:\nВыберите способ доставки'
        query.edit_message_text(
            text=text,
            reply_markup=m.take_items_back_delivery_keyboard()
        )


def box_size_inline_menu(update, context):
    query = update.callback_query
    query.answer()
    if query.data in ['S', 'M', 'L', 'XL']:
        Box.size = query.data
        text = f'Вы выбрали бокс *{query.data}-размера*\n' \
               'Пожалуйста выберите срок хранения.\n' \
               'Мы рады предложить Вам следующие варианты:'
        query.edit_message_text(
            text=text,
            reply_markup=m.storage_periods_keyboard(),
            parse_mode='markdown'
        )
    elif query.data == 'dont_want_measure':
        Box.size = 'Будет уточнен'
        text = 'Хорошо, мы замерим сами когда вы приедете на склад или замерит наш курьер'
        query.edit_message_text(
            text=text,
            reply_markup=m.storage_periods_keyboard()
        )


def month_spelling(num_month):
    if num_month == 1:
        return 'месяц'
    elif num_month in [2, 3, 4]:
        return 'месяца'
    else:
        return 'месяцев'


def storage_period_inline_menu(update, context):
    query = update.callback_query
    query.answer()
    if query.data in ['1_month', '3_month', '6_month', '12_month']:
        Orders.period = int(query.data.split('_')[0])
        text = f'Отлично, вы хотите поместить коробку размером' \
               f'\n*{Box.size}* на срок *{Orders.period} {month_spelling(Orders.period)}*.\n' \
               f'Пожалуйста выберите способ доставки:\n' \
               f'Курьерская служба *(абсолютно бесплатно)*\n' \
               f'Привезете сами на наш склад по адресу: {db_handler.get_storage_addresses()}'
        query.edit_message_text(
            text=text,
            reply_markup=m.is_delivery_keyboard(),
            parse_mode='markdown'
        )
        return 1  # DELIVERY


def is_delivery_inline_menu(update, context):
    query = update.callback_query
    query.answer()
    is_delivery_value = {
        'delivery': 1,
        'self_delivery': 0
    }
    if query.data == 'delivery':
        Orders.is_delivery = is_delivery_value[query.data]
        text = 'Прекрасно, вы выбрали доставку курьерской службой:\n' \
               'Нам потребуются ваши контактные данные.\n' \
               'Но прежде чем продолжить, пожалуйста примите\n' \
               '*Согласие на обработку персональных данных*'
        query.edit_message_text(
            text=text,
            reply_markup=m.personal_data_agreement_keyboard(),
            parse_mode='markdown'
        )
        return 2
    if query.data == 'self_delivery':
        Orders.is_delivery = is_delivery_value[query.data]
        text = f'Прекрасно, вы привезете вещи сами по адресу {db_handler.get_storage_addresses()}\n' \
               'Нам потребуются ваши контактные данные.\n' \
               'Но прежде чем продолжить, пожалуйста примите\n' \
               '*Согласие на обработку персональных данных*'
        query.edit_message_text(
            text=text,
            reply_markup=m.personal_data_agreement_keyboard(),
            parse_mode='markdown'
        )
        return 2


def personal_data_menu(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'accept':
        query.edit_message_text(
            text='Отлично, ваш заказ сформирован'
        )
    if query.data == 'not_accept':
        query.edit_message_text(
            text='Нам очень жаль'
        )
    return -1
