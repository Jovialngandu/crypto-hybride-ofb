import socket
import sys
from pathlib import Path

# Fix chemin import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modes.ofb import encrypt_ofb, decrypt_ofb

HOST = "0.0.0.0"  # Écoute sur toutes les interfaces réseau
PORT = 65432

# Paramètres partagés (ou reçus)
K_DES = "0100110001101111011001110110100101100011011010010110010101101100"
IV = "0011000100110010001100110011010000110101001101100011011100111000"

def start_server(chiffre: bool = True):
    mode_str = "CHIFFRÉ (DES-OFB)" if chiffre else "EN CLAIR (SANS SÉCURITÉ)"
    print(f"=== SERVEUR DÉMARRÉ EN MODE : {mode_str} ===")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"[+] Connexion reçue de : {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                
                message_recu = data.decode('utf-8')
                print(f"\n[Réseau Brut Reçu] : {message_recu}")

                if chiffre:
                    clair = decrypt_ofb(message_recu, IV, K_DES)
                    print(f"[Déchiffré Localement] : {clair}")
                else:
                    print(f"[Texte Brut] : {message_recu}")

if __name__ == "__main__":
    # Passer False pour tester la communication sans chiffrement
    start_server(chiffre=False)