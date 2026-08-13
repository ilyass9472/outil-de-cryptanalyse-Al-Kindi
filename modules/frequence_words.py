import sys
import os
import re
from collections import Counter

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from data.config import get_connection


# ============================================================
# CONFIGURATION
# ============================================================

CORPUS_PATH = "data/corpus.txt"
MAX_LENGTH = 30


# ============================================================
# LECTURE DU CORPUS
# ============================================================

def lire_corpus():

    if not os.path.exists(CORPUS_PATH):
        raise FileNotFoundError(
            f"Corpus introuvable : {CORPUS_PATH}"
        )

    with open(CORPUS_PATH, "r", encoding="utf-8") as fichier:
        return fichier.read()


# ============================================================
# EXTRACTION DES MOTS
# ============================================================

def extraire_mots(texte):

    mots = re.findall(r"[a-zA-Z]+", texte.lower())

    # Ignorer les mots de plus de 30 lettres
    mots = [
        mot
        for mot in mots
        if 1 <= len(mot) <= MAX_LENGTH
    ]

    return mots


# ============================================================
# CALCUL DES FREQUENCES
# ============================================================

def calculer_frequences(mots):

    compteur = Counter(mots)

    # Nombre total de mots du corpus
    total_mots = len(mots)

    frequences = {}

    for mot, nombre in compteur.items():

        # Fréquence relative
        frequence = nombre / total_mots

        frequences[mot] = frequence

    return frequences, compteur, total_mots


# ============================================================
# MISE A JOUR DE LA DATABASE
# ============================================================

def mettre_a_jour_database(frequences):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        total = len(frequences)
        compteur = 0

        for mot, frequence in frequences.items():

            longueur = len(mot)

            if longueur < 1 or longueur > MAX_LENGTH:
                continue

            # Table spéciale pour les mots d'une seule lettre
            if longueur == 1:
                table = "mots_1_lettre"
            else:
                table = f"mots_{longueur}_lettres"

            cursor.execute(
                f"""
                INSERT INTO {table} (mot, frequence)
                VALUES (%s, %s)

                ON CONFLICT (mot)
                DO UPDATE SET
                    frequence = EXCLUDED.frequence;
                """,
                (mot, frequence)
            )

            compteur += 1

            if compteur % 1000 == 0:
                print(
                    f"Progression : {compteur}/{total}"
                )

        conn.commit()

        print(
            f"\n{compteur} mots traités avec succès."
        )

    except Exception as e:

        conn.rollback()

        print(
            f"\nErreur pendant la mise à jour : {e}"
        )

        raise

    finally:

        cursor.close()
        conn.close()


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():

    print("=" * 60)
    print("CALCUL DES FREQUENCES DES MOTS")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Lecture du corpus
    # --------------------------------------------------------

    print("\n[1/4] Lecture du corpus...")

    texte = lire_corpus()

    print(
        f"      Taille du corpus : {len(texte):,} caractères"
    )

    # --------------------------------------------------------
    # 2. Extraction
    # --------------------------------------------------------

    print("\n[2/4] Extraction des mots...")

    mots = extraire_mots(texte)

    total_mots = len(mots)

    print(
        f"      Nombre total de mots : {total_mots:,}"
    )

    # --------------------------------------------------------
    # 3. Calcul
    # --------------------------------------------------------

    print("\n[3/4] Calcul des fréquences...")

    frequences, compteurs, total_mots = calculer_frequences(mots)

    print(
        f"      Mots différents : {len(frequences):,}"
    )

    # Top 10
    print("\n      Top 10 des mots :")

    for mot, nombre in compteurs.most_common(10):

        frequence = frequences[mot]

        print(
            f"      {mot:<15} "
            f"{nombre:>10,} occurrences   "
            f"{frequence:.8f}   "
            f"({frequence * 100:.4f}%)"
        )

    # --------------------------------------------------------
    # 4. PostgreSQL
    # --------------------------------------------------------

    print("\n[4/4] Mise à jour PostgreSQL...")

    mettre_a_jour_database(frequences)

    print("\n" + "=" * 60)
    print("TERMINÉ")
    print("=" * 60)


# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":
    main()