import sys
from pathlib import Path

# Ajustement du chemin pour les imports locaux
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.math_ops import extended_gcd, mod_inverse, mod_pow
from utils.helpers import generate_prime,get_safe_chunk_size


def generate_keypair(p: int = None, q: int = None, e: int = 65537) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Génère la clé publique (e, n) et la clé privée (d, n).
    Si p et q ne sont pas fournis, ils sont générés dynamiquement.
    """
    if p is None or q is None:
        p = generate_prime(100, 300)
        q = generate_prime(301, 600)
        while p == q:
            q = generate_prime(301, 600)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Vérification PGCD(e, phi(n)) == 1, adaptation de e si nécessaire
    gcd, _, _ = extended_gcd(e, phi_n)
    if gcd != 1:
        e = 3
        gcd, _, _ = extended_gcd(e, phi_n)
        while gcd != 1:
            e += 2
            gcd, _, _ = extended_gcd(e, phi_n)

    # Calcul de l'exposant privé d
    d = mod_inverse(e, phi_n)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key


def rsa_encrypt(message_num: int, public_key: tuple[int, int]) -> int:
    """
    Chiffrement RSA : C = M^e mod n.
    """
    e, n = public_key
    if message_num >= n:
        raise ValueError("Le message numérique doit être strictement inférieur au module n.")
    return mod_pow(message_num, e, n)


def rsa_decrypt(cipher_num: int, private_key: tuple[int, int]) -> int:
    """
    Déchiffrement RSA : M = C^d mod n.
    """
    d, n = private_key
    return mod_pow(cipher_num, d, n)


# --- SEGMENTATION ET CHUNKING (POUR LA CLÉ DES ET L'IV) ---


def encrypt_bits_chunked(bit_string: str, public_key: tuple[int, int]) -> list[int]:
    """
    Découpe une chaîne binaire (clé DES de 64 bits ou IV) en blocs stricts < n
    et chiffre chaque bloc avec rsa_encrypt.
    """
    _, n = public_key
    chunk_size = get_safe_chunk_size(n)
    encrypted_chunks = []

    for i in range(0, len(bit_string), chunk_size):
        chunk = bit_string[i:i + chunk_size]
        val = int(chunk, 2)
        c = rsa_encrypt(val, public_key)
        encrypted_chunks.append(c)

    return encrypted_chunks


def decrypt_bits_chunked(encrypted_chunks: list[int], private_key: tuple[int, int], original_length: int = 64) -> str:
    """
    Déchiffre la liste de blocs RSA avec rsa_decrypt et reconstruit la chaîne binaire d'origine.
    """
    _, n = private_key
    chunk_size = get_safe_chunk_size(n)
    bit_chunks = []

    num_chunks = len(encrypted_chunks)

    for idx, c in enumerate(encrypted_chunks):
        m = rsa_decrypt(c, private_key)

        # Taille attendue en bits pour préserver les 0 à gauche
        if idx == num_chunks - 1 and (original_length % chunk_size != 0):
            expected_bits = original_length % chunk_size
        else:
            expected_bits = chunk_size

        bin_str = format(m, f'0{expected_bits}b')
        bit_chunks.append(bin_str)

    return "".join(bit_chunks)