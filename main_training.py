from modules.frequence import calculer_frequence

with open("data/corpus.txt", "r", encoding="utf-8") as f:
    texte = f.read()

calculer_frequence(texte)

print("Training terminé.")