import logging
from typing import Dict, Any
import requests
from json import loads


def get_response(method: str, url: str, headers: Dict, params: Dict,
                 timeout: int, success=200) -> Any:
    """Sends request and returns response.text if success, otherwise returns status_code"""
    response = requests.request(
        method,
        url,
        headers=headers,
        params=params,
        timeout=timeout
    )

    status_code = response.status_code
    logging.debug(response.text)
    if status_code == success:
        return loads(response.text)

    return status_code
