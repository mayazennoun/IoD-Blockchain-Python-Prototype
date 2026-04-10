from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

ABI = [
    {
        "inputs": [{"internalType": "string", "name": "droneId", "type": "string"}],
        "name": "isAuthorized",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "droneId", "type": "string"}, {"internalType": "string", "name": "pubKey", "type": "string"}],
        "name": "registerDrone",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "droneId", "type": "string"}],
        "name": "getPublicKey",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
admin = w3.eth.accounts[0]

def register_drone(drone_id, public_key):
    tx = contract.functions.registerDrone(drone_id, public_key).transact({"from": admin})
    w3.eth.wait_for_transaction_receipt(tx)
    print(f"[Blockchain] Drone {drone_id} enregistré")

def is_authorized(drone_id):
    result = contract.functions.isAuthorized(drone_id).call()
    print(f"[Blockchain] {drone_id} autorisé : {result}")
    return result

if __name__ == "__main__":
    print("Connecté :", w3.is_connected())
    register_drone("DRONE_001", "cle_publique_drone_001")
    is_authorized("DRONE_001")
    is_authorized("DRONE_999")  # drone non enregistré