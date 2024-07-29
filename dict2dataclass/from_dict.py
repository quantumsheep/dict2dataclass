from __future__ import annotations

import dataclasses
import typing
from types import UnionType
from typing import Any, Union

from dict2dataclass.dict_field import DictField


def _is_primitive(value: Any) -> bool:
    return value in (str, int, float, bool)


@dataclasses.dataclass
class FromDict:
    @classmethod
    def from_dict(cls, data: Any, fieldname=""):
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data)} for {fieldname}")

        type_hints = typing.get_type_hints(cls)
        fields = dataclasses.fields(cls)
        to_rename: dict[str, str] = {}

        for field in fields:
            if not isinstance(field, DictField):
                continue

            type_hint = type_hints.pop(field.name)

            for key in field.from_dict_options.keys:
                type_hints[key] = type_hint
                to_rename[key] = field.name

        kwargs = {}
        for key, value in data.items():
            if key not in type_hints:
                raise ValueError(
                    f"Unknown field {key} in type {type(cls)} for {fieldname}"
                )

            type_hint = type_hints[key]

            kwargs_key = to_rename.get(key, key)
            kwargs[kwargs_key] = FromDict._from_any(type_hint, value, key)

        return cls(**kwargs)

    @staticmethod
    def _from_any(T: type, value: Any, fieldname="") -> Any:
        if value is None:
            return None

        origin = typing.get_origin(T)

        if origin is list:
            if not isinstance(value, list):
                raise ValueError(f"Expected list, got {type(value)} for {fieldname}")

            arg_type = typing.get_args(T)[0]

            return [
                FromDict._from_any(arg_type, item, f"{fieldname}[{i}]")
                for i, item in enumerate(value)
            ]
        elif origin is tuple:
            if not isinstance(value, list) and not isinstance(value, tuple):
                raise ValueError(
                    f"Expected list or tuple, got {type(value)} for {fieldname}"
                )

            arg_types = typing.get_args(T)

            if len(arg_types) != len(value):
                raise ValueError(
                    f"Expected {len(arg_types)} elements, got {len(value)} for {fieldname}"
                )

            return tuple(
                FromDict._from_any(arg_type, item, f"{fieldname}[{i}]")
                for i, (arg_type, item) in enumerate(zip(arg_types, value))
            )
        elif origin is dict:
            if not isinstance(value, dict):
                raise ValueError(f"Expected dict, got {type(value)} for {fieldname}")

            key_type, value_type = typing.get_args(T)
            return {
                FromDict._from_any(
                    key_type,
                    k,
                    f"{fieldname}[{k}]",
                ): FromDict._from_any(
                    value_type,
                    v,
                    f"{fieldname}[{k}]",
                )
                for k, v in value.items()
            }
        elif _is_primitive(T):
            if not isinstance(value, T):
                raise ValueError(f"Expected {T}, got {type(value)} for {fieldname}")

            return value
        elif origin is Union or origin is UnionType:
            types = typing.get_args(T)
            for subtype in types:
                try:
                    return FromDict._from_any(subtype, value, fieldname)
                except ValueError as e:
                    last_error = e

            raise last_error
        elif isinstance(T, type) and issubclass(T, FromDict):
            return T.from_dict(value, fieldname)

        raise ValueError(f"Unsupported type {T}")
