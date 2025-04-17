from collections.abc import Callable
from functools import reduce
from inspect import Signature

from pipe_fp import pipe


def set_return_annotations(f: Callable, s: Signature) -> None:
    def build_annotations(s: Signature):
        return {**f.__annotations__, "return": s.return_annotation}

    def pair_annotations(d: dict):
        return {"__signature__": s, "__annotations__": d}

    def set_annotations(d: dict):
        return reduce(lambda _, c: setattr(f, c[0], c[1]), d.items(), ...)

    return pipe(build_annotations, pair_annotations, set_annotations)(s)
