from agentic_ai_vass_tools.tools.odata_query_tool import ODataQueryTool
from agentic_ai_vass_tools.tools.odata_date_formatter_tools import ODataDateParserTool, ODataQueryDateFormatterTool
from agentic_ai_vass_tools.services.sap_connector_service import SAPConnectorService
from agentic_ai_vass_tools.models.connector_info import ConnectorInfo
from agentic_ai_vass_tools.models.query_tool_input import QueryToolServiceData

def getCFEnvCloudConnectorInfo(destination_service_name: str, destination_name: str) -> (ConnectorInfo | None): 
    return SAPConnectorService.getCFEnvCloudConnectorInfo(destination_service_name, destination_name);

def getOnPremODataQueryTool(destination_service_name: str, destination_name: str) -> (ODataQueryTool | None):
    connectorInfo = getCFEnvCloudConnectorInfo(destination_service_name, destination_name);
    if(connectorInfo is None): return None;
    return ODataQueryTool(serviceInfo=QueryToolServiceData(
        host=connectorInfo.proxy_url,
        tokenURL=connectorInfo.connectivity_token_url,
        authHeader=connectorInfo.auth_header,
        clientID=connectorInfo.connectivity_client_id,
        clientSecret=connectorInfo.connectivity_client_secret,
        additionalHeaders=connectorInfo.additional_headers,
    ));


__all__ = [
    ## TOOLS
    'ODataQueryTool', 
    'ODataDateParserTool', 
    'ODataQueryDateFormatterTool',

    ## FUNCTIONS
    'getCFEnvCloudConnectorInfo', 
    'getOnPremODataQueryTool', 
]