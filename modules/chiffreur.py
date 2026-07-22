<<<<<<< HEAD
=======
class chiffreur:
    def __init__(self, texte, cle):
        self.texte = texte
        self.cle = cle

mychiffreur = chiffreur("Bonjour", "haha")

>>>>>>> 7c6ecff0e835acf0bd90075f324aa7c34b50af14

def chiffrement(texte, cle):

    texte_chiffre = ""

    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m",
               "n","o","p","q","r","s","t","u","v","w","x","y","z"]

    Letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
               "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    numbers = ["0","1","2","3","4","5","6","7","8","9"]

    new_list_letters = []
    New_list_letters = []
    new_list_numbers = []
    new_letters = []

    cle = cle % 26

    # Construction du texte
    for i in range(len(texte)):
        new_letters.append(texte[i])

    # Alphabet minuscule et majuscule
    i = cle
    while i < len(letters):
        new_list_letters.append(letters[i])
        New_list_letters.append(Letters[i])

        if i == len(letters) - 1:
            i = -1

        if i == cle - 1:
            break

        i += 1

    # Chiffrement des nombres
    i = cle % 10
    while i < len(numbers):
        new_list_numbers.append(numbers[i])

        if i == len(numbers) - 1:
            i = -1

        if i == (cle % 10) - 1:
            break

        i += 1

    # Chiffrement du texte
    i = 0
    while i < len(new_letters):

        if new_letters[i] in letters:
            index = letters.index(new_letters[i])
            new_letters[i] = new_list_letters[index]

        elif new_letters[i] in Letters:
            index = Letters.index(new_letters[i])
            new_letters[i] = New_list_letters[index]

        elif new_letters[i] in numbers:
            index = numbers.index(new_letters[i])
            new_letters[i] = new_list_numbers[index]

        i += 1

    # Reconstruction du texte
    for i in range(len(new_letters)):
        texte_chiffre += new_letters[i]

    return texte_chiffre