class Input :
        def __init__(self, text):
            self.text = ""
        def get_text(self):
            print("Entrez le texte:")
            lignes = []
            while True:
                line = input()
                if line == "xa9la7":
                        break
                lignes.append(line)
            self.text = "\n".join(lignes)
            return self.text

