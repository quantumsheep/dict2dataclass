from __future__ import annotations

import dataclasses
import unittest

from dict2dataclass import dict_field
from dict2dataclass.to_dict import ToDict


class TestToDict(unittest.TestCase):
    @dataclasses.dataclass
    class Foo(ToDict):
        @dataclasses.dataclass
        class SubFoo(ToDict):
            subbar_str: str
            subbars_list_str: list[str]

        bar_str: str
        bar_list_str: list[str]
        bar_tuple_str: tuple[str, int, float]
        bar_dict_str_subfoo: dict[str, SubFoo]
        bar_subfoo: SubFoo
        bar_subfoos: list[SubFoo]

        bar_renamed_foo: str = dict_field(keys="bar_renamed")

    def test_to_dict(self):
        expected = {
            "bar_str": "bar",
            "bar_list_str": ["bar1", "bar2"],
            "bar_tuple_str": ["bar1", 1, 1.0],
            "bar_dict_str_subfoo": {
                "subfoo1": {"subbar_str": "subbar1", "subbars_list_str": ["subbar1"]},
                "subfoo2": {"subbar_str": "subbar2", "subbars_list_str": ["subbar2"]},
            },
            "bar_subfoo": {"subbar_str": "subbar", "subbars_list_str": ["subbar"]},
            "bar_subfoos": [
                {"subbar_str": "subbar1", "subbars_list_str": ["subbar1"]},
                {"subbar_str": "subbar2", "subbars_list_str": ["subbar2"]},
            ],
            "bar_renamed": "bar",
        }

        foo = self.Foo(
            bar_str="bar",
            bar_list_str=["bar1", "bar2"],
            bar_tuple_str=("bar1", 1, 1.0),
            bar_dict_str_subfoo={
                "subfoo1": self.Foo.SubFoo(
                    subbar_str="subbar1", subbars_list_str=["subbar1"]
                ),
                "subfoo2": self.Foo.SubFoo(
                    subbar_str="subbar2", subbars_list_str=["subbar2"]
                ),
            },
            bar_subfoo=self.Foo.SubFoo(
                subbar_str="subbar", subbars_list_str=["subbar"]
            ),
            bar_subfoos=[
                self.Foo.SubFoo(subbar_str="subbar1", subbars_list_str=["subbar1"]),
                self.Foo.SubFoo(subbar_str="subbar2", subbars_list_str=["subbar2"]),
            ],
            bar_renamed_foo="bar",
        )

        actual = foo.to_dict()
        self.assertDictEqual(expected, actual)
