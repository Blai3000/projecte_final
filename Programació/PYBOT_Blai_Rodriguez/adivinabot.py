import random

class AdivinaNumero:
    """
    Classe per gestionar el joc 'Adivina el número'.
    """
    def __init__(self):
        self.numero = random.randint(1, 100)
        self.intents = 0

    def endevinar(self, intent):
        """
        Comprova si l'intent és correcte, massa alt o massa baix.
        """
        self.intents += 1
        if intent == self.numero:
            return "correcte"
        elif intent < self.numero:
            return "baix"
        else:
            return "alt"