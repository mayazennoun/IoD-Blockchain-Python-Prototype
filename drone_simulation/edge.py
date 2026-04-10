import os
import time
from blockchain import is_authorized, register_drone

class EdgeNode:
    def __init__(self):
        self.session_keys = {}  
        self.gcs = None

    def set_gcs(self, gcs):
        self.gcs = gcs

    def authenticate_drone(self, request):
        drone_id = request["drone_id"]
        print(f"[Edge] Demande reçue de {drone_id}")
        print(f"[Edge] Vérification sur la blockchain...")

        time.sleep(0.1)

        authorized = is_authorized(drone_id)

        if authorized:
            session_key = os.urandom(32)
            self.session_keys[drone_id] = session_key
            print(f"[Edge] {drone_id} autorisé ✓ clé de session générée")
            return session_key
        else:
            print(f"[Edge] {drone_id} REFUSÉ ✗")
            return None

    def receive_frame(self, nonce, ciphertext, tag):
        print(f"[Edge] Trame reçue → relayée vers GCS")
        if self.gcs:
            self.gcs.receive_frame(nonce, ciphertext, tag)

if __name__ == "__main__":
    from blockchain import register_drone
    register_drone("DRONE_001", "cle_publique_001")
    
    edge = EdgeNode()
    request = {"drone_id": "DRONE_001", "nonce": os.urandom(16)}
    key = edge.authenticate_drone(request)
    print(f"Clé générée : {key.hex() if key else 'Aucune'}")
