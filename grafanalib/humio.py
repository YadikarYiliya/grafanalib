"""Helpers to create Humio-specific Grafana queries."""

from pydantic import BaseModel

class HumioTarget(BaseModel):
    """
    Generates Humio target JSON structure.

    Link to Humio Grafana plugin: https://grafana.com/grafana/plugins/humio-datasource/
    Humio docs on query language: https://library.humio.com/humio-server/syntax.html

    :param humioQuery: Query that will be executed on Humio.
    :param humioRepository: Repository to execute query on.
    :param refId: Target reference id.
    """
    humioQuery: str = ""
    humioRepository: str = ""
    refId: str = ""

    def to_json_data(self) -> dict:
        return {
            "humioQuery": self.humioQuery,
            "humioRepository": self.humioRepository,
            "refId": self.refId,
        }