# 🎭 Masks fp

### Functional wrapping for Python.
Advanced ⬦ Powerful ⬦ Tooling

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/A-4S/masks-fp/python-app.yml?logo=github&label=CI&style=for-the-badge)](https://github.com/A-4S/masks-fp/actions/workflows/python-app.yml) [![PyPI - Version](https://img.shields.io/pypi/v/masks-fp?style=for-the-badge)](https://pypi.org/project/masks-fp/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/masks-fp?style=for-the-badge)](https://pypi.org/project/masks-fp/)

---
## Background
Wrapping is a technique targeting function extensibility, taking metadata of one function and merging it with another, including any intended additional functionality, forming a new function.

## Usage
Mask fp is a powerful tool made for wrapping functions and is built on top of the `functools.wraps` function. The `masks` function allows for quick creation of *wrapper* function look-alikes by placing the `masks` *decorator* over target *wrapper* functions and calling it along with the desired target *wrapped* function. Furthermore, the `masks` function will preserve type hinting, signatures, annotations, and the application of default arg and kwarg values, for an enhanced developer experience and potentially advanced use cases.

## Features
- Automatic application of default arguments during calls, just as it would originally.
- Fully applied `__signature__` and `__annotations__` for wrappers; parameters of `wrapped` and return annotation of `wrapper`.
- Type hinting for newly created wrapper functions! ✨

## Install
Using pip
```sh
pip install masks-fp
```

Or using Poetry
```sh
poetry add masks-fp
```

## Example
```python
from collections.abc import Callable, Iterable

from mask_fp import masks


def decorator(f: Callable[..., Iterable[int]]) -> Callable:
    @masks(f)
    def wrapper(*args, **kwargs) -> dict[str, int | Iterable[int]]:
        """
        From ``wrapper`` ``docstring``. 👋
        """
        print(f"Sum of {f(*args, **kwargs)} is {sum(f(*args, **kwargs))}. 🎓")

        return f(*args, **kwargs)

    return wrapper


@decorator
def wrapped(a: int, /, b: int = 2, *, c: int = 3) -> tuple[int, int, int]:
    """
    From ``wrapped`` ``docstring``. 👋
    """
    return (a, b, c)
```

**Without using default values**
```python
>>> print(wrapped(1, 2, c=3))
Sum of (1, 2, 3) is 6. 🎓
(1, 2, 3)
```

**Using default values**
```python
>>> print(wrapped(1))
Sum of (1, 2, 3) is 6. 🎓
(1, 2, 3)
```
