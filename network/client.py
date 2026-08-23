import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modes.ofb import encrypt_ofb

SERVER_IP = "127.0.0.1"  # Remplace par l'IP du 2ème PC
PORT = 65432

K_DES = "0100110001101111011001110110100101100011011010010110010101101100"
IV = "0011000100110010001100110011010000110101001101100011011100111000"

def start_client(chiffre: bool = True):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        print("[+] Connecté au serveur !")
        
        while True:
            msg = input("Message à envoyer (ou 'exit') : ")
            if msg.lower() == 'exit':
                break
                
            if chiffre:
                a_envoyer = encrypt_ofb(msg, IV, K_DES)
            else:
                a_envoyer = msg
                
            s.sendall(a_envoyer.encode('utf-8'))

if __name__ == "__main__":
    start_client(chiffre=False)