import sys
from pathlib import Path

# Ajustement du chemin pour les imports locaux
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.math_ops import extended_gcd, mod_inverse, mod_pow


def generate_keypair(p: int, q: int, e: int = 65537) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Génère la clé publique (e, n) et la clé privée (d, n).
    """
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Vérification PGCD(e, phi(n)) == 1
    gcd, _, _ = extended_gcd(e, phi_n)
    if gcd != 1:
        raise ValueError(f"e={e} n'est pas premier avec phi(n)={phi_n}")

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