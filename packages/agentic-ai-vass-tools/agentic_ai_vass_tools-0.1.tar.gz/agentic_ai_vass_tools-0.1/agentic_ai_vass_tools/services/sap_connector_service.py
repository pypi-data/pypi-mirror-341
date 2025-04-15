from typing import Optional
import json;
import os

import requests;
from models.connector_info import ConnectorInfo, ODataEndpointInfo
from utils.btp_utils import getDestination
from models.query_tool_input import QueryToolServiceData

class SAPConnectorService:
    @staticmethod
    def getCFEnvCloudConnectorInfo(destination_service_name: str, destination_name: str) -> Optional[ConnectorInfo]:
        vcap_services = json.loads(os.getenv("VCAP_SERVICES", "{}"));

        # Extract the connectivity service credentials
        connectivity_service = vcap_services.get("connectivity", [{}])[0].get("credentials", {})
        proxy_host = connectivity_service.get("onpremise_proxy_host", "localhost")
        proxy_port = connectivity_service.get("onpremise_proxy_port", "20003")
        connectivity_client_id = connectivity_service.get("clientid")
        connectivity_client_secret = connectivity_service.get("clientsecret")
        connectivity_token_url = connectivity_service.get("token_service_url") + "/oauth/token"

        # Extract the destination service credentials
        destination = getDestination(sDestinationService=destination_service_name, sDestinationName=destination_name)

        if(destination == None): return None;
        auth_header = destination["authTokens"][0]["http_header"]["value"];

        # Use the proxy URL to route requests through the Cloud Connector
        proxy_url = f"http://{proxy_host}:{proxy_port}"
        sap_client = destination["destinationConfiguration"]["sap-client"];

        return ConnectorInfo(
            connectivity_service=connectivity_service,
            proxy_host=proxy_host,
            proxy_port=proxy_port,
            proxy_url=proxy_url,
            sap_client=sap_client,
            connectivity_client_id=connectivity_client_id,
            connectivity_client_secret=connectivity_client_secret,
            connectivity_token_url=connectivity_token_url + "/oauth/token",
            destination=destination,
            auth_header=auth_header,
        );

    @staticmethod
    def getODataEndpoint(service_info: QueryToolServiceData, path: str, accepts: Optional[str] = None) -> Optional[ODataEndpointInfo]:
        # service_info = SAPConnectorService.getServiceInfo();
        if(service_info == None): return None;


        # 🔹 Step 1: Retrieve Proxy Authorization Token
        proxy_auth_response = requests.post(
            service_info.tokenURL,
            data={"grant_type": "client_credentials"},
            auth=(service_info.clientID, service_info.clientSecret),
        )

        if proxy_auth_response.status_code != 200:
            return None;

        proxy_auth_token = proxy_auth_response.json()["access_token"]

        headers = {
            "Authorization": service_info.authHeader,  # Extracted from destination response
            "Proxy-Authorization": f"Bearer {proxy_auth_token}", 
        };

        if(accepts is not None): headers['Accept'] = accepts;

        return ODataEndpointInfo(
            endpoint=f"{service_info.host}{path}",
            headers=headers,
        );
    
    @staticmethod 
    def makeODataRequest(service_info: QueryToolServiceData, path: str) -> str:
        endpoint_info = SAPConnectorService.getODataEndpoint(service_info, path)
        if(endpoint_info == None): return 'No endpoint info received from SAPConnectorService'
        try:
        # Send request through the Cloud Connector
            response = requests.get(endpoint_info.endpoint, headers=endpoint_info.headers)
            if response.status_code == 200:
                return response.text
            else:
                return f'status_code: {response.status_code}'
        except requests.exceptions.RequestException as e:
            return f'{e}'





