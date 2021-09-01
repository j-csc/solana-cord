#!/usr/bin/env python
import os
import time
import sys

import asyncio
import pathlib
import requests
import discord
from discord.ext import commands, tasks
from aiohttp import ClientSession

from datetime import datetime, timedelta
from .logger import logger
from .config import Config, ConfigDefaults
from rpc.boosted_client import BoostedClient

class EpochBot(commands.Bot):
    def __init__(self, config_fn=None) -> None:
        intents = discord.Intents.default()   
                     
        if not config_fn:
            config_fn = ConfigDefaults.options_fn
        self.config = Config(config_fn)
        
        super().__init__(command_prefix=self.config.command_prefix, intents=intents)
        
        self.rpcClient = BoostedClient(self.config.endpoint_url)
        self._session = None
        
    '''
    Properties
    '''
    @property
    def session(self) -> ClientSession:
        if self._session is None:
            self._session = ClientSession(loop=self.loop)
        return self._session
    
    '''
    Main event Loop
    '''
    # https://github.com/kyb3r/modmail/blob/master/bot.py run loop
    def run(self):
        loop = self.loop
        async def runner():
            try:
                retry_intents = False
                try:
                    await self.start(self.config.token)
                except discord.PrivilegedIntentsRequired:
                    retry_intents = True
                if retry_intents:
                    await self.http.close()
                    if self.ws is not None and self.ws.open:
                        await self.ws.close(code=1000)
                    self._ready.clear()
                    intents = discord.Intents.default()
                    intents.members = True
                    # Try again with members intent
                    self._connection._intents = intents
                    logger.warning(
                        "Attempting to login with only the server members privileged intent. Some plugins might not work correctly."
                    )
                    await self.start(self.config.token)
            except discord.PrivilegedIntentsRequired:
                logger.critical(
                    "Privileged intents are not explicitly granted in the discord developers dashboard."
                )
            except discord.LoginFailure:
                logger.critical("Invalid token")
            except Exception:
                logger.critical("Fatal exception", exc_info=True)
            finally:
                if not self.is_closed():
                    await self.close()
                if self._session:
                    await self._session.close()

        def stop_loop_on_completion(f):
            loop.stop()

        def _cancel_tasks():
            if sys.version_info < (3, 8):
                task_retriever = asyncio.Task.all_tasks
            else:
                task_retriever = asyncio.all_tasks

            tasks = {t for t in task_retriever(loop=loop) if not t.done()}

            if not tasks:
                return

            logger.info("Cleaning up after %d tasks.", len(tasks))
            for task in tasks:
                task.cancel()

            loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            logger.info("All tasks finished cancelling.")

            for task in tasks:
                if task.cancelled():
                    continue
                if task.exception() is not None:
                    loop.call_exception_handler(
                        {
                            "message": "Unhandled exception during Client.run shutdown.",
                            "exception": task.exception(),
                            "task": task,
                        }
                    )

        future = asyncio.ensure_future(runner(), loop=loop)
        future.add_done_callback(stop_loop_on_completion)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info("Received signal to terminate bot and event loop.")
        finally:
            future.remove_done_callback(stop_loop_on_completion)
            logger.info("Cleaning up tasks.")

            try:
                _cancel_tasks()
                if sys.version_info >= (3, 6):
                    loop.run_until_complete(loop.shutdown_asyncgens())
            finally:
                logger.info("Closing the event loop.")
                loop.close()

        if not future.cancelled():
            try:
                return future.result()
            except KeyboardInterrupt:
                # I am unsure why this gets raised here but suppress it anyway
                return None
    
    '''
    On Ready
    '''
    async def on_ready(self):
        activity = discord.Activity(name='Solana Epoch Tracker', type=discord.ActivityType.watching)
        await self.change_presence(activity=activity)
        logger.info(f'{self.user} has connected to Discord!')
        