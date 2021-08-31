from typing import Any, Literal, NamedTuple, TypedDict, Union, Optional, Dict

class Error(NamedTuple):
    code: int
    message: str
    data: Optional[Any]    
    def __repr__(self) -> str:
        return f"Error(code={self.code!r}, message={self.message!r}, data={self.data!r}, id={self.id!r})"

class Request(TypedDict):
    jsonrpc: Literal["2.0"]
    method: str
    id: Any
    params: Union[Dict[str, Any], None]

class Response(TypedDict):
    jsonrpc: Literal["2.0"]    
    result: Any
    error: Optional[Error]
    id: int