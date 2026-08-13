import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class AESGCMCrypto:
    def __init__(self, secret_key: bytes = None):
        # Clé de 32 octets (AES-256) depuis la variable d'environnement ou générée
        key_env = os.getenv("CRYPTO_SECRET_KEY")
        if key_env:
            self.key = base64.b64decode(key_env)
        elif secret_key:
            self.key = secret_key
        else:
            # Clé par défaut pour le dev (32 octets)
            self.key = b'12345678901234567890123456789012'
        
        self.aesgcm = AESGCM(self.key)

    def encrypt(self, plain_text: str):
        # IV unique de 12 octets pour AES-GCM
        iv = os.urandom(12)
        cipher_bytes = self.aesgcm.encrypt(iv, plain_text.encode('utf-8'), None)
        
        cipher_b64 = base64.b64encode(cipher_bytes).decode('utf-8')
        iv_b64 = base64.b64encode(iv).decode('utf-8')
        
        return cipher_b64, iv_b64

    def decrypt(self, cipher_b64: str, iv_b64: str) -> str:
        cipher_bytes = base64.b64decode(cipher_b64)
        iv = base64.b64decode(iv_b64)
        
        plain_bytes = self.aesgcm.decrypt(iv, cipher_bytes, None)
        return plain_bytes.decode('utf-8')