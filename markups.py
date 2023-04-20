from telegram import ReplyKeyboardMarkup, KeyboardButton


def start_keyboard():
    button_list = [
        [KeyboardButton("🎿 Оформить заказ"),
         KeyboardButton("📕 Правила хранения")],
        [KeyboardButton("📦 Мои заказы")]
    ]
    reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    return reply_markup


def back_to_main_menu():
    back_button = [[KeyboardButton("⬅️ Назад в главное меню")]]
    return ReplyKeyboardMarkup(back_button)


def storage(addresses):
    num_addresses = len(addresses)
    num_rows = (num_addresses // 2) + (num_addresses % 2)

    button_list = []
    for row in range(num_rows):
        if row == num_rows - 1 and num_addresses % 2 != 0:
            button_list.append([KeyboardButton(f"🏪 {addresses[-1]}")])
        else:
            button_list.append([
                KeyboardButton(f"🏪 {addresses[row*2]}"),
                KeyboardButton(f"🏪 {addresses[row*2+1]}")
            ])
    button_list.append([KeyboardButton("🔙 Назад")])
    reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    return reply_markup
