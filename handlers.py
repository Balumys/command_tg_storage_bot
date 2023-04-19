import db_handler
from telegram.ext import CommandHandler, MessageHandler, Filters
from markups import start_keyboard, storage

from db import Base, Customer, Orders, Storage, Box


def start(update, context):
    hello_message_to_new_user = (
        "\n"
        "Вас приветствует *Garbage Collector* — Склад индивидуального хранения!\n"
        "Вас интересует аренда бокса?\n"
        "С радостью проконсультируем по нашим услугам.\n"
        "А пока посмотрите примеры и тд...\n"
    )
    first_name = update.message.from_user.first_name
    photo_path = 'media/storage.jpg'
    with open(photo_path, 'rb') as file:
        update.message.reply_photo(
            photo=file,
            caption=f"Приветствуем Вас *{first_name}*, {hello_message_to_new_user}",
            reply_markup=start_keyboard(),
            parse_mode='markdown'
        )

    db_handler.add_customer(first_name, update.message.from_user.last_name)  # JUST FOR TEST


def button(update, context):
    text = update.message.text
    if text == "🎿 Оформить заказ":
        addresses = db_handler.get_storage_addresses()  # JUST FOR TEST
        address_text = "\n".join(addresses)
        update.message.reply_text(
            f'        Наши склады находяться по адресам:\n{address_text}\n'
            f'        \nВыберете подходящий Вам склад.\n'
            f'        \nТак же у нас есть бесплатная доставка до склада.\n',
            reply_markup=storage(addresses)
        )
    elif text == "📕 Правила хранения":
        with open('media/Rules.txt', 'rb') as file:
            update.message.reply_document(file)
    elif text == "💰 Цены":
        with open('media/tariff.pdf', 'rb') as file:
            update.message.reply_document(file)
    elif text == "🔙 Назад":
        start(update, context)


start_handler = CommandHandler('start', start)
button_handler = MessageHandler(Filters.text, button)
