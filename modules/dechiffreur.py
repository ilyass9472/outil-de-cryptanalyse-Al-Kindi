def dechiffrement(texte, cle):
    
    texte_chiffre = ""
    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    Letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    new_list_letters = [] 
    New_list_letters = []
    new_letters = []
    k=0

    for i in range(len(texte)):
        new_letters.append(texte[i])
        
            
    i=cle
    while i < len(letters):
        new_list_letters.append(letters[i])
        New_list_letters.append(Letters[i])
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
        elif new_letters[i] in Letters:
            index = Letters.index(new_letters[i])
            new_letters[i] = New_list_letters[index]
        if new_letters[i] == "\n":
            new_letters[i] = ""



        i+=1
    for i in range(len(new_letters)):
        texte_chiffre += new_letters[i]
        
    return texte_chiffre
