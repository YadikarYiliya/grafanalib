"""Helpers to create InfluxDB-specific Grafana queries."""

from pydantic import BaseModel

TIME_SERIES_TARGET_FORMAT = 'time_series'


class InfluxDBTarget(BaseModel):
    """
    Generates InfluxDB target JSON structure.

    Grafana docs on using InfluxDB:
    https://grafana.com/docs/features/datasources/influxdb/
    InfluxDB docs on querying or reading data:
    https://v2.docs.influxdata.com/v2.0/query-data/

    :param alias: legend alias
    :param format: Bucket aggregators
    :param datasource: Influxdb name (for multiple datasource with same panel)
    :param measurement: Metric Aggregators
    :param query: query
    :param rawQuery: target reference id
    :param refId: target reference id
    """
    alias: str = ""
    format: str = TIME_SERIES_TARGET_FORMAT
    datasource: str = ""
    measurement: str = ""
    query: str = ""
    rawQuery: bool = True
    refId: str = ""

    def to_json_data(self) -> dict:
        return {
            'query': self.query,
            'resultFormat': self.format,
            'alias': self.alias,
            'datasource': self.datasource,
            'measurement': self.measurement,
            'rawQuery': self.rawQuery,
            'refId': self.refId
        }