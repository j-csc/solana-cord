from typing import Any, Dict, Iterator, Tuple, Union

class AsyncRequest():
    def __init__(
        self,
        client: Any,
        method: str,
        params: Union[Dict[str, Any], Tuple[Any, ...], None] = None,
        payload: Any = None,
        retries: bool = False,
        logger: Any = None
        ):
        self.client = client
        self.method = method
        self.params = params
        self.payload = payload
        self.retries = retries
        self.logger = logger
    
    def __str__(self) -> str:
        return "Async JSON RPC connection - {}".format(self.client.url)
    
    def _build_req(self) -> None:
        url = self.client.url
        id = self.client.id
        pass
    
    def make_req(self) -> None:
        pass
    
    def _pprint_request(self) -> str:
        if self.logger:
            self.logger.info("Requesting {} to {}".format(self.client.method, self.client.url))
            self.logger.debug(
                '{}\n{} {} application/json\n{}\n\n{}'.format(
                    '-----------RPC REQUEST-----------',
                    self.method,
                    self.client.url,
                    self.payload
                )
            )