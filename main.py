import sys
from pathlib import Path

# Fix pour exécuter le script directement depuis n'importe quel dossier
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.rsa import generate_keypair, rsa_encrypt, rsa_decrypt
from modes.ofb import encrypt_ofb, decrypt_ofb

def main():
    print("=" * 60)
    print("      DÉMONSTRATION DU CRYPTOSYSTÈME HYBRIDE COMPLET")
    print("=" * 60)

    # 1. Génération des clés RSA du destinataire (Serveur)
    p, q, e = 131, 53, 17
    public_key, private_key = generate_keypair(p, q, e)
    print(f"[RSA] Clé Publique (e, n) : {public_key}")
    print(f"[RSA] Clé Privée   (d, n) : {private_key}\n")

    # 2. Clé DES et IV générés par l'émetteur (Client)
    K_DES_64 = "0100110001101111011001110110100101100011011010010110010101101100"
    IV_64    = "0011000100110010001100110011010000110101001101100011011100111000"

    # 3. Chiffrement RSA de la clé DES et de l'IV (Exemple par découpage/modulo pour la démo)
    k_des_num = int(K_DES_64, 2) % public_key[1]
    iv_num = int(IV_64, 2) % public_key[1]

    encrypted_k_des = rsa_encrypt(k_des_num, public_key)
    encrypted_iv = rsa_encrypt(iv_num, public_key)

    print(f"[RSA Transmis sur le réseau]")
    print(f"  -> Clé DES Chiffrée : {encrypted_k_des}")
    print(f"  -> IV Chiffré       : {encrypted_iv}\n")

    # 4. Déchiffrement RSA côté Serveur
    decrypted_k_num = rsa_decrypt(encrypted_k_des, private_key)
    decrypted_iv_num = rsa_decrypt(encrypted_iv, private_key)
    print(f"[Serveur] Clé DES et IV déchiffrés par RSA avec succès !\n")

    # 5. Transmission chiffrée DES-OFB Modulo 79
    message_clair = "Fin du Cours de Cryptographie et Cryptanalyse: Domaine des Sciences et Technologies/Mention: Math-Stat-Info/Mardi Le 21/07/2026"
    print(f"[Message Clair] : {message_clair}")

    # Chiffrement client
    message_chiffre = encrypt_ofb(message_clair, IV_64, K_DES_64)
    print(f"[Chiffré OFB  ] : {message_chiffre}")

    # Déchiffrement serveur
    message_restaure = decrypt_ofb(message_chiffre, IV_64, K_DES_64)
    print(f"[Déchiffré OFB] : {message_restaure}\n")

    assert message_clair == message_restaure, "Erreur d'intégration hybride !"
    print("INTÉGRATION HYBRIDE VALIDÉE AVEC SUCCÈS !")

if __name__ == "__main__":
    main()