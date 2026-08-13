import sys
import os
import re
import math
from typing import Optional

# ============================================================
# PATH PROJECT
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from data.config import get_connection


# ============================================================
# CONFIGURATION
# ============================================================

MAX_LONGUEUR = 30

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "dechifre.txt"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "Dechiffre_Final.txt"
)


# ============================================================
# POIDS LANGUAGE MODEL
# ============================================================

ALPHA = 0.5
BETA = 1.0
GAMMA = 1.5


# ============================================================
# SMOOTHING
# ============================================================

# Petite probabilité utilisée lorsqu'un n-gramme
# n'existe pas dans la base.

SMOOTHING_PROBABILITY = 1e-12


# ============================================================
# DECISION
# ============================================================

MIN_IMPROVEMENT = 1.0


# ============================================================
# CANDIDATS
# ============================================================

MAX_CANDIDATS = 5000


# ============================================================
# DICTIONNAIRE
# ============================================================

class Dictionnaire:

    # ========================================================
    # INITIALISATION
    # ========================================================

    def __init__(self):

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        # ----------------------------------------------------
        # Caches
        # ----------------------------------------------------

        self.cache_unigram = {}
        self.cache_bigram = {}
        self.cache_trigram = {}

        # ----------------------------------------------------
        # Informations dictionnaire
        # ----------------------------------------------------

        self.total_words = self._get_total_words()
        self.vocab_size = self._get_vocab_size()

        print("=" * 60)
        print("DICTIONNAIRE - CORRECTION CONTEXTUELLE")
        print("=" * 60)

        print(
            f"Total words : "
            f"{self.total_words:.12f}"
        )

        print(
            f"Vocabulary  : "
            f"{self.vocab_size:,}"
        )

    # ========================================================
    # TABLE SELON LONGUEUR
    # ========================================================

    def _get_table(
        self,
        mot: str
    ) -> Optional[str]:

        longueur = len(mot)

        if longueur < 1 or longueur > MAX_LONGUEUR:
            return None

        if longueur == 1:
            return "mots_1_lettre"

        return f"mots_{longueur}_lettres"

    # ========================================================
    # TOTAL WORDS
    #
    # Si les fréquences des mots sont normalisées :
    #
    # SUM(frequence) ≈ 1
    #
    # ========================================================

    def _get_total_words(self):

        total = 0.0

        for longueur in range(
            1,
            MAX_LONGUEUR + 1
        ):

            table = (
                "mots_1_lettre"
                if longueur == 1
                else f"mots_{longueur}_lettres"
            )

            try:

                self.cursor.execute(
                    f"""
                    SELECT COALESCE(
                        SUM(frequence),
                        0
                    )
                    FROM {table};
                    """
                )

                result = self.cursor.fetchone()

                if (
                    result
                    and result[0] is not None
                ):
                    total += float(result[0])

            except Exception:

                self.conn.rollback()

        return total

    # ========================================================
    # VOCABULARY SIZE
    # ========================================================

    def _get_vocab_size(self):

        total = 0

        for longueur in range(
            1,
            MAX_LONGUEUR + 1
        ):

            table = (
                "mots_1_lettre"
                if longueur == 1
                else f"mots_{longueur}_lettres"
            )

            try:

                self.cursor.execute(
                    f"""
                    SELECT COUNT(*)
                    FROM {table};
                    """
                )

                result = self.cursor.fetchone()

                if result:
                    total += int(result[0])

            except Exception:

                self.conn.rollback()

        return max(total, 1)

    # ========================================================
    # GET UNIGRAM
    #
    # frequence = P(word)
    #
    # ========================================================

    def get_unigram(
        self,
        mot: str
    ):

        mot = mot.lower()

        if (
            len(mot) < 1
            or len(mot) > MAX_LONGUEUR
        ):
            return (
                0.0,
                -float("inf")
            )

        # ----------------------------------------------------
        # CACHE
        # ----------------------------------------------------

        if mot in self.cache_unigram:
            return self.cache_unigram[mot]

        table = self._get_table(mot)

        if table is None:
            return (
                0.0,
                -float("inf")
            )

        # ----------------------------------------------------
        # DATABASE
        # ----------------------------------------------------

        self.cursor.execute(
            f"""
            SELECT frequence
            FROM {table}
            WHERE mot = %s
            LIMIT 1;
            """,
            (mot,)
        )

        result = self.cursor.fetchone()

        # ----------------------------------------------------
        # Word not found
        # ----------------------------------------------------

        if not result:

            value = (
                0.0,
                -float("inf")
            )

            self.cache_unigram[mot] = value

            return value

        # ----------------------------------------------------
        # Frequency
        # ----------------------------------------------------

        frequence = float(result[0])

        if frequence <= 0:

            log_probability = -float("inf")

        else:

            # La fréquence est déjà une probabilité.
            probability = frequence

            log_probability = math.log(
                max(
                    probability,
                    SMOOTHING_PROBABILITY
                )
            )

        value = (
            frequence,
            log_probability
        )

        self.cache_unigram[mot] = value

        return value

    # ========================================================
    # EXISTE
    # ========================================================

    def existe(
        self,
        mot: str
    ) -> bool:

        frequency, _ = self.get_unigram(mot)

        return frequency > 0

    # ========================================================
    # BIGRAM
    #
    # word_bigrams.frequence
    #
    # frequence = P(word1, word2)
    #
    # Donc :
    #
    # P(word2 | word1)
    #
    # = P(word1, word2)
    #   ----------------
    #      P(word1)
    #
    # ========================================================

    def get_bigram_log_probability(
        self,
        word1: str,
        word2: str
    ):

        word1 = word1.lower()
        word2 = word2.lower()

        key = (
            word1,
            word2
        )

        # ----------------------------------------------------
        # CACHE
        # ----------------------------------------------------

        if key in self.cache_bigram:
            return self.cache_bigram[key]

        # ----------------------------------------------------
        # P(word1, word2)
        # ----------------------------------------------------

        self.cursor.execute(
            """
            SELECT frequence
            FROM word_bigrams
            WHERE word1 = %s
              AND word2 = %s
            LIMIT 1;
            """,
            (
                word1,
                word2
            )
        )

        result = self.cursor.fetchone()

        # ----------------------------------------------------
        # Bigram absent
        # ----------------------------------------------------

        if not result:

            score = math.log(
                SMOOTHING_PROBABILITY
            )

            self.cache_bigram[key] = score

            return score

        bigram_frequency = float(
            result[0]
        )

        # ----------------------------------------------------
        # P(word1)
        # ----------------------------------------------------

        word1_frequency, _ = (
            self.get_unigram(word1)
        )

        # ----------------------------------------------------
        # Conditional probability
        #
        # P(word2 | word1)
        # ----------------------------------------------------

        if (
            word1_frequency <= 0
            or bigram_frequency <= 0
        ):

            probability = (
                SMOOTHING_PROBABILITY
            )

        else:

            probability = (
                bigram_frequency
                /
                word1_frequency
            )

            probability = min(
                max(
                    probability,
                    SMOOTHING_PROBABILITY
                ),
                1.0
            )

        # ----------------------------------------------------
        # LOG
        # ----------------------------------------------------

        score = math.log(
            probability
        )

        self.cache_bigram[key] = score

        return score

    # ========================================================
    # TRIGRAM
    #
    # word_trigrams.frequence
    #
    # frequence = P(word1, word2, word3)
    #
    # word_bigrams.frequence
    #
    # frequence = P(word1, word2)
    #
    # Donc :
    #
    # P(word3 | word1, word2)
    #
    # =
    #
    # P(word1, word2, word3)
    # ----------------------
    #    P(word1, word2)
    #
    # ========================================================

    def get_trigram_log_probability(
        self,
        word1: str,
        word2: str,
        word3: str
    ):

        word1 = word1.lower()
        word2 = word2.lower()
        word3 = word3.lower()

        key = (
            word1,
            word2,
            word3
        )

        # ----------------------------------------------------
        # CACHE
        # ----------------------------------------------------

        if key in self.cache_trigram:
            return self.cache_trigram[key]

        # ----------------------------------------------------
        # P(word1, word2, word3)
        # ----------------------------------------------------

        self.cursor.execute(
            """
            SELECT frequence
            FROM word_trigrams
            WHERE word1 = %s
              AND word2 = %s
              AND word3 = %s
            LIMIT 1;
            """,
            (
                word1,
                word2,
                word3
            )
        )

        result = self.cursor.fetchone()

        if not result:

            score = math.log(
                SMOOTHING_PROBABILITY
            )

            self.cache_trigram[key] = score

            return score

        trigram_frequency = float(
            result[0]
        )

        # ----------------------------------------------------
        # P(word1, word2)
        # ----------------------------------------------------

        self.cursor.execute(
            """
            SELECT frequence
            FROM word_bigrams
            WHERE word1 = %s
              AND word2 = %s
            LIMIT 1;
            """,
            (
                word1,
                word2
            )
        )

        result = self.cursor.fetchone()

        if not result:

            score = math.log(
                SMOOTHING_PROBABILITY
            )

            self.cache_trigram[key] = score

            return score

        bigram_frequency = float(
            result[0]
        )

        # ----------------------------------------------------
        # P(word3 | word1, word2)
        # ----------------------------------------------------

        if (
            trigram_frequency <= 0
            or bigram_frequency <= 0
        ):

            probability = (
                SMOOTHING_PROBABILITY
            )

        else:

            probability = (
                trigram_frequency
                /
                bigram_frequency
            )

            probability = min(
                max(
                    probability,
                    SMOOTHING_PROBABILITY
                ),
                1.0
            )

        # ----------------------------------------------------
        # LOG
        # ----------------------------------------------------

        score = math.log(
            probability
        )

        self.cache_trigram[key] = score

        return score

    # ========================================================
    # CONTEXT SCORE
    #
    # Score =
    #
    # α log P(word)
    # +
    # β log P(word | previous)
    # +
    # γ log P(word | previous2, previous)
    #
    # ========================================================

    def context_score(
        self,
        word: str,
        previous_word: Optional[str] = None,
        previous2_word: Optional[str] = None
    ):

        word = word.lower()

        if (
            len(word) < 1
            or len(word) > MAX_LONGUEUR
        ):
            return -float("inf")

        total_score = 0.0

        # ====================================================
        # UNIGRAM
        # ====================================================

        _, unigram_score = (
            self.get_unigram(word)
        )

        if unigram_score != -float("inf"):

            total_score += (
                ALPHA
                *
                unigram_score
            )

        else:

            total_score += (
                ALPHA
                *
                math.log(
                    SMOOTHING_PROBABILITY
                )
            )

        # ====================================================
        # BIGRAM
        # ====================================================

        if previous_word:

            bigram_score = (
                self.get_bigram_log_probability(
                    previous_word,
                    word
                )
            )

            total_score += (
                BETA
                *
                bigram_score
            )

        # ====================================================
        # TRIGRAM
        # ====================================================

        if (
            previous2_word
            and previous_word
        ):

            trigram_score = (
                self.get_trigram_log_probability(
                    previous2_word,
                    previous_word,
                    word
                )
            )

            total_score += (
                GAMMA
                *
                trigram_score
            )

        return total_score

    # ========================================================
    # CANDIDATS
    #
    # نفس طول الكلمة.
    #
    # كنجيب candidates حسب unigram frequency.
    #
    # ========================================================

    def candidats(
        self,
        mot: str,
        limite: int = MAX_CANDIDATS
    ):

        mot = mot.lower()

        table = self._get_table(mot)

        if table is None:
            return []

        self.cursor.execute(
            f"""
            SELECT mot, frequence
            FROM {table}
            WHERE mot <> %s
              AND frequence > 0
            ORDER BY frequence DESC
            LIMIT %s;
            """,
            (
                mot,
                limite
            )
        )

        return self.cursor.fetchall()

    # ========================================================
    # CORRIGER MOT
    # ========================================================

    def corriger_mot(
        self,
        mot: str,
        previous_word: Optional[str] = None,
        previous2_word: Optional[str] = None
    ):

        mot_original = mot

        # ====================================================
        # PUNCTUATION
        # ====================================================

        match = re.match(
            r"^([^a-zA-Z]*)([a-zA-Z]+)([^a-zA-Z]*)$",
            mot
        )

        if not match:
            return mot_original

        prefixe = match.group(1)
        mot_pur = match.group(2)
        suffixe = match.group(3)

        mot_lower = mot_pur.lower()

        # ====================================================
        # MAX LENGTH
        # ====================================================

        if len(mot_lower) > MAX_LONGUEUR:
            return mot_original

        # ====================================================
        # ORIGINAL SCORE
        # ====================================================

        original_score = (
            self.context_score(
                mot_lower,
                previous_word,
                previous2_word
            )
        )

        # ====================================================
        # CHECK DICTIONARY
        # ====================================================

        original_frequency, _ = (
            self.get_unigram(
                mot_lower
            )
        )

        is_in_dictionary = (
            original_frequency > 0
        )

        # ====================================================
        # CANDIDATS
        # ====================================================

        candidates = self.candidats(
            mot_lower,
            MAX_CANDIDATS
        )

        if not candidates:
            return mot_original

        # ====================================================
        # BEST CANDIDATE
        # ====================================================

        best_candidate = mot_lower
        best_score = original_score

        # ====================================================
        # TEST CANDIDATES
        # ====================================================

        for candidate, frequency in candidates:

            candidate = candidate.lower()

            if candidate == mot_lower:
                continue

            candidate_score = (
                self.context_score(
                    candidate,
                    previous_word,
                    previous2_word
                )
            )

            if candidate_score > best_score:

                best_score = candidate_score
                best_candidate = candidate

        # ====================================================
        # IMPROVEMENT
        # ====================================================

        improvement = (
            best_score
            -
            original_score
        )

        # ====================================================
        # DECISION
        # ====================================================

        should_replace = (
            best_candidate != mot_lower
            and improvement >= MIN_IMPROVEMENT
        )

        # ====================================================
        # PROTECTION DES MOTS EXISTANTS
        #
        # Une vraie parole du dictionnaire ne doit pas
        # être remplacée trop facilement.
        # ====================================================

        if (
            is_in_dictionary
            and improvement < 2.0
        ):

            should_replace = False

        # ====================================================
        # KEEP ORIGINAL
        # ====================================================

        if not should_replace:
            return mot_original

        # ====================================================
        # PRESERVE CASE
        # ====================================================

        if mot_pur.isupper():

            meilleur_mot = (
                best_candidate.upper()
            )

        elif mot_pur.istitle():

            meilleur_mot = (
                best_candidate.capitalize()
            )

        else:

            meilleur_mot = (
                best_candidate.lower()
            )

        # ====================================================
        # RESULT
        # ====================================================

        resultat = (
            prefixe
            +
            meilleur_mot
            +
            suffixe
        )

        print(
            f"[CORRECTION] "
            f"{mot_original} -> {resultat} "
            f"| improvement={improvement:.3f}"
        )

        return resultat

    # ========================================================
    # CORRIGER FICHIER
    # ========================================================

    def corriger_fichier(self):

        if not os.path.exists(INPUT_FILE):

            print(
                f"Erreur : "
                f"{INPUT_FILE} introuvable."
            )

            return

        print()
        print("=" * 60)
        print("LECTURE DU TEXTE")
        print("=" * 60)

        # ====================================================
        # READ
        # ====================================================

        with open(
            INPUT_FILE,
            "r",
            encoding="utf-8"
        ) as fichier:

            texte = fichier.read()

        print(
            f"Taille : "
            f"{len(texte):,} caractères"
        )

        # ====================================================
        # LINES
        #
        # keepends=True
        # pour conserver exactement les \n.
        # ====================================================

        lignes = texte.splitlines(
            keepends=True
        )

        resultat_final = []

        mots_traites = 0
        mots_corriges = 0

        # ====================================================
        # PROCESS LINES
        # ====================================================

        for numero_ligne, ligne in enumerate(
            lignes,
            start=1
        ):

            # ------------------------------------------------
            # Find words
            # ------------------------------------------------

            spans = list(
                re.finditer(
                    r"[a-zA-Z]+",
                    ligne
                )
            )

            # ------------------------------------------------
            # No words
            # ------------------------------------------------

            if not spans:

                resultat_final.append(
                    ligne
                )

                continue

            # ------------------------------------------------
            # Mutable line
            # ------------------------------------------------

            nouvelle_ligne = list(
                ligne
            )

            # ------------------------------------------------
            # Context
            # ------------------------------------------------

            previous_word = None
            previous2_word = None

            # =================================================
            # WORDS
            # =================================================

            for span in spans:

                start = span.start()
                end = span.end()

                mot_original = (
                    ligne[start:end]
                )

                mot_pur = (
                    mot_original.lower()
                )

                # =============================================
                # > 30 characters
                # =============================================

                if len(mot_pur) > MAX_LONGUEUR:

                    previous2_word = (
                        previous_word
                    )

                    previous_word = (
                        mot_pur
                    )

                    continue

                # =============================================
                # CORRECTION
                # =============================================

                mot_corrige = (
                    self.corriger_mot(
                        mot_original,
                        previous_word,
                        previous2_word
                    )
                )

                mots_traites += 1

                # =============================================
                # REPLACE
                # =============================================

                if mot_corrige != mot_original:

                    mots_corriges += 1

                    nouvelle_ligne[
                        start:end
                    ] = mot_corrige

                    current_word = (
                        mot_corrige.lower()
                    )

                else:

                    current_word = (
                        mot_pur
                    )

                # =============================================
                # UPDATE CONTEXT
                # =============================================

                previous2_word = (
                    previous_word
                )

                previous_word = (
                    current_word
                )

            # ------------------------------------------------
            # Rebuild line
            # ------------------------------------------------

            resultat_final.append(
                "".join(
                    nouvelle_ligne
                )
            )

            # =================================================
            # PROGRESS
            # =================================================

            if numero_ligne % 100 == 0:

                print(
                    f"Lignes traitées : "
                    f"{numero_ligne:,}"
                )

        # ====================================================
        # FINAL TEXT
        # ====================================================

        texte_final = "".join(
            resultat_final
        )

        # ====================================================
        # SAVE
        # ====================================================

        output_directory = os.path.dirname(
            OUTPUT_FILE
        )

        os.makedirs(
            output_directory,
            exist_ok=True
        )

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as fichier:

            fichier.write(
                texte_final
            )

        # ====================================================
        # RESULT
        # ====================================================

        print()
        print("=" * 60)
        print("CORRECTION TERMINÉE")
        print("=" * 60)

        print(
            f"Mots traités  : "
            f"{mots_traites:,}"
        )

        print(
            f"Mots corrigés : "
            f"{mots_corriges:,}"
        )

        print(
            f"Fichier final : "
            f"{OUTPUT_FILE}"
        )

    # ========================================================
    # FERMER DATABASE
    # ========================================================

    def fermer(self):

        try:

            self.cursor.close()

        finally:

            self.conn.close()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    dico = Dictionnaire()

    try:

        dico.corriger_fichier()

    except Exception as e:

        print()
        print("=" * 60)
        print("ERREUR")
        print("=" * 60)

        print(e)

        # PostgreSQL rollback
        dico.conn.rollback()

        raise

    finally:

        dico.fermer()