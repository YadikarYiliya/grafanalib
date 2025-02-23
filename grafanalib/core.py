"""Low-level functions for building Grafana dashboards."""

from __future__ import annotations

import itertools
import math
import string
import warnings
from typing import Annotated, Any, Literal, NoReturn

from pydantic import BaseModel, Field, RootModel, field_validator
from pydantic.functional_serializers import PlainSerializer
from pydantic_extra_types.color import Color

# ---------------------------------------------------------------------------
# Basic Types
# ---------------------------------------------------------------------------


RGB = Annotated[
    Color,
    PlainSerializer(
        lambda x: x.as_rgb(),
        return_type=str,
        when_used="always",
    ),
]


RGBA = Annotated[
    Color,
    PlainSerializer(
        lambda x: x.as_rgb(),
        return_type=str,
        when_used="always",
    ),
]


class Pixels(RootModel):
    root: str

    @field_validator("root", mode="wrap")
    @classmethod
    def validate_pixels(cls, value, handler):
        # Convert integers to strings with "%" suffix
        if isinstance(value, int):
            return f"{value}px"

        # Call the next handler in the chain
        result = handler(value)

        # Check if the string ends with "%"
        if not result.endswith("px"):
            raise ValueError("String must end with 'px'")

        # Extract the numeric part and check if it is a valid integer
        num_part = result[:-2]  # Remove the "px" characters
        if not num_part.isdigit() or " " in num_part:
            raise ValueError(
                "The string must contain an integer with no spaces before the 'px'",
            )

        return result


class Percent(RootModel):
    root: str = "100%"

    @field_validator("root", mode="wrap")
    @classmethod
    def validate_percentage(cls, value, handler):
        # Convert integers to strings with "%" suffix
        if isinstance(value, int):
            return f"{value}%"

        # Call the next handler in the chain
        result = handler(value)

        # Check if the string ends with "%"
        if not result.endswith("%"):
            raise ValueError("String must end with '%'")

        # Extract the numeric part and check if it is a valid integer
        num_part = result[:-1]  # Remove the "%" character
        if not num_part.isdigit() or " " in num_part:
            raise ValueError(
                "The string must contain an integer with no spaces before the '%'",
            )

        return result


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GREY1 = Color((216, 200, 27, 0.27))
GREY2 = Color((234, 112, 112, 0.22))
BLUE_RGBA = Color((31, 118, 189, 0.18))
BLUE_RGB = Color((31, 120, 193))
GREEN = Color((50, 172, 45, 0.97))
ORANGE = Color((237, 129, 40, 0.89))
RED = Color((245, 54, 54, 0.9))
BLANK = Color((0, 0, 0, 0.0))
WHITE = Color((255, 255, 255))

INDIVIDUAL = "individual"
CUMULATIVE = "cumulative"

NULL_CONNECTED = "connected"
NULL_AS_ZERO = "null as zero"
NULL_AS_NULL = "null"

FLOT = "flot"

ABSOLUTE_TYPE = "absolute"
DASHBOARD_TYPE = Literal["dashboards", "link"]
ROW_TYPE = "row"
GRAPH_TYPE = "graph"
DISCRETE_TYPE = "natel-discrete-panel"
EPICT_TYPE = "larona-epict-panel"
STAT_TYPE = "stat"
SINGLESTAT_TYPE = "singlestat"
STATE_TIMELINE_TYPE = "state-timeline"
TABLE_TYPE = "table"
TEXT_TYPE = "text"
ALERTLIST_TYPE = "alertlist"
BARGAUGE_TYPE = "bargauge"
GAUGE_TYPE = "gauge"
DASHBOARDLIST_TYPE = "dashlist"
LOGS_TYPE = "logs"
HEATMAP_TYPE = "heatmap"
STATUSMAP_TYPE = "flant-statusmap-panel"
SVG_TYPE = "marcuscalidus-svg-panel"
PIE_CHART_TYPE = "grafana-piechart-panel"
PIE_CHART_V2_TYPE = "piechart"
TIMESERIES_TYPE = "timeseries"
WORLD_MAP_TYPE = "grafana-worldmap-panel"
NEWS_TYPE = "news"
HISTOGRAM_TYPE = "histogram"
AE3E_PLOTLY_TYPE = "ae3e-plotly-panel"
BAR_CHART_TYPE = "barchart"

DEFAULT_FILL = 1
DEFAULT_REFRESH = "10s"
DEFAULT_ALERT_EVALUATE_INTERVAL = "1m"
DEFAULT_ALERT_EVALUATE_FOR = "5m"
DEFAULT_ROW_HEIGHT = Pixels(250)
DEFAULT_LINE_WIDTH = 2
DEFAULT_POINT_RADIUS = 5
DEFAULT_RENDERER = FLOT
DEFAULT_STEP = 10
DEFAULT_LIMIT = 10
TOTAL_SPAN = 12

DARK_STYLE = "dark"
LIGHT_STYLE = "light"

UTC = "utc"

SCHEMA_VERSION = 12

# (DEPRECATED: use formatunits.py) Y Axis formats
DURATION_FORMAT = "dtdurations"
NO_FORMAT = "none"
OPS_FORMAT = "ops"
PERCENT_UNIT_FORMAT = "percentunit"
DAYS_FORMAT = "d"
HOURS_FORMAT = "h"
MINUTES_FORMAT = "m"
SECONDS_FORMAT = "s"
MILLISECONDS_FORMAT = "ms"
SHORT_FORMAT = "short"
BYTES_FORMAT = "bytes"
BITS_PER_SEC_FORMAT = "bps"
BYTES_PER_SEC_FORMAT = "Bps"
NONE_FORMAT = "none"
JOULE_FORMAT = "joule"
WATTHOUR_FORMAT = "watth"
WATT_FORMAT = "watt"
KWATT_FORMAT = "kwatt"
KWATTHOUR_FORMAT = "kwatth"
VOLT_FORMAT = "volt"
BAR_FORMAT = "pressurebar"
PSI_FORMAT = "pressurepsi"
CELSIUS_FORMAT = "celsius"
KELVIN_FORMAT = "kelvin"
GRAM_FORMAT = "massg"
EUR_FORMAT = "currencyEUR"
USD_FORMAT = "currencyUSD"
METER_FORMAT = "lengthm"
SQUARE_METER_FORMAT = "areaM2"
CUBIC_METER_FORMAT = "m3"
LITRE_FORMAT = "litre"
PERCENT_FORMAT = "percent"
VOLT_AMPERE_FORMAT = "voltamp"

# Alert rule state
STATE_NO_DATA = "no_data"
STATE_ALERTING = "alerting"
STATE_KEEP_LAST_STATE = "keep_state"
STATE_OK = "ok"

# Evaluator
EVAL_GT = "gt"
EVAL_LT = "lt"
EVAL_WITHIN_RANGE = "within_range"
EVAL_OUTSIDE_RANGE = "outside_range"
EVAL_NO_VALUE = "no_value"

# Reducer Type
RTYPE_AVG = "avg"
RTYPE_MIN = "min"
RTYPE_MAX = "max"
RTYPE_SUM = "sum"
RTYPE_COUNT = "count"
RTYPE_LAST = "last"
RTYPE_MEDIAN = "median"
RTYPE_DIFF = "diff"
RTYPE_PERCENT_DIFF = "percent_diff"
RTYPE_COUNT_NON_NULL = "count_non_null"

# Condition Type
CTYPE_QUERY = "query"

# Operator
OP_AND = "and"
OP_OR = "or"

# Alert Expression Types
EXP_TYPE_CLASSIC = "classic_conditions"
EXP_TYPE_REDUCE = "reduce"
EXP_TYPE_RESAMPLE = "resample"
EXP_TYPE_MATH = "math"

# Alert Expression Reducer Function
EXP_REDUCER_FUNC_MIN = "min"
EXP_REDUCER_FUNC_MAX = "max"
EXP_REDUCER_FUNC_MEAN = "mean"
EXP_REDUCER_FUNC_SUM = "sum"
EXP_REDUCER_FUNC_COUNT = "count"
EXP_REDUCER_FUNC_LAST = "last"

# Alert Expression Reducer Mode
EXP_REDUCER_MODE_STRICT = "strict"
EXP_REDUCER_FUNC_DROP_NN = "dropNN"
EXP_REDUCER_FUNC_REPLACE_NN = "replaceNN"

# Text panel modes
TEXT_MODE_MARKDOWN = "markdown"
TEXT_MODE_HTML = "html"
TEXT_MODE_TEXT = "text"

# Datasource plugins
PLUGIN_ID_GRAPHITE = "graphite"
PLUGIN_ID_PROMETHEUS = "prometheus"
PLUGIN_ID_INFLUXDB = "influxdb"
PLUGIN_ID_OPENTSDB = "opentsdb"
PLUGIN_ID_ELASTICSEARCH = "elasticsearch"
PLUGIN_ID_CLOUDWATCH = "cloudwatch"

# Target formats
TIME_SERIES_TARGET_FORMAT = "time_series"
TABLE_TARGET_FORMAT = "table"

# Table Transforms
AGGREGATIONS_TRANSFORM = "timeseries_aggregations"
ANNOTATIONS_TRANSFORM = "annotations"
COLUMNS_TRANSFORM = "timeseries_to_columns"
JSON_TRANSFORM = "json"
ROWS_TRANSFORM = "timeseries_to_rows"
TABLE_TRANSFORM = "table"

# Alertlist show selections
ALERTLIST_SHOW_CURRENT = "current"
ALERTLIST_SHOW_CHANGES = "changes"

# Alertlist state filter options
ALERTLIST_STATE_OK = "ok"
ALERTLIST_STATE_PAUSED = "paused"
ALERTLIST_STATE_NO_DATA = "no_data"
ALERTLIST_STATE_EXECUTION_ERROR = "execution_error"
ALERTLIST_STATE_ALERTING = "alerting"
ALERTLIST_STATE_PENDING = "pending"

# Alert Rule state filter options (Grafana 8.x)
ALERTRULE_STATE_DATA_OK = "OK"
ALERTRULE_STATE_DATA_NODATA = "No Data"
ALERTRULE_STATE_DATA_ALERTING = "Alerting"
ALERTRULE_STATE_DATA_ERROR = "Error"

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

GAUGE_CALC_LAST = "last"
GAUGE_CALC_FIRST = "first"
GAUGE_CALC_MIN = "min"
GAUGE_CALC_MAX = "max"
GAUGE_CALC_MEAN = "mean"
GAUGE_CALC_TOTAL = "sum"
GAUGE_CALC_COUNT = "count"
GAUGE_CALC_RANGE = "range"
GAUGE_CALC_DELTA = "delta"
GAUGE_CALC_STEP = "step"
GAUGE_CALC_DIFFERENCE = "difference"
GAUGE_CALC_LOGMIN = "logmin"
GAUGE_CALC_CHANGE_COUNT = "changeCount"
GAUGE_CALC_DISTINCT_COUNT = "distinctCount"

ORIENTATION_HORIZONTAL = "horizontal"
ORIENTATION_VERTICAL = "vertical"
ORIENTATION_AUTO = "auto"

GAUGE_DISPLAY_MODE_BASIC = "basic"
GAUGE_DISPLAY_MODE_LCD = "lcd"
GAUGE_DISPLAY_MODE_GRADIENT = "gradient"

GRAPH_TOOLTIP_MODE_NOT_SHARED = 0
GRAPH_TOOLTIP_MODE_SHARED_CROSSHAIR = 1
GRAPH_TOOLTIP_MODE_SHARED_TOOLTIP = 2  # Shared crosshair AND tooltip

DEFAULT_AUTO_COUNT = 30
DEFAULT_MIN_AUTO_INTERVAL = "10s"

DASHBOARD_LINK_ICON = Literal[
    "bolt",
    "cloud",
    "dashboard",
    "doc",
    "external link",
    "info",
    "question",
]

# ---------------------------------------------------------------------------
# Mapping and Value Mappings
# ---------------------------------------------------------------------------


class Mapping(BaseModel):
    name: Any
    value: int

    def to_json_data(self) -> dict:
        return {"name": self.name, "value": self.value}


MAPPING_TYPE_VALUE_TO_TEXT = 1
MAPPING_TYPE_RANGE_TO_TEXT = 2

MAPPING_VALUE_TO_TEXT = Mapping(name="value to text", value=MAPPING_TYPE_VALUE_TO_TEXT)
MAPPING_RANGE_TO_TEXT = Mapping(name="range to text", value=MAPPING_TYPE_RANGE_TO_TEXT)

# Value types for Stat panels
VTYPE_MIN = "min"
VTYPE_MAX = "max"
VTYPE_AVG = "avg"
VTYPE_CURR = "current"
VTYPE_TOTAL = "total"
VTYPE_NAME = "name"
VTYPE_FIRST = "first"
VTYPE_DELTA = "delta"
VTYPE_RANGE = "range"
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
    background_color: Any = Field(default="#000", alias="backgroundColor")
    blink_high: bool = Field(default=False, alias="blinkHigh")
    blink_low: bool = Field(default=False, alias="blinkLow")
    color: Any = "#000"
    color_high: Any = Field(default="#000", alias="colorHigh")
    color_low: Any = Field(default="#000", alias="colorLow")
    color_medium: Any = Field(default="#000", alias="colorMedium")
    color_symbol: bool = Field(default=False, alias="colorSymbol")
    custom_symbol: str = Field(default="", alias="customSymbol")
    decimal: int = 0
    font_size: int = Field(default=12, alias="fontSize")
    has_background: bool = Field(default=False, alias="hasBackground")
    has_orb: bool = Field(default=False, alias="hasOrb")
    has_symbol: bool = Field(default=False, alias="hasSymbol")
    is_using_thresholds: bool = Field(default=False, alias="isUsingThresholds")
    orb_hide_text: bool = Field(default=False, alias="orbHideText")
    orb_location: Literal["Left", "Right", "Top", "Bottom"] = Field(
        default="Left",
        alias="orbLocation",
    )
    orb_size: int = Field(default=13, alias="orbSize")
    prefix: str = ""
    prefix_size: int = Field(default=10, alias="prefixSize")
    selected: bool = False
    serie: str = ""
    suffix: str = ""
    suffix_size: int = Field(default=10, alias="suffixSize")
    symbol: str = ""
    symbol_def_height: int = Field(default=32, alias="symbolDefHeight")
    symbol_def_width: int = Field(default=32, alias="symbolDefWidth")
    symbol_height: int = Field(default=32, alias="symbolHeight")
    symbol_hide_text: bool = Field(default=False, alias="symbolHideText")
    symbol_width: int = Field(default=32, alias="symbolWidth")
    text: str = "N/A"
    thresholds: str = ""
    url: str = ""
    xpos: int = 0
    ypos: int = 0

    def to_json_data(self) -> dict:
        computed_symbol = "custom" if self.custom_symbol else self.symbol
        computed_is_using_thresholds = bool(self.thresholds)
        return {
            "angle": self.angle,
            "backgroundColor": self.background_color,
            "blinkHigh": self.blink_high,
            "blinkLow": self.blink_low,
            "color": self.color,
            "colorHigh": self.color_high,
            "colorLow": self.color_low,
            "colorMedium": self.color_medium,
            "colorSymbol": self.color_symbol,
            "customSymbol": self.custom_symbol,
            "decimal": self.decimal,
            "fontSize": self.font_size,
            "hasBackground": self.has_background,
            "hasOrb": self.has_orb,
            "hasSymbol": self.has_symbol,
            "isUsingThresholds": computed_is_using_thresholds,
            "orbHideText": self.orb_hide_text,
            "orbLocation": self.orb_location,
            "orbSize": self.orb_size,
            "prefix": self.prefix,
            "prefixSize": self.prefix_size,
            "selected": self.selected,
            "serie": self.serie,
            "suffix": self.suffix,
            "suffixSize": self.suffix_size,
            "symbol": computed_symbol,
            "symbolDefHeight": self.symbol_def_height,
            "symbolDefWidth": self.symbol_def_width,
            "symbolHeight": self.symbol_height,
            "symbolHideText": self.symbol_hide_text,
            "symbolWidth": self.symbol_width,
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
    threshold1: Any | None = None
    threshold1_color: RGBA = Field(default=GREY1, alias="threshold1Color")
    threshold2: Any | None = None
    threshold2_color: RGBA = Field(default=GREY2, alias="threshold2Color")

    def to_json_data(self) -> dict:
        return {
            "threshold1": self.threshold1,
            "threshold1Color": self.threshold1_color.to_json_data(),
            "threshold2": self.threshold2,
            "threshold2Color": self.threshold2_color.to_json_data(),
        }


class Legend(BaseModel):
    avg: bool = False
    current: bool = False
    max: bool = False
    min: bool = False
    show: bool = True
    total: bool = False
    values: Any | None = None
    align_as_table: bool = Field(default=False, alias="alignAsTable")
    hide_empty: bool = Field(default=False, alias="hideEmpty")
    hide_zero: bool = Field(default=False, alias="hideZero")
    right_side: bool = Field(default=False, alias="rightSide")
    side_width: Any | None = Field(default=None, alias="sideWidth")
    sort: Any | None = None
    sort_desc: bool = Field(default=False, alias="sortDesc")

    def to_json_data(self) -> dict:
        computed_values = (
            (self.avg or self.current or self.max or self.min)
            if self.values is None
            else self.values
        )
        return {
            "avg": self.avg,
            "current": self.current,
            "max": self.max,
            "min": self.min,
            "show": self.show,
            "total": self.total,
            "values": computed_values,
            "alignAsTable": self.align_as_table,
            "hideEmpty": self.hide_empty,
            "hideZero": self.hide_zero,
            "rightSide": self.right_side,
            "sideWidth": self.side_width,
            "sort": self.sort,
            "sortDesc": self.sort_desc,
        }


# ---------------------------------------------------------------------------
# Repeat and Target classes
# ---------------------------------------------------------------------------


class Repeat(BaseModel):
    direction: Any | None = None
    variable: Any | None = None
    max_per_row: int | None = Field(default=None, alias="maxPerRow")

    def to_json_data(self) -> dict:
        return {
            "direction": self.direction,
            "variable": self.variable,
            "maxPerRow": self.max_per_row,
        }


def is_valid_target(value: Any):
    if getattr(value, "refId", "") == "":
        msg = "Target should have non-empty 'refId' attribute"
        raise ValueError(msg)
    return value


class Target(BaseModel):
    expr: str = ""
    format: str = TIME_SERIES_TARGET_FORMAT
    hide: bool = False
    legend_format: str = Field(default="", alias="legendFormat")
    interval: str = ""
    interval_factor: int = Field(default=2, alias="intervalFactor")
    metric: str = ""
    ref_id: str = Field(default="", alias="refId")
    step: int = DEFAULT_STEP
    target: str = ""
    instant: bool = False
    datasource: Any | None = None

    def to_json_data(self) -> dict:
        return {
            "expr": self.expr,
            "query": self.expr,
            "target": self.target,
            "format": self.format,
            "hide": self.hide,
            "interval": self.interval,
            "intervalFactor": self.interval_factor,
            "legendFormat": self.legend_format,
            "alias": self.legend_format,
            "metric": self.metric,
            "refId": self.ref_id,
            "step": self.step,
            "instant": self.instant,
            "datasource": self.datasource,
        }


class LokiTarget(BaseModel):
    datasource: str = ""
    expr: str = ""
    hide: bool = False

    def to_json_data(self) -> dict:
        return {
            "datasource": {"type": "loki", "uid": self.datasource},
            "expr": self.expr,
            "hide": self.hide,
            "queryType": "range",
        }


class SqlTarget(Target):
    raw_sql: str = Field(default="", alias="rawSql")
    raw_query: bool = Field(default=True, alias="rawQuery")
    src_file_path: str = Field(default="", alias="srcFilePath")
    sql_params: dict[str, Any] = Field({}, alias="sqlParams")

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if self.src_file_path:
            with open(self.src_file_path) as f:
                self.raw_sql = f.read()
            if self.sql_params:
                self.raw_sql = self.raw_sql.format(**self.sql_params)

    def to_json_data(self) -> dict:
        super_json = super().to_json_data()
        super_json["rawSql"] = self.raw_sql
        super_json["rawQuery"] = self.raw_query
        return super_json


# ---------------------------------------------------------------------------
# Tooltip, XAxis, YAxis, and YAxes
# ---------------------------------------------------------------------------


class Tooltip(BaseModel):
    ms_resolution: bool = Field(default=True, alias="msResolution")
    shared: bool = True
    sort: int = 0
    value_type: str = Field(default=CUMULATIVE, alias="valueType")

    def to_json_data(self) -> dict:
        return {
            "msResolution": self.ms_resolution,
            "shared": self.shared,
            "sort": self.sort,
            "value_type": self.value_type,
        }


class XAxis(BaseModel):
    mode: Literal["time", "series", "histogram"] = "time"
    name: Any | None = None
    values: list[Any] = []
    show: bool = True

    def to_json_data(self) -> dict:
        return {
            "mode": self.mode,
            "name": self.name,
            "values": self.values,
            "show": self.show,
        }


class YAxis(BaseModel):
    decimals: Any | None = None
    format: Any | None = None
    label: Any | None = None
    log_base: int = Field(default=1, alias="logBase")
    max: Any | None = None
    min: Any | None = None
    show: bool = True

    def to_json_data(self) -> dict:
        return {
            "decimals": self.decimals,
            "format": self.format,
            "label": self.label,
            "logBase": self.log_base,
            "max": self.max,
            "min": self.min,
            "show": self.show,
        }


class YAxes(BaseModel):
    left: YAxis = YAxis(format=SHORT_FORMAT)
    right: YAxis = YAxis(format=SHORT_FORMAT)

    def to_json_data(self) -> list[Any]:
        return [self.left.to_json_data(), self.right.to_json_data()]


def single_y_axis(**kwargs) -> YAxes:
    axis = YAxis(**kwargs)
    return YAxes(left=axis, right=axis)


def to_y_axes(data: Any) -> YAxes:
    if isinstance(data, YAxes):
        return data
    if not isinstance(data, (list, tuple)):
        msg = f"Y axes must be either YAxes or a list of two values, got {data!r}"
        raise ValueError(msg)
    if len(data) != 2:
        msg = f"Must specify exactly two YAxes, got {len(data)}: {data!r}"
        raise ValueError(msg)
    warnings.warn(
        "Specify Y axes using YAxes or single_y_axis, rather than a list/tuple",
        DeprecationWarning,
        stacklevel=3,
    )
    return YAxes(left=data[0], right=data[1])


def _balance_panels(panels: list[Any]) -> list[Any]:
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
    h: int = Field(gt=0, description="Height must be greater than 0")
    w: int = Field(ge=1, le=24, description="Width must be in the range 1-24")
    x: int = Field(ge=0, description="X coordinate must be non-negative")
    y: int = Field(ge=0, description="Y coordinate must be non-negative")

    def to_json_data(self) -> dict:
        return {"h": self.h, "w": self.w, "x": self.x, "y": self.y}


class Annotations(BaseModel):
    list_: list[Any] = Field([], alias="list")

    def to_json_data(self) -> dict:
        return {"list": self.list_}


class DataLink(BaseModel):
    title: Any
    link_url: str = Field(alias="linkUrl")
    is_new_tab: bool = Field(default=False, alias="isNewTab")

    def to_json_data(self) -> dict:
        return {
            "title": self.title,
            "url": self.link_url,
            "targetBlank": self.is_new_tab,
        }


class DataSourceInput(BaseModel):
    name: Any
    label: Any
    plugin_id: Any = Field(alias="pluginId")
    plugin_name: Any = Field(alias="pluginName")
    description: str = ""

    def to_json_data(self) -> dict:
        return {
            "description": self.description,
            "label": self.label,
            "name": self.name,
            "pluginId": self.plugin_id,
            "pluginName": self.plugin_name,
            "type": "datasource",
        }


class ConstantInput(BaseModel):
    name: Any
    label: Any
    value: Any
    description: str = ""

    def to_json_data(self) -> dict:
        return {
            "description": self.description,
            "label": self.label,
            "name": self.name,
            "type": "constant",
            "value": self.value,
        }


class DashboardLink(BaseModel):
    as_dropdown: bool = Field(default=False, alias="asDropdown")
    icon: str = "external link"
    include_vars: bool = Field(default=False, alias="includeVars")
    keep_time: bool = Field(default=True, alias="keepTime")
    tags: list[str] = []
    target_blank: bool = Field(default=False, alias="targetBlank")
    title: str = ""
    tooltip: str = ""
    type_: str = Field(default="dashboards", alias="type")
    uri: str = ""

    def to_json_data(self) -> dict:
        return {
            "asDropdown": self.as_dropdown,
            "icon": self.icon,
            "includeVars": self.include_vars,
            "keepTime": self.keep_time,
            "tags": self.tags,
            "targetBlank": self.target_blank,
            "title": self.title,
            "tooltip": self.tooltip,
            "type": self.type_,
            "url": self.uri,
        }


class ExternalLink(BaseModel):
    uri: Any
    title: Any
    keep_time: bool = Field(default=False, alias="keepTime")

    def to_json_data(self) -> dict:
        return {
            "keepTime": self.keep_time,
            "title": self.title,
            "type": "link",
            "url": self.uri,
        }


# ---------------------------------------------------------------------------
# Template and Templating
# ---------------------------------------------------------------------------


class Template(BaseModel):
    name: Any
    query: Any
    current_: dict[str, Any] = Field(default={}, exclude=True)
    default: Any | None = None
    data_source: Any | None = Field(default=None, alias="dataSource")
    label: Any | None = None
    all_value: Any | None = Field(default=None, alias="allValue")
    include_all: bool = Field(default=False, alias="includeAll")
    multi: bool = False
    options: list[Any] = []
    regex: Any | None = None
    use_tags: bool = Field(default=False, alias="useTags")
    tags_query: Any | None = Field(default=None, alias="tagsQuery")
    tag_values_query: Any | None = Field(default=None, alias="tagValuesQuery")
    refresh: int = 1
    type_: str = Field(default="query", alias="type")
    hide: int = 0
    sort: Any = 1
    auto: bool = False
    auto_count: int = Field(default=30, alias="autoCount")
    auto_min: Any = Field(default="10s", alias="autoMin")

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if self.type_ == "custom":
            if not self.options:
                for value in str(self.query).split(","):
                    is_default = value == self.default
                    option = {"selected": is_default, "text": value, "value": value}
                    if is_default:
                        self.current_ = option
                    self.options.append(option)
            else:
                for option in self.options:
                    if option.get("selected"):
                        self.current_ = option
                        break
        else:
            self.current_ = {
                "selected": bool(self.default),
                "text": self.default,
                "value": self.default,
                "tags": [],
            }

    def to_json_data(self) -> dict:
        return {
            "allValue": self.all_value,
            "current": self.current_,
            "datasource": self.data_source,
            "hide": self.hide,
            "includeAll": self.include_all,
            "label": self.label,
            "multi": self.multi,
            "name": self.name,
            "options": self.options,
            "query": self.query,
            "refresh": self.refresh,
            "regex": self.regex,
            "sort": self.sort,
            "type": self.type_,
            "useTags": self.use_tags,
            "tagsQuery": self.tags_query,
            "tagValuesQuery": self.tag_values_query,
            "auto": self.auto,
            "auto_min": self.auto_min,
            "auto_count": self.auto_count,
        }


class Templating(BaseModel):
    list_: list[Any] = Field([], alias="list")

    def to_json_data(self) -> dict:
        return {"list": self.list_}


# ---------------------------------------------------------------------------
# Time and TimePicker
# ---------------------------------------------------------------------------


class Time(BaseModel):
    start: Any
    end: Any

    def to_json_data(self) -> dict:
        return {"from": self.start, "to": self.end}


DEFAULT_TIME = Time(start="now-1h", end="now")


class TimePicker(BaseModel):
    refresh_intervals: list[Any] = Field(alias="refreshIntervals")
    time_options: list[Any] = Field(alias="timeOptions")
    now_delay: Any | None = Field(default=None, alias="nowDelay")
    hidden: bool = False

    def to_json_data(self) -> dict:
        return {
            "refresh_intervals": self.refresh_intervals,
            "time_options": self.time_options,
            "nowDelay": self.now_delay,
            "hidden": self.hidden,
        }


DEFAULT_TIME_PICKER = TimePicker(
    refreshIntervals=["5s", "10s", "30s", "1m", "5m", "15m", "30m", "1h", "2h", "1d"],
    timeOptions=["5m", "15m", "1h", "6h", "12h", "24h", "2d", "7d", "30d"],
)

# ---------------------------------------------------------------------------
# Evaluator and TimeRange
# ---------------------------------------------------------------------------


class Evaluator(BaseModel):
    type: Any
    params: Any

    def to_json_data(self) -> dict:
        return {"type": self.type, "params": self.params}


# TODO: Update these to instances of Evaluator, not functions
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

    def to_json_data(self) -> list[Any]:
        return [self.from_time, self.to_time]


# ---------------------------------------------------------------------------
# Alert Conditions and Expressions
# ---------------------------------------------------------------------------


class AlertCondition(BaseModel):
    """
    A condition on an alert.

    :param target: Metric the alert condition is based on.
    :param evaluator: Evaluator function.
    :param time_range: TimeRange for the condition.
    :param operator: Combination operator.
    :param reducer_type: Reducer type.
    :param use_new_alerts: Whether to use Grafana 8.x new alerts.
    :param type_: Condition type.
    """

    target: Any | None = None
    evaluator: Any
    time_range: Any | None = Field(default=None, alias="timeRange")
    operator: str = Field(default="and", alias="operator")
    reducer_type: str = Field(default="last", alias="reducerType")
    use_new_alerts: bool = Field(default=False, alias="useNewAlerts")
    type_: str = Field(default="query", alias="type")

    def __get_query_params(self) -> list[Any]:
        if self.use_new_alerts:
            return [self.target.ref_id] if self.target else []
        if self.target and self.time_range:
            return [
                self.target.ref_id,
                self.time_range.from_time,
                self.time_range.to_time,
            ]
        return []

    def to_json_data(self) -> dict:
        condition = {
            "evaluator": self.evaluator.to_json_data(),
            "operator": {"type": self.operator},
            "query": {
                "model": self.target.to_json_data() if self.target else {},
                "params": self.__get_query_params(),
            },
            "reducer": {"params": [], "type": self.reducer_type},
            "type": self.type_,
        }
        if self.use_new_alerts:
            condition["query"].pop("model", None)
        return condition


class AlertExpression(BaseModel):
    ref_id: Any
    expression: str
    conditions: list[AlertCondition] = []
    expression_type: str = Field(default="classic_conditions", alias="expressionType")
    hide: bool = False
    interval_ms: int = Field(default=1000, alias="intervalMs")
    max_data_points: int = Field(default=43200, alias="maxDataPoints")
    reduce_function: str = Field(default="mean", alias="reduceFunction")
    reduce_mode: str = Field(default="strict", alias="reduceMode")
    reduce_replace_with: Any = Field(default=0, alias="reduceReplaceWith")
    resample_window: str = Field(default="10s", alias="resampleWindow")
    resample_downsampler: Any = Field(default="mean", alias="resampleDownsampler")
    resample_upsampler: Any = Field(default="fillna", alias="resampleUpsampler")

    def to_json_data(self) -> dict:
        conds = []
        for condition in self.conditions:
            condition.use_new_alerts = True
            if condition.target is None:
                condition.target = Any(ref_id=self.expression)
            conds.append(condition.to_json_data())
        return {
            "refId": self.ref_id,
            "queryType": "",
            "relativeTimeRange": {"from": 0, "to": 0},
            "datasourceUid": "-100",
            "model": {
                "conditions": conds,
                "datasource": {"type": "__expr__", "uid": "-100"},
                "expression": self.expression,
                "hide": self.hide,
                "intervalMs": self.interval_ms,
                "maxDataPoints": self.max_data_points,
                "refId": self.ref_id,
                "type": self.expression_type,
                "reducer": self.reduce_function,
                "settings": {
                    "mode": self.reduce_mode,
                    "replaceWithValue": self.reduce_replace_with,
                },
                "downsampler": self.resample_downsampler,
                "upsampler": self.resample_upsampler,
                "window": self.resample_window,
            },
        }


# ---------------------------------------------------------------------------
# Alert, AlertGroup, and Alert Rules
# ---------------------------------------------------------------------------


class Alert(BaseModel):
    name: Any
    message: Any
    alert_conditions: list[AlertCondition] = Field(default=[], alias="alertConditions")
    execution_error_state: str = Field(default="alerting", alias="executionErrorState")
    frequency: str = "60s"
    handler: int = 1
    no_data_state: str = Field(default="no_data", alias="noDataState")
    notifications: list[Any] = []
    grace_period: str = Field(default="5m", alias="gracePeriod")
    alert_rule_tags: dict[str, str] = Field({}, alias="alertRuleTags")

    def to_json_data(self) -> dict:
        return {
            "conditions": self.alert_conditions,
            "executionErrorState": self.execution_error_state,
            "frequency": self.frequency,
            "handler": self.handler,
            "message": self.message,
            "name": self.name,
            "noDataState": self.no_data_state,
            "notifications": self.notifications,
            "for": self.grace_period,
            "alertRuleTags": self.alert_rule_tags,
        }


class AlertGroup(BaseModel):
    name: Any
    rules: list[Any] = []
    folder: str = "alert"
    evaluate_interval: str = Field(default="1m", alias="evaluateInterval")

    def group_rules(self, rules: list[Any]) -> list[Any]:
        grouped_rules = []
        for each in rules:
            each.rule_group = self.name
            grouped_rules.append(each.to_json_data())
        return grouped_rules

    def to_json_data(self) -> dict:
        return {
            "name": self.name,
            "interval": self.evaluate_interval,
            "rules": self.group_rules(self.rules),
            "folder": self.folder,
        }


def is_valid_triggers(value: list[Any]) -> list[Any]:
    for trigger in value:
        if not isinstance(trigger, tuple):
            msg = "triggers must be a list of [(Target, AlertCondition)] tuples"
            raise ValueError(msg)
        if list(map(type, trigger)) != [Any, AlertCondition]:
            msg = "triggers must be a list of [(Target, AlertCondition)] tuples"
            raise ValueError(msg)
    return value


def is_valid_triggersv9(value: list[Any]) -> list[Any]:
    for trigger in value:
        if not isinstance(trigger, (Any, AlertExpression)):
            msg = "triggers must either be a Target or AlertExpression"
            raise ValueError(msg)
    return value


class AlertRulev8(BaseModel):
    title: Any
    triggers: list[Any] = Field(..., validator=is_valid_triggers)
    annotations: dict[Any, Any] = {}
    labels: dict[Any, Any] = {}
    evaluate_interval: str = Field(default="1m", alias="evaluateInterval")
    evaluate_for: str = Field(default="5m", alias="evaluateFor")
    no_data_alert_state: str = Field(default="Alerting", alias="noDataAlertState")
    error_alert_state: str = Field(default="Alerting", alias="errorAlertState")
    time_range_from: int = Field(default=300, alias="timeRangeFrom")
    time_range_to: int = Field(default=0, alias="timeRangeTo")
    uid: str | None = None
    dashboard_uid: str = ""
    panel_id: int = 0
    rule_group: str = ""

    def to_json_data(self) -> dict:
        data = []
        conditions = []
        for trigger, condition in self.triggers:
            data.append(
                {
                    "refId": trigger.ref_id,
                    "relativeTimeRange": {
                        "from": self.time_range_from,
                        "to": self.time_range_to,
                    },
                    "datasourceUid": trigger.datasource,
                    "model": trigger.to_json_data(),
                }
            )
            condition.use_new_alerts = True
            condition.target = trigger
            conditions.append(condition.to_json_data())
        data.append(
            {
                "refId": "CONDITION",
                "datasourceUid": "-100",
                "model": {
                    "conditions": conditions,
                    "refId": "CONDITION",
                    "type": "classic_conditions",
                },
            }
        )
        return {
            "for": self.evaluate_for,
            "labels": self.labels,
            "annotations": self.annotations,
            "grafana_alert": {
                "title": self.title,
                "condition": "CONDITION",
                "data": data,
                "intervalSeconds": self.evaluate_interval,
                "exec_err_state": self.error_alert_state,
                "no_data_state": self.no_data_alert_state,
                "uid": self.uid,
                "rule_group": self.rule_group,
            },
        }


class AlertRulev9(BaseModel):
    title: Any
    triggers: list[Any] = Field([], validator=is_valid_triggersv9)
    annotations: dict[Any, Any] = {}
    labels: dict[Any, Any] = {}
    evaluate_for: str = Field(default="5m", alias="evaluateFor")
    no_data_alert_state: str = Field(default="Alerting", alias="noDataAlertState")
    error_alert_state: str = Field(default="Alerting", alias="errorAlertState")
    condition: str = "B"
    time_range_from: int = Field(default=300, alias="timeRangeFrom")
    time_range_to: int = Field(default=0, alias="timeRangeTo")
    uid: str | None = None
    dashboard_uid: str = ""
    panel_id: int = 0

    def to_json_data(self) -> dict:
        data = []
        for trigger in self.triggers:
            if isinstance(trigger, Any):
                data.append(
                    {
                        "refId": trigger.ref_id,
                        "relativeTimeRange": {
                            "from": self.time_range_from,
                            "to": self.time_range_to,
                        },
                        "datasourceUid": trigger.datasource,
                        "model": trigger.to_json_data(),
                    }
                )
            else:
                data.append(trigger.to_json_data())
        return {
            "uid": self.uid,
            "for": self.evaluate_for,
            "labels": self.labels,
            "annotations": self.annotations,
            "grafana_alert": {
                "title": self.title,
                "condition": self.condition,
                "data": data,
                "no_data_state": self.no_data_alert_state,
                "exec_err_state": self.error_alert_state,
            },
        }


class AlertFileBasedProvisioning(BaseModel):
    groups: Any

    def to_json_data(self) -> dict:
        return {"apiVersion": 1, "groups": self.groups}


class Notification(BaseModel):
    uid: Any

    def to_json_data(self) -> dict:
        return {"uid": self.uid}


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------


class Dashboard(BaseModel):
    title: Any
    annotations: Any
    description: str = ""
    editable: bool = True
    gnet_id: Any | None = Field(default=None, alias="gnetId")
    graph_tooltip: int = Field(default=0, alias="graphTooltip")
    hide_controls: bool = Field(default=False, alias="hideControls")
    id: Any | None = None
    inputs: list[Any] = []
    links: list[Any] = []
    panels: list[Any] = []
    refresh: str = "10s"
    rows: list[Any] = []
    schema_version: int = Field(default=12, alias="schemaVersion")
    shared_crosshair: bool = Field(default=False, alias="sharedCrosshair")
    style: Any = "dark"
    tags: list[Any] = []
    templating: Any
    time: Any = Field(TimeRange(from_time="now-1h", to_time="now"))
    time_picker: Any = Field(
        default=TimePicker(
            refreshIntervals=[
                "5s",
                "10s",
                "30s",
                "1m",
                "5m",
                "15m",
                "30m",
                "1h",
                "2h",
                "1d",
            ],
            timeOptions=["5m", "15m", "1h", "6h", "12h", "24h", "2d", "7d", "30d"],
        ),
        alias="timePicker",
    )
    timezone: Any = "utc"
    version: int = 0
    uid: Any | None = None

    def _iter_panels(self):
        for row in self.rows:
            for panel in row._iter_panels():
                yield panel
        for panel in self.panels:
            yield panel
            if hasattr(panel, "_iter_panels"):
                yield from panel._iter_panels()

    def _map_panels(self, f) -> Any:
        new_rows = [row._map_panels(f) for row in self.rows]
        new_panels = [panel._map_panels(f) for panel in self.panels]
        return self.copy(update={"rows": new_rows, "panels": new_panels})

    def auto_panel_ids(self):
        ids = {panel.id for panel in self._iter_panels() if panel.id}
        auto_ids = (i for i in itertools.count(1) if i not in ids)

        def set_id(panel):
            return panel if panel.id else panel.copy(update={"id": next(auto_ids)})

        return self._map_panels(set_id)

    def to_json_data(self) -> dict:
        if self.panels and self.rows:
            pass  # Your logic here
        return {
            "__inputs": self.inputs,
            "annotations": self.annotations.to_json_data(),
            "description": self.description,
            "editable": self.editable,
            "gnetId": self.gnet_id,
            "graphTooltip": self.graph_tooltip,
            "hideControls": self.hide_controls,
            "id": self.id,
            "links": self.links,
            "panels": self.panels if not self.rows else [],
            "refresh": self.refresh,
            "rows": self.rows,
            "schemaVersion": self.schema_version,
            "sharedCrosshair": self.shared_crosshair,
            "style": self.style,
            "tags": self.tags,
            "templating": self.templating.to_json_data(),
            "title": self.title,
            "time": self.time.to_json_data(),
            "timepicker": self.time_picker.to_json_data(),
            "timezone": self.timezone,
            "version": self.version,
            "uid": self.uid,
        }


def _deep_update(base_dict: dict, extra_dict: dict | None) -> dict:
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
    data_source: Any | None = Field(default=None, alias="dataSource")
    targets: list[Any] = []
    title: str = ""
    cache_timeout: Any | None = Field(default=None, alias="cacheTimeout")
    description: Any | None = None
    editable: bool = True
    error: bool = False
    height: Any | None = None
    grid_pos: Any | None = Field(default=None, alias="gridPos")
    hide_time_override: bool = Field(default=False, alias="hideTimeOverride")
    id: Any | None = None
    interval: Any | None = None
    links: list[Any] = []
    max_data_points: int = Field(default=100, alias="maxDataPoints")
    min_span: Any | None = Field(default=None, alias="minSpan")
    repeat: Repeat
    span: Any | None = None
    thresholds: list[Any] = []
    threshold_type: str = Field(default="absolute", alias="thresholdType")
    time_from: Any | None = Field(default=None, alias="timeFrom")
    time_shift: Any | None = Field(default=None, alias="timeShift")
    transparent: bool = Field(default=False)
    transformations: list[Any] = []
    extra_json: dict[Any, Any] | None = Field(default=None, alias="extraJson")

    def _map_panels(self, f) -> Any:
        return f(self)

    def panel_json(self, overrides: dict) -> dict:
        res = {
            "cacheTimeout": self.cache_timeout,
            "datasource": self.data_source,
            "description": self.description,
            "editable": self.editable,
            "error": self.error,
            "fieldConfig": {
                "defaults": {
                    "thresholds": {
                        "mode": self.threshold_type,
                        "steps": self.thresholds,
                    },
                },
            },
            "height": self.height,
            "gridPos": self.grid_pos,
            "hideTimeOverride": self.hide_time_override,
            "id": self.id,
            "interval": self.interval,
            "links": self.links,
            "maxDataPoints": self.max_data_points,
            "minSpan": self.min_span,
            "repeat": self.repeat.variable,
            "repeatDirection": self.repeat.direction,
            "maxPerRow": self.repeat.max_per_row,
            "span": self.span,
            "targets": self.targets,
            "timeFrom": self.time_from,
            "timeShift": self.time_shift,
            "title": self.title,
            "transparent": self.transparent,
            "transformations": self.transformations,
        }
        _deep_update(res, overrides)
        _deep_update(res, self.extra_json)
        return res


class ePict(Panel):
    bg_url: str = Field(default="", alias="bgURL")
    auto_scale: bool = Field(default=True, alias="autoScale")
    boxes: list[ePictBox] = []

    def to_json_data(self) -> dict:
        graph_object = {
            "type": "larona-epict-panel",
            "options": {
                "autoScale": self.auto_scale,
                "bgURL": self.bg_url,
                "boxes": [box.to_json_data() for box in self.boxes],
            },
        }
        return self.panel_json(graph_object)


class RowPanel(Panel):
    panels: list[Any] = []
    collapsed: bool = False

    def _iter_panels(self):
        return iter(self.panels)

    def _map_panels(self, f):
        return self.copy(update={"panels": [f(panel) for panel in self.panels]})

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "collapsed": self.collapsed,
                "panels": [p.to_json_data() for p in self.panels],
                "type": "row",
            }
        )


class Row(BaseModel):
    panels: list[Any] = []
    collapse: bool = False
    editable: bool = True
    height: Pixels = Pixels(250)
    show_title: Any | None = Field(default=None, alias="showTitle")
    title: Any | None = None
    repeat: Any | None = None

    def _iter_panels(self):
        return iter(self.panels)

    def _map_panels(self, f):
        new_panels = [f(panel) for panel in self.panels]
        return self.copy(update={"panels": new_panels})

    def to_json_data(self) -> dict:
        show_title_val = False
        title_val = "New row"
        if self.title is not None:
            show_title_val = True
            title_val = self.title
        if self.show_title is not None:
            show_title_val = self.show_title
        return {
            "collapse": self.collapse,
            "editable": self.editable,
            "height": self.height.to_json_data(),
            "panels": [p.to_json_data() for p in self.panels],
            "showTitle": show_title_val,
            "title": title_val,
            "repeat": self.repeat,
        }


class Graph(Panel):
    alert: Any | None = None
    alert_threshold: bool = Field(default=True, alias="alertThreshold")
    alias_colors: dict[Any, Any] = Field({}, alias="aliasColors")
    align: bool = False
    align_level: int = Field(default=0, alias="alignLevel")
    bars: bool = False
    data_links: list[Any] = Field([], alias="dataLinks")
    fill: int = Field(default=1)
    fill_gradient: int = Field(default=0, alias="fillGradient")
    grid: Grid
    is_new: bool = Field(default=True, alias="isNew")
    legend: Legend
    lines: bool = True
    line_width: Any = Field(default=2, alias="lineWidth")
    null_point_mode: Any = Field(default="connected", alias="nullPointMode")
    percentage: bool = False
    point_radius: Any = Field(default=5, alias="pointRadius")
    points: bool = False
    renderer: Any = Field(default="flot")
    series_overrides: list[Any] = Field([], alias="seriesOverrides")
    stack: bool = False
    stepped_line: bool = Field(default=False, alias="steppedLine")
    tooltip: Tooltip
    thresholds: list[Any] = []
    unit: str = ""
    x_axis: XAxis = Field(alias="xAxis")
    y_axes: YAxes = Field(alias="yAxes")

    def to_json_data(self) -> dict:
        graph_object = {
            "aliasColors": self.alias_colors,
            "bars": self.bars,
            "error": self.error,
            "fieldConfig": {"defaults": {"unit": self.unit}},
            "fill": self.fill,
            "grid": self.grid.to_json_data(),
            "isNew": self.is_new,
            "legend": self.legend.to_json_data(),
            "lines": self.lines,
            "linewidth": self.line_width,
            "minSpan": self.min_span,
            "nullPointMode": self.null_point_mode,
            "options": {
                "dataLinks": self.data_links,
                "alertThreshold": self.alert_threshold,
            },
            "percentage": self.percentage,
            "pointradius": self.point_radius,
            "points": self.points,
            "renderer": self.renderer,
            "seriesOverrides": self.series_overrides,
            "stack": self.stack,
            "steppedLine": self.stepped_line,
            "tooltip": self.tooltip.to_json_data(),
            "thresholds": self.thresholds,
            "type": "graph",
            "xaxis": self.x_axis.to_json_data(),
            "yaxes": self.y_axes.to_json_data(),
            "yaxis": {"align": self.align, "alignLevel": self.align_level},
        }
        if self.alert:
            graph_object["alert"] = self.alert
            graph_object["thresholds"] = []
        return self.panel_json(graph_object)

    def _iter_targets(self):
        yield from self.targets

    def _map_targets(self, f):
        new_targets = [f(t) for t in self.targets]
        return self.copy(update={"targets": new_targets})

    def auto_ref_ids(self):
        ref_ids = {t.ref_id for t in self._iter_targets() if t.ref_id}
        double_candidate_refs = [
            p[0] + p[1] for p in itertools.product(string.ascii_uppercase, repeat=2)
        ]
        candidate_ref_ids = itertools.chain(
            string.ascii_uppercase, double_candidate_refs
        )
        auto_ref_ids = (i for i in candidate_ref_ids if i not in ref_ids)

        def set_refid(t):
            return t if t.ref_id else t.copy(update={"ref_id": next(auto_ref_ids)})

        return self._map_targets(set_refid)


class TimeSeries(Panel):
    axis_placement: str = Field(default="auto", alias="axisPlacement")
    axis_label: str = Field(default="", alias="axisLabel")
    bar_alignment: int = Field(default=0, alias="barAlignment")
    color_mode: str = Field(default="palette-classic", alias="colorMode")
    draw_style: str = Field(default="line", alias="drawStyle")
    fill_opacity: int = Field(default=0, alias="fillOpacity")
    gradient_mode: str = Field(default="none", alias="gradientMode")
    legend_display_mode: str = Field(default="list", alias="legendDisplayMode")
    legend_placement: str = Field(default="bottom", alias="legendPlacement")
    legend_calcs: list[str] = Field([], alias="legendCalcs")
    line_interpolation: str = Field(default="linear", alias="lineInterpolation")
    line_width: int = Field(default=1, alias="lineWidth")
    mappings: list[Any] = []
    overrides: list[Any] = []
    point_size: int = Field(default=5, alias="pointSize")
    scale_distribution_type: str = Field(
        default="linear", alias="scaleDistributionType"
    )
    scale_distribution_log: int = Field(default=2, alias="scaleDistributionLog")
    span_nulls: bool = Field(default=False, alias="spanNulls")
    show_points: str = Field(default="auto", alias="showPoints")
    stacking: dict[str, Any] = {}
    tooltip_mode: str = Field(default="single", alias="tooltipMode")
    tooltip_sort: str = Field(default="none", alias="tooltipSort")
    unit: str = ""
    thresholds_style_mode: str = Field(default="off", alias="thresholdsStyleMode")
    value_min: int | None = Field(default=None, alias="valueMin")
    value_max: int | None = Field(default=None, alias="valueMax")
    value_decimals: int | None = Field(default=None, alias="valueDecimals")
    axis_soft_min: int | None = Field(default=None, alias="axisSoftMin")
    axis_soft_max: int | None = Field(default=None, alias="axisSoftMax")

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": self.color_mode},
                        "custom": {
                            "axisPlacement": self.axis_placement,
                            "axisLabel": self.axis_label,
                            "drawStyle": self.draw_style,
                            "lineInterpolation": self.line_interpolation,
                            "barAlignment": self.bar_alignment,
                            "lineWidth": self.line_width,
                            "fillOpacity": self.fill_opacity,
                            "gradientMode": self.gradient_mode,
                            "spanNulls": self.span_nulls,
                            "showPoints": self.show_points,
                            "pointSize": self.point_size,
                            "stacking": self.stacking,
                            "scaleDistribution": {
                                "type": self.scale_distribution_type,
                                "log": self.scale_distribution_log,
                            },
                            "hideFrom": {
                                "tooltip": False,
                                "viz": False,
                                "legend": False,
                            },
                            "thresholdsStyle": {"mode": self.thresholds_style_mode},
                            "axisSoftMin": self.axis_soft_min,
                            "axisSoftMax": self.axis_soft_max,
                        },
                        "mappings": self.mappings,
                        "min": self.value_min,
                        "max": self.value_max,
                        "decimals": self.value_decimals,
                        "unit": self.unit,
                    },
                    "overrides": self.overrides,
                },
                "options": {
                    "legend": {
                        "displayMode": self.legend_display_mode,
                        "placement": self.legend_placement,
                        "calcs": self.legend_calcs,
                    },
                    "tooltip": {"mode": self.tooltip_mode, "sort": self.tooltip_sort},
                },
                "type": "timeseries",
            }
        )


# ---------------------------------------------------------------------------
# ValueMap, SparkLine, Gauge, RangeMap, and Discrete Panel
# ---------------------------------------------------------------------------


class ValueMap(BaseModel):
    text: Any
    value: Any
    op: str = "="

    def to_json_data(self) -> dict:
        return {"op": self.op, "text": self.text, "value": self.value}


class SparkLine(BaseModel):
    fill_color: RGBA = Field(default=Color((31, 118, 189, 0.18)), alias="fillColor")
    full: bool = False
    line_color: RGB = Field(default=Color((31, 120, 193)), alias="lineColor")
    show: bool = False

    def to_json_data(self) -> dict:
        return {
            "fillColor": self.fill_color.to_json_data(),
            "full": self.full,
            "lineColor": self.line_color.to_json_data(),
            "show": self.show,
        }


class Gauge(BaseModel):
    min_value: int = Field(default=0, alias="minValue")
    max_value: int = Field(default=100, alias="maxValue")
    show: bool = False
    threshold_labels: bool = Field(default=False, alias="thresholdLabels")
    threshold_markers: bool = Field(default=True, alias="thresholdMarkers")

    def to_json_data(self) -> dict:
        return {
            "maxValue": self.max_value,
            "minValue": self.min_value,
            "show": self.show,
            "thresholdLabels": self.threshold_labels,
            "thresholdMarkers": self.threshold_markers,
        }


class RangeMap(BaseModel):
    start: Any
    end: Any
    text: Any

    def to_json_data(self) -> dict:
        return {"from": self.start, "to": self.end, "text": self.text}


class DiscreteColorMappingItem(BaseModel):
    text: str
    color: Any = Field(default=Color((216, 200, 27, 0.27)))

    def to_json_data(self) -> dict:
        return {
            "color": self.color.to_json_data()
            if hasattr(self.color, "to_json_data")
            else self.color,
            "text": self.text,
        }


class Discrete(Panel):
    background_color: RGBA = Field(
        default=Color((128, 128, 128, 0.1)), alias="backgroundColor"
    )
    line_color: RGBA = Field(default=Color((0, 0, 0, 0.1)), alias="lineColor")
    metric_name_color: Any = Field(default="#000000", alias="metricNameColor")
    time_text_color: Any = Field(default="#d8d9da", alias="timeTextColor")
    value_text_color: Any = Field(default="#000000", alias="valueTextColor")
    decimals: int = 0
    legend_percent_decimals: int = Field(default=0, alias="legendPercentDecimals")
    row_height: int = Field(default=50, alias="rowHeight")
    text_size: int = Field(default=24, alias="textSize")
    text_size_time: int = Field(default=12, alias="textSizeTime")
    units: str = "none"
    legend_sort_by: str = Field(default="-ms", alias="legendSortBy")
    highlight_on_mouseover: bool = Field(default=True, alias="highlightOnMouseover")
    show_legend: bool = Field(default=True, alias="showLegend")
    show_legend_percent: bool = Field(default=True, alias="showLegendPercent")
    show_legend_names: bool = Field(default=True, alias="showLegendNames")
    show_legend_values: bool = Field(default=True, alias="showLegendValues")
    show_time_axis: bool = Field(default=True, alias="showTimeAxis")
    use_12_hour_clock: bool = Field(default=False, alias="use12HourClock")
    write_metric_names: bool = Field(default=False, alias="writeMetricNames")
    write_last_value: bool = Field(default=True, alias="writeLastValue")
    write_all_values: bool = Field(default=False, alias="writeAllValues")
    show_distinct_count: Any | None = Field(default=None, alias="showDistinctCount")
    show_legend_counts: Any | None = Field(default=None, alias="showLegendCounts")
    show_legend_time: Any | None = Field(default=None, alias="showLegendTime")
    show_transition_count: Any | None = Field(default=None, alias="showTransitionCount")
    color_maps: list[DiscreteColorMappingItem] = Field([], alias="colorMaps")
    range_maps: list[RangeMap] = Field([], alias="rangeMaps")
    value_maps: list[ValueMap] = Field([], alias="valueMaps")

    def to_json_data(self) -> dict:
        graph_object = {
            "type": "natel-discrete-panel",
            "backgroundColor": self.background_color.to_json_data()
            if hasattr(self.background_color, "to_json_data")
            else self.background_color,
            "lineColor": self.line_color.to_json_data()
            if hasattr(self.line_color, "to_json_data")
            else self.line_color,
            "metricNameColor": self.metric_name_color,
            "timeTextColor": self.time_text_color,
            "valueTextColor": self.value_text_color,
            "legendPercentDecimals": self.legend_percent_decimals,
            "decimals": self.decimals,
            "rowHeight": self.row_height,
            "textSize": self.text_size,
            "textSizeTime": self.text_size_time,
            "units": self.units,
            "legendSortBy": self.legend_sort_by,
            "highlightOnMouseover": self.highlight_on_mouseover,
            "showLegend": self.show_legend,
            "showLegendPercent": self.show_legend_percent,
            "showLegendNames": self.show_legend_names,
            "showLegendValues": self.show_legend_values,
            "showTimeAxis": self.show_time_axis,
            "use12HourClock": self.use_12_hour_clock,
            "writeMetricNames": self.write_metric_names,
            "writeLastValue": self.write_last_value,
            "writeAllValues": self.write_all_values,
            "showDistinctCount": self.show_distinct_count,
            "showLegendCounts": self.show_legend_counts,
            "showLegendTime": self.show_legend_time,
            "showTransitionCount": self.show_transition_count,
            "colorMaps": [cm.to_json_data() for cm in self.color_maps],
            "rangeMaps": [rm.to_json_data() for rm in self.range_maps],
            "valueMaps": [vm.to_json_data() for vm in self.value_maps],
        }
        return self.panel_json(graph_object)


# ---------------------------------------------------------------------------
# Text, Alertlist, and Stat Panels
# ---------------------------------------------------------------------------


class Text(Panel):
    content: str = ""
    error: bool = False
    mode: Literal["markdown", "text", "html"] = "markdown"

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "type": "text",
                "error": self.error,
                "options": {"content": self.content, "mode": self.mode},
            }
        )


class Alertlist(BaseModel):
    dashboard_tags: list[str] = Field([], alias="dashboardTags")
    description: str = ""
    grid_pos: GridPos | None = Field(default=None, alias="gridPos")
    id: Any | None = None
    limit: int = 10
    links: list[Any] = []
    name_filter: str = Field(default="", alias="nameFilter")
    only_alerts_on_dashboard: bool = Field(default=True, alias="onlyAlertsOnDashboard")
    show: Any = "current"
    sort_order: int = Field(default=1, alias="sortOrder")
    span: int = 6
    state_filter: list[Any] = Field([], alias="stateFilter")
    title: str = ""
    transparent: bool = False
    alert_name: str = Field(default="", alias="alertName")

    def to_json_data(self) -> dict:
        return {
            "dashboardTags": self.dashboard_tags,
            "description": self.description,
            "gridPos": self.grid_pos.to_json_data() if self.grid_pos else None,
            "id": self.id,
            "limit": self.limit,
            "links": self.links,
            "nameFilter": self.name_filter,
            "onlyAlertsOnDashboard": self.only_alerts_on_dashboard,
            "show": self.show,
            "sortOrder": self.sort_order,
            "span": self.span,
            "stateFilter": self.state_filter,
            "title": self.title,
            "transparent": self.transparent,
            "type": "alertlist",
            "options": {"alertName": self.alert_name},
        }


class Stat(Panel):
    alignment: str = "auto"
    color: Any | None = None
    color_mode: str = Field(default="value", alias="colorMode")
    decimals: Any | None = None
    format: str = "none"
    graph_mode: str = Field(default="area", alias="graphMode")
    mappings: list[Any] = []
    no_value: str = Field(default="none", alias="noValue")
    orientation: str = "auto"
    overrides: list[Any] = []
    reduce_calc: str = Field(default="mean", alias="reduceCalc")
    fields: str = ""
    text_mode: str = Field(default="auto", alias="textMode")
    thresholds: str = ""

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "fieldConfig": {
                    "defaults": {
                        "color": self.color,
                        "custom": {},
                        "decimals": self.decimals,
                        "mappings": self.mappings,
                        "unit": self.format,
                        "noValue": self.no_value,
                    },
                    "overrides": self.overrides,
                },
                "options": {
                    "textMode": self.text_mode,
                    "colorMode": self.color_mode,
                    "graphMode": self.graph_mode,
                    "justifyMode": self.alignment,
                    "orientation": self.orientation,
                    "reduceOptions": {
                        "calcs": [self.reduce_calc],
                        "fields": self.fields,
                        "values": False,
                    },
                },
                "type": "stat",
            }
        )


class StatValueMappingItem(BaseModel):
    text: Any
    map_value: str = Field(default="", alias="mapValue")
    color: str = ""
    index: Any | None = None

    def to_json_data(self) -> dict:
        return {
            self.map_value: {
                "text": self.text,
                "color": self.color,
                "index": self.index,
            },
        }


class StatValueMappings(BaseModel):
    mapping_items: list[StatValueMappingItem] = Field([], alias="mappingItems")

    def __init__(self, *mappings: StatValueMappingItem) -> None:
        super().__init__(mapping_items=list(mappings))

    def to_json_data(self) -> dict:
        ret_dict = {"type": "value", "options": {}}
        for item in self.mapping_items:
            ret_dict["options"].update(item.to_json_data())
        return ret_dict


class StatRangeMappings(BaseModel):
    text: Any
    start_value: int = Field(default=0, alias="startValue")
    end_value: int = Field(default=0, alias="endValue")
    color: str = ""
    index: Any | None = None

    def to_json_data(self) -> dict:
        return {
            "type": "range",
            "options": {
                "from": self.start_value,
                "to": self.end_value,
                "result": {"text": self.text, "color": self.color, "index": self.index},
            },
        }


class StatMapping(BaseModel):
    text: Any
    map_value: str = Field(default="", alias="mapValue")
    start_value: str = Field(default="", alias="startValue")
    end_value: str = Field(default="", alias="endValue")
    id: Any | None = None

    def to_json_data(self) -> dict:
        mapping_type = (
            1
            if self.map_value
            else 2  # MAPPING_TYPE_VALUE_TO_TEXT if value else MAPPING_TYPE_RANGE_TO_TEXT
        )
        return {
            "operator": "",
            "text": self.text,
            "type": mapping_type,
            "value": self.map_value,
            "from": self.start_value,
            "to": self.end_value,
            "id": self.id,
        }


class StatValueMapping(BaseModel):
    text: Any
    map_value: str = Field(default="", alias="mapValue")
    id: Any | None = None

    def to_json_data(self) -> dict:
        return StatMapping(
            text=self.text,
            map_value=self.map_value,
            id=self.id,
        ).to_json_data()


class StatRangeMapping(BaseModel):
    text: Any
    start_value: str = Field(default="", alias="startValue")
    end_value: str = Field(default="", alias="endValue")
    id: Any | None = None

    def to_json_data(self) -> dict:
        return StatMapping(
            text=self.text,
            start_value=self.start_value,
            end_value=self.end_value,
            id=self.id,
        ).to_json_data()


class SingleStat(Panel):
    cache_timeout: Any | None = Field(default=None, alias="cacheTimeout")
    colors: list[Color] = [
        Color((50, 172, 45, 0.97)),
        Color((237, 129, 40, 0.89)),
        Color((245, 54, 54, 0.9)),
    ]
    color_background: bool = Field(default=False, alias="colorBackground")
    color_value: bool = Field(default=False, alias="colorValue")
    decimals: Any | None = None
    format: str = "none"
    gauge: Gauge
    mapping_type: int = Field(
        default=1, alias="mappingType"
    )  # MAPPING_TYPE_VALUE_TO_TEXT
    mapping_types: list[Any] = [
        {"name": "value to text", "value": 1},
        {"name": "range to text", "value": 2},
    ]
    min_span: Any | None = Field(default=None, alias="minSpan")
    null_text: Any | None = Field(default=None, alias="nullText")
    null_point_mode: str = Field(default="connected", alias="nullPointMode")
    postfix: str = ""
    postfix_font_size: str = Field(default="50%", alias="postfixFontSize")
    prefix: str = ""
    prefix_font_size: str = Field(default="50%", alias="prefixFontSize")
    range_maps: list[Any] = Field([], alias="rangeMaps")
    sparkline: SparkLine
    thresholds: str = ""
    value_font_size: str = Field(default="80%", alias="valueFontSize")
    value_name: str = Field(default="avg", alias="valueName")  # VTYPE_DEFAULT
    value_maps: list[Any] = Field([], alias="valueMaps")

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "cacheTimeout": self.cache_timeout,
                "colorBackground": self.color_background,
                "colorValue": self.color_value,
                "colors": self.colors,
                "decimals": self.decimals,
                "format": self.format,
                "gauge": self.gauge.to_json_data(),
                "mappingType": self.mapping_type,
                "mappingTypes": self.mapping_types,
                "minSpan": self.min_span,
                "nullPointMode": self.null_point_mode,
                "nullText": self.null_text,
                "postfix": self.postfix,
                "postfixFontSize": self.postfix_font_size,
                "prefix": self.prefix,
                "prefixFontSize": self.prefix_font_size,
                "rangeMaps": self.range_maps,
                "sparkline": self.sparkline.to_json_data(),
                "thresholds": self.thresholds,
                "type": "singlestat",
                "valueFontSize": self.value_font_size,
                "valueMaps": self.value_maps,
                "valueName": self.value_name,
            }
        )


# ---------------------------------------------------------------------------
# Column Style and Table
# ---------------------------------------------------------------------------


class DateColumnStyleType(BaseModel):
    TYPE: str = "date"
    date_format: str = Field(default="YYYY-MM-DD HH:mm:ss", alias="dateFormat")

    def to_json_data(self) -> dict:
        return {"dateFormat": self.date_format, "type": self.TYPE}


class NumberColumnStyleType(BaseModel):
    TYPE: str = "number"
    color_mode: Any | None = Field(default=None, alias="colorMode")
    colors: list[Color] = [
        Color((50, 172, 45, 0.97)),
        Color((237, 129, 40, 0.89)),
        Color((245, 54, 54, 0.9)),
    ]
    thresholds: list[Any] = []
    decimals: int = Field(default=2)
    unit: str = Field(default="short", alias="unit")

    def to_json_data(self) -> dict:
        return {
            "colorMode": self.color_mode,
            "colors": self.colors,
            "decimals": self.decimals,
            "thresholds": self.thresholds,
            "type": self.TYPE,
            "unit": self.unit,
        }


class StringColumnStyleType(BaseModel):
    TYPE: str = "string"
    decimals: int = Field(default=2)
    color_mode: Any | None = Field(default=None, alias="colorMode")
    colors: list[Color] = [
        Color((50, 172, 45, 0.97)),
        Color((237, 129, 40, 0.89)),
        Color((245, 54, 54, 0.9)),
    ]
    thresholds: list[Any] = []
    preserve_format: bool = Field(default=False, alias="preserveFormat")
    sanitize: bool = False
    unit: str = Field(default="short", alias="unit")
    mapping_type: int = Field(
        default=1, alias="mappingType"
    )  # MAPPING_TYPE_VALUE_TO_TEXT
    value_maps: list[Any] = Field([], alias="valueMaps")
    range_maps: list[Any] = Field([], alias="rangeMaps")

    def to_json_data(self) -> dict:
        return {
            "decimals": self.decimals,
            "colorMode": self.color_mode,
            "colors": self.colors,
            "thresholds": self.thresholds,
            "unit": self.unit,
            "mappingType": self.mapping_type,
            "valueMaps": self.value_maps,
            "rangeMaps": self.range_maps,
            "preserveFormat": self.preserve_format,
            "sanitize": self.sanitize,
            "type": self.TYPE,
        }


class HiddenColumnStyleType(BaseModel):
    TYPE: str = "hidden"

    def to_json_data(self) -> dict:
        return {"type": self.TYPE}


class ColumnStyle(BaseModel):
    alias: str = ""
    pattern: str = ""
    align: Literal["auto", "left", "right", "center"] = "auto"
    link: bool = False
    link_open_in_new_tab: bool = Field(default=False, alias="linkOpenInNewTab")
    link_url: str = Field(default="", alias="linkUrl")
    link_tooltip: str = Field(default="", alias="linkTooltip")
    type: (
        NumberColumnStyleType
        | StringColumnStyleType
        | DateColumnStyleType
        | HiddenColumnStyleType
    )

    def to_json_data(self) -> dict:
        data = {
            "alias": self.alias,
            "pattern": self.pattern,
            "align": self.align,
            "link": self.link,
            "linkTargetBlank": self.link_open_in_new_tab,
            "linkUrl": self.link_url,
            "linkTooltip": self.link_tooltip,
        }
        data.update(self.type.to_json_data())
        return data


class ColumnSort(BaseModel):
    col: Any | None = None
    desc: bool = False

    def to_json_data(self) -> dict:
        return {"col": self.col, "desc": self.desc}


class Column(BaseModel):
    text: str = "Avg"
    value: str = "avg"

    def to_json_data(self) -> dict:
        return {"text": self.text, "value": self.value}


class TableSortByField(BaseModel):
    display_name: str = Field(default="", alias="displayName")
    desc: bool = False

    def to_json_data(self) -> dict:
        return {"displayName": self.display_name, "desc": self.desc}


class Table(Panel):
    align: str = "auto"
    color_mode: str = Field(default="thresholds", alias="colorMode")
    columns: list[Any] = []
    display_mode: str = Field(default="auto", alias="displayMode")
    font_size: str = Field(default="100%", alias="fontSize")
    filterable: bool = False
    mappings: list[Any] = []
    overrides: list[Any] = []
    show_header: bool = Field(default=True, alias="showHeader")
    span: int = 6
    unit: str = ""
    sort_by: list[TableSortByField] = Field([], alias="sortBy")

    @classmethod
    def with_styled_columns(cls, columns, styles=None, **kwargs) -> NoReturn:
        raise NotImplementedError

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "color": {"mode": self.color_mode},
                "columns": list(self.columns),
                "fontSize": self.font_size,
                "fieldConfig": {
                    "defaults": {
                        "custom": {
                            "align": self.align,
                            "displayMode": self.display_mode,
                            "filterable": self.filterable,
                        },
                        "unit": self.unit,
                        "mappings": self.mappings,
                    },
                    "overrides": self.overrides,
                },
                "hideTimeOverride": self.hide_time_override,
                "mappings": self.mappings,
                "minSpan": self.min_span,
                "options": {
                    "showHeader": self.show_header,
                    "sortBy": [s.to_json_data() for s in self.sort_by],
                },
                "type": "table",
            }
        )


class Threshold(BaseModel):
    color: Any
    index: int
    value: float
    line: bool = True
    op: str = Field(default="gt", alias="op")  # EVAL_GT
    yaxis: str = "left"

    def to_json_data(self) -> dict:
        return {
            "op": self.op,
            "yaxis": self.yaxis,
            "color": self.color,
            "line": self.line,
            "index": self.index,
            "value": "null" if self.index == 0 else self.value,
        }


# ---------------------------------------------------------------------------
# BarGauge and GaugePanel
# ---------------------------------------------------------------------------


class BarGauge(Panel):
    all_values: bool = Field(default=False, alias="allValues")
    calc: Any = Field(default="mean", alias="calc")
    data_links: list[Any] = Field([], alias="dataLinks")
    decimals: Any | None = None
    display_mode: Literal["lcd", "basic", "gradient"] = Field(
        default="basic", alias="displayMode"
    )
    format: str = "none"
    label: Any | None = None
    limit: Any | None = None
    max: int = 100
    min: int = 0
    orientation: Literal["horizontal", "vertical", "auto"] = "auto"
    range_maps: list[Any] = Field([], alias="rangeMaps")
    threshold_labels: bool = Field(default=False, alias="thresholdLabels")
    threshold_markers: bool = Field(default=True, alias="thresholdMarkers")
    thresholds: list[Threshold] = [
        Threshold(color="green", index=0, value=0.0),
        Threshold(color="red", index=1, value=80.0),
    ]
    value_maps: list[Any] = Field([], alias="valueMaps")

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "options": {
                    "displayMode": self.display_mode,
                    "fieldOptions": {
                        "calcs": [self.calc],
                        "defaults": {
                            "decimals": self.decimals,
                            "max": self.max,
                            "min": self.min,
                            "title": self.label,
                            "unit": self.format,
                            "links": self.data_links,
                        },
                        "limit": self.limit,
                        "mappings": self.value_maps,
                        "override": {},
                        "thresholds": self.thresholds,
                        "values": self.all_values,
                    },
                    "orientation": self.orientation,
                    "showThresholdLabels": self.threshold_labels,
                    "showThresholdMarkers": self.threshold_markers,
                },
                "type": "bargauge",
            }
        )


class GaugePanel(Panel):
    all_values: bool = Field(default=False, alias="allValues")
    calc: Any = Field(default="mean", alias="calc")
    data_links: list[Any] = Field([], alias="dataLinks")
    decimals: Any | None = None
    format: str = "none"
    label: Any | None = None
    limit: Any | None = None
    max: int = 100
    min: int = 0
    range_maps: list[Any] = Field([], alias="rangeMaps")
    threshold_labels: bool = Field(default=False, alias="thresholdLabels")
    threshold_markers: bool = Field(default=True, alias="thresholdMarkers")
    thresholds: list[Threshold] = [
        Threshold(color="green", index=0, value=0.0),
        Threshold(color="red", index=1, value=80.0),
    ]
    value_maps: list[Any] = Field([], alias="valueMaps")
    neutral: Any | None = None

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "fieldConfig": {
                    "defaults": {
                        "calcs": [self.calc],
                        "decimals": self.decimals,
                        "max": self.max,
                        "min": self.min,
                        "title": self.label,
                        "unit": self.format,
                        "links": self.data_links,
                        "limit": self.limit,
                        "mappings": self.value_maps,
                        "override": {},
                        "values": self.all_values,
                        "custom": {"neutral": self.neutral},
                    },
                    "showThresholdLabels": self.threshold_labels,
                    "showThresholdMarkers": self.threshold_markers,
                },
                "type": "gauge",
            }
        )


# ---------------------------------------------------------------------------
# Heatmap, Statusmap, Svg, PieChart, PieChartv2, Dashboardlist, and Logs
# ---------------------------------------------------------------------------


class HeatmapColor(BaseModel):
    card_color: str = Field(default="#b4ff00", alias="cardColor")
    color_scale: str = Field(default="sqrt", alias="colorScale")
    color_scheme: str = Field(default="interpolateOranges", alias="colorScheme")
    exponent: float = 0.5
    mode: str = "spectrum"
    max: Any | None = None
    min: Any | None = None

    def to_json_data(self) -> dict:
        return {
            "mode": self.mode,
            "cardColor": self.card_color,
            "colorScale": self.color_scale,
            "exponent": self.exponent,
            "colorScheme": self.color_scheme,
            "max": self.max,
            "min": self.min,
        }


class Heatmap(Panel):
    legend: dict[str, Any] = {"show": False}
    tooltip: Tooltip
    cards: dict[str, Any] = {"cardPadding": None, "cardRound": None}
    color: HeatmapColor
    data_format: str = Field(default="timeseries", alias="dataFormat")
    heatmap: dict[str, Any] = {}
    hide_zero_buckets: bool = Field(default=False, alias="hideZeroBuckets")
    highlight_cards: bool = Field(default=True, alias="highlightCards")
    options: list[Any] = []
    x_axis: XAxis = Field(alias="xAxis")
    x_bucket_number: Any | None = Field(default=None, alias="xBucketNumber")
    x_bucket_size: Any | None = Field(default=None, alias="xBucketSize")
    y_axis: YAxis = Field(alias="yAxis")
    y_bucket_bound: Any | None = Field(default=None, alias="yBucketBound")
    y_bucket_number: Any | None = Field(default=None, alias="yBucketNumber")
    y_bucket_size: Any | None = Field(default=None, alias="yBucketSize")
    reverse_y_buckets: bool = Field(default=False, alias="reverseYBuckets")

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "cards": self.cards,
                "color": self.color.to_json_data(),
                "dataFormat": self.data_format,
                "heatmap": self.heatmap,
                "hideZeroBuckets": self.hide_zero_buckets,
                "highlightCards": self.highlight_cards,
                "legend": self.legend,
                "options": self.options,
                "reverseYBuckets": self.reverse_y_buckets,
                "tooltip": self.tooltip.to_json_data(),
                "type": "heatmap",
                "xAxis": self.x_axis.to_json_data(),
                "xBucketNumber": self.x_bucket_number,
                "xBucketSize": self.x_bucket_size,
                "yAxis": self.y_axis.to_json_data(),
                "yBucketBound": self.y_bucket_bound,
                "yBucketNumber": self.y_bucket_number,
                "yBucketSize": self.y_bucket_size,
            }
        )


class StatusmapColor(BaseModel):
    card_color: str = Field(default="#b4ff00", alias="cardColor")
    color_scale: str = Field(default="sqrt", alias="colorScale")
    color_scheme: str = Field(default="GnYlRd", alias="colorScheme")
    exponent: float = 0.5
    mode: str = "spectrum"
    thresholds: list[Any] = []
    max: Any | None = None
    min: Any | None = None

    def to_json_data(self) -> dict:
        return {
            "mode": self.mode,
            "cardColor": self.card_color,
            "colorScale": self.color_scale,
            "exponent": self.exponent,
            "colorScheme": self.color_scheme,
            "max": self.max,
            "min": self.min,
            "thresholds": self.thresholds,
        }


class Statusmap(Panel):
    alert: Any | None = None
    cards: dict[str, Any] = {
        "cardRound": None,
        "cardMinWidth": 5,
        "cardHSpacing": 2,
        "cardVSpacing": 2,
    }
    color: StatusmapColor
    is_new: bool = Field(default=True, alias="isNew")
    legend: Legend
    null_point_mode: Any = Field(default="null as zero", alias="nullPointMode")
    tooltip: Tooltip
    x_axis: XAxis = Field(alias="xAxis")
    y_axis: YAxis = Field(alias="yAxis")

    def to_json_data(self) -> dict:
        graph_object = {
            "color": self.color.to_json_data(),
            "isNew": self.is_new,
            "legend": self.legend.to_json_data(),
            "minSpan": self.min_span,
            "nullPointMode": self.null_point_mode,
            "tooltip": self.tooltip.to_json_data(),
            "type": "flant-statusmap-panel",
            "xaxis": self.x_axis.to_json_data(),
            "yaxis": self.y_axis.to_json_data(),
        }
        if self.alert:
            graph_object["alert"] = self.alert
        return self.panel_json(graph_object)


class Svg(Panel):
    format: str = "none"
    js_code_file_path: str = Field("", alias="jsCodeFilePath")
    js_code_init_file_path: str = Field("", alias="jsCodeInitFilePath")
    height: Any | None = None
    svg_file_path: str = Field("", alias="svgFilePath")

    @staticmethod
    def read_file(file_path: str) -> str:
        if file_path:
            with open(file_path) as f:
                return f.read()
        return ""

    def to_json_data(self) -> dict:
        js_code = self.read_file(self.js_code_file_path)
        js_init_code = self.read_file(self.js_code_init_file_path)
        svg_data = self.read_file(self.svg_file_path)
        return self.panel_json(
            {
                "format": self.format,
                "js_code": js_code,
                "js_init_code": js_init_code,
                "svg_data": svg_data,
                "type": SVG_TYPE,
                "useSVGBuilder": False,
            },
        )


class PieChart(Panel):
    alias_colors: dict[Any, Any] = Field({}, alias="aliasColors")
    format: str = "none"
    legend_type: str = Field("Right side", alias="legendType")
    overrides: list[Any] = []
    pie_type: str = Field("pie", alias="pieType")
    percentage_decimals: int = Field(0, alias="percentageDecimals")
    show_legend: Any = Field(True, alias="showLegend")
    show_legend_values: Any = Field(True, alias="showLegendValues")
    show_legend_percentage: bool = Field(False, alias="showLegendPercentage")
    thresholds: str = ""

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "aliasColors": self.alias_colors,
                "format": self.format,
                "pieType": self.pie_type,
                "height": self.height,
                "fieldConfig": {
                    "defaults": {"custom": {}},
                    "overrides": self.overrides,
                },
                "legend": {
                    "show": self.show_legend,
                    "values": self.show_legend_values,
                    "percentage": self.show_legend_percentage,
                    "percentageDecimals": self.percentage_decimals,
                },
                "legendType": self.legend_type,
                "type": PIE_CHART_TYPE,
            },
        )


class PieChartv2(Panel):
    custom: dict[Any, Any] = {}
    color_mode: str = Field("palette-classic", alias="colorMode")
    legend_display_mode: str = Field("list", alias="legendDisplayMode")
    legend_placement: str = Field("bottom", alias="legendPlacement")
    legend_values: list[Any] = Field([], alias="legendValues")
    mappings: list[Any] = []
    overrides: list[Any] = []
    pie_type: str = Field("pie", alias="pieType")
    reduce_options_calcs: list[str] = Field(["lastNotNull"], alias="reduceOptionsCalcs")
    reduce_options_fields: str = Field("", alias="reduceOptionsFields")
    reduce_options_values: bool = Field(False, alias="reduceOptionsValues")
    tooltip_mode: str = Field("single", alias="tooltipMode")
    tooltip_sort: str = Field("none", alias="tooltipSort")
    unit: str = ""

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": self.color_mode},
                        "custom": self.custom,
                        "mappings": self.mappings,
                        "unit": self.unit,
                    },
                    "overrides": self.overrides,
                },
                "options": {
                    "reduceOptions": {
                        "values": self.reduce_options_values,
                        "calcs": self.reduce_options_calcs,
                        "fields": self.reduce_options_fields,
                    },
                    "pieType": self.pie_type,
                    "tooltip": {"mode": self.tooltip_mode, "sort": self.tooltip_sort},
                    "legend": {
                        "displayMode": self.legend_display_mode,
                        "placement": self.legend_placement,
                        "values": self.legend_values,
                    },
                },
                "type": PIE_CHART_V2_TYPE,
            },
        )


class Dashboardlist(Panel):
    show_headings: bool = Field(True, alias="showHeadings")
    show_search: bool = Field(False, alias="showSearch")
    show_recent: bool = Field(False, alias="showRecent")
    show_starred: bool = Field(True, alias="showStarred")
    max_items: int = Field(10, alias="maxItems")
    search_query: str = Field("", alias="searchQuery")
    search_tags: list[str] = Field([], alias="searchTags")
    overrides: list[Any] = []

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "fieldConfig": {
                    "defaults": {"custom": {}},
                    "overrides": self.overrides,
                },
                "headings": self.show_headings,
                "search": self.show_search,
                "recent": self.show_recent,
                "starred": self.show_starred,
                "limit": self.max_items,
                "query": self.search_query,
                "tags": self.search_tags,
                "type": DASHBOARDLIST_TYPE,
            },
        )


class Logs(Panel):
    show_labels: bool = Field(False, alias="showLabels")
    show_common_labels: bool = Field(False, alias="showCommonLabels")
    show_time: bool = Field(False, alias="showTime")
    wrap_log_messages: bool = Field(False, alias="wrapLogMessages")
    sort_order: str = Field("Descending", alias="sortOrder")
    dedup_strategy: str = Field("none", alias="dedupStrategy")
    enable_log_details: bool = Field(False, alias="enableLogDetails")
    overrides: list[Any] = []
    prettify_log_message: bool = Field(False, alias="prettifyLogMessage")

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "fieldConfig": {
                    "defaults": {"custom": {}},
                    "overrides": self.overrides,
                },
                "options": {
                    "showLabels": self.show_labels,
                    "showCommonLabels": self.show_common_labels,
                    "showTime": self.show_time,
                    "wrapLogMessage": self.wrap_log_messages,
                    "sortOrder": self.sort_order,
                    "dedupStrategy": self.dedup_strategy,
                    "enableLogDetails": self.enable_log_details,
                    "prettifyLogMessage": self.prettify_log_message,
                },
                "type": LOGS_TYPE,
            },
        )


# ---------------------------------------------------------------------------
# Thresholds and SeriesOverride
# ---------------------------------------------------------------------------


class GraphThreshold(BaseModel):
    """Threshold for Graph panels."""

    value: float
    color_mode: str = Field("critical", alias="colorMode")
    fill: bool = True
    line: bool = True
    op: str = EVAL_GT
    yaxis: str = "left"
    fill_color: Any = Field(RED, alias="fillColor")
    line_color: Any = Field(RED, alias="lineColor")

    def to_json_data(self) -> dict:
        data = {
            "value": self.value,
            "colorMode": self.color_mode,
            "fill": self.fill,
            "line": self.line,
            "op": self.op,
            "yaxis": self.yaxis,
        }
        if self.color_mode == "custom":
            data["fillColor"] = self.fill_color
            data["lineColor"] = self.line_color
        return data


class SeriesOverride(BaseModel):
    """To override properties of panels."""

    alias: str
    bars: bool = False
    lines: bool = True
    yaxis: int = Field(1, ge=1, le=2, alias="yaxis")
    fill: int = Field(1, ge=0, le=10, alias="fill")
    zindex: int = Field(0, ge=-3, le=3, alias="zindex")
    dashes: bool = False
    dash_length: int | None = Field(default=None, alias="dashLength")
    space_length: int | None = Field(default=None, alias="spaceLength")
    color: Any | None = None
    fill_below_to: str | None = Field(default=None, alias="fillBelowTo")

    def to_json_data(self) -> dict:
        return {
            "alias": self.alias,
            "bars": self.bars,
            "lines": self.lines,
            "yaxis": self.yaxis,
            "fill": self.fill,
            "color": self.color,
            "fillBelowTo": self.fill_below_to,
            "zindex": self.zindex,
            "dashes": self.dashes,
            "dashLength": self.dash_length,
            "spaceLength": self.space_length,
        }


class Worldmap(Panel):
    circle_max_size: int = Field(30, alias="circleMaxSize")
    circle_min_size: int = Field(2, alias="circleMinSize")
    decimals: int = 0
    geo_point: str = Field("geohash", alias="geoPoint")
    location_data: Literal[
        "countries",
        "countries_3letter",
        "states",
        "probes",
        "geohash",
        "json_endpoint",
        "jsonp endpoint",
        "json result",
        "table",
    ] = Field("countries", alias="locationData")
    location_name: str = Field("", alias="locationName")
    hide_empty: bool = Field(False, alias="hideEmpty")
    hide_zero: bool = Field(False, alias="hideZero")
    initial_zoom: int = Field(1, alias="initialZoom")
    json_url: str = Field("", alias="jsonUrl")
    jsonp_callback: str = Field("", alias="jsonpCallback")
    map_center: Literal[
        "(0°, 0°)",
        "North America",
        "Europe",
        "West Asia",
        "SE Asia",
        "Last GeoHash",
        "custom",
    ] = Field("(0°, 0°)", alias="mapCenter")
    map_center_latitude: int = Field(0, alias="mapCenterLatitude")
    map_center_longitude: int = Field(0, alias="mapCenterLongitude")
    metric: str = "Value"
    mouse_wheel_zoom: bool = Field(False, alias="mouseWheelZoom")
    sticky_labels: bool = Field(False, alias="stickyLabels")
    thresholds: str = "0,100,150"
    threshold_colors: list[str] = Field(
        ["#73BF69", "#73BF69", "#FADE2A", "#C4162A"], alias="thresholdColors"
    )
    unit_plural: str = Field("", alias="unitPlural")
    unit_single: str = Field("", alias="unitSingle")
    unit_singular: str = Field("", alias="unitSingular")
    aggregation: str = "total"

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "circleMaxSize": self.circle_max_size,
                "circleMinSize": self.circle_min_size,
                "colors": self.threshold_colors,
                "decimals": self.decimals,
                "esGeoPoint": self.geo_point,
                "esMetric": self.metric,
                "locationData": self.location_data,
                "esLocationName": self.location_name,
                "hideEmpty": self.hide_empty,
                "hideZero": self.hide_zero,
                "initialZoom": self.initial_zoom,
                "jsonUrl": self.json_url,
                "jsonpCallback": self.jsonp_callback,
                "mapCenter": self.map_center,
                "mapCenterLatitude": self.map_center_latitude,
                "mapCenterLongitude": self.map_center_longitude,
                "mouseWheelZoom": self.mouse_wheel_zoom,
                "stickyLabels": self.sticky_labels,
                "thresholds": self.thresholds,
                "unitPlural": self.unit_plural,
                "unitSingle": self.unit_single,
                "unitSingular": self.unit_singular,
                "valueName": self.aggregation,
                "tableQueryOptions": {
                    "queryType": "geohash",
                    "geohashField": "geohash",
                    "latitudeField": "latitude",
                    "longitudeField": "longitude",
                    "metricField": "metric",
                },
                "type": WORLD_MAP_TYPE,
            },
        )


class StateTimeline(Panel):
    align_value: str = Field("left", alias="alignValue")
    color_mode: str = Field("thresholds", alias="colorMode")
    fill_opacity: int = Field(70, alias="fillOpacity")
    legend_display_mode: str = Field("list", alias="legendDisplayMode")
    legend_placement: str = Field("bottom", alias="legendPlacement")
    line_width: int = Field(0, alias="lineWidth")
    mappings: list[Any] = []
    overrides: list[Any] = []
    merge_values: bool = Field(True, alias="mergeValues")
    row_height: float = Field(0.9, alias="rowHeight")
    show_value: str = Field("auto", alias="showValue")
    tooltip_mode: str = Field("single", alias="tooltipMode")

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "fieldConfig": {
                    "defaults": {
                        "custom": {
                            "lineWidth": self.line_width,
                            "fillOpacity": self.fill_opacity,
                        },
                        "color": {"mode": self.color_mode},
                        "mappings": self.mappings,
                    },
                    "overrides": self.overrides,
                },
                "options": {
                    "mergeValues": self.merge_values,
                    "showValue": self.show_value,
                    "alignValue": self.align_value,
                    "rowHeight": self.row_height,
                    "legend": {
                        "displayMode": self.legend_display_mode,
                        "placement": self.legend_placement,
                    },
                    "tooltip": {"mode": self.tooltip_mode},
                },
                "type": STATE_TIMELINE_TYPE,
            },
        )


class Histogram(Panel):
    bucket_offset: int = Field(0, alias="bucketOffset")
    bucket_size: int = Field(0, alias="bucketSize")
    color_mode: str = Field("thresholds", alias="colorMode")
    combine: bool = False
    fill_opacity: int = Field(80, alias="fillOpacity")
    legend_display_mode: str = Field("list", alias="legendDisplayMode")
    legend_placement: str = Field("bottom", alias="legendPlacement")
    line_width: int = Field(0, alias="lineWidth")
    mappings: list[Any] = []
    overrides: list[Any] = []

    def to_json_data(self) -> dict:
        histogram = self.panel_json(
            {
                "fieldConfig": {
                    "defaults": {
                        "custom": {
                            "lineWidth": self.line_width,
                            "fillOpacity": self.fill_opacity,
                        },
                        "color": {"mode": self.color_mode},
                        "mappings": self.mappings,
                    },
                    "overrides": self.overrides,
                },
                "options": {
                    "legend": {
                        "displayMode": self.legend_display_mode,
                        "placement": self.legend_placement,
                    },
                    "bucketOffset": self.bucket_offset,
                    "combine": self.combine,
                },
                "type": HISTOGRAM_TYPE,
            },
        )
        if self.bucket_size > 0:
            histogram["options"]["bucketSize"] = self.bucket_size
        return histogram


class News(Panel):
    feed_url: str = Field("", alias="feedUrl")
    show_image: bool = Field(True, alias="showImage")
    use_proxy: bool = Field(False, alias="useProxy")

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "options": {
                    "feedUrl": self.feed_url,
                    "showImage": self.show_image,
                    "useProxy": self.use_proxy,
                },
                "type": NEWS_TYPE,
            },
        )


class Ae3ePlotly(Panel):
    configuration: dict[Any, Any] = {}
    data: list[Any] = []
    layout: dict[Any, Any] = {}
    script: str = """console.log(data)
           var trace = {
             x: data.series[0].fields[0].values.buffer,
             y: data.series[0].fields[1].values.buffer
           };
           return {data:[trace],layout:{title:'My Chart'}};"""
    click_script: str = Field("", alias="clickScript")

    def to_json_data(self) -> dict:
        plotly = self.panel_json(
            {
                "fieldConfig": {"defaults": {}, "overrides": []},
                "options": {
                    "configuration": {},
                    "data": self.data,
                    "layout": {},
                    "onclick": self.click_script,
                    "script": self.script,
                },
                "type": AE3E_PLOTLY_TYPE,
            },
        )
        _deep_update(plotly["options"]["layout"], self.layout)
        _deep_update(plotly["options"]["configuration"], self.configuration)
        return plotly


class BarChart(Panel):
    orientation: str = "auto"
    x_tick_label_rotation: int = Field(0, alias="xTickLabelRotation")
    x_tick_label_spacing: int = Field(0, alias="xTickLabelSpacing")
    show_value: str = Field("auto", alias="showValue")
    stacking: str = "none"
    group_width: float = Field(0.7, alias="groupWidth")
    bar_width: float = Field(0.97, alias="barWidth")
    bar_radius: float = Field(0.0, alias="barRadius")
    tooltip_mode: str = Field("single", alias="tooltipMode")
    tooltip_sort: str = Field("none", alias="tooltipSort")
    show_legend: bool = Field(True, alias="showLegend")
    legend_display_mode: str = Field("list", alias="legendDisplayMode")
    legend_placement: str = Field("bottom", alias="legendPlacement")
    legend_calcs: list[Any] = Field([], alias="legendCalcs")
    line_width: int = Field(1, alias="lineWidth")
    fill_opacity: int = Field(80, alias="fillOpacity")
    gradient_mode: str = Field("none", alias="gradientMode")
    axis_placement: str = Field("auto", alias="axisPlacement")
    axis_label: str = Field("", alias="axisLabel")
    axis_color_mode: str = Field("text", alias="axisColorMode")
    scale_distribution_type: str = Field("linear", alias="scaleDistributionType")
    axis_centered_zero: bool = Field(False, alias="axisCenteredZero")
    hide_from_tooltip: bool = Field(False, alias="hideFromTooltip")
    hide_from_viz: bool = Field(False, alias="hideFromViz")
    hide_from_legend: bool = Field(False, alias="hideFromLegend")
    color_mode: str = Field("palette-classic", alias="colorMode")
    fixed_color: str = Field("blue", alias="fixedColor")
    mappings: list[Any] = []
    thresholds_mode: str = Field("absolute", alias="thresholdsMode")
    threshold_steps: list[Any] = Field(
        [{"value": None, "color": "green"}, {"value": 80, "color": "red"}],
        alias="thresholdSteps",
    )
    overrides: list[Any] = []

    def to_json_data(self) -> dict:
        return self.panel_json(
            {
                "options": {
                    "orientation": self.orientation,
                    "xTickLabelRotation": self.x_tick_label_rotation,
                    "xTickLabelSpacing": self.x_tick_label_spacing,
                    "showValue": self.show_value,
                    "stacking": self.stacking,
                    "groupWidth": self.group_width,
                    "barWidth": self.bar_width,
                    "barRadius": self.bar_radius,
                    "tooltip": {"mode": self.tooltip_mode, "sort": self.tooltip_sort},
                    "legend": {
                        "show": self.show_legend,
                        "displayMode": self.legend_display_mode,
                        "placement": self.legend_placement,
                        "calcs": self.legend_calcs,
                    },
                },
                "fieldConfig": {
                    "defaults": {
                        "custom": {
                            "lineWidth": self.line_width,
                            "fillOpacity": self.fill_opacity,
                            "gradientMode": self.gradient_mode,
                            "axisPlacement": self.axis_placement,
                            "axisLabel": self.axis_label,
                            "axisColorMode": self.axis_color_mode,
                            "scaleDistribution": {"type": self.scale_distribution_type},
                            "axisCenteredZero": self.axis_centered_zero,
                            "hideFrom": {
                                "tooltip": self.hide_from_tooltip,
                                "viz": self.hide_from_viz,
                                "legend": self.hide_from_legend,
                            },
                        },
                        "color": {
                            "mode": self.color_mode,
                            "fixedColor": self.fixed_color
                            if self.color_mode == "fixed"
                            else "none",
                        },
                        "mappings": self.mappings,
                        "thresholds": {
                            "mode": self.thresholds_mode,
                            "steps": self.threshold_steps,
                        },
                    },
                    "overrides": self.overrides,
                },
                "type": BAR_CHART_TYPE,
            },
        )
