class Input :
        def __init__(self, text):
            self.text = ""
        def get_text(self):
            print("Entrez le texte:")
            lignes = []
            while True:
                line = input()
                if line == "":
                        break
                lignes.append(line)
            self.text = "\n".join(lignes)
            return self.text

