import telebot

main_inline_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
reg_btn = telebot.types.InlineKeyboardButton(
    "✍️ Registration", callback_data="register_info"
)
prof_btn = telebot.types.InlineKeyboardButton(
    "👤 My Profile", callback_data="my_profile"
)
btn_two = telebot.types.InlineKeyboardButton("two", callback_data="btn_two")
btn_three = telebot.types.InlineKeyboardButton("three", callback_data="btn_three")
help_btn = telebot.types.InlineKeyboardButton("❓ Help", callback_data="help_menu")
about_btn = telebot.types.InlineKeyboardButton("ℹ️ About Us", callback_data="about_us")

main_inline_markup.add(reg_btn, prof_btn)
main_inline_markup.add(btn_two, btn_three)
main_inline_markup.add(help_btn, about_btn)

home_btn = telebot.types.InlineKeyboardButton("🏠 Home", callback_data="go_home")

about_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
github_btn = telebot.types.InlineKeyboardButton(
    "Github", url="https://github.com/shayan24soley85"
)
telegram_btn = telebot.types.InlineKeyboardButton(
    "Telegram", url="https://t.me/shayan357v"
)
about_markup.add(github_btn, telegram_btn)
about_markup.add(home_btn)

help_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
help_markup.add(home_btn)

profile_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
edit_btn = telebot.types.InlineKeyboardButton("✏️ Edit Info", callback_data="edit_info")
clear_btn = telebot.types.InlineKeyboardButton(
    "🚮 Clear Info", callback_data="clear_info"
)
profile_markup.add(edit_btn, clear_btn)
profile_markup.add(home_btn)
