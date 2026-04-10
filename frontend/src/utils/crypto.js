import forge from 'node-forge';
import axios from 'axios';

const PUBLIC_KEY_URL = '/auth/public-key';
let cachedPublicKey = null;

export const EncryptionService = {
    async getPublicKey() {
        if (cachedPublicKey) return cachedPublicKey;

        try {
            const resp = await axios.get(import.meta.env.VITE_API_BASE_URL + PUBLIC_KEY_URL);
            cachedPublicKey = forge.pki.publicKeyFromPem(resp.data.public_key);
            return cachedPublicKey;
        } catch (e) {
            console.error("Failed to fetch public key for encryption", e);
            throw e;
        }
    },

    /**
     * Encrypts a payload using Hybrid RSA + AES-GCM
     */
    async encrypt(payload) {
        const publicKey = await this.getPublicKey();

        // 1. Generate random AES-256 key (32 bytes) and IV (12 bytes)
        const symmetricKey = forge.random.getBytesSync(32);
        const iv = forge.random.getBytesSync(12);

        // 2. Encrypt the symmetric key with RSA-OAEP
        // Note: forge's RSA-OAEP defaults to SHA-1. Backend uses SHA-256.
        const encryptedKey = publicKey.encrypt(symmetricKey, 'RSA-OAEP', {
            md: forge.md.sha256.create(),
            mgf1: {
                md: forge.md.sha256.create()
            }
        });

        // 3. Encrypt payload with AES-GCM
        const cipher = forge.cipher.createCipher('AES-GCM', symmetricKey);
        cipher.start({ iv: iv });
        cipher.update(forge.util.createBuffer(JSON.stringify(payload), 'utf-8'));
        cipher.finish();

        const ciphertext = cipher.output.getBytes();
        const tag = cipher.mode.tag.getBytes();

        return {
            ciphertext: forge.util.encode64(ciphertext),
            encrypted_key: forge.util.encode64(encryptedKey),
            iv: forge.util.encode64(iv),
            tag: forge.util.encode64(tag),
            symmetric_key: forge.util.encode64(symmetricKey)
        };
    },

    /**
     * Decrypts a response if it's encrypted
     */
    async decrypt(encryptedResponse, symmetricKeyB64) {
        const symmetricKey = forge.util.decode64(symmetricKeyB64);
        const ciphertext = forge.util.decode64(encryptedResponse.ciphertext);
        const iv = forge.util.decode64(encryptedResponse.iv);
        const tag = forge.util.decode64(encryptedResponse.tag);

        const decipher = forge.cipher.createDecipher('AES-GCM', symmetricKey);
        decipher.start({
            iv: iv,
            tag: forge.util.createBuffer(tag)
        });
        decipher.update(forge.util.createBuffer(ciphertext));
        const pass = decipher.finish();

        if (!pass) {
            throw new Error("Decryption integrity check failed (invalid tag)");
        }

        return JSON.parse(decipher.output.toString('utf-8'));
    }
};
