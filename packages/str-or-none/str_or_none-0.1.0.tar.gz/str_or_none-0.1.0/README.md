# str-or-none

A tiny Python utility to safely convert a value to a `str` or `None`.

- Returns a stripped string if possible, or `None` if the value is `None`.
- Raises `ValueError` for non-string types in strict mode (default).
- Supports file-like objects, numbers, datetimes, sequences, dicts, and custom objects.
- Can be used as a function or directly as a module call.

## Usage

```python
import str_or_none
# or: from str_or_none import str_or_none

str_or_none("  hello  ")           # 'hello'
str_or_none(None)                   # None
str_or_none(123)                    # ValueError (strict mode)
str_or_none(123, strict=False)      # '123'
str_or_none([1, 2, 3], strict=False) # '[1, 2, 3]'
str_or_none({"a": 1}, strict=False) # '{"a": 1}'

import io
str_or_none(io.StringIO("  hi  ")) # 'hi'
str_or_none("  hi  ", strip=False)  # '  hi  '

class Custom:
    def __str__(self):
        return "custom!"

str_or_none(Custom(), strict=False)  # 'custom!'
str_or_none("")  # None (default: empty_str_to_none=True)
str_or_none("", empty_str_to_none=False)  # ''
str_or_none("   ")  # None (after strip)
str_or_none("   ", empty_str_to_none=False)  # ''
```

## API

```python
def str_or_none(value, *, strip=True, strict=True, empty_str_to_none=True) -> Optional[str]:
    ...
```

- `strip`: Remove leading/trailing whitespace (default: True)
- `strict`: Raise `ValueError` for non-string types (default: True)
- `empty_str_to_none`: If True, return None for empty strings (after optional strip). Default: True.

Returns a string or `None`, or raises `ValueError` if conversion is not allowed.
