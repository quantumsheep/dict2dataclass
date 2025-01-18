from __future__ import annotations

import dataclasses
import unittest

from dict2dataclass import FromDict, dict_field


class TestFromDict(unittest.TestCase):
    @dataclasses.dataclass
    class Foo(FromDict):
        @dataclasses.dataclass
        class SubFoo(FromDict):
            subbar_str: str
            subbars_list_str: list[str]

        bar_str: str
        bar_list_str: list[str]
        bar_tuple_str: tuple[str, int, float]
        bar_dict_str_subfoo: dict[str, SubFoo]
        bar_subfoo: SubFoo
        bar_subfoos: list[SubFoo]

        bar_renamed_foo: str = dict_field(keys="bar_renamed")

    def test_from_dict(self):
        data = {
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

        foo = self.Foo.from_dict(data)

        self.assertEqual(foo.bar_str, "bar")
        self.assertEqual(foo.bar_list_str, ["bar1", "bar2"])
        self.assertEqual(foo.bar_tuple_str, ("bar1", 1, 1.0))
        self.assertEqual(foo.bar_dict_str_subfoo["subfoo1"].subbar_str, "subbar1")
        self.assertEqual(
            foo.bar_dict_str_subfoo["subfoo1"].subbars_list_str, ["subbar1"]
        )
        self.assertEqual(foo.bar_dict_str_subfoo["subfoo2"].subbar_str, "subbar2")
        self.assertEqual(
            foo.bar_dict_str_subfoo["subfoo2"].subbars_list_str, ["subbar2"]
        )
        self.assertEqual(foo.bar_subfoo.subbar_str, "subbar")
        self.assertEqual(foo.bar_subfoo.subbars_list_str, ["subbar"])
        self.assertEqual(foo.bar_subfoos[0].subbar_str, "subbar1")
        self.assertEqual(foo.bar_subfoos[0].subbars_list_str, ["subbar1"])
        self.assertEqual(foo.bar_subfoos[1].subbar_str, "subbar2")
        self.assertEqual(foo.bar_subfoos[1].subbars_list_str, ["subbar2"])
        self.assertEqual(foo.bar_renamed_foo, "bar")

    def test_unsupported_type(self):
        @dataclasses.dataclass
        class Foo(FromDict):
            bar_int: int
            bar_list: list[int]
            bar_tuple: tuple[int, int]
            bar_dict: dict[int, int]

        # Correct
        Foo.from_dict(
            {
                "bar_int": 1,
                "bar_list": [1, 2],
                "bar_tuple": (1, 2),
                "bar_dict": {1: 2},
            }
        )

        # Bad primitive
        with self.assertRaises(ValueError):
            Foo.from_dict(
                {
                    "bar_int": "1",
                    "bar_list": [1, 2],
                    "bar_tuple": (1, 2),
                    "bar_dict": {1: 2},
                }
            )

        # Bad list
        with self.assertRaises(ValueError):
            Foo.from_dict(
                {
                    "bar_int": 1,
                    "bar_list": ["1", 2],
                    "bar_tuple": (1, 2),
                    "bar_dict": {1: 2},
                }
            )

        # Bad tuple
        with self.assertRaises(ValueError):
            Foo.from_dict(
                {
                    "bar_int": 1,
                    "bar_list": [1, 2],
                    "bar_tuple": (1, "2"),
                    "bar_dict": {1: 2},
                }
            )

        # Bad dict key
        with self.assertRaises(ValueError):
            Foo.from_dict(
                {
                    "bar_int": 1,
                    "bar_list": [1, 2],
                    "bar_tuple": (1, 2),
                    "bar_dict": {"1": 2},
                }
            )

        # Bad dict value
        with self.assertRaises(ValueError):
            Foo.from_dict(
                {
                    "bar_int": 1,
                    "bar_list": [1, 2],
                    "bar_tuple": (1, 2),
                    "bar_dict": {1: "2"},
                }
            )

    def test_subclass(self):
        @dataclasses.dataclass
        class Foo(FromDict):
            bar_str: str

        @dataclasses.dataclass
        class Bar(Foo):
            bar_int: int

        data = {"bar_str": "bar", "bar_int": 1}
        bar = Bar.from_dict(data)

        self.assertEqual(bar.bar_str, "bar")
        self.assertEqual(bar.bar_int, 1)

    def test_raise_on_unknown_fields(self):
        @dataclasses.dataclass
        class Foo(FromDict):
            bar_str: str

        with self.assertRaises(ValueError):
            Foo.from_dict({"bar_str": "bar", "bar_int": 1}, ignore_unknown_fields=False)
