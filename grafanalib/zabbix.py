import itertools
from numbers import Number
from typing import Any, Optional
from pydantic import BaseModel, Field, validator
from grafanalib.validators import is_interval, is_in, is_color_code, is_list_of
from grafanalib.core import RGBA, Percent, Pixels, DashboardLink, DEFAULT_ROW_HEIGHT, BLANK, GREEN

ZABBIX_TRIGGERS_TYPE = 'alexanderzobnin-zabbix-triggers-panel'

ZABBIX_QMODE_METRICS = 0
ZABBIX_QMODE_SERVICES = 1
ZABBIX_QMODE_TEXT = 2

ZABBIX_SLA_PROP_STATUS = {
    'name': 'Status',
    'property': 'status'
}

ZABBIX_SLA_PROP_SLA = {
    'name': 'SLA',
    'property': 'sla'
}

ZABBIX_SLA_PROP_OKTIME = {
    'name': 'OK time',
    'property': 'okTime'
}

ZABBIX_SLA_PROP_PROBTIME = {
    'name': 'Problem time',
    'property': 'problemTime'
}

ZABBIX_SLA_PROP_DOWNTIME = {
    'name': 'Down time',
    'property': 'downtimeTime',
}

ZABBIX_EVENT_PROBLEMS = {
    'text': 'Problems',
    'value': [1]
}

ZABBIX_EVENT_OK = {
    'text': 'OK',
    'value': [0]
}

ZABBIX_EVENT_ALL = {
    'text': 'All',
    'value': [0, 1]
}

ZABBIX_TRIGGERS_SHOW_ALL = 'all triggers'
ZABBIX_TRIGGERS_SHOW_ACK = 'acknowledged'
ZABBIX_TRIGGERS_SHOW_NACK = 'unacknowledged'

ZABBIX_SORT_TRIGGERS_BY_CHANGE = {
    'text': 'last change',
    'value': 'lastchange',
}
ZABBIX_SORT_TRIGGERS_BY_SEVERITY = {
    'text': 'severity',
    'value': 'priority',
}

ZABBIX_SEVERITY_COLORS = (
    ('#B7DBAB', 'Not classified'),
    ('#82B5D8', 'Information'),
    ('#E5AC0E', 'Warning'),
    ('#C15C17', 'Average'),
    ('#BF1B00', 'High'),
    ('#890F02', 'Disaster'),
)

def convertZabbixSeverityColors(colors):
    priorities = itertools.count(0)
    return [ZabbixColor(color=c, priority=next(priorities), severity=s) for c, s in colors]

class ZabbixTargetOptions(BaseModel):
    showDisabledItems: bool = False

    def to_json_data(self) -> dict:
        return {'showDisabledItems': self.showDisabledItems}

class ZabbixTargetField(BaseModel):
    filter: str = ""

    def to_json_data(self) -> dict:
        return {'filter': self.filter}

class ZabbixTarget(BaseModel):
    application: str = ""
    expr: str = ""
    functions: list = []
    group: str = ""
    host: str = ""
    intervalFactor: int = 2
    item: str = ""
    itService: str = ""
    mode: int = ZABBIX_QMODE_METRICS
    options: ZabbixTargetOptions = Field(default_factory=ZabbixTargetOptions)
    refId: str = ""
    slaProperty: dict = {}
    textFilter: str = ""
    useCaptureGroups: bool = False

    def to_json_data(self) -> dict:
        obj = {
            'application': ZabbixTargetField(filter=self.application).to_json_data(),
            'expr': self.expr,
            'functions': self.functions,
            'group': ZabbixTargetField(filter=self.group).to_json_data(),
            'host': ZabbixTargetField(filter=self.host).to_json_data(),
            'intervalFactor': self.intervalFactor,
            'item': ZabbixTargetField(filter=self.item).to_json_data(),
            'mode': self.mode,
            'options': self.options.to_json_data(),
            'refId': self.refId,
        }
        if self.mode == ZABBIX_QMODE_SERVICES:
            obj['slaProperty'] = self.slaProperty
            obj['itservice'] = {'name': self.itService}
        if self.mode == ZABBIX_QMODE_TEXT:
            obj['textFilter'] = self.textFilter
            obj['useCaptureGroups'] = self.useCaptureGroups
        return obj

class ZabbixDeltaFunction(BaseModel):
    added: bool = False

    def to_json_data(self) -> dict:
        text = "delta()"
        definition = {
            'category': 'Transform',
            'name': 'delta',
            'defaultParams': [],
            'params': []
        }
        return {'added': self.added, 'text': text, 'def': definition, 'params': []}

class ZabbixGroupByFunction(BaseModel):
    _options: list = ['avg', 'min', 'max', 'median']
    _default_interval: str = '1m'
    _default_function: str = 'avg'
    added: bool = False
    interval: str = Field(default='1m')
    function: str = Field(default='avg')

    @validator('interval')
    def validate_interval(cls, v):
        return is_interval(v)
    
    @validator('function')
    def validate_function(cls, v):
        return is_in(['avg', 'min', 'max', 'median'])(v)
    
    def to_json_data(self) -> dict:
        text = "groupBy({interval}, {function})"
        definition = {
            'category': 'Transform',
            'name': 'groupBy',
            'defaultParams': [self._default_interval, self._default_function],
            'params': [
                {'name': 'interval', 'type': 'string'},
                {'name': 'function', 'options': self._options, 'type': 'string'}
            ]
        }
        return {
            'def': definition,
            'text': text.format(interval=self.interval, function=self.function),
            'params': [self.interval, self.function],
            'added': self.added,
        }

class ZabbixScaleFunction(BaseModel):
    _default_factor: Number = 100
    added: bool = False
    factor: Number = 100

    def to_json_data(self) -> dict:
        text = "scale({factor})"
        definition = {
            'category': 'Transform',
            'name': 'scale',
            'defaultParams': [self._default_factor],
            'params': [{'name': 'factor', 'options': [100, 0.01, 10, -1], 'type': 'float'}]
        }
        return {
            'def': definition,
            'text': text.format(factor=self.factor),
            'params': [self.factor],
            'added': self.added,
        }

class ZabbixAggregateByFunction(BaseModel):
    _options: list = ['avg', 'min', 'max', 'median']
    _default_interval: str = '1m'
    _default_function: str = 'avg'
    added: bool = False
    interval: str = Field(default='1m')
    function: str = Field(default='avg')

    @validator('interval')
    def validate_interval(cls, v):
        return is_interval(v)
    
    @validator('function')
    def validate_function(cls, v):
        return is_in(['avg', 'min', 'max', 'median'])(v)
    
    def to_json_data(self) -> dict:
        text = "aggregateBy({interval}, {function})"
        definition = {
            'category': 'Aggregate',
            'name': 'aggregateBy',
            'defaultParams': [self._default_interval, self._default_function],
            'params': [
                {'name': 'interval', 'type': 'string'},
                {'name': 'function', 'options': self._options, 'type': 'string'}
            ]
        }
        return {
            'def': definition,
            'text': text.format(interval=self.interval, function=self.function),
            'params': [self.interval, self.function],
            'added': self.added,
        }

class ZabbixAverageFunction(BaseModel):
    _default_interval: str = '1m'
    added: bool = False
    interval: str = Field(default='1m')

    @validator('interval')
    def validate_interval(cls, v):
        return is_interval(v)
    
    def to_json_data(self) -> dict:
        text = "average({interval})"
        definition = {
            'category': "Aggregate",
            "name": "average",
            "defaultParams": [self._default_interval],
            'params': [{'name': 'interval', 'type': 'string'}]
        }
        return {'def': definition, 'text': text.format(interval=self.interval), 'params': [self.interval], 'added': self.added}

class ZabbixMaxFunction(BaseModel):
    _default_interval: str = '1m'
    added: bool = False
    interval: str = Field(default='1m')

    @validator('interval')
    def validate_interval(cls, v):
        return is_interval(v)
    
    def to_json_data(self) -> dict:
        text = "max({interval})"
        definition = {
            'category': 'Aggregate',
            'name': 'max',
            'defaultParams': [self._default_interval],
            'params': [{'name': 'interval', 'type': 'string'}]
        }
        return {'def': definition, 'text': text.format(interval=self.interval), 'params': [self.interval], 'added': self.added}

class ZabbixMedianFunction(BaseModel):
    _default_interval: str = '1m'
    added: bool = False
    interval: str = Field(default='1m')

    @validator('interval')
    def validate_interval(cls, v):
        return is_interval(v)
    
    def to_json_data(self) -> dict:
        text = "median({interval})"
        definition = {
            'category': 'Aggregate',
            'name': 'median',
            'defaultParams': [self._default_interval],
            'params': [{'name': 'interval', 'type': 'string'}]
        }
        return {'def': definition, 'text': text.format(interval=self.interval), 'params': [self.interval], 'added': self.added}

class ZabbixMinFunction(BaseModel):
    _default_interval: str = '1m'
    added: bool = False
    interval: str = Field(default='1m')

    @validator('interval')
    def validate_interval(cls, v):
        return is_interval(v)
    
    def to_json_data(self) -> dict:
        text = "min({interval})"
        definition = {
            'category': 'Aggregate',
            'name': 'min',
            'defaultParams': [self._default_interval],
            'params': [{'name': 'interval', 'type': 'string'}]
        }
        return {'def': definition, 'text': text.format(interval=self.interval), 'params': [self.interval], 'added': self.added}

class ZabbixSumSeriesFunction(BaseModel):
    added: bool = False

    def to_json_data(self) -> dict:
        text = "sumSeries()"
        definition = {
            'category': 'Aggregate',
            'name': 'sumSeries',
            'defaultParams': [],
            'params': []
        }
        return {'added': self.added, 'text': text, 'def': definition, 'params': []}

class ZabbixBottomFunction(BaseModel):
    _options: list = ['avg', 'min', 'max', 'median']
    _default_number: int = 5
    _default_function: str = 'avg'
    added: bool = False
    number: int = 5
    function: str = Field(default='avg')

    @validator('function')
    def validate_function(cls, v):
        return is_in(['avg', 'min', 'max', 'median'])(v)
    
    def to_json_data(self) -> dict:
        text = "bottom({number}, {function})"
        definition = {
            'category': 'Filter',
            'name': 'bottom',
            'defaultParams': [self._default_number, self._default_function],
            'params': [
                {'name': 'number', 'type': 'string'},
                {'name': 'function', 'options': self._options, 'type': 'string'}
            ]
        }
        return {'def': definition, 'text': text.format(number=self.number, function=self.function), 'params': [self.number, self.function], 'added': self.added}

class ZabbixTopFunction(BaseModel):
    _options: list = ['avg', 'min', 'max', 'median']
    _default_number: int = 5
    _default_function: str = 'avg'
    added: bool = False
    number: int = 5
    function: str = Field(default='avg')

    @validator('function')
    def validate_function(cls, v):
        return is_in(['avg', 'min', 'max', 'median'])(v)
    
    def to_json_data(self) -> dict:
        text = "top({number}, {function})"
        definition = {
            'category': 'Filter',
            'name': 'top',
            'defaultParams': [self._default_number, self._default_function],
            'params': [
                {'name': 'number', 'type': 'string'},
                {'name': 'function', 'options': self._options, 'type': 'string'}
            ]
        }
        return {'def': definition, 'text': text.format(number=self.number, function=self.function), 'params': [self.number, self.function], 'added': self.added}

class ZabbixTrendValueFunction(BaseModel):
    _options: list = ['avg', 'min', 'max']
    _default_type: str = 'avg'
    added: bool = False
    type: str = Field(default='avg')

    @validator('type')
    def validate_type(cls, v):
        return is_in(['avg', 'min', 'max'])(v)
    
    def to_json_data(self) -> dict:
        text = "trendValue({type})"
        definition = {
            'category': 'Trends',
            'name': 'trendValue',
            'defaultParams': [self._default_type],
            'params': [{'name': 'type', 'options': self._options, 'type': 'string'}]
        }
        return {'def': definition, 'text': text.format(type=self.type), 'params': [self.type], 'added': self.added}

class ZabbixTimeShiftFunction(BaseModel):
    _options: list = ['24h', '7d', '1M', '+24h', '-24h']
    _default_interval: str = '24h'
    added: bool = False
    interval: str = Field(default='24h')

    @validator('interval')
    def validate_interval(cls, v):
        return is_in(['24h', '7d', '1M', '+24h', '-24h'])(v)
    
    def to_json_data(self) -> dict:
        text = "timeShift({interval})"
        definition = {
            'category': 'Time',
            'name': 'timeShift',
            'defaultParams': [self._default_interval],
            'params': [{'name': 'interval', 'options': self._options, 'type': 'string'}]
        }
        return {'def': definition, 'text': text.format(interval=self.interval), 'params': [self.interval], 'added': self.added}

class ZabbixSetAliasFunction(BaseModel):
    alias: str
    added: bool = False

    def to_json_data(self) -> dict:
        text = "setAlias({alias})"
        definition = {
            'category': 'Alias',
            'name': 'setAlias',
            'defaultParams': [],
            'params': [{'name': 'alias', 'type': 'string'}]
        }
        return {'def': definition, 'text': text.format(alias=self.alias), 'params': [self.alias], 'added': self.added}

class ZabbixSetAliasByRegexFunction(BaseModel):
    regexp: str
    added: bool = False

    def to_json_data(self) -> dict:
        text = "setAliasByRegex({regexp})"
        definition = {
            'category': 'Alias',
            'name': 'setAliasByRegex',
            'defaultParams': [],
            'params': [{'name': 'aliasByRegex', 'type': 'string'}]
        }
        return {'def': definition, 'text': text.format(regexp=self.regexp), 'params': [self.regexp], 'added': self.added}

def zabbixMetricTarget(application: str, group: str, host: str, item: str, functions: list = None) -> ZabbixTarget:
    if functions is None:
        functions = []
    return ZabbixTarget(
        mode=ZABBIX_QMODE_METRICS,
        application=application,
        group=group,
        host=host,
        item=item,
        functions=functions,
    )

def zabbixServiceTarget(service: str, sla: dict = ZABBIX_SLA_PROP_STATUS) -> ZabbixTarget:
    return ZabbixTarget(
        mode=ZABBIX_QMODE_SERVICES,
        itService=service,
        slaProperty=sla,
    )

def zabbixTextTarget(application: str, group: str, host: str, item: str, text: str, useCaptureGroups: bool = False) -> ZabbixTarget:
    return ZabbixTarget(
        mode=ZABBIX_QMODE_TEXT,
        application=application,
        group=group,
        host=host,
        item=item,
        textFilter=text,
        useCaptureGroups=useCaptureGroups,
    )

class ZabbixColor(BaseModel):
    color: str
    priority: int
    severity: str
    show: bool = True

    @validator('color')
    def check_color(cls, v):
        return is_color_code(v)
    
    def to_json_data(self) -> dict:
        return {
            'color': self.color,
            'priority': self.priority,
            'severity': self.severity,
            'show': self.show,
        }

class ZabbixTrigger(BaseModel):
    application: str = ""
    group: str = ""
    host: str = ""
    trigger: str = ""

    def to_json_data(self) -> dict:
        return {
            'application': ZabbixTargetField(filter=self.application).to_json_data(),
            'group': ZabbixTargetField(filter=self.group).to_json_data(),
            'host': ZabbixTargetField(filter=self.host).to_json_data(),
            'trigger': ZabbixTargetField(filter=self.trigger).to_json_data(),
        }

class ZabbixTriggersPanel(BaseModel):
    dataSource: Any
    title: Any
    ackEventColor: RGBA = Field(default_factory=lambda: BLANK)
    ageField: bool = True
    customLastChangeFormat: bool = False
    description: str = ""
    fontSize: Percent = Field(default_factory=Percent)
    height: Pixels = Field(default_factory=lambda: DEFAULT_ROW_HEIGHT)
    hideHostsInMaintenance: bool = False
    hostField: bool = True
    hostTechNameField: bool = False
    id: Optional[Any] = None
    infoField: bool = True
    lastChangeField: bool = True
    lastChangeFormat: str = ""
    limit: int = 10
    links: list[DashboardLink] = Field(default_factory=list)
    markAckEvents: bool = False
    minSpan: Optional[Any] = None
    okEventColor: RGBA = Field(default_factory=lambda: GREEN)
    pageSize: int = 10
    repeat: Optional[Any] = None
    scroll: bool = True
    severityField: bool = False
    showEvents: Any = Field(default_factory=lambda: ZABBIX_EVENT_PROBLEMS)
    showTriggers: str = ZABBIX_TRIGGERS_SHOW_ALL
    sortTriggersBy: dict = Field(default_factory=lambda: ZABBIX_SORT_TRIGGERS_BY_CHANGE)
    span: Optional[Any] = None
    statusField: bool = False
    transparent: bool = False
    triggers: ZabbixTrigger = Field(default_factory=ZabbixTrigger)
    triggerSeverity: list[ZabbixColor] = Field(default_factory=lambda: convertZabbixSeverityColors(ZABBIX_SEVERITY_COLORS))

    def to_json_data(self) -> dict:
        return {
            'type': ZABBIX_TRIGGERS_TYPE,
            'datasource': self.dataSource,
            'title': self.title,
            'ackEventColor': self.ackEventColor.to_json_data() if hasattr(self.ackEventColor, "to_json_data") else self.ackEventColor,
            'ageField': self.ageField,
            'customLastChangeFormat': self.customLastChangeFormat,
            'description': self.description,
            'fontSize': self.fontSize.to_json_data() if hasattr(self.fontSize, "to_json_data") else self.fontSize,
            'height': self.height.to_json_data() if hasattr(self.height, "to_json_data") else self.height,
            'hideHostsInMaintenance': self.hideHostsInMaintenance,
            'hostField': self.hostField,
            'hostTechNameField': self.hostTechNameField,
            'id': self.id,
            'infoField': self.infoField,
            'lastChangeField': self.lastChangeField,
            'lastChangeFormat': self.lastChangeFormat,
            'limit': self.limit,
            'links': [link.to_json_data() for link in self.links],
            'markAckEvents': self.markAckEvents,
            'minSpan': self.minSpan,
            'okEventColor': self.okEventColor.to_json_data() if hasattr(self.okEventColor, "to_json_data") else self.okEventColor,
            'pageSize': self.pageSize,
            'repeat': self.repeat,
            'scroll': self.scroll,
            'severityField': self.severityField,
            'showEvents': self.showEvents,
            'showTriggers': self.showTriggers,
            'sortTriggersBy': self.sortTriggersBy,
            'span': self.span,
            'statusField': self.statusField,
            'transparent': self.transparent,
            'triggers': self.triggers.to_json_data() if hasattr(self.triggers, "to_json_data") else self.triggers,
            'triggerSeverity': [color.to_json_data() for color in self.triggerSeverity],
        }