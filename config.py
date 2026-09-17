import os
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
bot = telebot.TeleBot(TOKEN)
user_data = {}
