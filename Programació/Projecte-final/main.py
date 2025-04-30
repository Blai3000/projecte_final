import telebot
import mysql.connector
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import time

TOKEN = "8102878335:AAFR95xufQKYnzLxK-ZdLpQjQQHSTY24d1c"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# Estat global per controlar si el bot està actiu
bot_actiu = True

def verificar_actiu(func):
    def wrapper(*args, **kwargs):
        global bot_actiu
        if not bot_actiu:
            bot = args[0]  # El primer argument sempre serà el bot
            message = args[1]  # El segon argument sempre serà el message
            bot.send_message(message.chat.id, "El bot està desactivat. Escriu /start per reiniciar-lo.")
            return
        return func(*args, **kwargs)
    return wrapper

# Comanda /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global bot_actiu
    bot_actiu = True  # Activa el bot
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("/help"))
    bot.send_message(message.chat.id, "Benvingut al bot de tasques. Pots escriure /help per veure les comandes disponibles.", reply_markup=markup)
    
# Comanda /help
@bot.message_handler(commands=['help'])
@verificar_actiu
def send_help(message):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("/jocs"), KeyboardButton("/informacio"), KeyboardButton("/stop"))
    bot.send_message(message.chat.id, "No saps què puc fer? Mira les meves comandes: \n\n /xxx1 \n info de xxx1 \n\n /xxx2 \n info de xxx2 \n\n /stop \n Aturar en qualsevol moment el bot", reply_markup=markup)

# Desactiva el bot
@bot.message_handler(commands=['stop'])
def stop_bot(message):
    global bot_actiu
    bot_actiu = False
    bot.send_message(message.chat.id, "El bot s'ha aturat. Escriu /start per reiniciar-lo.")


bot.infinity_polling()
