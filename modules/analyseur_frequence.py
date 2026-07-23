class AnalyseurFrequence:
    def __init__(self, texte):
        self.texte = texte
        self.frequences = 0
    def calculer_frequence(self):
            caracteres = [
            c for c in self.texte
            if c.islower() or c.isupper() or c.isdigit()
            or (not c.isalnum() and not c.isspace())
            ]
            i=0
            
            while i < len(self.texte):
                j=0
                while j < len(self.texte):
                     if self.texte[i] == self.texte[j]:

                        if self.texte[i].islower() and self.texte[i] in lettres_lower:
                             self.frequences
                            
                j += 1
            i += 1
