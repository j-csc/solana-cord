import requests
import json

endpoint = "https://api.mainnet-beta.solana.com"

def main():
    # payload = {
    #     "method": "getEpochInfo",
    #     "jsonrpc": "2.0",
    #     "id": 1
    # }
    # response = requests.post(endpoint, json=payload).json()
    # assert response["jsonrpc"]
    # assert response["id"] == 1
    resp = requests.get(endpoint+"/health")
    print(resp.text)

if __name__ == "__main__":
    main()