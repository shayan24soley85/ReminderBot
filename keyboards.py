import telebot

main_inline_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
reg_btn = telebot.types.InlineKeyboardButton(
    "✍️ Information Registration", callback_data="register_info"
)
prof_btn = telebot.types.InlineKeyboardButton(
    "👤 My Profile", callback_data="my_profile"
)
about_btn = telebot.types.InlineKeyboardButton("ℹ️ About Us", callback_data="about_us")
help_btn = telebot.types.InlineKeyboardButton("❓ Help", callback_data="help_menu")

main_inline_markup.add(reg_btn)
main_inline_markup.add(prof_btn)
main_inline_markup.add(about_btn, help_btn)

home_btn = telebot.types.InlineKeyboardButton("🏠 Home", callback_data="home")

home_markup = telebot.types.InlineKeyboardMarkup()
home_markup.add(home_btn)

about_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
github_button = telebot.types.InlineKeyboardButton(
    "Github", url="https://github.com/shayan24soley85"
)
telegram_button = telebot.types.InlineKeyboardButton(
    "Telegram", url="https://t.me/shayan357v"
)
about_markup.add(github_button, telegram_button)
about_markup.add(home_btn)

profile_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
edit_btn = telebot.types.InlineKeyboardButton("✏️ Edit Info", callback_data="edit_info")
clear_btn = telebot.types.InlineKeyboardButton(
    "🚮 Clear Info", callback_data="clear_info"
)
profile_markup.add(edit_btn, clear_btn)
profile_markup.add(home_btn)

cancel_markup = telebot.types.InlineKeyboardMarkup()
cancel_btn = telebot.types.InlineKeyboardButton("❌ Cancel", callback_data="cancel_reg")
cancel_markup.add(cancel_btn)
