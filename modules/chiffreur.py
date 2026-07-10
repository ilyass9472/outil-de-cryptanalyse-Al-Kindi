class chiffreur:
    def __init__(self, texte, cle):
        self.texte = texte
        self.cle = cle
mychiffreur = chiffreur("Bonjour", "haha")



def chiffrement(texte, cle):
    
    texte_chiffre = ""
    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    new_list_letters = []
    new_letters = []
    cle = cle % 26
    for i in range(len(texte)):
        new_letters.append(texte[i])
    i=cle
    while i < len(letters):
        new_list_letters.append(letters[i])
        if i == len(letters) - 1:
            i = -1
        if i == cle - 1:
            break
        i+= 1
    i=0
    while i < len(new_letters):
        if new_letters[i] in letters:
            index = letters.index(new_letters[i])
            new_letters[i] = new_list_letters[index]
        i+=1
    return new_letters

chiffrement.cle = 3
texte = "bonjour"
print(chiffrement(texte, chiffrement.cle))