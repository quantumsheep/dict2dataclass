from __future__ import annotations

import dataclasses
import sys
from typing import Any, Mapping


@dataclasses.dataclass
class DictOptions:
    keys: list[str]


class DictField(dataclasses.Field):
    __slots__ = ("from_dict_options",)

    # In Python 3.10, dataclasses adds a new parameter to the :class:`Field`
    # constructor: `kw_only`
    #
    # Ref: https://docs.python.org/3.10/library/dataclasses.html#dataclasses.dataclass
    if sys.version_info[:2] >= (3, 10):  # pragma: no cover

        def __init__(
            self,
            keys: list[str],
            default: Any,
            default_factory: Any,
            init: bool,
            repr: bool,
            hash: bool | None,
            compare: bool,
            metadata: Mapping[Any, Any],
        ):
            super().__init__(
                default,
                default_factory,
                init,
                repr,
                hash,
                compare,
                metadata,
                False,
            )

            if isinstance(keys, str):
                keys = (keys,)

            self.from_dict_options = DictOptions(keys=keys)

    else:  # pragma: no cover

        def __init__(
            self,
            keys: list[str],
            default: Any,
            default_factory: Any,
            init: bool,
            repr: bool,
            hash: bool | None,
            compare: bool,
            metadata: Mapping[Any, Any],
        ):
            super().__init__(
                default,
                default_factory,
                init,
                repr,
                hash,
                compare,
                metadata,
            )

            if isinstance(keys, str):
                keys = (keys,)

            self.from_dict_options = DictOptions(keys=keys)


def dict_field(
    keys: list[str] | str,
    *,
    default=dataclasses.MISSING,
    default_factory=dataclasses.MISSING,
    init=True,
    repr=True,
    hash=None,
    compare=True,
    metadata=None,
):
    if (
        default is not dataclasses.MISSING
        and default_factory is not dataclasses.MISSING
    ):
        raise ValueError("cannot specify both default and default_factory")

    return DictField(
        keys if isinstance(keys, list) else [keys],
        default,
        default_factory,
        init,
        repr,
        hash,
        compare,
        metadata,
    )
