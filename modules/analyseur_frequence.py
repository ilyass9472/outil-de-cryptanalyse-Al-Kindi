
from data.config import get_connection
from collections import Counter


class AnalyseurFrequence:
    def __init__(self, texte):
        self.texte = texte
        self.frequences = 0
    def calculer_frequence(self):
        try:
            conn = get_connection()
        except Exception as e:
            print("Erreur lors de la connexion à la base de données :", e)
        cursor = conn.cursor()
        cursor.execute("UPDATE lettres_lower_chiffre SET frequence = 0")
        cursor.execute("UPDATE lettres_upper_chiffre SET frequence = 0")
        cursor.execute("UPDATE nombres_chiffre SET frequence = 0")
        cursor.execute("UPDATE symbole_chiffre SET frequence = 0")
        print("Longueur du texte :", len(self.texte))
    
        caracteres = [
        c for c in self.texte
        if c.islower() or c.isupper() or c.isdigit()
        or (not c.isalnum() and not c.isspace())
        ]
        i=0
            
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
        for caractere, repetition in compteur.items():
            frequence = repetition / total
            if caractere.islower():
                try:
                    cursor.execute(
                    """
                    UPDATE lettres_lower_chiffre
                    SET frequence = %s
                    WHERE lettre = %s
                    """,
                    (frequence, caractere)
                )
                except Exception as e:
                    print("Erreur lors de la mise à jour de la fréquence des lettres minuscules :", e)
            elif caractere.isupper():
                try:
                    
                    cursor.execute(""" UPDATE lettres_upper_chiffre SET frequence = %s WHERE lettre = %s  """, (frequence, caractere))
                except Exception as e:
                    print("Erreur lors de la mise à jour de la fréquence des lettres majuscules :", e)
            elif caractere.isdigit():
                try:
                    cursor.execute(""" UPDATE nombres_chiffre SET frequence = %s WHERE chiffre = %s  """, (frequence, caractere))
                except Exception as e:
                    print("Erreur lors de la mise à jour de la fréquence des nombres :",e)
            elif not caractere.isalnum() and not caractere.isspace():
                try:
                    cursor.execute(""" UPDATE symbole_chiffre SET frequence = %s WHERE symbole = %s  """, (frequence, caractere))
                except Exception as e:
                    print("Erreur lors de la mise à jour de la fréquence des symboles :", e)
            conn.commit()
        cursor.execute("SELECT lettre, frequence FROM lettres_lower ORDER BY lettre;")
        print(cursor.fetchall(  ))
        print("Fréquences de text chiffré calculées avec succès.")
        cursor.close()
        conn.close()