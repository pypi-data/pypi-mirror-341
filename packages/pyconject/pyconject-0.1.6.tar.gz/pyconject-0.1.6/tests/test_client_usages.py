import os
from unittest import TestCase
from unittest.mock import patch
import tempfile
from pathlib import Path
import yaml

from pyconject import pyconject
from pyconject.context import CntxStack

from unittest_utils import get_dynamic_mock_open, remove_file_or_directory
from black_p.black_sp.black_m import black_func, BlackClass
from dev_p.dev_sp.dev_m import dev_func_m


class ClientUsageTest(TestCase):

    def setUp(self):
        self.configs = yaml.dump(
            {
                "black_p": {
                    "black_sp": {
                        "black_m": {
                            "black_func": {
                                "b": "clt-defined-in-configs-b",
                                "c": "clt-defined-in-configs-c",
                            }
                        }
                    }
                }
            }
        )
        self.configs_dev = yaml.dump(
            {
                "black_p": {
                    "black_sp": {
                        "black_m": {"black_func": {"c": "clt-defined-in-configs-dev-c"}}
                    }
                }
            }
        )
        with open("tests/cfgs.yml", "wt") as f:
            yaml.safe_dump(
                {"dev_p": {"dev_sp": {"dev_m": {"dev_func_m": {"a": "a1"}}}}}, f
            )
        while len(pyconject._cntx_stack.config_stack) > 0:
            pyconject._cntx_stack.config_stack.pop()
        while len(pyconject._cntx_stack.target_stack) > 0:
            pyconject._cntx_stack.target_stack.pop()

    def tearDown(self) -> None:
        remove_file_or_directory(Path("tests/cfgs.yml"))
        return super().tearDown()

    def test_vanilla(self):
        with self.assertRaises(TypeError):
            black_func()

        a, b, c, d = black_func(1, 2, 3)
        assert (a, b, c, d) == (1, 2, 3, "dev-default-in-func-definion")

    def test_cntx_default(self):
        with patch(
            "builtins.open",
            get_dynamic_mock_open(
                {
                    (Path("./configs.yml"), "rt"): self.configs,
                    (Path("./configs-dev.yml"), "rt"): self.configs_dev,
                }
            ),
        ):
            pyconject.init(globals())
            with pyconject.cntx():
                a, b, c, d = black_func(1, 2)
                assert (a, b, c, d) == (
                    1,
                    2,
                    "clt-defined-in-configs-c",
                    "dev-default-in-func-definion",
                )

    def test_cntx_target_dev(self):
        with patch(
            "builtins.open",
            get_dynamic_mock_open(
                {
                    (Path("./configs.yml"), "rt"): self.configs,
                    (Path("./configs-dev.yml"), "rt"): self.configs_dev,
                }
            ),
        ):
            pyconject.init(globals())
            with pyconject.cntx(target="dev"):
                a, b, c, d = black_func(1, 2)
                assert (a, b, c, d) == (
                    1,
                    2,
                    "clt-defined-in-configs-dev-c",
                    "dev-default-in-func-definion",
                )

    def test_cntx_custom_cfg_files(self):
        with patch(
            "builtins.open",
            get_dynamic_mock_open(
                {
                    (Path("./cfgs.yml"), "rt"): self.configs,
                    (Path("./cfgs-dev.yml"), "rt"): self.configs_dev,
                }
            ),
        ):
            pyconject.init(globals())
            with pyconject.cntx(config_path="cfgs.yml"):
                a, b, c, d = black_func(1, 2)
                assert (a, b, c, d) == (
                    1,
                    2,
                    "clt-defined-in-configs-c",
                    "dev-default-in-func-definion",
                )

    def test_cntx_custom_cfg_files_target_dev(self):
        with patch(
            "builtins.open",
            get_dynamic_mock_open(
                {
                    (Path("./cfgs.yml"), "rt"): self.configs,
                    (Path("./cfgs-dev.yml"), "rt"): self.configs_dev,
                }
            ),
        ):
            pyconject.init(globals())
            with pyconject.cntx(config_path="cfgs.yml", target="dev"):
                a, b, c, d = black_func(1, 2)
                assert (a, b, c, d) == (
                    1,
                    2,
                    "clt-defined-in-configs-dev-c",
                    "dev-default-in-func-definion",
                )

    def test_cntx_custom_cfg_dict_target_dev(self):
        with patch(
            "builtins.open",
            get_dynamic_mock_open(
                {
                    (Path("./cfgs-custom.yml"), "rt"): self.configs,
                    (Path("./custom-cfgs-dev.yml"), "rt"): self.configs_dev,
                }
            ),
        ):
            pyconject.init(globals())
            with pyconject.cntx(
                config_path={"": "./cfgs-custom.yml", "dev": "./custom-cfgs-dev.yml"},
                target="dev",
            ):
                a, b, c, d = black_func(1, 2)
                assert (a, b, c, d) == (
                    1,
                    2,
                    "clt-defined-in-configs-dev-c",
                    "dev-default-in-func-definion",
                )

    def test_cntx_default_m_func(self):
        pyconject.init(globals())
        with pyconject.cntx(config_path="tests/cfgs.yml"):
            a, b, c, d = dev_func_m()
            assert (a, b, c, d) == ("a1", 20002, 3003, 404)

    def test_cntx_with_relative_references(self):
        configs = yaml.dump(
            {
                "black_p": {
                    "black_sp": {
                        "black_m": {
                            "black_func": {
                                "a": "a",
                                "b": "b",
                                "c": "@config-main.yml:black_func_configs.value_c",
                                "d": "@config-main.yml:black_func_configs.value_d",
                            }
                        }
                    }
                }
            }
        )
        config_main = yaml.dump(
            {
                "black_func_configs": {
                    "value_c": "ccc",
                    "value_d": "ddd",
                }
            }
        )

        with patch(
            "builtins.open",
            get_dynamic_mock_open(
                {
                    (Path("./config.yml"), "rt"): configs,
                    (Path("./config-main.yml"), "rt"): config_main,
                }
            ),
        ):

            pyconject.init(globals())
            with pyconject.cntx(config_path="./config.yml"):
                a, b, c, d = black_func()
                assert (a, b, c, d) == ("a", "b", "ccc", "ddd")

    def test_class(self):
        configs = yaml.dump(
            {
                "black_p": {
                    "black_sp": {
                        "black_m": {
                            "BlackClass": {
                                "__init__": {"a": "a"},
                                "black_method": {
                                    "b": "b",
                                },
                            }
                        }
                    }
                }
            }
        )

        with patch(
            "builtins.open",
            get_dynamic_mock_open(
                {
                    (Path("./config.yml"), "rt"): configs,
                }
            ),
        ):

            pyconject.init(globals())
            with pyconject.cntx(config_path="./config.yml"):
                black_class = BlackClass()
                assert black_class.a == "a"
                results = black_class.black_method()
                assert results == ("a", "b")
