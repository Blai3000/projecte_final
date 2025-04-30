import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import time
from enrayabot import EnRaya  # Importa el joc En Raya
import adivinabot  # Importa el mòdul adivinabot per a la funció de "Adivina el número"
import quiz

TOKEN = "7746852534:AAHs8KyWnCy2eDR-kbCtNiC4Om5dlrK1et8"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# Estat global per controlar si el bot està actiu
bot_actiu = True

# Decorador per verificar si el bot està actiu
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

# Diccionaris per gestionar les partides actives
jocs_adivina = {}
partides_en_raya = {}

# Funció modular per la transició
def transicio(bot, message, missatge_final):
    bot.send_chat_action(message.chat.id, action="typing")
    sent_message = bot.send_message(message.chat.id, "Inicialitzant...")
    passos = ["Inicialitzant_", "__nicalitzan_", "___icialitza_",
              "____cialitz_", "_____alit_", "______li_", "_______",
              "_____", "____", "_____"]
    for pas in passos:
        time.sleep(0.2)
        bot.edit_message_text(pas, chat_id=sent_message.chat.id, message_id=sent_message.message_id)
        bot.send_chat_action(message.chat.id, action="typing")
    time.sleep(0.5)
    bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    bot.send_message(message.chat.id, missatge_final, parse_mode="Markdown")

# Comanda /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global bot_actiu
    bot_actiu = True  # Activa el bot
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("/help"))
    bot.send_message(message.chat.id, "Benvingut! Sóc el teu bot de jocs. Pots escriure /help per veure les comandes disponibles.", reply_markup=markup)

# Comanda /help
@bot.message_handler(commands=['help'])
@verificar_actiu
def send_help(message):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("/jocs"), KeyboardButton("/informacio"), KeyboardButton("/stop"))
    bot.send_message(message.chat.id, "No saps què puc fer? Mira les meves comandes: \n\n /jocs \n Jugar als jocs implementats \n\n /informacio \n Llegir la informació del bot i del seu creador \n\n /stop \n Aturar en qualsevol moment el bot", reply_markup=markup)

@bot.message_handler(commands=['informacio'])
@verificar_actiu
def presentacio(message):
    bot.send_message(message.chat.id, "Bones, soc en Blai Rodríguez Moratal, he creat aquest bot a la classe de programació de 2n de Batxillerat (2024-2025) i el meu bot és un que et permet jugar a tres jocs distints, cinc si tens en compte els *en_ratlla* com tres diferents. Pots jugar a /adivina_el_numero, a /en_ratlla amb un amic o fer un /quiz de cultura general. Està aqui per que passis una bona estona.")

# Comanda /jocs
@bot.message_handler(commands=['jocs'])
@verificar_actiu
def opcions(message):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("/adivina_el_numero"), 
               KeyboardButton("/en_ratlla"),
               KeyboardButton("/quiz"))
    bot.send_message(message.chat.id, "Aquí pots jugar a tot això: \n\n /adivina_el_numero \n Un fàcil joc per provar si penses en el mateix número que jo \n\n /en_ratlla \n Pots triar entre 3, 4 o 5 _en_ratlla per jugar \n\n /quiz \n 20 preguntes per comprovar els teus coneixements de cultura general", reply_markup=markup)

# Comanda /adivina_el_numero
@bot.message_handler(commands=['adivina_el_numero'])
@verificar_actiu
def iniciar_adivina(message):
    transicio(bot, message, "Nam a jugar a *Adivina el número*!!")
    jocs_adivina[message.chat.id] = adivinabot.AdivinaNumero()  # Crear una nova partida
    bot.send_message(message.chat.id, "He pensat un número entre 1 i 100. Pots endevinar quin és?")
    bot.register_next_step_handler(message, comprovar_adivina)

# Funció per comprovar els intents de l'usuari en "Adivina el número"
def comprovar_adivina(message):
    if message.chat.id not in jocs_adivina:
        bot.send_message(message.chat.id, "No tens cap partida activa. Usa /adivina_el_numero per començar.")
        return

    joc = jocs_adivina[message.chat.id]

    try:
        intent = int(message.text)
        if not 1 <= intent <= 100:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Introdueix un número entre 1 i 100.")
        bot.register_next_step_handler(message, comprovar_adivina)
        return

    resultat = joc.endevinar(intent)
    if resultat == "correcte":
        bot.send_message(message.chat.id, f"🎉 Felicitats! Has encertat el número {joc.numero} en {joc.intents} intents!")
        del jocs_adivina[message.chat.id]  # Finalitzar la partida
    elif resultat == "baix":
        bot.send_message(message.chat.id, "🔽 Massa baix. Torna a intentar-ho!")
        bot.register_next_step_handler(message, comprovar_adivina)
    elif resultat == "alt":
        bot.send_message(message.chat.id, "🔼 Massa alt. Torna a intentar-ho!")
        bot.register_next_step_handler(message, comprovar_adivina)

# Comanda /en_ratlla
@bot.message_handler(commands=['en_ratlla'])
@verificar_actiu
def iniciar_enraya(message):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(KeyboardButton("3_en_ratlla"), KeyboardButton("4_en_ratlla"), KeyboardButton("5_en_ratlla"))
    bot.send_message(message.chat.id, "Escriu el tipus de joc En Ratxa: \n 3_en_ratlla \n 4_en_ratlla \n 5_en_ratlla", reply_markup=markup)
    bot.register_next_step_handler(message, iniciar_partida_enraya)

# Funció per començar la partida En Raya
@verificar_actiu
def iniciar_partida_enraya(message):
    mida = None
    if message.text == "3_en_ratlla":
        mida = 3
    elif message.text == "4_en_ratlla":
        mida = 4
    elif message.text == "5_en_ratlla":
        mida = 5
    else:
        bot.send_message(message.chat.id, "Opció no vàlida, prova de nou.")
        return

    transicio(bot, message, f"Nam a jugar a *{mida} _en_ratlla*!!")
    partides_en_raya[message.chat.id] = EnRaya(mida)  # Inicialitza el joc
    joc = partides_en_raya[message.chat.id]

    # Afegeix els jugadors
    joc.afegir_jugadors("Jugador 1 (❌)", "Jugador 2 (🔴)")

    bot.send_message(message.chat.id, "Aquí tens el tauler inicial:\n" + joc.mostrar_tauler())
    bot.send_message(message.chat.id, f"És el torn de {joc.jugadors[0]['nom']}. Escriu la fila i la columna (exemple: 1 2).")
    bot.register_next_step_handler(message, jugar_enraya)

# Funció per jugar al joc EnRaya
@verificar_actiu
def jugar_enraya(message):
    if message.chat.id not in partides_en_raya:
        bot.send_message(message.chat.id, "No tens cap partida activa. Usa /en_ratlla per començar.")
        return

    joc = partides_en_raya[message.chat.id]
    try:
        fila, columna = map(int, message.text.split())
        fila -= 1
        columna -= 1
    except ValueError:
        bot.send_message(message.chat.id, "Format incorrecte! Escriu fila i columna separades per un espai (exemple: 1 2).")
        bot.register_next_step_handler(message, jugar_enraya)
        return

    missatge = joc.fer_jugada(fila, columna)
    if missatge:
        bot.send_message(message.chat.id, missatge)
    if joc.comprova_guanyador() or joc.tauler_ple():
        del partides_en_raya[message.chat.id]
        return

    bot.send_message(message.chat.id, "Tauler actual:\n" + joc.mostrar_tauler())
    bot.send_message(message.chat.id, f"És el torn de {joc.jugadors[joc.torn]['nom']}. Escriu la fila i la columna (exemple: 1 2).")
    bot.register_next_step_handler(message, jugar_enraya)


@bot.message_handler(commands=['quiz'])
@verificar_actiu
def iniciar_quiz_comanda(message):
    quiz.iniciar_quiz(bot, message)

# Funció per comprovar la resposta del quiz
@bot.message_handler(func=lambda message: message.chat.id in quiz.partides_quiz)
@verificar_actiu
def comprovar_quiz(message):
    # Passa tant el bot com el missatge al mòdul quiz.py per comprovar la resposta
    quiz.comprovar_resposta(bot, message)



@bot.message_handler(commands=['stop'])
def stop_bot(message):
    global bot_actiu
    bot_actiu = False  # Desactiva el bot
    bot.send_message(message.chat.id, "El bot s'ha aturat. Escriu /start per reiniciar-lo.")


bot.infinity_polling()
