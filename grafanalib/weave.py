"""Weave-specific dashboard configuration.

Unlike 'core', which has logic for building generic Grafana dashboards, this
has our Weave-specific preferences.
"""

from typing import List, Tuple
import grafanalib.core as G
from grafanalib import prometheus
from pydantic import BaseModel, Field

YELLOW = '#EAB839'
GREEN = '#7EB26D'
BLUE = '#6ED0E0'
ORANGE = '#EF843C'
RED = '#E24D42'

ALIAS_COLORS = {
    '1xx': YELLOW,
    '2xx': GREEN,
    '3xx': BLUE,
    '4xx': ORANGE,
    '5xx': RED,
    'success': GREEN,
    'error': RED,
}

class QPSGraphConfig(BaseModel):
    """Configuration for QPS Graph in Grafana"""
    data_source: str
    title: str
    expressions: List[str] = Field(..., min_items=5, max_items=7)
    kwargs: dict = Field(default_factory=dict)

    def create_graph(self):
        """Create a graph of QPS, broken up by response code."""
        legends = sorted(ALIAS_COLORS.keys())
        exprs = list(zip(legends, self.expressions))

        return stacked(prometheus.PromGraph(
            data_source=self.data_source,
            title=self.title,
            expressions=exprs,
            aliasColors=ALIAS_COLORS,
            yAxes=G.YAxes(
                G.YAxis(format=G.OPS_FORMAT),
                G.YAxis(format=G.SHORT_FORMAT),
            ),
            **self.kwargs
        ))


def stacked(graph):
    """Turn a graph into a stacked graph using Pydantic."""
    return graph.copy(update={
        "lineWidth": 0,
        "nullPointMode": G.NULL_AS_ZERO,
        "stack": True,
        "fill": 10,
        "tooltip": G.Tooltip(
            sort=G.SORT_DESC,
            valueType=G.INDIVIDUAL,
        ),
    })


def PercentUnitAxis(label: str = None):
    """A Y axis that shows a percentage based on a unit value."""
    return G.YAxis(
        format=G.PERCENT_UNIT_FORMAT,
        label=label,
        logBase=1,
        max=1,
        min=0,
    )
