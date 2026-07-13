from modules.chiffreur import chiffrement
from utils.input import Input
from utils.cle import cle
reader = Input("")
text = reader.get_text()
key = cle()

print(chiffrement(text, key))