from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import requests
from app.core.exceptions import ThirdPartyAPIException

class ThirdPartyAPI(ABC):
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
    
    @abstractmethod
    def get_headers(self) -> Dict[str, str]:
        """Return headers required for the API calls"""
        pass

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to the API with error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self.get_headers()
        
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
            del kwargs['headers']
            
        try:
            response = self.session.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ThirdPartyAPIException(
                f"Error calling {url}: {str(e)}",
                status_code=getattr(e.response, 'status_code', 500) if hasattr(e, 'response') else 500,
                raw_error=e
            )
