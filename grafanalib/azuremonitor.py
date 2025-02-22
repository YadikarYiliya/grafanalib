"""Helpers to create Azure Monitor specific Grafana queries."""

from pydantic import BaseModel
from typing import List

class AzureMonitorMetricsTarget(BaseModel):
    """
    Generates Azure Monitor Metrics target JSON structure.

    Grafana docs on using Azure Monitor:
    https://grafana.com/docs/grafana/latest/datasources/azuremonitor/#querying-azure-monitor-metrics

    :param aggregation: Metrics Aggregation (Total, None, Minimum, Maximum, Average, Count)
    :param dimensionFilters: Dimension Filters
    :param metricsDefinition: Metrics Definition https://docs.microsoft.com/en-us/azure/azure-monitor/essentials/metrics-supported
    :param metricNamespace: Metrics Namespace
    :param resourceGroup: Resource Group the resource resides in
    :param timeGrain: Time Granularity
    :param queryType: Type of Query (Azure Monitor in this case)
    :param subscription: Azure Subscription ID to scope to
    :param refId: Reference ID for the target
    """
    
    aggregation: str = "Total"
    dimensionFilters: List[str] = []
    metricDefinition: str = ""
    metricName: str = ""
    metricNamespace: str = ""
    resourceGroup: str = ""
    resourceName: str = ""
    timeGrain: str = "auto"
    queryType: str = "Azure Monitor"
    subscription: str = ""
    refId: str = ""
    alias: str = ""

    def to_json_data(self):
        return {
            "azureMonitor": {
                "aggregation": self.aggregation,
                "alias": self.alias,
                "dimensionFilters": self.dimensionFilters,
                "metricDefinition": self.metricDefinition,
                "metricName": self.metricName,
                "metricNamespace": self.metricNamespace,
                "resourceGroup": self.resourceGroup,
                "resourceName": self.resourceName,
                "timeGrain": self.timeGrain,
            },
            "queryType": self.queryType,
            "refId": self.refId,
            "subscription": self.subscription,
        }


class AzureLogsTarget(BaseModel):
    """
    Generates Azure Monitor Logs target JSON structure.

    Grafana docs on using Azure Logs:
    https://grafana.com/docs/grafana/latest/datasources/azuremonitor/#querying-azure-monitor-logs

    :param query: Query to execute
    :param resource: Identification string for resource e.g. /subscriptions/1234-abcd/resourceGroups/myResourceGroup/providers/Microsoft.DataFactory/factories/myDataFactory
    :param resultFormat: Output Format of the logs
    :param queryType: Type of Query (Azure Log Analytics in this case)
    :param subscription: Azure Subscription ID to scope to
    :param refId: Reference ID for the target
    """
    
    query: str = ""
    resource: str = ""
    resultFormat: str = "table"
    queryType: str = "Azure Log Analytics"
    subscription: str = ""
    refId: str = ""

    def to_json_data(self):
        return {
            "azureLogAnalytics": {
                "query": self.query,
                "resource": self.resource,
                "resultFormat": self.resultFormat,
            },
            "queryType": self.queryType,
            "refId": self.refId,
            "subscription": self.subscription,
        }


class AzureResourceGraphTarget(BaseModel):
    """
    Generates Azure Resource Graph target JSON structure.

    Grafana docs on using Azure Resource Graph:
    https://grafana.com/docs/grafana/latest/datasources/azuremonitor/#querying-azure-resource-graph

    :param query: Query to execute
    :param queryType: Type of Query (Azure Resource Graph in this case)
    :param subscription: Azure Subscription ID to scope to
    :param refId: Reference ID for the target
    """
    
    query: str = ""
    resource: str = ""
    queryType: str = "Azure Resource Graph"
    subscription: str = ""
    refId: str = ""

    def to_json_data(self):
        return {
            "azureResourceGraph": {"query": self.query},
            "queryType": self.queryType,
            "refId": self.refId,
            "subscription": self.subscription,
        }
