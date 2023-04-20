import db_handler
from telegram.ext import CommandHandler, MessageHandler, Filters
from markups import start_keyboard, take_items_choice_keyboard, \
    take_items_back_delivery_keyboard, box_size_keyboard
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
        # INLINE MENU
        update.message.reply_text(
            'Тут будет меню выбора бокса', parse_mode='Markdown',
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


def take_item_back_inline_menu(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'take_items':
        query.edit_message_reply_markup(reply_markup=take_items_choice_keyboard())
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
    if query.data == 'S-size':
        pass
    if query.data == 'M-size':
        pass
    if query.data == 'L-size':
        pass
    if query.data == '>L-size':
        pass


start_handler = CommandHandler('start', start)
button_handler = MessageHandler(Filters.text, button)
