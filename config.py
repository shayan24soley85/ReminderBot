import os
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
SHARIF_USER = os.getenv("SHARIF_USERNAME")
SHARIF_PASS = os.getenv("SHARIF_PASSWORD")
user_data = {}
