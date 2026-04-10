import os
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from typing import Tuple, Dict, Any

KEYS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".keys")
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "private.pem")
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, "public.pem")

class EncryptionHelper:
    _private_key = None
    _public_key_pem = None

    @classmethod
    def init_keys(cls):
        try:
            if not os.path.exists(KEYS_DIR):
                os.makedirs(KEYS_DIR, mode=0o700)

            if not os.path.exists(PRIVATE_KEY_PATH):
                # Generate new RSA key pair
                private_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048
                )
                # Save private key
                with open(PRIVATE_KEY_PATH, "wb") as f:
                    f.write(private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption()
                    ))
                # Save public key
                public_key = private_key.public_key()
                with open(PUBLIC_KEY_PATH, "wb") as f:
                    f.write(public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    ))
                print("Generated new RSA key pair for E2EE.", flush=True)

            # Load keys into memory
            with open(PRIVATE_KEY_PATH, "rb") as f:
                cls._private_key = serialization.load_pem_private_key(f.read(), password=None)
            
            with open(PUBLIC_KEY_PATH, "rb") as f:
                cls._public_key_pem = f.read().decode('utf-8')
                
        except Exception as e:
            # If keys can't be loaded from files, generate in-memory
            print(f"WARNING: Could not load keys from disk ({e}), generating in-memory keys.", flush=True)
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            cls._private_key = private_key
            cls._public_key_pem = private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')

    @classmethod
    def get_public_key(cls) -> str:
        if not cls._public_key_pem:
            cls.init_keys()
        return cls._public_key_pem

    @classmethod
    def decrypt_symmetric_key(cls, encrypted_key_b64: str) -> bytes:
        if not cls._private_key:
            cls.init_keys()
        
        encrypted_key = base64.b64decode(encrypted_key_b64)
        symmetric_key = cls._private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return symmetric_key

    @classmethod
    def decrypt_data(cls, ciphertext_b64: str, symmetric_key: bytes, iv_b64: str, tag_b64: str) -> Dict[str, Any]:
        ciphertext = base64.b64decode(ciphertext_b64)
        iv = base64.b64decode(iv_b64)
        tag = base64.b64decode(tag_b64)
        
        aesgcm = AESGCM(symmetric_key)
        # AESGCM.decrypt expects ciphertext + tag combined or uses tag internally if available
        # In node-forge/standard AES-GCM, tag is often separate. 
        # Cryptography's AESGCM.decrypt expects the 16-byte tag to be appended to the ciphertext.
        decrypted_data = aesgcm.decrypt(iv, ciphertext + tag, None)
        return json.loads(decrypted_data.decode('utf-8'))

    @classmethod
    def encrypt_data(cls, data: Dict[str, Any], symmetric_key: bytes) -> Tuple[str, str, str]:
        iv = os.urandom(12)
        aesgcm = AESGCM(symmetric_key)
        plaintext = json.dumps(data).encode('utf-8')
        
        ciphertext_with_tag = aesgcm.encrypt(iv, plaintext, None)
        # Separate ciphertext and tag (tag is last 16 bytes)
        ciphertext = ciphertext_with_tag[:-16]
        tag = ciphertext_with_tag[-16:]
        
        return (
            base64.b64encode(ciphertext).decode('utf-8'),
            base64.b64encode(iv).decode('utf-8'),
            base64.b64encode(tag).decode('utf-8')
        )
    
    # Correction for base64 function name
    @classmethod
    def b64encode(cls, data: bytes) -> str:
        return base64.b64encode(data).decode('utf-8')

    @classmethod
    def serialize_data(cls, data: Dict[str, Any]) -> str:
        def default_handler(obj):
            import uuid
            from datetime import datetime
            if isinstance(obj, uuid.UUID):
                return str(obj)
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
        
        return json.dumps(data, default=default_handler)

    @classmethod
    def encrypt_response(cls, data: Dict[str, Any], symmetric_key: bytes) -> Dict[str, str]:
        iv = os.urandom(12)
        aesgcm = AESGCM(symmetric_key)
        plaintext = cls.serialize_data(data).encode('utf-8')
        
        ciphertext_with_tag = aesgcm.encrypt(iv, plaintext, None)
        ciphertext = ciphertext_with_tag[:-16]
        tag = ciphertext_with_tag[-16:]
        
        return {
            "ciphertext": cls.b64encode(ciphertext),
            "iv": cls.b64encode(iv),
            "tag": cls.b64encode(tag)
        }

# Pre-initialize keys on module load
try:
    EncryptionHelper.init_keys()
except Exception as e:
    print(f"WARNING: Encryption key init failed: {e}", flush=True)
