import telebot
import math

main_inline_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
reg_btn = telebot.types.InlineKeyboardButton(
    "✍️ ثبت اطلاعات", callback_data="register_info"
)
prof_btn = telebot.types.InlineKeyboardButton(
    "👤 پروفایل من", callback_data="my_profile"
)
about_btn = telebot.types.InlineKeyboardButton("ℹ️ درباره ما", callback_data="about_us")
help_btn = telebot.types.InlineKeyboardButton("❓ راهنما", callback_data="help_menu")
Reminder_btn = telebot.types.InlineKeyboardButton(
    "🔔 منوی یادآورها", callback_data="Reminder_menu"
)
main_inline_markup.add(Reminder_btn)
main_inline_markup.add(reg_btn)
main_inline_markup.add(prof_btn)
main_inline_markup.add(about_btn, help_btn)

home_btn = telebot.types.InlineKeyboardButton("🏠 خانه", callback_data="home")

home_markup = telebot.types.InlineKeyboardMarkup()
home_markup.add(home_btn)

about_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
github_button = telebot.types.InlineKeyboardButton(
    "🐙 گیت‌هاب", url="https://github.com/shayan24soley85"
)
telegram_button = telebot.types.InlineKeyboardButton(
    "✈️ تلگرام", url="https://t.me/shayan357v"
)
about_markup.add(github_button, telegram_button)
about_markup.add(home_btn)

profile_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
edit_btn = telebot.types.InlineKeyboardButton(
    "✏️ ویرایش اطلاعات", callback_data="edit_info"
)
clear_btn = telebot.types.InlineKeyboardButton(
    "🚮 پاک کردن اطلاعات", callback_data="clear_info"
)
profile_markup.add(edit_btn, clear_btn)
profile_markup.add(home_btn)

cancel_markup = telebot.types.InlineKeyboardMarkup()
cancel_btn = telebot.types.InlineKeyboardButton("❌ لغو", callback_data="cancel_reg")
cancel_markup.add(cancel_btn)

reminder_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
daily_btn = telebot.types.InlineKeyboardButton(
    "📝 کارهای روزانه", callback_data="cat_daily"
)
uni_btn = telebot.types.InlineKeyboardButton("🎓 دانشگاه", callback_data="cat_uni")
bday_btn = telebot.types.InlineKeyboardButton("🎂 تولدها", callback_data="cat_bday")
work_btn = telebot.types.InlineKeyboardButton("💼 کار", callback_data="cat_work")
health_btn = telebot.types.InlineKeyboardButton("💊 سلامتی", callback_data="cat_health")

reminder_markup.add(daily_btn, uni_btn)
reminder_markup.add(bday_btn, work_btn)
reminder_markup.add(health_btn)
reminder_markup.add(home_btn)

university_dashboard_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
uni_courses_btn = telebot.types.InlineKeyboardButton(
    "📚 دروس من", callback_data="uni_courses"
)
uni_exams_btn = telebot.types.InlineKeyboardButton(
    "📝 امتحانات", callback_data="uni_exams"
)
uni_homeworks_btn = telebot.types.InlineKeyboardButton(
    "🎒 تکالیف", callback_data="uni_homeworks"
)
uni_back_btn = telebot.types.InlineKeyboardButton(
    "🔙 بازگشت", callback_data="Reminder_menu"
)

university_dashboard_markup.add(uni_courses_btn)
university_dashboard_markup.add(uni_exams_btn, uni_homeworks_btn)
university_dashboard_markup.add(uni_back_btn, home_btn)


def get_my_courses_markup(courses=None):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)

    if courses:
        for course in courses:
            btn_course = telebot.types.InlineKeyboardButton(
                f"🏷 {course['name']}", callback_data=f"select_course_{course['id']}"
            )
            btn_delete = telebot.types.InlineKeyboardButton(
                "❌ حذف", callback_data=f"delete_course_{course['id']}"
            )
            markup.row(btn_course, btn_delete)

    add_course_btn = telebot.types.InlineKeyboardButton(
        "➕ افزودن درس", callback_data="add_course"
    )
    back_btn = telebot.types.InlineKeyboardButton("🔙 بازگشت", callback_data="cat_uni")

    markup.row(add_course_btn)
    markup.row(back_btn, home_btn)

    return markup


course_dashboard_markup = telebot.types.InlineKeyboardMarkup(row_width=2)

course_exams_btn = telebot.types.InlineKeyboardButton(
    "📝 امتحانات", callback_data="course_exams"
)
course_homeworks_btn = telebot.types.InlineKeyboardButton(
    "🎒 تکالیف", callback_data="course_homeworks"
)

course_back_btn = telebot.types.InlineKeyboardButton(
    "🔙 بازگشت", callback_data="uni_courses"
)

course_dashboard_markup.add(course_exams_btn, course_homeworks_btn)
course_dashboard_markup.add(course_back_btn, home_btn)


def get_departments_markup(departments):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    if departments:
        for dep in departments:
            btn = telebot.types.InlineKeyboardButton(
                f"🏢 {dep[1]}", callback_data=f"select_dep_{dep[0]}"
            )
            markup.add(btn)

    back_btn = telebot.types.InlineKeyboardButton(
        "🔙 بازگشت", callback_data="uni_courses"
    )
    markup.add(back_btn, home_btn)

    return markup


def get_department_courses_markup(courses, dep_id, page=1):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    ITEMS_PER_PAGE = 30
    total_pages = math.ceil(len(courses) / ITEMS_PER_PAGE)

    if total_pages == 0:
        total_pages = 1

    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE

    current_courses = courses[start_idx:end_idx]

    if current_courses:
        for course in current_courses:
            course_id, c_code, group, c_name, prof, exam, units = course
            btn_text = f"➕ {c_name} - {c_code} (گروه {group})"
            btn_callback = f"save_course_{course_id}"

            btn = telebot.types.InlineKeyboardButton(
                text=btn_text, callback_data=btn_callback
            )
            markup.add(btn)

    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            telebot.types.InlineKeyboardButton(
                "⬅️ قبلی", callback_data=f"select_dep_{dep_id}_{page-1}"
            )
        )

    nav_buttons.append(
        telebot.types.InlineKeyboardButton(
            f"📄 صفحه {page} از {total_pages}", callback_data="ignore"
        )
    )

    if page < total_pages:
        nav_buttons.append(
            telebot.types.InlineKeyboardButton(
                "بعدی ➡️", callback_data=f"select_dep_{dep_id}_{page+1}"
            )
        )

    if nav_buttons:
        markup.row(*nav_buttons)

    back_btn = telebot.types.InlineKeyboardButton(
        "🔙 بازگشت", callback_data="add_course"
    )
    markup.add(back_btn, home_btn)

    return markup
