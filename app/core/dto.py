from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class RequestDTO:
    data: Dict[str, Any]

@dataclass
class ResponseDTO:
    status: int
    data: Dict[str, Any]
    message: str = ""

    @classmethod
    def success(cls, data: Dict[str, Any], message: str = "Success") -> "ResponseDTO":
        return cls(status=200, data=data, message=message)

    @classmethod
    def error(cls, message: str, status: int = 400) -> "ResponseDTO":
        return cls(status=status, data={}, message=message)
