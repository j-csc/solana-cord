import requests
import json
from rpc.boosted_client import BoostedClient

endpoint = "https://api.mainnet-beta.solana.com"

if __name__ == "__main__":
    # Sample usage
    URL = "https://api.mainnet-beta.solana.com"
    solClient = BoostedClient(URL)
    res = solClient.getEpochProgress()
    print(res)