#!/usr/bin/env python
import requests
import json
from math import floor
import logging
import os
import sys
from enum import Enum

# Solana mainnet url
URL = "https://api.mainnet-beta.solana.com"

# Set up basic logger
logger = logging.getLogger('sol.client')

# Setup stdout logger
soh = logging.StreamHandler(sys.stdout)
logger.addHandler(soh)

# File handler for logging to a file
fh = logging.FileHandler('apiWrapper.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

# Get log level from env vars
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
if os.environ.get('DEBUG'):
    if log_level:
        logger.warn("Overriding LOG_LEVEL setting with DEBUG")
    log_level = 'DEBUG'

try:
    logger.setLevel(log_level)
except ValueError:
    logger.setLevel(logging.INFO)
    logger.warn("Variable LOG_LEVEL not valid - Setting Log Level to INFO")

class SolClient(object):
    def __init__(self,url,id):
        self.url = url
        self.id = id
        self.session = requests.Session()
        logger.info('Testing for health...')
        if self._healthCheck():
            logger.info('Health check successful!')
        else:
            logger.info('Health check failed!')
            raise ConnectionError('Health check failed!')
    
    def _healthCheck(self):
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
        
    def _make_request(self, method, query_params=None, payload=None):
        '''
        Handles all requests to Solana API
        '''
        url = self.url
        req = requests.Request(method, url, params=query_params, json=payload)
        prepped = self.session.prepare_request(req)

        # Log request prior to sending
        self._pprint_request(prepped)

        # Actually make request to endpoint
        r = self.session.send(prepped)

        # Log response immediately upon return
        self._pprint_response(r)

        # Handle all response codes as elegantly as needed in a single spot
        if r.status_code == requests.codes.ok:
            try:
                resp_json = r.json()
                logger.debug('Response: {}'.format(resp_json))
                return resp_json
            except ValueError:
                return r.text

        elif r.status_code == 401:
            logger.info("Request unsuccessful!")
            try:
                resp_json = r.json()
                logger.debug('Details: ' + str(resp_json))
                raise ConnectionError(resp_json)
            except ValueError:
                raise

        # TODO handle rate limiting gracefully

        # Raises HTTP error if status_code is 4XX or 5XX
        elif r.status_code >= 400:
            logger.error('Received a ' + str(r.status_code) + ' error!')
            try:
                logger.debug('Details: ' + str(r.json()))
            except ValueError:
                pass
            r.raise_for_status()

    def _pprint_request(self, prepped):
        method = prepped.method
        url = prepped.path_url
        # TODO retrieve HTTP version
        headers = '\n'.join('{}: {}'.format(k, v) for k, v in
                            prepped.headers.items())
        # Print body if present or empty string if not
        body = prepped.body or ""

        logger.info("Requesting {} to {}".format(method, url))

        logger.debug(
            '{}\n{} {} HTTP/1.1\n{}\n\n{}'.format(
                '-----------REQUEST-----------',
                method,
                url,
                headers,
                body
            )
        )

    def _pprint_response(self, r):
        httpv = 'HTTP/{}.{}'.format(httpv0, httpv1)
        status_code = r.status_code
        status_text = r.reason
        headers = '\n'.join('{}: {}'.format(k, v) for k, v in
                            r.headers.items())
        body = r.text or ""
        # Convert timedelta to milliseconds
        elapsed = floor(r.elapsed.total_seconds() * 1000)

        logger.info(
            "Response {} {} received in {}ms".format(
                status_code,
                status_text,
                elapsed
            )
        )

        logger.debug(
            '{}\n{} {} {}\n{}\n\n{}'.format(
                '-----------RESPONSE-----------',
                httpv,
                status_code,
                status_text,
                headers,
                body
            )
        )

    def make_request(
        self,
        endpoint,
        method="GET",
        query_params=None,
        body=None
    ):
        return self._make_request(endpoint, method, query_params, body)

    def get_version(self):
        """Returns the current solana versions running on the node"""
         
        pass
    
    def get_users(
            self,
            tags=[],
            offset=0,
            limit=20
    ):
        '''Get list of users in Example
        :tags: list of tags to filter users on
        '''
        endpoint = '/api/v1/users'
        params = {}
        if tags:
            params['tags'] = ','.join(tags)
        else:
            tags = None
        params['offset'] = offset
        params['limit'] = limit
        params['include_tags'] = True

        return self._make_request(endpoint, 'GET', query_params=params)

    def get_user(self, user_id):
        """return user object
        """
        endpoint = '/api/v1/users/{}'.format(user_id)
        return self._make_request(endpoint, 'GET')


if __name__ == "__main__":
    solClient = SolClient(URL, 1)
    pass