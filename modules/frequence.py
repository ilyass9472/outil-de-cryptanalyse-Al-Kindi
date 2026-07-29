from data.config import get_connection
from collections import Counter


def calculer_frequence(texte):

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

  
    # cursor.execute("UPDATE lettres_lower SET frequence = 0")
    # cursor.execute("UPDATE lettres_upper SET frequence = 0")
    # cursor.execute("UPDATE nombres SET frequence = 0")
    # cursor.execute("UPDATE symboles SET frequence = 0")
    print("Longueur du texte :", len(texte))
    # only caractères 
    caracteres = [
    c for c in texte
    if c.islower()
    or c.isupper()
    or c.isdigit()
    or c == " "
    or (not c.isalnum() and not c.isspace())
]
    cursor.execute("""
    SELECT current_database(),
       current_user,
       inet_server_addr(),
       inet_server_port();
    """)

    print(cursor.fetchone())
    total = len(caracteres)
    cursor.execute("""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_name='lettres_lower';
    """)

    print(cursor.fetchall())
    if total == 0:
        print("Aucun caractère valide trouvé.")
        cursor.close()
        conn.close()
        return


    compteur = Counter(caracteres)

    # insert in PostgreSQL
    for caractere, repetition in compteur.items():

        frequence = repetition / total

        if caractere.islower():

            cursor.execute(
                """
                UPDATE lettres_lower
                SET frequence = %s
                WHERE lettre = %s
                """,
                (frequence, caractere)
            )

        elif caractere.isupper():

            cursor.execute(
                """
                UPDATE lettres_upper
                SET frequence = %s
                WHERE lettre = %s
                """,
                (frequence, caractere)
            )

        elif caractere.isdigit():

            cursor.execute(
                """
                UPDATE nombres
                SET frequence = %s
                WHERE chiffre = %s
                """,
                (frequence, caractere)
            )
        elif not caractere.isalnum() and not caractere.isspace():

            cursor.execute(
                """
                UPDATE symboles
                SET frequence = %s
                WHERE symbole = %s
                """,
                (frequence, caractere)
            )

    conn.commit()
    cursor.execute("SELECT lettre, frequence FROM lettres_lower ORDER BY lettre;")
    print(cursor.fetchall())
    print("Base de données entraînée avec succès.")

    cursor.close()
    conn.close()