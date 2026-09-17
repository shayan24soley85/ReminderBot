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


def save_user_course(call):
    chat_id = call.message.chat.id
    course_id = int(call.data.split("_")[2])

    success = database.add_course_to_user(chat_id, course_id)

    if success:
        bot.answer_callback_query(
            call.id, "✅ درس با موفقیت به لیست شما اضافه شد!", show_alert=True
        )
    else:
        bot.answer_callback_query(
            call.id, "⚠️ این درس از قبل در لیست شما وجود دارد!", show_alert=True
        )


def show_user_exams(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    exams = database.get_user_exams_objects(chat_id)

    if not exams:
        text = "📝 <b>امتحانات من</b>\n\nشما در حال حاضر هیچ امتحان ثبت‌شده‌ای ندارید."
    else:
        text = "📝 <b>برنامه امتحانات من:</b>\n\n"
        for exam in exams:
            course_name = exam.course.name
            e_type = exam.exam_type.value
            date = exam.date_time
            status = exam.exam_status.value

            text += f"▪️ <b>{course_name}</b> (نوع: {e_type})\n"
            text += f"   📅 تاریخ: {date}\n"
            text += f"   وضعیت: {status}\n\n"

    import telebot

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔙 بازگشت", callback_data="cat_uni"))

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        parse_mode="HTML",
        reply_markup=markup,
    )


def remove_user_course(call):
    chat_id = call.message.chat.id
    course_id = int(call.data.split("_")[2])

    database.remove_course_from_user(chat_id, course_id)
    bot.answer_callback_query(
        call.id, "🗑 درس و امتحانات مرتبط با آن با موفقیت حذف شدند!", show_alert=True
    )

    refresh_my_courses(call)


def refresh_my_courses(call):
    chat_id = call.message.chat.id
    courses_list = database.get_user_courses(chat_id)

    text = "📚 <b>دروس من</b>\n\n"
    if courses_list:
        text += (
            "در اینجا لیست دروس ثبت‌نامی شما قرار دارد (برای مدیریت روی درس کلیک کنید):"
        )
    else:
        text += "شما هنوز هیچ درسی ثبت نکرده‌اید! برای شروع روی دکمه «افزودن درس» کلیک کنید."

    from keyboards import get_my_courses_markup

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text=text,
        parse_mode="HTML",
        reply_markup=get_my_courses_markup(courses_list),
    )


def process_add_exam_command(message, admin_id):
    if message.chat.id != admin_id:
        bot.reply_to(
            message, "⛔️ شما ادمین نیستید و دسترسی لازم برای این دستور را ندارید!"
        )
        return

    parts = message.text.split()

    if len(parts) < 5:
        help_text = (
            "⚠️ <b>فرمت دستور اشتباه است!</b>\n\n"
            "استفاده صحیح:\n"
            "<code>/addexam [کد_درس] [گروه] [نوع] [تاریخ]</code>\n\n"
            "انواع مجاز: Midterm, Final, Quiz\n"
            "مثال:\n"
            "<code>/addexam 40419 1 Midterm 1403/08/25</code>"
        )
        bot.reply_to(message, help_text, parse_mode="HTML")
        return

    try:
        course_code = parts[1]
        group_number = parts[2]
        exam_type = parts[3]
        date_time = " ".join(parts[4:])

        from Enums import ExamType

        valid_types = [e.value for e in ExamType]
        if exam_type not in valid_types:
            bot.reply_to(
                message,
                f"❌ نوع امتحان باید یکی از این موارد باشد: {', '.join(valid_types)}",
            )
            return

        course_id = database.get_course_id(course_code, group_number)

        if not course_id:
            bot.reply_to(
                message, f"❌ درسی با کد {course_code} و گروه {group_number} یافت نشد!"
            )
            return

        database.add_exam_to_course(course_id, exam_type, date_time)

        bot.reply_to(
            message,
            f"✅ امتحان {exam_type} برای درس {course_code} (گروه {group_number}) با موفقیت در تاریخ {date_time} ثبت شد.",
        )

    except Exception as e:
        bot.reply_to(message, f"❌ خطای سیستمی: {e}")


def clear_user_info(call):
    chat_id = call.message.chat.id
    database.delete_user(chat_id)

    if chat_id in user_data:
        del user_data[chat_id]

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text="🗑 اطلاعات پروفایل شما به طور کامل حذف شد!",
        reply_markup=home_markup,
    )
    bot.answer_callback_query(call.id, "اطلاعات پاک شد!", show_alert=True)
