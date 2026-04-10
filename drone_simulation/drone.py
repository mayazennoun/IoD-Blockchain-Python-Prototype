import os
import time
from Crypto.Cipher import ChaCha20_Poly1305

class Drone:
    def __init__(self, drone_id):
        self.drone_id = drone_id
        self.session_key = None

    def request_access(self):
        nonce = os.urandom(16)
        print(f"[Drone {self.drone_id}] Demande d'accès envoyée à l'Edge")
        return {"drone_id": self.drone_id, "nonce": nonce}

    def receive_session_key(self, key):
        self.session_key = key
        print(f"[Drone {self.drone_id}] Clé de session reçue ✓")

    def encrypt_frame(self, frame_data):
        nonce = os.urandom(12)
        cipher = ChaCha20_Poly1305.new(key=self.session_key, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(frame_data)
        return nonce, ciphertext, tag

    def stream_video(self, edge):
        print(f"[Drone {self.drone_id}] Début du streaming vidéo...")
        for i in range(10):  
            frame = f"frame_{i}_drone_{self.drone_id}".encode()
            nonce, ciphertext, tag = self.encrypt_frame(frame)
            print(f"[Drone {self.drone_id}] Trame {i} chiffrée → envoyée à l'Edge")
            edge.receive_frame(nonce, ciphertext, tag)
            time.sleep(0.033)  

if __name__ == "__main__":
    drone = Drone("DRONE_001")
    drone.receive_session_key(os.urandom(32))  
    
    class FakeEdge:
        def receive_frame(self, nonce, ciphertext, tag):
            print(f"[Edge] Trame reçue")
    
    drone.stream_video(FakeEdge())
