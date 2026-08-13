def dechiffrement(texte, cle):

    texte_dechiffre = ""

    letters = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
    ]

    Letters = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
    ]

    numbers = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    ]

    new_list_letters = []
    New_list_letters = []
    new_list_numbers = []
    new_letters = []

    # =========================================================
    # Normalisation de la clé
    # =========================================================

    cle = cle % 26

    # =========================================================
    # Construction du texte
    # =========================================================

    for i in range(len(texte)):
        new_letters.append(texte[i])

    # =========================================================
    # Construction alphabet minuscule et majuscule
    # =========================================================

    i = cle

    while i < len(letters):

        new_list_letters.append(letters[i])
        New_list_letters.append(Letters[i])

        if i == len(letters) - 1:
            i = -1

        if i == cle - 1:
            break

        i += 1

    # =========================================================
    # Construction des nombres
    # =========================================================

    i = cle % 10

    while i < len(numbers):

        new_list_numbers.append(numbers[i])

        if i == len(numbers) - 1:
            i = -1

        if i == (cle % 10) - 1:
            break

        i += 1

    # =========================================================
    # Déchiffrement
    # =========================================================

    i = 0

    while i < len(new_letters):

        # Lettres minuscules
        if new_letters[i] in letters:

            index = letters.index(new_letters[i])
            new_letters[i] = new_list_letters[index]

        # Lettres majuscules
        elif new_letters[i] in Letters:

            index = Letters.index(new_letters[i])
            new_letters[i] = New_list_letters[index]

        # Nombres
        elif new_letters[i] in numbers:

            index = numbers.index(new_letters[i])
            new_letters[i] = new_list_numbers[index]

        i += 1

    # =========================================================
    # Reconstruction du texte
    # 10 mots maximum par ligne
    # =========================================================

    nombre_mots = 0
    dans_un_mot = False

    for caractere in new_letters:

        texte_dechiffre += caractere

        # Vérifier si le caractère appartient à un mot
        if caractere.isalpha():

            # Début d'un nouveau mot
            if not dans_un_mot:

                dans_un_mot = True
                nombre_mots += 1

                # Après 10 mots -> nouvelle ligne
                if nombre_mots == 10:

                    texte_dechiffre += "\n"
                    nombre_mots = 0

        else:

            # Fin du mot
            dans_un_mot = False

    # =========================================================
    # Sauvegarde dans data/dechifre.txt
    # =========================================================

    with open(
        "data/dechifre.txt",
        "w",
        encoding="utf-8"
    ) as fichier:

        fichier.write(texte_dechiffre)

    # =========================================================
    # Retourner le texte
    # =========================================================

    return texte_dechiffre