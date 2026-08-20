from core.des import des_encrypt_block, generate_subkeys
from mapping.alphabet import char_to_index, index_to_char


def encrypt_ofb(plaintext: str, IV_64: str, K_des_64: str) -> str:
    """
    Chiffrer un texte en utilisant DES en mode OFB avec le modulo 79.
    """
    subkeys = generate_subkeys(K_des_64)
    current_input = IV_64
    ciphertext = ""

    for char in plaintext:
        # 1. Génération du bloc O_i via DES(IV)
        O_i = des_encrypt_block(current_input, subkeys)

        # 2. Rétroaction pour le tour suivant
        current_input = O_i

        # 3. Extraction de la clé k_i = O_i mod 79
        k_i = int(O_i, 2) % 79

        # 4. Chiffrement : C_i = (P_i + k_i) mod 79
        P_i = char_to_index(char)
        C_i = (P_i + k_i) % 79
        ciphertext += index_to_char(C_i)

    return ciphertext


def decrypt_ofb(ciphertext: str, IV_64: str, K_des_64: str) -> str:
    """
    Déchiffrer un texte en utilisant DES en mode OFB avec le modulo 79.
    Note : On utilise STRICTEMENT la fonction de chiffrement de DES !
    """
    subkeys = generate_subkeys(K_des_64)
    current_input = IV_64
    plaintext = ""

    for char in ciphertext:
        # 1. Génération de la MÊME suite de blocs O_i
        O_i = des_encrypt_block(current_input, subkeys)
        current_input = O_i

        # 2. Extraction de k_i = O_i mod 79
        k_i = int(O_i, 2) % 79

        # 3. Déchiffrement : P_i = (C_i - k_i) mod 79
        C_i = char_to_index(char)
        P_i = (C_i - k_i) % 79
        plaintext += index_to_char(P_i)

    return plaintext