# Diccionari per gestionar les partides del quiz
partides_quiz = {}

class Quiz:
    def __init__(self, preguntes):
        self.preguntes = preguntes
        self.index_actual = 0
        self.correctes = 0

    def obtenir_pregunta_actual(self):
        pregunta = self.preguntes[self.index_actual]["pregunta"]
        opcions = self.preguntes[self.index_actual]["opcions"]
        opcions_formatades = "\n".join([f"{etiqueta}) {text}" for etiqueta, text in opcions.items()])
        return pregunta, opcions_formatades

    def verificar_resposta(self, resposta):
        correcta = self.preguntes[self.index_actual]["resposta"]
        if resposta.lower() == correcta:
            self.correctes += 1
            resultat = True
        else:
            resultat = False

        self.index_actual += 1
        return resultat

    def queden_preguntes(self):
        return self.index_actual < len(self.preguntes)


# Funció per iniciar el quiz
def iniciar_quiz(bot, message):
    # Preguntes del quiz
    preguntes = [
       {"pregunta": "Quin és el riu més llarg del món?", "opcions": {"a": "Amazonas", "b": "Nil", "c": "Tajo"}, "resposta": "b"},
        {"pregunta": "Quina és la capital de França?", "opcions": {"a": "Roma", "b": "París", "c": "Madrid"}, "resposta": "b"},
        {"pregunta": "Qui va pintar La Gioconda?", "opcions": {"a": "Leonardo da Vinci", "b": "Picasso", "c": "Van Gogh"}, "resposta": "a"},
        {"pregunta": "Quin és el planeta més gran del sistema solar?", "opcions": {"a": "Saturn", "b": "Júpiter", "c": "Neptú"}, "resposta": "b"},
        {"pregunta": "Quina és la llengua més parlada al món?", "opcions": {"a": "Mandarí", "b": "Anglès", "c": "Espanyol"}, "resposta": "a"},
        {"pregunta": "Qui va escriure 'El Quixot'?", "opcions": {"a": "Cervantes", "b": "Shakespeare", "c": "Homer"}, "resposta": "a"},
        {"pregunta": "Quants continents hi ha?", "opcions": {"a": "5", "b": "6", "c": "7"}, "resposta": "c"},
        {"pregunta": "Quin animal és conegut com el rei de la selva?", "opcions": {"a": "Elefant", "b": "Tigre", "c": "Lleó"}, "resposta": "c"},
        {"pregunta": "Quina substància és essencial per respirar?", "opcions": {"a": "Hidrogen", "b": "Oxigen", "c": "Diòxid de carboni"}, "resposta": "b"},
        {"pregunta": "Quin és l'oceà més gran del món?", "opcions": {"a": "Atlàntic", "b": "Índic", "c": "Pacífic"}, "resposta": "c"},
        {"pregunta": "En quin any va arribar l'home a la Lluna?", "opcions": {"a": "1969", "b": "1972", "c": "1965"}, "resposta": "a"},
        {"pregunta": "Quina és la muntanya més alta del món?", "opcions": {"a": "K2", "b": "Everest", "c": "Mont Blanc"}, "resposta": "b"},
        {"pregunta": "Quina és la moneda oficial del Japó?", "opcions": {"a": "Yuan", "b": "Ien", "c": "Won"}, "resposta": "b"},
        {"pregunta": "Qui va ser el primer president dels Estats Units?", "opcions": {"a": "George Washington", "b": "Thomas Jefferson", "c": "Abraham Lincoln"}, "resposta": "a"},
        {"pregunta": "Quin és el metall més comú a la Terra?", "opcions": {"a": "Alumini", "b": "Ferro", "c": "Coure"}, "resposta": "b"},
        {"pregunta": "Quants ossos hi ha al cos humà adult?", "opcions": {"a": "206", "b": "208", "c": "210"}, "resposta": "a"},
        {"pregunta": "Quina és la ciutat més poblada del món?", "opcions": {"a": "Tòquio", "b": "Nova York", "c": "Shanghai"}, "resposta": "a"},
        {"pregunta": "Quin és l'esport més popular del món?", "opcions": {"a": "Bàsquet", "b": "Futbol", "c": "Tennis"}, "resposta": "b"},
        {"pregunta": "Quina és la fórmula química de l'aigua?", "opcions": {"a": "H2O", "b": "O2", "c": "CO2"}, "resposta": "a"},
        {"pregunta": "Qui va descobrir Amèrica?", "opcions": {"a": "Cristòfor Colom", "b": "Magallanes", "c": "Vasco da Gama"}, "resposta": "a"},
    ]

    # Crear una nova partida i guardar-la
    partides_quiz[message.chat.id] = Quiz(preguntes)

    # Mostrar la primera pregunta
    processar_pregunta(bot, message)


# Funció per processar les preguntes del quiz
def processar_pregunta(bot, message):
    if message.chat.id not in partides_quiz:
        bot.send_message(message.chat.id, "No tens cap quiz actiu. Escriu /quiz per començar.")
        return

    partida = partides_quiz[message.chat.id]
    pregunta, opcions = partida.obtenir_pregunta_actual()

    # Format de les opcions corregit
    text_pregunta = f"**{pregunta}**\nEscriu tan sols 'a', 'b' o 'c':\n{opcions}"
    bot.send_message(message.chat.id, text_pregunta, parse_mode="Markdown")



def comprovar_resposta(bot, message):
    if message.chat.id not in partides_quiz:
        bot.send_message(message.chat.id, "No tens cap quiz actiu. Escriu /quiz per començar.")
        return

    partida = partides_quiz[message.chat.id]
    resposta = message.text.strip().lower()

    if resposta not in ["a", "b", "c"]:
        bot.send_message(message.chat.id, "❌ Resposta no vàlida. Escriu només 'a', 'b' o 'c'.")
        processar_pregunta(bot, message)
        return

    # Verificació de la resposta
    correcta = partida.verificar_resposta(resposta)
    if correcta:
        bot.send_message(message.chat.id, "✅ Correcte!")
    else:
        bot.send_message(message.chat.id, "❌ Incorrecte.")

    if partida.queden_preguntes():
        processar_pregunta(bot, message)
    else:
        bot.send_message(message.chat.id, f"🎉 Has completat el quiz amb {partida.correctes} respostes correctes!")
        del partides_quiz[message.chat.id]
