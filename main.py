import sys
from pathlib import Path

# Fix pour exécuter le script directement depuis n'importe quel dossier
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.rsa import (
    generate_keypair, 
    encrypt_bits_chunked, 
    decrypt_bits_chunked
)
from modes.ofb import encrypt_ofb, decrypt_ofb
from utils.helpers import generate_random_iv


def main():
    print("=" * 60)
    print("      DÉMONSTRATION DU CRYPTOSYSTÈME HYBRIDE COMPLET")
    print("=" * 60)

    # 1. Génération dynamique des clés RSA du destinataire (Serveur)
    # (Si p et q ne sont pas fournis, generate_keypair les génère dynamiquement)
    public_key, private_key = generate_keypair()
    print(f"[RSA] Clé Publique (e, n) : {public_key}")
    print(f"[RSA] Clé Privée   (d, n) : {private_key}\n")

    # 2. Clé DES (64 bits) et IV (64 bits) générés aléatoirement par l'émetteur (Client)
    K_DES_64 = generate_random_iv(64)  # Réutilisation de generate_random_iv pour la clé DES
    IV_64    = generate_random_iv(64)
    #K_DES_64 = "0100110001101111011001110110100101100011011010010110010101101100"
    #IV_64    = "0011000100110010001100110011010000110101001101100011011100111000"

    print(f"[Client] Clé DES générée : {K_DES_64}")
    print(f"[Client] IV généré       : {IV_64}\n")

    # 3. Chiffrement RSA par segmentation (chunking) de la clé DES et de l'IV
    encrypted_k_des_chunks = encrypt_bits_chunked(K_DES_64, public_key)
    encrypted_iv_chunks    = encrypt_bits_chunked(IV_64, public_key)

    print(f"[RSA Transmis sur le réseau]")
    print(f"  -> Clé DES Chiffrée (blocs RSA) : {encrypted_k_des_chunks}")
    # print(f"  -> IV Chiffré       (blocs RSA) : {encrypted_iv_chunks}\n")

    # 4. Déchiffrement RSA côté Serveur pour reconstituer K_DES et IV
    decrypted_k_des = decrypt_bits_chunked(encrypted_k_des_chunks, private_key, original_length=64)
    decrypted_iv    = decrypt_bits_chunked(encrypted_iv_chunks, private_key, original_length=64)

    print(f"[Serveur] Clé DES déchiffrée : {decrypted_k_des}")
    # print(f"[Serveur] IV déchiffré       : {decrypted_iv}")
    
    assert K_DES_64 == decrypted_k_des, "Erreur : La clé DES déchiffrée ne correspond pas à l'originale !"
    assert IV_64 == decrypted_iv, "Erreur : L'IV déchiffré ne correspond pas à l'original !"
    # print("[Serveur] Clé DES et IV déchiffrés par RSA avec succès !\n")

    # 5. Chiffrement et Transmission du message avec DES-OFB
    message_clair = "Fin du Cours de Cryptographie et Cryptanalyse: Domaine des Sciences et Technologies/Mention: Math-Stat-Info/Mardi Le 21/07/2026"
    print(f"[Message Clair] : {message_clair}")

    # Chiffrement par le client avec sa clé DES et son IV d'origine
    message_chiffre = encrypt_ofb(message_clair, IV_64, K_DES_64)
    print(f"[Chiffré OFB  ] : {message_chiffre}")

    # Déchiffrement par le serveur avec la clé DES et l'IV QU'IL A DÉCHIFFRÉS par RSA
    message_restaure = decrypt_ofb(message_chiffre, decrypted_iv, decrypted_k_des)
    print(f"[Déchiffré OFB] : {message_restaure}\n")

    assert message_clair == message_restaure, "Erreur d'intégration hybride !"
    print("=" * 60)
    print("INTÉGRATION HYBRIDE VALIDÉE AVEC SUCCÈS !")
    print("=" * 60)


if __name__ == "__main__":
    main()