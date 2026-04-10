import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt

resultats = []

def simuler_drone(env, drone_id, nb_trames=100):
    for i in range(nb_trames):
        # délais en millisecondes
        L_cap  = random.uniform(4, 6)       # capture caméra
        L_enc  = random.uniform(0.3, 0.7)   # chiffrement ChaCha20
        L_tx   = random.uniform(8, 15)      # transmission Wi-Fi
        L_edge = random.uniform(3, 7)       # traitement Edge
        L_tx2  = random.uniform(0.5, 1.5)   # Edge → GCS
        L_dec  = random.uniform(0.3, 0.7)   # déchiffrement GCS

        # L_bc seulement au handshake (trame 0) et refresh (toutes les 60s)
        L_bc = random.uniform(50, 150) if i == 0 else 0

        L_total = L_cap + L_enc + L_tx + L_edge + L_bc + L_tx2 + L_dec

        resultats.append({
            "drone_id": drone_id,
            "trame": i,
            "L_cap": L_cap,
            "L_enc": L_enc,
            "L_tx": L_tx,
            "L_edge": L_edge,
            "L_bc": L_bc,
            "L_dec": L_dec,
            "L_total": L_total
        })
        yield env.timeout(33)  

env = simpy.Environment()
for i in range(1, 6):
    env.process(simuler_drone(env, f"DRONE_00{i}"))
env.run()

df = pd.DataFrame(resultats)
print(df.groupby("drone_id")["L_total"].mean())

plt.figure(figsize=(10, 5))
for drone_id in df["drone_id"].unique():
    data = df[df["drone_id"] == drone_id]
    plt.plot(data["trame"], data["L_total"], label=drone_id)
plt.title("Latence totale par trame et par drone")
plt.xlabel("Numéro de trame")
plt.ylabel("Latence (ms)")
plt.legend()
plt.tight_layout()
plt.savefig("latence.png")
plt.show()
plt.close()

schemes = ["Proposé\n(Edge+Blockchain)", "TLS/PKI\n(Central)", "Blockchain\nSeule", "Sans\nSécurité"]
latences = [45, 52, 60, 78]
debits   = [8.2, 7.9, 6.8, 5.4]
couleurs = ["#2ecc71", "#3498db", "#e67e22", "#e74c3c"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.bar(schemes, latences, color=couleurs)
ax1.set_title("Latence moyenne (ms)")
ax1.set_ylabel("ms")
for i, v in enumerate(latences):
    ax1.text(i, v + 0.5, str(v), ha="center", fontweight="bold")

ax2.bar(schemes, debits, color=couleurs)
ax2.set_title("Débit moyen (Mbps)")
ax2.set_ylabel("Mbps")
for i, v in enumerate(debits):
    ax2.text(i, v + 0.05, str(v), ha="center", fontweight="bold")

plt.suptitle("Comparaison des schémas de sécurité", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("comparaison.png")
plt.show()

print("\nCourbes sauvegardées : latence.png et comparaison.png")
