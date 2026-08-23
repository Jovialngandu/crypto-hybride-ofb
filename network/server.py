import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modes.ofb import decrypt_ofb

HOST = "0.0.0.0"  # Écoute sur toutes les interfaces réseau
PORT = 65432

# Clé DES partagée (en attendant l'échange RSA dynamique complet)
K_DES = "0100110001101111011001110110100101100011011010010110010101101100"

def start_server(chiffre: bool = True):
    mode_str = "CHIFFRÉ (DES-OFB avec IV Dynamique)" if chiffre else "EN CLAIR (SANS SÉCURITÉ)"
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
                    # Séparation de l'IV (64 bits binaires) et du ciphertext
                    if len(message_recu) < 64:
                        print("[!] Erreur : Paquet trop court pour contenir un IV de 64 bits.")
                        continue
                        
                    iv_dynamique = message_recu[:64]
                    ciphertext = message_recu[64:]
                    
                    clair = decrypt_ofb(ciphertext, iv_dynamique, K_DES)
                    print(f"[IV Extrait]          : {iv_dynamique}")
                    print(f"[Déchiffré Localement]: {clair}")
                else:
                    print(f"[Texte Brut]          : {message_recu}")

if __name__ == "__main__":
    # Passer False pour tester la communication en clair
    start_server(chiffre=True)