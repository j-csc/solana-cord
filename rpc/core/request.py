#!/usr/bin/env python
from typing import Any, Dict, Tuple, Union, cast
import requests
import sys
from math import floor
from .logger import logger
from .base import Request, Response

# TODO: - Add error handling

'''
Custom RPC Request
'''
class RPCRequest:
    def __init__(
        self,
        url: str,
        method: str,
        id: int = 1,
        params: Union[Dict[str, Any], Tuple[Any, ...], None] = None,
        session: Any = None
        ):
        self.url = url
        self.id = id
        self.method = method
        self.params = params
        self.session = session
        
    def _build_request(self) -> Request:
        return {
            "jsonrpc": "2.0",
            "method": self.method,
            **({"params": self.params} if self.params else {}),
            "id": self.id
        }
            
    def make_request(self) -> Response:
        request = self._build_request()
        self._pprint_request()
        resp = None
        if self.session:
            resp = self.session.post(self.url, json=request)
        else:
            resp = requests.post(self.url, request)
        
        return self._process_response(resp)
    
    def _process_response(self, raw: requests.Response) -> Response:
        raw.raise_for_status()
        self._pprint_response(raw)
        return cast(Response, raw.json())
    
    def _pprint_response(self, r:requests.Response) -> None:
        if logger:
            status_code = r.status_code
            body = r.text
            elapsed = floor(r.elapsed.total_seconds() * 1000)
            
            logger.info("Response {} received in {}ms".format(
                status_code,
                elapsed))
            
            logger.debug(
                '\n{}\ncode: {} \ntype: application/json\nbody: {}\n'.format(
                    '-----------RPC RESPONSE-----------',
                    status_code,
                    body
                )
            )
    
    def _pprint_request(self) -> None:
        if logger:
            logger.info("Requesting {} to {}".format(self.method, self.url))
            logger.debug(
                '\n{}\nmethod: {}\nurl: {}\ntype: application/json\nparams: {}\n'.format(
                    '-----------RPC REQUEST-----------',
                    self.method,
                    self.url,
                    self.params
                )
            )
    
    @classmethod
    def _cls_build_request(
        cls,
        id: int,
        method: str,
        params: Union[Dict[str, Any], Tuple[Any, ...], None] = None
        ) -> Request:
        return {
            "jsonrpc": "2.0",
            "method": method,
            **({"params": params} if params else {}),
            "id": id
        }

    @classmethod
    def cls_make_request(
        cls,
        url: str,
        id: int,
        method: str,
        params: Union[Dict[str, Any], Tuple[Any, ...], None] = None,
        logger: Any = None
    ) -> Response:
        req = cls._build_request(id, method, params)
        return cast(Response, requests.post(url, json=req).json())