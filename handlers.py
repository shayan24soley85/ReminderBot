from config import bot, user_data
import database
import controllers
from keyboards import (
    main_inline_markup,
    about_markup,
    home_markup,
    reminder_markup,
    university_dashboard_markup,
    course_dashboard_markup,
)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "home":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Hi Welcome to Reminder Bot!\nChoose an option from the menu below:",
            reply_markup=main_inline_markup,
        )
        bot.answer_callback_query(call.id)

    elif call.data == "about_us":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="👨‍💻 <b>About Us</b>\n\nWelcome to Reminder Bot.\nYou can follow our work and contact us through the links below:",
            parse_mode="HTML",
            reply_markup=about_markup,
        )
        bot.answer_callback_query(call.id)

    elif call.data == "help_menu":
        help_text = (
            "🤖 <b>Your Reminder Bot Guide:</b>\n\n"
            "🔹 /start - Start the bot\n"
            "🔹 /help - Show this help message\n"
            "🔹 /add - Add a new reminder (Coming soon...)\n\n"
            "Navigate using the menu buttons!"
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
        database.delete_user(call.message.chat.id)

        if call.message.chat.id in user_data:
            del user_data[call.message.chat.id]

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🗑 Your profile information has been completely deleted!",
            reply_markup=home_markup,
        )
        bot.answer_callback_query(call.id, "Information cleared!", show_alert=True)

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
            text="❌ Registration canceled.",
            reply_markup=home_markup,
        )
        bot.answer_callback_query(call.id)

    elif call.data == "Reminder_menu":
        text = (
            "🔔 <b>Reminders Menu</b>\n\n"
            "Here you can manage all your tasks and events.\n"
            "<i>Please select a category below:</i>"
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
            text="🎓 <b>University Dashboard</b>\n\nPlease select a section to manage:",
            parse_mode="HTML",
            reply_markup=university_dashboard_markup,
        )
        bot.answer_callback_query(call.id)
    elif call.data == "uni_courses":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📚 <b>Course Dashboard</b>\n\nPlease select a section to manage:",
            parse_mode="HTML",
            reply_markup=course_dashboard_markup,
        )
        bot.answer_callback_query(call.id)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, action="typing")
    bot.send_message(
        message.chat.id,
        "Hi Welcome to Reminder Bot!\nChoose an option from the menu below:",
        reply_markup=main_inline_markup,
    )


@bot.message_handler(commands=["help"])
def send_help(message):
    help_text = (
        "🤖 <b>Your Reminder Bot Guide:</b>\n\n"
        "🔹 /start - Start the bot\n"
        "🔹 /help - Show this help message\n"
        "🔹 /add - Add a new reminder (Coming soon...)\n\n"
        "Choose an option from the menu below:"
    )
    bot.send_chat_action(message.chat.id, action="typing")
    bot.reply_to(message, help_text, parse_mode="HTML", reply_markup=main_inline_markup)
