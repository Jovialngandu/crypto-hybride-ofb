import sys
from pathlib import Path

# Force Python à regarder dans la racine du projet
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modes.ofb import encrypt_ofb, decrypt_ofb
# Clé de 64 bits et IV de 64 bits en binaire
K_DES = "0100110001101111011001110110100101100011011010010110010101101100"
IV = "0011000100110010001100110011010000110101001101100011011100111000"

message_original = "Bonjour l'equipe !"

# Chiffrement
chiffre = encrypt_ofb(message_original, IV, K_DES)
print(f"Message clair : {message_original}")
print(f"Message chiffré : {chiffre}")

# Déchiffrement
clair_retrouve = decrypt_ofb(chiffre, IV, K_DES)
print(f"Message déchiffré : {clair_retrouve}")

assert message_original == clair_retrouve, "Erreur : Le message déchiffré ne correspond pas !"
