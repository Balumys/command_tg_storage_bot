import re

from telegram import ReplyKeyboardRemove

import db_handler
import markups as m
import sqlalchemy

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
    elif text == "📕 Правила хранения":
        storage_rules = 'Спасибо, что выбрали наш сервис сезонного хранения вещей *Garbage Collector*. Наше хранилище ' \
                        'не принимает в хранение *жидкости, наркотики, биткоины, оружие и другие неприемлемые вещи*. ' \
                        'У нас есть ограничение на количество хранимых вещей. Хранение происходит на свой страх и ' \
                        'риск. *Пожалуйста, забирайте свои вещи вовремя*, чтобы избежать огромных финансовых потерь. '
        update.message.reply_text(storage_rules, parse_mode='Markdown')
    elif text == "📦 Мои заказы":
        user_id = update.message.from_user.id
        customer_id = db_handler.get_customer_id(user_id)
        if customer_id:
            # INLINE MENU
            my_boxes = db_handler.get_customer_orders(customer_id)
            update.message.reply_text(my_boxes, parse_mode='Markdown', reply_markup=m.take_items_choice_keyboard())
        else:
            update.message.reply_text(
                'Простите, но кажется у вас еще нет барохла на хранении 😞\n Пожалуйста оформите заказ.',
                parse_mode='Markdown',
            )
    elif context.user_data.get('state') == 'PHONE':
        print('TYT')


def callback_handler(update, context):
    query = update.callback_query
    query.answer()
    # TAKE ITEMS BACK
    if query.data in ['take_items_all', 'take_items_partial']:
        take_item_back_inline_menu(update, context)
    # PLACE ORDER
    if query.data in ['S', 'M', 'L', 'XL', 'dont_want_measure']:
        box_size_inline_menu(update, context)
    if query.data in ['1_month', '3_month', '6_month', '12_month']:
        storage_period_inline_menu(update, context)
    if query.data in ['delivery', 'self_delivery']:
        is_delivery_inline_menu(update, context)
    if query.data == 'accept':
        pass
    if query.data == 'not_accept':
        text = 'Нам очень жаль'
        query.edit_message_text(
            text=text
        )


def take_item_back_inline_menu(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'take_items_all':
        text = 'Вы собираетесь забрать все вещи:\nВыберете способ доставки'
        query.edit_message_text(
            text=text,
            reply_markup=m.take_items_back_delivery_keyboard()
        )
    if query.data == 'take_items_partial':
        text = 'Вы собираетесь забрать лишь часть вещей:\nВыберете способ доставки'
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
               f'Пожалуйста выберите срок хранения.\nМы рады предложить Вам следующие варианты:'
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
               f'Пожалуйста выбирете способ доставки:\n' \
               f'Курьерская служба *(абсолютно бесплатно)*\n' \
               f'Привезете сами на наш склад по адресу: {db_handler.get_storage_addresses()}'
        query.edit_message_text(
            text=text,
            reply_markup=m.is_delivery_keyboard(),
            parse_mode='markdown'
        )


def is_delivery_inline_menu(update, context):
    query = update.callback_query
    query.answer()
    is_delivery_value = {
        'delivery': 1,
        'self_delivery': 0
    }
    if query.data == 'delivery':
        Orders.is_delivery = is_delivery_value[query.data]
        text = f'Прекрасно, вы выбрали доставку курьерской службой:\n' \
               f'Нам подтребуются ваши контактные данные.\n' \
               f'Но прежде чем продолжить, пожалуйста примите\n*Согласие на обработку персональных данных*'
        query.edit_message_text(
            text=text,
            reply_markup=m.personal_data_agreement_keyboard(),
            parse_mode='markdown'
        )
    else:
        Orders.is_delivery = is_delivery_value[query.data]
        text = f'Прекрасно, вы привезете вещи сами по адресу {db_handler.get_storage_addresses()}\n' \
               f'Нам подтребуются ваши контактные данные.\n' \
               f'Но прежде чем продолжить, пожалуйста примите\n*Согласие на обработку персональных данных*'
        query.edit_message_text(
            text=text,
            reply_markup=m.personal_data_agreement_keyboard(),
            parse_mode='markdown'
        )


def personal_data_agreement_inline_menu(update, context):
    query = update.callback_query
    query.answer()
    if query.data in ['1_month', '3_month', '6_month', '12_month']:
        Orders.period = int(query.data.split('_')[0])
        text = f'Отлично, вы хотите поместить коробку размером' \
               f'\n*{Box.size}* на срок *{Orders.period} {month_spelling(Orders.period)}*.\n' \
               f'Пожалуйста выбирете способ доставки:\n' \
               f'Курьерская служба *(абсолютно бесплатно)*\n' \
               f'Привезете сами на наш склад по адресу: *{db_handler.get_storage_addresses()}*'
        query.edit_message_text(
            text=text,
            reply_markup=m.is_delivery_keyboard(),
            parse_mode='markdown'
        )


start_handler = CommandHandler('start', start)
button_handler = MessageHandler(Filters.text, button)
