from typing import Any, Optional


class ConnectorInfo:
    connectivity_service = {};
    proxy_host = '';
    proxy_port = '';
    proxy_url = '';
    sap_client = '';
    connectivity_client_id = '';
    connectivity_client_secret = '';
    connectivity_token_url = '';
    destination: Any | None = None;
    auth_header = '';
    additional_headers: Optional[dict[str, str]] = None;

    def __init__(
        self, 
        connectivity_service: Any, 
        proxy_host: str, 
        proxy_port: str, 
        proxy_url: str, 
        sap_client: str, 
        connectivity_client_id: str, 
        connectivity_client_secret: str, 
        connectivity_token_url: str,
        auth_header: str,
        additional_headers: Optional[dict[str, str]],
        destination: Any | None,
    ) -> None:
        self.sap_client = sap_client;
        self.connectivity_client_id = connectivity_client_id;
        self.connectivity_client_secret = connectivity_client_secret;
        self.connectivity_service = connectivity_service;
        self.connectivity_token_url = connectivity_token_url;
        self.proxy_host = proxy_host;
        self.proxy_port = proxy_port;
        self.proxy_url = proxy_url;
        self.destination = destination;
        self.auth_header = auth_header;
        self.additional_headers = additional_headers;