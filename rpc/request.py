from typing import Any, Dict, Tuple, Union
from base import Request, Error, Response
import requests

class RPCRequest:
    def __init__(
        self, 
        client: Any,
        method: str, 
        params: Union[Dict[str, Any], Tuple[Any, ...], None] = None,
        retries: bool = False
        ):
        self.client = client
        self.method = method
        self.params = params
        self.retries = retries
        
    def _build_request(self) -> Request:
        return {
            "jsonrpc": "2.0",
            "method": self.method,
            **({"params": self.params} if self.params else {}),
            "id": self.client.id
        }
    
    def make_request(self) -> Response:
        request = self._build_request()
        self._pprint_request()
        
        if self.client.session:
            return self.client.session.post(self.client.url, json=request)
        else:
            return requests.post(self.client.url, request)
    
    def _pprint_request(self) -> str:
        if self.client.logger:
            self.client.logger.info("Requesting {} to {}".format(self.client.method, self.client.url))
            self.client.logger.debug(
                '{}\n{} {} application/json\n{}\n\n{}'.format(
                    '-----------RPC REQUEST-----------',
                    self.method,
                    self.client.url,
                    self.params
                )
            )
    
    @classmethod
    def _build_request(
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
    def make_request(
        cls,
        url: str,
        id: int,
        method: str,
        params: Union[Dict[str, Any], Tuple[Any, ...], None] = None,
        logger: Any = None
    ) -> Response:
        request = RPCRequest._build_request(id, method, params)
        RPCRequest._pprint_request(url, request)
        return requests.post(url, json=request).json()
        
    @classmethod
    def _pprint_request(
        cls,
        url: str,
        request: Request,
        logger: Any = None
    ) -> Response:
        if logger:
            logger.info("Requesting {} to {}".format(request.method, url))
            logger.debug(
                '{}\n{} {} application/json\n{}\n\n{}'.format(
                    '-----------RPC REQUEST-----------',
                    request.method,
                    url,
                    request.params
                )
            )

if __name__ == '__main__':
    resp = RPCRequest.make_request("https://api.mainnet-beta.solana.com", 1, "getEpochInfo")
    print(resp)