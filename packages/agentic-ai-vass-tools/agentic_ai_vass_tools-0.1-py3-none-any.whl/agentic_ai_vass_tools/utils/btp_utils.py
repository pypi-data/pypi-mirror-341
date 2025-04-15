from typing import Optional
from cfenv import AppEnv
import requests
from models.query_tool_input import MyQueryToolInput, QueryToolServiceData

 

def getDestination(sDestinationService, sDestinationName):

    # Read the environment variables

    # -------------------------------------------------------------------------------

    env = AppEnv()

    dest_service = env.get_service(name=sDestinationService)

    if dest_service is None:

        print(f"Service {sDestinationService} not found")

        return None


    sUaaCredentials = dest_service.credentials['clientid'] + ':' + dest_service.credentials['clientsecret']

    # Request a JWT token to access the destination service 

    # -------------------------------------------------------------------------------

    headers = {'Authorization': 'Basic '+sUaaCredentials, 'content-type': 'application/x-www-form-urlencoded'}

    form = [('client_id', dest_service.credentials['clientid'] ),('client_secret', dest_service.credentials['clientsecret'] ), ('grant_type', 'client_credentials')]


    url = dest_service.credentials['url'] +"/oauth/token"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=form)


    # Search your destination in the destination service

    # -------------------------------------------------------------------------------

    token = response.json()["access_token"]

    headers= { 'Authorization': 'Bearer ' + token }

    r = requests.get(dest_service.credentials['uri'] + '/destination-configuration/v1/destinations/'+sDestinationName, headers=headers)

    print("DEST URI:",dest_service.credentials['uri'])

    

    # Access the destination securely

    # -------------------------------------------------------------------------------

    destination = r.json()


    return destination

def buildODataQueryPath(query_info: MyQueryToolInput, responseFormat: Optional[str] = None, noMax: bool = False) -> str: 
    # base_url: str, entity_set: str, filters: List[str] = None, top: int = None, skip: int = None, select: list = None, orderby: str = None
    """
    Constructs a properly formatted SAP OData query path.
    query_info should have the following optional parameters:
    - base_url (required): Base URL of the SAP OData service. 
    - service (required): The OData service to query (e.g., Products). 
    - path (required): the path to query within the entity_set.
    - param (optional): OData endpoint parameter to request a specific record.
    - filters (optional): A list of filter expressions.
    - top (optional): Number of records to retrieve
    - skip (optional): Number of records to skip (for pagination)
    - select (required): List of fields to retrieve (e.g., [\"ProductName\", \"Price\"])
    - orderby (optional): Field to order results by (e.g., \"Price desc\")."
    - expand: the string with the name of the subentity to expand
    """

    query_params = []
    filters = query_info.filters if query_info.filters is not None else None;
    # param = query_info.param if query_info.param is not None else None;
    top = query_info.top if query_info.top is not None else None;
    expand = query_info.expand if query_info.expand is not None else None;
    skip = query_info.skip if query_info.skip is not None else None;
    select = query_info.select if query_info.select is not None else None;
    orderby = query_info.orderby if query_info.orderby is not None else None;
    service_path = query_info.path if query_info.path is not None else "";
    count = query_info.count if query_info.count is not None else False;
    # apply = query_info.apply if query_info.apply is not None else None;

    # Add filters (properly formatted for SAP OData)
    if filters:
        query_params.append(f"$filter={' and '.join(filters)}")
        # filter_conditions = [f"{key} eq '{value}'" for key, value in filters.items()]

    # Add $top, $skip, $select, $orderby parameters
    if (top != None or noMax is False) and not count:
        query_params.append(f"$top={top if top != None else 10}")
    
    if skip and not count:
        query_params.append(f"$skip={skip}")
    if select and not count:
        query_params.append(f"$select={','.join(select) if len(select) <= 4 else '*'}")
    if orderby and not count:
        query_params.append(f"$orderby={orderby}")
    # if apply:
    #     query_params.append(f"$apply={apply}")
    if expand:
        query_params.append(f"$expand={expand}")
    if responseFormat and not count:
        query_params.append(f"$format={responseFormat}")

    # Construct final URL
    query_string = "&".join(query_params);
    normalizedPath =  service_path.removeprefix('/') if service_path.startswith('/') else service_path;
    
    base_path = f"/sap/opu/odata/sap/{normalizedPath}{'/$count' if count else ''}"
    full_path = f"{base_path}?{query_string}" if query_params else f"{base_path}"
    return full_path;