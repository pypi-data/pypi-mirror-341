# -*- coding: utf-8 -*-
# cython: language_level = 3


"""
.. versionadded:: 0.2.0
"""

from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import MutableMapping
from dataclasses import dataclass
from dataclasses import field
from types import NotImplementedType
from typing import Any
from typing import Optional
from typing import Self
from typing import cast
from typing import override

import wrapt  # type: ignore[import-untyped]

from .mapping import MappingConfigData
from ..abc import PathLike
from ..utils import Unset


@dataclass
class Difference:
    """
    与初始化数据的差异
    """

    updated: set[str] = field(default_factory=set)
    """
    修改/新增的键

    .. note::
       为了 `性能/内存` 所以实现的不是很完美，如果一个键更改为了另一个值再改回来仍然会被认为是被修改过的键
    """
    removed: set[str] = field(default_factory=set)
    """
    删除的键
    """

    def clear(self) -> None:
        """
        清空差异
        """
        self.updated.clear()
        self.removed.clear()

    def __iadd__(self, other: Any) -> Self | NotImplementedType:
        if not isinstance(other, Iterable):
            return NotImplemented
        other = set(other)
        self.updated |= other
        self.removed -= other
        return self

    def __isub__(self, other: Any) -> Self | NotImplementedType:
        if not isinstance(other, Iterable):
            return NotImplemented
        other = set(other)
        self.updated -= other
        self.removed |= other
        return self

    def __bool__(self) -> bool:
        return bool(self.updated and self.removed)


def diff_keys[F: Callable[..., Any]](func: F) -> F:
    @wrapt.decorator  # type: ignore[misc]
    def wrapper(
            wrapped: F,
            instance: Any,
            args: tuple[Any, ...],
            kwargs: dict[str, Any]
    ) -> Any:
        if not isinstance(instance, EnvironmentConfigData):
            raise TypeError(  # pragma: no cover
                f"instance must be {EnvironmentConfigData.__name__} but got {type(instance).__name__}"
            )

        before = set(instance.keys())
        before_never_changed = before - instance.difference.updated - instance.difference.removed
        may_change = {k: instance[k] for k in before_never_changed}

        result = wrapped(*args, **kwargs)
        after = set(instance.keys())

        added = after - before
        deleted = before - after

        instance.difference += added
        instance.difference -= deleted

        current_never_changed = before_never_changed - added - deleted
        for may_changed in current_never_changed:
            if may_change[may_changed] != instance[may_changed]:
                instance.difference += {may_changed}

        return result

    return cast(F, wrapper(func))


class EnvironmentConfigData(MappingConfigData[MutableMapping[str, str]]):
    """
    环境变量配置数据

    内部维护了与初始化参数的键差异

    .. note::
       :py:class:`~Config.processor.OSEnv.OSEnvSL` 在保存时会重置差异数据
    """

    def __init__(self, data: Optional[MutableMapping[str, str]] = None):
        super().__init__(data)
        self.difference = Difference()

    @diff_keys
    @override
    def modify(self, path: PathLike, value: str, *, allow_create: bool = True) -> Self:
        return super().modify(path, value, allow_create=allow_create)

    @diff_keys
    @override
    def delete(self, path: PathLike) -> Self:
        return super().delete(path)

    @diff_keys
    @override
    def unset(self, path: PathLike) -> Self:
        return super().unset(path)

    @diff_keys
    @override
    def setdefault(self, path: PathLike, default: Optional[Any] = None, *, return_raw_value: bool = False) -> Any:
        return super().setdefault(path, default, return_raw_value=return_raw_value)

    @diff_keys
    @override
    def clear(self) -> None:
        super().clear()

    @diff_keys
    @override
    def pop(self, path: PathLike, /, default: Any = Unset) -> Any:
        return super().pop(path, default)

    @diff_keys
    @override
    def popitem(self) -> Any:
        return super().popitem()

    @diff_keys
    @override
    def update(self, m: Optional[Any] = None, /, **kwargs: str) -> None:
        super().update(m, **kwargs)

    @diff_keys
    @override
    def __setitem__(self, index: str, value: str) -> None:
        super().__setitem__(index, value)

    @diff_keys
    @override
    def __delitem__(self, index: str) -> None:
        super().__delitem__(index)

    @diff_keys
    def __ior__(self, other: MutableMapping[str, str]) -> Self:
        return super().__ior__(other)  # type: ignore[misc, no-any-return]


__all__ = (
    "Difference",
    "EnvironmentConfigData",
)
