from config import bot, user_data, ADMIN_ID
import database
import controllers
from keyboards import (
    main_inline_markup,
    about_markup,
    home_markup,
    reminder_markup,
    university_dashboard_markup,
    course_dashboard_markup,
    get_my_courses_markup,
)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "home":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="سلام! به ربات یادآور خوش آمدید!\nیک گزینه از منوی زیر انتخاب کنید:",
            reply_markup=main_inline_markup,
        )
        bot.answer_callback_query(call.id)

    elif call.data == "about_us":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="👨‍💻 <b>درباره ما</b>\n\nبه ربات یادآور خوش آمدید.\nشما می‌توانید کارهای ما را دنبال کرده و از طریق لینک‌های زیر با ما در ارتباط باشید:",
            parse_mode="HTML",
            reply_markup=about_markup,
        )
        bot.answer_callback_query(call.id)

    elif call.data == "help_menu":
        help_text = (
            "🤖 <b>راهنمای ربات یادآور شما:</b>\n\n"
            "🔹 /start - شروع کار با ربات\n"
            "🔹 /help - نمایش این پیام راهنما\n"
            "🔹 /add - افزودن یادآور جدید (به زودی...)\n\n"
            "با استفاده از دکمه‌های منو جابجا شوید!"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=help_text,
            parse_mode="HTML",
            reply_markup=home_markup,
        )
        bot.answer_callback_query(call.id)

    elif call.data == "clear_info":
        controllers.clear_user_info(call)

    elif call.data == "edit_info":
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
        controllers.register_info_button(call.message)
        bot.answer_callback_query(call.id)

    elif call.data == "register_info":
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
        controllers.register_info_button(call.message)
        bot.answer_callback_query(call.id)

    elif call.data == "my_profile":
        controllers.show_profile(call.message, call.message.message_id)
        bot.answer_callback_query(call.id)

    elif call.data == "cancel_reg":
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="❌ ثبت نام لغو شد.",
            reply_markup=home_markup,
        )
        bot.answer_callback_query(call.id)

    elif call.data == "Reminder_menu":
        text = (
            "🔔 <b>منوی یادآورها</b>\n\n"
            "در اینجا می‌توانید تمام کارها و رویدادهای خود را مدیریت کنید.\n"
            "<i>لطفاً یک دسته‌بندی از زیر انتخاب کنید:</i>"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=reminder_markup,
        )
        bot.answer_callback_query(call.id)

    elif call.data == "cat_uni":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🎓 <b>داشبورد دانشگاه</b>\n\nلطفاً یک بخش را برای مدیریت انتخاب کنید:",
            parse_mode="HTML",
            reply_markup=university_dashboard_markup,
        )
        bot.answer_callback_query(call.id)

    elif call.data == "uni_courses":
        controllers.refresh_my_courses(call)
        bot.answer_callback_query(call.id)

    elif call.data.startswith("select_course_"):
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📚 <b>داشبورد درس</b>\n\nلطفاً یک بخش را برای مدیریت انتخاب کنید:",
            parse_mode="HTML",
            reply_markup=course_dashboard_markup,
        )
        bot.answer_callback_query(call.id)

    elif call.data == "add_course":
        controllers.show_departments(call)
        bot.answer_callback_query(call.id)

    elif call.data.startswith("select_dep_"):
        controllers.show_department_courses(call)
        bot.answer_callback_query(call.id)

    elif call.data == "ignore":
        bot.answer_callback_query(call.id)

    elif call.data.startswith("save_course_"):
        controllers.save_user_course(call)

    elif call.data == "uni_exams":
        controllers.show_user_exams(call)
        bot.answer_callback_query(call.id)

    elif call.data.startswith("delete_course_"):
        controllers.remove_user_course(call)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, action="typing")
    bot.send_message(
        message.chat.id,
        "سلام! به ربات یادآور خوش آمدید!\nیک گزینه از منوی زیر انتخاب کنید:",
        reply_markup=main_inline_markup,
    )


@bot.message_handler(commands=["help"])
def send_help(message):
    help_text = (
        "🤖 <b>راهنمای ربات یادآور شما:</b>\n\n"
        "🔹 /start - شروع کار با ربات\n"
        "🔹 /help - نمایش این پیام راهنما\n"
        "🔹 /add - افزودن یادآور جدید (به زودی...)\n\n"
        "یک گزینه از منوی زیر انتخاب کنید:"
    )
    bot.send_chat_action(message.chat.id, action="typing")
    bot.reply_to(message, help_text, parse_mode="HTML", reply_markup=main_inline_markup)


@bot.message_handler(commands=["add_exam"])
def add_exam_command(message):
    controllers.process_add_exam_command(message, ADMIN_ID)


@bot.message_handler(commands=["remove_exam"])
def remove_exam_command(message):
    controllers.process_remove_exam_command(message, ADMIN_ID)
