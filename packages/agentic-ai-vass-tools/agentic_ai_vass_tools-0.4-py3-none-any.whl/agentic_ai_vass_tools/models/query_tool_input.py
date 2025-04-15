from typing import List, Optional
from pydantic import BaseModel, Field

class QueryToolServiceData(BaseModel):
    host: str = Field(..., description="The host URL path for the OData service")
    tokenURL: str = Field(..., description="The full URL to fetch the Auth token")
    authHeader: str = Field(..., description="The value of the Authorization header")
    additionalHeaders: Optional[dict[str, str]] = Field(None, description="Any additional headers for the OData request")
    clientID: str = Field(..., description="The client ID to authenticate to the OData service")
    clientSecret: str = Field(..., description="The client Secret to authenticate to the OData service")

class MyQueryToolInput(BaseModel):
    ## required parameters:
    path: str = Field(..., description="The path to the OData entity to query")
    select: List[str] = Field(..., description="List of columns to select from the table accessed by the OData query (use \'*\' to select all)")
    ### optional parameters: 
    count: Optional[bool] = Field(False, description="Request only a count of the records that match the query filters")
    filters: Optional[List[str]] = Field(None, description="optional list of filters to apply to the OData query to filter the data request")
    top: Optional[int] = Field(None, description="Optional number of total records to retrieve from the OData query request")
    skip: Optional[int] = Field(None, description="Optional number of records to skip when requesting pagination")
    orderby: Optional[str] = Field(None, description="Optional name of table column to be used to sort and order the query results")
    expand: Optional[str] = Field(None, description="Optional string value for the $expand feature in OData V2")
    # apply: Optional[str] = Field(None, description="The $apply filter for OData V2 queries")
