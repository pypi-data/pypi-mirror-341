from typing import Any

class ODataEndpointInfo:
    endpoint = '';
    headers = {};

    def __init__(self, endpoint: str, headers: Any) -> None:
        self.endpoint = endpoint;
        self.headers = headers;