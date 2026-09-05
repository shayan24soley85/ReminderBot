import re
import time
from config import bot, user_data
import telebot
import database
from keyboards import markup, key_markup, github_button, telegram_button, random2_button


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "random":
        edited_random_btn = telebot.types.InlineKeyboardButton(
            "edited_random", callback_data="random"
        )
        new_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        new_markup.add(
            github_button, telegram_button, edited_random_btn, random2_button
        )

        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=new_markup,
        )

        bot.answer_callback_query(call.id, "Button name changed!")

    elif call.data == "random2":
        bot.send_chat_action(call.message.chat.id, action="typing")
        bot.send_message(call.message.chat.id, "you clicked on random2 button")
        bot.answer_callback_query(
            call.id, "you clicked on random2 button", show_alert=True
        )


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, action="typing")
    bot.send_message(
        message.chat.id, "Hi Welcome to Reminder Bot!", reply_markup=markup
    )


@bot.message_handler(commands=["help"])
def send_help(message):
    help_text = (
        "🤖 <b>Your Reminder Bot Guide:</b>\n\n"
        "🔹 /start - Start the bot\n"
        "🔹 /help - Show this help message\n"
        "🔹 /add - Add a new reminder (Coming soon...)\n\n"
        "Choose a command to get started!"
    )
    bot.send_chat_action(message.chat.id, action="typing")
    bot.reply_to(message, help_text, parse_mode="HTML", reply_markup=key_markup)


@bot.message_handler(func=lambda m: m.text == "✍️ Information Registration")
def register_info_button(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_chat_action(message.chat.id, action="typing")
    msg = bot.send_message(
        chat_id,
        "Registering your information:\nPlease enter your full name!",
    )
    bot.register_next_step_handler(msg, get_name)


def get_name(message):
    chat_id = message.chat.id
    user_data[chat_id]["name"] = message.text.strip()
    bot.send_chat_action(message.chat.id, action="typing")
    msg = bot.send_message(chat_id, "Please enter your age!")
    bot.register_next_step_handler(msg, get_age)


def get_age(message):
    chat_id = message.chat.id
    age_text = message.text.strip()

    if not re.match(r"^[1-9][0-9]?$|^1[0-1][0-9]$", age_text):
        bot.send_chat_action(message.chat.id, action="typing")
        msg = bot.send_message(
            chat_id, "Invalid age! Please enter a valid number (e.g., 25):"
        )
        bot.register_next_step_handler(msg, get_age)
        return

    user_data[chat_id]["age"] = age_text
    bot.send_chat_action(message.chat.id, action="typing")
    msg = bot.send_message(chat_id, "Please enter your phone number!")
    bot.register_next_step_handler(msg, get_phone)


def get_phone(message):
    chat_id = message.chat.id
    phone_text = message.text.strip()

    if not re.match(r"^(?:0|\+98)9\d{9}$", phone_text):
        bot.send_chat_action(message.chat.id, action="typing")
        msg = bot.send_message(
            chat_id,
            "Invalid phone number format! Please use the 09xxxxxxxxx format (e.g., 09121111111). Try again:",
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
    bot.send_message(chat_id, msg)


@bot.message_handler(func=lambda m: m.text == "two")
def button_two(message):
    bot.send_chat_action(message.chat.id, action="typing")
    m = bot.send_message(message.chat.id, "you tapped two button!")
    time.sleep(2)
    bot.delete_messages(message.chat.id, [message.message_id, m.message_id])


@bot.message_handler(func=lambda m: m.text == "three")
def button_three(message):
    bot.send_chat_action(message.chat.id, action="typing")
    m = bot.send_message(
        message.chat.id,
        "you tapped three button!this message will be edited after 3 seconds!",
    )
    time.sleep(3)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=m.message_id,
        text="message have been edited!",
    )


@bot.message_handler(func=lambda m: m.text == "👤 My Profile")
def show_profile(message):
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
            f"<i>💡 To edit your info, simply tap 'Information Registration' again.</i>"
        )
    else:

        text = "❌ You haven't registered yet!\nPlease tap 'Information Registration' to set up your profile."

    bot.send_message(chat_id, text, parse_mode="HTML")


@bot.message_handler(func=lambda m: m.text == "🔚 Back")
def close_keyboard(message):
    bot.send_chat_action(message.chat.id, action="typing")

    remove_markup = telebot.types.ReplyKeyboardRemove()

    bot.send_message(
        message.chat.id,
        "Menu closed! Type /help to open it again.",
        reply_markup=remove_markup,
    )
