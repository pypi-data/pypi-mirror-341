# str_or_none/__init__.py
import datetime
import json
import sys
import types
import typing
from numbers import Number


def str_or_none(
    value: typing.Any,
    *,
    strip: bool = True,
    strict: bool = True,
    empty_str_to_none: bool = True,
) -> typing.Optional[str]:
    if value is None:
        return None

    # Handle file-like objects (TextIO, StringIO, etc.)
    if hasattr(value, "read") and callable(value.read):
        _text = value.read()
        _text = _text.strip() if strip else _text
        return None if not _text and empty_str_to_none else _text

    elif isinstance(value, typing.Text):
        _text = value
        _text = _text.strip() if strip else _text
        return None if not _text and empty_str_to_none else _text

    elif isinstance(value, (int, float, bool, Number)):
        if strict:
            raise ValueError(
                f"Number cannot be converted to str in strict mode: {value}"
            )
        return str(value)

    elif isinstance(value, datetime.datetime):
        if strict:
            raise ValueError(
                f"Datetime cannot be converted to str in strict mode: {value}"
            )
        return value.isoformat()

    # Dict check before sequence/iterable
    elif isinstance(value, dict):
        if strict:
            raise ValueError(f"Dict cannot be converted to str in strict mode: {value}")
        return json.dumps(value, default=str)

    elif isinstance(value, (list, tuple, set, typing.Sequence, typing.Iterable)):
        if strict:
            raise ValueError(
                f"Sequence cannot be converted to str in strict mode: {value}"
            )
        return json.dumps(list(value), default=str)

    # __str__ or __repr__
    elif hasattr(value, "__str__") or hasattr(value, "__repr__"):
        if strict:
            raise ValueError(
                "Object with __str__ or __repr__ cannot be converted to str "
                + f"in strict mode: {value}"
            )
        _text = str(value).strip() if strip else str(value)
        return None if not _text and empty_str_to_none else _text

    else:
        raise ValueError(f"Cannot convert to str: {value}")


class CallableModule(types.ModuleType):
    def __call__(
        self,
        value: typing.Any,
        *,
        strip: bool = True,
        strict: bool = True,
        empty_str_to_none: bool = True,
    ) -> typing.Optional[str]:
        return str_or_none(
            value, strip=strip, strict=strict, empty_str_to_none=empty_str_to_none
        )


current_module = sys.modules[__name__]
current_module.__class__ = CallableModule


__all__ = ["str_or_none"]
__version__ = "0.1.0"
