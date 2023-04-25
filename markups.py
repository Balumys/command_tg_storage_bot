import re
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def start_keyboard():
    button_list = [
        [KeyboardButton("🎿 Оформить заказ"),
         KeyboardButton("📕 Правила хранения")],
        [KeyboardButton("📦 Мои заказы")]
    ]
    reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    return reply_markup


""" Раздел Мои заказы """


def customer_orders_keyboard(orders):
    button_list = []
    for order in orders:
        order_id = re.search(r'\d+', order).group()
        button_list.append(
            [
                InlineKeyboardButton(
                    f'{order}',
                    callback_data=f'take_order_{order_id}',
                )
            ]
        )
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def take_items_choice_keyboard():
    button_list = [
        [InlineKeyboardButton("Забрать всё", callback_data='take_items_all'),
         InlineKeyboardButton("Забрать часть", callback_data='take_items_partial')]
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def take_items_back_delivery_keyboard():
    button_list = [
        [InlineKeyboardButton("🚚 Доставка", callback_data='take_items_back_delivery'),
         InlineKeyboardButton("👨🏻 Самовывоз", callback_data='take_items_back_myself')]
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def new_phonenumber_keyboard():
    button_list = [
        [
            InlineKeyboardButton("Ввести новый 📞", callback_data='update_customer_phone'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


""" Раздел Оформить Заказ"""


def box_size_keyboard():
    button_list = [
        [
            InlineKeyboardButton("📦 S (1кв.м)", callback_data='S'),
            InlineKeyboardButton("📦 M (3кв.м)", callback_data='M')
        ],
        [
            InlineKeyboardButton("📦 L (5кв.м)", callback_data='L'),
            InlineKeyboardButton("📦 >L (>5кв.м)", callback_data='XL')
        ],
        [
            InlineKeyboardButton("❌ Я не хочу замерять сам", callback_data='dont_want_measure'),
            InlineKeyboardButton("❌ Отмена", callback_data='cancel'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def storage_periods_keyboard():
    button_list = [
        [
            InlineKeyboardButton("1 месяц", callback_data='1_month'),
            InlineKeyboardButton("3 месяца", callback_data='3_month'),
        ],
        [
            InlineKeyboardButton("6 месяцев", callback_data='6_month'),
            InlineKeyboardButton("12 месяцев", callback_data='12_month')
        ],
        [
            InlineKeyboardButton("❌ Отмена", callback_data='cancel'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def is_delivery_keyboard():
    button_list = [
        [
            InlineKeyboardButton("🚚 С доставкой", callback_data='delivery'),
            InlineKeyboardButton("👨🏻 Привезу сам", callback_data='self_delivery')
        ],
        [
            InlineKeyboardButton("❌ Отмена", callback_data='cancel'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def personal_data_agreement_keyboard():
    button_list = [
        [InlineKeyboardButton("✅ Согласен", callback_data='accept'),
         InlineKeyboardButton("❌ Нет", callback_data='cancel')],
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def cancel_keyboard():
    button_list = [
        [
            InlineKeyboardButton("❌ Отмена", callback_data='cancel'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def phone_keyboard():
    button_list = [
        # [
        #     InlineKeyboardButton("✅ Да", callback_data='approve phone'),
        # ],
        [
            InlineKeyboardButton("❌ Отмена", callback_data='cancel'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def email_keyboard():
    button_list = [
        [
            InlineKeyboardButton("✅ Да", callback_data='approve email'),
        ],
        [
            InlineKeyboardButton("❌ Отмена", callback_data='cancel'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def verify_order_keyboard():
    button_list = [
        [
            InlineKeyboardButton("✅ Да", callback_data='approve order'),
        ],
        [
            InlineKeyboardButton("❌ Нет", callback_data='cancel'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


### CLIENT BOT ###


def client_start_keyboard():
    button_list = [
        [
            KeyboardButton("🎿 Статистика"),
            KeyboardButton("🚚 Заказы с доставкой"),
        ],
        [
            KeyboardButton("📦 Просроченные Заказы"),
        ]
    ]
    reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    return reply_markup


def customer_orders_keyboard_(orders):
    button_list = []
    for order in orders:
        button_list.append(
            [
                InlineKeyboardButton(
                    f'Заказ №{order.id}',
                    callback_data=f'take_order_{order.id}',
                )
            ]
        )
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup
