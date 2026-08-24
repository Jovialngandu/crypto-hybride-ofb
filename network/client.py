import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.rsa import encrypt_bits_chunked
from modes.ofb import encrypt_ofb
from utils.helpers import generate_random_iv
from network.config import SERVER_IP, PORT, BUFFER_SIZE, ENABLE_ENCRYPTION, FIXED_IV_MODE
from network.helpers import get_current_iv, serialize_packet, deserialize_packet

def start_client():
    mode_str = "CHIFFRÉ (RSA + DES-OFB)" if ENABLE_ENCRYPTION else "EN CLAIR (INSÉCURISÉ)"
    iv_str = "FIXE (Vulnérable)" if FIXED_IV_MODE else "DYNAMIQUE (Aléatoire)"

    print("=" * 65)
    print(f"  CLIENT MESSAGERIE - MODE : {mode_str}")
    if ENABLE_ENCRYPTION:
        print(f"  GESTION DES IV   : {iv_str}")
    print("=" * 65)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"[*] Connexion au serveur {SERVER_IP}:{PORT}...")
        s.connect((SERVER_IP, PORT))
        print("[+] Connecté !")

        k_des_session = None

        if ENABLE_ENCRYPTION:
            # 1. Réception de la clé publique RSA du serveur
            pub_data = deserialize_packet(s.recv(BUFFER_SIZE))
            public_key = (pub_data["e"], pub_data["n"])

            # 2. Génération unique de la clé DES et envoi RSA au serveur
            k_des_session = generate_random_iv(64)
            encrypted_k_des = encrypt_bits_chunked(k_des_session, public_key)
            s.sendall(serialize_packet({"encrypted_k_des": encrypted_k_des}))
            print("[RSA Handshake] Clé DES transmise de façon sécurisée !\n")

        while True:
            msg = input("\nMessage à envoyer (ou 'exit') : ")
            if msg.lower() == 'exit':
                break
            if not msg.strip():
                continue

            if ENABLE_ENCRYPTION:
                # Sélection dynamique ou fixe de l'IV
                current_iv = get_current_iv()
                ciphertext = encrypt_ofb(msg, current_iv, k_des_session)
                
                packet = serialize_packet({
                    "iv": current_iv,
                    "ciphertext": ciphertext
                })
            else:
                # Transmis en clair
                packet = msg.encode('utf-8')

            s.sendall(packet)
            print("[+] Message envoyé sur le réseau !")

if __name__ == "__main__":
    start_client()