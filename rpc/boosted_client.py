#!/usr/bin/env python
from typing import Tuple
import datetime
from .response_helper import EpochInfoResponse
from .core.async_client import AsyncClient

# TODO - Add more boosted methods

'''
Boosted Sol JSON RPC Client
'''
class BoostedClient(AsyncClient):
    def __init__(self, url: str, id: int = 1) -> None:
        super().__init__(url, id=id)
        
    async def getEpochProgress(self) -> Tuple[float,str]:
        # Get epoch info
        epochInfoResp = (await self.getEpochInfo())["result"]
        ei = EpochInfoResponse(**epochInfoResp)

        # Estimate time remaining
        percentCompleted = (ei.slotIndex / ei.slotsInEpoch) 
        startSlotTime = (await self.getBlockTime(ei.absoluteSlot - ei.slotIndex))["result"]
        currSlotTime = (await self.getBlockTime(ei.absoluteSlot))["result"]
        estimatedTimeRemaining = (currSlotTime - startSlotTime) / percentCompleted
        
        # Pretty print
        
        seconds_in_day = 60 * 60 * 24
        seconds_in_hour = 60 * 60
        seconds_in_minute = 60
        days = estimatedTimeRemaining // seconds_in_day
        hours = (estimatedTimeRemaining - (days * seconds_in_day)) // seconds_in_hour
        minutes = (estimatedTimeRemaining - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute
        
        res_time_remaining = "{}d {}h {}m".format(int(days), int(hours), int(minutes))
        res_percent_completed = "{0:.2f}%".format(percentCompleted*100)
        
        return res_percent_completed, res_time_remaining