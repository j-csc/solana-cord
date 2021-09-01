#!/usr/bin/env python
from typing import Any, Dict, Tuple, Union, cast
import requests
import sys
from math import floor
import httpx
from .logger import logger
from .base import Request, Response
from .request import RPCRequest


'''
Async RPC Request
'''
class AsyncRPCRequest(RPCRequest):
    def __init__(
        self,
        url: str,
        method: str,
        id: int = 1,
        params: Union[Dict[str, Any], Tuple[Any, ...], None] = None,
        session: Any = None
        ):
        
        super().__init__(
            url=url,
            method=method,
            id=1,
            params=params,
            session=session
        )

        if session:
            self.session = session
        else:
            self.session = httpx.AsyncClient()
        
    def _build_request(self) -> Request:
        self._pprint_request()
        return {
            "jsonrpc": "2.0",
            "method": self.method,
            **({"params": self.params} if self.params else {}),
            "id": self.id
        }
            
    async def make_request(self) -> Response:
        request = self._build_request()
        resp = await self.session.post(self.url, json=request)
        return await self._process_response(resp)
    
    async def _process_response(self, raw: requests.Response) -> Response:
        raw.raise_for_status()
        self._pprint_response(raw)
        return cast(Response, raw.json())