import os
import re
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

user_data = {}

github_button = telebot.types.InlineKeyboardButton(
    "Github", url="https://github.com/shayan24soley85"
)
telegram_button = telebot.types.InlineKeyboardButton(
    "Telegram", url="https://t.me/shayan357v"
)
random_button = telebot.types.InlineKeyboardButton("random", callback_data="random")
random2_button = telebot.types.InlineKeyboardButton("random2", callback_data="random2")

markup = telebot.types.InlineKeyboardMarkup()
markup.add(github_button, telegram_button, random_button, random2_button, row_width=2)

key_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
key_markup.add("Information Registration", "two", "three")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "random":
        bot.send_message(call.message.chat.id, "you clicked on random button")
        bot.answer_callback_query(call.id, "you clicked on random button")
    elif call.data == "random2":
        bot.send_message(call.message.chat.id, "you clicked on random2 button")
        bot.answer_callback_query(
            call.id, "you clicked on random2 button", show_alert=True
        )


@bot.message_handler(commands=["start"])
def send_welcome(message):
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
    bot.reply_to(message, help_text, parse_mode="HTML", reply_markup=key_markup)


@bot.message_handler(func=lambda m: True)
def keyboard(message):
    chat_id = message.chat.id
    if message.text == "Information Registration":
        user_data[chat_id] = {}
        msg = bot.send_message(
            chat_id,
            "Registering your information:\nPlease enter your full name!",
        )
        bot.register_next_step_handler(msg, get_name)
    elif message.text == "two":
        bot.send_message(chat_id, "you tapped two button!")
    elif message.text == "three":
        bot.send_message(chat_id, "you tapped three button!")


def get_name(message):
    chat_id = message.chat.id
    user_data[chat_id]["name"] = message.text.strip()
    msg = bot.send_message(chat_id, "Please enter your age!")
    bot.register_next_step_handler(msg, get_age)


def get_age(message):
    chat_id = message.chat.id
    age_text = message.text.strip()

    if not re.match(r"^[1-9][0-9]?$|^1[0-1][0-9]$", age_text):
        msg = bot.send_message(
            chat_id, "Invalid age! Please enter a valid number (e.g., 25):"
        )
        bot.register_next_step_handler(msg, get_age)
        return

    user_data[chat_id]["age"] = age_text
    msg = bot.send_message(chat_id, "Please enter your phone number!")
    bot.register_next_step_handler(msg, get_phone)


def get_phone(message):
    chat_id = message.chat.id
    phone_text = message.text.strip()

    if not re.match(r"^(?:0|\+98)?9\d{9}$", phone_text):
        msg = bot.send_message(chat_id, "Invalid phone format! Please try again:")
        bot.register_next_step_handler(msg, get_phone)
        return

    user_data[chat_id]["phone"] = phone_text
    final_step(message)


def final_step(message):
    chat_id = message.chat.id
    name = user_data[chat_id].get("name")
    age = user_data[chat_id].get("age")
    phone = user_data[chat_id].get("phone")

    msg = f"✅ Registration Complete!\n\nYour name: {name}\nYour age: {age}\nYour phone number: {phone}\n"
    bot.send_message(chat_id, msg)


bot.infinity_polling()
