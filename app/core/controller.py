from typing import Any, Dict
from flask import jsonify
from app.core.dto import ResponseDTO
from app.core.exceptions import ApplicationException

class BaseController:
    def __init__(self):
        pass

    def _create_response(self, response: ResponseDTO) -> tuple[Dict[str, Any], int]:
        return jsonify({
            'status': 'success' if response.status < 400 else 'error',
            'message': response.message,
            'data': response.data
        }), response.status

    def handle_request(self, use_case_callable: callable, *args, **kwargs) -> tuple[Dict[str, Any], int]:
        try:
            result = use_case_callable(*args, **kwargs)
            return self._create_response(result)
        except ApplicationException as e:
            return self._create_response(
                ResponseDTO.error(message=str(e), status=e.status_code)
            )
        except Exception as e:
            return self._create_response(
                ResponseDTO.error(message=str(e), status=500)
            )
