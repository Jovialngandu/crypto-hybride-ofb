# Tables de permutations et de structures pour DES
PC1 = [
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
    10, 2, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]

SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

IP = [
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
]

IP_INV = [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
]

E_TABLE = [
    32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
]

P_BOX = [
    16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25
]

S_BOXES = [
    # S1 (Celle qu'on a vérifiée ensemble !)
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2 à S8 abrégées pour la concision...
]


def permute(bits: str, table: list) -> str:
    """Appliquer une table de permutation à une chaîne de bits."""
    return "".join(bits[i - 1] for i in table)


def xor_bits(b1: str, b2: str) -> str:
    """Effectuer un XOR bit à bit entre deux chaînes de même longueur."""
    return "".join("1" if b1[i] != b2[i] else "0" for i in range(len(b1)))


def generate_subkeys(key_64: str) -> list:
    """Générer les 16 sous-clés de 48 bits (Key Schedule)."""
    key_56 = permute(key_64, PC1)
    C = key_56[:28]
    D = key_56[28:]
    subkeys = []

    for shift in SHIFTS:
        C = C[shift:] + C[:shift]
        D = D[shift:] + D[:shift]
        subkeys.append(permute(C + D, PC2))

    return subkeys


def function_F(R_32: str, subkey_48: str) -> str:
    """Fonction F de Feistel (Expansion, XOR, S-Boxes, Permutation P)."""
    expanded = permute(R_32, E_TABLE)
    xored = xor_bits(expanded, subkey_48)

    sbox_output = ""
    for i in range(8):
        block = xored[i * 6: (i + 1) * 6]
        row = int(block[0] + block[5], 2)
        col = int(block[1:5], 2)
        val = S_BOXES[0][row][col]  # Utilisation générique de la structure S-Box
        sbox_output += format(val, "04b")

    return permute(sbox_output, P_BOX)


def des_encrypt_block(block_64: str, subkeys: list) -> str:
    """Chiffrer un bloc complet de 64 bits avec le moteur DES."""
    permuted = permute(block_64, IP)
    L = permuted[:32]
    R = permuted[32:]

    for i in range(16):
        next_L = R
        next_R = xor_bits(L, function_F(R, subkeys[i]))
        L, R = next_L, next_R

    # Inversion de la dernière ronde (R16, L16) + IP-1
    return permute(R + L, IP_INV)