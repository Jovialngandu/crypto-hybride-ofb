import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.rsa import generate_keypair, decrypt_bits_chunked
from modes.ofb import decrypt_ofb
from network.config import SERVER_IP, PORT, BUFFER_SIZE, ENABLE_ENCRYPTION, FIXED_IV_MODE
from network.helpers import serialize_packet, deserialize_packet

HOST = "0.0.0.0"

def start_server():
    mode_str = "CHIFFRE (RSA + DES-OFB)" if ENABLE_ENCRYPTION else "EN CLAIR (INSÉCURISÉ)"
    iv_str = "FIXE (Vulnérable Cryptanalyse)" if FIXED_IV_MODE else "DYNAMIQUE (Sécurisé)"
    
    print("=" * 65)
    print(f"  SERVEUR MESSAGERIE - MODE : {mode_str}")
    if ENABLE_ENCRYPTION:
        print(f"  GESTION DES IV    : {iv_str}")
    print("=" * 65)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] Serveur en écoute sur {HOST}:{PORT}...")

        conn, addr = s.accept()
        with conn:
            print(f"[+] Connexion reçue de : {addr}")

            k_des_session = None

            if ENABLE_ENCRYPTION:
                # 1. Génération RSA et Envoi Clé Publique
                public_key, private_key = generate_keypair()
                conn.sendall(serialize_packet({"e": public_key[0], "n": public_key[1]}))

                # 2. Reception et Déchiffrement RSA de K_DES
                raw_hs = conn.recv(BUFFER_SIZE)
                hs_payload = deserialize_packet(raw_hs)
                k_des_session = decrypt_bits_chunked(hs_payload["encrypted_k_des"], private_key, original_length=64)
                print(f"[RSA Handshake] Clé DES de session établie : {k_des_session}\n")

            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    print("[-] Client déconnecté.")
                    break

                if ENABLE_ENCRYPTION:
                    payload = deserialize_packet(data)
                    iv = payload["iv"]
                    ciphertext = payload["ciphertext"]
                    clair = decrypt_ofb(ciphertext, iv, k_des_session)

                    print(f"\n[Réseau Brut (Wireshark)] : {data.decode('utf-8')}")
                    print(f"[IV Extrait]              : {iv}")
                    print(f"[Ciphertext DES-OFB]      : {ciphertext}")
                    print(f"[Déchiffré Localement]    : {clair}")
                else:
                    # Traitement en clair (Visible à 100% sur Wireshark)
                    print(f"\n[Réseau Brut Reçu (Wireshark)] : {data.decode('utf-8')}")

if __name__ == "__main__":
    start_server()