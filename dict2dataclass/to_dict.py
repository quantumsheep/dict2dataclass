import dataclasses
from typing import Any
import typing

from dict2dataclass.dict_field import DictField


@dataclasses.dataclass
class ToDict:
    def to_dict(self) -> dict[str, Any]:
        result = dict[str, Any]()

        fields = dataclasses.fields(type(self))

        for field in fields:
            value = getattr(self, field.name)

            if isinstance(value, ToDict):
                value = value.to_dict()
            elif isinstance(value, list) or isinstance(value, tuple):
                value = [v.to_dict() if isinstance(v, ToDict) else v for v in value]
            elif isinstance(value, dict):
                value = {
                    k: v.to_dict() if isinstance(v, ToDict) else v
                    for k, v in value.items()
                }

            name = field.name
            if isinstance(field, DictField):
                name = field.from_dict_options.keys[0]

            result[name] = value

        return result
