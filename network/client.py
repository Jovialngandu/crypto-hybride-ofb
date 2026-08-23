import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modes.ofb import encrypt_ofb

SERVER_IP = "127.0.0.1"  # Remplace par l'IP du 2ème PC
PORT = 65432
K_DES = "0100110001101111011001110110100101100011011010010110010101101100"
    
from utils.helpers import generate_random_iv
from modes.ofb import encrypt_ofb

def start_client(chiffre: bool = True):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        print("[+] Connecté au serveur !")
        
        while True:
            msg = input("Message à envoyer (ou 'exit') : ")
            if msg.lower() == 'exit':
                break
                
            if chiffre:
                # Génération dynamique d'un IV unique par message
                current_iv = generate_random_iv(64)
                ciphertext = encrypt_ofb(msg, current_iv, K_DES)
                
                # Format du paquet : [IV sur 64 bits (64 chars)] + [Ciphertext]
                a_envoyer = current_iv + ciphertext
            else:
                a_envoyer = msg
                
            s.sendall(a_envoyer.encode('utf-8'))

if __name__ == "__main__":
    start_client(chiffre=True)