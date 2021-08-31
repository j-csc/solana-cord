from typing import Any, Dict, Tuple, Union, cast
from base import Request, Response
import requests
from logger import logger
import sys

# TODO: - Add error handling

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
        return cast(Response, raw.json())
    
    def _pprint_response(self) -> None:
        if logger:
            logger.info("Requesting {} to {}".format(self.method, self.url))
            logger.debug(
                '{}\nmethod: {}\nurl: {}\ntype: application/json\nparams: {}\n'.format(
                    '-----------RPC RESPONSE-----------',
                    self.method,
                    self.url,
                    self.params
                )
            )
    
    def _pprint_request(self) -> None:
        if logger:
            logger.info("Requesting {} to {}".format(self.method, self.url))
            logger.debug(
                '{}\nmethod: {}\nurl: {}\ntype: application/json\nparams: {}\n'.format(
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