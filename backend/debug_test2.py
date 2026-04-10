import asyncio
import httpx
import base64
import json
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

async def test_login():
    async with httpx.AsyncClient() as client:
        # Get public key
        resp = await client.get('http://localhost:8000/api/auth/public-key')
        pub_key_pem = resp.json()['public_key'].encode('utf-8')
        public_key = serialization.load_pem_public_key(pub_key_pem)

        # Generate symmetric key
        symmetric_key = AESGCM.generate_key(bit_length=256)
        
        # Encrypt symmetric key
        encrypted_sym_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Encrypt payload
        payload = {"phone": "9390999539", "password": "password"} # Try some known or unknown pass
        iv = os.urandom(12)
        aesgcm = AESGCM(symmetric_key)
        ciphertext_with_tag = aesgcm.encrypt(iv, json.dumps(payload).encode(), None)
        ciphertext = ciphertext_with_tag[:-16]
        tag = ciphertext_with_tag[-16:]
        
        req_body = {
            "encrypted_key": base64.b64encode(encrypted_sym_key).decode(),
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "iv": base64.b64encode(iv).decode(),
            "tag": base64.b64encode(tag).decode()
        }
        
        result = await client.post('http://localhost:8000/api/auth/login', json=req_body)
        print("STATUS:", result.status_code)
        print("RESPONSE:", result.text)

asyncio.run(test_login())
