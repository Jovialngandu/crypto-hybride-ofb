# network/config.py
SERVER_IP = "127.0.0.1"  # Remplace par l'IP réseau (ex: "192.168.1.50") pour tester sur 2 machines
PORT = 65432
BUFFER_SIZE = 4096

# --- OPTIONS DE SÉCURITÉ ET DÉMO WIRESHARK ---
ENABLE_ENCRYPTION = True     # True = RSA + DES-OFB | False = Envoi du texte en clair brut

# --- OPTIONS DE CRYPTANALYSE (RÉUTILISATION D'IV) ---
FIXED_IV_MODE = False        # True = Utilise FIXED_IV pour TOUS les messages (Vulnérabilité OFB)
                             # False = Génère un IV aléatoire unique par message (Sécurisé)

FIXED_IV = "0011000100110010001100110011010000110101001101100011011100111000"  # 64 bits