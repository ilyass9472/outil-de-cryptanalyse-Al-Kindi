import os
import sys
import re
from collections import Counter

# ============================================================
# PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ============================================================
# DATABASE
# ============================================================

from data.config import get_connection
from psycopg2.extras import execute_values


# ============================================================
# CONFIGURATION
# ============================================================

CORPUS_FILE = os.path.join(
    BASE_DIR,
    "data",
    "corpus.txt"
)

MAX_WORD_LENGTH = 30

BATCH_SIZE = 10_000

WORD_PATTERN = re.compile(
    r"[a-z]+"
)


# ============================================================
# LECTURE DU CORPUS
# ============================================================

def read_corpus():

    print("=" * 60)
    print("LECTURE DU CORPUS")
    print("=" * 60)

    if not os.path.exists(CORPUS_FILE):

        raise FileNotFoundError(
            f"Corpus introuvable : {CORPUS_FILE}"
        )

    print(
        f"Corpus : {CORPUS_FILE}"
    )

    file_size = os.path.getsize(
        CORPUS_FILE
    )

    print(
        f"Taille : {file_size:,} octets"
    )

    with open(
        CORPUS_FILE,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as fichier:

        text = fichier.read().lower()

    print(
        f"Taille texte : "
        f"{len(text):,} caractères"
    )

    return text


# ============================================================
# EXTRACTION DES MOTS
# ============================================================

def extract_words(text):

    print("\n" + "=" * 60)
    print("TOKENISATION")
    print("=" * 60)

    all_words = WORD_PATTERN.findall(
        text
    )

    total_raw = len(all_words)

    print(
        f"Tokens trouvés : "
        f"{total_raw:,}"
    )

    # --------------------------------------------------------
    # On garde uniquement les mots <= 30 caractères.
    # Les mots > 30 sont ignorés.
    # --------------------------------------------------------

    words = [
        word
        for word in all_words
        if 1 <= len(word) <= MAX_WORD_LENGTH
    ]

    ignored = (
        total_raw
        - len(words)
    )

    print(
        f"Tokens valides (1-{MAX_WORD_LENGTH}) : "
        f"{len(words):,}"
    )

    print(
        f"Tokens ignorés (> {MAX_WORD_LENGTH}) : "
        f"{ignored:,}"
    )

    return words


# ============================================================
# BUILD BIGRAM
# ============================================================
#
# On calcule d'abord les occurrences.
#
# Exemple :
#
# the man
# the man
# the house
#
# occurrences :
#
# the | man   | 2
# the | house | 1
#
# Ensuite :
#
# total = 3
#
# frequence :
#
# the | man   | 2/3 = 0.666666...
# the | house | 1/3 = 0.333333...
#
# ============================================================

def build_bigrams(words):

    print("\n" + "=" * 60)
    print("CONSTRUCTION BIGRAM")
    print("=" * 60)

    counter = Counter()

    previous = None

    for word in words:

        if previous is not None:

            counter[
                (
                    previous,
                    word
                )
            ] += 1

        previous = word

    total_occurrences = sum(
        counter.values()
    )

    print(
        f"Bigram uniques : "
        f"{len(counter):,}"
    )

    print(
        f"Bigram occurrences : "
        f"{total_occurrences:,}"
    )

    if total_occurrences == 0:

        return {}

    # --------------------------------------------------------
    # NORMALISATION
    # --------------------------------------------------------

    normalized = {
        key: (
            frequency /
            total_occurrences
        )
        for key, frequency
        in counter.items()
    }

    return normalized


# ============================================================
# BUILD TRIGRAM
# ============================================================
#
# Même principe :
#
# frequence =
#
# occurrences trigram
# ------------------
# total occurrences trigram
#
# ============================================================

def build_trigrams(words):

    print("\n" + "=" * 60)
    print("CONSTRUCTION TRIGRAM")
    print("=" * 60)

    counter = Counter()

    previous2 = None
    previous1 = None

    for word in words:

        if (
            previous2 is not None
            and previous1 is not None
        ):

            counter[
                (
                    previous2,
                    previous1,
                    word
                )
            ] += 1

        previous2 = previous1
        previous1 = word

    total_occurrences = sum(
        counter.values()
    )

    print(
        f"Trigram uniques : "
        f"{len(counter):,}"
    )

    print(
        f"Trigram occurrences : "
        f"{total_occurrences:,}"
    )

    if total_occurrences == 0:

        return {}

    # --------------------------------------------------------
    # NORMALISATION
    # --------------------------------------------------------

    normalized = {
        key: (
            frequency /
            total_occurrences
        )
        for key, frequency
        in counter.items()
    }

    return normalized


# ============================================================
# CREATE TABLES
# ============================================================

def ensure_tables(cursor):

    print("\n" + "=" * 60)
    print("VERIFICATION DES TABLES")
    print("=" * 60)

    # --------------------------------------------------------
    # BIGRAM
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS word_bigrams (

            word1 VARCHAR(30) NOT NULL,

            word2 VARCHAR(30) NOT NULL,

            frequence DOUBLE PRECISION NOT NULL,

            PRIMARY KEY (
                word1,
                word2
            )

        );
        """
    )

    # --------------------------------------------------------
    # TRIGRAM
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS word_trigrams (

            word1 VARCHAR(30) NOT NULL,

            word2 VARCHAR(30) NOT NULL,

            word3 VARCHAR(30) NOT NULL,

            frequence DOUBLE PRECISION NOT NULL,

            PRIMARY KEY (
                word1,
                word2,
                word3
            )

        );
        """
    )

    print(
        "✓ word_bigrams existe"
    )

    print(
        "✓ word_trigrams existe"
    )


# ============================================================
# IMPORTANT :
# MIGRATION DES ANCIENNES COLONNES
# ============================================================
#
# Si les anciennes tables avaient :
#
# frequence BIGINT
#
# PostgreSQL ne peut pas insérer correctement des probabilités
# décimales.
#
# Donc on transforme la colonne en DOUBLE PRECISION.
#
# ============================================================

def alter_frequency_columns(cursor):

    print("\n" + "=" * 60)
    print("VERIFICATION TYPE FREQUENCE")
    print("=" * 60)

    cursor.execute(
        """
        ALTER TABLE word_bigrams
        ALTER COLUMN frequence
        TYPE DOUBLE PRECISION
        USING frequence::DOUBLE PRECISION;
        """
    )

    cursor.execute(
        """
        ALTER TABLE word_trigrams
        ALTER COLUMN frequence
        TYPE DOUBLE PRECISION
        USING frequence::DOUBLE PRECISION;
        """
    )

    print(
        "✓ word_bigrams.frequence = DOUBLE PRECISION"
    )

    print(
        "✓ word_trigrams.frequence = DOUBLE PRECISION"
    )


# ============================================================
# CLEAN OLD DATA
# ============================================================

def clean_tables(cursor):

    print("\n" + "=" * 60)
    print("NETTOYAGE DES ANCIENNES DONNÉES")
    print("=" * 60)

    cursor.execute(
        """
        TRUNCATE TABLE
            word_bigrams,
            word_trigrams;
        """
    )

    print(
        "✓ Tables nettoyées"
    )


# ============================================================
# INSERT BIGRAM
# ============================================================

def insert_bigrams(
    cursor,
    frequencies
):

    print("\n" + "=" * 60)
    print("INSERTION BIGRAM")
    print("=" * 60)

    data = [
        (
            word1,
            word2,
            frequency
        )
        for (
            word1,
            word2
        ), frequency
        in frequencies.items()
    ]

    total = len(data)

    print(
        f"Total bigrams uniques : "
        f"{total:,}"
    )

    if total == 0:

        print(
            "⚠ Aucun bigram à insérer."
        )

        return

    query = """
        INSERT INTO word_bigrams
        (
            word1,
            word2,
            frequence
        )
        VALUES %s
    """

    for start in range(
        0,
        total,
        BATCH_SIZE
    ):

        batch = data[
            start:start + BATCH_SIZE
        ]

        execute_values(
            cursor,
            query,
            batch,
            page_size=BATCH_SIZE
        )

        done = min(
            start + BATCH_SIZE,
            total
        )

        print(
            f"{done:,} / {total:,}"
        )

    print(
        "✓ Bigram insertion terminée"
    )


# ============================================================
# INSERT TRIGRAM
# ============================================================

def insert_trigrams(
    cursor,
    frequencies
):

    print("\n" + "=" * 60)
    print("INSERTION TRIGRAM")
    print("=" * 60)

    data = [
        (
            word1,
            word2,
            word3,
            frequency
        )
        for (
            word1,
            word2,
            word3
        ), frequency
        in frequencies.items()
    ]

    total = len(data)

    print(
        f"Total trigrams uniques : "
        f"{total:,}"
    )

    if total == 0:

        print(
            "⚠ Aucun trigram à insérer."
        )

        return

    query = """
        INSERT INTO word_trigrams
        (
            word1,
            word2,
            word3,
            frequence
        )
        VALUES %s
    """

    for start in range(
        0,
        total,
        BATCH_SIZE
    ):

        batch = data[
            start:start + BATCH_SIZE
        ]

        execute_values(
            cursor,
            query,
            batch,
            page_size=BATCH_SIZE
        )

        done = min(
            start + BATCH_SIZE,
            total
        )

        print(
            f"{done:,} / {total:,}"
        )

    print(
        "✓ Trigram insertion terminée"
    )


# ============================================================
# INDEXES
# ============================================================

def create_indexes(cursor):

    print("\n" + "=" * 60)
    print("CREATION DES INDEX")
    print("=" * 60)

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_word_bigrams_word1
        ON word_bigrams(word1);
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_word_bigrams_word2
        ON word_bigrams(word2);
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_word_trigrams_word1_word2
        ON word_trigrams(
            word1,
            word2
        );
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_word_trigrams_word2_word3
        ON word_trigrams(
            word2,
            word3
        );
        """
    )

    print(
        "✓ Index créés"
    )


# ============================================================
# STATISTICS
# ============================================================

def show_statistics(cursor):

    print("\n" + "=" * 60)
    print("STATISTIQUES DATABASE")
    print("=" * 60)

    # --------------------------------------------------------
    # BIGRAM UNIQUE
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM word_bigrams;
        """
    )

    bigram_count = cursor.fetchone()[0]

    # --------------------------------------------------------
    # TRIGRAM UNIQUE
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM word_trigrams;
        """
    )

    trigram_count = cursor.fetchone()[0]

    # --------------------------------------------------------
    # SOMME DES PROBABILITES BIGRAM
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COALESCE(
            SUM(frequence),
            0
        )
        FROM word_bigrams;
        """
    )

    bigram_total = cursor.fetchone()[0]

    # --------------------------------------------------------
    # SOMME DES PROBABILITES TRIGRAM
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COALESCE(
            SUM(frequence),
            0
        )
        FROM word_trigrams;
        """
    )

    trigram_total = cursor.fetchone()[0]

    print(
        f"Bigram uniques : "
        f"{bigram_count:,}"
    )

    print(
        f"Somme frequence bigram : "
        f"{bigram_total:.12f}"
    )

    print(
        f"Trigram uniques : "
        f"{trigram_count:,}"
    )

    print(
        f"Somme frequence trigram : "
        f"{trigram_total:.12f}"
    )


# ============================================================
# EXEMPLES
# ============================================================

def show_examples(cursor):

    print("\n" + "=" * 60)
    print("EXEMPLES")
    print("=" * 60)

    # --------------------------------------------------------
    # BIGRAMS
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            word1,
            word2,
            frequence
        FROM word_bigrams
        ORDER BY frequence DESC
        LIMIT 10;
        """
    )

    bigrams = cursor.fetchall()

    print(
        "\nword_bigrams"
    )

    print(
        "-" * 60
    )

    for (
        word1,
        word2,
        frequency
    ) in bigrams:

        print(
            f"{word1:<15} | "
            f"{word2:<15} | "
            f"{frequency:.10f}"
        )

    # --------------------------------------------------------
    # TRIGRAMS
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            word1,
            word2,
            word3,
            frequence
        FROM word_trigrams
        ORDER BY frequence DESC
        LIMIT 10;
        """
    )

    trigrams = cursor.fetchall()

    print(
        "\nword_trigrams"
    )

    print(
        "-" * 60
    )

    for (
        word1,
        word2,
        word3,
        frequency
    ) in trigrams:

        print(
            f"{word1:<12} | "
            f"{word2:<12} | "
            f"{word3:<12} | "
            f"{frequency:.10f}"
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("BUILD LANGUAGE MODEL")
    print("=" * 60)
    print()

    conn = None
    cursor = None

    try:

        # ====================================================
        # 1. READ CORPUS
        # ====================================================

        text = read_corpus()

        # ====================================================
        # 2. TOKENISATION
        # ====================================================

        words = extract_words(
            text
        )

        print(
            f"\nTotal words utilisées : "
            f"{len(words):,}"
        )

        if not words:

            raise ValueError(
                "Aucun mot valide trouvé dans le corpus."
            )

        # ====================================================
        # 3. BUILD BIGRAM
        # ====================================================

        bigrams = build_bigrams(
            words
        )

        # ====================================================
        # 4. BUILD TRIGRAM
        # ====================================================

        trigrams = build_trigrams(
            words
        )

        # ====================================================
        # Libération mémoire
        # ====================================================

        del text

        # ====================================================
        # 5. DATABASE
        # ====================================================

        print("\n" + "=" * 60)
        print("CONNEXION DATABASE")
        print("=" * 60)

        conn = get_connection()

        cursor = conn.cursor()

        print(
            "✓ Connexion PostgreSQL réussie"
        )

        # ====================================================
        # 6. CREATE TABLES
        # ====================================================

        ensure_tables(
            cursor
        )

        # ====================================================
        # 7. TYPE FREQUENCE
        # ====================================================

        alter_frequency_columns(
            cursor
        )

        # ====================================================
        # 8. CLEAN
        # ====================================================

        clean_tables(
            cursor
        )

        # ====================================================
        # 9. INSERT BIGRAM
        # ====================================================

        insert_bigrams(
            cursor,
            bigrams
        )

        # ====================================================
        # 10. INSERT TRIGRAM
        # ====================================================

        insert_trigrams(
            cursor,
            trigrams
        )

        # ====================================================
        # 11. INDEXES
        # ====================================================

        create_indexes(
            cursor
        )

        # ====================================================
        # 12. COMMIT
        # ====================================================

        conn.commit()

        print(
            "\n✓ COMMIT réussi"
        )

        # ====================================================
        # 13. STATISTICS
        # ====================================================

        show_statistics(
            cursor
        )

        # ====================================================
        # 14. EXAMPLES
        # ====================================================

        show_examples(
            cursor
        )

        print(
            "\n" + "=" * 60
        )

        print(
            "LANGUAGE MODEL TERMINÉ"
        )

        print(
            "=" * 60
        )

    except Exception as error:

        print(
            "\n" + "=" * 60
        )

        print(
            "ERREUR"
        )

        print(
            "=" * 60
        )

        print(
            f"{type(error).__name__}: "
            f"{error}"
        )

        if conn is not None:

            conn.rollback()

            print(
                "✓ Rollback effectué"
            )

        raise

    finally:

        if cursor is not None:

            cursor.close()

            print(
                "✓ Cursor fermé"
            )

        if conn is not None:

            conn.close()

            print(
                "✓ Connexion fermée"
            )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()