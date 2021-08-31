#!/usr/bin/env python
'''
Custom response objects
'''
class EpochInfoResponse:
    def __init__(
        self, 
        absoluteSlot:str,
        blockHeight:int,
        epoch:int,
        slotIndex:int,
        slotsInEpoch:int,
        transactionCount:int
        ) -> None:
        self.absoluteSlot = absoluteSlot
        self.blockHeight = blockHeight
        self.epoch = epoch
        self.slotIndex = slotIndex
        self.slotsInEpoch = slotsInEpoch
        self.transactionCount = transactionCount