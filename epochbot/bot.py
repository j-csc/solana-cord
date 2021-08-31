#!/usr/bin/env python
import os
import time
import sys
import asyncio
import pathlib

import aiohttp
import requests
import discord

from datetime import timedelta
from .logger import logger
from .config import Config, ConfigDefaults
from rpc.boosted_client import BoostedClient

class EpochBot(discord.Client):
    def __init__(self, config_fn=None) -> None:
        super().__init__()
        
        if not config_fn:
            config_fn = ConfigDefaults.options_fn
        
        self.config = Config(config_fn)
    
    async def on_ready(self):
        pass
    
    async def on_message(self, message):
        pass