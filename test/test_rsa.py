import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.rsa import generate_keypair, rsa_encrypt, rsa_decrypt

# Test avec petits nombres premiers
p, q, e = 61, 53, 17
pub_key, priv_key = generate_keypair(p, q, e)

print(f"Clé Publique (e, n) : {pub_key}")
print(f"Clé Privée   (d, n) : {priv_key}")

# Test de chiffrement d'un nombre (ex: un bloc de clé)
message = 65
chiffre = rsa_encrypt(message, pub_key)
dechiffre = rsa_decrypt(chiffre, priv_key)

print(f"Message clair : {message}")
print(f"Chiffré RSA   : {chiffre}")
print(f"Déchiffré RSA : {dechiffre}")

assert message == dechiffre, "Erreur de déchiffrement RSA !"
print("\nTest RSA validé avec succès !")