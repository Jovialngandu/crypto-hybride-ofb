def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Algorithme d'Euclide étendu.
    Renvoie (pgcd, x, y) tel que a*x + b*y = pgcd(a, b).
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(e: int, phi: int) -> int:
    """
    Calcule l'inverse modulaire : d = e^-1 mod phi.
    """
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("L'exposant e et phi(n) ne sont pas premiers entre eux !")
    return x % phi


def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Exponentiation modulaire rapide : (base^exp) % mod.
    """
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result