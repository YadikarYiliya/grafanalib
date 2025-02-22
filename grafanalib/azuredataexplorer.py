"""Helpers to create Azure Data Explorer specific Grafana queries."""

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
    database: str = ""
    query: str = ""
    resultFormat: str = TIME_SERIES_RESULT_FORMAT
    alias: str = ""
    refId: str = ""
    
    class Config:
        # Pydantic configuration for serialization and deserialization
        use_enum_values = True

    def to_json_data(self):
        # Convert the Pydantic model to a dictionary (JSON-like structure)
        return self.dict()

# Test function
def test_azure_data_explorer_target():
    # Test 1: Default values
    target = AzureDataExplorerTarget()
    assert target.database == ""  # Default value for database
    assert target.query == ""  # Default value for query
    assert target.resultFormat == TIME_SERIES_RESULT_FORMAT  # Default result format
    assert target.alias == ""  # Default value for alias
    assert target.refId == ""  # Default value for refId
    
    # Test 2: Creating with custom values
    custom_target = AzureDataExplorerTarget(
        database="my_database",
        query="SELECT * FROM my_table",
        resultFormat="table",
        alias="my_alias",
        refId="target_1"
    )
    
    # Assert the custom values
    assert custom_target.database == "my_database"
    assert custom_target.query == "SELECT * FROM my_table"
    assert custom_target.resultFormat == "table"
    assert custom_target.alias == "my_alias"
    assert custom_target.refId == "target_1"
    
    # Test 3: Converting to JSON-like dictionary
    json_data = custom_target.to_json_data()
    
    # Assert the dictionary structure
    assert json_data == {
        'database': "my_database",
        'query': "SELECT * FROM my_table",
        'resultFormat': "table",
        'alias': "my_alias",
        'refId': "target_1"
    }
    
    print("All tests passed.")

# Run the tests
if __name__ == "__main__":
    test_azure_data_explorer_target()
