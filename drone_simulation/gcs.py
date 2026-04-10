from Crypto.Cipher import ChaCha20_Poly1305

class GCS:
    def __init__(self):
        self.session_key = None
        self.frames_received = 0

    def receive_session_key(self, key):
        self.session_key = key
        print(f"[GCS] Clé de session reçue ✓")

    def receive_frame(self, nonce, ciphertext, tag):
        try:
            cipher = ChaCha20_Poly1305.new(key=self.session_key, nonce=nonce)
            frame = cipher.decrypt_and_verify(ciphertext, tag)
            self.frames_received += 1
            print(f"[GCS] Trame déchiffrée : {frame.decode()}")
        except Exception as e:
            print(f"[GCS] Erreur déchiffrement : {e}")

if __name__ == "__main__":
    import os
    from Crypto.Cipher import ChaCha20_Poly1305

    key = os.urandom(32)
    gcs = GCS()
    gcs.receive_session_key(key)

    nonce = os.urandom(12)
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(b"frame_test")

    gcs.receive_frame(nonce, ciphertext, tag)
