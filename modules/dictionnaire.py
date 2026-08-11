import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.config import get_connection
class Dictionnaire:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def existe(self, mot):
        self.cursor.execute(
            "SELECT 1 FROM words WHERE mot=%s LIMIT 1;",
            (mot.lower(),)
        )
        return self.cursor.fetchone() is not None

    def candidats(self, mot, limite=5):
        self.cursor.execute("""
            SELECT mot
            FROM words
            WHERE levenshtein(mot, %s) <= 2
            ORDER BY levenshtein(mot, %s), frequence DESC
            LIMIT %s;
        """, (mot.lower(), mot.lower(), limite))

        return [x[0] for x in self.cursor.fetchall()]



if __name__ == "__main__":
    dico = Dictionnaire()

    print(dico.existe("hope"))
    print(dico.candidats("sope"))