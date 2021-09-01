#!/usr/bin/env python
from math import floor
import os, sys
from enum import Enum
import requests
import httpx
from .async_request import AsyncRPCRequest
from .base import Response
from .logger import logger

'''
Async Sol JSON RPC Client
'''
class AsyncClient(object):
    def __init__(self, url: str, id: int = 1) -> None:
        self.url = url
        self.id = id
        self.session = httpx.AsyncClient()
        
        # logging
        logger.info('Testing for health...')
        if self._healthCheck():
            logger.info('Health check successful!')
        else:
            logger.info('Health check failed!')
            raise ConnectionError('Health check failed!')
    
    def _healthCheck(self) -> bool:
        '''
        Health check
        '''
        endpoint = '/health'
        r = requests.get(self.url + endpoint)
        r.raise_for_status()
        try:
            pass
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        
        return True if r else False
    
    async def getVersion(self) -> Response:
        '''
        Returns the current solana version running on the node
        '''
        return await AsyncRPCRequest(url=self.url, id=self.id, method='getFees', session=self.session).make_request()
    
    async def getFees(self) -> Response:
        '''
        Returns a recent block hash from the ledger, a fee schedule that can be used to compute the cost of submitting a transaction using it, and the last slot in which the blockhash will be valid.
        '''
        return await AsyncRPCRequest(url=self.url, id=self.id, method='getFees', session=self.session).make_request()
        
    async def getFirstAvailableBlock(self) -> Response:
        '''
        Returns the slot of the lowest confirmed block that has not been purged from the ledger
        '''
        return await AsyncRPCRequest(url=self.url, id=self.id, method='getFirstAvailableBlock', session=self.session).make_request()

    async def getGenesisHash(self) -> Response:
        '''
        Returns the genesis hash
        '''
        return await AsyncRPCRequest(url=self.url, id=self.id, method='getGenesisHash', session=self.session).make_request()
    
    async def getHealth(self) -> Response:
        '''
        Returns the current health of the node.
        '''
        return await AsyncRPCRequest(url=self.url, id=self.id, method='getHealth', session=self.session).make_request()

    async def getLeaderSchedule(self) -> Response:
        '''
        Returns the leader schedule for an epoch
        '''
        return await AsyncRPCRequest(url=self.url, id=self.id, method='getLeaderSchedule', session=self.session).make_request()
    
    async def getSlot(self) -> Response:
        '''
        Returns the slot that has reached the given or default commitment level
        '''
        return await AsyncRPCRequest(url=self.url, id=self.id, method='getSlot', session=self.session).make_request()
    
    async def getSlotLeader(self) -> Response:
        '''
        Returns the current slot leader
        '''
        return await AsyncRPCRequest(url=self.url, id=self.id, method='getSlotLeader', session=self.session).make_request()
    
    async def getInflationRate(self) -> Response:
        '''
        Returns the specific inflation values for the current epoch
        '''
        return await AsyncRPCRequest(url=self.url, id=self.id, method='getInflationRate', session=self.session).make_request()
    
    async def getInflationGovernor(self) -> Response:
        '''
        Returns the current inflation governor
        '''
        return await AsyncRPCRequest(url=self.url, id=self.id, method='getInflationGovernor', session=self.session).make_request()

    async def getEpochInfo(self) -> Response:
        '''
        Returns information about the current epoch
        '''
        return await AsyncRPCRequest(url=self.url, id=self.id, method='getEpochInfo', session=self.session).make_request()

    async def getEpochSchedule(self) -> Response:
        '''
        Returns epoch schedule information from this cluster's genesis config
        '''
        return await AsyncRPCRequest(url=self.url, id=self.id, method='getEpochSchedule', session=self.session).make_request()

    async def getBlockTime(self, slot) -> Response:
        '''
        Returns the estimated production time of a block.
        '''
        return await AsyncRPCRequest(url=self.url, id=self.id, method='getBlockTime', params=[slot], session=self.session).make_request()


if __name__ == "__main__":
    # Sample usage
    URL = "https://api.mainnet-beta.solana.com"
    solClient = Client(URL)
    res = solClient.getEpochInfo()
    print(res)