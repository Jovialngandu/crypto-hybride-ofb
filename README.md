# 🔒 Cryptosystème Hybride (DES + RSA) - Mode OFB

Implémentation complète d'un cryptosystème hybride combinant RSA, DES et le mode OFB (modulo 79) en Python, *from scratch* (sans bibliothèques cryptographiques externes).

---

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
                    |   - RSA : Échange/Chiffrement de la Clé DES et IV           |
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

---

## 📂 Arborescence du Projet

```text
crypto-hybride-ofb/
├── main.py                   # Orchestration globale du cryptosystème hybride
├── requirements.txt          # Aucune dépendance tierce (Standard Library uniquement)
├── mapping/
│   └── alphabet.py           # Alphabet de 79 caractères et fonctions de mapping
├── utils/
│   ├── math_ops.py           # Outils arithmétiques (Euclide étendu, mod_pow, mod_inverse)
│   └── helpers.py            # Génération d'IV aléatoires et conversion de bits
├── core/
│   ├── des.py                # Moteur symétrique DES 64 bits (IP, S-Boxes 1-8, Feistel)
│   └── rsa.py                # Moteur asymétrique RSA (Génération de clés, Chiffrement)
├── modes/
│   └── ofb.py                # Mode opératoire OFB & Chiffrement/Déchiffrement Modulo 79
├── network/
│   ├── config.py             # Configuration du serveur/client TCP (IP, Port)
│   ├── server.py             # Serveur TCP récepteur avec déchiffrement dynamique
│   └── client.py             # Client TCP émetteur avec génération d'IV dynamique
└── tests/
    ├── test_ofb.py           # Tests unitaires du moteur DES-OFB Modulo 79
    └── test_rsa.py           # Tests unitaires du module RSA
```

---

## 🛠️ Responsabilité des Modules

### 1. `utils/` (Arithmétique & Helpers)
*   **`math_ops.py`** : Euclide étendu (`extended_gcd`), inverse modulaire (`mod_inverse`) et exponentiation rapide (`mod_pow`).
*   **`helpers.py`** : Génération sécurisée d'IV aléatoire 64-bit (`generate_random_iv`).

### 2. `core/` (Moteurs Cryptographiques)
*   **`des.py`** : Implémentation complète de la norme FIPS PUB 46-3 (PC1, PC2, IP, 16 rondes de Feistel, 8 S-Boxes officielles, P-Box).
*   **`rsa.py`** : Génération de paires de clés $(e, n)$ et $(d, n)$, chiffrement $C = M^e \pmod n$ et déchiffrement $M = C^d \pmod n$.

### 3. `mapping/` & `modes/`
*   **`alphabet.py`** : Définition de l'espace de travail à 79 symboles et conversions bijectives char ↔ index.
*   **`ofb.py`** : Génération du Keystream $O_i = \text{DES}(O_{i-1}, K)$ et chiffrement/déchiffrement par addition/soustraction modulo 79.

### 4. `network/` (Communication Réseau Socket TCP)
*   **`server.py`** : Reçoit le paquet, extrait les 64 bits d'IV dynamique et déchiffre le message.
*   **`client.py`** : Génère un IV unique par message, chiffre le texte clair et transmet la trame `[IV_64] + [Ciphertext]`.

---

## 🚀 Guide d'Exécution

Aucune installation de paquet externe n'est requise. Le projet utilise exclusivement la bibliothèque standard de Python 3.

### 1. Exécuter les tests unitaires
Pour vérifier le bon fonctionnement des modules RSA et DES-OFB :
```bash
python -m unittest discover test/
```

### 2. Lancer la démonstration complète (Orchestration Hybride)
Pour exécuter le scénario d'échange de clés RSA et de chiffrement/déchiffrement DES-OFB en local :
```bash
python main.py
```

### 3. Tester la communication Client/Serveur TCP avec IV Dynamique
Ouvre deux terminaux séparés dans le dossier racine du projet :

*   **Terminal 1 (Lancer le Serveur) :**
    ```bash
    python -m network.server
    ```
*   **Terminal 2 (Lancer le Client) :**
    ```bash
    python -m network.client
    ```
