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
    k=0
    cle = input("Entrez la clé de chiffrement (un entier) : ")
    cle = int(cle)
    while cle == 0:
        cle = input("Entrez la clé de chiffrement (un entier) : ")
        cle = int(cle)
        k+= 1
    
    j=0
    while cle < 0:
        cle = 26 + cle
        j += 1
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
    for i in range(len(new_letters)):
        texte_chiffre += new_letters[i]
    return texte_chiffre

chiffrement.cle = 3
texte = "bonjour mongol"
print(chiffrement(texte, chiffrement.cle))