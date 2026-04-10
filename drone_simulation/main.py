from blockchain import register_drone
from drone import Drone
from edge import EdgeNode
from gcs import GCS

print("=" * 50)
print("PHASE 0 - Enregistrement des drones")
print("=" * 50)
register_drone("DRONE_001", "cle_publique_001")
register_drone("DRONE_002", "cle_publique_002")

print("\n" + "=" * 50)
print("PHASE 1 - Authentification")
print("=" * 50)
gcs = GCS()
edge = EdgeNode()
edge.set_gcs(gcs)

drone1 = Drone("DRONE_001")
drone2 = Drone("DRONE_002")

request1 = drone1.request_access()
key1 = edge.authenticate_drone(request1)
drone1.receive_session_key(key1)
gcs.receive_session_key(key1)

print("\n" + "=" * 50)
print("PHASE 2 - Streaming vidéo")
print("=" * 50)
drone1.stream_video(edge)

print("\n" + "=" * 50)
print(f"RÉSULTAT : {gcs.frames_received} trames reçues par la GCS")
print("=" * 50)
