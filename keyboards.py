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
Reminder_btn = telebot.types.InlineKeyboardButton(
    "🔔 Reminder Menu", callback_data="Reminder_menu"
)
main_inline_markup.add(Reminder_btn)
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

reminder_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
daily_btn = telebot.types.InlineKeyboardButton(
    "🏠 Daily Tasks", callback_data="cat_daily"
)
uni_btn = telebot.types.InlineKeyboardButton("🎓 University", callback_data="cat_uni")
bday_btn = telebot.types.InlineKeyboardButton("🎂 Birthdays", callback_data="cat_bday")
work_btn = telebot.types.InlineKeyboardButton("💼 Work", callback_data="cat_work")
health_btn = telebot.types.InlineKeyboardButton("💊 Health", callback_data="cat_health")

reminder_markup.add(daily_btn, uni_btn)
reminder_markup.add(bday_btn, work_btn)
reminder_markup.add(health_btn)
reminder_markup.add(home_btn)

university_dashboard_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
uni_courses_btn = telebot.types.InlineKeyboardButton(
    "📚 Courses", callback_data="uni_courses"
)
uni_exams_btn = telebot.types.InlineKeyboardButton(
    "📝 Exams", callback_data="uni_exams"
)
uni_homeworks_btn = telebot.types.InlineKeyboardButton(
    "🎒 Homeworks", callback_data="uni_homeworks"
)
uni_back_btn = telebot.types.InlineKeyboardButton(
    "🔙 Back", callback_data="Reminder_menu"
)

university_dashboard_markup.add(uni_courses_btn)
university_dashboard_markup.add(uni_exams_btn, uni_homeworks_btn)
university_dashboard_markup.add(uni_back_btn, home_btn)
