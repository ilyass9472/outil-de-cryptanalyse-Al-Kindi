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
 '''
from modules.frequence import calculer_frequence
from modules.analyseur_frequence import AnalyseurFrequence
from modules.chiffreur import chiffrement
from modules.dechiffreur import dechiffrement
from utils.input import Input
from utils.cle import cle
from modules.analyseur_lexical import AnalyseurLexical
print(banner)
choix = input("choisis une option: ")

match choix:
    case "1":
        print("[1]: chiffrage cesar avec cle")

        reader = Input("")
        text = reader.get_text()
        key = cle()
        
        print(chiffrement(text, key))

    case "2":
        print("[2]: dechiffrage cesar avec cle")

        reader = Input("")
        text = reader.get_text()
        key = -1*int(cle())

        print(dechiffrement(text, key))

    case "3":
        print("[3]: dechiffrage cesar sans cle")
        
        with open("data/texte_chiffre.txt", "r", encoding="utf-8") as f:

            texte = f.read()

        analyseur = AnalyseurFrequence(texte)
        analyseur.calculer_frequence()
        analyseur_lexical = AnalyseurLexical()
        print("Training dechifrage frequence terminé.")
        resultat = analyseur_lexical.compare_frequence(texte)

        print("\n==============================")
        print("Texte déchiffré (approximation)")
        print("==============================")
        print(resultat)        

    case _:
        print("Option invalide")