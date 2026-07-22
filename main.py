from modules.chiffreur import chiffrement
from modules.dechiffreur import dechiffreur
from utils.input import Input
from utils.cle import cle
from data.config import get_connection
try:
    conn = get_connection()
    print("Connexion réussie !")

    cursor = conn.cursor()
    cursor.execute("SELECT version();")

    print(cursor.fetchone())

    cursor.close()
    conn.close()

except Exception as e:
    print("Erreur :", e)
reader = Input("")
text = reader.get_text()
key = cle()

switcher = ""

while switcher not in ["C", "D"]:
    switcher = input("Voulez-vous chiffrer ou déchiffrer le texte ? (C/D) : ").upper()

if switcher == "C":
    print(chiffrement(text, key))

elif switcher == "D":
    dechiffreur_obj = dechiffreur(text, key)
    print(dechiffreur_obj.dechiffrement())