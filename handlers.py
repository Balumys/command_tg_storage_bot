from telegram.ext import CommandHandler, MessageHandler, Filters
from markups import start_keyboard, storage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, Customer, Orders, Storage, Box


engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()


def start(update, context):
    hello_message_to_new_user = """
Вас приветствует *Garbage Collector* — Склад индивидуального хранения!
Вас интересует аренда бокса?
С радостью проконсультируем по нашим услугам.
А пока посмотрите примеры и тд...
    """
    first_name = update.message.from_user.first_name
    photo_path = 'media/storage.jpg'
    with open(photo_path, 'rb') as file:
        update.message.reply_photo(photo=file,
                                   caption=f"Приветствуем Вас *{first_name}*, {hello_message_to_new_user}",
                                   reply_markup=start_keyboard(),
                                   parse_mode='markdown')


def button(update, context):
    text = update.message.text
    if text == "🎿 Оформить заказ":
        addresses = [row[0] for row in session.query(Storage.address).all()]
        address_text = "\n".join(addresses)
        update.message.reply_text(
            f'''
        Наши склады находяться по адресам:\n{address_text}
        \nВыберете подходящий Вам склад.
        \nТак же у нас есть бесплатная доставка до склада.
            ''',
            reply_markup=storage(addresses))
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

session = Session()
