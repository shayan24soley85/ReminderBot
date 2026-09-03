import os
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

print("successfully connected to telegram!")

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


key_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
key_markup.add("one", "two", "three")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "random":
        bot.send_message(call.message.chat.id, "you clicked on random button")
        # show_alert=true is another option in this part
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


@bot.message_handler()
def keyboard(message):
    if message.text == "one":
        bot.send_message(message.chat.id, "you tapped one button!")
    elif message.text == "two":
        bot.send_message(message.chat.id, "you tapped two button!")
    elif message.text == "three":
        bot.send_message(message.chat.id, "you tapped three button!")


bot.infinity_polling()
