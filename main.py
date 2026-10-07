from config import bot
import controllers
import handlers
import database

if __name__ == "__main__":
    print("Initializing Database...")
    database.init_db()

    print("successfully connected to telegram!")
    controllers.start_scheduler()
    bot.infinity_polling()
