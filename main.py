from config import bot
import handlers

if __name__ == "__main__":
    print("successfully connected to telegram!")
    bot.infinity_polling()
