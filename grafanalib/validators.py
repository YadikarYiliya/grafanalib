import re
from typing import Any, List

class IsInValidator:
    def __init__(self, choices: List[Any]):
        self.choices = choices

    def __call__(self, value: Any) -> Any:
        if value not in self.choices:
            raise ValueError(f"{value!r} should be one of {self.choices}")
        return value

    def __repr__(self) -> str:
        return f"<IsInValidator choices={self.choices}>"

def is_in(choices: List[Any]):
    """
    A validator that raises a ValueError if the attribute value is not in a provided list.
    
    :param choices: List of valid choices
    """
    return IsInValidator(choices)

def is_interval(value: str) -> str:
    """
    A validator that raises a ValueError if the string does not match the interval regex.
    
    Valid interval should match the expression: ^[+-]?\d*[smhdMY]$
    Examples: "24h", "7d", "1M", "+24h", "-24h"
    """
    if not re.match(r"^[+-]?\d*[smhdMY]$", value):
        raise ValueError(
            "Valid interval should be a string matching the expression: ^[+-]?\\d*[smhdMY]$. "
            "Examples: 24h, 7d, 1M, +24h, -24h")
    return value

def is_color_code(value: str) -> str:
    """
    A validator that raises a ValueError if the string is not a valid color code.
    
    A valid color code starts with '#' followed by 6 hexadecimal digits (e.g. "#37872D").
    """
    err = "Value should be a valid color code (e.g. #37872D)"
    if not value.startswith("#"):
        raise ValueError(err)
    if len(value) != 7:
        raise ValueError(err)
    try:
        int(value[1:], 16)
    except ValueError:
        raise ValueError(err)
    return value

class ListOfValidator:
    def __init__(self, etype: type):
        self.etype = etype

    def __call__(self, value: List[Any]) -> List[Any]:
        if not all(isinstance(el, self.etype) for el in value):
            raise ValueError(f"Value should be a list of {self.etype}")
        return value

    def __repr__(self) -> str:
        return f"<ListOfValidator etype={self.etype}>"

def is_list_of(etype: type):
    """
    A validator that raises a ValueError if the value is not a list of the specified type.
    
    :param etype: The expected type for each element in the list.
    """
    return ListOfValidator(etype)