from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from decouple import config
from PIL import Image
import pytesseract
import sqlite3
import re

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello World!')

def handle_image(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')

    text = pytesseract.image_to_string(Image.open('user_photo.jpg'))
    
    # Extract the amount
    match = re.search(r'Valor enviado\s*\n\s*\$\s*([\d\.]+),00', text)
    if match:
        amount = match.group(1)
        amount = float(amount.replace('.', ''))  # Remove '.' and convert to float
    else:
        amount = 0.0  # If no amount found, default to 0.0
        
    
    save_user(user.username, text, amount)
    update.message.reply_text(f'Mi vale estas bien pobre, como asi que una transferencia de ${amount} pesos? Eso es lo que me gasto yo en un fincho con las babys')



def handle_text(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Invalid message. Please send an image.')

def main() -> None:
    updater = Updater(token=config('TELEGRAM_TOKEN'))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_text))

    updater.start_polling()

    updater.idle()

def save_user(phone_number: str, text: str, amount: float):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''INSERT INTO transferencia(username, description, amount)
                  VALUES (?, ?, ?)''', (phone_number, text, amount))

    conn.commit()
    conn.close()

def create_table():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS transferencia
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT(40),
                  amount REAL,
                  description TEXT)''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
    main()
