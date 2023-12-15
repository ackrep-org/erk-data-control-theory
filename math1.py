from typing import Union
import pyirk as p

# noinspection PyUnresolvedReferences
from ipydex import IPS, activate_ips_on_exception  # noqa

ag = p.irkloader.load_mod_from_path("./agents1.py", prefix="ag")

__URI__ = "irk:/ocse/0.2/math"

keymanager = p.KeyManager()
p.register_mod(__URI__, keymanager)
p.start_mod(__URI__)

# data store on module level
ds = {}


I5000 = p.create_item(
    R1__has_label="scalar zero",
    R2__has_description="entity representing the zero-element in the set of complex numbers and its subsets",
    R4__is_instance_of=p.I38["non-negative integer"],
    R24__has_LaTeX_string="$0$",
)


I5001 = p.create_item(
    R1__has_label="scalar one",
    R2__has_description="entity representing the one-element in the set of complex numbers and its subsets",
    R4__is_instance_of=p.I39["positive integer"],
    R24__has_LaTeX_string="$1$",
)


I4895 = p.create_item(
    R1__has_label="mathematical operator",
    R2__has_description="general (unspecified) mathematical operator",
    R3__is_subclass_of=p.I12["mathematical object"],
)

# make all instances of operators callable:
I4895["mathematical operator"].add_method(p.create_evaluated_mapping, "_custom_call")


I9904 = p.create_item(
    R1__has_label="matrix",
    R2__has_description="matrix of (in general) complex numbers, i.e. matrix over the field of complex numbers",
    R3__is_subclass_of=p.I18["mathematical expression"],
)

I7151 = p.create_item(
    R1__has_label="vector",
    R2__has_description="vector of (in general) complex numbers, i.e. vector over the field of complex numbers",
    R3__is_subclass_of=p.I18["mathematical expression"],
)

I3240 = p.create_item(
    R1__has_label="matrix element",
    R2__has_description=(
        "mathematical operation wich maps a Matrix A, and two integers i, j to the scalar matrix entry A[i, j]. "
        "Index counting starts at 1"
    ),
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I9904["matrix"],
    R9__has_domain_of_argument_2=p.I39["positive integer"],
    R10__has_domain_of_argument_3=p.I39["positive integer"],
    R11__has_range_of_result=p.I34["complex number"],
    R13__has_canonical_symbol=r"$\mathrm{elt}$",
    R18__has_usage_hint=(
        "This operator is assumed be used as callable , e.g. `A_3_6 = I3240['matrix element'](A, 3, 6)`"
    ),
)

I3240["matrix element"].add_method(p.create_evaluated_mapping, "_custom_call")


# currently we do not need this (we attach start, stop, step to the range-element directly)
I1195 = p.create_item(
    R1__has_label="integer range",
    R2__has_description="represents an integer range with start-, stop- and step-value",
    R4__is_instance_of=p.I2["Metaclass"],
)


R1616 = p.create_relation(
    R1__has_label="has start value",
    R2__has_description="...",
    R8__has_domain_of_argument_1=I1195["integer range"],
    R11__has_range_of_result=p.I37["integer number"],
    R22__is_functional=True,
)

R1617 = p.create_relation(
    R1__has_label="has stop value",
    R2__has_description="...",
    R8__has_domain_of_argument_1=I1195["integer range"],
    R11__has_range_of_result=p.I37["integer number"],
    R22__is_functional=True,
)

R1618 = p.create_relation(
    R1__has_label="has step value",
    R2__has_description="...",
    R8__has_domain_of_argument_1=I1195["integer range"],
    R11__has_range_of_result=p.I37["integer number"],
    R22__is_functional=True,
)


# TODO: this is probably obsolete
def Range(start, stop, step=1, r1: str = None, r2: str = None):

    range_item = p.instance_of(I1195["integer range"], r1, r2)
    range_item.R1616__has_start_value = start
    range_item.R1617__has_stop_value = stop
    range_item.R1618__has_step_value = step

    return range_item


I6012 = p.create_item(
    R1__has_label="integer range element",
    R2__has_description="class whose instances represent an element from a specified range (I1195)",
    R3__is_subclass_of=p.I37["integer number"],
    R18__has_usage_hint=(
        "Should always have an R3240__has_associated_range relation; "
        "should be created via the context manager IntegerRangeElement (see below)"
    ),
)


R3240 = p.create_relation(
    R1__has_label="has associated range",
    R2__has_description="...",
    R8__has_domain_of_argument_1=I6012["integer range element"],
    R11__has_range_of_result=I1195["integer range"],
    R22__is_functional=True,
)


class IntegerRangeElement:
    """
    Context manager to model that a statement (or more) have an assertive claim for all elements of a sequence.

    ```
    with RangeElement(start=1, end=3) as i:
        I456["some item"].R789_has_some_property(i)
    ```

    Has (roughly) the same meaning as

    ```
    I456["some item"].R789_has_some_property(1)
    I456["some item"].R789_has_some_property(2)
    I456["some item"].R789_has_some_property(3)
    ```

    Note, however, that the defining attributes of RangeElement, i.e. `start`, `stop`, `step` can be also variables.

    Behind the sc

    """

    def __init__(self, start: Union[int, p.Item], stop: Union[int, p.Item], step: Union[int, p.Item] = 1):
        self.start = start
        self.stop = stop
        self.step = step

        # these might serve to provide optional information to the range_element_item
        self.r1 = None
        self.r2 = None

    @staticmethod
    def is_positive(i: Union[int, p.Item]) -> bool:
        if isinstance(i, int):
            return i > 0
        else:
            return p.is_instance_of(i, p.I39["positive integer"])

    @staticmethod
    def is_nonnegative(i: Union[int, p.Item]) -> bool:
        if isinstance(i, int):
            return i >= 0
        else:
            return p.is_instance_of(i, p.I38["non-negative integer"])

    def __enter__(self):
        """
        implicitly called in the head of the with statement
        :return:
        """

        if self.is_positive(self.start) and self.is_positive(self.step):
            class_item = p.I39["positive integer"]
        elif self.is_nonnegative(self.start) and self.is_nonnegative(self.step):
            class_item = p.I38["non-negative integer"]
        else:
            class_item = p.I37["integer number"]

        element = p.instance_of(class_item, self.r1, self.r2)
        element.R30__is_secondary_instance_of = I6012["integer range element"]

        # run this explicitly in the context of this module (otherwise R1616 etc. is not defined)
        with p.uri_context(uri=__URI__):
            element.R1616__has_start_value = self.start
            element.R1617__has_stop_value = self.stop
            element.R1618__has_step_value = self.step

        element.finalize()
        return element

    def __exit__(self, exc_type, exc_val, exc_tb):
        # this is the place to handle exceptions
        pass


I9905 = p.create_item(
    R1__has_label="zero matrix",
    R2__has_description="like its superclass but with all entries equal to zero",
    R3__is_subclass_of=I9904["matrix"],
)

I9906 = p.create_item(
    R1__has_label="square matrix",
    R2__has_description="a matrix for which the number of rows and columns are equal",
    R3__is_subclass_of=I9904["matrix"],
    # TODO: formalize the condition inspired by OWL
)

R5938 = p.create_relation(
    R1__has_label="has row number",
    R2__has_description="specifies the number of rows of a matrix",
    R8__has_domain_of_argument_1=I9904["matrix"],
    R11__has_range_of_result=p.I38["non-negative integer"],
    R22__is_functional=True,
)

# todo: specifies that this item defines I9905
R5939 = p.create_relation(
    R1__has_label="has column number",
    R2__has_description="specifies the number of columns of a matrix",
    R8__has_domain_of_argument_1=I9904["matrix"],
    R11__has_range_of_result=p.I38["non-negative integer"],
    R22__is_functional=True,
)


#            start definition

I9223 = p.create_item(
    R1__has_label="definition of zero matrix",
    R2__has_description="the defining statement of what a zero matrix is",
    R4__is_instance_of=p.I20["mathematical definition"],
)


with I9223["definition of zero matrix"].scope("setting") as cm:
    cm.new_var(M=p.uq_instance_of(I9904["matrix"]))

    cm.new_var(nr=p.uq_instance_of(p.I39["positive integer"]))
    cm.new_var(nc=p.instance_of(p.I39["positive integer"]))

    cm.new_rel(cm.M, R5938["has row number"], cm.nr)
    cm.new_rel(cm.M, R5939["has column number"], cm.nc)


with I9223["definition of zero matrix"].scope("premise") as cm:
    with IntegerRangeElement(start=1, stop=cm.nr) as i:
        with IntegerRangeElement(start=1, stop=cm.nc) as j:

            # create an auxiliary variable (not part part of the graph)
            M_ij = I3240["matrix element"](cm.M, i, j)
            cm.new_equation(lhs=M_ij, rhs=I5000["scalar zero"])


with I9223["definition of zero matrix"].scope("assertion") as cm:
    cm.new_rel(cm.M, p.R30["is secondary instance of"], I9905["zero matrix"])

#            end definition

# ---------------------------------------------------------------------------------------------------------------------

#            start definition

I1608 = p.create_item(
    R1__has_label="identity matrix",  # TODO: also known as "unit matrix"
    R2__has_description="square matrix with only ones at the main diagonal and every other element zero",
    R3__is_subclass_of=I9906["square matrix"],
)


I7169 = p.create_item(
    R1__has_label="definition of identity matrix",
    R2__has_description="the defining statement of what an identity matrix is",
    R4__is_instance_of=p.I20["mathematical definition"],
    R67__is_definition_of=I1608["identity matrix"],
)

I1608["identity matrix"].set_relation(p.R37["has definition"], I7169["definition of identity matrix"])


with I7169["definition of identity matrix"].scope("setting") as cm:
    cm.new_var(M=p.uq_instance_of(I9906["square matrix"]))

    cm.new_var(nr=p.uq_instance_of(p.I39["positive integer"]))

    cm.new_rel(cm.M, R5938["has row number"], cm.nr)


with I7169["definition of identity matrix"].scope("premise") as cm:

    # todo: the running indices should be related to the context cm
    # there should be a context stack
    with IntegerRangeElement(start=1, stop=cm.nr) as i:
        with IntegerRangeElement(start=1, stop=cm.nr) as j:

            # create an auxiliary variable (not part part of the graph)
            M_ij = I3240["matrix element"](cm.M, i, j)

            # Condition in human-readable form:
            # In case i != j, the matrix element M_ij must be 0
            # In case i == j, the matrix element M_ij must be 1

            # These are two implications (as logical statement, with their specific truth table)
            # Both implications must be fulfilled for the premise of the definition to be fulfilled

            with p.ImplicationStatement() as imp1:
                imp1.antecedent_relation(lhs=i, rsgn="!=", rhs=j)
                imp1.consequent_relation(lhs=M_ij, rsgn="==", rhs=I5000["scalar zero"])

            with p.ImplicationStatement() as imp2:
                imp2.antecedent_relation(lhs=i, rsgn="==", rhs=j)
                imp2.consequent_relation(lhs=M_ij, rsgn="==", rhs=I5001["scalar one"])


with I7169["definition of identity matrix"].scope("assertion") as cm:
    cm.new_rel(cm.M, p.R30["is secondary instance of"], I1608["identity matrix"])

#            end definition

# ---------------------------------------------------------------------------------------------------------------------

I8133 = p.create_item(
    R1__has_label="field of numbers",
    R1__has_label__de="Zahlenkörper",
    R2__has_description="general field of numbers; baseclass for the fields of real and complex numbers",
    R3__is_subclass_of=p.I13["mathematical set"],
)

# R3033 = p.create_relation(
#     R1__has_label="has type of elements",
#     R2__has_description=(
#         "specifies the item-type of the elements of a mathematical set; "
#         "should be a subclass of I12['mathematical object']"
#     ),
#     R8__has_domain_of_argument_1=p.I13["mathematical set"],
#     R11__has_range_of_result=p.I42["mathematical type (metaclass)"],
# )

I5006 = p.create_item(
    R1__has_label="imaginary part",
    R2__has_description="returns the imaginary part of a complex number",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=p.I34["complex number"],
    R11__has_range_of_result=p.I35["real number"],
)

I5807 = p.create_item(
    R1__has_label="sign",
    R2__has_description="returns the sign of a real number, i.e. on element of {-1, 0, 1}",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=p.I35["real number"],
    R11__has_range_of_result=p.I37["integer number"],
)


I2738 = p.create_item(
    R1__has_label="field of complex numbers",
    R2__has_description="field of complex numbers",
    R4__is_instance_of=I8133["field of numbers"],
    R13__has_canonical_symbol=r"$\mathbb{C}$",
    # R3033__has_type_of_elements=p.I34["complex number"],
)

I2739 = p.create_item(
    R1__has_label="open left half plane",
    R2__has_description="set of all complex numbers with negative real part",
    R4__is_instance_of=p.I13["mathematical set"],
    R14__is_subset_of=I2738["field of complex numbers"],
)

I1979 = p.create_item(
    R1__has_label="definition of open left half plane",
    R2__has_description="the defining statement of what I2739['open left half plane'] is",
    R4__is_instance_of=p.I20["mathematical definition"],
    R67__is_definition_of=I2739["open left half plane"],
)


with I1979["definition of open left half plane"].scope("setting") as cm:
    # Let HP be an arbitrary subset of complex numbers
    cm.new_var(HP=p.instance_of(p.I13["mathematical set"]))
    cm.new_rel(cm.HP, p.R14["is subset of"], I2738["field of complex numbers"])

    cm.new_var(z=p.instance_of(p.I34["complex number"]))
    # the premise should hold   for all   elements z of the subset HP
    cm.new_rel(cm.z, p.R15["is element of"], cm.HP, qualifiers=p.univ_quant(True))

    imag = I5006["imaginary part"]
    cm.new_var(y=imag(cm.z))

with I1979["definition of open left half plane"].scope("premise") as cm:
    cm.new_math_relation(cm.y, "<", I5000["scalar zero"])

with I1979["definition of open left half plane"].scope("assertion") as cm:
    cm.new_rel(cm.HP, p.R47["is same as"], I2739["open left half plane"])


I6259 = p.create_item(
    R1__has_label="sequence",
    R2__has_description="common (secondary) base class of sequence of mathematical objects",
    R3__is_subclass_of=p.I12["mathematical object"],
)


R7490 = p.create_relation(
    R1__has_label="has sequence element",
    R2__has_description=(
        "specifies the item-type of the elements of a mathematical set; "
        "should be a subclass of I12['mathematical object']"
    ),
    R8__has_domain_of_argument_1=I6259["sequence"],
    R11__has_range_of_result=p.I12["mathematical object"],
)


I3237 = p.create_item(
    R1__has_label="column stack",
    R2__has_description="sequence of columns of equal length which are stacked horizontally",
    R3__is_subclass_of=I9904["matrix"],
    R30__is_secondary_instance_of=I6259["sequence"],
    R18__has_usage_hint="see unittest in `test_package.Test_01_math.test_c01_column_stack`",
)


I5177 = p.create_item(
    R1__has_label="matmul",
    R2__has_description=("matrix multiplication operator"),
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I9904["matrix"],
    R9__has_domain_of_argument_2=I9904["matrix"],
    R11__has_range_of_result=I9904["matrix"],
)


I1474 = p.create_item(
    R1__has_label="matpow",
    R2__has_description=("power function for matrices like A**0 = I, A**1 = A, A**2 = A*A"),
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I9904["matrix"],
    R9__has_domain_of_argument_2=p.I38["non-negative integer"],
    R11__has_range_of_result=I9904["matrix"],
)

I9493 = p.create_item(
    R1__has_label="matadd",
    R2__has_description="matrix addition operator",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I9904["matrix"],
    R9__has_domain_of_argument_2=I9904["matrix"],
    R11__has_range_of_result=I9904["matrix"],
)

I1536 = p.create_item(
    R1__has_label="matneg",
    R2__has_description="negation operator for matrices",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I9904["matrix"],
    R11__has_range_of_result=I9904["matrix"],
)

I3263 = p.create_item(
    R1__has_label="transpose",
    R2__has_description="matrix transposition operator",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I9904["matrix"],
    R11__has_range_of_result=I9904["matrix"],
)

# copied from control_theory1:


I5484 = p.create_item(
    R1__has_label="finite set of complex numbers",
    R2__has_description="...",
    R3__is_subclass_of=p.I13["mathematical set"],
)

I1060 = p.create_item(
    R1__has_label="general function",
    R2__has_description="function that maps from some set (domain) into another (range);",
    R3__is_subclass_of=p.I18["mathematical expression"],
    R18__has_usage_hint="this is the base class for more specific types of functions",
)

I5094 = p.create_item(
    R1__has_label="linear function",
    R2__has_description="linear map from some set (domain) into another (range)",
    R3__is_subclass_of=I1060["general function"],
)

R9493 = p.create_relation(
    R1__has_label="has assigned linear map",
    R2__has_description="a matrix is assigned a linear map, that describes the transformation between two vector spaces",
    R8__has_domain_of_argument_1=I9904["matrix"],
    R11__has_range_of_result=I5094["linear function"],
    R22__is_functional=True,
)

I1063 = p.create_item(
    R1__has_label="scalar function",
    R2__has_description="function that has one (in general complex) number as result",
    R3__is_subclass_of=I1060["general function"],
    R46__is_secondary_subclass_of=p.I42["scalar mathematical object"],
)

I4237 = p.create_item(
    R1__has_label="monovariate rational function",
    R2__has_description="...",
    R3__is_subclass_of=I1063["scalar function"],
)

I4237["monovariate rational function"].add_method(p.create_evaluated_mapping, "_custom_call")

I6209 = p.create_item(
    R1__has_label="scalneg",
    R2__has_description="negation operator for scalars",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=p.I42["scalar mathematical object"],
    R11__has_range_of_result=p.I42["scalar mathematical object"],
)

I4239 = p.create_item(
    R1__has_label="abstract monovariate polynomial",
    R2__has_description=(
        "abstract monovariate polynomial (argument might be a complex-valued scalar, a matrix, an operator, etc.)"
    ),
    R3__is_subclass_of=I4237["monovariate rational function"],
)


R1757 = p.create_relation(
    R1__has_label="has set of roots",
    R2__has_description="set of roots for a monovariate function",
    R8__has_domain_of_argument_1=p.I18["mathematical expression"],  # todo: this is too broad
    R11__has_range_of_result=I5484["finite set of complex numbers"],
)


I1594 = p.create_item(
    R1__has_label="Stodolas necessary condition for polynomial coefficients",
    R2__has_description=(
        "establishes the fact that if all roots of a polynomial are located in the open left half plane, "
        "then all coefficients have the same sign."
    ),
    R4__is_instance_of=p.I15["implication proposition"],
    # TODO: test this feature (attribute name beginning with prefix) in pyirk.test_core
    ag__R6876__is_named_after=ag.I2276["Aurel Stodola"],
)


I9739 = p.create_item(
    R1__has_label="finite scalar sequence",
    R2__has_description="base class of a finite sequence of (in general) complex numbers; can be indexed",
    R3__is_subclass_of=I6259["sequence"],
)


R3668 = p.create_relation(
    R1__has_label="has sequence of coefficients",
    R2__has_description="object is the enumerated sequence of coefficients of a monovariate polynomial",
    R8__has_domain_of_argument_1=I4239["abstract monovariate polynomial"],
    R11__has_range_of_result=I9739["finite scalar sequence"],
)


with I1594["Stodolas necessary condition for polynomial coefficients"].scope("setting") as cm:

    cm.new_var(p=p.instance_of(I4239["abstract monovariate polynomial"]))
    cm.new_var(set_of_roots=p.instance_of(I5484["finite set of complex numbers"]))
    cm.new_var(seq_of_coeffs=p.instance_of(I9739["finite scalar sequence"]))

    cm.new_var(c1=p.instance_of(p.I35["real number"]))
    cm.new_var(c2=p.instance_of(p.I35["real number"]))

    cm.new_rel(cm.p, R1757["has set of roots"], cm.set_of_roots)
    cm.new_rel(cm.p, R3668["has sequence of coefficients"], cm.seq_of_coeffs)

    cm.new_rel(cm.c1, p.R15["is element of"], cm.seq_of_coeffs, qualifiers=p.univ_quant(True))
    cm.new_rel(cm.c2, p.R15["is element of"], cm.seq_of_coeffs, qualifiers=p.univ_quant(True))


with I1594["Stodolas necessary condition for polynomial coefficients"].scope("premise") as cm:
    cm.new_rel(cm.set_of_roots, p.R14["is subset of"], I2739["open left half plane"])

with I1594["Stodolas necessary condition for polynomial coefficients"].scope("assertion") as cm:
    cm.new_math_relation(lhs=I5807["sign"](cm.c1), rsgn="==", rhs=I5807["sign"](cm.c2))


I4240 = p.create_item(
    R1__has_label="matrix polynomial",
    R2__has_description="monovariate polynomial of quadratic matrices",
    R3__is_subclass_of=I4239["abstract monovariate polynomial"],
    R8__has_domain_of_argument_1=I9906["square matrix"],
    R11__has_range_of_result=I9906["square matrix"],
)

I1935 = p.create_item(
    R1__has_label="polynomial matrix",
    R2__has_description="matrix whose entries contain (scalar) polynomials",
    R3__is_subclass_of=I9904["matrix"],
    R50__is_different_from=I4240["matrix polynomial"],
)

I5030 = p.create_item(
    R1__has_label="variable",
    R2__has_description="symbol which can represent another mathematical object",
    R3__is_subclass_of=p.I12["mathematical object"],
)


R8736 = p.create_relation(
    R1__has_label="depends polynomially on",
    R2__has_description="subject has a polynomial dependency object",
    R8__has_domain_of_argument_1=p.I12["mathematical object"],
    R11__has_range_of_result=I5030["variable"],
    R18__has_usage_hint=("This relation is intentionally not functional to model multivariate polynomial dependency"),
)

# eigenvalues

I6324 = p.create_item(
    R1__has_label="canonical first order monic polynomial matrix",
    R2__has_description="for a given square matrix A returns the polynomial matrix (s·I - A)",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I9906["square matrix"],
    R9__has_domain_of_argument_2=I5030["variable"],
    R11__has_range_of_result=I1935["polynomial matrix"],
)


def I6324_cc_pp(self, res, *args, **kwargs):
    """
    :param self:    mapping item (to which this function will be attached)
    :param res:     instance of I1935["polynomial matrix"] (determined by R11__has_range_of_result)
    :param args:    arg tuple (<matrix>, <variable>) with which the mapping is called
    """

    assert len(args) == 2
    matrix, var = args

    # check that `var` is an instance of I5030["variable"]
    assert ("R4", I5030["variable"]) in p.get_taxonomy_tree(var)
    res.set_relation(R8736["depends polynomially on"], var)

    return res


I6324["canonical first order monic polynomial matrix"].add_method(I6324_cc_pp, "_custom_call_post_process")

I5359 = p.create_item(
    R1__has_label="determinant",
    R2__has_description="returns the determinant of a square matrix",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I9906["square matrix"],
    R11__has_range_of_result=p.I42["scalar mathematical object"],
)


def I5359_cc_pp(self, res, *args, **kwargs):
    """
    Function which will be attached as custom-call-post-process-method to I5359["determinant"].

    The I5359["determinant"] is an I4895__mathematical_operator. If it is called it creates an instance of
    I32__evaluated_mapping. The the `_custom_call_post_process`-method (i.e. this function) of the operator is called.

    :param self:    determinant operator item (to which this function will be attached)
    :param res:     instance of I7765["scalar mathematical object"] (determined by R11__has_range_of_result)
    :param args:    arg tuple (<matrix>) with which the mapping is called
    """

    assert len(args) == 1
    (matrix,) = args

    if poly_vars := matrix.R8736__depends_polynomially_on:
        for var in poly_vars:
            assert ("R4", I5030["variable"]) in p.get_taxonomy_tree(var)
            res.set_relation(R8736["depends polynomially on"], var)

    return res


I5359["determinant"].add_method(I5359_cc_pp, "_custom_call_post_process")


I9160 = p.create_item(
    R1__has_label="set of eigenvalues of a matrix",
    R2__has_description="returns the set of eigenvalues of a matrix",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I9906["square matrix"],
    R11__has_range_of_result=I5484["finite set of complex numbers"],
)

I1373 = p.create_item(
    R1__has_label="definition of set of eigenvalues of a matrix",
    R2__has_description="the defining statement of what a zero matrix is",
    R4__is_instance_of=p.I20["mathematical definition"],
    R67__is_definition_of=I9160["set of eigenvalues of a matrix"],
)


with I1373["definition of set of eigenvalues of a matrix"].scope("setting") as cm:
    cm.new_var(A=p.instance_of(I9906["square matrix"]))
    cm.new_var(s=p.instance_of(I5030["variable"]))
    cm.new_var(r=p.instance_of(I5484["finite set of complex numbers"]))

    # auxiliary variables
    M = I6324["canonical first order monic polynomial matrix"](cm.A, cm.s)

    # TODO: __automate_typing__
    M.R30__is_secondary_instance_of = I9906["square matrix"]

    d = I5359["determinant"](M)

with I1373["definition of set of eigenvalues of a matrix"].scope("premise") as cm:
    cm.new_rel(d, R1757["has set of roots"], cm.r)

with I1373["definition of set of eigenvalues of a matrix"].scope("assertion") as cm:
    cm.new_equation(I9160["set of eigenvalues of a matrix"](cm.A), cm.r)

# TODO: relate/unify this with R3668__has_sequence_of_coefficients
I3058 = p.create_item(
    R1__has_label="coefficients of characteristic polynomial",
    R2__has_description="...",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I9906["square matrix"],
    R11__has_range_of_result=I9739["finite scalar sequence"],
)

# the following theorem demonstrate the usage of the existential quantifier ∃ (expressed as qualifiers)
# see also https://pyirk-core.readthedocs.io/en/develop/userdoc/overview.html#universal-and-existential-quantification
# TODO: drop branch name in above link, once the docs are in main

I1566 = p.create_item(
    R1__has_label="theorem on the successor of integer numbers",
    R2__has_description=(
        "establishes the fact that for every integer x there exists another integer y which is bigger."
    ),
    R4__is_instance_of=p.I15["implication proposition"],
)

with I1566["theorem on the successor of integer numbers"].scope("setting") as cm:
    cm.new_var(x=p.uq_instance_of(p.I37["integer number"]))

with I1566["theorem on the successor of integer numbers"].scope("premise") as cm:
    # no further condition apart from the setting
    pass

with I1566["theorem on the successor of integer numbers"].scope("assertion") as cm:
    # technical note: the qualifier is passed to `instance_of()`, not to `new_var`
    cm.new_var(y=p.instance_of(p.I37["integer number"], qualifiers=[p.exis_quant(True)]))
    cm.new_math_relation(cm.y, ">", cm.x)


# preparation for next theorem

R5940 = p.create_relation(
    R1__has_label="has characteristic polynomial",
    R2__has_description="specifies the characteristic polynomial of a square matrix A, i.e. det(s·I-A)",
    R8__has_domain_of_argument_1=I9906["square matrix"],
    R11__has_range_of_result=I4239["abstract monovariate polynomial"],
)

# <definition>
I9907 = p.create_item(
    R1__has_label="definition of square matrix",
    R2__has_description="the defining statement of what a square matrix is",
    R4__is_instance_of=p.I20["mathematical definition"],
)

with I9907.scope("setting") as cm:
    cm.new_var(M=p.uq_instance_of(I9904["matrix"]))
    cm.new_var(nr=p.uq_instance_of(p.I39["positive integer"]))

    cm.new_var(nc=p.instance_of(p.I39["positive integer"]))

    cm.new_rel(cm.M, R5938["has row number"], cm.nr)
    cm.new_rel(cm.M, R5939["has column number"], cm.nc)

with I9907.scope("premise") as cm:
    # number of rows == number of columns
    cm.new_equation(lhs=cm.nr, rhs=cm.nc)

with I9907.scope("assertion") as cm:
    cm.new_rel(cm.M, p.R30["is secondary instance of"], I9906["square matrix"])

# </definition>

I9906["square matrix"].set_relation(p.R37["has definition"], I9907["definition of square matrix"])

# <theorem>

I3749 = p.create_item(
    R1__has_label="Cayley-Hamilton theorem",
    R2__has_description="establishes that every square matrix is a root of its own characteristic polynomial",
    R4__is_instance_of=p.I15["implication proposition"],
)

# TODO: specify universal quantification for A and n

with I3749["Cayley-Hamilton theorem"].scope("setting") as cm:
    cm.new_var(A=p.uq_instance_of(I9906["square matrix"]))
    cm.new_var(n=p.uq_instance_of(p.I39["positive integer"]))
    cm.new_var(coeffs_cp_A=I3058["coefficients of characteristic polynomial"](cm.A))

    cm.new_var(P=p.instance_of(I4240["matrix polynomial"]))

    cm.new_var(Z=p.instance_of(I9905["zero matrix"]))

    cm.new_rel(cm.A, R5938["has row number"], cm.n)
    cm.new_rel(cm.A, R5940["has characteristic polynomial"], cm.P)
    cm.new_rel(cm.Z, R5938["has row number"], cm.n)
    cm.new_rel(cm.Z, R5939["has column number"], cm.n)
    cm.new_rel(cm.Z, p.R24["has LaTeX string"], r"\mathbf{0}")

with I3749["Cayley-Hamilton theorem"].scope("assertion") as cm:
    cm.new_equation(lhs=cm.P(cm.A), rhs=cm.Z)

# </theorem>



I7559 = p.create_item(
    R1__has_label="cardinality",
    R2__has_description="returns the cardinality of a set or multiset",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=p.I13["mathematical set"],  # TODO: introduce multiset
    R11__has_range_of_result=p.I38["non-negative integer"],
)


I3589 = p.create_item(
    R1__has_label="monovariate polynomial degree",
    R2__has_description="returns degree of a monovariate polynomial",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I4239["abstract monovariate polynomial"],
    R11__has_range_of_result=p.I38["non-negative integer"],
)

I9628 = p.create_item(
    R1__has_label="theorem on the number of roots of a polynomial",
    R2__has_description=(
        "establishes the fact that a polynomial of degree n has exactly n roots "
        "(counting multiplicities)"
    ),
    R4__is_instance_of=p.I15["implication proposition"],
)

with I9628["theorem on the number of roots of a polynomial"].scope("setting") as cm:
    P = cm.new_var(P=p.instance_of(I4239["abstract monovariate polynomial"]))
    r = cm.new_var(r=p.instance_of(I5484["finite set of complex numbers"]))

with I9628["theorem on the number of roots of a polynomial"].scope("premise") as cm:
    cm.new_rel(P, R1757["has set of roots"], r)
    deg = I3589["monovariate polynomial degree"](P)
    card = I7559["cardinality"](r)

with I9628["theorem on the number of roots of a polynomial"].scope("assertion") as cm:
    cm.new_math_relation(deg, "==", card)


I6709 = p.create_item(
    R1__has_label="Lipschitz continuity",
    R2__has_description="states that the slope of a function is bounded",
    R4__is_instance_of=p.I54["mathematical property"],
    ag__R6876__is_named_after=ag.I7906["Rudolf Lipschitz"],
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/wiki/Q652707",
    R78__is_applicable_to=I1060["general function"],
)


# imported entities from control_theory1.py:

R3326 = p.create_relation(
    R1__has_label="has dimension",
    R2__has_description="specifies the dimension of a (dimensional) mathematical object",
    R8__has_domain_of_argument_1=p.I12["mathematical object"],
    R11__has_range_of_result=p.I38["non-negative integer"],
    R22__is_functional=True,
)

# TODO: improve taxonomy here
I5166 = p.create_item(
    R1__has_label="vector space",
    R2__has_description="type for a vector space",
    R3__is_subclass_of=p.I13["mathematical set"],
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/wiki/Q125977",
    R41__has_required_instance_relation=R3326["has dimension"],
)


# TODO: consider "state manifold"
I5167 = p.create_item(
    R1__has_label="state space",
    R2__has_description="type for a state space of a dynamical system (I6886)",
    R3__is_subclass_of=I5166["vector space"],

    # this should be defined via inheritance from vector space
    # TODO: test that this is the case
    # R41__has_required_instance_relation=R3326["has dimension"],
)


R5405 = p.create_relation(
    R1__has_label="has associated state space",
    R2__has_description="specifies the associated state space of the subject (e.g. a I9273__explicit...ode_system)",
    R8__has_domain_of_argument_1=p.I12["mathematical object"],
    R11__has_range_of_result=I5167["state space"],
    R22__is_functional=True,
)


# TODO: it might be worth to generalize this: creating a type from a set (where the set is an instance of another type)

I1169 = p.create_item(
    R1__has_label="point in vector space",
    R2__has_description="type for a point in a given vector space",
    R3__is_subclass_of=p.I12["mathematical object"],
)

I1168 = p.create_item(
    R1__has_label="point in state space",
    R2__has_description="type for a point in a given state space",
    R3__is_subclass_of=I1169["point in vector space"],
    R41__has_required_instance_relation=R5405["has associated state space"],
)

R9651 = p.create_relation(
    R1__has_label="has domain",
    R2__has_description="specifies that the subject (a function or operator) is defined for all values of the object (a set)",
    R8__has_domain_of_argument_1=I4895["mathematical operator"],
    R11__has_range_of_result=p.I13["mathematical set"],
    R22__is_functional=True,
)


R3798 = p.create_relation(
    R1__has_label="has origin",
    R2__has_description="specifies that the subject (a vector space) has the object as origin",
    R8__has_domain_of_argument_1=I5166["vector space"],
    R11__has_range_of_result=I1169["point in vector space"],
    R22__is_functional=True,
)


I9923 = p.create_item(
    R1__has_label="scalar field",
    R2__has_description="...",
    R3__is_subclass_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I1168["point in state space"],
    R11__has_range_of_result=p.I35["real number"],
)


I9841 = p.create_item(
    R1__has_label="vector field",
    R2__has_description="...",
    R3__is_subclass_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I1168["point in state space"],
    R11__has_range_of_result=I7151["vector"],
)


# The following is contributed by Xinghao Huang (during a semester project 2022/23)
# supervision: Carsten Knoll
# adaptation: assume only the origin is the point of interest


I5843 = p.create_item(
    R1__has_label="neighborhood",
    R2__has_description="a region of space around a point",
    R3__is_subclass_of=p.I13["mathematical set"],
)


R4963 = p.create_relation(
    R1__has_label="is neighborhood of",
    R2__has_description="specifies that the subject (a set) is a neighborhood of the object (a point)",
    R8__has_domain_of_argument_1=I5843["neighborhood"],
    R11__has_range_of_result=I1168["point in state space"],
)

R1536 = p.create_relation(
    R1__has_label="is valid on set",
    R2__has_description="specifies when a statement becomes true",
    R18__has_usage_hint="to be used as a qualifier",
)
on_set = p.QualifierFactory(R1536["is valid on set"])

I3133 = p.create_item(
    R1__has_label="local positive definiteness",
    R2__has_description="a special property of a scalar field in a neighborhood of the origin",
    R4__is_instance_of=p.I54["mathematical property"],
    R78__is_applicable_to=I9923["scalar field"],
)

I3134 = p.create_item(
    R1__has_label="definition of local positive definiteness",
    R2__has_description="the defining statement of positive definite",
    R4__is_instance_of=p.I20["mathematical definition"],
)

with I3134["definition of local positive definiteness"].scope("setting") as cm:
    h = cm.new_var(h=p.instance_of(I9923["scalar field"]))
    cm.new_rel(I3134["definition of local positive definiteness"], p.R79["has main subject"], h)

    n = cm.new_var(n=p.instance_of(p.I39["positive integer"]))
    M = cm.new_var(M=p.instance_of(I5167["state space"]))

    cm.new_rel(cm.h, R9651["has domain"], cm.M)
    cm.new_rel(cm.M, R3326["has dimension"], cm.n)

    x0 = cm.new_var(x0=p.instance_of(I1168["point in state space"]))
    cm.new_rel(cm.M, R3798["has origin"], cm.x0)

    u = cm.new_var(u=p.uq_instance_of(I5843["neighborhood"]))
    cm.new_rel(cm.u, R4963["is neighborhood of"], cm.x0)
    cm.new_rel(cm.u, p.R14["is subset of"],cm.M) # todo is this necessary? maybe rule in neighborhood

    x = cm.new_var(x=p.uq_instance_of(I1168["point in state space"]))


with I3134["definition of local positive definiteness"].scope("premise") as cm:
    cm.new_rel(cm.x, p.R15["is element of"], cm.u, qualifiers=p.univ_quant(True))
    # todo: nested implication statements
    with p.ImplicationStatement() as imp1:
        imp1.antecedent_relation(lhs=cm.x, rsgn="==", rhs=cm.x0)
        imp1.consequent_relation(lhs=cm.h(cm.x), rsgn="==", rhs=I5000["scalar zero"])

    with p.ImplicationStatement() as imp2:
        imp2.antecedent_relation(lhs=cm.x, rsgn="!=", rhs=cm.x0)
        imp2.consequent_relation(lhs=cm.h(cm.x), rsgn=">", rhs=I5000["scalar zero"])

with I3134["definition of local positive definiteness"].scope("assertion") as cm:
    cm.h.set_relation(p.R16["has property"], I3133["local positive definiteness"], qualifiers=[on_set(cm.u)])


I3133["local positive definiteness"].set_relation(
    p.R37["has definition"], I3134["definition of local positive definiteness"]
)

# TODO: for the following properties it would be nice to state the definition "relatively" to the
# definition of I3133["local positive definiteness"]
# for now: leave them as stubs

I3135 = p.create_item(
    R1__has_label="positive semidefiniteness",
    R2__has_description="a special property of a scalar field in a neighborhood of the origin",
    R4__is_instance_of=p.I54["mathematical property"],
    R78__is_applicable_to=I9923["scalar field"],
)

I3136 = p.create_item(
    R1__has_label="negative definiteness",
    R2__has_description="a special property of a scalar field in a neighborhood of the origin",
    R4__is_instance_of=p.I54["mathematical property"],
    R78__is_applicable_to=I9923["scalar field"],
)

I8492 = p.create_item(
    R1__has_label="definition of negative definiteness",
    R2__has_description="the defining statement of negative definiteness",
    R4__is_instance_of=p.I20["mathematical definition"],
)

with I8492["definition of negative definiteness"].scope("setting") as cm:
    cm.copy_from(I3134["definition of local positive definiteness"].get_subscope("setting"))

with I8492["definition of negative definiteness"].scope("premise") as cm:
    cm.new_rel(I6209["scalneg"](cm.h(cm.x)), p.R16["has property"], I3133["local positive definiteness"])

with I8492["definition of negative definiteness"].scope("assertion") as cm:
    cm.h.set_relation(p.R16["has property"], I3136["negative definiteness"])


I3136["negative definiteness"].set_relation(
    p.R37["has definition"], I8492["definition of negative definiteness"]
)

I3137 = p.create_item(
    R1__has_label="negative semidefiniteness",
    R2__has_description="a special property of a scalar field in a neighborhood of the origin",
    R4__is_instance_of=p.I54["mathematical property"],
    R78__is_applicable_to=I9923["scalar field"],
)


I9807 = p.create_item(
    R1__has_label="local Lipschitz continuity",
    R2__has_description="",
    R4__is_instance_of=p.I54["mathematical property"],
    R17__is_subproperty_of=I6709["Lipschitz continuity"]
)


I4505 = p.create_item(
    R1__has_label="global Lipschitz continuity",
    R2__has_description="",
    R4__is_instance_of=p.I54["mathematical property"],
    R17__is_subproperty_of=I6709["Lipschitz continuity"]
)


# TODO: specify to which objects this property can be meaningfully applied
I5753 = p.create_item(
    R1__has_label="radially unboundedness",
    R2__has_description=(
        "states that a function tend towards infinity if the argument goes to infinity "
        "(independent of direction)"
    ),
    R4__is_instance_of=p.I54["mathematical property"],
    R78__is_applicable_to=I9923["scalar field"],
)

I1778 = p.create_item(
    R1__has_label="homogeneity",
    R2__has_description=(
        "states that if all arguments of a function are multiplied by a scalar value, the function value is multiplied"
        " by some power k of same scalar"
    ),
    R4__is_instance_of=p.I54["mathematical property"],
    R78__is_applicable_to=I1060["general function"],
)

I4864 = p.create_item(
    R1__has_label="infinity class",
    R2__has_description="class for typechecking of infinity-object",
    R3__is_subclass_of=p.I18["mathematical expression"],
)

I4291 = p.create_item(
    R1__has_label="infinity",
    R2__has_description="infinity",
    R4__is_instance_of=I4864["infinity class"],
)

I6043 = p.create_item(
    R1__has_label="sum",
    R2__has_description="base class for general sums (result of addition)",
    R3__is_subclass_of=p.I18["mathematical expression"]
)

I5916 = p.create_item(
    R1__has_label="product",
    R2__has_description="base class for general products (result of multiplication)",
    R3__is_subclass_of=p.I18["mathematical expression"]
)


I5441 = p.create_item(
    R1__has_label="sum over index",
    R2__has_description="summation operator (capital Sigma)",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=p.I18["mathematical expression"],
    R9__has_domain_of_argument_2=p.I37["integer number"], # start
    R10__has_domain_of_argument_3=[p.I37["integer number"], I4864["infinity class"]], # stop
    R11__has_range_of_result=p.I18["mathematical expression"],

    # TODO:
    # R11__has_range_of_result=I6043["sum"],
)

I9489 = p.create_item(
    R1__has_label="vector to matrix",
    R2__has_description="convert a vector item to a matrix item for calculus",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I7151["vector"],
    R11__has_range_of_result=I9904["matrix"],
    R18__has_usage_hint="Use this operator to convert to matrix, then use matmul, matadd etc.",
)

I1284 = p.create_item(
    R1__has_label="point in vector space to vector",
    R2__has_description="convert a point in a vector space to the vector, pointing to that point",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I1169["point in vector space"],
    R11__has_range_of_result=I7151["vector"],
    R18__has_usage_hint="Use this operator to convert to vector/ matrix, then use matmul, matadd etc.",
)

I4218 = p.create_item(
    R1__has_label="matrix to vector",
    R2__has_description="convert a nx1 matrix item to a vector item for calculus",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I9904["matrix"],
    R11__has_range_of_result=I7151["vector"],
)

I2328 = p.create_item(
    R1__has_label="matrix to scalar",
    R2__has_description="convert a 1x1 matrix item to a scalar value",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I9904["matrix"],
    R11__has_range_of_result=I1063["scalar function"],
) # TODO build test

I7481 = p.create_item(
    R1__has_label="Jacobian",
    R2__has_description="Jacobi matrix of a vector field, operator",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I9841["vector field"],
    R11__has_range_of_result=I9906["square matrix"],
)

I2378 = p.create_item(
    R1__has_label="solution to a mathematical algorithm",
    R2__has_description="",
    R3__is_subclass_of=p.I12["mathematical object"],
)

I9827 = p.create_item(
    R1__has_label="mathematical algorithm",
    R2__has_description="",
    R4__is_instance_of=I4895["mathematical operator"],
    # R8__has_domain_of_argument_1=??,
    R11__has_range_of_result=p.I53["bool"], # if a solution exists or not
)

R3263 = p.create_relation(
    R1__has_label="has solution",
    R2__has_description="solution of a mathematical algorithm",
    R8__has_domain_of_argument_1=I9827["mathematical algorithm"],
    R11__has_range_of_result=I2378["solution to a mathematical algorithm"],
)

I9827["mathematical algorithm"].set_relation(R3263["has solution"], I2378["solution to a mathematical algorithm"])


# items to specify components of formulas


I2495 = p.create_item(
    R1__has_label="add",
    R2__has_description="general addition operator",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=p.I18["mathematical expression"],
    R9__has_domain_of_argument_2=p.I18["mathematical expression"],
    R11__has_range_of_result=I6043["sum"],
)

I9738 = p.create_item(
    R1__has_label="mul",
    R2__has_description="general multiplication operator",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=p.I18["mathematical expression"],
    R9__has_domain_of_argument_2=p.I18["mathematical expression"],
    R11__has_range_of_result=I5916["product"],
)


# helper function to simplify creation of formulas


def items_to_symbols(*args, relation=None) -> list:

    if not "item_symbol_map" in ds:
        ds["item_symbol_map"] = p.aux.OneToOneMapping()
    item_symbol_map = ds["item_symbol_map"]

    import sympy as sp
    n = len(item_symbol_map.a)
    res = []

    if relation is not None:
        # apply the provided relation
        assert isinstance(relation, p.core.Relation)
        args = [itm.get_relations(relation.uri, return_obj=True)[0] for itm in args]

    for i, itm in enumerate(args, start=n):
        assert isinstance(itm, p.Item)
        # TODO: check meaningful types (numbers, expressions, evaluated mappings, but not eg. ag.I7435["human"])
        suffix = itm.R1__has_label.split(" ")[0]
        name = f"s{i}_{suffix}"
        symb = sp.Symbol(name)
        res.append(symb)

        # a: keys=uris, values=symbols; b: keys=symbols, values=uris;
        item_symbol_map.add_pair(itm.uri, symb)

    return res


class symbolicExpressionToGraphExpressionConverter:
    def __init__(self, symb_expression) -> None:
        try:
            self.item_symbol_map = ds["item_symbol_map"]
        except KeyError:
            raise p.aux.PyIRKError("no item-symbol-associations were registered")

        # prevent sympy import on global level (because it is unnecessary in most cases)
        import sympy
        self.sp = sympy

        self.symb_expression = symb_expression

    def convert(self):
        return self._conv_object(self.symb_expression)

    def _conv_object(self, obj):
        if isinstance(obj, p.Item):
            return obj
        elif isinstance(obj, self.sp.Symbol):
            try:
                uri = self.item_symbol_map.b[obj]
            except KeyError:
                msg = f"unknown symbol {obj} while converting expression {self.symb_expression}"
            return p.ds.get_entity_by_uri(uri)
        elif isinstance(obj, self.sp.Add):
            return self._conv_add(obj.args)
        elif isinstance(obj, self.sp.Mul):
            return self._conv_mul(obj.args)

    def _conv_add(self, args):
        return self._apply_operator(args, I2495["add"])

    def _conv_mul(self, args):
        return self._apply_operator(args, I9738["mul"])

    def _apply_operator(self, args, operator_item):
        if len(args) == 2:
            arg1, arg2 = self._conv_object(args[0]), self._conv_object(args[1])
            return operator_item(arg1, arg2)

        elif len(args) > 2:
            new_args = (self._apply_operator(args[:2], operator_item), *args[2:])
            assert len(new_args) == len(args) - 1
            return self._apply_operator(new_args, operator_item)
        else:
            self._raise_error_invalid_length(len(args))


    def _raise_error_invalid_length(self, length):
        msg = f"unexpected length of arguments: {length} while converting expression {self.symb_expression}"
        raise p.aux.PyIRKError(msg)


def symbolic_expression_to_graph_expression(symb_expression):
    converter = symbolicExpressionToGraphExpressionConverter(symb_expression=symb_expression)
    return converter.convert()




# add knowledge elements of planar geometry (for Pythagorean theorem)

I1913 = p.create_item(
    R1__has_label="geometric object",
    R2__has_description="general (unspecified) geometric object",
    R3__is_subclass_of=p.I12["mathematical object"],
)


I7280 = p.create_item(
    R1__has_label="planar polygon",
    R2__has_description="base class for general planar polygons",
    R3__is_subclass_of=I1913["geometric object"],
)


I2917 = p.create_item(
    R1__has_label="planar triangle",
    R2__has_description="base class for general planar triangles",
    R3__is_subclass_of=I7280["planar polygon"],
)


I8172 = p.create_item(
    R1__has_label="polygon side",
    R2__has_description="base class for sides of a polygon",
    R3__is_subclass_of=I1913["geometric object"],
)


R2495 = p.create_relation(
    R1__has_label="has length",
    R2__has_description="specifies the length of a geometric object",
    R8__has_domain_of_argument_1=I1913["geometric object"],
    R11__has_range_of_result=p.I35["real number"],
    R22__is_functional=True,
)

I9148 = p.create_item(
    R1__has_label="get polygon sides ordered by length",
    R2__has_description="operator that returns a tuple of I8172__polygon_side instances",
    R4__is_instance_of=I4895["mathematical operator"],
    R8__has_domain_of_argument_1=I7280["planar polygon"],

    # TODO: find a way to specify this further (e.g. with qualifiers), because we know the type of the result
    # another idea: introduce a callable Item like I95["typed tuple"](I8172["polygon side"])
    R11__has_range_of_result=p.I33["tuple"],
)

I9148["get polygon sides ordered by length"].add_method(p.create_evaluated_mapping, "_custom_call")


def I9148_cc_pp(self, res, *args, **kwargs):
    """
    :param self:    mapping item (to which this function will be attached)
    :param res:     instance of I33["tuple"] (determined by R11__has_range_of_result)
    :param args:    arg tuple (<polygon>,) with which the mapping is called
    """
    assert len(args) == 1
    polygon = args[0]
    res.overwrite_statement("R1__has_label", f"sides-tuple of {polygon}")

    if p.is_instance_of(polygon, I2917["planar triangle"]):

        last_length = None
        for i, name in zip(range(3), ["a", "b", "c"]):
            # note: every assignment adds a new R39-statement
            side = p.instance_of(I8172["polygon side"], r1=name)
            side.R5__is_part_of = polygon

            length = p.instance_of(p.I35["real number"], r1=f"l_{name}")
            side.R2495__has_length = length
            res.R39__has_element = side

            if last_length is not None:
                # state that this length not less then the last one
                p.new_mathematical_relation(last_length, "<=", length)
            last_length = last_length
            p.core.Entity.set_relation
    else:
        raise p.aux.NotYetFinishedError("other types of polygons not yet supported")

    return res


I9148["get polygon sides ordered by length"].add_method(I9148_cc_pp, "_custom_call_post_process")



# <new_entities>

# this section in the source file is helpful for bulk-insertion of new items
# use it together with `pyirk --insert-keys-for-placeholders path/to/this_module.py`
# this will replace the `_newitemkey_` and `p.I000["..."]` strings accordingly
# see also pyirk --help

# _newitemkey_ = p.create_item(
#     R1__has_label="",
#     R2__has_description="",
#     R4__is_instance_of=p.I50["stub"],
#     R72__is_generally_related_to=p.I000["item specified by label"]
# )


#</new_entities>


p.end_mod()

"""

      R7280
      R1913
      R2917
      R8172
      R9148
      R9738
     R5916
I6117      R6117
I9192      R9192
I3648      R3648
      R6209
      R8492
      R1284
      R4218
      R2328
      R9489
      R4864
      R5094
       R2378
     R1716
      R9827
      R7151
      R7481
      R4291
      R5441
      R1778






"""
