from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from decouple import config
from PIL import Image
import pytesseract
import sqlite3
import re

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hola, soy el bot K-ching. Puedes enviarme una foto de tu transferencia y yo la guardaré en mi base de datos.')
    
    
def cierre(update: Update, context: CallbackContext) -> None:
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    username = update.message.from_user.username

    #Get the sum of all amounts in the current date for the user sending the message
    c.execute('''SELECT SUM(amount) FROM transferencia
                    WHERE date(created_at) = date('now')
                    AND username = ?
                ''', (username,))
    row = c.fetchone()
    if row:
        update.message.reply_text(f'Has recibido ${row[0]} pesos hoy.')
    else:
        update.message.reply_text('No has recibido dinero hoy.')

    #Now display all the transactions for the current date and the user sending the message
    c.execute('''SELECT amount, created_at FROM transferencia
                    WHERE date(created_at) = date('now')
                    AND username = ?
                ''', (username,))
    rows = c.fetchall()
    
    if rows:
        update.message.reply_text('A continuación, el detalle de tus transferencias de hoy:')
        for row in rows:
            update.message.reply_text(f'Transferencia por ${row[0]} \nFecha de registro: {row[1]}')
    
    conn.close()
    

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
    update.message.reply_text(f'Transferencia de ${amount} pesos registrada.')


def handle_text(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Invalid message. Please send an image.')
    

def main() -> None:
    updater = Updater(token=config('TELEGRAM_TOKEN'))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("cierre", cierre))
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
                username    TEXT(40),
                amount      REAL,
                description TEXT,
                created_at  datetime default CURRENT_TIMESTAMP not null)''')

    conn.commit()
    conn.close()
    

if __name__ == '__main__':
    create_table()
    main()
