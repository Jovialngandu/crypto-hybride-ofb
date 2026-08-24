import secrets
import random


def generate_random_iv(length_bits: int = 64) -> str:
    """
    Génère un vecteur d'initialisation (IV) binaire aléatoire.
    Par défaut 64 bits pour DES.
    """
    # Génère un entier aléatoire sécurisé entre 0 et 2^64 - 1
    random_int = secrets.randbits(length_bits)
    # Formate l'entier en chaîne binaire sur 64 bits remplie de 0 à gauche
    return format(random_int, f'0{length_bits}b')

def is_prime(n: int) -> bool:
    """
    Vérifie si un nombre entier n est premier.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_prime(start: int = 100, end: int = 500) -> int:
    """
    Génère un nombre premier aléatoire dans l'intervalle donné.
    """
    primes = [n for n in range(start, end) if is_prime(n)]
    if not primes:
        raise ValueError("Aucun nombre premier trouvé dans l'intervalle spécifié.")
    return random.choice(primes)


def get_safe_chunk_size(n: int) -> int:
    """
    Calcule la taille maximale de bloc en bits (k bits) telle que 2^k < n.
    Garantit que chaque sous-bloc converti en entier reste strictement inférieur à n.
    """
    chunk_size = n.bit_length() - 1
    return max(1, chunk_size)