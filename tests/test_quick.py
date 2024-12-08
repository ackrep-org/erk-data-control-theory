"""
This module serves for quickly testing specific features during development.
(because ordinary tests take long to setup)
"""

import os
import unittest
from packaging import version
import itertools
from os.path import join as pjoin
from pathlib import Path
import pyirk as p
from ipydex import IPS, activate_ips_on_exception  # noqa


if os.environ.get("IPYDEX_AIOE") == "true":
    activate_ips_on_exception()

if not os.environ.get("PYIRK_DISABLE_CONSISTENCY_CHECKING", "").lower() == "true":
    p.cc.enable_consistency_checking()

PACKAGE_ROOT_PATH = Path(__file__).parent.parent.absolute().as_posix()
ma = p.irkloader.load_mod_from_path(pjoin(PACKAGE_ROOT_PATH, "math1.py"), prefix="ma", reuse_loaded=True)

class Test_02_math(unittest.TestCase):
    def setUp(self):
        p.start_mod(ma.__URI__)

    def tearDown(self):
        p.end_mod()

    def test_a00__ensure_version(self):
        self.assertGreaterEqual(version.parse(p.__version__), version.parse("0.13.2"))

    def test_q01__sp_to_irk_conversion(self):
        # run with `pytest -s tests/test_quick.py`
        I1000 = p.create_item(R1__has_label="a", R4__is_instance_of=p.I35["real number"])
        I1001 = p.create_item(R1__has_label="b", R4__is_instance_of=p.I35["real number"])
        I1002 = p.create_item(R1__has_label="c", R4__is_instance_of=p.I35["real number"])

        a, b, c = ma.items_to_symbols(I1000, I1001, I1002)
        formula1 = a + b*(a + c)

        res1 = ma.convert_sympy_to_irk(formula1)
        self.assertEqual(res1.R4__is_instance_of, p.I12["mathematical object"])
        self.assertEqual(res1.R35__is_applied_mapping_of, p.I55["add"])

        # note that sympy changes the order (w.r.t. how formula1 is written above)
        # formula1.args -> (s1_b*(s0_a + s2_c), s0_a)
        self.assertEqual(res1.R36__has_argument_tuple.R39__has_element[1], I1000["a"])

        # now use short versions of R36__has_argument_tuple and R39__has_element
        self.assertEqual(res1.R36.R39[0].R35__is_applied_mapping_of, p.I56["mul"])
        self.assertEqual(res1.R36.R39[0].R36.R39[0], I1001["b"])
