def cle():
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
    return cle