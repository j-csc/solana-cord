#!/usr/bin/env python
from typing import Tuple
from client import Client
from response_helper import EpochInfoResponse
import datetime

# TODO - Add more boosted methods

class BoostedClient(Client):
    def __init__(self, url: str, id: int = 1) -> None:
        super().__init__(url, id=id)
        
    def getEpochProgress(self) -> Tuple[float,str]:
        # Get epoch info
        epochInfoResp = self.getEpochInfo()["result"]
        ei = EpochInfoResponse(**epochInfoResp)

        # Estimate time remaining
        percentCompleted = (ei.slotIndex / ei.slotsInEpoch) 
        startSlotTime = self.getBlockTime(ei.absoluteSlot - ei.slotIndex)["result"]
        currSlotTime = self.getBlockTime(ei.absoluteSlot)["result"]
        estimatedTimeRemaining = (currSlotTime - startSlotTime) / percentCompleted
        
        return percentCompleted, str(datetime.timedelta(seconds=estimatedTimeRemaining))
    
if __name__ == "__main__":
    # Sample usage
    URL = "https://api.mainnet-beta.solana.com"
    solClient = BoostedClient(URL)
    ei = solClient.getEpochProgress()
    print(ei)