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
ag = p.irkloader.load_mod_from_path(pjoin(PACKAGE_ROOT_PATH, "agents1.py"), prefix="ag")
ma = p.irkloader.load_mod_from_path(pjoin(PACKAGE_ROOT_PATH, "math1.py"), prefix="ma", reuse_loaded=True)
ct = p.irkloader.load_mod_from_path(pjoin(PACKAGE_ROOT_PATH, "control_theory1.py"), prefix="ct", reuse_loaded=True)


class Test_01_basics(unittest.TestCase):
    def test_a00__ensure_version(self):
        self.assertGreaterEqual(version.parse(p.__version__), version.parse("0.13.0"))


class Test_02_math(unittest.TestCase):
    def setUp(self):
        p.start_mod(ma.__URI__)

    def tearDown(self):
        p.end_mod()

    def test_c01__column_stack(self):

        # create some matrices which will be stacked later
        A = p.instance_of(ma.I9904["matrix"])
        b = p.instance_of(ma.I9904["matrix"])

        # different ways to define column stacks:
        colstack1: p.Item = p.instance_of(ma.I3237["column stack"])

        # add the elements of the column-stack element by element
        colstack1.set_relation(ma.R7490["has sequence element"], A)
        colstack1.set_relation(ma.R7490["has sequence element"], b)

        # check
        rels = colstack1.get_relations("ma__R7490__has_sequence_element", return_obj=True)
        self.assertEqual(rels, [A, b])

        # add the elements of the column-stack all at once
        colstack2: p.Item = p.instance_of(ma.I3237["column stack"])
        colstack2.set_multiple_relations(ma.R7490["has sequence element"], (A, b))

        # check
        rels = colstack2.get_relations("ma__R7490__has_sequence_element", return_obj=True)
        self.assertEqual(rels, [A, b])

        # construct a situation like in the Kalman controllability matrix: Q = (b, A*b, A^2*b, ...)
        colstack3: p.Item = p.instance_of(ma.I3237["column stack"])

        # arbitrary range (here from 0 to 24)
        with ma.IntegerRangeElement(start=0, stop=24) as i:
            prod = ma.I5177["matmul"](ma.I1474["matpow"](A, i), b)
            colstack3.set_relation("ma__R7490__has_sequence_element", prod)

    def test_c02__eigenvalues(self):
        A = p.instance_of(ma.I9906["square matrix"])
        s = p.instance_of(ma.I5030["variable"])

        # construct sI - A
        M = ma.I6324["canonical first order monic polynomial matrix"](A, s)

        # TODO: __automate_typing__
        M.R30__is_secondary_instance_of = ma.I9906["square matrix"]

        self.assertTrue(M.R4__is_instance_of, ma.I1935["polynomial matrix"])
        self.assertTrue(M.ma__R8736__depends_polynomially_on, s)

        d = ma.I5359["determinant"](M)
        self.assertTrue(d.ma__R8736__depends_polynomially_on, s)

    def test_c04a_symbolic_formula1(self):

        t = p.instance_of(ma.I2917["planar triangle"])
        sides = ma.I9148["get polygon sides ordered by length"](t)
        a, b, c = sides.R39__has_element

        la, lb, lc = ma.items_to_symbols(a, b, c, relation=ma.R2495["has length"])
        symbolic_sum = la + lb + lc

        sum_item = ma.symbolic_expression_to_graph_expression(symbolic_sum)
        self.assertEqual(sum_item.get_arguments()[0].get_arguments(), [a.R2495__has_length, b.R2495__has_length])
        self.assertEqual(sum_item.get_arguments()[1], c.R2495__has_length)
        self.assertEqual(sum_item.R4__is_instance_of, ma.I6043["sum"])

        symbolic_prod = la*lb
        prod_item = ma.symbolic_expression_to_graph_expression(symbolic_prod)
        self.assertEqual(prod_item.get_arguments(), [a.R2495__has_length, b.R2495__has_length])
        self.assertEqual(prod_item.R4__is_instance_of, ma.I5916["product"])

    # @unittest.expectedFailure
    def test_c04b_symbolic_formula2(self):

        A = p.instance_of(ma.I9904["matrix"])
        P = p.instance_of(ma.I9904["matrix"])
        A_T = ma.I3263["transpose"](A)

        As, Ps = ma.items_to_symbols(A, P)

        self.assertIsInstance(As.T, ma.sp.Symbol)
        self.assertTrue(As.T is As.T)

        # abbreviation for convenience
        se_to_ge = ma.symbolic_expression_to_graph_expression


        sum1 = se_to_ge(Ps + As)
        self.assertEqual(sum1.R4__is_instance_of, ma.I9904["matrix"])
        self.assertEqual(sum1.R35__is_applied_mapping_of, ma.I9493["matadd"])

        prod1 = se_to_ge(Ps*As)
        self.assertEqual(prod1.R4__is_instance_of, ma.I9904["matrix"])
        self.assertEqual(prod1.R35__is_applied_mapping_of, ma.I5177["matmul"])

        expr_item1 = ma.I9493["matadd"](ma.I5177["matmul"](ma.I3263["transpose"](A), P), ma.I5177["matmul"](P, A))

        expr2 = As.T*Ps + Ps*As
        expr_item2 = se_to_ge(expr2)
        self.assertEqual(expr_item1, expr_item2)

        x = p.instance_of(ma.I1168["point in state space"])

        D = p.instance_of(ma.I5167["state space"])
        n = n=p.instance_of(p.I39["positive integer"])
        D.ma__R3326__has_dimension = n
        x.R15__is_element_of = D

        x_mat = ma.I9489["vector to matrix"](ma.I1284["point in vector space to vector"](x))

        xs = ma.items_to_symbols(x_mat)
        V = xs.T*Ps*xs

        V_expr_item = se_to_ge(V)

        self.assertEqual(V_expr_item.R4__is_instance_of, ma.I9904["matrix"])
        self.assertEqual(V_expr_item.R35__is_applied_mapping_of, ma.I5177["matmul"])


    def test_c05__cc_matrix_dimensions(self):

        I5073 = ma.I5073

        # test the rule which produces a I48["constraint violation"] instance
        res = p.ruleengine.apply_semantic_rule(I5073, ma.__URI__)

        self.assertGreaterEqual(len(res.new_statements), 1)
        self.assertEqual(len(res.new_entities), 1)

        cvio, = ma.failed_multiplication.R74__has_constraint_violation
        self.assertEqual(cvio.R76__has_associated_rule, I5073)
        self.assertEqual(cvio.R4__is_instance_of, p.I48["constraint violation"])

        # self.assertEqual(A2B.R74__has_constraint_violation, [])

        # test propagation of matrix dimensions in the product: x.T * P * x

        itm = ct.I2613["theorem for Lyapunov functions for linear systems"]
        stm = itm.scp__assertion.get_inv_relations("R20", return_subj=True)[3]
        self.assertTrue(isinstance(stm, p.Statement))
        res = stm.object
        self.assertEqual(res.R4__is_instance_of, ma.I1063["scalar function"])

        # get the matmul-result
        xTPx = res.R36__has_argument_tuple.R39__has_element[0]
        xTP, x = xTPx.R36__has_argument_tuple.R39__has_element
        xT, P = xTP.R36__has_argument_tuple.R39__has_element

        x_vect = x.R36__has_argument_tuple.R39__has_element[0]

        n = P.R5938__has_row_number
        self.assertEqual(str(n.R1__has_label), "n")
        self.assertEqual(P.R5939__has_column_number, n)
        self.assertEqual(x_vect.R3326__has_dimension, n)
        self.assertEqual(x.R5938__has_row_number, n)
        self.assertEqual(x.R5939__has_column_number, 1)

        self.assertEqual(xT.R5938__has_row_number, 1)
        self.assertEqual(xT.R5939__has_column_number, n)

    def test_c06__cc_opposite_relation(self):

        I5073 = ct.I5073["create I48__constraint_violation for is_opposite_of relation"]

        # test entities
        ## should fail:
        contradicting_equilibrium = p.instance_of(ct.I9820["equilibrium point"])
        contradicting_equilibrium.set_relation(p.R16["has property"], ct.I8303["strict Lyapunov instability"])
        contradicting_equilibrium.set_relation(p.R16["has property"], ct.I2931["local Lyapunov stability"])
        ## shouldn't fail
        x = p.instance_of(ct.I9820["equilibrium point"])
        x.set_relation(p.R16["has property"], ct.I6467["saddle"])
        x.set_relation(p.R16["has property"], ct.I2931["local Lyapunov stability"])


        # test the rule which produces a I48["constraint violation"] instance
        res = p.ruleengine.apply_semantic_rule(I5073, ct.__URI__)


        # gather test entities that are expected to fail
        expected_failed_statements = [s for s in res.new_statements if s.subject == contradicting_equilibrium]
        self.assertEqual(len(expected_failed_statements), 1)

        cvio = contradicting_equilibrium.R74__has_constraint_violation[0]
        self.assertEqual(cvio.R76__has_associated_rule, I5073)
        self.assertEqual(cvio.R76__has_associated_rule, I5073)

        # actually problematic entities
        wrong_statements = [[s, d] for s, d in zip(res.new_statements, res.partial_results[0].statement_reports)
            if s.subject != contradicting_equilibrium and s.subject.R4 != p.I48["constraint violation"]]


        msg = ""
        for s, d in wrong_statements:
            info = d["bindinfo"]
            msg += f"Entity {info[1][1]} has contradicting relations {info[2][1]} and {info[3][1]}\n"

        self.assertEqual(len(wrong_statements), 0, msg=msg)
        # todo work some magic to give hint at where the problematic definitions are

    def test_c07__cc_theorem_application(self):

        # test system
        # linear, but not explicitly time invariant
        testrep_lin = p.instance_of(ct.I2928["general model representation"])
        testrep_lin.set_relation(ct.R5100["has model representation property"], ct.I4761["linearity"])
        testsys_lin = p.instance_of(ct.I7641["general system model"])
        testsys_lin.set_relation(ct.R2928["has model representation"], testrep_lin)

        # LTI
        testrep_lti = p.instance_of(ct.I2928["general model representation"])
        testrep_lti.set_relation(ct.R5100["has model representation property"], ct.I4761["linearity"])
        testsys_lti = p.instance_of(ct.I7641["general system model"])
        testsys_lti.set_relation(ct.R2928["has model representation"], testrep_lti)
        testsys_lti.set_relation(ct.R8303["has general system property"], ct.I7733["time invariance"])

        # polynomial, time invariant
        testrep_ti_poly = p.instance_of(ct.I2928["general model representation"])
        testrep_ti_poly.set_relation(ct.R5100["has model representation property"], ct.I5247["polynomial"])
        testsys_ti_poly = p.instance_of(ct.I7641["general system model"])
        testsys_ti_poly.set_relation(ct.R2928["has model representation"], testrep_ti_poly)
        testsys_ti_poly.set_relation(ct.R8303["has general system property"], ct.I7733["time invariance"])

        # only time invariant
        testrep_ti = p.instance_of(ct.I2928["general model representation"])
        testsys_ti = p.instance_of(ct.I7641["general system model"])
        testsys_ti.set_relation(ct.R2928["has model representation"], testrep_ti)
        testsys_ti.set_relation(ct.R8303["has general system property"], ct.I7733["time invariance"])

        # <theorem>
        I6210 = p.create_item(
            R1__has_label="test theorem",
            R2__has_description=("test"),
            R4__is_instance_of=p.I17["equivalence proposition"],
        )

        with I6210["test theorem"].scope("setting") as cm:
            sys = cm.new_var(sys=p.instance_of(ct.I7641["general system model"]))
            rep = cm.new_var(rep=p.instance_of(ct.I2928["general model representation"]))
            cm.new_rel(sys, ct.R2928["has model representation"], rep)
            cm.new_rel(rep, ct.R5100["has model representation property"], ct.I5247["polynomial"])

        with I6210["test theorem"].scope("premise") as cm:
            cm.new_rel(rep, ct.R5100["has model representation property"], ct.I4761["linearity"])

        with I6210["test theorem"].scope("assertion") as cm:
            V = cm.new_var(V=p.instance_of(ct.I9199["strong Lyapunov Function"]))
        # </theorem>


        # test start here:

        theorems = p.get_all_instances_of(p.I14["mathematical proposition"])
        systems = p.get_all_instances_of(ct.I7641["general system model"])

        def cond_func(sys, rep, th):
            # Note: most sys items here will be the systems created in the scope of a theorem. matching those doesn't make sense.
            # they have to be filtered out first
            # sys is from a setting scope:
            if sys.get_relations("R20"):
                if sys.get_relations("R20", return_obj=True)[0].R64 == "SETTING":
                    return False


            scopes = th.get_inv_relations("R21",return_subj=True)
            set, pre, ass = None, None, None
            for scope in scopes:
                match scope.R64:
                    case "SETTING":
                        set = scope
                    case "PREMISE":
                        pre = scope
                    case "ASSERTION":
                        ass = scope

            if set is None:
                return False

            setting_items = set.get_inv_relations("R20", return_subj=True)
            systh = [i for i in setting_items if isinstance(i, p.Item) and p.is_instance_of(i, ct.I7641["general system model"])]
            if len(systh) != 1:
                return False
            systh = systh[0]

            repth = [i for i in setting_items if isinstance(i, p.Item) and p.is_instance_of(i, ct.I2928["general model representation"])]
            if len(repth) != 1:
                return False
            repth = repth[0]

            cond = True
            # for each statement regarding sys in theorem
            for statement in sum(systh.get_relations().values(), []):
                # take only the property relations for now
                if "property" in statement.relation.R1:
                    rel_uri = statement.relation.uri
                    obj = statement.object
                    # make sure the systems has the same or more restrictive property as sys in th
                    # if relation does not exist -> False
                    cond = cond and (len(sys.get_relations(rel_uri)) > 0)
                    for stm in sys.get_relations(rel_uri):
                        if not p.is_subproperty(stm.object, obj):
                            cond = False
            # same for rep
            for statement in sum(repth.get_relations().values(), []):
                if "property" in statement.relation.R1:
                    rel_uri = statement.relation.uri
                    obj = statement.object
                    cond = cond and (len(rep.get_relations(rel_uri)) > 0)
                    for stm in rep.get_relations(rel_uri):
                        if not p.is_subproperty(stm.object, obj):
                            cond = cond and False


            return cond

        res_list = []
        for th, sys in itertools.product(theorems, systems):

            rep = sys.get_relations("irk:/ocse/0.2/control_theory#R2928", return_obj=True) # R2928__has_model_repr
            if len(rep) == 1:
                if cond_func(sys, rep[0], th):
                    res_list.append((sys, th))
            elif len(rep) == 0:
                continue
            else:
                raise IndexError

        res = p.RuleResult()
        for s, t in res_list:
            res.new_statements.append(t.set_relation(p.R80["applies to"], s))
            # print(t, "applies to", s)
        print(res.new_statements)
        self.assertTrue(len(res.new_statements) >= 7)

    def test_d01__sp_to_irk_conversion(self):
        I4000 = p.create_item(R1__has_label="a", R4__is_instance_of=p.I35["real number"])
        I4001 = p.create_item(R1__has_label="b", R4__is_instance_of=p.I35["real number"])
        I4002 = p.create_item(R1__has_label="c", R4__is_instance_of=p.I35["real number"])

        a, b, c = ma.items_to_symbols(I4000, I4001, I4002)
        formula1 = a + b*(a + c)

        res1 = ma.convert_sympy_to_irk(formula1)
        self.assertEqual(res1.R4__is_instance_of, p.I12["mathematical object"])
        self.assertEqual(res1.R35__is_applied_mapping_of, p.I55["add"])

        # note that sympy changes the order (w.r.t. how formula1 is written above)
        # formula1.args -> (s1_b*(s0_a + s2_c), s0_a)
        self.assertEqual(res1.R36__has_argument_tuple.R39__has_element[1], I4000["a"])

        # now use short versions of R36__has_argument_tuple and R39__has_element
        self.assertEqual(res1.R36.R39[0].R35__is_applied_mapping_of, p.I56["mul"])
        self.assertEqual(res1.R36.R39[0].R36.R39[0], I4001["b"])


class Test_02_control_theory(unittest.TestCase):
    def setUp(self):
        p.start_mod(ct.__URI__)

    def tearDown(self):
        p.end_mod()

    def test_b01__test_multilinguality(self):
        ct.I5290["reference value"].R1__has_label__de == "Sollwert"@p.de


class Test_03_agents(unittest.TestCase):
    def setUp(self):
        p.start_mod(ag.__URI__)

    def tearDown(self):
        p.end_mod()

    def test_c03__publications(self):
        x = ag.I7558["2002_Khalil"]
        self.assertEqual(x.ag__R8433__has_authors[0], ag.I9700["Hassan Khalil"])

        segment = ag.get_source_segment(ag.I7558["2002_Khalil"], "Section 4.1")
        self.assertEqual(segment.ag__R8437__has_segment_specification, ["Section 4.1"])

        segment2 = ag.get_source_segment(ag.I7558["2002_Khalil"], "Section 4.1")
        self.assertTrue(segment2 is segment)
