class EnRaya:
    def __init__(self, mida):
        """
        Inicialitza el joc d'En Ratxa amb una mida especificada del tauler.
        :param mida: La mida del tauler (3 per Tres en Ratxa, 4 per Quatre en Ratxa, etc.)
        """
        self.mida = mida
        self.tauler = [["⬜" for _ in range(mida)] for _ in range(mida)]  # Crea el tauler
        self.jugadors = []
        self.torn = 0  # Indica el torn actual (index de la llista de jugadors)

    def afegir_jugadors(self, nom_j1, nom_j2):
        """
        Assigna els jugadors i els símbols respectius.
        :param nom_j1: Nom del jugador 1
        :param nom_j2: Nom del jugador 2
        """
        self.jugadors = [{"nom": nom_j1, "simbol": "❌"}, {"nom": nom_j2, "simbol": "🔴"}]

    def mostrar_tauler(self):
        """
        Retorna el tauler en format text per mostrar-lo al jugador.
        """
        return "\n".join(" ".join(fila) for fila in self.tauler)

    def jugada_valida(self, fila, columna):
        """
        Comprova si una jugada és vàlida (dins del tauler i en una casella buida).
        :param fila: Índex de la fila
        :param columna: Índex de la columna
        """
        return (
            0 <= fila < self.mida and
            0 <= columna < self.mida and
            self.tauler[fila][columna] == "⬜"
        )

    def fer_jugada(self, fila, columna):
        """
        Processa una jugada. Comprova si és vàlida i actualitza el tauler.
        Retorna un missatge d'estat del joc.
        :param fila: Índex de la fila
        :param columna: Índex de la columna
        """
        if not self.jugada_valida(fila, columna):
            return "Jugada no vàlida. Torna a intentar-ho."

        jugador_actual = self.jugadors[self.torn]
        self.tauler[fila][columna] = jugador_actual["simbol"]

        if self.comprova_guanyador():
            return f"🎉 {jugador_actual['nom']} ha guanyat!"
        
        if self.tauler_ple():
            return "🤝 Empat! El tauler està ple."

        # Canvia de torn
        self.torn = 1 - self.torn
        return f"✅ {self.jugadors[self.torn]['nom']}, és el teu torn!"

    def comprova_guanyador(self):
        """
        Comprova si hi ha un guanyador al tauler.
        Retorna True si hi ha un guanyador; False en cas contrari.
        """
        # Comprovar files
        for fila in self.tauler:
            if self.verifica_victoria(fila):
                return True

        # Comprovar columnes
        for col in range(self.mida):
            columna = [self.tauler[fila][col] for fila in range(self.mida)]
            if self.verifica_victoria(columna):
                return True

        # Comprovar diagonals
        diagonal1 = [self.tauler[i][i] for i in range(self.mida)]
        diagonal2 = [self.tauler[i][self.mida - 1 - i] for i in range(self.mida)]
        if self.verifica_victoria(diagonal1) or self.verifica_victoria(diagonal2):
            return True

        return False

    def verifica_victoria(self, linia):
        """
        Comprova si una línia té tots els símbols iguals (no buits).
        :param linia: Línia a verificar (pot ser una fila, columna o diagonal)
        """
        return len(set(linia)) == 1 and linia[0] != "⬜"

    def tauler_ple(self):
        """
        Comprova si el tauler està ple.
        """
        for fila in self.tauler:
            if "⬜" in fila:
                return False
        return True