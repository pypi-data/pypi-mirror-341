import datetime
from typing import Any, List, Type
from crewai.crew import BaseModel
from crewai.task import BaseTool
from pydantic import Field
import re

class MyQueryDateFormatterInput(BaseModel):
    dates: List[str] = Field([], description="A list of dates in the format MM-DD-YYYY")

class MyDateParserInput(BaseModel):
    sap_dates: List[str] = Field([], description="A list of SAP dates in the format /Date(<milliseconds>)/")


class ODataQueryDateFormatterTool(BaseTool):
    args_schema: Type[BaseModel] = MyQueryDateFormatterInput;
    name: str = "Query Date Formatter"
    description: str = "Format a list of dates (MM-DD-YYYY) into a list of strings compatible with OData V2 query filters requirements. Only supports dates in format MM-DD-YYYY. ";

    def convert_dates_to_odata(self, dates: List[str]):
        """
        Converts a list of dates from MM-DD-YYYY to OData V2 datetime format.
        """
        odata_dates = [
            f"datetime'{datetime.datetime.strptime(date, '%m-%d-%Y').strftime('%Y-%m-%dT00:00:00')}'"
            for date in dates
        ]
        return odata_dates


    def _run(self, dates: List[str]) -> Any:
        return self.convert_dates_to_odata(dates=dates);

class ODataDateParserTool(BaseTool): 
    args_schema: Type[BaseModel] = MyDateParserInput;
    name: str = "Date Formatter Tool"
    description: str = "Format a list of SAP dates (/Date(<milliseconds>)/) into a user friendly string. Only supports dates. Does not support time. ";

    def format_sap_date(self, sap_dates: List[str]) -> List[dict]:
        """Converts SAP date format (/Date(<milliseconds>)/) to a user-friendly format."""
        result: List[dict] = [];
        for sap_date in sap_dates:
            try:
            # Extract the milliseconds part using regex
                match = re.search(r"/Date\((\d+)\)/", str(sap_date))
                if not match:
                    result.append({  "sap_date": sap_date, "formatted_date": sap_date }) # Return input as is if the format is incorrect
                    continue;
                # Convert milliseconds to datetime
                timestamp = int(match.group(1)) / 1000  # Convert milliseconds to seconds
                dt = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)

                # Determine the day suffix (st, nd, rd, th)
                day = dt.day
                suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

                # Format date
                formatted_date = dt.strftime(f"%B {day}{suffix}, %Y")  # Example: "February 20th, 2024"

                result.append({ "sap_date": sap_date, "formatted_date":formatted_date })
            except Exception as e:
                print(f'exception formatting SAP date: {e}')
                result.append({ "sap_date": sap_date, "formatted_date": sap_date }) # Return input if an error occurs
        return result;


    def _run(self, sap_dates: List[str]) -> Any:
        return self.format_sap_date(sap_dates=sap_dates);
