import re
from config import bot, user_data
import database
from keyboards import home_markup, profile_markup, cancel_markup


def convert_persian_numbers(text):
    mapping = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    return text.translate(mapping)


def register_info_button(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_chat_action(message.chat.id, action="typing")
    msg = bot.send_message(
        chat_id,
        "در حال ثبت اطلاعات شما:\nلطفاً نام کامل خود را وارد کنید!",
        reply_markup=cancel_markup,
    )
    bot.register_next_step_handler(msg, get_name)


def get_name(message):
    chat_id = message.chat.id
    user_data[chat_id]["name"] = message.text.strip()
    bot.send_chat_action(message.chat.id, action="typing")
    msg = bot.send_message(
        chat_id, "لطفاً سن خود را وارد کنید!", reply_markup=cancel_markup
    )
    bot.register_next_step_handler(msg, get_age)


def get_age(message):
    chat_id = message.chat.id
    age_text = convert_persian_numbers(message.text.strip())

    if not re.match(r"^[1-9][0-9]?$|^1[0-1][0-9]$", age_text):
        bot.send_chat_action(message.chat.id, action="typing")
        msg = bot.send_message(
            chat_id,
            "سن نامعتبر است! لطفاً یک عدد صحیح وارد کنید (مثلاً ۲۵):",
            reply_markup=cancel_markup,
        )
        bot.register_next_step_handler(msg, get_age)
        return

    user_data[chat_id]["age"] = age_text
    bot.send_chat_action(message.chat.id, action="typing")
    msg = bot.send_message(
        chat_id, "لطفاً شماره موبایل خود را وارد کنید!", reply_markup=cancel_markup
    )
    bot.register_next_step_handler(msg, get_phone)


def get_phone(message):
    chat_id = message.chat.id
    phone_text = convert_persian_numbers(message.text.strip())

    if not re.match(r"^(?:0|\+98)9\d{9}$", phone_text):
        bot.send_chat_action(message.chat.id, action="typing")
        msg = bot.send_message(
            chat_id,
            "فرمت شماره موبایل نامعتبر است! لطفاً از فرمت 09xxxxxxxxx استفاده کنید (مثلاً 09121111111). دوباره تلاش کنید:",
            reply_markup=cancel_markup,
        )
        bot.register_next_step_handler(msg, get_phone)
        return

    user_data[chat_id]["phone"] = phone_text
    final_step(message)


def final_step(message):
    chat_id = message.chat.id
    name = user_data[chat_id].get("name")
    age = user_data[chat_id].get("age")
    phone = user_data[chat_id].get("phone")

    database.save_user(chat_id, name, age, phone)

    msg = f"✅ ثبت نام با موفقیت انجام و ذخیره شد!\n\nنام شما: {name}\nسن شما: {age}\nشماره موبایل شما: {phone}\n"
    bot.send_chat_action(message.chat.id, action="typing")
    bot.send_message(chat_id, msg, reply_markup=home_markup)


def show_profile(message, message_id=None):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, action="typing")

    user = database.get_user(chat_id)

    if user:
        name, age, phone = user
        text = (
            f"👤 <b>پروفایل شما</b>\n\n"
            f"🔹 <b>نام:</b> {name}\n"
            f"🔹 <b>سن:</b> {age}\n"
            f"🔹 <b>موبایل:</b> {phone}\n\n"
            f"<i>💡 یک گزینه از منوی زیر انتخاب کنید:</i>"
        )
    else:
        text = "❌ شما هنوز ثبت نام نکرده‌اید!\nلطفاً برای ایجاد پروفایل روی 'ثبت اطلاعات' کلیک کنید."

    if message_id:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=profile_markup,
        )
    else:
        bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=profile_markup)


def show_departments(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    departments = database.get_departments()

    if not departments:
        bot.answer_callback_query(call.id, "هیچ دانشکده‌ای یافت نشد!", show_alert=True)
        return

    from keyboards import get_departments_markup

    markup = get_departments_markup(departments)

    text = "🏢 <b>انتخاب دانشکده:</b>\n\nلطفاً دانشکده خود را از لیست زیر انتخاب کنید:"

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        parse_mode="HTML",
        reply_markup=markup,
    )


def show_department_courses(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    parts = call.data.split("_")
    dep_id = int(parts[2])

    page = 1
    if len(parts) > 3:
        page = int(parts[3])

    courses = database.get_courses_by_department(dep_id)

    if not courses:
        bot.answer_callback_query(
            call.id, "هیچ درسی برای این دانشکده یافت نشد!", show_alert=True
        )
        return

    from keyboards import get_department_courses_markup

    markup = get_department_courses_markup(courses, dep_id, page)

    text = f"📚 <b>لیست دروس (صفحه {page}):</b>\n\nلطفاً درس مورد نظر خود را برای افزودن به لیست دروس خود انتخاب کنید:"

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        parse_mode="HTML",
        reply_markup=markup,
    )
