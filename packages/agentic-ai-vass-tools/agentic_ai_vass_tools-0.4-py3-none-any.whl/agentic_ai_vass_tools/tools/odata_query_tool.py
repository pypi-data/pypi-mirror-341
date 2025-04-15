from crewai.crew import BaseModel
from crewai.task import BaseTool
from typing import List, Optional, Type
from agentic_ai_vass_tools.utils.btp_utils import buildODataQueryPath
from agentic_ai_vass_tools.services.sap_connector_service import SAPConnectorService
from agentic_ai_vass_tools.models.query_tool_input import MyQueryToolInput, QueryToolServiceData
import json

class ODataQueryTool(BaseTool):
    args_schema: Type[BaseModel] = MyQueryToolInput;
    service_info: Type[BaseModel] = QueryToolServiceData;
    name: str = "SAP OData Query Tool"
    description: str = ("Fetch data from an SAP HANA OData endpoint by passing the OData query variables for the URL and receive structured data back.")

    def __init__(self, serviceInfo: QueryToolServiceData):
        super().__init__();
        self.service_info = serviceInfo;
    
    def getODataPath(self, info: MyQueryToolInput): 
        return buildODataQueryPath(query_info=info, responseFormat='json', noMax=False);

    def __run_query(
        self,
        path: str,
        select: List[str] = [], 
        filters: Optional[List[str]] = None, 
        top: Optional[int] = None, 
        skip: Optional[int] = None, 
        orderby: Optional[str] = None,
        expand: Optional[str] = None,
        count: Optional[bool] = False,
        # apply: Optional[str] = None,
    ) -> str:
        """Executes an OData query and returns results."""
        request_path = self.getODataPath(
            info=MyQueryToolInput(
                path=path,
                select=select,
                filters=filters,
                top=top,
                skip=skip,
                orderby=orderby,
                expand=expand,
                count=count,
                # apply=apply
            ),
        );
        resp = SAPConnectorService.makeODataRequest(service_info=self.service_info, path=request_path);
        return resp if not count else json.dumps({'count': resp});
    
    def _run(
            self, 
            path: str,
            select: List[str] = [], 
            filters: Optional[List[str]] = None, 
            top: Optional[int] = None, 
            skip: Optional[int] = None, 
            orderby: Optional[str] = None,
            expand: Optional[str] = None,
            count: Optional[bool] = False,
            # apply: Optional[str] = None,
        ) -> str:
        return self.__run_query(
            path=path,
            select=select,
            filters=filters,
            top=top,
            skip=skip,
            orderby=orderby,
            expand=expand,
            count=count,
            # apply=apply
        );