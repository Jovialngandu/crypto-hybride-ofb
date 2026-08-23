# 🔒 Cryptosystème Hybride (DES + RSA) - Mode OFB

Implémentation complète d'un cryptosystème hybride combinant RSA, DES et le mode OFB (modulo 79) en Python, *from scratch*.

## 🗺️ Diagramme d'Architecture (Flux de Données)

```text
					+-------------------------------------------------------------+
					
					|                     COUCHE APPLICATION                      |
					|       (Gestion des entrées/sorties, CLI ou Interface, I/O)  |
					+-------------------------------------------------------------+
					                               |
					                               v
					+-------------------------------------------------------------+
					
					|                       COUCHE HYBRIDE                        |
					|   - RSA : Échange/Chiffrement de la Clé DES et IV          |
					|   - Mode OFB : Génération du flux de clés (Keystream)       |
					|   - Modulo 79 : Mapping Alphabétique Character-by-Char      |
					+-------------------------------------------------------------+
					                               |
					                               v
					+-------------------------------------------------------------+
					
					|                     MOTEUR DES (64-bit)                     |
					|   - Key Schedule (PC1, Shifts, PC2 -> K1..K16)              |
					|   - Permutation IP / IP-1                                   |
					|   - Fonction F (Expansion E, XOR, S-Boxes 1..8, Perm P)     |
					+-------------------------------------------------------------+
					                               |
					                               v
					+-------------------------------------------------------------+
					
					|                 BOÎTE À OUTILS MATHÉMATIQUES                |
					|   - Euclide Étendu (Inverse Modulaire)                      |
					|   - Exponentiation Modulaire Rapide                         |
					|   - Utilitaires de conversion (Bitwise, XOR, Offsets)       |
					+-------------------------------------------------------------+
```

## 📂 Arborescence du Projet

```text
crypto-hybride-ofb/
├── main.py                   # Point d'entrée principal (Orchestration hybride)
├── requirements.txt          # Fichier vide (Utilise uniquement la bibliothèque standard Python)
├── mapping/
│   └── alphabet.py           # Table de correspondance de l'alphabet à 79 caractères
├── utils/
│   └── math_ops.py           # Outils mathématiques (Euclide étendu, mod_pow, mod_inverse)
├── core/
│   ├── des.py                # Moteur symétrique DES 64 bits (IP, S-Boxes, Feistel, IP⁻¹)
│   └── rsa.py                # Moteur asymétrique RSA (Génération de clés, Chiffrement Mᵉ mod n)
├── modes/
│   └── ofb.py                # Mode opératoire OFB & Chiffrement/Déchiffrement Modulo 79
├── network/
│   ├── config.py             # Configuration réseau (IP, Ports, Tailles de buffer)
│   ├── server.py             # Serveur Socket TCP (Déchiffrement local & écoute)
│   └── client.py             # Client Socket TCP (Chiffrement & transmission)
└── tests/
    ├── test_ofb.py           # Tests unitaires pour le moteur DES-OFB Modulo 79
    └── test_rsa.py           # Tests unitaires pour le module RSA
```

## 🛠️ Responsabilité de Chaque Module

### 1. `utils/math_ops.py` (Boîte à outils mathématiques)
* **`extended_gcd(a, b)` :** Algorithme d'Euclide étendu (renvoie PGCD, $x$, $y$).
* **`mod_inverse(e, phi)` :** Calcul de l'exposant privé $d = e^{-1} \pmod{\phi(n)}$.
* **`mod_pow(base, exp, mod)` :** Exponentiation modulaire rapide pour $M^e \pmod n$ et $C^d \pmod n$.
* **`bitwise_xor(bits1, bits2)` :** Opération XOR bit à bit sur des listes ou chaînes de bits.

### 2. `core/des.py` (Moteur DES 64-bit)
* **`PC1, PC2, IP, IP_INV, E_TABLE, P_BOX, S_BOXES` :** Tables de constantes officielles.
* **`key_schedule(K_64)` :** Génération des 16 sous-clés de 48 bits ($K_1 \dots K_{16}$).
* **`function_F(R_32, K_sub_48)` :** Élargissement $E$, XOR avec sous-clé, passage dans les 8 S-Boxes, permutation $P$.
* **`des_encrypt_block(block_64, subkeys)` :** Permutation $IP \rightarrow 16 \text{ rondes de Feistel} \rightarrow IP^{-1}$.

### 3. `core/rsa.py` (Moteur RSA)
* **`generate_keypair(p, q, e)` :** Calcul de $n = p \times q$, $\phi(n) = (p-1)(q-1)$ et vérification $\text{PGCD}(e, \phi(n)) = 1$.
* **`rsa_encrypt(M, e, n)` :** Chiffrement de la clé/IV symétrique ($C = M^e \pmod n$).
* **`rsa_decrypt(C, d, n)` :** Déchiffrement de la clé/IV symétrique ($M = C^d \pmod n$).

### 4. `mapping/alphabet.py` (Table Modulo 79)
* **`ALPHABET_79` :** Chaîne ou liste contenant exactement tes 79 caractères autorisés.
* **`char_to_index(char)` :** Convertit une lettre en son indice $P_i \in [0, 78]$.
* **`index_to_char(index)` :** Convertit un indice $C_i \in [0, 78]$ en lettre.

### 5. `modes/ofb.py` (Mode Output Feedback)
* **`generate_keystream(IV, K_des, length)` :** Calcule $O_1 = \text{DES}(IV, K_{\text{des}})$, $O_2 = \text{DES}(O_1, K_{\text{des}})$, etc. Extrait pour chaque tour $k_i = O_i \pmod{79}$.
* **`encrypt_ofb(plaintext, IV, K_des)` :** Applique $(P_i + k_i) \pmod{79}$.
* **`decrypt_ofb(ciphertext, IV, K_des)` :** Applique $(C_i - k_i) \pmod{79}$.

### 6. `main.py` (Point d'entrée principal)
* Orchestre l'ensemble du flux de chiffrement et de déchiffrement en faisant le lien entre l'utilisateur et les différentes couches du système.
