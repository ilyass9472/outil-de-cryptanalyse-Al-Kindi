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
            or c == " "
            or (not c.isalnum() and not c.isspace())
        ]

        if len(caracteres) == 0:
            print("Aucun caractère valide.")
            return

        compteur = Counter(caracteres)

        # =============================
        # DEBUG
        # =============================

        print("\n========== DEBUG ==========")
        print("Premier 100 caractères du texte :")
        print(repr(texte[:100]))

        print("\nOccurrences :")
        print("$ :", compteur.get("$", 0))
        print("@ :", compteur.get("@", 0))
        print("espace :", compteur.get(" ", 0))

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

            # Ne jamais remplacer l'espace
            if symbole_chiffre[i][0] == " " or symbole[i][0] == " ":
                continue

            correspondance[symbole_chiffre[i][0]] = symbole[i][0]        

        # Forcer le remplacement de $ par espace
        # correspondance["$"] = " "

        # =============================
        # DEBUG Correspondance
        # =============================

        print("\n========== CORRESPONDANCE ==========")

        print("$ existe ?", "$" in correspondance)
        print("$ ->", repr(correspondance.get("$")))
        print("@ ->", repr(correspondance.get("@")))

        print("\nTous les symboles :")
        for k, v in correspondance.items():
            if not k.isalnum():
                print(repr(k), "->", repr(v))

        # =============================
        # Déchiffrement
        # =============================

        texte_dechiffre = ""
        print(repr(texte[:80]))

        for i, c in enumerate(texte):

            # if not c.isalnum():
            #     print(
            #         f"Index={i} | Caractère={repr(c)} | ASCII={ord(c)}"
            #     )

            # if c == "$":
            #     print(">>> Dollar détecté <<<")
            #     texte_dechiffre += " "
            if c in correspondance:
                texte_dechiffre += correspondance[c]
            else:
                texte_dechiffre += c
        # =============================
        # DEBUG Résultat
        # =============================

        print("\n========== RESULTAT ==========")
        print(repr(texte_dechiffre[:200]))

        cursor.close()
        self.conn.close()

        return texte_dechiffre