import sys
import os
from collections import Counter

# ============================================================
# AJOUT DU DOSSIER RACINE DU PROJET AU PYTHON PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ============================================================
# IMPORT DATABASE
# ============================================================

from data.config import get_connection
# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "data/chifre.txt"
OUTPUT_FILE = "data/dechifre.txt"

# بالنسبة للحروف: نعم
MAP_LETTERS = True

# الأرقام والرموز:
# نخليوهم False افتراضياً لأن المرحلة الأساسية هي الحروف.
MAP_NUMBERS = False
MAP_SYMBOLS = False


# ============================================================
# ANALYSEUR DE FREQUENCE
# ============================================================

class FrequencyAnalysis:

    def __init__(self, texte):
        self.texte = texte

        self.conn = None

        self.cipher_lower_freq = Counter()
        self.cipher_upper_freq = Counter()
        self.cipher_numbers_freq = Counter()
        self.cipher_symbols_freq = Counter()

        self.mapping = {}

    # ========================================================
    # CONNEXION DB
    # ========================================================

    def connect(self):

        try:
            self.conn = get_connection()

            if self.conn is None:
                raise RuntimeError(
                    "La connexion PostgreSQL est None."
                )

        except Exception as e:
            raise RuntimeError(
                f"Erreur de connexion PostgreSQL : {e}"
            )

    # ========================================================
    # CALCUL DES FREQUENCES DU TEXTE CHIFFRE
    # ========================================================

    def calculer_frequences(self):

        print("\n" + "=" * 60)
        print("1. ANALYSE FREQUENTIELLE")
        print("=" * 60)

        print(f"Taille du texte : {len(self.texte):,} caractères")

        # ----------------------------------------------------
        # Reset des anciennes fréquences
        # ----------------------------------------------------

        cursor = self.conn.cursor()

        cursor.execute(
            "UPDATE lettres_lower_chiffre SET frequence = 0"
        )

        cursor.execute(
            "UPDATE lettres_upper_chiffre SET frequence = 0"
        )

        cursor.execute(
            "UPDATE nombres_chiffre SET frequence = 0"
        )

        cursor.execute(
            "UPDATE symbole_chiffre SET frequence = 0"
        )

        # ----------------------------------------------------
        # Séparation des catégories
        # ----------------------------------------------------

        for caractere in self.texte:

            if caractere.islower():

                self.cipher_lower_freq[caractere] += 1

            elif caractere.isupper():

                self.cipher_upper_freq[caractere] += 1

            elif caractere.isdigit():

                self.cipher_numbers_freq[caractere] += 1

            elif (
                not caractere.isalnum()
                and not caractere.isspace()
            ):

                self.cipher_symbols_freq[caractere] += 1

        # ----------------------------------------------------
        # Totaux
        # ----------------------------------------------------

        total_lower = sum(
            self.cipher_lower_freq.values()
        )

        total_upper = sum(
            self.cipher_upper_freq.values()
        )

        total_numbers = sum(
            self.cipher_numbers_freq.values()
        )

        total_symbols = sum(
            self.cipher_symbols_freq.values()
        )

        print(f"\nLettres minuscules : {total_lower:,}")
        print(f"Lettres majuscules : {total_upper:,}")
        print(f"Chiffres            : {total_numbers:,}")
        print(f"Symboles            : {total_symbols:,}")

        # ----------------------------------------------------
        # Mise à jour DB
        # ----------------------------------------------------

        if total_lower > 0:

            for lettre, count in self.cipher_lower_freq.items():

                frequence = count / total_lower

                cursor.execute(
                    """
                    UPDATE lettres_lower_chiffre
                    SET frequence = %s
                    WHERE lettre = %s
                    """,
                    (
                        frequence,
                        lettre
                    )
                )

        if total_upper > 0:

            for lettre, count in self.cipher_upper_freq.items():

                frequence = count / total_upper

                cursor.execute(
                    """
                    UPDATE lettres_upper_chiffre
                    SET frequence = %s
                    WHERE lettre = %s
                    """,
                    (
                        frequence,
                        lettre
                    )
                )

        if total_numbers > 0:

            for chiffre, count in self.cipher_numbers_freq.items():

                frequence = count / total_numbers

                cursor.execute(
                    """
                    UPDATE nombres_chiffre
                    SET frequence = %s
                    WHERE chiffre = %s
                    """,
                    (
                        frequence,
                        chiffre
                    )
                )

        if total_symbols > 0:

            for symbole, count in self.cipher_symbols_freq.items():

                frequence = count / total_symbols

                cursor.execute(
                    """
                    UPDATE symbole_chiffre
                    SET frequence = %s
                    WHERE symbole = %s
                    """,
                    (
                        frequence,
                        symbole
                    )
                )

        # ----------------------------------------------------
        # IMPORTANT:
        # UN SEUL COMMIT
        # ----------------------------------------------------

        self.conn.commit()

        cursor.close()

        print("\n✓ Fréquences du texte chiffré calculées.")


    # ========================================================
    # CHARGER LES FREQUENCES DE LA LANGUE
    # ========================================================

    def charger_frequences_langue(self):

        cursor = self.conn.cursor()

        # ----------------------------------------------------
        # Lettres minuscules
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT lettre, frequence
            FROM lettres_lower
            ORDER BY frequence DESC
            """
        )

        lower = cursor.fetchall()

        # ----------------------------------------------------
        # Lettres majuscules
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT lettre, frequence
            FROM lettres_upper
            ORDER BY frequence DESC
            """
        )

        upper = cursor.fetchall()

        # ----------------------------------------------------
        # Chiffres
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT chiffre, frequence
            FROM nombres
            ORDER BY frequence DESC
            """
        )

        numbers = cursor.fetchall()

        # ----------------------------------------------------
        # Symboles
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT symbole, frequence
            FROM symboles
            ORDER BY frequence DESC
            """
        )

        symbols = cursor.fetchall()

        cursor.close()

        return lower, upper, numbers, symbols


    # ========================================================
    # CONSTRUIRE LE MAPPING PAR RANG DE FREQUENCE
    # ========================================================

    def construire_mapping(self):

        print("\n" + "=" * 60)
        print("2. CONSTRUCTION DU MAPPING FREQUENTIEL")
        print("=" * 60)

        (
            language_lower,
            language_upper,
            language_numbers,
            language_symbols
        ) = self.charger_frequences_langue()

        # ----------------------------------------------------
        # LOWERCASE
        # ----------------------------------------------------

        if MAP_LETTERS:

            cipher_lower = sorted(
                self.cipher_lower_freq.items(),
                key=lambda x: x[1],
                reverse=True
            )

            language_lower = sorted(
                language_lower,
                key=lambda x: x[1],
                reverse=True
            )

            # ------------------------------------------------
            # Mapping bijectif
            # ------------------------------------------------

            used_plain = set()

            for cipher_char, _ in cipher_lower:

                for plain_char, _ in language_lower:

                    if plain_char not in used_plain:

                        self.mapping[cipher_char] = plain_char

                        used_plain.add(plain_char)

                        break

        # ----------------------------------------------------
        # UPPERCASE
        # ----------------------------------------------------

        if MAP_LETTERS:

            cipher_upper = sorted(
                self.cipher_upper_freq.items(),
                key=lambda x: x[1],
                reverse=True
            )

            language_upper = sorted(
                language_upper,
                key=lambda x: x[1],
                reverse=True
            )

            used_plain_upper = set()

            for cipher_char, _ in cipher_upper:

                for plain_char, _ in language_upper:

                    if plain_char not in used_plain_upper:

                        self.mapping[cipher_char] = plain_char

                        used_plain_upper.add(plain_char)

                        break

        # ----------------------------------------------------
        # NUMBERS
        # ----------------------------------------------------

        if MAP_NUMBERS:

            cipher_numbers = sorted(
                self.cipher_numbers_freq.items(),
                key=lambda x: x[1],
                reverse=True
            )

            language_numbers = sorted(
                language_numbers,
                key=lambda x: x[1],
                reverse=True
            )

            used_numbers = set()

            for cipher_char, _ in cipher_numbers:

                for plain_char, _ in language_numbers:

                    if plain_char not in used_numbers:

                        self.mapping[cipher_char] = plain_char

                        used_numbers.add(plain_char)

                        break

        # ----------------------------------------------------
        # SYMBOLS
        # ----------------------------------------------------

        if MAP_SYMBOLS:

            cipher_symbols = sorted(
                self.cipher_symbols_freq.items(),
                key=lambda x: x[1],
                reverse=True
            )

            language_symbols = sorted(
                language_symbols,
                key=lambda x: x[1],
                reverse=True
            )

            used_symbols = set()

            for cipher_char, _ in cipher_symbols:

                # On ne remplace jamais l'espace ici
                if cipher_char == " ":
                    continue

                for plain_char, _ in language_symbols:

                    if plain_char == " ":
                        continue

                    if plain_char not in used_symbols:

                        self.mapping[cipher_char] = plain_char

                        used_symbols.add(plain_char)

                        break

        # ----------------------------------------------------
        # AFFICHAGE
        # ----------------------------------------------------

        print("\nMapping trouvé :")

        for cipher_char, plain_char in sorted(
            self.mapping.items()
        ):

            print(
                f"  {repr(cipher_char)} -> {repr(plain_char)}"
            )

        print(
            f"\nNombre de correspondances : "
            f"{len(self.mapping)}"
        )


    # ========================================================
    # APPLIQUER LE MAPPING
    # ========================================================

    def dechiffrer(self):

        print("\n" + "=" * 60)
        print("3. APPLICATION DU MAPPING")
        print("=" * 60)

        resultat = []

        for caractere in self.texte:

            if caractere in self.mapping:

                resultat.append(
                    self.mapping[caractere]
                )

            else:

                # espace, ponctuation inconnue,
                # caractères non mappés...
                resultat.append(caractere)

        texte_dechiffre = "".join(resultat)

        print(
            f"✓ Texte généré : "
            f"{len(texte_dechiffre):,} caractères"
        )

        return texte_dechiffre


    # ========================================================
    # SAUVEGARDE
    # ========================================================

    def sauvegarder(self, texte):

        os.makedirs(
            os.path.dirname(OUTPUT_FILE),
            exist_ok=True
        )

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as fichier:

            fichier.write(texte)

        print(
            f"\n✓ Résultat sauvegardé dans : "
            f"{OUTPUT_FILE}"
        )


    # ========================================================
    # EXECUTION COMPLETE
    # ========================================================

    def executer(self):

        self.connect()

        try:

            # 1. fréquence du texte chiffré
            self.calculer_frequences()

            # 2. mapping fréquence
            self.construire_mapping()

            # 3. déchiffrement
            texte_dechiffre = self.dechiffrer()

            # 4. sauvegarde
            self.sauvegarder(
                texte_dechiffre
            )

        finally:

            if self.conn is not None:

                self.conn.close()


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 60)
    print("FREQUENCY ANALYSIS - AL KINDI")
    print("=" * 60)

    # --------------------------------------------------------
    # Vérification fichier
    # --------------------------------------------------------

    if not os.path.exists(INPUT_FILE):

        print(
            f"\nERREUR : fichier introuvable : "
            f"{INPUT_FILE}"
        )

        return

    # --------------------------------------------------------
    # Lecture texte chiffré
    # --------------------------------------------------------

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as fichier:

        texte = fichier.read()

    if not texte:

        print("\nERREUR : le fichier est vide.")

        return

    print(
        f"\nFichier source : {INPUT_FILE}"
    )

    print(
        f"Taille         : {len(texte):,} caractères"
    )

    # --------------------------------------------------------
    # Analyse
    # --------------------------------------------------------

    analyseur = FrequencyAnalysis(
        texte
    )

    analyseur.executer()

    print("\n" + "=" * 60)
    print("FREQUENCY ANALYSIS TERMINEE")
    print("=" * 60)

    print(
        f"\nFichier suivant : {OUTPUT_FILE}"
    )

    print(
        "\n→ La phase suivante sera dictionnaire.py"
    )


if __name__ == "__main__":

    main()