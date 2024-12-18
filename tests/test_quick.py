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
import sympy as sp

import pyirk as p
from pyirk.utils import GeneralHousekeeperMixin
from ipydex import IPS, activate_ips_on_exception  # noqa


if os.environ.get("IPYDEX_AIOE") == "true":
    activate_ips_on_exception()

if not os.environ.get("PYIRK_DISABLE_CONSISTENCY_CHECKING", "").lower() == "true":
    p.cc.enable_consistency_checking()

PACKAGE_ROOT_PATH = Path(__file__).parent.parent.absolute().as_posix()


TEST_BASE_URI = "irk:/local/unittest"

class Test_02_math(GeneralHousekeeperMixin, unittest.TestCase):
    def setUp(self):
        # p.start_mod(ma.__URI__)
        super().setUp()
        self.ma = p.irkloader.load_mod_from_path(pjoin(PACKAGE_ROOT_PATH, "math1.py"), prefix="ma", reuse_loaded=True)

    # def tearDown(self):
    #     p.end_mod()

    def test_a00__ensure_version(self):
        self.assertGreaterEqual(version.parse(p.__version__), version.parse("0.13.2"))

    def test_q01__sp_to_irk_conversion1_basics(self):
        with p.uri_context(uri=TEST_BASE_URI, prefix="ut"):
            # run with `pytest -s tests/test_quick.py`
            I1000 = p.create_item(R1__has_label="a", R4__is_instance_of=p.I35["real number"])
            I1001 = p.create_item(R1__has_label="b", R4__is_instance_of=p.I35["real number"])
            I1002 = p.create_item(R1__has_label="c", R4__is_instance_of=p.I35["real number"])

            a, b, c = self.ma.items_to_symbols(I1000, I1001, I1002)
            formula1 = a + b * (a + c)

            res1 = self.ma.convert_sympy_to_irk(formula1)
            self.assertEqual(res1.R4__is_instance_of, p.I12["mathematical object"])
            self.assertEqual(res1.R35__is_applied_mapping_of, p.I55["add"])

            # note that sympy changes the order (w.r.t. how formula1 is written above)
            # formula1.args -> (s1_b*(s0_a + s2_c), s0_a)
            self.assertEqual(res1.R36__has_argument_tuple.R39__has_element[1], I1000["a"])

            # now use short versions of R36__has_argument_tuple and R39__has_element
            self.assertEqual(res1.R36.R39[0].R35__is_applied_mapping_of, p.I56["mul"])
            self.assertEqual(res1.R36.R39[0].R36.R39[0], I1001["b"])

    def test_q02__sp_to_irk_conversion2_advanced(self):
        with p.uri_context(uri=TEST_BASE_URI, prefix="ut"):
            # run with `pytest -s tests/test_quick.py`
            I2000 = p.create_item(R1__has_label="a", R4__is_instance_of=p.I35["real number"])
            I2001 = p.create_item(R1__has_label="b", R4__is_instance_of=p.I35["real number"])
            I2002 = p.create_item(R1__has_label="c", R4__is_instance_of=p.I35["real number"])
            I2003 = p.create_item(R1__has_label="j", R4__is_instance_of=p.I35["real number"])

            a, b, c, j = self.ma.items_to_symbols(I2000, I2001, I2002, I2003)
            formula1 = sp.Sum(a**j, (j, b, c))

            res1 = self.ma.convert_sympy_to_irk(formula1)

            self.assertTrue(p.is_instance_of(res1, p.I12["mathematical object"]))
            self.assertEqual(res1.R35__is_applied_mapping_of, self.ma.I5441["sum over index"])
            self.assertEqual(res1, self.ma.I5441["sum over index"](p.I57["pow"](I2000, I2003), I2003, self.ma.I5440["limits"](I2001, I2002)))

            formula2 = sp.Integral(a**2, (a, b, c))

            res2 = self.ma.convert_sympy_to_irk(formula2)

            self.assertTrue(p.is_instance_of(res2, p.I12["mathematical object"]))
            self.assertEqual(res2.R35__is_applied_mapping_of, self.ma.I5443["definite integral"])
            self.assertEqual(res2, self.ma.I5443["definite integral"](p.I57["pow"](I2000, 2), I2000, self.ma.I5440["limits"](I2001, I2002)))

            f3 = sp.Derivative(a*b, (a, 2))

            res3 = self.ma.convert_sympy_to_irk(f3)
            self.assertTrue(p.is_instance_of(res3, p.I12["mathematical object"]))
            self.assertEqual(res3.R35__is_applied_mapping_of, self.ma.I3513["derivative"])
            self.assertEqual(res3, self.ma.I3513["derivative"](p.I56["mul"](I2000, I2001), I2000, 2))


    def test_q03__sp_to_irk_conversion3_from_latex(self):
        from sympy.parsing.latex import parse_latex_lark
        with p.uri_context(uri=TEST_BASE_URI, prefix="ut"):
            I3000 = p.create_item(R1__has_label="s", R4__is_instance_of=p.I34["complex number"])
            I3001 = p.create_item(R1__has_label="i", R4__is_instance_of=p.I35["real number"])
            I3002 = p.create_item(R1__has_label="j", R4__is_instance_of=p.I35["real number"])
            I3003 = p.create_item(R1__has_label="F",
                                R4__is_instance_of=p.I7["mathematical operation with arity 1"],
                                R8__has_domain_of_argument_1=p.I34["complex number"],
                                R11__has_range_of_result=p.I34["complex number"])
            I3004 = p.create_item(R1__has_label="f",
                                R4__is_instance_of=p.I7["mathematical operation with arity 1"],
                                R8__has_domain_of_argument_1=p.I35["real number"],
                                R11__has_range_of_result=p.I35["real number"])
            I3005 = p.create_item(R1__has_label="k", R4__is_instance_of=p.I35["real number"]) # item that doesnt appear
            I3006 = p.create_item(R1__has_label="t", R4__is_instance_of=p.I35["real number"])
            item_list = [I3000, I3001, I3002, I3003, I3004, I3005, I3006]
            latex = r"s^i * F(s) - \sum\limits_{j=0}^{i-1}(s^{i-1-j} * f(t)^{j})"
            formula1 = parse_latex_lark(latex)
            res = self.ma.convert_latex_to_irk(formula1, item_list)
            target = p.I55["add"](
                p.I56["mul"](
                    -1,
                    self.ma.I5441["sum over index"](
                        p.I56["mul"](
                            p.I57["pow"](
                                I3000["s"],
                                p.add_items(
                                    -1,
                                    I3001["i"],
                                    p.I56["mul"](-1, I3002["j"])
                                )
                            ),
                            p.I57["pow"](I3004["f"](I3006["t"]), I3002["j"])
                        ),
                        I3002["j"],
                        self.ma.I5440["limits"](
                            self.ma.I5000["scalar zero"],
                            p.I55["add"](-1, I3001["i"])
                        )
                    )
                ),
                p.I56["mul"](
                    p.I57["pow"](I3000["s"], I3001["i"]),
                    I3003["F"](I3000["s"])
                )
            )
            self.assertEqual(res, target)

            latex = r"\frac{d}{dt}(1*f(t))"
            formula1 = parse_latex_lark(latex)
            res = self.ma.convert_latex_to_irk(formula1, item_list)
            self.assertEqual(res.R35__is_applied_mapping_of, self.ma.I3513["derivative"])


    def test_q04__irk_to_sp_conversion1(self):
        with p.uri_context(uri=TEST_BASE_URI, prefix="ut"):
            I4000 = p.create_item(R1__has_label="s", R4__is_instance_of=p.I34["complex number"])
            I4001 = p.create_item(R1__has_label="i", R4__is_instance_of=p.I35["real number"])
            I4002 = p.create_item(R1__has_label="j", R4__is_instance_of=p.I35["real number"])
            I4003 = p.create_item(R1__has_label="F",
                                R4__is_instance_of=p.I7["mathematical operation with arity 1"],
                                R8__has_domain_of_argument_1=p.I34["complex number"],
                                R11__has_range_of_result=p.I34["complex number"])
            I4004 = p.create_item(R1__has_label="f",
                                R4__is_instance_of=p.I7["mathematical operation with arity 1"],
                                R8__has_domain_of_argument_1=p.I35["real number"],
                                R11__has_range_of_result=p.I35["real number"])
            s, i, j = self.ma.items_to_symbols(I4000, I4001, I4002)
            F, f = self.ma.items_to_symbols(I4003, I4004, callable=True)
            expr = I4003["F"](I4000["s"]) + I4001["i"]**2 * I4004["f"](2)/(I4001["i"]-I4002["j"])
            res = self.ma.convert_irk_to_sympy(expr)
            self.assertIsInstance(res, sp.Add)
            target = F(s) + i**2*f(2) / (i-j)
            # only test subpart since F and f have different symbols
            self.assertEqual(res.args[0].args[1:], target.args[0].args[1:])

            expr2 = self.ma.I5444["indefinite integral"](I4000["s"]**2, I4000["s"])
            res2 = self.ma.convert_irk_to_sympy(expr2)
            target = sp.Integral(s**2, s)
            self.assertEqual(res2, target)

            expr3 = self.ma.derivative(I4000["s"]**3, I4000["s"], 2)
            res3 = self.ma.convert_irk_to_sympy(expr3)
            target = sp.Derivative(s**3, (s, 2))
            self.assertEqual(res3, target)

    @unittest.expectedFailure
    def test_q05__call_of_evaluted_mappings(self):
        with p.uri_context(uri=TEST_BASE_URI, prefix="ut"):
            # some mathematical function
            I4000 = p.create_item(R1__has_label="f",
                R4__is_instance_of=p.I7["mathematical operation with arity 1"],
                R8__has_domain_of_argument_1=p.I35["real number"],
                R11__has_range_of_result=p.I35["real number"])
            # some variables
            I4001 = p.create_item(R1__has_label="x", R4__is_instance_of=p.I35["real number"])
            I4002 = p.create_item(R1__has_label="t", R4__is_instance_of=p.I35["real number"])

            # derivative of a function that should return a callable
            deriv = self.ma.derivative(I4000["f"](I4001["x"]), I4001["x"])
            # evaluate the derivative
            deriv(0)

            # derivative of a constant should not be callable
            res = self.ma.derivative(1, I4001["x"])
            self.assertRaises(TypeError, res, 0)

            # integral of a function that should return a callable
            # integral = self.ma.I5444["indefinie integral"](I4000["f"](I4001["x"]), (I4001["x"]), self.ma.I5440["limits"](0, I4002["t"]))
            # eval
            # integral(0)
