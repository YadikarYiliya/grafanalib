"""Helpers to create Elasticsearch-specific Grafana queries."""

import itertools
from typing import Any
from pydantic import BaseModel, Field

DATE_HISTOGRAM_DEFAULT_FIELD = 'time_iso8601'
ORDER_ASC = 'asc'
ORDER_DESC = 'desc'


class CountMetricAgg(BaseModel):
    id: int = 0
    hide: bool = False
    inline: str = ""

    def to_json_data(self) -> dict[str, Any]:
        settings: dict[str, Any] = {}
        if self.inline:
            settings['script'] = {'inline': self.inline}
        return {
            'id': str(self.id),
            'hide': self.hide,
            'type': 'count',
            'field': 'select field',
            'inlineScript': self.inline,
            'settings': settings,
        }


class MaxMetricAgg(BaseModel):
    field: str = ""
    id: int = 0
    hide: bool = False
    inline: str = ""

    def to_json_data(self) -> dict[str, Any]:
        settings: dict[str, Any] = {}
        if self.inline:
            settings['script'] = {'inline': self.inline}
        return {
            'id': str(self.id),
            'hide': self.hide,
            'type': 'max',
            'field': self.field,
            'inlineScript': self.inline,
            'settings': settings,
        }


class CardinalityMetricAgg(BaseModel):
    field: str = ""
    id: int = 0
    hide: bool = False
    inline: str = ""

    def to_json_data(self) -> dict[str, Any]:
        settings: dict[str, Any] = {}
        if self.inline:
            settings['script'] = {'inline': self.inline}
        return {
            'id': str(self.id),
            'hide': self.hide,
            'type': 'cardinality',
            'field': self.field,
            'inlineScript': self.inline,
            'settings': settings,
        }


class AverageMetricAgg(BaseModel):
    field: str = ""
    id: int = 0
    hide: bool = False
    inline: str = ""

    def to_json_data(self) -> dict[str, Any]:
        settings: dict[str, Any] = {}
        if self.inline:
            settings['script'] = {'inline': self.inline}
        return {
            'id': str(self.id),
            'hide': self.hide,
            'type': 'avg',
            'field': self.field,
            'inlineScript': self.inline,
            'settings': settings,
            'meta': {}
        }


class DerivativeMetricAgg(BaseModel):
    field: str = ""
    hide: bool = False
    id: int = 0
    pipelineAgg: int = 1
    unit: str = ""

    def to_json_data(self) -> dict[str, Any]:
        settings: dict[str, Any] = {}
        if self.unit:
            settings['unit'] = self.unit
        return {
            'id': str(self.id),
            'pipelineAgg': str(self.pipelineAgg),
            'hide': self.hide,
            'type': 'derivative',
            'field': self.field,
            'settings': settings,
        }


class SumMetricAgg(BaseModel):
    field: str = ""
    id: int = 0
    hide: bool = False
    inline: str = ""

    def to_json_data(self) -> dict[str, Any]:
        settings: dict[str, Any] = {}
        if self.inline:
            settings['script'] = {'inline': self.inline}
        return {
            'id': str(self.id),
            'hide': self.hide,
            'type': 'sum',
            'field': self.field,
            'inlineScript': self.inline,
            'settings': settings,
        }


class DateHistogramGroupBy(BaseModel):
    id: int = 0
    field: str = DATE_HISTOGRAM_DEFAULT_FIELD
    interval: str = "auto"
    minDocCount: int = 0

    def to_json_data(self) -> dict[str, Any]:
        return {
            'field': self.field,
            'id': str(self.id),
            'settings': {
                'interval': self.interval,
                'min_doc_count': self.minDocCount,
                'trimEdges': 0,
            },
            'type': 'date_histogram',
        }


class BucketScriptAgg(BaseModel):
    fields: dict[str, int] = Field(default_factory=dict)
    id: int = 0
    hide: bool = False
    script: str = ""

    def to_json_data(self) -> dict[str, Any]:
        pipelineVars: list[Any] = []
        for field_name, agg_id in self.fields.items():
            pipelineVars.append({
                'name': str(field_name),
                'pipelineAgg': str(agg_id)
            })
        return {
            'field': 'select field',
            'type': 'bucket_script',
            'id': str(self.id),
            'hide': self.hide,
            'pipelineVariables': pipelineVars,
            'settings': {
                'script': self.script
            },
        }


class Filter(BaseModel):
    label: str = ""
    query: str = ""

    def to_json_data(self) -> dict[str, Any]:
        return {
            'label': self.label,
            'query': self.query,
        }


class FiltersGroupBy(BaseModel):
    id: int = 0
    filters: list[Filter] = Field(default_factory=list)

    def to_json_data(self) -> dict[str, Any]:
        return {
            'id': str(self.id),
            'settings': {
                'filters': [f.to_json_data() for f in self.filters],
            },
            'type': 'filters',
        }


class TermsGroupBy(BaseModel):
    field: str
    id: int = 0
    minDocCount: int = 1
    order: str = ORDER_DESC
    orderBy: str = '_term'
    size: int = 0

    def to_json_data(self) -> dict[str, Any]:
        return {
            'id': str(self.id),
            'type': 'terms',
            'field': self.field,
            'settings': {
                'min_doc_count': self.minDocCount,
                'order': self.order,
                'orderBy': self.orderBy,
                'size': self.size,
            },
        }


class ElasticsearchTarget(BaseModel):
    alias: Any = None
    bucketAggs: list[Any] = Field(default_factory=lambda: [DateHistogramGroupBy()])
    metricAggs: list[Any] = Field(default_factory=lambda: [CountMetricAgg()])
    query: str = ""
    refId: str = ""
    timeField: str = "@timestamp"
    hide: bool = False

    def auto_bucket_agg_ids(self) -> "ElasticsearchTarget":
        ids = {agg.id for agg in self.bucketAggs if agg.id}
        auto_ids = (i for i in itertools.count(1) if i not in ids)
        new_bucketAggs = []
        for agg in self.bucketAggs:
            if agg.id:
                new_bucketAggs.append(agg)
            else:
                new_bucketAggs.append(agg.copy(update={"id": next(auto_ids)}))
        return self.copy(update={"bucketAggs": new_bucketAggs})

    def to_json_data(self) -> dict[str, Any]:
        return {
            'alias': self.alias,
            'bucketAggs': [agg.to_json_data() for agg in self.bucketAggs],
            'metrics': [agg.to_json_data() for agg in self.metricAggs],
            'query': self.query,
            'refId': self.refId,
            'timeField': self.timeField,
            'hide': self.hide,
        }


class ElasticsearchAlertCondition(BaseModel):
    target: ElasticsearchTarget = None
    evaluator: Any
    timeRange: Any = None
    operator: str = "and"
    reducerType: str = "last"
    useNewAlerts: bool = False
    type: str = Field(default="query", alias="type")

    def to_json_data(self) -> dict[str, Any]:
        query_params: list[Any] = []
        if self.useNewAlerts:
            if self.target:
                query_params = [self.target.refId]
        elif self.target and self.timeRange:
            query_params = [self.target.refId, self.timeRange.from_time, self.timeRange.to_time]
        condition = {
            'evaluator': self.evaluator.to_json_data(),
            'operator': {'type': self.operator},
            'query': {
                'model': self.target.to_json_data() if self.target else {},
                'params': query_params,
            },
            'reducer': {'params': [], 'type': self.reducerType},
            'type': self.type,
        }
        if self.useNewAlerts:
            condition['query'].pop('model', None)
        return condition


class MinMetricAgg(BaseModel):
    field: str = ""
    id: int = 0
    hide: bool = False
    inline: str = ""

    def to_json_data(self) -> dict[str, Any]:
        settings: dict[str, Any] = {}
        if self.inline:
            settings['script'] = {'inline': self.inline}
        return {
            'id': str(self.id),
            'hide': self.hide,
            'type': 'min',
            'field': self.field,
            'inlineScript': self.inline,
            'settings': settings,
        }


class PercentilesMetricAgg(BaseModel):
    field: str = ""
    id: int = 0
    hide: bool = False
    inline: str = ""
    percents: list[float] = Field(default_factory=list)

    def to_json_data(self) -> dict[str, Any]:
        settings: dict[str, Any] = {}
        settings['percents'] = self.percents
        if self.inline:
            settings['script'] = {'inline': self.inline}
        return {
            'id': str(self.id),
            'hide': self.hide,
            'type': 'percentiles',
            'field': self.field,
            'inlineScript': self.inline,
            'settings': settings,
        }


class RateMetricAgg(BaseModel):
    field: str = ""
    id: int = 0
    hide: bool = False
    unit: str = ""
    mode: str = ""
    script: str = ""

    def to_json_data(self) -> dict[str, Any]:
        settings: dict[str, Any] = {}
        if self.unit:
            settings["unit"] = self.unit
        if self.mode:
            settings["mode"] = self.mode
        if self.script:
            settings["script"] = self.script
        return {
            "id": str(self.id),
            "hide": self.hide,
            "field": self.field,
            "settings": settings,
            "type": "rate",
        }