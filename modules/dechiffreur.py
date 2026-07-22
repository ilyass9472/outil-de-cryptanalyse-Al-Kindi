<<<<<<< HEAD
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
=======
class dechiffreur:
    def __init__(self, texte_chiffre, cle):
        self.texte_chiffre = texte_chiffre
        self.cle = cle

    def dechiffrement(self):

        letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
                   "n","o","p","q","r","s","t","u","v","w","x","y","z"]

        Letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
                   "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

        numbers = ["0","1","2","3","4","5","6","7","8","9"]

        new_list_letters = []
        New_list_letters = []
        new_list_numbers = []
        new_letters = []

        cle = self.cle % 26

        
        for i in range(len(self.texte_chiffre)):
            new_letters.append(self.texte_chiffre[i])

        
        i = cle
        while i < len(letters):
            new_list_letters.append(letters[i])
            New_list_letters.append(Letters[i])

            if i == len(letters) - 1:
                i = -1

            if i == cle - 1:
                break

            i += 1

        
        i = cle % 10
        while i < len(numbers):
            new_list_numbers.append(numbers[i])

            if i == len(numbers) - 1:
                i = -1

            if i == (cle % 10) - 1:
                break

            i += 1

        

        i = 0
        while i < len(new_letters):

            if new_letters[i] in new_list_letters:
                index = new_list_letters.index(new_letters[i])
                new_letters[i] = letters[index]

            elif new_letters[i] in New_list_letters:
                index = New_list_letters.index(new_letters[i])
                new_letters[i] = Letters[index]

            elif new_letters[i] in new_list_numbers:
                index = new_list_numbers.index(new_letters[i])
                new_letters[i] = numbers[index]

            i += 1

        texte_dechiffre = ""

        for i in range(len(new_letters)):
            texte_dechiffre += new_letters[i]

        return texte_dechiffre
>>>>>>> 7c6ecff0e835acf0bd90075f324aa7c34b50af14
