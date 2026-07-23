banner = '''
\033[38;2;213;155;125m+---------------------------------------------------------------------------------+
\033[38;2;213;155;125m|     ▄▄     ▄▄▄▄                ▄▄   ▄▄▄     ██                     ▄▄     ██    |
\033[38;2;213;155;125m|    ████    ▀▀██                ██  ██▀      ▀▀                     ██     ▀▀    |
\033[38;2;213;155;125m|    ████      ██                ██▄██      ████     ██▄████▄   ▄███▄██   ████    |
\033[38;2;213;155;125m|   ██  ██     ██                █████        ██     ██▀   ██  ██▀  ▀██     ██    |
\033[38;2;213;155;125m|   ██████     ██                ██  ██▄      ██     ██    ██  ██    ██     ██    |
\033[38;2;213;155;125m|  ▄██  ██▄    ██▄▄▄             ██   ██▄  ▄▄▄██▄▄▄  ██    ██  ▀██▄▄███  ▄▄▄██▄▄▄ |
\033[38;2;213;155;125m|  ▀▀    ▀▀     ▀▀▀▀             ▀▀    ▀▀  ▀▀▀▀▀▀▀▀  ▀▀    ▀▀    ▀▀▀ ▀▀  ▀▀▀▀▀▀▀▀ |
\033[38;2;213;155;125m+---------------------------------------------------------------------------------+\033[0m
 choisis l'option que tu veux faire 
 [1]: chiffrage cesar avec cle
 [2]: dechiffrage cesar avec cle
 [3]: dechiffrage cesar sans cle
 [4]: option 4
 [5]: option 5 
 '''

from modules.chiffreur import chiffrement
from modules.dechiffreur import dechiffrement
from utils.input import Input
from utils.cle import cle

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
        key = -1*int(cle())

        print(dechiffrement(text, key))
    case "3":
        print("dechiffrage cesar sans cle")
    case "4":
        print("Option 4")
    case "5":
        print("Option 5")
    case _:
        print("Option invalide")