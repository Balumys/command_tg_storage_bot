from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def start_keyboard():
    button_list = [
        [KeyboardButton("🎿 Оформить заказ"),
         KeyboardButton("📕 Правила хранения")],
        [KeyboardButton("📦 Мои заказы")]
    ]
    reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    return reply_markup


def back_to_main_menu():
    button_list = [[KeyboardButton("⬅️ Назад в главное меню")]]
    return ReplyKeyboardMarkup(button_list)


def take_items():
    button_list = [[InlineKeyboardButton("Забрать вещи с хранения", callback_data='take_items')]]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def take_items_choice():
    button_list = [
        [InlineKeyboardButton("Забрать все вещи", callback_data='take_items_all'),
         InlineKeyboardButton("Забрать часть вещей", callback_data='take_items_partial')]
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def take_items_back_delivery():
    button_list = [
        [InlineKeyboardButton("Доставка (платная)", callback_data='take_items_back_delivery'),
         InlineKeyboardButton("Самовывоз", callback_data='take_items_back_myself')]
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    return reply_markup


def storage(addresses):
    num_addresses = len(addresses)
    num_rows = (num_addresses // 2) + (num_addresses % 2)

    button_list = []
    for row in range(num_rows):
        if row == num_rows - 1 and num_addresses % 2 != 0:
            button_list.append([KeyboardButton(f"🏪 {addresses[-1]}")])
        else:
            button_list.append([
                KeyboardButton(f"🏪 {addresses[row * 2]}"),
                KeyboardButton(f"🏪 {addresses[row * 2 + 1]}")
            ])
    button_list.append([KeyboardButton("🔙 Назад")])
    reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    return reply_markup
