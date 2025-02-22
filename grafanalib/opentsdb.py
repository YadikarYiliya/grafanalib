"""Support for OpenTSDB."""

from typing import Any, List, Optional
from pydantic import BaseModel, Field, validator

# OpenTSDB aggregators
OTSDB_AGG_AVG = 'avg'
OTSDB_AGG_COUNT = 'count'
OTSDB_AGG_DEV = 'dev'
OTSDB_AGG_EP50R3 = 'ep50r3'
OTSDB_AGG_EP50R7 = 'ep50r7'
OTSDB_AGG_EP75R3 = 'ep75r3'
OTSDB_AGG_EP75R7 = 'ep75r7'
OTSDB_AGG_EP90R3 = 'ep90r3'
OTSDB_AGG_EP90R7 = 'ep90r7'
OTSDB_AGG_EP95R3 = 'ep95r3'
OTSDB_AGG_EP95R7 = 'ep95r7'
OTSDB_AGG_EP99R3 = 'ep99r3'
OTSDB_AGG_EP99R7 = 'ep99r7'
OTSDB_AGG_EP999R3 = 'ep999r3'
OTSDB_AGG_EP999R7 = 'ep999r7'
OTSDB_AGG_FIRST = 'first'
OTSDB_AGG_LAST = 'last'
OTSDB_AGG_MIMMIN = 'mimmin'
OTSDB_AGG_MIMMAX = 'mimmax'
OTSDB_AGG_MIN = 'min'
OTSDB_AGG_MAX = 'max'
OTSDB_AGG_NONE = 'none'
OTSDB_AGG_P50 = 'p50'
OTSDB_AGG_P75 = 'p75'
OTSDB_AGG_P90 = 'p90'
OTSDB_AGG_P95 = 'p95'
OTSDB_AGG_P99 = 'p99'
OTSDB_AGG_P999 = 'p999'
OTSDB_AGG_SUM = 'sum'
OTSDB_AGG_ZIMSUM = 'zimsum'

OTSDB_DOWNSAMPLING_FILL_POLICIES = ('none', 'nan', 'null', 'zero')
OTSDB_DOWNSAMPLING_FILL_POLICY_DEFAULT = 'none'

OTSDB_QUERY_FILTERS = (
    'literal_or', 'iliteral_or', 'not_literal_or',
    'not_iliteral_or', 'wildcard', 'iwildcard', 'regexp')
OTSDB_QUERY_FILTER_DEFAULT = 'literal_or'


class OpenTSDBFilter(BaseModel):
    value: Any
    tag: Any
    type: str = Field(default=OTSDB_QUERY_FILTER_DEFAULT)
    groupBy: bool = False

    @validator('type')
    def validate_type(cls, v):
        if v not in OTSDB_QUERY_FILTERS:
            raise ValueError(f"type must be one of {OTSDB_QUERY_FILTERS}")
        return v

    def to_json_data(self) -> dict:
        return {
            'filter': self.value,
            'tagk': self.tag,
            'type': self.type,
            'groupBy': self.groupBy
        }


class OpenTSDBTarget(BaseModel):
    """
    Generates OpenTSDB target JSON structure.

    Grafana docs on using OpenTSDB:
    http://docs.grafana.org/features/datasources/opentsdb/
    OpenTSDB docs on querying or reading data:
    http://opentsdb.net/docs/build/html/user_guide/query/index.html

    :param metric: OpenTSDB metric name
    :param refId: target reference id
    :param aggregator: defines metric aggregator.
    :param alias: legend alias. Use patterns like $tag_tagname to replace part
        of the alias for a tag value.
    :param isCounter: defines if rate function results should be interpreted as counter
    :param counterMax: defines rate counter max value
    :param counterResetValue: defines rate counter reset value
    :param disableDownsampling: defines if downsampling should be disabled.
    :param downsampleAggregator: defines downsampling aggregator
    :param downsampleFillPolicy: defines downsampling fill policy
    :param downsampleInterval: defines downsampling interval
    :param filters: defines the list of metric query filters.
    :param shouldComputeRate: defines if rate function should be used.
    :param currentFilterGroupBy: defines if grouping should be enabled for current filter
    :param currentFilterKey: defines current filter key
    :param currentFilterType: defines current filter type
    :param currentFilterValue: defines current filter value
    """
    metric: Any
    refId: str = ""
    aggregator: str = 'sum'
    alias: Optional[Any] = None
    isCounter: bool = False
    counterMax: Optional[Any] = None
    counterResetValue: Optional[Any] = None
    disableDownsampling: bool = False
    downsampleAggregator: str = OTSDB_AGG_SUM
    downsampleFillPolicy: str = Field(default=OTSDB_DOWNSAMPLING_FILL_POLICY_DEFAULT)
    downsampleInterval: Optional[Any] = None
    filters: List[Any] = Field(default_factory=list)
    shouldComputeRate: bool = False
    currentFilterGroupBy: bool = False
    currentFilterKey: str = ""
    currentFilterType: str = OTSDB_QUERY_FILTER_DEFAULT
    currentFilterValue: str = ""

    @validator('downsampleFillPolicy')
    def validate_downsample_fill_policy(cls, v):
        if v not in OTSDB_DOWNSAMPLING_FILL_POLICIES:
            raise ValueError(f"downsampleFillPolicy must be one of {OTSDB_DOWNSAMPLING_FILL_POLICIES}")
        return v

    def to_json_data(self) -> dict:
        return {
            'aggregator': self.aggregator,
            'alias': self.alias,
            'isCounter': self.isCounter,
            'counterMax': self.counterMax,
            'counterResetValue': self.counterResetValue,
            'disableDownsampling': self.disableDownsampling,
            'downsampleAggregator': self.downsampleAggregator,
            'downsampleFillPolicy': self.downsampleFillPolicy,
            'downsampleInterval': self.downsampleInterval,
            'filters': self.filters,
            'metric': self.metric,
            'refId': self.refId,
            'shouldComputeRate': self.shouldComputeRate,
            'currentFilterGroupBy': self.currentFilterGroupBy,
            'currentFilterKey': self.currentFilterKey,
            'currentFilterType': self.currentFilterType,
            'currentFilterValue': self.currentFilterValue,
        }