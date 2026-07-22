<<<<<<< HEAD
banner = '''
\033[38;2;213;155;125m-----------------------------------------------------------------------------------
\033[38;2;213;155;125m|     ▄▄     ▄▄▄▄                ▄▄   ▄▄▄     ██                     ▄▄     ██    |
\033[38;2;213;155;125m|    ████    ▀▀██                ██  ██▀      ▀▀                     ██     ▀▀    |
\033[38;2;213;155;125m|    ████      ██                ██▄██      ████     ██▄████▄   ▄███▄██   ████    |
\033[38;2;213;155;125m|   ██  ██     ██                █████        ██     ██▀   ██  ██▀  ▀██     ██    |
\033[38;2;213;155;125m|   ██████     ██                ██  ██▄      ██     ██    ██  ██    ██     ██    |
\033[38;2;213;155;125m|  ▄██  ██▄    ██▄▄▄             ██   ██▄  ▄▄▄██▄▄▄  ██    ██  ▀██▄▄███  ▄▄▄██▄▄▄ |
\033[38;2;213;155;125m|  ▀▀    ▀▀     ▀▀▀▀             ▀▀    ▀▀  ▀▀▀▀▀▀▀▀  ▀▀    ▀▀    ▀▀▀ ▀▀  ▀▀▀▀▀▀▀▀ |
\033[38;2;213;155;125m-----------------------------------------------------------------------------------\033[0m
 choisis l'option que tu veux faire 
 [1]: chiffrage cesar avec cle
 [2]: dechiffrage cesar avec cle
 [3]: dechiffrage cesar sans cle
 [4]: option 4
 [5]: option 5 
 '''
print(banner)
choix = input("choisis une option: ")

match choix:
    case "1":
        from modules.chiffreur import chiffrement
        from utils.input import Input
        from utils.cle import cle
        print("[1]: chiffrage cesar avec cle")

        reader = Input("")
        text = reader.get_text()
        key = cle()
        
        print(chiffrement(text, key))
    case "2":
        from modules.dechiffreur import dechiffrement
        from utils.input import Input
        from utils.cle import cle
        print("[2]: dechiffrage cesar avec cle")

        reader = Input("")
        text = reader.get_text()
        key = int(cle())*-1

        print(dechiffrement(text, key))
    case "3":
        print("dechiffrage cesar sans cle")
    case "4":
        print("Option 4")
    case "5":
        print("Option 5")
    case _:
        print("Option invalide")
=======
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
>>>>>>> 7c6ecff0e835acf0bd90075f324aa7c34b50af14
