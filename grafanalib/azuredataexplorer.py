"""Helpers to create Azure Data Explorer specific Grafana queries."""

from typing import Optional
from pydantic import BaseModel

# Constants for result formats
TIME_SERIES_RESULT_FORMAT = 'time_series'
TABLE_RESULT_FORMAT = 'table'
ADX_TIME_SERIES_RESULT_FORMAT = 'time_series_adx_series'

class AzureDataExplorerTarget(BaseModel):
    """
    Generates Azure Data Explorer target JSON structure.

    Link to Azure Data Explorer datasource Grafana plugin:
    https://grafana.com/grafana/plugins/grafana-azure-data-explorer-datasource/

    Azure Data Explorer docs on query language (KQL):
    https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/

    :param database: Database to execute query on
    :param query: Query in Kusto Query Language (KQL)
    :param resultFormat: Output format of the query result
    :param alias: legend alias
    :param refId: target reference id
    """
    
    # Define class attributes with type hints and default values
    database: Optional[str] = None
    query: str = ""
    resultFormat: str = TIME_SERIES_RESULT_FORMAT
    alias: str = ""
    refId: str = ""
    
    class Config:
        # Pydantic configuration for serialization and deserialization
        use_enum_values = True