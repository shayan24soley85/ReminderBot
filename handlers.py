import re
import time
from config import bot, user_data
import telebot
import database
from keyboards import (
    main_inline_markup,
    about_markup,
    profile_markup,
    home_markup,
    cancel_markup,
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
        register_info_button(call.message)
        bot.answer_callback_query(call.id)

    elif call.data == "register_info":
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id
        )
        register_info_button(call.message)
        bot.answer_callback_query(call.id)

    elif call.data == "my_profile":
        show_profile(call.message, call.message.message_id)
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


def register_info_button(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_chat_action(message.chat.id, action="typing")
    msg = bot.send_message(
        chat_id,
        "Registering your information:\nPlease enter your full name!",
        reply_markup=cancel_markup,
    )
    bot.register_next_step_handler(msg, get_name)


def get_name(message):
    chat_id = message.chat.id
    user_data[chat_id]["name"] = message.text.strip()
    bot.send_chat_action(message.chat.id, action="typing")
    msg = bot.send_message(
        chat_id, "Please enter your age!", reply_markup=cancel_markup
    )
    bot.register_next_step_handler(msg, get_age)


def get_age(message):
    chat_id = message.chat.id
    age_text = message.text.strip()

    if not re.match(r"^[1-9][0-9]?$|^1[0-1][0-9]$", age_text):
        bot.send_chat_action(message.chat.id, action="typing")
        msg = bot.send_message(
            chat_id,
            "Invalid age! Please enter a valid number (e.g., 25):",
            reply_markup=cancel_markup,
        )
        bot.register_next_step_handler(msg, get_age)
        return

    user_data[chat_id]["age"] = age_text
    bot.send_chat_action(message.chat.id, action="typing")
    msg = bot.send_message(
        chat_id, "Please enter your phone number!", reply_markup=cancel_markup
    )
    bot.register_next_step_handler(msg, get_phone)


def get_phone(message):
    chat_id = message.chat.id
    phone_text = message.text.strip()

    if not re.match(r"^(?:0|\+98)9\d{9}$", phone_text):
        bot.send_chat_action(message.chat.id, action="typing")
        msg = bot.send_message(
            chat_id,
            "Invalid phone number format! Please use the 09xxxxxxxxx format (e.g., 09121111111). Try again:",
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

    msg = f"✅ Registration Complete and Saved!\n\nYour name: {name}\nYour age: {age}\nYour phone number: {phone}\n"
    bot.send_chat_action(message.chat.id, action="typing")
    bot.send_message(chat_id, msg, reply_markup=home_markup)


def show_profile(message, message_id=None):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, action="typing")

    user = database.get_user(chat_id)

    if user:
        name, age, phone = user
        text = (
            f"👤 <b>Your Profile</b>\n\n"
            f"🔹 <b>Name:</b> {name}\n"
            f"🔹 <b>Age:</b> {age}\n"
            f"🔹 <b>Phone:</b> {phone}\n\n"
            f"<i>💡 Choose an option below:</i>"
        )
    else:
        text = "❌ You haven't registered yet!\nPlease tap 'Information Registration' to set up your profile."

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
