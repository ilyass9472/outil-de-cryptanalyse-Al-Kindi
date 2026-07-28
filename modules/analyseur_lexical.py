from collections import Counter
from data.config import get_connection


class AnalyseurLexical:

    def __init__(self):
        try:
            self.conn = get_connection()
        except Exception as e:
            print("Erreur lors de la connexion :", e)
            self.conn = None

    def compare_frequence(self, texte):

        if self.conn is None:
            print("Connexion non établie.")
            return

        cursor = self.conn.cursor()

        caracteres = [
            c for c in texte
            if c.islower()
            or c.isupper()
            or c.isdigit()
            or (not c.isalnum() and not c.isspace())
        ]

        if len(caracteres) == 0:
            print("Aucun caractère valide.")
            return

        compteur = Counter(caracteres)

        # =============================
        # Récupération des fréquences
        # =============================

        cursor.execute("""
            SELECT chiffre, frequence
            FROM nombres_chiffre
            ORDER BY frequence DESC
        """)
        nombres_chiffre = cursor.fetchall()

        cursor.execute("""
            SELECT chiffre, frequence
            FROM nombres
            ORDER BY frequence DESC
        """)
        nombres = cursor.fetchall()

        cursor.execute("""
            SELECT lettre, frequence
            FROM lettres_lower_chiffre
            ORDER BY frequence DESC
        """)
        lower_chiffre = cursor.fetchall()

        cursor.execute("""
            SELECT lettre, frequence
            FROM lettres_lower
            ORDER BY frequence DESC
        """)
        lower = cursor.fetchall()

        cursor.execute("""
            SELECT lettre, frequence
            FROM lettres_upper_chiffre
            ORDER BY frequence DESC
        """)
        upper_chiffre = cursor.fetchall()

        cursor.execute("""
            SELECT lettre, frequence
            FROM lettres_upper
            ORDER BY frequence DESC
        """)
        upper = cursor.fetchall()

        cursor.execute("""
            SELECT symbole, frequence
            FROM symbole_chiffre
            ORDER BY frequence DESC
        """)
        symbole_chiffre = cursor.fetchall()

        cursor.execute("""
            SELECT symbole, frequence
            FROM symboles
            ORDER BY frequence DESC
        """)
        symbole = cursor.fetchall()

        # =============================
        # Construction des correspondances
        # =============================

        correspondance = {}

        for i in range(min(len(lower), len(lower_chiffre))):
            correspondance[lower_chiffre[i][0]] = lower[i][0]

        for i in range(min(len(upper), len(upper_chiffre))):
            correspondance[upper_chiffre[i][0]] = upper[i][0]

        for i in range(min(len(nombres), len(nombres_chiffre))):
            correspondance[nombres_chiffre[i][0]] = nombres[i][0]

        for i in range(min(len(symbole), len(symbole_chiffre))):
            correspondance[symbole_chiffre[i][0]] = symbole[i][0]

        # =============================
        # Déchiffrement
        # =============================

        texte_dechiffre = ""

        for c in texte:
            if c in correspondance:
                texte_dechiffre += correspondance[c]
            else:
                texte_dechiffre += c

        cursor.close()
        self.conn.close()

        return texte_dechiffre