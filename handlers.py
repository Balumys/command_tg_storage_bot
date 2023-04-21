import db_handler
from telegram.ext import CommandHandler, MessageHandler, Filters
from markups import start_keyboard, take_items_choice_keyboard, \
    take_items_back_delivery_keyboard, box_size_keyboard, storage_periods_keyboard
from db import Base, Customer, Orders, Storage, Box
from environs import Env

env = Env()


def start(update, context):
    hello_message_to_new_user = env.str('HELLO_MESSAGE')
    first_name = update.message.from_user.first_name
    photo_path = 'media/storage.jpg'
    with open(photo_path, 'rb') as file:
        update.message.reply_photo(
            photo=file,
            caption=f"Приветствуем Вас *{first_name}*, {hello_message_to_new_user}",
            reply_markup=start_keyboard(),
            parse_mode='markdown'
        )


def button(update, context):
    text = update.message.text
    if text == "🎿 Оформить заказ":
        storage_address = db_handler.get_storage_addresses()
        # INLINE MENU
        update.message.reply_text(
            'Мы предоставляем стандартные размеры коробок для хранения. Если вы знаете точный размер, выберите '
            'подходящий для вас вариант. Если же вы не уверены в нужном размере, наши консультанты помогут вам '
            'выбрать подходящую коробку при вашем визите на склад. Также наш курьер может замерить необходимые '
            'параметры, чтобы помочь вам определиться с выбором.\n'
            f'Наш склад находиться по адресу: *{storage_address}*',
            parse_mode='Markdown',
            reply_markup=box_size_keyboard()
        )
    elif text == "📕 Правила хранения":
        storage_rules = env.str('STORAGE_RULES')
        update.message.reply_text(storage_rules, parse_mode='Markdown')
    elif text == "📦 Мои заказы":
        user_id = update.message.from_user.id
        customer_id = db_handler.get_customer_id(user_id)
        if customer_id:
            # INLINE MENU
            my_boxes = db_handler.get_stored_boxes(customer_id)
            update.message.reply_text(my_boxes, parse_mode='Markdown', reply_markup=take_items_choice_keyboard())
        else:
            update.message.reply_text(
                'У вас еще нет заказов',
                parse_mode='Markdown',
            )


def callback_handler(update, context):
    query = update.callback_query
    query.answer()
    if query.data in ['take_items_all', 'take_items_partial']:
        take_item_back_inline_menu(update, context)
    elif query.data in ['S', 'M', 'L', 'XL', 'dont_want_measure']:
        make_order_inline_menu(update, context)


def take_item_back_inline_menu(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'take_items_all':
        text = 'Вы собираетесь забрать все вещи:\nВыберете способ доставки'
        query.edit_message_text(
            text=text,
            reply_markup=take_items_back_delivery_keyboard()
        )
    if query.data == 'take_items_partial':
        text = 'Вы собираетесь забрать лишь часть вещей:\nВыберете способ доставки'
        query.edit_message_text(
            text=text,
            reply_markup=take_items_back_delivery_keyboard()
        )


def make_order_inline_menu(update, context):
    query = update.callback_query
    query.answer()
    if query.data in ['S', 'M', 'L', 'XL']:
        text = f'Вы выбрали {query.data}-размер'
        query.edit_message_text(
            text=text,
            reply_markup=storage_periods_keyboard()
        )
    elif query.data == 'dont_want_measure':
        text = 'Хорошо, мы замерим сами когда вы приедете на склад или замерит наш курьер'
        query.edit_message_text(
            text=text,
            reply_markup=storage_periods_keyboard()
        )


start_handler = CommandHandler('start', start)
button_handler = MessageHandler(Filters.text, button)
