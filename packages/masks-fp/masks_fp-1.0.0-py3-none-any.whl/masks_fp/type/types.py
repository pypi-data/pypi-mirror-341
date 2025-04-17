from collections.abc import Callable
from typing import Any, ParamSpec, TypeAlias, TypeVar


T = TypeVar("T")

P = ParamSpec("P")

Wrapped: TypeAlias = Callable[P, Any]

Wrapper: TypeAlias = Callable[..., T]

Masked: TypeAlias = Callable[P, T]
