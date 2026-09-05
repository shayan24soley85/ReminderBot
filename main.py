from config import bot
import handlers
import database

if __name__ == "__main__":
    print("Initializing Database...")
    database.init_db()

    print("successfully connected to telegram!")
    bot.infinity_polling()
