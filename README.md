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
                    |   - Handshake RSA : Échange unique de la Clé DES de session |
                    |   - Mode OFB  : Génération du flux de clés (Keystream)      |
                    |   - Modulo 79 : Mapping Alphabétique Character-by-Char     |
                    +-------------------------------------------------------------+
                                                   |
                                                   v
                    +-------------------------------------------------------------+

                    |                COUCHE RÉSEAU (SOCKETS TCP)                  |
                    |   - config.py   : Switch Chiffré/Clair & IV Fixe/Dynamique  |
                    |   - helpers.py  : Sérialisation JSON & Gestion des IV       |
                    |   - Server/Client TCP : Protocoles Handshake & Transmissions|
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
├── main.py                   # Orchestration globale du cryptosystème hybride local
├── README.md                 # Documentation du projet
├── requirements.txt          # Aucune dépendance tierce (Standard Library uniquement)
├── mapping/
│   └── alphabet.py           # Alphabet de 79 caractères et fonctions de mapping
├── utils/
│   ├── math_ops.py           # Outils arithmétiques (Euclide étendu, mod_pow, mod_inverse)
│   └── helpers.py            # Génération d'IV/Clés aléatoires et conversions de bits
├── core/
│   ├── des.py                # Moteur symétrique DES 64 bits (IP, S-Boxes 1-8, Feistel)
│   └── rsa.py                # Moteur asymétrique RSA (Clés, Chiffrement par blocs/bits)
├── modes/
│   └── ofb.py                # Mode opératoire OFB & Chiffrement/Déchiffrement Modulo 79
├── network/
│   ├── config.py             # Configuration centrale (Switch Sécurité, IP, Port, IV Fixe)
│   ├── helpers.py            # Helpers réseau (Sérialisation JSON, injection d'IV)
│   ├── server.py             # Serveur TCP (Handshake RSA + Réception DES-OFB / Clair)
│   └── client.py             # Client TCP (Handshake RSA + Émission DES-OFB / Clair)
└── tests/
    ├── test_ofb.py           # Tests unitaires du moteur DES-OFB Modulo 79
    └── test_rsa.py           # Tests unitaires du module RSA
```

---

## 🛠️ Responsabilité des Modules

### 1. `utils/` (Arithmétique & Helpers)
* **`math_ops.py` :** Euclide étendu (`extended_gcd`), inverse modulaire (`mod_inverse`) et exponentiation rapide (`mod_pow`).
* **`helpers.py` :** Génération d'IV/Clés 64 bits aléatoires (`generate_random_iv`), manipulation et conversions bitwise/ASCII.

### 2. `core/` (Moteurs Cryptographiques)
* **`des.py` :** Implémentation complète de la norme FIPS PUB 46-3 (PC1, PC2, IP, 16 rondes de Feistel, 8 S-Boxes officielles, P-Box).
* **`rsa.py` :** Génération de paires de clés $(e, n)$ et $(d, n)$, chiffrement/déchiffrement RSA avec gestion du découpage par blocs de bits (`encrypt_bits_chunked`, `decrypt_bits_chunked`).

### 3. `mapping/` & `modes/`
* **`alphabet.py` :** Définition de l'espace de travail à 79 symboles et conversions bijectives char ↔ index.
* **`ofb.py` :** Génération du Keystream $O_i = \text{DES}(O_{i-1}, K)$ et chiffrement/déchiffrement par addition/soustraction modulo 79.

### 4. `network/` (Communication Réseau Socket TCP)
* **`config.py` :** Point de contrôle unique des paramètres réseau et de sécurité :
  * `ENABLE_ENCRYPTION` : Active ou désactive le chiffrement (pour démonstration Wireshark).
  * `FIXED_IV_MODE` & `FIXED_IV` : Permet la réutilisation d'un même IV (pour démonstration de cryptanalyse).
  * `SERVER_IP`, `PORT`, `BUFFER_SIZE` : Configuration des sockets TCP.
* **`helpers.py` :** Fonctions d'aide réseau pour la sérialisation/désérialisation JSON et la sélection dynamique/fixe de l'IV.
* **`server.py` :**
  * *En mode chiffré :* Génère sa paire RSA, transmet la clé publique, reçoit la clé DES chiffrée (Handshake unique), puis déchiffre les messages en DES-OFB.
  * *En mode clair :* Reçoit directement le texte brut.
* **`client.py` :**
  * *En mode chiffré :* Récupère la clé publique RSA du serveur, génère la clé DES de session, l'envoie chiffrée avec RSA, puis transmet les messages chiffrés en DES-OFB avec leur IV.
  * *En mode clair :* Transmet directement le texte brut.

---

## 🚀 Guide d'Exécution & Scénarios de Démo

Aucune installation de paquet externe n'est requise.

### 1. Exécuter les tests unitaires
```bash
python -m unittest discover tests/
```

### 2. Lancer la démonstration hybride en local (Sans Réseau)
```bash
python main.py
```

### 3. Utiliser la Messagerie Réseau (Client / Serveur TCP)
Ouvre deux terminaux séparés à la racine du projet :

* **Terminal 1 (Lancer le Serveur) :**
  ```bash
  python -m network.server
  ```
* **Terminal 2 (Lancer le Client) :**
  ```bash
  python -m network.client
  ```

---

## 🧪 Scénarios de Démonstration (Wireshark & Cryptanalyse)

Tous les scénarios se configurent dans `network/config.py` :

### Scénario A : Interception de flux en clair (Démo Wireshark)
1. Dans `network/config.py`, règle : `ENABLE_ENCRYPTION = False`
2. Lance le serveur et le client, puis envoie un message.
3. *Analyse Wireshark :* Le texte est parfaitement lisible en ASCII dans la capture de paquets TCP sur le port 65432.

### Scénario B : Communication sécurisée Hybride (Mode Normal)
1. Dans `network/config.py`, règle : `ENABLE_ENCRYPTION = True` et `FIXED_IV_MODE = False`
2. Le serveur et le client négocient la clé DES via RSA lors du Handshake.
3. Chaque message utilise un nouvel IV aléatoire transmis en clair avec le texte chiffré DES-OFB.
4. *Analyse Wireshark :* Les paquets réseau ne contiennent que des structures JSON chiffrées inintelligibles.

### Scénario C : Vulnérabilité par Réutilisation d'IV (Cryptanalyse OFB)
1. Dans `network/config.py`, règle : `ENABLE_ENCRYPTION = True` et `FIXED_IV_MODE = True`
2. Envoie deux fois le même message (ex: "Bonjour").
3. *Constat :* Les deux paquets chiffrés générés sur le réseau sont rigoureusement identiques, ce qui permet à un attaquant de détecter la répétition de messages et d'effectuer une attaque par XOR ($C_1 \oplus C_2 = P_1 \oplus P_2$).
