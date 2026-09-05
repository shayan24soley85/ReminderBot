import telebot

github_button = telebot.types.InlineKeyboardButton(
    "Github", url="https://github.com/shayan24soley85"
)
telegram_button = telebot.types.InlineKeyboardButton(
    "Telegram", url="https://t.me/shayan357v"
)
random_button = telebot.types.InlineKeyboardButton("random", callback_data="random")
random2_button = telebot.types.InlineKeyboardButton("random2", callback_data="random2")

markup = telebot.types.InlineKeyboardMarkup()
markup.add(github_button, telegram_button, random_button, random2_button, row_width=2)

key_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
key_markup.add(
    "✍️ Information Registration", "👤 My Profile", "two", "three", "🔚 Back"
)
profile_markup = telebot.types.InlineKeyboardMarkup(row_width=2)

edit_btn = telebot.types.InlineKeyboardButton("✏️ Edit Info", callback_data="edit_info")
clear_btn = telebot.types.InlineKeyboardButton(
    "🚮 Clear Info", callback_data="clear_info"
)
back_btn = telebot.types.InlineKeyboardButton("🔙 Back", callback_data="back_profile")


profile_markup.add(edit_btn, clear_btn)
profile_markup.add(back_btn)
