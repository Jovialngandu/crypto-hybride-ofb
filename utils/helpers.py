import secrets

def generate_random_iv(length_bits: int = 64) -> str:
    """
    Génère un vecteur d'initialisation (IV) binaire aléatoire.
    Par défaut 64 bits pour DES.
    """
    # Génère un entier aléatoire sécurisé entre 0 et 2^64 - 1
    random_int = secrets.randbits(length_bits)
    # Formate l'entier en chaîne binaire sur 64 bits remplie de 0 à gauche
    return format(random_int, f'0{length_bits}b')