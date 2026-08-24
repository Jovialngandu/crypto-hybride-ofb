# network/helpers.py
import json
from network.config import FIXED_IV_MODE, FIXED_IV
from utils.helpers import generate_random_iv

def get_current_iv() -> str:
    """Retourne l'IV approprié selon la configuration activée."""
    if FIXED_IV_MODE:
        return FIXED_IV
    return generate_random_iv(64)

def serialize_packet(data_dict: dict) -> bytes:
    """Encode un dictionnaire Python en binaire JSON pour le réseau."""
    return json.dumps(data_dict).encode('utf-8')

def deserialize_packet(data_bytes: bytes) -> dict:
    """Décode les données réseau binaires en dictionnaire Python."""
    return json.loads(data_bytes.decode('utf-8'))