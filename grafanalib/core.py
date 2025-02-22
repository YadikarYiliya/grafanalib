"""Low-level functions for building Grafana dashboards.
The functions in this module don't enforce Weaveworks policy, and only mildly
encourage it by way of some defaults. Rather, they are ways of building
arbitrary Grafana JSON.
"""

from __future__ import annotations
import itertools
import math
import string
import warnings
from numbers import Number
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Basic Types
# ---------------------------------------------------------------------------

class RGBA(BaseModel):
    r: int
    g: int
    b: int
    a: float

    def to_json_data(self) -> str:
        return "rgba({}, {}, {}, {})".format(self.r, self.g, self.b, self.a)

class RGB(BaseModel):
    r: int
    g: int
    b: int

    def to_json_data(self) -> str:
        return "rgb({}, {}, {})".format(self.r, self.g, self.b)

class Pixels(BaseModel):
    num: int

    def to_json_data(self) -> str:
        return "{}px".format(self.num)

class Percent(BaseModel):
    num: Number = 100

    def to_json_data(self) -> str:
        return "{}%".format(self.num)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GREY1 = RGBA(r=216, g=200, b=27, a=0.27)
GREY2 = RGBA(r=234, g=112, b=112, a=0.22)
BLUE_RGBA = RGBA(r=31, g=118, b=189, a=0.18)
BLUE_RGB = RGB(r=31, g=120, b=193)
GREEN = RGBA(r=50, g=172, b=45, a=0.97)
ORANGE = RGBA(r=237, g=129, b=40, a=0.89)
RED = RGBA(r=245, g=54, b=54, a=0.9)
BLANK = RGBA(r=0, g=0, b=0, a=0.0)
WHITE = RGB(r=255, g=255, b=255)

INDIVIDUAL = 'individual'
CUMULATIVE = 'cumulative'

NULL_CONNECTED = 'connected'
NULL_AS_ZERO = 'null as zero'
NULL_AS_NULL = 'null'

FLOT = 'flot'

ABSOLUTE_TYPE = 'absolute'
DASHBOARD_TYPE = Literal['dashboards', 'link']
ROW_TYPE = 'row'
GRAPH_TYPE = 'graph'
DISCRETE_TYPE = 'natel-discrete-panel'
EPICT_TYPE = 'larona-epict-panel'
STAT_TYPE = 'stat'
SINGLESTAT_TYPE = 'singlestat'
STATE_TIMELINE_TYPE = 'state-timeline'
TABLE_TYPE = 'table'
TEXT_TYPE = 'text'
ALERTLIST_TYPE = 'alertlist'
BARGAUGE_TYPE = 'bargauge'
GAUGE_TYPE = 'gauge'
DASHBOARDLIST_TYPE = 'dashlist'
LOGS_TYPE = 'logs'
HEATMAP_TYPE = 'heatmap'
STATUSMAP_TYPE = 'flant-statusmap-panel'
SVG_TYPE = 'marcuscalidus-svg-panel'
PIE_CHART_TYPE = 'grafana-piechart-panel'
PIE_CHART_V2_TYPE = 'piechart'
TIMESERIES_TYPE = 'timeseries'
WORLD_MAP_TYPE = 'grafana-worldmap-panel'
NEWS_TYPE = 'news'
HISTOGRAM_TYPE = 'histogram'
AE3E_PLOTLY_TYPE = 'ae3e-plotly-panel'
BAR_CHART_TYPE = 'barchart'

DEFAULT_FILL = 1
DEFAULT_REFRESH = '10s'
DEFAULT_ALERT_EVALUATE_INTERVAL = '1m'
DEFAULT_ALERT_EVALUATE_FOR = '5m'
DEFAULT_ROW_HEIGHT = Pixels(num=250)
DEFAULT_LINE_WIDTH = 2
DEFAULT_POINT_RADIUS = 5
DEFAULT_RENDERER = FLOT
DEFAULT_STEP = 10
DEFAULT_LIMIT = 10
TOTAL_SPAN = 12

DARK_STYLE = 'dark'
LIGHT_STYLE = 'light'

UTC = 'utc'

SCHEMA_VERSION = 12

# (DEPRECATED: use formatunits.py) Y Axis formats
DURATION_FORMAT = 'dtdurations'
NO_FORMAT = 'none'
OPS_FORMAT = 'ops'
PERCENT_UNIT_FORMAT = 'percentunit'
DAYS_FORMAT = 'd'
HOURS_FORMAT = 'h'
MINUTES_FORMAT = 'm'
SECONDS_FORMAT = 's'
MILLISECONDS_FORMAT = 'ms'
SHORT_FORMAT = 'short'
BYTES_FORMAT = 'bytes'
BITS_PER_SEC_FORMAT = 'bps'
BYTES_PER_SEC_FORMAT = 'Bps'
NONE_FORMAT = 'none'
JOULE_FORMAT = 'joule'
WATTHOUR_FORMAT = 'watth'
WATT_FORMAT = 'watt'
KWATT_FORMAT = 'kwatt'
KWATTHOUR_FORMAT = 'kwatth'
VOLT_FORMAT = 'volt'
BAR_FORMAT = 'pressurebar'
PSI_FORMAT = 'pressurepsi'
CELSIUS_FORMAT = 'celsius'
KELVIN_FORMAT = 'kelvin'
GRAM_FORMAT = 'massg'
EUR_FORMAT = 'currencyEUR'
USD_FORMAT = 'currencyUSD'
METER_FORMAT = 'lengthm'
SQUARE_METER_FORMAT = 'areaM2'
CUBIC_METER_FORMAT = 'm3'
LITRE_FORMAT = 'litre'
PERCENT_FORMAT = 'percent'
VOLT_AMPERE_FORMAT = 'voltamp'

# Alert rule state
STATE_NO_DATA = 'no_data'
STATE_ALERTING = 'alerting'
STATE_KEEP_LAST_STATE = 'keep_state'
STATE_OK = 'ok'

# Evaluator
EVAL_GT = 'gt'
EVAL_LT = 'lt'
EVAL_WITHIN_RANGE = 'within_range'
EVAL_OUTSIDE_RANGE = 'outside_range'
EVAL_NO_VALUE = 'no_value'

# Reducer Type
RTYPE_AVG = 'avg'
RTYPE_MIN = 'min'
RTYPE_MAX = 'max'
RTYPE_SUM = 'sum'
RTYPE_COUNT = 'count'
RTYPE_LAST = 'last'
RTYPE_MEDIAN = 'median'
RTYPE_DIFF = 'diff'
RTYPE_PERCENT_DIFF = 'percent_diff'
RTYPE_COUNT_NON_NULL = 'count_non_null'

# Condition Type
CTYPE_QUERY = 'query'

# Operator
OP_AND = 'and'
OP_OR = 'or'

# Alert Expression Types
EXP_TYPE_CLASSIC = 'classic_conditions'
EXP_TYPE_REDUCE = 'reduce'
EXP_TYPE_RESAMPLE = 'resample'
EXP_TYPE_MATH = 'math'

# Alert Expression Reducer Function
EXP_REDUCER_FUNC_MIN = 'min'
EXP_REDUCER_FUNC_MAX = 'max'
EXP_REDUCER_FUNC_MEAN = 'mean'
EXP_REDUCER_FUNC_SUM = 'sum'
EXP_REDUCER_FUNC_COUNT = 'count'
EXP_REDUCER_FUNC_LAST = 'last'

# Alert Expression Reducer Mode
EXP_REDUCER_MODE_STRICT = 'strict'
EXP_REDUCER_FUNC_DROP_NN = 'dropNN'
EXP_REDUCER_FUNC_REPLACE_NN = 'replaceNN'

# Text panel modes
TEXT_MODE_MARKDOWN = 'markdown'
TEXT_MODE_HTML = 'html'
TEXT_MODE_TEXT = 'text'

# Datasource plugins
PLUGIN_ID_GRAPHITE = 'graphite'
PLUGIN_ID_PROMETHEUS = 'prometheus'
PLUGIN_ID_INFLUXDB = 'influxdb'
PLUGIN_ID_OPENTSDB = 'opentsdb'
PLUGIN_ID_ELASTICSEARCH = 'elasticsearch'
PLUGIN_ID_CLOUDWATCH = 'cloudwatch'

# Target formats
TIME_SERIES_TARGET_FORMAT = 'time_series'
TABLE_TARGET_FORMAT = 'table'

# Table Transforms
AGGREGATIONS_TRANSFORM = 'timeseries_aggregations'
ANNOTATIONS_TRANSFORM = 'annotations'
COLUMNS_TRANSFORM = 'timeseries_to_columns'
JSON_TRANSFORM = 'json'
ROWS_TRANSFORM = 'timeseries_to_rows'
TABLE_TRANSFORM = 'table'

# AlertList show selections
ALERTLIST_SHOW_CURRENT = 'current'
ALERTLIST_SHOW_CHANGES = 'changes'

# AlertList state filter options
ALERTLIST_STATE_OK = 'ok'
ALERTLIST_STATE_PAUSED = 'paused'
ALERTLIST_STATE_NO_DATA = 'no_data'
ALERTLIST_STATE_EXECUTION_ERROR = 'execution_error'
ALERTLIST_STATE_ALERTING = 'alerting'
ALERTLIST_STATE_PENDING = 'pending'

# Alert Rule state filter options (Grafana 8.x)
ALERTRULE_STATE_DATA_OK = 'OK'
ALERTRULE_STATE_DATA_NODATA = 'No Data'
ALERTRULE_STATE_DATA_ALERTING = 'Alerting'
ALERTRULE_STATE_DATA_ERROR = 'Error'

# Display Sort Order
SORT_ASC = 1
SORT_DESC = 2
SORT_IMPORTANCE = 3

# Template
REFRESH_NEVER = 0
REFRESH_ON_DASHBOARD_LOAD = 1
REFRESH_ON_TIME_RANGE_CHANGE = 2
SHOW = 0
HIDE_LABEL = 1
HIDE_VARIABLE = 2
SORT_DISABLED = 0
SORT_ALPHA_ASC = 1
SORT_ALPHA_DESC = 2
SORT_NUMERIC_ASC = 3
SORT_NUMERIC_DESC = 4
SORT_ALPHA_IGNORE_CASE_ASC = 5
SORT_ALPHA_IGNORE_CASE_DESC = 6

GAUGE_CALC_LAST = 'last'
GAUGE_CALC_FIRST = 'first'
GAUGE_CALC_MIN = 'min'
GAUGE_CALC_MAX = 'max'
GAUGE_CALC_MEAN = 'mean'
GAUGE_CALC_TOTAL = 'sum'
GAUGE_CALC_COUNT = 'count'
GAUGE_CALC_RANGE = 'range'
GAUGE_CALC_DELTA = 'delta'
GAUGE_CALC_STEP = 'step'
GAUGE_CALC_DIFFERENCE = 'difference'
GAUGE_CALC_LOGMIN = 'logmin'
GAUGE_CALC_CHANGE_COUNT = 'changeCount'
GAUGE_CALC_DISTINCT_COUNT = 'distinctCount'

ORIENTATION_HORIZONTAL = 'horizontal'
ORIENTATION_VERTICAL = 'vertical'
ORIENTATION_AUTO = 'auto'

GAUGE_DISPLAY_MODE_BASIC = 'basic'
GAUGE_DISPLAY_MODE_LCD = 'lcd'
GAUGE_DISPLAY_MODE_GRADIENT = 'gradient'

GRAPH_TOOLTIP_MODE_NOT_SHARED = 0
GRAPH_TOOLTIP_MODE_SHARED_CROSSHAIR = 1
GRAPH_TOOLTIP_MODE_SHARED_TOOLTIP = 2  # Shared crosshair AND tooltip

DEFAULT_AUTO_COUNT = 30
DEFAULT_MIN_AUTO_INTERVAL = '10s'

DASHBOARD_LINK_ICON = Literal['bolt', 'cloud', 'dashboard', 'doc',
                              'external link', 'info', 'question']

# ---------------------------------------------------------------------------
# Mapping and Value Mappings
# ---------------------------------------------------------------------------

class Mapping(BaseModel):
    name: Any
    value: int

    def to_json_data(self) -> dict:
        return {'name': self.name, 'value': self.value}

MAPPING_TYPE_VALUE_TO_TEXT = 1
MAPPING_TYPE_RANGE_TO_TEXT = 2

MAPPING_VALUE_TO_TEXT = Mapping(name='value to text', value=MAPPING_TYPE_VALUE_TO_TEXT)
MAPPING_RANGE_TO_TEXT = Mapping(name='range to text', value=MAPPING_TYPE_RANGE_TO_TEXT)

# Value types for Stat panels
VTYPE_MIN = 'min'
VTYPE_MAX = 'max'
VTYPE_AVG = 'avg'
VTYPE_CURR = 'current'
VTYPE_TOTAL = 'total'
VTYPE_NAME = 'name'
VTYPE_FIRST = 'first'
VTYPE_DELTA = 'delta'
VTYPE_RANGE = 'range'
VTYPE_DEFAULT = VTYPE_AVG

# ---------------------------------------------------------------------------
# ePictBox and related classes
# ---------------------------------------------------------------------------

class ePictBox(BaseModel):
    """
    ePict Box.

    :param angle: Rotation angle of box
    :param backgroundColor: Dito
    :param blinkHigh: Blink if below threshold
    :param blinkLow: Blink if above threshold
    :param color: Text color
    :param colorHigh: High value color
    :param colorLow: Low value color
    :param colorMedium: In between value color
    :param colorSymbol: Whether to enable background color for symbol
    :param customSymbol: URL to custom symbol (will set symbol to "custom" if set)
    :param decimal: Number of decimals
    :param fontSize: Dito
    :param hasBackground: Whether to enable background color for text
    :param hasOrb: Whether an orb should be displayed
    :param hasSymbol: Whether a (custom) symbol should be displayed
    :param isUsingThresholds: Whether to enable thresholds.
    :param orbHideText: Whether to hide text next to orb
    :param orbLocation: Orb location (choose from 'Left', 'Right', 'Top' or 'Bottom')
    :param orbSize: Dito
    :param prefix: Value prefix to be displayed (e.g. °C)
    :param prefixSize: Dito
    :param selected: Dont know
    :param serie: Which series to use data from
    :param suffix: Value suffix to be displayed
    :param suffixSize: Dito
    :param symbol: Automatically placed by the plugin format: `data:image/svg+xml;base64,<base64>`
    :param symbolDefHeight: Dont know
    :param symbolDefWidth: Dont know
    :param symbolHeight: Dito
    :param symbolHideText: Whether to hide value text next to symbol
    :param symbolWidth: Dito
    :param text: Dont know
    :param thresholds: Coloring thresholds (if set, also enables isUsingThresholds)
    :param url: URL to open when clicked on
    :param xpos: X in (0, X size of image)
    :param ypos: Y in (0, Y size of image)
    """
    angle: int = 0
    backgroundColor: Any = "#000"  # Accepts RGBA, RGB, or str
    blinkHigh: bool = False
    blinkLow: bool = False
    color: Any = "#000"
    colorHigh: Any = "#000"
    colorLow: Any = "#000"
    colorMedium: Any = "#000"
    colorSymbol: bool = False
    customSymbol: str = ""
    decimal: int = 0
    fontSize: int = 12
    hasBackground: bool = False
    hasOrb: bool = False
    hasSymbol: bool = False
    isUsingThresholds: bool = False
    orbHideText: bool = False
    orbLocation: str = Field("Left", regex="^(Left|Right|Top|Bottom)$")
    orbSize: int = 13
    prefix: str = ""
    prefixSize: int = 10
    selected: bool = False
    serie: str = ""
    suffix: str = ""
    suffixSize: int = 10
    symbol: str = ""
    symbolDefHeight: int = 32
    symbolDefWidth: int = 32
    symbolHeight: int = 32
    symbolHideText: bool = False
    symbolWidth: int = 32
    text: str = "N/A"
    thresholds: str = ""
    url: str = ""
    xpos: int = 0
    ypos: int = 0

    def to_json_data(self) -> dict:
        computed_symbol = "custom" if self.customSymbol else self.symbol
        computed_isUsingThresholds = bool(self.thresholds)
        return {
            "angle": self.angle,
            "backgroundColor": self.backgroundColor,
            "blinkHigh": self.blinkHigh,
            "blinkLow": self.blinkLow,
            "color": self.color,
            "colorHigh": self.colorHigh,
            "colorLow": self.colorLow,
            "colorMedium": self.colorMedium,
            "colorSymbol": self.colorSymbol,
            "customSymbol": self.customSymbol,
            "decimal": self.decimal,
            "fontSize": self.fontSize,
            "hasBackground": self.hasBackground,
            "hasOrb": self.hasOrb,
            "hasSymbol": self.hasSymbol,
            "isUsingThresholds": computed_isUsingThresholds,
            "orbHideText": self.orbHideText,
            "orbLocation": self.orbLocation,
            "orbSize": self.orbSize,
            "prefix": self.prefix,
            "prefixSize": self.prefixSize,
            "selected": self.selected,
            "serie": self.serie,
            "suffix": self.suffix,
            "suffixSize": self.suffixSize,
            "symbol": computed_symbol,
            "symbolDefHeight": self.symbolDefHeight,
            "symbolDefWidth": self.symbolDefWidth,
            "symbolHeight": self.symbolHeight,
            "symbolHideText": self.symbolHideText,
            "symbolWidth": self.symbolWidth,
            "text": self.text,
            "thresholds": self.thresholds,
            "url": self.url,
            "xpos": self.xpos,
            "ypos": self.ypos,
        }

# ---------------------------------------------------------------------------
# Grid and Legend classes
# ---------------------------------------------------------------------------

class Grid(BaseModel):
    threshold1: Optional[Any] = None
    threshold1Color: RGBA = Field(default_factory=lambda: GREY1)
    threshold2: Optional[Any] = None
    threshold2Color: RGBA = Field(default_factory=lambda: GREY2)

    def to_json_data(self) -> dict:
        return {
            'threshold1': self.threshold1,
            'threshold1Color': self.threshold1Color.to_json_data(),
            'threshold2': self.threshold2,
            'threshold2Color': self.threshold2Color.to_json_data(),
        }

class Legend(BaseModel):
    avg: bool = False
    current: bool = False
    max: bool = False
    min: bool = False
    show: bool = True
    total: bool = False
    values: Optional[Any] = None
    alignAsTable: bool = False
    hideEmpty: bool = False
    hideZero: bool = False
    rightSide: bool = False
    sideWidth: Optional[Any] = None
    sort: Optional[Any] = None
    sortDesc: bool = False

    def to_json_data(self) -> dict:
        computed_values = (self.avg or self.current or self.max or self.min) if self.values is None else self.values
        return {
            'avg': self.avg,
            'current': self.current,
            'max': self.max,
            'min': self.min,
            'show': self.show,
            'total': self.total,
            'values': computed_values,
            'alignAsTable': self.alignAsTable,
            'hideEmpty': self.hideEmpty,
            'hideZero': self.hideZero,
            'rightSide': self.rightSide,
            'sideWidth': self.sideWidth,
            'sort': self.sort,
            'sortDesc': self.sortDesc,
        }

# ---------------------------------------------------------------------------
# Repeat and Target classes
# ---------------------------------------------------------------------------

def is_valid_max_per_row(value: Optional[int]) -> Optional[int]:
    if value is not None and not isinstance(value, int):
        raise ValueError("maxPerRow should either be None or an integer")
    return value

class Repeat(BaseModel):
    """
    Panel repetition settings.

    :param direction: The direction into which to repeat ('h' or 'v')
    :param variable: The name of the variable over whose values to repeat
    :param maxPerRow: The maximum number of panels per row in horizontal repetition
    """
    direction: Optional[Any] = None
    variable: Optional[Any] = None
    maxPerRow: Optional[int] = Field(default=None)

    @field_validator("maxPerRow")
    @classmethod
    def validate_maxPerRow(cls, v: Optional[int]) -> Optional[int]:
        return is_valid_max_per_row(v)

    def to_json_data(self) -> dict:
        return {
            'direction': self.direction,
            'variable': self.variable,
            'maxPerRow': self.maxPerRow,
        }

def is_valid_target(value: Any):
    if getattr(value, 'refId', "") == "":
        raise ValueError("Target should have non-empty 'refId' attribute")
    return value

class Target(BaseModel):
    """
    Metric to show.

    :param expr: Graphite way to select data.
    :param legendFormat: Target alias.
    """
    expr: str = ""
    format: str = TIME_SERIES_TARGET_FORMAT
    hide: bool = False
    legendFormat: str = ""
    interval: str = ""
    intervalFactor: int = 2
    metric: str = ""
    refId: str = ""
    step: int = DEFAULT_STEP
    target: str = ""
    instant: bool = False
    datasource: Optional[Any] = None

    def to_json_data(self) -> dict:
        return {
            'expr': self.expr,
            'query': self.expr,
            'target': self.target,
            'format': self.format,
            'hide': self.hide,
            'interval': self.interval,
            'intervalFactor': self.intervalFactor,
            'legendFormat': self.legendFormat,
            'alias': self.legendFormat,
            'metric': self.metric,
            'refId': self.refId,
            'step': self.step,
            'instant': self.instant,
            'datasource': self.datasource,
        }

class LokiTarget(BaseModel):
    """
    Target for Loki LogQL queries
    """
    datasource: str = ""
    expr: str = ""
    hide: bool = False

    def to_json_data(self) -> dict:
        return {
            'datasource': {'type': 'loki', 'uid': self.datasource},
            'expr': self.expr,
            'hide': self.hide,
            'queryType': 'range',
        }

class SqlTarget(Target):
    """
    Metric target to support SQL queries
    """
    rawSql: str = ""
    rawQuery: bool = True
    srcFilePath: str = ""
    sqlParams: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.srcFilePath:
            with open(self.srcFilePath, "r") as f:
                self.rawSql = f.read()
            if self.sqlParams:
                self.rawSql = self.rawSql.format(**self.sqlParams)

    def to_json_data(self) -> dict:
        super_json = super().to_json_data()
        super_json["rawSql"] = self.rawSql
        super_json["rawQuery"] = self.rawQuery
        return super_json

# ---------------------------------------------------------------------------
# Tooltip, XAxis, YAxis, and YAxes
# ---------------------------------------------------------------------------

class Tooltip(BaseModel):
    msResolution: bool = True
    shared: bool = True
    sort: int = 0
    valueType: str = CUMULATIVE

    def to_json_data(self) -> dict:
        return {
            'msResolution': self.msResolution,
            'shared': self.shared,
            'sort': self.sort,
            'value_type': self.valueType,
        }

def is_valid_xaxis_mode(v: str) -> str:
    XAXIS_MODES = ('time', 'series')
    if v not in XAXIS_MODES:
        raise ValueError(f"mode should be one of {XAXIS_MODES}")
    return v

class XAxis(BaseModel):
    """
    X Axis

    :param mode: Mode of axis can be time, series or histogram
    :param name: X axis name
    :param values: list of values eg. ["current"] or ["avg"]
    :param show: show X axis
    """
    mode: str = "time"
    name: Optional[Any] = None
    values: List[Any] = Field(default_factory=list)
    show: bool = True

    @field_validator("mode", mode=True)
    @classmethod
    def validate_mode(cls, v: str) -> str:
        return is_valid_xaxis_mode(v)

    def to_json_data(self) -> dict:
        return {
            'mode': self.mode,
            'name': self.name,
            'values': self.values,
            'show': self.show,
        }

class YAxis(BaseModel):
    """A single Y axis.

    Grafana graphs have two Y axes, a left one and a right one.

    :param decimals: Defines how many decimals are displayed for Y value.
    :param format: The display unit for the Y value
    :param label: The Y axis label.
    :param logBase: The scale to use for the Y value, linear, or logarithmic.
    :param max: The maximum Y value
    :param min: The minimum Y value
    :param show: Show or hide the axis
    """
    decimals: Optional[Any] = None
    format: Optional[Any] = None
    label: Optional[Any] = None
    logBase: int = 1
    max: Optional[Any] = None
    min: Optional[Any] = None
    show: bool = True

    def to_json_data(self) -> dict:
        return {
            'decimals': self.decimals,
            'format': self.format,
            'label': self.label,
            'logBase': self.logBase,
            'max': self.max,
            'min': self.min,
            'show': self.show,
        }

class YAxes(BaseModel):
    """
    The pair of Y axes on a Grafana graph.
    """
    left: YAxis = Field(default_factory=lambda: YAxis(format=SHORT_FORMAT))
    right: YAxis = Field(default_factory=lambda: YAxis(format=SHORT_FORMAT))

    def to_json_data(self) -> List[Any]:
        return [self.left.to_json_data(), self.right.to_json_data()]

def single_y_axis(**kwargs) -> YAxes:
    """Specify that a graph has a single Y axis."""
    axis = YAxis(**kwargs)
    return YAxes(left=axis, right=axis)

def to_y_axes(data: Any) -> YAxes:
    """Backwards compatibility for 'YAxes'."""
    if isinstance(data, YAxes):
        return data
    if not isinstance(data, (list, tuple)):
        raise ValueError(f"Y axes must be either YAxes or a list of two values, got {data!r}")
    if len(data) != 2:
        raise ValueError(f"Must specify exactly two YAxes, got {len(data)}: {data!r}")
    warnings.warn(
        "Specify Y axes using YAxes or single_y_axis, rather than a list/tuple",
        DeprecationWarning, stacklevel=3
    )
    return YAxes(left=data[0], right=data[1])

def _balance_panels(panels: List[Any]) -> List[Any]:
    """Resize panels so they are evenly spaced."""
    allotted_spans = sum(panel.span if panel.span else 0 for panel in panels)
    no_span_set = [panel for panel in panels if panel.span is None]
    auto_span = math.ceil((TOTAL_SPAN - allotted_spans) / (len(no_span_set) or 1))
    return [
        panel.copy(update={"span": auto_span}) if panel.span is None else panel
        for panel in panels
    ]

# ---------------------------------------------------------------------------
# GridPos, Annotations, DataLink, DataSourceInput, ConstantInput, DashboardLink, ExternalLink
# ---------------------------------------------------------------------------

class GridPos(BaseModel):
    """
    GridPos describes the panel size and position in grid coordinates.

    :param h: height of the panel (each unit represents 30 pixels)
    :param w: width of the panel (1-24)
    :param x: x coordinate of the panel
    :param y: y coordinate of the panel
    """
    h: int
    w: int
    x: int
    y: int

    def to_json_data(self) -> dict:
        return {'h': self.h, 'w': self.w, 'x': self.x, 'y': self.y}

class Annotations(BaseModel):
    list: List[Any] = Field(default_factory=list)

    def to_json_data(self) -> dict:
        return {'list': self.list}

class DataLink(BaseModel):
    title: Any
    linkUrl: str = ""
    isNewTab: bool = False

    def to_json_data(self) -> dict:
        return {
            'title': self.title,
            'url': self.linkUrl,
            'targetBlank': self.isNewTab,
        }

class DataSourceInput(BaseModel):
    name: Any
    label: Any
    pluginId: Any
    pluginName: Any
    description: str = ""

    def to_json_data(self) -> dict:
        return {
            'description': self.description,
            'label': self.label,
            'name': self.name,
            'pluginId': self.pluginId,
            'pluginName': self.pluginName,
            'type': 'datasource',
        }

class ConstantInput(BaseModel):
    name: Any
    label: Any
    value: Any
    description: str = ""

    def to_json_data(self) -> dict:
        return {
            'description': self.description,
            'label': self.label,
            'name': self.name,
            'type': 'constant',
            'value': self.value,
        }

class DashboardLink(BaseModel):
    """
    Create a link to other dashboards, or external resources.
    """
    asDropdown: bool = False
    icon: DASHBOARD_LINK_ICON = Field('external link')
    includeVars: bool = False
    keepTime: bool = True
    tags: List[str] = Field(default_factory=list)
    targetBlank: bool = False
    title: str = ""
    tooltip: str = ""
    type: DASHBOARD_TYPE = Field('dashboards')
    uri: str = ""

    def to_json_data(self) -> dict:
        return {
            'asDropdown': self.asDropdown,
            'icon': self.icon,
            'includeVars': self.includeVars,
            'keepTime': self.keepTime,
            'tags': self.tags,
            'targetBlank': self.targetBlank,
            'title': self.title,
            'tooltip': self.tooltip,
            'type': self.type,
            'url': self.uri,
        }

class ExternalLink(BaseModel):
    """
    ExternalLink creates a top-level link attached to a dashboard.
    """
    uri: Any
    title: Any
    keepTime: bool = False

    def to_json_data(self) -> dict:
        return {'keepTime': self.keepTime, 'title': self.title, 'type': 'link', 'url': self.uri}

# ---------------------------------------------------------------------------
# Template and Templating
# ---------------------------------------------------------------------------

class Template(BaseModel):
    """
    Template creates a new 'variable' for the dashboard.
    """
    name: Any
    query: Any
    _current: Dict[str, Any] = Field(default_factory=dict, exclude=True)
    default: Optional[Any] = None
    dataSource: Optional[Any] = None
    label: Optional[Any] = None
    allValue: Optional[Any] = None
    includeAll: bool = False
    multi: bool = False
    options: List[Any] = Field(default_factory=list)
    regex: Optional[Any] = None
    useTags: bool = False
    tagsQuery: Optional[Any] = None
    tagValuesQuery: Optional[Any] = None
    refresh: int = REFRESH_ON_DASHBOARD_LOAD
    type: str = "query"
    hide: int = SHOW
    sort: Any = SORT_ALPHA_ASC
    auto: bool = False
    autoCount: int = 30
    autoMin: Any = DEFAULT_MIN_AUTO_INTERVAL

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.type == 'custom':
            if not self.options:
                for value in str(self.query).split(','):
                    is_default = (value == self.default)
                    option = {'selected': is_default, 'text': value, 'value': value}
                    if is_default:
                        self._current = option
                    self.options.append(option)
            else:
                for option in self.options:
                    if option.get('selected'):
                        self._current = option
                        break
        else:
            self._current = {
                'selected': bool(self.default),
                'text': self.default,
                'value': self.default,
                'tags': [],
            }

    def to_json_data(self) -> dict:
        return {
            'allValue': self.allValue,
            'current': self._current,
            'datasource': self.dataSource,
            'hide': self.hide,
            'includeAll': self.includeAll,
            'label': self.label,
            'multi': self.multi,
            'name': self.name,
            'options': self.options,
            'query': self.query,
            'refresh': self.refresh,
            'regex': self.regex,
            'sort': self.sort,
            'type': self.type,
            'useTags': self.useTags,
            'tagsQuery': self.tagsQuery,
            'tagValuesQuery': self.tagValuesQuery,
            'auto': self.auto,
            'auto_min': self.autoMin,
            'auto_count': self.autoCount
        }

class Templating(BaseModel):
    list: List[Any] = Field(default_factory=list)

    def to_json_data(self) -> dict:
        return {'list': self.list}

# ---------------------------------------------------------------------------
# Time and TimePicker
# ---------------------------------------------------------------------------

class Time(BaseModel):
    start: Any
    end: Any

    def to_json_data(self) -> dict:
        return {'from': self.start, 'to': self.end}

DEFAULT_TIME = Time(start='now-1h', end='now')

class TimePicker(BaseModel):
    """
    Time Picker

    :param refreshIntervals: dashboard auto-refresh interval options
    :param timeOptions: dashboard time range options
    :param nowDelay: exclude recent data that may be incomplete
    :param hidden: hide the time picker from dashboard
    """
    refreshIntervals: List[Any]
    timeOptions: List[Any]
    nowDelay: Optional[Any] = None
    hidden: bool = False

    def to_json_data(self) -> dict:
        return {
            'refresh_intervals': self.refreshIntervals,
            'time_options': self.timeOptions,
            'nowDelay': self.nowDelay,
            'hidden': self.hidden
        }

DEFAULT_TIME_PICKER = TimePicker(
    refreshIntervals=['5s', '10s', '30s', '1m', '5m', '15m', '30m', '1h', '2h', '1d'],
    timeOptions=['5m', '15m', '1h', '6h', '12h', '24h', '2d', '7d', '30d']
)

# ---------------------------------------------------------------------------
# Evaluator and TimeRange
# ---------------------------------------------------------------------------

class Evaluator(BaseModel):
    type: Any
    params: Any

    def to_json_data(self) -> dict:
        return {'type': self.type, 'params': self.params}

def GreaterThan(value: Any) -> Evaluator:
    return Evaluator(type=EVAL_GT, params=[value])

def LowerThan(value: Any) -> Evaluator:
    return Evaluator(type=EVAL_LT, params=[value])

def WithinRange(from_value: Any, to_value: Any) -> Evaluator:
    return Evaluator(type=EVAL_WITHIN_RANGE, params=[from_value, to_value])

def OutsideRange(from_value: Any, to_value: Any) -> Evaluator:
    return Evaluator(type=EVAL_OUTSIDE_RANGE, params=[from_value, to_value])

def NoValue() -> Evaluator:
    return Evaluator(type=EVAL_NO_VALUE, params=[])

class TimeRange(BaseModel):
    """
    A time range for an alert condition.

    :param from_time: e.g. "5m" or "now"
    :param to_time: e.g. "5m" or "now"
    """
    from_time: Any
    to_time: Any

    def to_json_data(self) -> List[Any]:
        return [self.from_time, self.to_time]

# ---------------------------------------------------------------------------
# Alert Conditions and Expressions
# ---------------------------------------------------------------------------

class AlertCondition(BaseModel):
    """
    A condition on an alert.

    :param target: Metric the alert condition is based on.
    :param evaluator: Evaluator function.
    :param timeRange: TimeRange for the condition.
    :param operator: Combination operator.
    :param reducerType: Reducer type.
    :param useNewAlerts: Whether to use Grafana 8.x new alerts.
    :param type: Condition type.
    """
    target: Optional[Target] = None
    evaluator: Evaluator
    timeRange: Optional[TimeRange] = None
    operator: str = OP_AND
    reducerType: str = RTYPE_LAST
    useNewAlerts: bool = False
    type: str = Field(default=CTYPE_QUERY, alias="type")

    def __get_query_params(self) -> List[Any]:
        if self.useNewAlerts:
            return [self.target.refId] if self.target else []
        if self.target and self.timeRange:
            return [self.target.refId, self.timeRange.from_time, self.timeRange.to_time]
        return []

    def to_json_data(self) -> dict:
        condition = {
            'evaluator': self.evaluator.to_json_data(),
            'operator': {'type': self.operator},
            'query': {
                'model': self.target.to_json_data() if self.target else {},
                'params': self.__get_query_params(),
            },
            'reducer': {'params': [], 'type': self.reducerType},
            'type': self.type,
        }
        if self.useNewAlerts:
            condition['query'].pop('model', None)
        return condition

class AlertExpression(BaseModel):
    """
    An alert expression to be evaluated in Grafana v9.x+.

    :param refId: Expression reference ID.
    :param expression: Expression string.
    :param conditions: List of AlertConditions.
    :param expressionType: Expression type.
    :param hide: Whether to hide the alert.
    :param intervalMs: Evaluation interval in ms.
    :param maxDataPoints: Maximum data points.
    :param reduceFunction: Reducer function.
    :param reduceMode: Reducer mode.
    :param reduceReplaceWith: Replacement value.
    :param resampleWindow: Resample window.
    :param resampleDownsampler: Downsampler.
    :param resampleUpsampler: Upsampler.
    """
    refId: Any
    expression: str
    conditions: List[AlertCondition] = Field(default_factory=list)
    expressionType: str = EXP_TYPE_CLASSIC
    hide: bool = False
    intervalMs: int = 1000
    maxDataPoints: int = 43200
    reduceFunction: str = EXP_REDUCER_FUNC_MEAN
    reduceMode: str = EXP_REDUCER_MODE_STRICT
    reduceReplaceWith: Any = 0
    resampleWindow: str = "10s"
    resampleDownsampler: Any = "mean"
    resampleUpsampler: Any = "fillna"

    def to_json_data(self) -> dict:
        conds = []
        for condition in self.conditions:
            condition.useNewAlerts = True
            if condition.target is None:
                condition.target = Target(refId=self.expression)
            conds.append(condition.to_json_data())
        expression_obj = {
            'refId': self.refId,
            'queryType': '',
            'relativeTimeRange': {'from': 0, 'to': 0},
            'datasourceUid': '-100',
            'model': {
                'conditions': conds,
                'datasource': {'type': '__expr__', 'uid': '-100'},
                'expression': self.expression,
                'hide': self.hide,
                'intervalMs': self.intervalMs,
                'maxDataPoints': self.maxDataPoints,
                'refId': self.refId,
                'type': self.expressionType,
                'reducer': self.reduceFunction,
                'settings': {'mode': self.reduceMode, 'replaceWithValue': self.reduceReplaceWith},
                'downsampler': self.resampleDownsampler,
                'upsampler': self.resampleUpsampler,
                'window': self.resampleWindow
            }
        }
        return expression_obj

# ---------------------------------------------------------------------------
# Alert, AlertGroup, and Alert Rules
# ---------------------------------------------------------------------------

class Alert(BaseModel):
    """
    Alert object.

    :param name: Alert name.
    :param message: Alert message.
    :param alertConditions: Alert conditions.
    :param executionErrorState: Execution error state.
    :param frequency: Frequency of evaluation.
    :param handler: Alert handler.
    :param noDataState: No-data state.
    :param notifications: List of notifications.
    :param gracePeriod: Grace period.
    :param alertRuleTags: Alert rule tags.
    """
    name: Any
    message: Any
    alertConditions: Any
    executionErrorState: str = STATE_ALERTING
    frequency: str = "60s"
    handler: int = 1
    noDataState: str = STATE_NO_DATA
    notifications: List[Any] = Field(default_factory=list)
    gracePeriod: str = "5m"
    alertRuleTags: Dict[str, str] = Field(default_factory=dict)

    def to_json_data(self) -> dict:
        return {
            'conditions': self.alertConditions,
            'executionErrorState': self.executionErrorState,
            'frequency': self.frequency,
            'handler': self.handler,
            'message': self.message,
            'name': self.name,
            'noDataState': self.noDataState,
            'notifications': self.notifications,
            'for': self.gracePeriod,
            'alertRuleTags': self.alertRuleTags,
        }

class AlertGroup(BaseModel):
    """
    Create an alert group of Grafana 8.x alerts.

    :param name: Alert group name.
    :param rules: List of AlertRule objects.
    :param folder: Folder for alerts.
    :param evaluateInterval: Evaluation interval.
    """
    name: Any
    rules: List[Any] = Field(default_factory=list)
    folder: str = "alert"
    evaluateInterval: str = "1m"

    def group_rules(self, rules: List[Any]) -> List[Any]:
        grouped_rules = []
        for each in rules:
            each.rule_group = self.name
            grouped_rules.append(each.to_json_data())
        return grouped_rules

    def to_json_data(self) -> dict:
        return {
            'name': self.name,
            'interval': self.evaluateInterval,
            'rules': self.group_rules(self.rules),
            'folder': self.folder
        }

def is_valid_triggers(value: List[Any]) -> List[Any]:
    for trigger in value:
        if not isinstance(trigger, tuple):
            raise ValueError("triggers must be a list of [(Target, AlertCondition)] tuples")
        if list(map(type, trigger)) != [Target, AlertCondition]:
            raise ValueError("triggers must be a list of [(Target, AlertCondition)] tuples")
        is_valid_target(trigger[0])
    return value

def is_valid_triggersv9(value: List[Any]) -> List[Any]:
    for trigger in value:
        if not (isinstance(trigger, Target) or isinstance(trigger, AlertExpression)):
            raise ValueError("triggers must either be a Target or AlertExpression")
        if isinstance(trigger, Target):
            is_valid_target(trigger)
    return value

class AlertRulev8(BaseModel):
    """
    Create a Grafana 8.x Alert Rule.

    :param title: Alert title.
    :param triggers: List of (Target, AlertCondition) tuples.
    :param annotations: Annotations.
    :param labels: Labels.
    :param evaluateInterval: Evaluation frequency.
    :param evaluateFor: Duration before alert.
    :param noDataAlertState: No-data state.
    :param errorAlertState: Error state.
    :param timeRangeFrom: Start time range.
    :param timeRangeTo: End time range.
    :param uid: Unique alert UID.
    :param dashboard_uid: Dashboard UID.
    :param panel_id: Panel ID.
    """
    title: Any
    triggers: List[Any] = Field(..., validator=is_valid_triggers)
    annotations: Dict[Any, Any] = Field(default_factory=dict)
    labels: Dict[Any, Any] = Field(default_factory=dict)
    evaluateInterval: str = DEFAULT_ALERT_EVALUATE_INTERVAL
    evaluateFor: str = DEFAULT_ALERT_EVALUATE_FOR
    noDataAlertState: str = Field(default=ALERTRULE_STATE_DATA_ALERTING)
    errorAlertState: str = Field(default=ALERTRULE_STATE_DATA_ALERTING)
    timeRangeFrom: int = 300
    timeRangeTo: int = 0
    uid: Optional[str] = None
    dashboard_uid: str = ""
    panel_id: int = 0
    rule_group: str = ""

    def to_json_data(self) -> dict:
        data = []
        conditions = []
        for target, condition in self.triggers:
            data.append({
                "refId": target.refId,
                "relativeTimeRange": {"from": self.timeRangeFrom, "to": self.timeRangeTo},
                "datasourceUid": target.datasource,
                "model": target.to_json_data(),
            })
            condition.useNewAlerts = True
            condition.target = target
            conditions.append(condition.to_json_data())
        data.append({
            "refId": "CONDITION",
            "datasourceUid": "-100",
            "model": {"conditions": conditions, "refId": "CONDITION", "type": "classic_conditions"}
        })
        return {
            "for": self.evaluateFor,
            "labels": self.labels,
            "annotations": self.annotations,
            "grafana_alert": {
                "title": self.title,
                "condition": "CONDITION",
                "data": data,
                "intervalSeconds": self.evaluateInterval,
                "exec_err_state": self.errorAlertState,
                "no_data_state": self.noDataAlertState,
                "uid": self.uid,
                "rule_group": self.rule_group,
            }
        }

class AlertRulev9(BaseModel):
    """
    Create a Grafana 9.x+ Alert Rule.

    :param title: Alert title.
    :param triggers: List of Targets or AlertExpressions.
    :param annotations: Annotations.
    :param labels: Labels.
    :param condition: Condition reference (e.g. "B").
    :param evaluateFor: Duration before alert fires.
    :param noDataAlertState: No-data state.
    :param errorAlertState: Error state.
    :param timeRangeFrom: Start time range.
    :param timeRangeTo: End time range.
    :param uid: Unique alert UID.
    :param dashboard_uid: Dashboard UID.
    :param panel_id: Panel ID.
    """
    title: Any
    triggers: List[Any] = Field(default_factory=list, validator=is_valid_triggersv9)
    annotations: Dict[Any, Any] = Field(default_factory=dict)
    labels: Dict[Any, Any] = Field(default_factory=dict)
    evaluateFor: str = DEFAULT_ALERT_EVALUATE_FOR
    noDataAlertState: str = Field(default=ALERTRULE_STATE_DATA_ALERTING)
    errorAlertState: str = Field(default=ALERTRULE_STATE_DATA_ALERTING)
    condition: str = "B"
    timeRangeFrom: int = 300
    timeRangeTo: int = 0
    uid: Optional[str] = None
    dashboard_uid: str = ""
    panel_id: int = 0

    def to_json_data(self) -> dict:
        data = []
        for trigger in self.triggers:
            if isinstance(trigger, Target):
                data.append({
                    "refId": trigger.refId,
                    "relativeTimeRange": {"from": self.timeRangeFrom, "to": self.timeRangeTo},
                    "datasourceUid": trigger.datasource,
                    "model": trigger.to_json_data(),
                })
            else:
                data.append(trigger.to_json_data())
        return {
            "uid": self.uid,
            "for": self.evaluateFor,
            "labels": self.labels,
            "annotations": self.annotations,
            "grafana_alert": {
                "title": self.title,
                "condition": self.condition,
                "data": data,
                "no_data_state": self.noDataAlertState,
                "exec_err_state": self.errorAlertState,
            },
        }

class AlertFileBasedProvisioning(BaseModel):
    """
    Used to generate JSON data for file based alert provisioning.

    :param groups: List of AlertGroups.
    """
    groups: Any

    def to_json_data(self) -> dict:
        return {'apiVersion': 1, 'groups': self.groups}

class Notification(BaseModel):
    uid: Any

    def to_json_data(self) -> dict:
        return {'uid': self.uid}

# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

class Dashboard(BaseModel):
    title: Any
    annotations: Annotations = Field(default_factory=Annotations)
    description: str = ""
    editable: bool = True
    gnetId: Optional[Any] = None
    graphTooltip: int = 0  # GRAPH_TOOLTIP_MODE_NOT_SHARED
    hideControls: bool = False
    id: Optional[Any] = None
    inputs: List[Any] = Field(default_factory=list)
    links: List[Any] = Field(default_factory=list)
    panels: List[Any] = Field(default_factory=list)
    refresh: str = DEFAULT_REFRESH
    rows: List[Any] = Field(default_factory=list)
    schemaVersion: int = SCHEMA_VERSION
    sharedCrosshair: bool = False
    style: Any = DARK_STYLE
    tags: List[Any] = Field(default_factory=list)
    templating: Templating = Field(default_factory=Templating)
    time: Time = Field(default_factory=lambda: DEFAULT_TIME)
    timePicker: TimePicker = Field(default_factory=lambda: DEFAULT_TIME_PICKER)
    timezone: Any = UTC
    version: int = 0
    uid: Optional[Any] = None

    def _iter_panels(self):
        for row in self.rows:
            for panel in row._iter_panels():
                yield panel
        for panel in self.panels:
            yield panel
            if hasattr(panel, '_iter_panels'):
                for row_panel in panel._iter_panels():
                    yield row_panel

    def _map_panels(self, f) -> Any:
        new_rows = [row._map_panels(f) for row in self.rows]
        new_panels = [panel._map_panels(f) for panel in self.panels]
        return self.copy(update={"rows": new_rows, "panels": new_panels})

    def auto_panel_ids(self):
        """Assign unique IDs to panels without IDs."""
        ids = {panel.id for panel in self._iter_panels() if panel.id}
        auto_ids = (i for i in itertools.count(1) if i not in ids)
        def set_id(panel):
            return panel if panel.id else panel.copy(update={"id": next(auto_ids)})
        return self._map_panels(set_id)

    def to_json_data(self) -> dict:
        if self.panels and self.rows:
            print(
                "Warning: You are using both panels and rows in this dashboard, please use one or the other. "
                "Panels should be used in preference over rows."
            )
        return {
            '__inputs': self.inputs,
            'annotations': self.annotations.to_json_data(),
            'description': self.description,
            'editable': self.editable,
            'gnetId': self.gnetId,
            'graphTooltip': self.graphTooltip,
            'hideControls': self.hideControls,
            'id': self.id,
            'links': self.links,
            'panels': self.panels if not self.rows else [],
            'refresh': self.refresh,
            'rows': self.rows,
            'schemaVersion': self.schemaVersion,
            'sharedCrosshair': self.sharedCrosshair,
            'style': self.style,
            'tags': self.tags,
            'templating': self.templating.to_json_data(),
            'title': self.title,
            'time': self.time.to_json_data(),
            'timepicker': self.timePicker.to_json_data(),
            'timezone': self.timezone,
            'version': self.version,
            'uid': self.uid,
        }

def _deep_update(base_dict: dict, extra_dict: Optional[dict]) -> dict:
    if extra_dict is None:
        return base_dict
    for k, v in extra_dict.items():
        if k in base_dict and hasattr(base_dict[k], "to_json_data"):
            base_dict[k] = base_dict[k].to_json_data()
        if k in base_dict and isinstance(base_dict[k], dict):
            _deep_update(base_dict[k], v)
        else:
            base_dict[k] = v
    return base_dict

# ---------------------------------------------------------------------------
# Panel and its subclasses
# ---------------------------------------------------------------------------

class Panel(BaseModel):
    """
    Generic panel for shared defaults.

    :param dataSource: Grafana datasource name.
    :param targets: List of metric targets.
    :param title: Panel title.
    :param cacheTimeout: Query cache timeout.
    :param description: Panel description.
    :param editable: Whether panel is editable.
    :param error: Panel error state.
    :param height: Panel height.
    :param gridPos: Grid position.
    :param hideTimeOverride: Whether to hide time overrides.
    :param id: Panel ID.
    :param interval: Query interval.
    :param links: Additional links.
    :param maxDataPoints: Maximum data points.
    :param minSpan: Minimum span.
    :param repeat: Repeat settings.
    :param span: Panel span.
    :param thresholds: Thresholds.
    :param thresholdType: Type of threshold.
    :param timeFrom: Time override.
    :param timeShift: Time shift.
    :param transparent: Whether panel is transparent.
    :param transformations: Transformations.
    :param extraJson: Extra JSON overrides.
    """
    dataSource: Optional[Any] = None
    targets: List[Any] = Field(default_factory=list)
    title: str = ""
    cacheTimeout: Optional[Any] = None
    description: Optional[Any] = None
    editable: bool = True
    error: bool = False
    height: Optional[Any] = None
    gridPos: Optional[Any] = None
    hideTimeOverride: bool = False
    id: Optional[Any] = None
    interval: Optional[Any] = None
    links: List[Any] = Field(default_factory=list)
    maxDataPoints: int = 100
    minSpan: Optional[Any] = None
    repeat: Repeat = Field(default_factory=Repeat)
    span: Optional[Any] = None
    thresholds: List[Any] = Field(default_factory=list)
    thresholdType: str = "absolute"
    timeFrom: Optional[Any] = None
    timeShift: Optional[Any] = None
    transparent: bool = False
    transformations: List[Any] = Field(default_factory=list)
    extraJson: Optional[Dict[Any, Any]] = None

    def _map_panels(self, f) -> Any:
        return f(self)

    def panel_json(self, overrides: dict) -> dict:
        res = {
            'cacheTimeout': self.cacheTimeout,
            'datasource': self.dataSource,
            'description': self.description,
            'editable': self.editable,
            'error': self.error,
            'fieldConfig': {
                'defaults': {
                    'thresholds': {'mode': self.thresholdType, 'steps': self.thresholds},
                },
            },
            'height': self.height,
            'gridPos': self.gridPos,
            'hideTimeOverride': self.hideTimeOverride,
            'id': self.id,
            'interval': self.interval,
            'links': self.links,
            'maxDataPoints': self.maxDataPoints,
            'minSpan': self.minSpan,
            'repeat': self.repeat.variable,
            'repeatDirection': self.repeat.direction,
            'maxPerRow': self.repeat.maxPerRow,
            'span': self.span,
            'targets': self.targets,
            'timeFrom': self.timeFrom,
            'timeShift': self.timeShift,
            'title': self.title,
            'transparent': self.transparent,
            'transformations': self.transformations,
        }
        _deep_update(res, overrides)
        _deep_update(res, self.extraJson)
        return res

class ePict(Panel):
    """
    Generates ePict panel json structure.
    https://grafana.com/grafana/plugins/larona-epict-panel/

    :param autoScale: Whether to auto scale image to panel size.
    :param bgURL: Where to load the image from.
    :param boxes: The info boxes to be placed on the image.
    """
    bgURL: str = ""
    autoScale: bool = True
    boxes: List[ePictBox] = Field(default_factory=list)

    def to_json_data(self) -> dict:
        graph_object = {
            'type': EPICT_TYPE,
            'options': {
                'autoScale': self.autoScale,
                'bgURL': self.bgURL,
                'boxes': [box.to_json_data() for box in self.boxes],
            }
        }
        return self.panel_json(graph_object)

class RowPanel(Panel):
    """
    Generates Row panel json structure.

    :param title: Title of the panel.
    :param collapsed: Whether the row is collapsed.
    :param panels: List of panels in the row.
    """
    panels: List[Any] = Field(default_factory=list)
    collapsed: bool = False

    def _iter_panels(self):
        return iter(self.panels)

    def _map_panels(self, f):
        new_obj = self.copy(update={"panels": [f(panel) for panel in self.panels]})
        return new_obj

    def to_json_data(self) -> dict:
        return self.panel_json({
            'collapsed': self.collapsed,
            'panels': [p.to_json_data() for p in self.panels],
            'type': ROW_TYPE
        })

class Row(BaseModel):
    """
    Legacy support for old row, when not used with gridPos.
    """
    panels: List[Any] = Field(default_factory=list)
    collapse: bool = False
    editable: bool = True
    height: Pixels = DEFAULT_ROW_HEIGHT
    showTitle: Optional[Any] = None
    title: Optional[Any] = None
    repeat: Optional[Any] = None

    def _iter_panels(self):
        return iter(self.panels)

    def _map_panels(self, f):
        new_panels = [f(panel) for panel in self.panels]
        return self.copy(update={"panels": new_panels})

    def to_json_data(self) -> dict:
        showTitle_val = False
        title_val = "New row"
        if self.title is not None:
            showTitle_val = True
            title_val = self.title
        if self.showTitle is not None:
            showTitle_val = self.showTitle
        return {
            'collapse': self.collapse,
            'editable': self.editable,
            'height': self.height.to_json_data(),
            'panels': [p.to_json_data() for p in self.panels],
            'showTitle': showTitle_val,
            'title': title_val,
            'repeat': self.repeat,
        }

class Graph(Panel):
    """
    Generates Graph panel json structure.
    """
    alert: Optional[Any] = None
    alertThreshold: bool = True
    aliasColors: Dict[Any, Any] = Field(default_factory=dict)
    align: bool = False
    alignLevel: int = 0
    bars: bool = False
    dataLinks: List[Any] = Field(default_factory=list)
    error: bool = False
    fill: int = 1
    fillGradient: int = 0
    grid: Grid = Field(default_factory=Grid)
    isNew: bool = True
    legend: Legend = Field(default_factory=Legend)
    lines: bool = True
    lineWidth: Any = DEFAULT_LINE_WIDTH
    nullPointMode: Any = NULL_CONNECTED
    percentage: bool = False
    pointRadius: Any = DEFAULT_POINT_RADIUS
    points: bool = False
    renderer: Any = DEFAULT_RENDERER
    seriesOverrides: List[Any] = Field(default_factory=list)
    stack: bool = False
    steppedLine: bool = False
    tooltip: Tooltip = Field(default_factory=Tooltip)
    thresholds: List[Any] = Field(default_factory=list)
    unit: str = ""
    xAxis: XAxis = Field(default_factory=XAxis)
    yAxes: YAxes = Field(default_factory=YAxes)

    def to_json_data(self) -> dict:
        graphObject = {
            'aliasColors': self.aliasColors,
            'bars': self.bars,
            'error': self.error,
            'fieldConfig': {
                'defaults': {'unit': self.unit},
            },
            'fill': self.fill,
            'grid': self.grid.to_json_data(),
            'isNew': self.isNew,
            'legend': self.legend.to_json_data(),
            'lines': self.lines,
            'linewidth': self.lineWidth,
            'minSpan': self.minSpan,
            'nullPointMode': self.nullPointMode,
            'options': {
                'dataLinks': self.dataLinks,
                'alertThreshold': self.alertThreshold,
            },
            'percentage': self.percentage,
            'pointradius': self.pointRadius,
            'points': self.points,
            'renderer': self.renderer,
            'seriesOverrides': self.seriesOverrides,
            'stack': self.stack,
            'steppedLine': self.steppedLine,
            'tooltip': self.tooltip.to_json_data(),
            'thresholds': self.thresholds,
            'type': GRAPH_TYPE,
            'xaxis': self.xAxis.to_json_data(),
            'yaxes': self.yAxes.to_json_data(),
            'yaxis': {'align': self.align, 'alignLevel': self.alignLevel}
        }
        if self.alert:
            graphObject['alert'] = self.alert
            graphObject['thresholds'] = []
        if self.thresholds and self.alert:
            print("Warning: Graph threshold ignored as Alerts defined")
        return self.panel_json(graphObject)

    def _iter_targets(self):
        for t in self.targets:
            yield t

    def _map_targets(self, f):
        new_targets = [f(t) for t in self.targets]
        return self.copy(update={"targets": new_targets})

    def auto_ref_ids(self):
        ref_ids = {t.refId for t in self._iter_targets() if t.refId}
        double_candidate_refs = [p[0] + p[1] for p in itertools.product(string.ascii_uppercase, repeat=2)]
        candidate_ref_ids = itertools.chain(string.ascii_uppercase, double_candidate_refs)
        auto_ref_ids = (i for i in candidate_ref_ids if i not in ref_ids)
        def set_refid(t):
            return t if t.refId else t.copy(update={"refId": next(auto_ref_ids)})
        return self._map_targets(set_refid)

class TimeSeries(Panel):
    """
    Generates Time Series panel json structure added in Grafana v8.
    """
    axisPlacement: str = "auto"
    axisLabel: str = ""
    barAlignment: int = 0
    colorMode: str = "palette-classic"
    drawStyle: str = "line"
    fillOpacity: int = 0
    gradientMode: str = "none"
    legendDisplayMode: str = "list"
    legendPlacement: str = "bottom"
    legendCalcs: List[str] = Field(default_factory=list)
    lineInterpolation: str = "linear"
    lineWidth: int = 1
    mappings: List[Any] = Field(default_factory=list)
    overrides: List[Any] = Field(default_factory=list)
    pointSize: int = 5
    scaleDistributionType: str = "linear"
    scaleDistributionLog: int = 2
    spanNulls: bool = False
    showPoints: str = "auto"
    stacking: Dict[Any, Any] = Field(default_factory=dict)
    tooltipMode: str = "single"
    tooltipSort: str = "none"
    unit: str = ""
    thresholdsStyleMode: str = "off"
    valueMin: Optional[int] = None
    valueMax: Optional[int] = None
    valueDecimals: Optional[int] = None
    axisSoftMin: Optional[int] = None
    axisSoftMax: Optional[int] = None

    def to_json_data(self) -> dict:
        return self.panel_json({
            'fieldConfig': {
                'defaults': {
                    'color': {'mode': self.colorMode},
                    'custom': {
                        'axisPlacement': self.axisPlacement,
                        'axisLabel': self.axisLabel,
                        'drawStyle': self.drawStyle,
                        'lineInterpolation': self.lineInterpolation,
                        'barAlignment': self.barAlignment,
                        'lineWidth': self.lineWidth,
                        'fillOpacity': self.fillOpacity,
                        'gradientMode': self.gradientMode,
                        'spanNulls': self.spanNulls,
                        'showPoints': self.showPoints,
                        'pointSize': self.pointSize,
                        'stacking': self.stacking,
                        'scaleDistribution': {'type': self.scaleDistributionType, 'log': self.scaleDistributionLog},
                        'hideFrom': {'tooltip': False, 'viz': False, 'legend': False},
                        'thresholdsStyle': {'mode': self.thresholdsStyleMode},
                        'axisSoftMin': self.axisSoftMin,
                        'axisSoftMax': self.axisSoftMax
                    },
                    'mappings': self.mappings,
                    "min": self.valueMin,
                    "max": self.valueMax,
                    "decimals": self.valueDecimals,
                    'unit': self.unit
                },
                'overrides': self.overrides
            },
            'options': {
                'legend': {'displayMode': self.legendDisplayMode, 'placement': self.legendPlacement, 'calcs': self.legendCalcs},
                'tooltip': {'mode': self.tooltipMode, 'sort': self.tooltipSort}
            },
            'type': TIMESERIES_TYPE,
        })

# ---------------------------------------------------------------------------
# ValueMap, SparkLine, Gauge, RangeMap, and Discrete Panel
# ---------------------------------------------------------------------------

class ValueMap(BaseModel):
    """
    Generates JSON structure for a value mapping item.
    """
    text: Any
    value: Any
    op: str = "="

    def to_json_data(self) -> dict:
        return {'op': self.op, 'text': self.text, 'value': self.value}

class SparkLine(BaseModel):
    fillColor: RGBA = Field(default_factory=lambda: BLUE_RGBA)
    full: bool = False
    lineColor: RGB = Field(default_factory=lambda: BLUE_RGB)
    show: bool = False

    def to_json_data(self) -> dict:
        return {
            'fillColor': self.fillColor.to_json_data(),
            'full': self.full,
            'lineColor': self.lineColor.to_json_data(),
            'show': self.show,
        }

class Gauge(BaseModel):
    minValue: int = 0
    maxValue: int = 100
    show: bool = False
    thresholdLabels: bool = False
    thresholdMarkers: bool = True

    def to_json_data(self) -> dict:
        return {
            'maxValue': self.maxValue,
            'minValue': self.minValue,
            'show': self.show,
            'thresholdLabels': self.thresholdLabels,
            'thresholdMarkers': self.thresholdMarkers,
        }

class RangeMap(BaseModel):
    start: Any
    end: Any
    text: Any

    def to_json_data(self) -> dict:
        return {'from': self.start, 'to': self.end, 'text': self.text}

class DiscreteColorMappingItem(BaseModel):
    """
    Generates JSON structure for a value mapping item for discrete panels.
    """
    text: str
    color: Any = GREY1

    def to_json_data(self) -> dict:
        return {
            "color": self.color.to_json_data() if hasattr(self.color, "to_json_data") else self.color,
            "text": self.text,
        }

class Discrete(Panel):
    """
    Generates Discrete panel JSON structure.
    https://grafana.com/grafana/plugins/natel-discrete-panel/
    """
    backgroundColor: Any = Field(default=RGBA(r=128, g=128, b=128, a=0.1))
    lineColor: Any = Field(default=RGBA(r=0, g=0, b=0, a=0.1))
    metricNameColor: Any = "#000000"
    timeTextColor: Any = "#d8d9da"
    valueTextColor: Any = "#000000"
    decimals: int = 0
    legendPercentDecimals: int = 0
    rowHeight: int = 50
    textSize: int = 24
    textSizeTime: int = 12
    units: str = "none"
    legendSortBy: str = "-ms"
    highlightOnMouseover: bool = True
    showLegend: bool = True
    showLegendPercent: bool = True
    showLegendNames: bool = True
    showLegendValues: bool = True
    showTimeAxis: bool = True
    use12HourClock: bool = False
    writeMetricNames: bool = False
    writeLastValue: bool = True
    writeAllValues: bool = False
    showDistinctCount: Optional[Any] = None
    showLegendCounts: Optional[Any] = None
    showLegendTime: Optional[Any] = None
    showTransitionCount: Optional[Any] = None
    colorMaps: List[DiscreteColorMappingItem] = Field(default_factory=list)
    rangeMaps: List[RangeMap] = Field(default_factory=list)
    valueMaps: List[ValueMap] = Field(default_factory=list)

    def to_json_data(self) -> dict:
        graphObject = {
            'type': DISCRETE_TYPE,
            'backgroundColor': self.backgroundColor.to_json_data() if hasattr(self.backgroundColor, "to_json_data") else self.backgroundColor,
            'lineColor': self.lineColor.to_json_data() if hasattr(self.lineColor, "to_json_data") else self.lineColor,
            'metricNameColor': self.metricNameColor,
            'timeTextColor': self.timeTextColor,
            'valueTextColor': self.valueTextColor,
            'legendPercentDecimals': self.legendPercentDecimals,
            'decimals': self.decimals,
            'rowHeight': self.rowHeight,
            'textSize': self.textSize,
            'textSizeTime': self.textSizeTime,
            'units': self.units,
            'legendSortBy': self.legendSortBy,
            'highlightOnMouseover': self.highlightOnMouseover,
            'showLegend': self.showLegend,
            'showLegendPercent': self.showLegendPercent,
            'showLegendNames': self.showLegendNames,
            'showLegendValues': self.showLegendValues,
            'showTimeAxis': self.showTimeAxis,
            'use12HourClock': self.use12HourClock,
            'writeMetricNames': self.writeMetricNames,
            'writeLastValue': self.writeLastValue,
            'writeAllValues': self.writeAllValues,
            'showDistinctCount': self.showDistinctCount,
            'showLegendCounts': self.showLegendCounts,
            'showLegendTime': self.showLegendTime,
            'showTransitionCount': self.showTransitionCount,
            'colorMaps': [cm.to_json_data() for cm in self.colorMaps],
            'rangeMaps': [rm.to_json_data() for rm in self.rangeMaps],
            'valueMaps': [vm.to_json_data() for vm in self.valueMaps],
        }
        return self.panel_json(graphObject)

# ---------------------------------------------------------------------------
# Text, AlertList, and Stat Panels
# ---------------------------------------------------------------------------

class Text(Panel):
    """
    Generates a Text panel.
    """
    content: str = ""
    error: bool = False
    mode: str = Field(default=TEXT_MODE_MARKDOWN, regex=f"^({TEXT_MODE_MARKDOWN}|{TEXT_MODE_HTML}|{TEXT_MODE_TEXT})$")

    def to_json_data(self) -> dict:
        return self.panel_json({
            'type': TEXT_TYPE,
            'error': self.error,
            'options': {'content': self.content, 'mode': self.mode},
        })

class AlertList(BaseModel):
    """
    Generates the AlertList Panel.
    """
    dashboardTags: List[str] = Field(default_factory=list)
    description: str = ""
    gridPos: Optional[GridPos] = None
    id: Optional[Any] = None
    limit: int = DEFAULT_LIMIT
    links: List[Any] = Field(default_factory=list)
    nameFilter: str = ""
    onlyAlertsOnDashboard: bool = True
    show: Any = ALERTLIST_SHOW_CURRENT
    sortOrder: int = SORT_ASC
    span: int = 6
    stateFilter: List[Any] = Field(default_factory=list)
    title: str = ""
    transparent: bool = False
    alertName: str = ""

    def to_json_data(self) -> dict:
        return {
            'dashboardTags': self.dashboardTags,
            'description': self.description,
            'gridPos': self.gridPos.to_json_data() if self.gridPos else None,
            'id': self.id,
            'limit': self.limit,
            'links': self.links,
            'nameFilter': self.nameFilter,
            'onlyAlertsOnDashboard': self.onlyAlertsOnDashboard,
            'show': self.show,
            'sortOrder': self.sortOrder,
            'span': self.span,
            'stateFilter': self.stateFilter,
            'title': self.title,
            'transparent': self.transparent,
            'type': ALERTLIST_TYPE,
            "options": {"alertName": self.alertName},
        }

class Stat(Panel):
    """
    Generates Stat panel json structure.
    """
    alignment: str = "auto"
    color: Optional[Any] = None
    colorMode: str = "value"
    decimals: Optional[Any] = None
    format: str = "none"
    graphMode: str = "area"
    mappings: List[Any] = Field(default_factory=list)
    noValue: str = "none"
    orientation: str = "auto"
    overrides: List[Any] = Field(default_factory=list)
    reduceCalc: str = "mean"
    fields: str = ""
    textMode: str = "auto"
    thresholds: str = ""

    def to_json_data(self) -> dict:
        return self.panel_json({
            'fieldConfig': {
                'defaults': {
                    'color': self.color,
                    'custom': {},
                    'decimals': self.decimals,
                    'mappings': self.mappings,
                    'unit': self.format,
                    'noValue': self.noValue
                },
                'overrides': self.overrides
            },
            'options': {
                'textMode': self.textMode,
                'colorMode': self.colorMode,
                'graphMode': self.graphMode,
                'justifyMode': self.alignment,
                'orientation': self.orientation,
                'reduceOptions': {
                    'calcs': [self.reduceCalc],
                    'fields': self.fields,
                    'values': False
                }
            },
            'type': STAT_TYPE,
        })

class StatValueMappingItem(BaseModel):
    """
    Generates JSON structure for a value mapping item for Stat panels.
    """
    text: Any
    mapValue: str = ""
    color: str = ""
    index: Optional[Any] = None

    def to_json_data(self) -> dict:
        return {
            self.mapValue: {
                'text': self.text,
                'color': self.color,
                'index': self.index
            }
        }

class StatValueMappings(BaseModel):
    """
    Generates JSON structure for the value mappings for the Stat panel.
    """
    mappingItems: List[StatValueMappingItem] = Field(default_factory=list)

    def __init__(self, *mappings: StatValueMappingItem):
        super().__init__(mappingItems=list(mappings))

    def to_json_data(self) -> dict:
        ret_dict = {'type': 'value', 'options': {}}
        for item in self.mappingItems:
            ret_dict['options'].update(item.to_json_data())
        return ret_dict

class StatRangeMappings(BaseModel):
    """
    Generates JSON structure for the range mappings for the Stat panel.
    """
    text: Any
    startValue: int = 0
    endValue: int = 0
    color: str = ""
    index: Optional[Any] = None

    def to_json_data(self) -> dict:
        return {
            'type': 'range',
            'options': {
                'from': self.startValue,
                'to': self.endValue,
                'result': {'text': self.text, 'color': self.color, 'index': self.index}
            }
        }

class StatMapping(BaseModel):
    """
    Deprecated Grafana v8: Generates JSON for value mapping.
    """
    text: Any
    mapValue: str = ""
    startValue: str = ""
    endValue: str = ""
    id: Optional[Any] = None

    def to_json_data(self) -> dict:
        mappingType = MAPPING_TYPE_VALUE_TO_TEXT if self.mapValue else MAPPING_TYPE_RANGE_TO_TEXT
        return {
            'operator': '',
            'text': self.text,
            'type': mappingType,
            'value': self.mapValue,
            'from': self.startValue,
            'to': self.endValue,
            'id': self.id
        }

class StatValueMapping(BaseModel):
    """
    Deprecated Grafana v8: Generates JSON for stat value mapping.
    """
    text: Any
    mapValue: str = ""
    id: Optional[Any] = None

    def to_json_data(self) -> dict:
        return StatMapping(text=self.text, mapValue=self.mapValue, id=self.id).to_json_data()

class StatRangeMapping(BaseModel):
    """
    Deprecated Grafana v8: Generates JSON for stat range mapping.
    """
    text: Any
    startValue: str = ""
    endValue: str = ""
    id: Optional[Any] = None

    def to_json_data(self) -> dict:
        return StatMapping(text=self.text, startValue=self.startValue, endValue=self.endValue, id=self.id).to_json_data()

class SingleStat(Panel):
    """
    Generates Single Stat panel JSON structure.

    (Deprecated in Grafana 7.0, please use Stat instead)
    """
    cacheTimeout: Optional[Any] = None
    colors: List[Any] = Field(default_factory=lambda: [GREEN, ORANGE, RED])
    colorBackground: bool = False
    colorValue: bool = False
    decimals: Optional[Any] = None
    format: str = "none"
    gauge: Gauge = Field(default_factory=Gauge)
    mappingType: int = MAPPING_TYPE_VALUE_TO_TEXT
    mappingTypes: List[Any] = Field(default_factory=lambda: [MAPPING_VALUE_TO_TEXT, MAPPING_RANGE_TO_TEXT])
    minSpan: Optional[Any] = None
    nullText: Optional[Any] = None
    nullPointMode: str = "connected"
    postfix: str = ""
    postfixFontSize: str = "50%"
    prefix: str = ""
    prefixFontSize: str = "50%"
    rangeMaps: List[Any] = Field(default_factory=list)
    sparkline: SparkLine = Field(default_factory=SparkLine)
    thresholds: str = ""
    valueFontSize: str = "80%"
    valueName: str = VTYPE_DEFAULT
    valueMaps: List[Any] = Field(default_factory=list)

    def to_json_data(self) -> dict:
        return self.panel_json({
            'cacheTimeout': self.cacheTimeout,
            'colorBackground': self.colorBackground,
            'colorValue': self.colorValue,
            'colors': self.colors,
            'decimals': self.decimals,
            'format': self.format,
            'gauge': self.gauge.to_json_data(),
            'mappingType': self.mappingType,
            'mappingTypes': self.mappingTypes,
            'minSpan': self.minSpan,
            'nullPointMode': self.nullPointMode,
            'nullText': self.nullText,
            'postfix': self.postfix,
            'postfixFontSize': self.postfixFontSize,
            'prefix': self.prefix,
            'prefixFontSize': self.prefixFontSize,
            'rangeMaps': self.rangeMaps,
            'sparkline': self.sparkline.to_json_data(),
            'thresholds': self.thresholds,
            'type': SINGLESTAT_TYPE,
            'valueFontSize': self.valueFontSize,
            'valueMaps': self.valueMaps,
            'valueName': self.valueName,
        })

# ---------------------------------------------------------------------------
# Column Style and Table
# ---------------------------------------------------------------------------

class DateColumnStyleType(BaseModel):
    TYPE: str = "date"
    dateFormat: str = "YYYY-MM-DD HH:mm:ss"

    def to_json_data(self) -> dict:
        return {'dateFormat': self.dateFormat, 'type': self.TYPE}

class NumberColumnStyleType(BaseModel):
    TYPE: str = "number"
    colorMode: Optional[Any] = None
    colors: List[Any] = Field(default_factory=lambda: [GREEN, ORANGE, RED])
    thresholds: List[Any] = Field(default_factory=list)
    decimals: int = 2
    unit: str = SHORT_FORMAT

    def to_json_data(self) -> dict:
        return {
            'colorMode': self.colorMode,
            'colors': self.colors,
            'decimals': self.decimals,
            'thresholds': self.thresholds,
            'type': self.TYPE,
            'unit': self.unit,
        }

class StringColumnStyleType(BaseModel):
    TYPE: str = "string"
    decimals: int = 2
    colorMode: Optional[Any] = None
    colors: List[Any] = Field(default_factory=lambda: [GREEN, ORANGE, RED])
    thresholds: List[Any] = Field(default_factory=list)
    preserveFormat: bool = False
    sanitize: bool = False
    unit: str = SHORT_FORMAT
    mappingType: int = MAPPING_TYPE_VALUE_TO_TEXT
    valueMaps: List[Any] = Field(default_factory=list)
    rangeMaps: List[Any] = Field(default_factory=list)

    def to_json_data(self) -> dict:
        return {
            'decimals': self.decimals,
            'colorMode': self.colorMode,
            'colors': self.colors,
            'thresholds': self.thresholds,
            'unit': self.unit,
            'mappingType': self.mappingType,
            'valueMaps': self.valueMaps,
            'rangeMaps': self.rangeMaps,
            'preserveFormat': self.preserveFormat,
            'sanitize': self.sanitize,
            'type': self.TYPE,
        }

class HiddenColumnStyleType(BaseModel):
    TYPE: str = "hidden"

    def to_json_data(self) -> dict:
        return {'type': self.TYPE}

class ColumnStyle(BaseModel):
    alias: str = ""
    pattern: str = ""
    align: str = Field("auto", regex="^(auto|left|right|center)$")
    link: bool = False
    linkOpenInNewTab: bool = False
    linkUrl: str = ""
    linkTooltip: str = ""
    type: Any = Field(default_factory=NumberColumnStyleType)

    def to_json_data(self) -> dict:
        data = {
            'alias': self.alias,
            'pattern': self.pattern,
            'align': self.align,
            'link': self.link,
            'linkTargetBlank': self.linkOpenInNewTab,
            'linkUrl': self.linkUrl,
            'linkTooltip': self.linkTooltip,
        }
        data.update(self.type.to_json_data())
        return data

class ColumnSort(BaseModel):
    col: Optional[Any] = None
    desc: bool = False

    def to_json_data(self) -> dict:
        return {'col': self.col, 'desc': self.desc}

class Column(BaseModel):
    text: str = "Avg"
    value: str = "avg"

    def to_json_data(self) -> dict:
        return {'text': self.text, 'value': self.value}

class TableSortByField(BaseModel):
    displayName: str = ""
    desc: bool = False

    def to_json_data(self) -> dict:
        return {'displayName': self.displayName, 'desc': self.desc}

class Table(Panel):
    align: str = "auto"
    colorMode: str = "thresholds"
    columns: List[Any] = Field(default_factory=list)
    displayMode: str = "auto"
    fontSize: str = "100%"
    filterable: bool = False
    mappings: List[Any] = Field(default_factory=list)
    overrides: List[Any] = Field(default_factory=list)
    showHeader: bool = True
    span: int = 6
    unit: str = ""
    sortBy: List[TableSortByField] = Field(default_factory=list)

    @classmethod
    def with_styled_columns(cls, columns, styles=None, **kwargs):
        print("Error: Styled columns is not supported in Grafana v8 Table")
        raise NotImplementedError

    def to_json_data(self) -> dict:
        return self.panel_json({
            "color": {"mode": self.colorMode},
            'columns': [col for col in self.columns],
            'fontSize': self.fontSize,
            'fieldConfig': {
                'defaults': {
                    'custom': {'align': self.align, 'displayMode': self.displayMode, 'filterable': self.filterable},
                    'unit': self.unit,
                    'mappings': self.mappings
                },
                'overrides': self.overrides
            },
            'hideTimeOverride': self.hideTimeOverride,
            'mappings': self.mappings,
            'minSpan': self.minSpan,
            'options': {'showHeader': self.showHeader, 'sortBy': [s.to_json_data() for s in self.sortBy]},
            'type': TABLE_TYPE,
        })

# ---------------------------------------------------------------------------
# BarGauge and GaugePanel
# ---------------------------------------------------------------------------

class BarGauge(Panel):
    allValues: bool = False
    calc: Any = GAUGE_CALC_MEAN
    dataLinks: List[Any] = Field(default_factory=list)
    decimals: Optional[Any] = None
    displayMode: str = Field(DEFAULT_RENDERER, regex="^(lcd|basic|gradient)$")
    format: str = "none"
    label: Optional[Any] = None
    limit: Optional[Any] = None
    max: int = 100
    min: int = 0
    orientation: str = Field(ORIENTATION_HORIZONTAL, regex="^(horizontal|vertical|auto)$")
    rangeMaps: List[Any] = Field(default_factory=list)
    thresholdLabels: bool = False
    thresholdMarkers: bool = True
    thresholds: List[Any] = Field(default_factory=lambda: [
        Threshold(color='green', index=0, value=0.0),
        Threshold(color='red', index=1, value=80.0)
    ])
    valueMaps: List[Any] = Field(default_factory=list)

    def to_json_data(self) -> dict:
        return self.panel_json({
            'options': {
                'displayMode': self.displayMode,
                'fieldOptions': {
                    'calcs': [self.calc],
                    'defaults': {
                        'decimals': self.decimals,
                        'max': self.max,
                        'min': self.min,
                        'title': self.label,
                        'unit': self.format,
                        'links': self.dataLinks,
                    },
                    'limit': self.limit,
                    'mappings': self.valueMaps,
                    'override': {},
                    'thresholds': self.thresholds,
                    'values': self.allValues,
                },
                'orientation': self.orientation,
                'showThresholdLabels': self.thresholdLabels,
                'showThresholdMarkers': self.thresholdMarkers,
            },
            'type': BARGAUGE_TYPE,
        })

class GaugePanel(Panel):
    allValues: bool = False
    calc: Any = GAUGE_CALC_MEAN
    dataLinks: List[Any] = Field(default_factory=list)
    decimals: Optional[Any] = None
    format: str = "none"
    label: Optional[Any] = None
    limit: Optional[Any] = None
    max: int = 100
    min: int = 0
    rangeMaps: List[Any] = Field(default_factory=list)
    thresholdLabels: bool = False
    thresholdMarkers: bool = True
    thresholds: List[Any] = Field(default_factory=lambda: [
        Threshold(color='green', index=0, value=0.0),
        Threshold(color='red', index=1, value=80.0)
    ])
    valueMaps: List[Any] = Field(default_factory=list)
    neutral: Optional[Any] = None

    def to_json_data(self) -> dict:
        return self.panel_json({
            'fieldConfig': {
                'defaults': {
                    'calcs': [self.calc],
                    'decimals': self.decimals,
                    'max': self.max,
                    'min': self.min,
                    'title': self.label,
                    'unit': self.format,
                    'links': self.dataLinks,
                    'limit': self.limit,
                    'mappings': self.valueMaps,
                    'override': {},
                    'values': self.allValues,
                    'custom': {'neutral': self.neutral},
                },
                'showThresholdLabels': self.thresholdLabels,
                'showThresholdMarkers': self.thresholdMarkers,
            },
            'type': GAUGE_TYPE,
        })

# ---------------------------------------------------------------------------
# Heatmap, Statusmap, Svg, PieChart, PieChartv2, DashboardList, and Logs
# ---------------------------------------------------------------------------

class HeatmapColor(BaseModel):
    """
    A Color object for heatmaps.
    """
    cardColor: str = "#b4ff00"
    colorScale: str = "sqrt"
    colorScheme: str = "interpolateOranges"
    exponent: float = 0.5
    mode: str = "spectrum"
    max: Optional[Any] = None
    min: Optional[Any] = None

    def to_json_data(self) -> dict:
        return {
            'mode': self.mode,
            'cardColor': self.cardColor,
            'colorScale': self.colorScale,
            'exponent': self.exponent,
            'colorScheme': self.colorScheme,
            'max': self.max,
            'min': self.min,
        }

class Heatmap(Panel):
    legend: Dict[Any, Any] = Field(default_factory=lambda: {'show': False})
    tooltip: Tooltip = Field(default_factory=Tooltip)
    cards: Dict[Any, Any] = Field(default_factory=lambda: {'cardPadding': None, 'cardRound': None})
    color: HeatmapColor = Field(default_factory=HeatmapColor)
    dataFormat: str = "timeseries"
    heatmap: Dict[Any, Any] = {}
    hideZeroBuckets: bool = False
    highlightCards: bool = True
    options: List[Any] = Field(default_factory=list)
    xAxis: XAxis = Field(default_factory=XAxis)
    xBucketNumber: Optional[Any] = None
    xBucketSize: Optional[Any] = None
    yAxis: YAxis = Field(default_factory=YAxis)
    yBucketBound: Optional[Any] = None
    yBucketNumber: Optional[Any] = None
    yBucketSize: Optional[Any] = None
    reverseYBuckets: bool = False

    def to_json_data(self) -> dict:
        return self.panel_json({
            'cards': self.cards,
            'color': self.color.to_json_data(),
            'dataFormat': self.dataFormat,
            'heatmap': self.heatmap,
            'hideZeroBuckets': self.hideZeroBuckets,
            'highlightCards': self.highlightCards,
            'legend': self.legend,
            'options': self.options,
            'reverseYBuckets': self.reverseYBuckets,
            'tooltip': self.tooltip.to_json_data(),
            'type': HEATMAP_TYPE,
            'xAxis': self.xAxis.to_json_data(),
            'xBucketNumber': self.xBucketNumber,
            'xBucketSize': self.xBucketSize,
            'yAxis': self.yAxis.to_json_data(),
            'yBucketBound': self.yBucketBound,
            'yBucketNumber': self.yBucketNumber,
            'yBucketSize': self.yBucketSize
        })

class StatusmapColor(BaseModel):
    """
    A Color object for Statusmaps.
    """
    cardColor: str = "#b4ff00"
    colorScale: str = "sqrt"
    colorScheme: str = "GnYlRd"
    exponent: float = 0.5
    mode: str = "spectrum"
    thresholds: List[Any] = Field(default_factory=list)
    max: Optional[Any] = None
    min: Optional[Any] = None

    def to_json_data(self) -> dict:
        return {
            'mode': self.mode,
            'cardColor': self.cardColor,
            'colorScale': self.colorScale,
            'exponent': self.exponent,
            'colorScheme': self.colorScheme,
            'max': self.max,
            'min': self.min,
            'thresholds': self.thresholds
        }

class Statusmap(Panel):
    alert: Optional[Any] = None
    cards: Dict[Any, Any] = Field(default_factory=lambda: {
        'cardRound': None,
        'cardMinWidth': 5,
        'cardHSpacing': 2,
        'cardVSpacing': 2,
    })
    color: StatusmapColor = Field(default_factory=StatusmapColor)
    isNew: bool = True
    legend: Legend = Field(default_factory=Legend)
    nullPointMode: Any = NULL_AS_ZERO
    tooltip: Tooltip = Field(default_factory=Tooltip)
    xAxis: XAxis = Field(default_factory=XAxis)
    yAxis: YAxis = Field(default_factory=YAxis)

    def to_json_data(self) -> dict:
        graphObject = {
            'color': self.color.to_json_data(),
            'isNew': self.isNew,
            'legend': self.legend.to_json_data(),
            'minSpan': self.minSpan,
            'nullPointMode': self.nullPointMode,
            'tooltip': self.tooltip.to_json_data(),
            'type': STATUSMAP_TYPE,
            'xaxis': self.xAxis.to_json_data(),
            'yaxis': self.yAxis.to_json_data(),
        }
        if self.alert:
            graphObject['alert'] = self.alert
        return self.panel_json(graphObject)

class Svg(Panel):
    format: str = "none"
    jsCodeFilePath: str = ""
    jsCodeInitFilePath: str = ""
    height: Optional[Any] = None
    svgFilePath: str = ""

    @staticmethod
    def read_file(file_path: str) -> str:
        if file_path:
            with open(file_path) as f:
                return f.read()
        return ""

    def to_json_data(self) -> dict:
        js_code = self.read_file(self.jsCodeFilePath)
        js_init_code = self.read_file(self.jsCodeInitFilePath)
        svg_data = self.read_file(self.svgFilePath)
        return self.panel_json({
            'format': self.format,
            'js_code': js_code,
            'js_init_code': js_init_code,
            'svg_data': svg_data,
            'type': SVG_TYPE,
            'useSVGBuilder': False
        })

class PieChart(Panel):
    """
    Generates Pie Chart panel JSON structure.

    Deprecated in Grafana 8.0; please use PieChartv2 instead.
    """
    aliasColors: Dict[Any, Any] = Field(default_factory=dict)
    format: str = "none"
    legendType: str = "Right side"
    overrides: List[Any] = Field(default_factory=list)
    pieType: str = "pie"
    percentageDecimals: int = 0
    showLegend: Any = True
    showLegendValues: Any = True
    showLegendPercentage: bool = False
    thresholds: str = ""

    def to_json_data(self) -> dict:
        print("PieChart panel was deprecated in Grafana 8.0, please use PieChartv2 instead")
        return self.panel_json({
            'aliasColors': self.aliasColors,
            'format': self.format,
            'pieType': self.pieType,
            'height': self.height,
            'fieldConfig': {
                'defaults': {'custom': {}},
                'overrides': self.overrides
            },
            'legend': {
                'show': self.showLegend,
                'values': self.showLegendValues,
                'percentage': self.showLegendPercentage,
                'percentageDecimals': self.percentageDecimals
            },
            'legendType': self.legendType,
            'type': PIE_CHART_TYPE,
        })

class PieChartv2(Panel):
    custom: Dict[Any, Any] = Field(default_factory=dict)
    colorMode: str = "palette-classic"
    legendDisplayMode: str = "list"
    legendPlacement: str = "bottom"
    legendValues: List[Any] = Field(default_factory=list)
    mappings: List[Any] = Field(default_factory=list)
    overrides: List[Any] = Field(default_factory=list)
    pieType: str = "pie"
    reduceOptionsCalcs: List[str] = Field(default_factory=lambda: ["lastNotNull"])
    reduceOptionsFields: str = ""
    reduceOptionsValues: bool = False
    tooltipMode: str = "single"
    tooltipSort: str = "none"
    unit: str = ""

    def to_json_data(self) -> dict:
        return self.panel_json({
            'fieldConfig': {
                'defaults': {
                    'color': {'mode': self.colorMode},
                    'custom': self.custom,
                    'mappings': self.mappings,
                    'unit': self.unit,
                },
                'overrides': self.overrides,
            },
            'options': {
                'reduceOptions': {
                    'values': self.reduceOptionsValues,
                    'calcs': self.reduceOptionsCalcs,
                    'fields': self.reduceOptionsFields
                },
                'pieType': self.pieType,
                'tooltip': {'mode': self.tooltipMode, 'sort': self.tooltipSort},
                'legend': {'displayMode': self.legendDisplayMode, 'placement': self.legendPlacement, 'values': self.legendValues},
            },
            'type': PIE_CHART_V2_TYPE,
        })

class DashboardList(Panel):
    showHeadings: bool = True
    showSearch: bool = False
    showRecent: bool = False
    showStarred: bool = True
    maxItems: int = 10
    searchQuery: str = ""
    searchTags: List[str] = Field(default_factory=list)
    overrides: List[Any] = Field(default_factory=list)

    def to_json_data(self) -> dict:
        return self.panel_json({
            'fieldConfig': {
                'defaults': {'custom': {}},
                'overrides': self.overrides
            },
            'headings': self.showHeadings,
            'search': self.showSearch,
            'recent': self.showRecent,
            'starred': self.showStarred,
            'limit': self.maxItems,
            'query': self.searchQuery,
            'tags': self.searchTags,
            'type': DASHBOARDLIST_TYPE,
        })

class Logs(Panel):
    showLabels: bool = False
    showCommonLabels: bool = False
    showTime: bool = False
    wrapLogMessages: bool = False
    sortOrder: str = "Descending"
    dedupStrategy: str = "none"
    enableLogDetails: bool = False
    overrides: List[Any] = Field(default_factory=list)
    prettifyLogMessage: bool = False

    def to_json_data(self) -> dict:
        return self.panel_json({
            'fieldConfig': {
                'defaults': {'custom': {}},
                'overrides': self.overrides
            },
            'options': {
                'showLabels': self.showLabels,
                'showCommonLabels': self.showCommonLabels,
                'showTime': self.showTime,
                'wrapLogMessage': self.wrapLogMessages,
                'sortOrder': self.sortOrder,
                'dedupStrategy': self.dedupStrategy,
                'enableLogDetails': self.enableLogDetails,
                'prettifyLogMessage': self.prettifyLogMessage
            },
            'type': LOGS_TYPE,
        })

# ---------------------------------------------------------------------------
# Thresholds and SeriesOverride
# ---------------------------------------------------------------------------

class Threshold(BaseModel):
    """
    Threshold for panels.

    Example:
        thresholds = [
            Threshold(color='green', index=0, value=0.0),
            Threshold(color='red', index=1, value=80.0)
        ]
    """
    color: Any
    index: int
    value: float
    line: bool = True
    op: str = EVAL_GT
    yaxis: str = "left"

    def to_json_data(self) -> dict:
        return {
            'op': self.op,
            'yaxis': self.yaxis,
            'color': self.color,
            'line': self.line,
            'index': self.index,
            'value': 'null' if self.index == 0 else self.value,
        }

class GraphThreshold(BaseModel):
    """
    Threshold for Graph panels.
    """
    value: float
    colorMode: str = "critical"
    fill: bool = True
    line: bool = True
    op: str = EVAL_GT
    yaxis: str = "left"
    fillColor: Any = RED
    lineColor: Any = RED

    def to_json_data(self) -> dict:
        data = {
            'value': self.value,
            'colorMode': self.colorMode,
            'fill': self.fill,
            'line': self.line,
            'op': self.op,
            'yaxis': self.yaxis,
        }
        if self.colorMode == "custom":
            data['fillColor'] = self.fillColor
            data['lineColor'] = self.lineColor
        return data

class SeriesOverride(BaseModel):
    """
    To override properties of panels.
    """
    alias: str
    bars: bool = False
    lines: bool = True
    yaxis: int = Field(1, ge=1, le=2)
    fill: int = Field(1, ge=0, le=10)
    zindex: int = Field(0, ge=-3, le=3)
    dashes: bool = False
    dashLength: Optional[int] = Field(default=None)
    spaceLength: Optional[int] = Field(default=None)
    color: Optional[Any] = None
    fillBelowTo: Optional[str] = None

    def to_json_data(self) -> dict:
        return {
            'alias': self.alias,
            'bars': self.bars,
            'lines': self.lines,
            'yaxis': self.yaxis,
            'fill': self.fill,
            'color': self.color,
            'fillBelowTo': self.fillBelowTo,
            'zindex': self.zindex,
            'dashes': self.dashes,
            'dashLength': self.dashLength,
            'spaceLength': self.spaceLength,
        }

# ---------------------------------------------------------------------------
# Worldmap, StateTimeline, Histogram, News, Ae3ePlotly, BarChart
# ---------------------------------------------------------------------------

WORLDMAP_CENTER = ['(0°, 0°)', 'North America', 'Europe', 'West Asia', 'SE Asia', 'Last GeoHash', 'custom']
WORLDMAP_LOCATION_DATA = ['countries', 'countries_3letter', 'states', 'probes', 'geohash', 'json_endpoint', 'jsonp endpoint', 'json result', 'table']

class Worldmap(Panel):
    circleMaxSize: int = 30
    circleMinSize: int = 2
    decimals: int = 0
    geoPoint: str = "geohash"
    locationData: str = Field("countries", regex="^(" + "|".join(WORLDMAP_LOCATION_DATA) + ")$")
    locationName: str = ""
    hideEmpty: bool = False
    hideZero: bool = False
    initialZoom: int = 1
    jsonUrl: str = ""
    jsonpCallback: str = ""
    mapCenter: str = Field("(0°, 0°)", regex="^(" + "|".join(WORLDMAP_CENTER) + ")$")
    mapCenterLatitude: int = 0
    mapCenterLongitude: int = 0
    metric: str = "Value"
    mouseWheelZoom: bool = False
    stickyLabels: bool = False
    thresholds: str = "0,100,150"
    thresholdColors: List[str] = Field(default_factory=lambda: ["#73BF69", "#73BF69", "#FADE2A", "#C4162A"])
    unitPlural: str = ""
    unitSingle: str = ""
    unitSingular: str = ""
    aggregation: str = "total"

    def to_json_data(self) -> dict:
        return self.panel_json({
            'circleMaxSize': self.circleMaxSize,
            'circleMinSize': self.circleMinSize,
            'colors': self.thresholdColors,
            'decimals': self.decimals,
            'esGeoPoint': self.geoPoint,
            'esMetric': self.metric,
            'locationData': self.locationData,
            'esLocationName': self.locationName,
            'hideEmpty': self.hideEmpty,
            'hideZero': self.hideZero,
            'initialZoom': self.initialZoom,
            'jsonUrl': self.jsonUrl,
            'jsonpCallback': self.jsonpCallback,
            'mapCenter': self.mapCenter,
            'mapCenterLatitude': self.mapCenterLatitude,
            'mapCenterLongitude': self.mapCenterLongitude,
            'mouseWheelZoom': self.mouseWheelZoom,
            'stickyLabels': self.stickyLabels,
            'thresholds': self.thresholds,
            'unitPlural': self.unitPlural,
            'unitSingle': self.unitSingle,
            'unitSingular': self.unitSingular,
            'valueName': self.aggregation,
            'tableQueryOptions': {
                'queryType': 'geohash',
                'geohashField': 'geohash',
                'latitudeField': 'latitude',
                'longitudeField': 'longitude',
                'metricField': 'metric'
            },
            'type': WORLD_MAP_TYPE
        })

class StateTimeline(Panel):
    alignValue: str = "left"
    colorMode: str = "thresholds"
    fillOpacity: int = 70
    legendDisplayMode: str = "list"
    legendPlacement: str = "bottom"
    lineWidth: int = 0
    mappings: List[Any] = Field(default_factory=list)
    overrides: List[Any] = Field(default_factory=list)
    mergeValues: bool = True
    rowHeight: float = 0.9
    showValue: str = "auto"
    tooltipMode: str = "single"

    def to_json_data(self) -> dict:
        return self.panel_json({
            'fieldConfig': {
                'defaults': {
                    'custom': {'lineWidth': self.lineWidth, 'fillOpacity': self.fillOpacity},
                    'color': {'mode': self.colorMode},
                    'mappings': self.mappings
                },
                'overrides': self.overrides
            },
            'options': {
                'mergeValues': self.mergeValues,
                'showValue': self.showValue,
                'alignValue': self.alignValue,
                'rowHeight': self.rowHeight,
                'legend': {'displayMode': self.legendDisplayMode, 'placement': self.legendPlacement},
                'tooltip': {'mode': self.tooltipMode}
            },
            'type': STATE_TIMELINE_TYPE,
        })

class Histogram(Panel):
    bucketOffset: int = 0
    bucketSize: int = 0
    colorMode: str = "thresholds"
    combine: bool = False
    fillOpacity: int = 80
    legendDisplayMode: str = "list"
    legendPlacement: str = "bottom"
    lineWidth: int = 0
    mappings: List[Any] = Field(default_factory=list)
    overrides: List[Any] = Field(default_factory=list)

    def to_json_data(self) -> dict:
        histogram = self.panel_json({
            'fieldConfig': {
                'defaults': {
                    'custom': {'lineWidth': self.lineWidth, 'fillOpacity': self.fillOpacity},
                    'color': {'mode': self.colorMode},
                    'mappings': self.mappings
                },
                'overrides': self.overrides
            },
            'options': {
                'legend': {'displayMode': self.legendDisplayMode, 'placement': self.legendPlacement},
                "bucketOffset": self.bucketOffset,
                "combine": self.combine,
            },
            'type': HISTOGRAM_TYPE,
        })
        if self.bucketSize > 0:
            histogram['options']['bucketSize'] = self.bucketSize
        return histogram

class News(Panel):
    feedUrl: str = ""
    showImage: bool = True
    useProxy: bool = False

    def to_json_data(self) -> dict:
        return self.panel_json({
            'options': {
                'feedUrl': self.feedUrl,
                'showImage': self.showImage,
                'useProxy': self.useProxy
            },
            'type': NEWS_TYPE,
        })

class Ae3ePlotly(Panel):
    configuration: Dict[Any, Any] = Field(default_factory=dict)
    data: List[Any] = Field(default_factory=list)
    layout: Dict[Any, Any] = Field(default_factory=dict)
    script: str = """console.log(data)
            var trace = {
              x: data.series[0].fields[0].values.buffer,
              y: data.series[0].fields[1].values.buffer
            };
            return {data:[trace],layout:{title:'My Chart'}};"""
    clickScript: str = ""

    def to_json_data(self) -> dict:
        plotly = self.panel_json({
            'fieldConfig': {'defaults': {}, 'overrides': []},
            'options': {
                'configuration': {},
                'data': self.data,
                'layout': {},
                'onclick': self.clickScript,
                'script': self.script,
            },
            'type': AE3E_PLOTLY_TYPE,
        })
        _deep_update(plotly["options"]["layout"], self.layout)
        _deep_update(plotly["options"]["configuration"], self.configuration)
        return plotly

class BarChart(Panel):
    orientation: str = "auto"
    xTickLabelRotation: int = 0
    xTickLabelSpacing: int = 0
    showValue: str = "auto"
    stacking: str = "none"
    groupWidth: float = 0.7
    barWidth: float = 0.97
    barRadius: float = 0.0
    tooltipMode: str = "single"
    tooltipSort: str = "none"
    showLegend: bool = True
    legendDisplayMode: str = "list"
    legendPlacement: str = "bottom"
    legendCalcs: List[Any] = Field(default_factory=list)
    lineWidth: int = 1
    fillOpacity: int = 80
    gradientMode: str = "none"
    axisPlacement: str = "auto"
    axisLabel: str = ""
    axisColorMode: str = "text"
    scaleDistributionType: str = "linear"
    axisCenteredZero: bool = False
    hideFromTooltip: bool = False
    hideFromViz: bool = False
    hideFromLegend: bool = False
    colorMode: str = "palette-classic"
    fixedColor: str = "blue"
    mappings: List[Any] = Field(default_factory=list)
    thresholdsMode: str = "absolute"
    thresholdSteps: List[Any] = Field(default_factory=lambda: [
        {"value": None, "color": "green"},
        {"value": 80, "color": "red"}
    ])
    overrides: List[Any] = Field(default_factory=list)

    def to_json_data(self) -> dict:
        bar_chart = self.panel_json({
            'options': {
                'orientation': self.orientation,
                'xTickLabelRotation': self.xTickLabelRotation,
                'xTickLabelSpacing': self.xTickLabelSpacing,
                'showValue': self.showValue,
                'stacking': self.stacking,
                'groupWidth': self.groupWidth,
                'barWidth': self.barWidth,
                'barRadius': self.barRadius,
                'tooltip': {'mode': self.tooltipMode, 'sort': self.tooltipSort},
                'legend': {'showLegend': self.showLegend, 'displayMode': self.legendDisplayMode,
                           'placement': self.legendPlacement, 'calcs': self.legendCalcs},
            },
            'fieldConfig': {
                'defaults': {
                    'custom': {
                        'lineWidth': self.lineWidth,
                        'fillOpacity': self.fillOpacity,
                        'gradientMode': self.gradientMode,
                        'axisPlacement': self.axisPlacement,
                        'axisLabel': self.axisLabel,
                        'axisColorMode': self.axisColorMode,
                        'scaleDistribution': {'type': self.scaleDistributionType},
                        'axisCenteredZero': self.axisCenteredZero,
                        'hideFrom': {'tooltip': self.hideFromTooltip, 'viz': self.hideFromViz, 'legend': self.hideFromLegend}
                    },
                    'color': {'mode': self.colorMode, 'fixedColor': self.fixedColor if self.colorMode == 'fixed' else 'none'},
                    'mappings': self.mappings,
                    'thresholds': {'mode': self.thresholdsMode, 'steps': self.thresholdSteps}
                },
                'overrides': self.overrides
            },
            'type': BAR_CHART_TYPE,
        })
        return bar_chart