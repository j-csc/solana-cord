#!/usr/bin/env python
import os
import sys
import configparser
import shutil
from .utils import ENDPOINT_URLS
from .logger import logger

class Config:
    def __init__(self, fn) -> None:
        self.fn = fn
        self.check_config_fn()

        config = configparser.ConfigParser(interpolation=None)
        config.read(fn, encoding='utf-8')
        
        confsections = {"Credentials","Sol","Chat"}.difference(config.sections())
        if confsections:
            logger.warn("Please ensure all required config sections are in {}".format(fn))
        
        self.token = config.get("Credentials", "Token", fallback=ConfigDefaults.token)
        self.endpoint = config.get("Sol", "Endpoint", fallback=ConfigDefaults.endpoint)
        self.command_prefix = config.get("Chat", "CommandPrefix", fallback=ConfigDefaults.command_prefix)
        self.bound_channels = config.get("Chat", "BindToChannels", fallback=ConfigDefaults.bound_channels)
        self.endpoint_url = None
                
        self.check_config()
        
        logger.info("Configuration completed!")
    
    def check_config(self) -> None:
        if not self.token:
            logger.warn("Token required!")
        
        if not self.command_prefix or self.command_prefix == '':
            logger.warn("Command prefix set to None or ''")
            
        if not self.endpoint or not self.endpoint.isalpha() or self.endpoint not in ENDPOINT_URLS.keys():
            logger.warn("Faulty endpoint specified, binding to mainnet")
            # default to mainnet
            self.endpoint = ConfigDefaults.endpoint

        self.endpoint_url = ENDPOINT_URLS[self.endpoint]
        
        if self.bound_channels:
            try:
                self.bound_channels = set(x for x in self.bound_channels.replace(',', ' ').split() if x)
            except:
                logger.warn('BindToChannels data invalid, not binding to any channels')
                self.bound_channels = set
    
    def check_config_fn(self) -> None:
        config = configparser.ConfigParser(interpolation=None)
        if not os.path.isfile(self.fn):
            logger.warn("options.ini not found, using default config options")
        elif not config.read(self.fn, encoding='utf-8'):
            logger.warn("Unable to parse options.ini")

class ConfigDefaults:
    token = None
    command_prefix = "."
    bound_channels = set()
    endpoint = 'MAIN'
    options_fn = 'config/options.ini'
    
if __name__ == '__main__':
    print(ENDPOINT_URLS[0])
    pass