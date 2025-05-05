import telebot
import random
import database

TOKEN = "7732799135:AAHf616ZaXyMKupTIHdqAcgP3Rxvwm7Sv04"

bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Vols jugar?")
    bot.reply_to(message, "Diguem un número del 1 al 10")
    # bot.register_next_step_handler (message, adivinanca)
    bot.send_message(message.chat.id, "Mala sort! No has adivinat el nombre")  

@bot.message_handler(commands=["obtenir_usuaris"])
def obtenir_usuaris(message):
    [conn, cursor] = database.obrir_connexio()
    # Executar una consulta SQL
    cursor.execute("SELECT * FROM usuaris")

    # Obtenir els resultats
    resultats = cursor.fetchall()
    for fila in resultats:
        bot.send_message(message.chat.id, f"ID: {fila[0]}\nNOM: {fila[1]}\nLLINATGES: {fila[2]}")  
    database.tancar_connexio(conn, cursor)

@bot.message_handler(commands=["afegir_usuaris"])
def afegir_usuaris(message):
    [conn, cursor] = database.obrir_connexio()
    # Executar una consulta SQL
    cursor.execute("INSERT INTO USUARIS VALUES (4, 'Sebas', 'Vicens Oliver', 'svicensol@iessoler.com', 'home', 's1234', '625372635', 170, 90, 20)")
    conn.commit()
    
    database.tancar_connexio(conn, cursor)


bot.infinity_polling()
