# Configuration de l'alphabet de 79 caractères
ALPHABET_79 = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    " .,'!?-+*/=():;\n\t"
)

# Vérification de sécurité
assert len(ALPHABET_79) == 79, f"L'alphabet doit contenir exactement 79 caractères (actuel : {len(ALPHABET_79)})"


def char_to_index(char: str) -> int:
    """Renvoyer l'indice (0-78) d'un caractère."""
    if char not in ALPHABET_79:
        raise ValueError(f"Caractère '{char}' non présent dans l'alphabet de 79 symboles.")
    return ALPHABET_79.index(char)


def index_to_char(index: int) -> str:
    """Renvoyer le caractère correspondant à un indice modulo 79."""
    return ALPHABET_79[index % 79]