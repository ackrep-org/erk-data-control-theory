import pyirk as p


# noinspection PyUnresolvedReferences
from ipydex import IPS, activate_ips_on_exception  # noqa

ma = p.irkloader.load_mod_from_path("./math1.py", prefix="ma")
ag = ma.ag


# todo: rename .scope("context") to .scope("setting")


__URI__ = "irk:/ocse/0.2/control_theory"

keymanager = p.KeyManager()
p.register_mod(__URI__, keymanager)
p.start_mod(__URI__)

I5948 = p.create_item(
    R1__has_label="dynamical system",
    R2__has_description="system with the capability to change over time, optionally with explicit input and/or output",
    R4__is_instance_of=p.I2["Metaclass"],  # this means: this Item is an ordinary class
)

I7641 = p.create_item(
    R1__has_label="general system model",
    R2__has_description="model of a dynamical system",
    R4__is_instance_of=p.I2["Metaclass"],
)

R7641 = p.create_relation(
    R1__has_label="has approximation",
    R2__has_description="object or class which is an approximation of a dynamical system",
    R8__has_domain_of_argument_1=I5948["dynamical system"],
    R11__has_range_of_result=I7641["general system model"],
)


I4466 = p.create_item(
    R1__has_label="Systems Theory",
    R2__has_description="academic field; might be regarded as part of applied mathematics",
    R4__is_instance_of=p.I3["Field of science"],
    R5__is_part_of=[p.I4["Mathematics"], p.I5["Engineering"]],
)

R1001 = p.create_relation(
    R1__has_label="studies", R2__has_description="object or class which an academic field studies"
)

I4466["Systems Theory"].set_relation(R1001["studies"], I5948["dynamical system"])


R4347 = p.create_relation(
    R1__has_label="has context",
    R2__has_description="establishes the context of a statement",
    # R8__has_domain_of_argument_1=I7723("general mathematical proposition"),
    # R11__has_range_of_result=<!! container of definition-items>
)

R4348 = p.create_relation(
    R1__has_label="has premise",
    R2__has_description="establishes the premise (if-part) of an implication",
    R8__has_domain_of_argument_1=p.I15["implication proposition"],
    # R11__has_range_of_result=<!! container of statements>
)

R4349 = p.create_relation(
    R1__has_label="has assertion",
    R2__has_description="establishes the assertion (then-part) of an implication",
    R8__has_domain_of_argument_1=p.I15["implication proposition"],
    # R11__has_range_of_result=<!! container of statements>
)


R9125 = p.create_relation(
    R1__has_label="has input dimension",
    R8__has_domain_of_argument_1=I7641["general system model"],
    R11__has_range_of_result=p.I38["non-negative integer"],
    R22__is_functional=True,
)

R8978 = p.create_relation(
    R1__has_label="has output dimension",
    R8__has_domain_of_argument_1=I7641["general system model"],
    R11__has_range_of_result=p.I38["non-negative integer"],
    R22__is_functional=True,
)

I1793 = p.create_item(
    R1__has_label="general model representation property",
    R2__has_description="general property of the representation of a model of a dynamical system \
        (not an intrinsic system property)",
    R4__is_instance_of=p.I54["mathematical property"],
)

I2928 = p.create_item(
    R1__has_label="general model representation",
    R2__has_description="general (mathematical) representation of a model of a dynamical system",
    R3__is_subclass_of=p.I12["mathematical object"],
)

R2928 = p.create_relation(
    R1__has_label="has model representation",
    R2__has_description="system model has a mathematical representation",
    R8__has_domain_of_argument_1=I7641["general system model"],
    R11__has_range_of_result=I2928["general model representation"],
)

R5100 = p.create_relation(
    R1__has_label="has model representation property",
    R2__has_description="model representation has mathematical property",
    R8__has_domain_of_argument_1=I2928["general model representation"],
    R11__has_range_of_result=I1793["general model representation property"],
)

R2279 = p.create_relation(
    R1__has_label="does not have model representation property",
    R2__has_description="model representation does not have mathematical property",
    R8__has_domain_of_argument_1=I2928["general model representation"],
    R11__has_range_of_result=I1793["general model representation property"],
)

I6886 = p.create_item(
    R1__has_label="general ode state space representation",
    R2__has_description="explicit ODE system description of a dynamical system",
    R3__is_subclass_of=I2928["general model representation"],
    # TODO: this has to use create_equation (to be implemented)
    R6__has_defining_mathematical_relation=p.create_expression(r"$\dot x = f(x, u)$"),
)

R2112 = p.create_relation(
    R1__has_label="has state dimension",
    R2__has_description="number of components of the state vector",
    R8__has_domain_of_argument_1=I6886["general ode state space representation"],
    R11__has_range_of_result=p.I38["non-negative integer"],
)

I6850 = p.create_item(
    R1__has_label="state space model representation",
    R2__has_description="explicit state space model of a dynamical system",
    R3__is_subclass_of=I6886["general ode state space representation"],
    # TODO: this has to use create_equation (to be implemented)
    R6__has_defining_mathematical_relation=p.create_expression(r"$\dot x = Ax + Bu$"),
    # TODO: Rule, system order = 1
)

R7178 = p.create_relation(
    R1__has_label="has number of degrees of freedom",
    R2__has_description=(
        "number of independent parameters that define its configuration in space; applicable to mechanical systems"
    ),
    R8__has_domain_of_argument_1=I7641["general system model"],
    R11__has_range_of_result=p.I38["non-negative integer"],
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/entity/Q2480745",
    # TODO: add formal comment to clarify the conflicting usages of language:
    # "degree of freedom" vs. "number of degrees of freedom"
)

I5356 = p.create_item(
    R1__has_label="general system property",
    R2__has_description="general property of a model of a dynamical system (not of its representation)",
    R4__is_instance_of=p.I2["Metaclass"],
)

R8303 = p.create_relation(
    R1__has_label="has general system property",
    R2__has_description="model has mathematical property",
    R8__has_domain_of_argument_1=I7641["general system model"],
    R11__has_range_of_result=I5356["general system property"],
)

R6458 = p.create_relation(
    R1__has_label="does not have general system property",
    R2__has_description="model does not have mathematical property",
    R8__has_domain_of_argument_1=I7641["general system model"],
    R11__has_range_of_result=I5356["general system property"],
)

I5357 = p.create_item(
    R1__has_label="differential flatness",
    R4__is_instance_of=I5356["general system property"],
    R2__has_description="differential flatness",
)

I5358 = p.create_item(
    R1__has_label="exact input-to-state linearizability",
    R4__is_instance_of=I5356["general system property"],
    # TODO: it might be necessary to restrict this to ode-state-space-systems
    R2__has_description="exact input-to-state linearizability (via static state feedback)",
)

I7178 = p.create_item(
    R1__has_label="local strong accessibility",
    R4__is_instance_of=I5356["general system property"],
    R2__has_description="local strong accessibility",
    # TODO: put this in relation to controllability
)

"""
def create_I5847():
    R1__has_label = "Equivalence of flat systems and exact input-to-state linearizable systems"
    R4__is_instance_of = c.I15["implication proposition"]
    R2__has_description = (
                             "Establishes that differentially flat systems and exact input-to-state linearizable systems "
                             "are equivalent in the SISO case"
                         )

    def R4347__has_context():
        ctx = c.Context()
        ctx.sys = c.generic_instance(I6886["general_ode_state_space_representation"])
        c.set_restriction(ctx.sys, R9125["has input dimension"], 1)
        return ctx

    def R4348__has_premise(ctx: c.Context):
        ctx.sys.R

    def R4349__has_assertion():
        pass

    return c.create_item_from_namespace()


I5847 = create_I5847()

"""


# attempt without writing code

I2640 = p.create_item(
    R1__has_label="transfer function representation",
    R2__has_description="...",
    R4__is_instance_of=p.I2["Metaclass"],
)

I5600 = p.create_item(
    R1__has_label="denominator",
    R2__has_description="denominator of some scalar mathematical term",
    R3__is_subclass_of=p.I42["scalar mathematical expression"]
)

R5323 = p.create_relation(
    R1__has_label="has denominator",
    R2__has_description="...",
    R8__has_domain_of_argument_1=p.I42["scalar mathematical expression"],
    R11__has_range_of_result=p.I42["scalar mathematical expression"],
)


R5334 = p.create_relation(
    R1__has_label="has representation",
    R2__has_description="relates an entity with an abstract mathematical representation",
    # R8__has_domain_of_argument_1= ...
    R11__has_range_of_result=p.I12["mathematical object"],
)


I8181 = p.create_item(
    R1__has_label="properness",
    R2__has_description=(
        "applicable to monovariate rational functions; "
        "satisfied if degree of denominator is not smaller than degree of numerator"
    ),
    R4__is_instance_of=p.I54["mathematical property"],
)

I8182 = p.create_item(
    R1__has_label="strict properness",
    R2__has_description="satisfied if degree of denominator is greater than degree of numerator",
    R17__is_subproperty_of=I8181["properness"],
)

# I7206 = p.create_item(
#     R1__has_label="system-dynamical property",
#     R2__has_description="base class for all system-dynamical properties",
#     R3__is_subclass_of=p.I54["mathematical property"],
# )

I7207 = p.create_item(
    R1__has_label="stability",
    R2__has_description="tendency to stay close to some distinguished trajectory (e.g. equilibrium)",
    R4__is_instance_of=p.I54["mathematical property"],
)

I7599 = p.create_item(
    R1__has_label="instability",
    R2__has_description="tendency to not stay close to some distinguished trajectory (e.g. equilibrium)",
    # TODO: description not ideal
    R4__is_instance_of=p.I54["mathematical property"],
    R43__is_opposite_of=I7207["stability"],
)

# todo: this entity should be made more precise whether it is global or local
I7208 = p.create_item(
    R1__has_label="BIBO stability",
    R2__has_description=(
        "'bounded-input bounded-output stability'; "
        "satisfied if the system responds to every bounded input signal with a bounded output signal"
    ),
    R17__is_subproperty_of=I7207["stability"],
)

I4975 = p.create_item(
    R1__has_label="general algebraic equation",
    R2__has_description="explicit algebraic equation",
    R3__is_subclass_of=p.I18["mathematical expression"],
    # TODO: this has to use create_equation (to be implemented)
    R6__has_defining_mathematical_relation=p.create_expression(r"$0 = f(x)$"),
)

I2865 = p.create_item(
    R1__has_label="differential algebraic system of equation",
    R2__has_description="system of differential algebraic equations representing a dynamical system",
    R3__is_subclass_of=I2928["general model representation"],
    R6__has_defining_mathematical_relation=p.create_expression(r"$0 = f(\dot{x}, x, t)$"),
    # TODO make connection to ode and algebraic equation
)

I2562 = p.create_item(
    R1__has_label="general property of pde",
    R2__has_description="general property of partial differential equations",
    R3__is_subclass_of=I1793["general model representation property"],
)

I6197 = p.create_item(
    R1__has_label="differential equation",
    R2__has_description="type of mathematical equation that involves derivatives",
    R3__is_subclass_of=p.I12["mathematical object"],
)

I8063 = p.create_item(
    R1__has_label="partial differential equation",
    R2__has_description="differential equation which contains derivatives w.r.t. more than one independent variable",
    R3__is_subclass_of=I6197["differential equation"],
)

R5718 = p.create_relation(
    R1__has_label="has general pde property",
    R2__has_description="pde has mathematical property",
    R8__has_domain_of_argument_1=I8063["partial differential equation"],
    R11__has_range_of_result=I2562["general property of pde"],
)

I9964 = p.create_item(
    R1__has_label="strict nonlinearity",
    R2__has_description="states that the pde",
    R17__is_subproperty_of=I2562["general property of pde"],
)

I2557 = p.create_item(
    R1__has_label="quasilinearity",
    R2__has_description="states that in a pde the highest order derivatives appear linearly, with their coefficients \
        being functions of the independent variables and their (lower order) derivatives",
    R17__is_subproperty_of=I2562["general property of pde"],
)

I3114 = p.create_item(
    R1__has_label="semilinearity",
    R2__has_description="states that in a pde the highest order derivatives appear linearly, with their coefficients \
        being functions of only the independent variables",
    R17__is_subproperty_of=I2557["quasilinearity"],
)

I3863 = p.create_item(
    R1__has_label="linearity",
    R2__has_description="states that in a pde the unknown function and all its derivatives appear linearly, with their coefficients \
        being functions of only the independent variables",
    R17__is_subproperty_of=I3114["semilinearity"],
)

I5325 = p.create_item(
    R1__has_label="Hurwitz polynomial",
    R2__has_description="monovariate polynomial of quadratic matrices",
    R3__is_subclass_of=ma.I4239["abstract monovariate polynomial"],
)

# <definition>
I4455 = p.create_item(
    R1__has_label="definition of Hurwitz polynomial",
    R2__has_description="the defining statement of what a Hurwitz polynomial is",
    R4__is_instance_of=p.I20["mathematical definition"],
)

with I4455.scope("setting") as cm:
    cm.new_var(P=p.uq_instance_of(ma.I4239["abstract monovariate polynomial"]))
    cm.new_var(set_of_roots=p.instance_of(ma.I5484["finite set of complex numbers"]))
    cm.new_rel(cm.P, ma.R1757["has set of roots"], cm.set_of_roots)


with I4455.scope("premise") as cm:
    cm.new_rel(cm.set_of_roots, p.R14["is subset of"], ma.I2739["open left half plane"])

with I4455.scope("assertion") as cm:
    # TODO: this should be something like p.R000["is instances of by definition"]
    cm.new_rel(cm.P, p.R30["is secondary instance of"], I5325["Hurwitz polynomial"])

I5325["Hurwitz polynomial"].set_relation(p.R37["has definition"], I4455["definition of Hurwitz polynomial"])
# </definition>


# TODO: open question should  I3007["stability theorem for a rational transfer function"] be constructed by using I5325["Hurwitz polynomial"]
# con: BIBO-stability might be meaningful also for transfer functions with non-polynomial denominators


# <theorem>
# todo this should be an equivalence instead of an implication
I3007 = p.create_item(
    R1__has_label="stability theorem for a rational transfer function",
    R2__has_description="establishes the relation between BIBO-Stability and the poles of the transfer function",
    R4__is_instance_of=p.I15["implication proposition"],
)

with I3007.scope("setting") as cm:
    cm.new_var(sys=p.uq_instance_of(I7641["general system model"]))

    cm.new_var(tf_rep=p.instance_of(I2640["transfer function representation"]))
    cm.new_var(denom=p.instance_of(ma.I4239["abstract monovariate polynomial"]))
    cm.new_var(set_of_poles=p.instance_of(ma.I5484["finite set of complex numbers"]))

    cm.new_rel(cm.sys, R5334["has representation"], cm.tf_rep)
    cm.new_rel(cm.tf_rep, R5323["has denominator"], cm.denom)
    cm.new_rel(cm.denom, ma.R1757["has set of roots"], cm.set_of_poles)

with I3007.scope("premise") as cm:
    cm.new_rel(cm.set_of_poles, p.R14["is subset of"], ma.I2739["open left half plane"])
    cm.new_rel(cm.tf_rep, p.R16["has property"], I8181["properness"])

with I3007.scope("assertion") as cm:
    cm.new_rel(cm.sys, p.R16["has property"], I7208["BIBO stability"])
# </theorem>


# todo: find the context of this and reformulate as IntegerRangeSequence
# p.Sequence("y", p._I000["time derivative of order i"], link_op=p._I000["listing"], start=0, stop="k")

# → it would be nice if one could interactively execute/write out such a sequence for given variable values


I4349 = p.create_item(
    R1__has_label="equivalence of flatness and input-state-linearizability for SISO systems",
    R2__has_description="establishes the equivalence of flatness and input-state-linearizability for SISO systems",
    R4__is_instance_of=p.I15["implication proposition"],
)

# </theorem>
# <statement preparation>
I2277 = p.create_item(
    R1__has_label="statement",
    R2__has_description=(
        "models an 'ordinary statement' e.g. of a publication which is not distinguished as a formal theorem"
    ),
    R3__is_subclass_of=p.I15["implication proposition"],
)

# </statement preparation>

# <statement>
# source: A software framework for embedded nonlinear model predictive control using a gradient‐based augmented Lagrangian approach (GRAMPC)
# source doi: https://doi.org/10.1007/s11081-018-9417-2

# this is still unfinished work in progress:
I4216 = p.create_item(
    R1__has_label="statement about MPC for linear systems and the reducibility to quadratic problems",
    R2__has_description=(
        "for linear systems, the MPC problem can be reduced to a quadratic problem, for which the optimal control"
        "over the admissible polyhedral set can be precomputed."
    ),
    R4__is_instance_of=I2277["statement"],
)


with I4216.scope("setting") as cm:
    cm.new_var(sys=p.instance_of(I5948["dynamical system"]))
    cm.new_var(state_space_sys=p.instance_of(I6886["general ode state space representation"]))
    cm.new_var(mpc_problem=p.instance_of(I5948["dynamical system"]))
    cm.new_var(quadratic_problem=p.instance_of(I5948["dynamical system"]))
    cm.new_var(mathematical_solution=p.instance_of(I5948["dynamical system"]))
    cm.new_var(optimal_control_law=p.instance_of(I5948["dynamical system"]))

    cm.new_rel(cm.mpc_problem, p.R000["refers to"], cm.sys)

with I4216.scope("premise") as cm:
    cm.new_rel(cm.sys, p.R000["refers to"], cm.sys)

with I4216.scope("assertion") as cm:
    cm.new_rel(cm.mpc_problem, p.R000["can be reduced to"], cm.quadratic_problem)

"""
Particularly for linear systems, the MPC problem can be reduced to a quadratic
problem, for which the optimal control over the admissible polyhedral set can be
precomputed.
"""

# </statement>

# defined in math because positive definiteness etc depends on it
assert ma.R5405["has associated state space"]
assert ma.I1168["point in state space"]


I9273 = p.create_item(
    R1__has_label="explicit first order ODE system",
    R2__has_description="system of explicit first order ordinary differential equations",
    R3__is_subclass_of=p.I12["mathematical object"],
    R41__has_required_instance_relation=ma.R5405["has associated state space"],
    # TODO: make explicit the relation to I6886["general ode state space representation"]
)

R4122 = p.create_relation(
    R1__has_label="has associated drift vector field",
    R2__has_description=(
        "specifies the associated drift vector field of the subject " "(e.g. a I9273__explicit...ode_system)"
    ),
    R8__has_domain_of_argument_1=I9273["explicit first order ODE system"],
    R11__has_range_of_result=ma.I9841["vector field"],
    R22__is_functional=True,
)

# add this relation to the required relations
I9273["explicit first order ODE system"].set_relation(
    p.R41["has required instance relation"], R4122["has associated drift vector field"]
)

I2753 = p.create_item(
    R1__has_label="flow of a vector field",
    R2__has_description="operator yielding the solution of the associated I9273__explicit_first_order_ODE_system",
    # this is an instance and not a subclass because there is only one flow operator
    R4__is_instance_of=p.I9["mathematical operation with arity 3"],
    R8__has_domain_of_argument_1=ma.I1168["point in state space"],
    R9__has_domain_of_argument_2=p.I35["real number"],
    R10__has_domain_of_argument_3=I9273["explicit first order ODE system"],
    R11__has_range_of_result=ma.I1168["point in state space"],
    # TODO: display and evaluate this notation
    # (\cdot_i) means: the i-th argument
    R13__has_canonical_symbol=r"$\varphi_{(\cdot_2)}^{(\cdot_3)}(\cdot_1)$",
)
# TODO: find a way to assign labels to the arguments: "initial value x", "time t", "vector field f"


I2075 = p.create_item(
    R1__has_label="substitution",
    R2__has_description=(
        "operator yielding an new expression where in expression arg1 the subexpression arg2 is replaced by arg3"
    ),
    R4__is_instance_of=p.I9["mathematical operation with arity 3"],
    R8__has_domain_of_argument_1=p.I18["mathematical expression"],
    R9__has_domain_of_argument_2=p.I18["mathematical expression"],
    R10__has_domain_of_argument_3=p.I18["mathematical expression"],
    R11__has_range_of_result=p.I18["mathematical expression"],
    R13__has_canonical_symbol=r"$\left.(\cdot_1)\left|_{(\cdot_2)=(\cdot_3)}$",
)


I1347 = p.create_item(
    R1__has_label="Lie derivative of scalar field",
    R2__has_description=(
        "mathematical operation wich maps a scalar field h_1 to a new scalar field h_2, depending on a vector field f; "
        "h2 can be interpreted as the time derivative of h_1 along the solution of the ode associated with f; "
        "in other words: along the flow of f"
    ),
    R4__is_instance_of=p.I8["mathematical operation with arity 2"],
    R8__has_domain_of_argument_1=ma.I9923["scalar field"],
    R9__has_domain_of_argument_2=ma.I9841["vector field"],
    # R10__has_domain_of_argument_3=ma.I1168["point in state space"],# todo remove argument
    R11__has_range_of_result=ma.I9923["scalar field"],
    R13__has_canonical_symbol=r"$L$",
    # TODO: complete defining equation
    ag__R6876__is_named_after=ag.I4853["Sophus Lie"],
)

# <definition>
I6229 = p.create_item(
    R1__has_label="definition of Lie derivative of scalar field",
    R2__has_description="the defining statement of a Lie derivative of a scalar field",
    R4__is_instance_of=p.I20["mathematical definition"],
)

with I6229["definition of Lie derivative of scalar field"].scope("setting") as cm:
    h = cm.new_var(h=p.uq_instance_of(ma.I9923["scalar field"]))
    M = cm.new_var(M=p.instance_of(ma.I5167["state space"]))
    n = cm.new_var(n=p.instance_of(p.I39["positive integer"]))

    cm.new_rel(cm.M, ma.R3326["has dimension"], cm.n)
    cm.new_rel(cm.h, ma.R5405["has associated state space"], cm.M)

    # TODO: this should be more specific (related to cm.M)
    # h.R8__has_domain_of_argument_1 = ma.I1168["point in state space"]
    # TODO: __automate_typing__
    # h.R11__has_range_of_result = p.I35["real number"]

    ode_sys = cm.new_var(ode_sys=p.instance_of(I9273["explicit first order ODE system"]))
    cm.new_rel(cm.ode_sys, ma.R5405["has associated state space"], cm.M)

    f = cm.new_var(f=p.instance_of(ma.I9841["vector field"]))
    cm.new_rel(cm.ode_sys, R4122["has associated drift vector field"], cm.f)

    x = cm.new_var(x=p.instance_of(ma.I1168["point in state space"]))

    # TODO: check

    cm.new_rel(cm.x, p.R15["is element of"], M)

    t = cm.new_var(t=p.instance_of(ma.I4122["independent variable"]))

    # TODO: __automate_typing__
    t.R30__is_secondary_instance_of = p.I35["real number"]

    # evaluate the mappings
    phi = I2753["flow of a vector field"](x, t, ode_sys)

    h_evaluated = h(phi)

    # TODO: __automate_typing__
    h_evaluated.R30__is_secondary_instance_of = p.I18["mathematical expression"]

    # perform the derivative
    deriv_evaluated = ma.derivative(h_evaluated, t)

    # some auxiliary expressions are stored as attributes of the parent item of the cm

    cm.item.subs = I2075["substitution"](deriv_evaluated, t, ma.I5000["scalar zero"])
    cm.item.L_evaluated = I1347["Lie derivative of scalar field"](h, f)


with I6229.scope("assertion") as cm:
    # TODO: encode the directional character of this equation (lhs := rhs)
    cm.new_equation(lhs=cm.L_evaluated(x), rhs=cm.subs)

I1347["Lie derivative of scalar field"].set_relation(
    p.R37["has definition"], I6229["definition of Lie derivative of scalar field"]
)
# </definition>


I1371 = p.create_item(
    R1__has_label="iterated Lie derivative of scalar field",
    R2__has_description="iterated version of I1347__Lie_derivative_of_scalar_field",
    R3__is_subclass_of=p.I9["mathematical operation with arity 3"],
    R8__has_domain_of_argument_1=ma.I9923["scalar field"],
    R9__has_domain_of_argument_2=ma.I9841["vector field"],
    R10__has_domain_of_argument_3=p.I38["non-negative integer"],
    R11__has_range_of_result=ma.I9923["scalar field"],
    # TODO: add defining equation
)

# <definition>
I8302 = p.create_item(
    R1__has_label="definition of iterated Lie derivative of scalar field",
    R2__has_description=("the defining statement of " "I1371['iterated Lie derivative of scalar field']"),
    R4__is_instance_of=p.I20["mathematical definition"],
)

with I8302["definition of iterated Lie derivative of scalar field"].scope("setting") as cm:
    n = cm.new_var(n=p.uq_instance_of(p.I39["positive integer"]))
    M = cm.new_var(M=p.uq_instance_of(ma.I5167["state space"]))
    h = cm.new_var(h=p.uq_instance_of(ma.I9923["scalar field"]))
    f = cm.new_var(f=p.uq_instance_of(ma.I9841["vector field"]))


# TODO: complete definition

# </definition>

# < Model Properties>

# reminder of already existing entities
assert I5356["general system property"]
assert I5357["differential flatness"]
assert I5358["exact input-to-state linearizability"]
assert p.R17["is subproperty of"]


I4101 = p.create_item(
    R1__has_label="general time variance",
    R2__has_description="states that the model of a dynamical system (i.e. its parameters) might change over time",
    R4__is_instance_of=I5356["general system property"],
)

I7733 = p.create_item(
    R1__has_label="time invariance",
    R2__has_description="states that the model of a dynamical system (i.e. its parameters) does not change over time",
    R4__is_instance_of=I5356["general system property"],
    R17__is_subproperty_of=I4101["general time variance"],
    R77__has_alternative_label="autonomy",
)


I9030 = p.create_item(
    R1__has_label="strict time variance",
    R2__has_description="states that the model of a dynamical system (i.e. its parameters) do change over time",
    R4__is_instance_of=I5356["general system property"],
    R17__is_subproperty_of=I4101["general time variance"],
    R43__is_opposite_of=I7733["time invariance"],
)

I9210 = p.create_item(
    R1__has_label="stabilizability",
    R2__has_description="states that for the model of a dynamical system there exists a state feedback such that the \
        system is stable",
    R4__is_instance_of=I5356["general system property"],
)

I7864 = p.create_item(
    R1__has_label="controllability",
    R2__has_description="states that the state of the model of a dynamical system can be changed from any arbitrary \
        starting state to any desired state in a finite amount of time using an external input",
    R4__is_instance_of=I5356["general system property"],
    R17__is_subproperty_of=I9210["stabilizability"],
)

I9853 = p.create_item(
    R1__has_label="detectability",
    R2__has_description="states that all unobservable state components of the model of a dynamical system are \
        stable",
    R4__is_instance_of=I5356["general system property"],
)

I3227 = p.create_item(
    R1__has_label="observability",
    R2__has_description="states that all state components of the model of a dynamical system can be reconstructed using\
        only information of the system outputs",
    R4__is_instance_of=I5356["general system property"],
    R17__is_subproperty_of=I9853["detectability"],
)

I3321 = p.create_item(
    R1__has_label="minimum phase",
    R2__has_description="states that the model of a dynamical system has stable zero dynamics",
    R4__is_instance_of=I5356["general system property"],
)

I2827 = p.create_item(
    R1__has_label="general nonlinearity",
    R2__has_description="states that the system model equations might not be linear",
    R4__is_instance_of=I1793["general model representation property"],
)

I6091 = p.create_item(
    R1__has_label="control affine",
    R2__has_description="states that in the system model equations the input only appears linearly",
    R4__is_instance_of=I1793["general model representation property"],
    R6__has_defining_mathematical_relation=p.create_expression(r"$\dot{x}=f(x)+g(x)u$"),
    R17__is_subproperty_of=I2827["general nonlinearity"],
)

I5247 = p.create_item(
    R1__has_label="polynomial",
    R2__has_description="states that the system model equations are polynomial w.r.t. the state components",
    R4__is_instance_of=I1793["general model representation property"],
    R17__is_subproperty_of=I6091["control affine"],
)

I4761 = p.create_item(
    R1__has_label="linearity",
    R2__has_description="states that the system model equations are linear",
    R4__is_instance_of=I1793["general model representation property"],
    R17__is_subproperty_of=I5247["polynomial"],
)

I1898 = p.create_item(
    R1__has_label="lti",
    R2__has_description="states that the system model is linear and time-invariant",
    R4__is_instance_of=I5356["general system property"],
    R17__is_subproperty_of=[I4761["linearity"], I7733["time invariance"]],
)

I4478 = p.create_item(
    R1__has_label="strict nonlinearity",
    R2__has_description="states that the system model equations are not linear",
    R4__is_instance_of=I1793["general model representation property"],
    R17__is_subproperty_of=I2827["general nonlinearity"],
    R43__is_opposite_of=I4761["linearity"],
)

I8978 = p.create_item(
    R1__has_label="time continuity",
    R2__has_description="states that the system is modeled continuously",
    R4__is_instance_of=I1793["general model representation property"],
)

I5031 = p.create_item(
    R1__has_label="time discreteness",
    R2__has_description="states that the system is modeled discretely",
    R4__is_instance_of=I1793["general model representation property"],
    R43__is_opposite_of=I8978["time continuity"],
)

I5718 = p.create_item(
    R1__has_label="autonomy",
    R2__has_description="states that the model of a dynamical system is autonomous",
    R4__is_instance_of=I5356["general system property"],
    # TODO rule with R9125["has input dimension"] 0
)

I5236 = p.create_item(
    R1__has_label="general trajectory property",
    R2__has_description="general property of a trajectory",
    R4__is_instance_of=p.I54["mathematical property"],
)

I7062 = p.create_item(
    R1__has_label="trajectory",
    R2__has_description="solution to a differential equation",
    R3__is_subclass_of=p.I12["mathematical object"],
)

R7062 = p.create_relation(
    R1__has_label="has general trajectory property",
    R2__has_description="trajectory has mathematical property",
    R8__has_domain_of_argument_1=I7062["trajectory"],
    R11__has_range_of_result=I5236["general trajectory property"],
)

R5031 = p.create_relation(
    R1__has_label="has trajectory",
    R2__has_description="object or class has a trajectory",
    R8__has_domain_of_argument_1=I7641["general system model"],
    R11__has_range_of_result=I7062["trajectory"],
)

I9820 = p.create_item(
    R1__has_label="equilibrium point",
    R2__has_description="constant solution to a differential equation",
    R3__is_subclass_of=I7062["trajectory"],
)

I1664 = p.create_item(
    R1__has_label="limit cycle",
    R2__has_description="closed trajectory which other trajectories spiral into or out of",
    R3__is_subclass_of=I7062["trajectory"],
)

R3898 = p.create_relation(
    R1__has_label="has system order",
    R2__has_description="highest time derivative present in the system equations",
    R8__has_domain_of_argument_1=I2928["general model representation"],
    R11__has_range_of_result=p.I38["non-negative integer"],
    R22__is_functional=True,
)

R6134 = p.create_relation(
    R1__has_label="has highest time derivative",
    R2__has_description="the highest time derivative occurring in the model equations",
    R8__has_domain_of_argument_1=I7641["general system model"],
    R11__has_range_of_result=p.I38["non-negative integer"],
    R22__is_functional=True,
)

# Lyapunov stability

I5082 = p.create_item(
    R1__has_label="local attractiveness",
    R2__has_description="states that all trajectories that start close enough to the trajectory in consideration will \
        converge to it",
    R4__is_instance_of=I5236["general trajectory property"],
)

I8059 = p.create_item(
    R1__has_label="global attractiveness",
    R2__has_description="states that all trajectories will converge to the trajectory in consideration",
    R4__is_instance_of=I5236["general trajectory property"],
    R17__is_subproperty_of=I5082["local attractiveness"],
)

I2931 = p.create_item(
    R1__has_label="local Lyapunov stability",
    R2__has_description="states that all trajectories that start close enough to the equilibrium will not leave a \
        certain neighborhood",
    R4__is_instance_of=I5236["general trajectory property"],
    R17__is_subproperty_of=I7207["stability"],
    ag__R6876__is_named_after=ag.I2151["Aleksandr Lyapunov"],
)

I8744 = p.create_item(
    R1__has_label="global Lyapunov stability",
    R2__has_description="states that all trajectories will not leave a certain neighborhood around the equilibrium",
    R4__is_instance_of=I5236["general trajectory property"],
    R17__is_subproperty_of=I2931["local Lyapunov stability"],
    ag__R6876__is_named_after=ag.I2151["Aleksandr Lyapunov"],
)

I4900 = p.create_item(
    R1__has_label="local asymptotic stability",
    R2__has_description="states that all trajectories that start close enough to the equilibrium remain close enough \
        and will converge to it",
    R4__is_instance_of=I5236["general trajectory property"],
    R17__is_subproperty_of=[I2931["local Lyapunov stability"], I5082["local attractiveness"]],
)

I5677 = p.create_item(
    R1__has_label="global asymptotic stability",
    R2__has_description="states that all trajectories remain close enough to the equilibrium and will converge to it",
    R4__is_instance_of=I5236["general trajectory property"],
    R17__is_subproperty_of=[
        I8744["global Lyapunov stability"],
        I8059["global attractiveness"],
        I4900["local asymptotic stability"],
    ],
)

I9642 = p.create_item(
    R1__has_label="local exponential stability",
    R2__has_description="states that an equilibrium is locally asymptotically stable and all trajectories converge at \
        least exponentially fast",
    R4__is_instance_of=I5236["general trajectory property"],
    R17__is_subproperty_of=I4900["local asymptotic stability"],
)

I5100 = p.create_item(
    R1__has_label="global exponential stability",
    R2__has_description="states that an equilibrium is globally asymptotically stable and all trajectories converge at \
        least exponentially fast",
    R4__is_instance_of=I5236["general trajectory property"],
    R17__is_subproperty_of=[I5677["global asymptotic stability"], I9642["local exponential stability"]],
)

I8303 = p.create_item(
    R1__has_label="strict Lyapunov instability",
    R2__has_description="states that some trajectories that start close enough to the equilibrium will still leave a \
        certain neighborhood",
    R4__is_instance_of=I5236["general trajectory property"],
    R43__is_opposite_of=I2931["local Lyapunov stability"],
    ag__R6876__is_named_after=ag.I2151["Aleksandr Lyapunov"],
)

I9304 = p.create_item(
    R1__has_label="knot",
    R2__has_description="states that the phase portrait forms a knot near the equilibrium point",
    R4__is_instance_of=I5236["general trajectory property"],
    # rule system order=2,
)

I6467 = p.create_item(
    R1__has_label="saddle",
    R2__has_description="states that the phase portrait forms a saddle near the equilibrium point",
    R4__is_instance_of=I5236["general trajectory property"],
    # rule system order=2,
    # TODO: Implement rule that saddle is always unstable
)


I4610 = p.create_item(
    R1__has_label="spiral",
    R2__has_description="states that the phase portrait forms a spiral near the equilibrium point",
    R4__is_instance_of=I5236["general trajectory property"],
    # rule system order=2,
)

I3241 = p.create_item(
    R1__has_label="chaotic behavior",
    R2__has_description="states that small deviations in the initial conditions result in qualitative changes in the \
        trajectory",
    R4__is_instance_of=I5236["general trajectory property"],
)

I1779 = p.create_item(
    R1__has_label="driftlessness",
    R2__has_description="states that the drift term of an input affine system is always 0",
    R4__is_instance_of=I1793["general model representation property"],
    R17__is_subproperty_of=I6091["control affine"],
)

I4131 = p.create_item(
    R1__has_label="domain",
    R2__has_description="area of research",
    R4__is_instance_of=p.I2["Metaclass"],
)

R8316 = p.create_relation(
    R1__has_label="belongs to domain",
    R2__has_description="states that the model of a dynamical system belongs to a specific domain",
    R8__has_domain_of_argument_1=I7641["general system model"],
    R11__has_range_of_result=I4131["domain"],
)

I4498 = p.create_item(
    R1__has_label="artificial domain",
    R2__has_description="domain containing research on the topic of artificial systems",
    R4__is_instance_of=I4131["domain"],
)

I7667 = p.create_item(
    R1__has_label="thermal domain",
    R2__has_description="domain containing research on the topic of thermodynamics",
    R4__is_instance_of=I4131["domain"],
)

I1052 = p.create_item(
    R1__has_label="electrical domain",
    R2__has_description="domain containing research on the topic of electrical systems",
    R4__is_instance_of=I4131["domain"],
)

I6203 = p.create_item(
    R1__has_label="chemical domain",
    R2__has_description="domain containing research on the topic of chemical systems",
    R4__is_instance_of=I4131["domain"],
)

I1696 = p.create_item(
    R1__has_label="physical domain",
    R2__has_description="domain containing research on the topic of physical systems (e.g. mechanical systems)",
    R4__is_instance_of=I4131["domain"],
)

I4931 = p.create_item(
    R1__has_label="biological domain",
    R2__has_description="domain containing research on the topic of biological systems",
    R4__is_instance_of=I4131["domain"],
)

I9223 = p.create_item(
    R1__has_label="mechanical domain",
    R2__has_description="domain containing research on the topic of mechanical systems",
    R3__is_subclass_of=I1696["physical domain"],
)

# general equation of linear second order pde with 2 independent variables
I2112 = p.instance_of(p.I18["mathematical expression"])
I2112.set_relation(
    p.R24["has LaTeX string"], r"$A(x,y)u_{xx} + 2B(x,y)u_{xy} + C(x,y)u_{yy} + f(x,y,u,u_x,u_y)$"
)

I1070 = p.new_equation(lhs=I2112, rhs=ma.I5000["scalar zero"])

I6963 = p.instance_of(p.I18["mathematical expression"])
I6963.set_relation(p.R24["has LaTeX string"], r"$B^2-AC$")

I2279 = p.new_mathematical_relation(lhs=I6963, rsgn="<", rhs=ma.I5000["scalar zero"])
I9769 = p.new_mathematical_relation(lhs=I6963, rsgn="==", rhs=ma.I5000["scalar zero"])
I6458 = p.new_mathematical_relation(lhs=I6963, rsgn=">", rhs=ma.I5000["scalar zero"])

I4704 = p.create_item(
    R1__has_label="hyperbolic",
    R2__has_description="b²-ac>0",
    R6__has_defining_mathematical_relation=I6458,
    R17__is_subproperty_of=I3863["linearity"],
    # rule system order=2,
)

I8844 = p.create_item(
    R1__has_label="parabolic",
    R2__has_description="b²-ac=0",
    R6__has_defining_mathematical_relation=I9769,
    R17__is_subproperty_of=I3863["linearity"],
    # rule system order=2,
)

I5239 = p.create_item(
    R1__has_label="elliptic",
    R2__has_description="b²-ac<0",
    R6__has_defining_mathematical_relation=I2279,
    R17__is_subproperty_of=I3863["linearity"],
    # rule system order=2,
)

I1892 = p.create_item(
    R1__has_label="boundary condition",
    R2__has_description="boundary condition of a pde",
    R4__is_instance_of=p.I12["mathematical object"],
)

R9746 = p.create_relation(
    R1__has_label="has boundary condition",
    R2__has_description="state that the pde has a specific boundary condition",
    R8__has_domain_of_argument_1=I8063["partial differential equation"],
    R11__has_range_of_result=I1892["boundary condition"],
)

# TODO: make a connection to system order >= 2 , consistency checking rule
I6830 = p.create_item(
    R1__has_label="Dirichlet boundary condition",
    R2__has_description="explicit specification of the values of the solution at the boundary of the domain",
    R3__is_subclass_of=I1892["boundary condition"],
)

I7095 = p.create_item(
    R1__has_label="Robin boundary condition",
    R2__has_description="explicit specification of a linear combination solution values and solution derivative values \
        at the boundary of the domain",
    R3__is_subclass_of=I1892["boundary condition"],
)

I3659 = p.create_item(
    R1__has_label="Neumann boundary condition",
    R2__has_description="explicit specification of the values of the derivative of the solution at the boundary of \
        the domain",
    R3__is_subclass_of=I1892["boundary condition"],
)

I8316 = p.create_item(
    R1__has_label="bifurcation",
    R2__has_description="states that a small change in the bifurcation parameter causes a qualitative change in the \
        systems trajectory",
    R3__is_subclass_of=I5356["general system property"],
    R6__has_defining_mathematical_relation=p.I23["equation"],
)

R2950 = p.create_relation(
    R1__has_label="has corresponding ackrep key",
    R2__has_description="...",
    R8__has_domain_of_argument_1=I7641["general system model"],
    R11__has_range_of_result=p.I52["string"],
    R22__is_functional=True,
)

I2699 = p.create_item(
    R1__has_label="general ackrep entity",
    R2__has_description="general ackrep entity",
    R4__is_instance_of=p.I2["Metaclass"],
)

I5919 = p.create_item(
    R1__has_label="problem specification",
    R2__has_description="type of ackrep entity",
    R3__is_subclass_of=I2699["general ackrep entity"],
)

I4635 = p.create_item(
    R1__has_label="problem solution",
    R2__has_description="type of ackrep entity",
    R3__is_subclass_of=I2699["general ackrep entity"],
)


# TODO: move ackrep-specific entities to own module
I1161 = p.create_item(
    R1__has_label="old tag",
    R2__has_description="",
    R3__is_subclass_of=p.I1["general item"],
)

R1070 = p.create_relation(
    R1__has_label="has old tag",
    R2__has_description="state that an ackrep entity has an old tag",
    R8__has_domain_of_argument_1=I2699["general ackrep entity"],
    R11__has_range_of_result=I1161["old tag"],
)


I2933 = p.create_item(
    R1__has_label="Lyapunov Function",
    R2__has_description="Class of scalar functions that may be used to prove the stability",
    R3__is_subclass_of=ma.I1063["scalar function"],
    ag__R6876__is_named_after=ag.I2151["Aleksandr Lyapunov"],
)


I5483 = p.create_item(
    R1__has_label="Control Lyapunov Function",
    R2__has_description="...",
    R3__is_subclass_of=ma.I1063["scalar function"],
    ag__R6876__is_named_after=ag.I2151["Aleksandr Lyapunov"],
)


I3369 = p.create_item(
    R1__has_label="Sontags formula",
    R2__has_description="...",
    R3__is_subclass_of=p.I18["mathematical expression"],
    ag__R6876__is_named_after=ag.I8430["Eduardo Daniel Sontag"],
    R72__is_generally_related_to=I5483["Control Lyapunov Function"],
)


I7916 = p.create_item(
    R1__has_label="pole placement",
    R2__has_description="control design method for LTI systems (explicitly specifying the roots of the CLCP)",
    R4__is_instance_of=p.I50["stub"],
)


I4201 = p.create_item(
    R1__has_label="Ackermanns Formula",
    R2__has_description="...",
    R3__is_subclass_of=p.I18["mathematical expression"],
    ag__R6876__is_named_after=ag.I2339["Jürgen Ackermann"],
    # TODO:
    R72__is_generally_related_to=I7916["pole placement"],
)


I6950 = p.create_item(
    R1__has_label="controller",
    R2__has_description="sub system of a dynamical system which is designed to impose desired behavior to the overall system",
    R4__is_instance_of=p.I50["stub"],
)


I5829 = p.create_item(
    R1__has_label="open loop controller", R2__has_description="", R3__is_subclass_of=I6950["controller"]
)


I1068 = p.create_item(
    R1__has_label="closed loop controller", R2__has_description="", R3__is_subclass_of=I6950["controller"]
)


I8048 = p.create_item(
    R1__has_label="control loop",
    R2__has_description="dynamical system consisting of components one of which is an I000__controller",
    R4__is_instance_of=p.I50["stub"],
)


I4023 = p.create_item(
    R1__has_label="plant",
    R2__has_description="subsystem of a I000__control_loop which is to be influenced by the I000__controller",
    R4__is_instance_of=p.I50["stub"],
)


I4596 = p.create_item(
    R1__has_label="feedback",
    R2__has_description="type of connection between subsystems of a dynamical system: input depends on output.",
    R4__is_instance_of=p.I50["stub"],
)


# TODO: align this with the topology of the default control loop (where the controller is not located in the backward path)
I9152 = p.create_item(
    R1__has_label="feedback law",
    R2__has_description="other word for controller",
    R4__is_instance_of=p.I50["stub"],
    # todo: formal relation to I6950["controller"], R77__alternative_label?
)


I9395 = p.create_item(
    R1__has_label="overshooting",
    R2__has_description="type of behavior of a dynamical system, for some excitation, wrt. some reference",
    R4__is_instance_of=p.I50["stub"],
)


I3506 = p.create_item(
    R1__has_label="undershooting",
    R2__has_description="type of behavior of a dynamical system, for some excitation, wrt. some reference",
    R4__is_instance_of=p.I50["stub"],
)


I5036 = p.create_item(
    R1__has_label="system quantity",
    R2__has_description="quantity (variable) that numerically describes some aspect of a dynamical system at a given time instant",
    R4__is_instance_of=p.I50["stub"],
)


I3573 = p.create_item(
    R1__has_label="input signal",
    R2__has_description="type of system quantity the numerical value of which is provided from outside of the system boundaries",
    R3__is_subclass_of=I5036["system quantity"],
)


I4741 = p.create_item(
    R1__has_label="measurable output signal",
    R2__has_description="type of system quantity the numerical value of which is available outside of the system boundaries",
    R3__is_subclass_of=I5036["system quantity"],
)


I5698 = p.create_item(
    R1__has_label="output signal to be controlled",
    R2__has_description="type of system quantity the numerical value of which is should be influenced (e.g. by the control facility)",
    R3__is_subclass_of=I5036["system quantity"],
)


I3432 = p.create_item(
    R1__has_label="SISO",
    R2__has_description="property of a dynamical system to have a single scalar input and a single scalar output",
    R4__is_instance_of=p.I50["stub"],
)


I7214 = p.create_item(
    R1__has_label="MIMO",
    R2__has_description="property of a dynamical system to have a multiple scalar inputs and a multiple scalar outputs",
    R4__is_instance_of=p.I50["stub"],
)


I6873 = p.create_item(
    R1__has_label="stabilization (feedback law)",
    R2__has_description="specialization of feedback law that achieves some sort of I7207__stability for a dynamical system",
    R3__is_subclass_of=I9152["feedback law"],
)


I2531 = p.create_item(
    R1__has_label="stabilization (effect)",
    R2__has_description=(
        "effect imposed on a dynamical system, e.g. by application of a feedback law or parameter change "
        "leading to property change from I7599__instability to I7207__stability"
    ),
    R4__is_instance_of=p.I50["stub"],
)


I9936 = p.create_item(
    R1__has_label="destabilization",
    R2__has_description=(
        "effect imposed on a dynamical system, e.g. by application of a feedback law or parameter change "
        "leading to property change I7207__stability to from I7599__instability"
    ),
    R4__is_instance_of=p.I50["stub"],
)


I4857 = p.create_item(
    R1__has_label="reference trajectory",
    R2__has_description="input signal of a closed control loop or a controller",
    R3__is_subclass_of=I3573["input signal"],
)


# TODO: allow multilinguality in create item
I5290 = p.create_item(
    R1__has_label="reference value",
    R1__has_label__de="Sollwert",
    R2__has_description="reference trajectory evaluated at some given time instant",
    R4__is_instance_of=p.I50["stub"],
)


I2108 = p.create_item(
    R1__has_label="noise", R2__has_description="stochastic signal", R4__is_instance_of=p.I50["stub"]
)



I1462 = p.create_item(
    R1__has_label="ordinary differential equation",
    R2__has_description="differential equation which contains only derivatives w.r.t. one variable",
    R3__is_subclass_of=I6197["differential equation"],
)


I9671 = p.create_item(
    R1__has_label="fractional order differential equation",
    R2__has_description="...",
    R3__is_subclass_of=I6197["differential equation"],
)

I8095 = p.create_item(
    R1__has_label="differential algebraic equation",
    R2__has_description="type of (vector valued) equation which contains both ode and algebraic components",
    R3__is_subclass_of=I6197["differential equation"],
)
# TODO: should there be a difference between scalar and vector valued equation?
# TODO: elaborate on the taxonomy (e.g. there could be combinations of pde, fractional, time delayed, dae-property)
# -> find a clever way to extend the taxonomy as needed

I3035 = p.create_item(
    R1__has_label="solution of a differential equation",
    R2__has_description="...",
    R4__is_instance_of=p.I50["stub"],
    R72__is_generally_related_to=I2753["flow of a vector field"],
)


# TODO: export to math
I2083 = p.create_item(
    R1__has_label="dimension",
    R2__has_description="...",
    R4__is_instance_of=p.I54["mathematical property"],
    R72__is_generally_related_to=ma.I5166["vector space"],
)


# TODO: introduce alternative lable: state quantity (Zustandsgröße@de)
I8679 = p.create_item(
    R1__has_label="state (of a dynamical system)",
    R2__has_description="",
    R4__is_instance_of=p.I50["stub"],
    R72__is_generally_related_to=ma.I1168["point in state space"],
)


I3554 = p.create_item(
    R1__has_label="state component",
    R2__has_description="one entry of the state vector of a state space system",
    R4__is_instance_of=p.I50["stub"],
    R5__is_part_of=I8679["state (of a dynamical system)"],
    R72__is_generally_related_to=I5036["system quantity"],
)


I8092 = p.create_item(
    R1__has_label="observer",
    R2__has_description="dynamical system which serves to estimate inner quantities of another dynamical system",
    R4__is_instance_of=p.I50["stub"],
    # TODO: introduce duality
    R72__is_generally_related_to=I6950["controller"],
)


I9199 = p.create_item(
    R1__has_label="strong Lyapunov Function",
    R2__has_description="Lyapunov function with a negative definite Lie Derivative",
    # TODO: evaluate wether R3 is a good relation here
    R3__is_subclass_of=I2933["Lyapunov Function"],  # TODO: is this a subclass of weak Lyapunov func?
    R77__has_alternative_label="strict Lyapunov Function",
)


I9208 = p.create_item(
    R1__has_label="weak Lyapunov Function",
    R2__has_description="Lyapunov function with a negative semidefinite Lie Derivative",
    # TODO: evaluate wether R3 is a good relation here
    R3__is_subclass_of=I2933["Lyapunov Function"],
    R77__has_alternative_label="non-strict Lyapunov Function",
)

# <theorem>
I4663 = p.create_item(
    R1__has_label="theorem for local Lyapunov stability of state space system",  # TODO this is one formulation among many
    R2__has_description=(
        "establishes a sufficient condition for the stability of an equilibrium point "
        "of a state space system"
    ),
    R4__is_instance_of=p.I15["implication proposition"],
    ag__R8439__is_described_by_source=ag.get_source_segment(ag.I7558["2002_Khalil"], "Section 4.1"),
)

with I4663["theorem for local Lyapunov stability of state space system"].scope("setting") as cm:
    # todo v needs to be continuous differentiable
    ode_sys = cm.new_var(ode_sys=p.uq_instance_of(I9273["explicit first order ODE system"]))
    # todo a similar theorem can be formulated for systems that do not fulfill these properties
    cm.new_rel(ode_sys, p.R16["has property"], I7733["time invariance"])
    cm.new_rel(ode_sys, p.R16["has property"], I5718["autonomy"])

    D = cm.new_var(D=p.instance_of(ma.I5167["state space"]))

    cm.new_rel(ode_sys, ma.R5405["has associated state space"], D)

    n = cm.new_var(n=p.instance_of(p.I39["positive integer"]))
    cm.new_rel(D, ma.R3326["has dimension"], n)

    x0 = cm.new_var(x0=p.instance_of(ma.I1168["point in state space"]))
    cm.new_rel(D, ma.R3798["has origin"], x0)
    # x = cm.new_var(x=p.instance_of(ma.I1168["point in state space"]))
    # cm.new_rel(x, p.R15["is element of"], D)
    u = cm.new_var(u=p.uq_instance_of(ma.I5843["neighborhood"]))
    cm.new_rel(u, ma.R4963["is neighborhood of"], x0)

    f = cm.new_var(f=p.instance_of(ma.I9841["vector field"]))
    cm.new_rel(ode_sys, R4122["has associated drift vector field"], f)

    V = cm.new_var(V=p.instance_of(ma.I9923["scalar field"]))

    cm.new_var(LfV=I1347["Lie derivative of scalar field"](V, f))

with I4663["theorem for local Lyapunov stability of state space system"].scope("premise") as cm:
    cm.new_rel(V, p.R16["has property"], ma.I3133["positive definiteness"], qualifiers=[ma.on_set(cm.u)])
    cm.new_rel(
        cm.LfV, p.R16["has property"], ma.I3137["negative semidefiniteness"], qualifiers=[ma.on_set(cm.u)]
    )

with I4663["theorem for local Lyapunov stability of state space system"].scope("assertion") as cm:
    # TODO: double check the meaning of global here @ca: global is wrong here
    cm.new_rel(cm.x0, p.R16["has property"], I2931["local Lyapunov stability"])
# </theorem>
V.set_relation(p.R30["is secondary instance of"], I9208["weak Lyapunov Function"])


# <theorem>
I8733 = p.create_item(
    R1__has_label="theorem for local asymptotic Lyapunov stability of state space system",
    R2__has_description=(
        "establishes a sufficient condition for the asymptotic stability of an equilibrium point "
        "of a states pace system"
    ),
    R4__is_instance_of=p.I15["implication proposition"],
    ag__R8439__is_described_by_source=ag.get_source_segment(ag.I7558["2002_Khalil"], "Section 4.1"),
)

with I8733["theorem for local asymptotic Lyapunov stability of state space system"].scope("setting") as cm:
    cm.copy_from(I4663["theorem for local Lyapunov stability of state space system"].get_subscope("setting"))
    V = cm.V

with I8733["theorem for local asymptotic Lyapunov stability of state space system"].scope("premise") as cm:
    cm.new_rel(cm.V, p.R16["has property"], ma.I3133["positive definiteness"], qualifiers=[ma.on_set(cm.u)])
    cm.new_rel(cm.LfV, p.R16["has property"], ma.I3136["negative definiteness"], qualifiers=[ma.on_set(cm.u)])

with I8733["theorem for local asymptotic Lyapunov stability of state space system"].scope("assertion") as cm:
    cm.new_rel(cm.x0, p.R16["has property"], I4900["local asymptotic stability"])
# </theorem>
V.set_relation(p.R30["is secondary instance of"], I9199["strong Lyapunov Function"])


# <theorem>
I2983 = p.create_item(
    R1__has_label="theorem for global asymptotic Lyapunov stability of state space system",
    R2__has_description=(
        "establishes a sufficient condition for the global asymptotic stability of the origin "
        "of a state space system"
    ),
    R4__is_instance_of=p.I15["implication proposition"],
    ag__R8439__is_described_by_source=ag.get_source_segment(ag.I7558["2002_Khalil"], "Section 4.1"),
)

with I2983["theorem for global asymptotic Lyapunov stability of state space system"].scope("setting") as cm:
    cm.copy_from(I4663["theorem for local Lyapunov stability of state space system"].get_subscope("setting"))

with I2983["theorem for global asymptotic Lyapunov stability of state space system"].scope("premise") as cm:
    cm.new_rel(cm.V, p.R16["has property"], ma.I3133["positive definiteness"], qualifiers=[ma.on_set(cm.D)])
    cm.new_rel(cm.LfV, p.R16["has property"], ma.I3136["negative definiteness"], qualifiers=[ma.on_set(cm.D)])
    cm.new_rel(cm.V, p.R16["has property"], ma.I5753["radially unboundedness"])

with I2983["theorem for global asymptotic Lyapunov stability of state space system"].scope("assertion") as cm:
    cm.new_rel(cm.x0, p.R16["has property"], I5677["global asymptotic stability"])

# </theorem>
V.set_relation(p.R30["is secondary instance of"], I9199["strong Lyapunov Function"])


I3503 = p.create_item(
    R1__has_label="input-to-state stability",
    R2__has_description=(
        "ISS; property is fulfilled if the control system is globally asymptotically stable "
        "in the absence of external inputs and if its trajectories are bounded by a function "
        "of the size of the input for all sufficiently large times. "
    ),
    R17__is_subproperty_of=I5677["global asymptotic stability"],
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/wiki/Q48995800",
    R72__is_generally_related_to=I7208["BIBO stability"],
)


I6994 = p.create_item(
    R1__has_label="Chetaev instability theorem",
    R2__has_description="",
    R4__is_instance_of=p.I15["implication proposition"],
    ag__R6876__is_named_after=ag.I1511["Nikolaï Gouryevitch Tchetaev"],
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/wiki/Q17006544",
    ag__R8439__is_described_by_source=ag.get_source_segment(ag.I7558["2002_Khalil"], "Theorem 4.4"),
)

I3303 = p.create_item(
    R1__has_label="attractor",
    R2__has_description="trajectory of a dynamical system to which other trajectories converge",
    R3__is_subclass_of=I7062["trajectory"],
)


I5106 = p.create_item(
    R1__has_label="repulsor",
    R2__has_description="trajectory of a dynamical system to which other trajectories converge in backward time",
    R43__is_opposite_of=I3303["attractor"],
    R3__is_subclass_of=I7062["trajectory"],
)


# TODO: add definition
I9875 = p.create_item(
    R1__has_label="region of attraction",
    R2__has_description=(
        "subset of a state space from which all trajectories converge towards an I3303__attractor"
    ),
    R4__is_instance_of=p.I13["mathematical set"],
    R72__is_generally_related_to=I3303["attractor"],
)


I9903 = p.create_item(
    R1__has_label="LaSalle's invariance principle",
    R2__has_description="establishes a sufficient condition for asymptotic stability",
    R4__is_instance_of=p.I15["implication proposition"],
    R72__is_generally_related_to=I5677["global asymptotic stability"],
    R77__has_alternative_label="Krasovskii-LaSalle principle",
    ag__R6876__is_named_after=[ag.I1257["Joseph Pierre LaSalle"]],  # I7934
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/wiki/Q3922068",
)

I9903.set_relation(p.R77["has alternative label"], "Barbashin-Krasovskii-LaSalle principle")
I9903.set_relation(ag.R6876["is named after"], ag.I7934["Nikolai Krasovsky"])


I6338 = p.create_item(
    R1__has_label="Lyapunov equation",
    R2__has_description="...",
    R3__is_subclass_of=p.I23["equation"],
    R8__has_domain_of_argument_1=ma.I9906["square matrix"],  # A
    R9__has_domain_of_argument_2=ma.I9906["square matrix"],  # P
    R10__has_domain_of_argument_3=ma.I9906["square matrix"],  # Q
    ag__R6876__is_named_after=ag.I2151["Aleksandr Lyapunov"],
)

# <theorem>
I3712 = p.create_item(
    R1__has_label="theorem on Lyapunov equation and Stability",
    R2__has_description="theorem characterizes asymptotic stability of the origin in terms of the solution of the "
    "Lyapunov equation",
    R4__is_instance_of=p.I17["equivalence proposition"],
    # H. K. Khalil, Nonlinear systems, Pearson new internat. ed., 3. ed. in Always learning. Harlow: Pearson Education, 2014.
    # Theorem 4.6
)

with I3712.scope("setting") as cm:
    n = cm.new_var(n=p.uq_instance_of(p.I39["positive integer"]))
    A = cm.new_var(A=p.instance_of(ma.I9906["square matrix"]))
    Q = cm.new_var(Q=p.instance_of(ma.I9906["square matrix"]))

    cm.new_rel(A, ma.R5938["has row number"], n)
    cm.new_rel(Q, ma.R5938["has row number"], n)

    cm.new_rel(Q, p.R16["has property"], ma.I3135["positive semidefiniteness"])  # todo matrix

    eig = cm.new_var(eig=p.instance_of(ma.I5484["finite set of complex numbers"]))
    cm.new_equation(eig, ma.I9160["set of eigenvalues of a matrix"](A))

with I3712.scope("premise") as cm:
    cm.new_rel(eig, p.R14["is subset of"], ma.I2739["open left half plane"])

with I3712.scope("assertion") as cm:
    P = cm.new_var(P=p.instance_of(ma.I9906["square matrix"], qualifiers=[p.exis_quant(True)]))
    cm.new_rel(P, ma.R5938["has row number"], n)
    cm.new_rel(P, p.R16["has property"], ma.I3648["positive definiteness (matrix)"])

    E = cm.new_equation(
        ma.I1536["matneg"](cm.Q),
        ma.I9493["matadd"](
            ma.I5177["matmul"](cm.P, cm.A), ma.I5177["matmul"](ma.I3263["transpose"](cm.A), cm.P)
        ),
    )

E.set_relation(p.R30["is secondary instance of"], I6338["Lyapunov equation"])

# </theorem>

I4432 = p.create_item(
    R1__has_label="Vannelli recursive algorithm to find Lyapunov function",
    R2__has_description=(""),
    R4__is_instance_of=ma.I9827["mathematical algorithm"],
    # R8__has_domain_of_argument_1=ma.I9841["vector field"], # f -> F_i
    # R9__has_domain_of_argument_2=ma.I9906["square matrix"], # R_2
    # R10__has_domain_of_argument_3=ma.I9906["square matrix"], # Q_1
    # todo how to deal with >3 inputs? nesting?
    # R11__has_range_of_result=p.I53["bool"], #todo this is done in parent class, sufficient?
    # A. Vannelli and M. Vidyasagar, “Maximal Lyapunov Functions and Domains of Attraction for Autonomous Nonlinear
    # Systems,” Automatica, vol. 21, no. 1, pp. 69–60, 1985, doi: https://doi.org/10.1016/0005-1098(85)90099-8.
)


# <theorem>
I8142 = p.create_item(
    R1__has_label="theorem by Vannelli for Lyapunov functions for homogeneous systems",
    R2__has_description=(
        "use a recursive algorithm to find Lyapunov functions for systems that are the sum of homogeneous functions"
    ),
    R4__is_instance_of=p.I15["implication proposition"],
    # A. Vannelli and M. Vidyasagar, “Maximal Lyapunov Functions and Domains of Attraction for Autonomous Nonlinear
    # Systems,” Automatica, vol. 21, no. 1, pp. 69–60, 1985, doi: https://doi.org/10.1016/0005-1098(85)90099-8.
    # Theorem 4
)


with I8142["theorem by Vannelli for Lyapunov functions for homogeneous systems"].scope("setting") as cm:
    sys = cm.new_var(sys=p.instance_of(I7641["general system model"]))
    cm.sys.set_relation(R8303["has general system property"], I7733["time invariance"])
    state_space_sys = cm.new_var(
        state_space_sys=p.instance_of(I6886["general ode state space representation"])
    )
    sys.set_relation(R2928["has model representation"], state_space_sys)

    n = cm.new_var(n=p.instance_of(p.I39["positive integer"]))

    f = cm.new_var(f=p.instance_of(ma.I9841["vector field"]))
    cm.new_rel(state_space_sys, R4122["has associated drift vector field"], f)

    x = cm.new_var(x=p.instance_of(ma.I1168["point in state space"]))

    with ma.IntegerRangeElement(start=1, stop=ma.I4291["infinity"]) as i:
        F_i = cm.new_var(F_i=p.instance_of(ma.I9841["vector field"]))
        # F_i is a vector of polynomials of degree i
        evaluated_F_i = cm.new_var(F_i_x=p.instance_of(ma.I7151["vector"]))
        cm.new_equation(F_i(x), evaluated_F_i)
        cm.new_rel(
            evaluated_F_i, p.R16["has property"], ma.I1778["homogeneity"]
        )  # todo does this apply to Fi or Fi_x?
        with ma.IntegerRangeElement(start=1, stop=n) as j:
            # F_ij is the j-th element of a vector of polynomials of degree i
            evaluated_F_ij = cm.new_var(
                evaluated_F_ij=p.instance_of(ma.I4239["abstract monovariate polynomial"])
            )
            cm.new_equation(ma.I3589["monovariate polynomial degree"](evaluated_F_ij), i)

    cm.new_equation(
        f(x), ma.I5441["sum over index"](evaluated_F_i, i, ma.I5440["limits"](ma.I5001["scalar one"], ma.I4291["infinity"]))
    )

    D = cm.new_var(M=p.instance_of(ma.I5167["state space"]))
    cm.new_rel(D, ma.R3326["has dimension"], n)
    cm.new_rel(state_space_sys, ma.R5405["has associated state space"], D)

    x0 = cm.new_var(x0=p.instance_of(ma.I1168["point in state space"]))
    cm.new_rel(D, ma.R3798["has origin"], x0)

    cm.new_rel(x0, R5031["has trajectory"], I9820["equilibrium point"])

    Q = cm.new_var(Q=p.instance_of(ma.I9906["square matrix"]))
    cm.new_rel(Q, p.R16["has property"], ma.I3133["positive definiteness"])

with I8142["theorem by Vannelli for Lyapunov functions for homogeneous systems"].scope("premise") as cm:
    F1 = cm.new_var(F1=p.instance_of(ma.I9841["vector field"]))  # todo relation to F_i with i=1 ??
    A = cm.new_var(A=p.instance_of(ma.I9906["square matrix"]))
    cm.new_equation(A, ma.I7481["Jacobian"](F1))

    # linearized system is asymptotically stable
    eig = cm.new_var(eig=p.instance_of(ma.I5484["finite set of complex numbers"]))
    cm.new_equation(eig, ma.I9160["set of eigenvalues of a matrix"](A))
    cm.new_rel(eig, p.R14["is subset of"], ma.I2739["open left half plane"])

    # recursive equations are satisfied
    cm.new_equation(I4432["Vannelli recursive algorithm to find Lyapunov function"], True)


with I8142["theorem by Vannelli for Lyapunov functions for homogeneous systems"].scope("assertion") as cm:
    # there exists an algorithm to iteratively calculate Lyapunov function
    cm.new_var(V=p.instance_of(I2933["Lyapunov Function"], qualifiers=[p.exis_quant(True)]))
    cm.new_rel(I4432["Vannelli recursive algorithm to find Lyapunov function"], ma.R3263["has solution"], V)

# </theorem>


# <theorem>
I4274 = p.create_item(
    R1__has_label="theorem by Goubault for Lyapunov functions for polynomial systems",
    R2__has_description=(
        "Find Darboux polynomials, calculate differential variants using Sum-Of-Squares, get Lyapunov function"
    ),
    R4__is_instance_of=p.I15["implication proposition"],
    # E. Goubault, J.-H. Jourdan, S. Putot, and S. Sankaranarayanan, “Finding non-polynomial positive invariants and
    # Lyapunov functions for polynomial systems through Darboux polynomials,” in 2014 American Control Conference,
    # Portland, OR, USA: IEEE, Jun. 2014, pp. 3571–3578. doi: 10.1109/ACC.2014.6859330.
)

I7006 = p.create_item(
    R1__has_label="Goubault algorithm to find Lyapunov function",
    R2__has_description=(
        "Algorithm to find Lyapunov Function. Find Darboux polynomials to the system of equations, find differential "
        "variant using Sum-Of-Squares programming, combine variants to construct a polynomial Lyapunov function"
    ),
    R4__is_instance_of=ma.I9827["mathematical algorithm"],
    # todo arguments?
    # R11__has_range_of_result=p.I53["bool"], #todo this is done in parent class, sufficient?
    # E. Goubault, J.-H. Jourdan, S. Putot, and S. Sankaranarayanan, “Finding non-polynomial positive invariants and
    # Lyapunov functions for polynomial systems through Darboux polynomials,” in 2014 American Control Conference,
    # Portland, OR, USA: IEEE, Jun. 2014, pp. 3571–3578. doi: 10.1109/ACC.2014.6859330.
)

with I4274["theorem by Goubault for Lyapunov functions for polynomial systems"].scope("setting") as cm:
    sys = cm.new_var(sys=p.instance_of(I7641["general system model"]))
    cm.sys.set_relation(R8303["has general system property"], I7733["time invariance"])
    rep = cm.new_var(rep=p.instance_of(I2928["general model representation"]))
    sys.set_relation(R2928["has model representation"], rep)
    cm.new_rel(rep, R5100["has model representation property"], I5247["polynomial"])

    n = cm.new_var(n=p.uq_instance_of(p.I39["positive integer"]))
    D = cm.new_var(M=p.instance_of(ma.I5167["state space"]))
    cm.new_rel(D, ma.R3326["has dimension"], n)
    cm.new_rel(rep, ma.R5405["has associated state space"], D)

    x0 = cm.new_var(x0=p.instance_of(ma.I1168["point in state space"]))
    cm.new_rel(D, ma.R3798["has origin"], x0)

    cm.new_rel(x0, R5031["has trajectory"], I9820["equilibrium point"])

with I4274["theorem by Goubault for Lyapunov functions for polynomial systems"].scope("premise") as cm:
    # find rational differential variants of Darboux polynomials
    # using sum of squares method
    # combine invariants to create a polynomial with 3 conditions
    # if solution to exists
    cm.new_equation(I7006["Goubault algorithm to find Lyapunov function"], True)

with I4274["theorem by Goubault for Lyapunov functions for polynomial systems"].scope("assertion") as cm:
    # polynomial is Lyapunov function
    cm.new_var(V=p.instance_of(I2933["Lyapunov Function"], qualifiers=[p.exis_quant(True)]))
    cm.new_rel(I7006["Goubault algorithm to find Lyapunov function"], ma.R3263["has solution"], V)
    pass

# </theorem>


# <theorem>
I2613 = p.create_item(
    R1__has_label="theorem for Lyapunov functions for linear systems",
    R2__has_description=("Construct a Lyapunov function by solving the Lyapunov Equation."),
    R4__is_instance_of=p.I17["equivalence proposition"],
)

with I2613["theorem for Lyapunov functions for linear systems"].scope("setting") as cm:
    sys = cm.new_var(sys=p.instance_of(I7641["general system model"]))
    ode_sys = cm.new_var(ode_sys=p.instance_of(I6850["state space model representation"]))
    cm.new_rel(sys, R2928["has model representation"], ode_sys)
    cm.new_rel(ode_sys, R5100["has model representation property"], I4761["linearity"])

    n = cm.new_var(n=p.instance_of(p.I39["positive integer"]))

    D = cm.new_var(M=p.instance_of(ma.I5167["state space"]))
    cm.new_rel(D, ma.R3326["has dimension"], n)

    cm.new_rel(ode_sys, ma.R5405["has associated state space"], D)

    x0 = cm.new_var(x0=p.instance_of(ma.I1168["point in state space"]))
    cm.new_rel(D, ma.R3798["has origin"], x0)
    x = cm.new_var(x=p.instance_of(ma.I1168["point in state space"]))
    cm.new_rel(x, p.R15["is element of"], D)

    A = cm.new_var(A=p.instance_of(ma.I9906["square matrix"]))
    Q = cm.new_var(Q=p.uq_instance_of(ma.I9906["square matrix"]))
    cm.new_rel(A, ma.R5938["has row number"], n)
    cm.new_rel(Q, ma.R5938["has row number"], n)
    Q.set_relation(p.R16["has property"], ma.I3648["positive definiteness (matrix)"])
    # TODO: rethink if this should be part of the premise
    # also: introduce set of positive definite matrices (dimension-dependency!)

    x_mat = ma.I9489["vector to matrix"](ma.I1284["point in vector space to vector"](cm.x))

    # specify f(x) = Ax
    f = cm.new_var(f=p.instance_of(ma.I9841["vector field"]))
    cm.new_rel(ode_sys, R4122["has associated drift vector field"], f)
    cm.new_equation(f(x), ma.I4218["matrix to vector"](ma.I5177["matmul"](A, x_mat)))


with I2613["theorem for Lyapunov functions for linear systems"].scope("premise") as cm:
    P = cm.new_var(P=p.instance_of(ma.I9906["square matrix"], qualifiers=[p.exis_quant(True)]))
    cm.new_rel(P, ma.R5938["has row number"], n)
    # TODO: this should be inferred by a rule
    cm.new_rel(P, ma.R5939["has column number"], n)
    cm.new_rel(cm.P, p.R16["has property"], ma.I3648["positive definiteness (matrix)"])

    # TODO: use convenient formula representation here
    E = cm.new_equation(
        ma.I1536["matneg"](cm.Q),
        ma.I9493["matadd"](
            ma.I5177["matmul"](ma.I3263["transpose"](cm.A), cm.P), ma.I5177["matmul"](cm.P, cm.A)
        ),
    )
    E.set_relation(p.R30["is secondary instance of"], I6338["Lyapunov equation"])

with I2613["theorem for Lyapunov functions for linear systems"].scope("assertion") as cm:
    cm.new_rel(cm.x0, p.R16["has property"], I5677["global asymptotic stability"])
    V = cm.new_var(V=p.instance_of(I9199["strong Lyapunov Function"]))

    # TODO: use convenient formula representation here
    cm.new_equation(
        V,
        ma.I2328["matrix to scalar"](
            ma.I5177["matmul"](ma.I5177["matmul"](ma.I3263["transpose"](x_mat), cm.P), x_mat)
        ),
    )
# </theorem>

# test system
# linear, but not explicitly time invariant
testreplin = p.instance_of(I2928["general model representation"])
testreplin.set_relation(R5100["has model representation property"], I4761["linearity"])
testsyslin = p.instance_of(I7641["general system model"])
testsyslin.set_relation(R2928["has model representation"], testreplin)

# LTI
testreplti = p.instance_of(I2928["general model representation"])
testreplti.set_relation(R5100["has model representation property"], I4761["linearity"])
testsyslti = p.instance_of(I7641["general system model"])
testsyslti.set_relation(R2928["has model representation"], testreplti)
testsyslti.set_relation(R8303["has general system property"], I7733["time invariance"])

# polynomial, time invariant
testreptipoly = p.instance_of(I2928["general model representation"])
testreptipoly.set_relation(R5100["has model representation property"], I5247["polynomial"])
testsystipoly = p.instance_of(I7641["general system model"])
testsystipoly.set_relation(R2928["has model representation"], testreptipoly)
testsystipoly.set_relation(R8303["has general system property"], I7733["time invariance"])

# only time invariant
testrepti = p.instance_of(I2928["general model representation"])
testsysti = p.instance_of(I7641["general system model"])
testsysti.set_relation(R2928["has model representation"], testrepti)
testsysti.set_relation(R8303["has general system property"], I7733["time invariance"])


# <theorem>
I6210 = p.create_item(
    R1__has_label="test theorem",
    R2__has_description=("test"),
    R4__is_instance_of=p.I17["equivalence proposition"],
)

with I6210["test theorem"].scope("setting") as cm:
    sys = cm.new_var(sys=p.instance_of(I7641["general system model"]))
    rep = cm.new_var(rep=p.instance_of(I2928["general model representation"]))
    cm.new_rel(sys, R2928["has model representation"], rep)
    cm.new_rel(rep, R5100["has model representation property"], I5247["polynomial"])


with I6210["test theorem"].scope("premise") as cm:
    cm.new_rel(rep, R5100["has model representation property"], I4761["linearity"])


with I6210["test theorem"].scope("assertion") as cm:
    V = cm.new_var(V=p.instance_of(I9199["strong Lyapunov Function"]))

# </theorem>


# Rules


# I4147 = p.create_item(
#     R1__has_label="link applicable theorems",
#     R2__has_description="...",
#     R4__is_instance_of=p.I47["constraint rule"], #todo type probably wrong
# )

# with I4147.scope("setting") as cm:
#     cm.new_var(sys=p.instance_of(I7641["general system model"]))
#     cm.new_var(rep=p.instance_of(I2928["general model representation"]))
#     cm.new_rel(cm.sys, R2928["has model representation"], cm.rep)

#     cm.new_var(th=p.instance_of(p.I14["mathematical proposition"]))
#     # cm.new_var(scope=p.instance_of(p.I16["scope"]))
#     # cm.new_var(premise=p.instance_of(p.I16["scope"]))
#     # cm.new_var(assertion=p.instance_of(p.I16["scope"]))

#     # cm.new_rel(cm.premise, p.R21["is scope of"], cm.th)
#     # cm.new_rel(cm.assertion, p.R21["is scope of"], cm.th)

#     cm.uses_external_entities(cm.rule)

# with I4147.scope("premise") as cm:
#     # cm.new_rel(cm.scope, p.R21["is scope of"], cm.th)
#     # theorem has to be about a system
#     # cm.new_var(sys_in_th=p.instance_of(I7641["general system model"]))
#     # cm.new_rel(cm.sys_in_th, p.R20["has defining scope"], cm.setting)
#     # system has to have a model rep
#     # cm.new_var(rep_in_th=p.instance_of(I2928["general model representation"]))
#     # cm.new_rel(cm.rep_in_th, p.R20["has defining scope"], cm.setting)

#     def cond_func(_, sys, rep, th):
#         # first argument (anchor item) can be ignored here

#         set, prem, ass = th.get_inv_relations("R21",return_subj=True)

#         setting_items = set.get_inv_relations("R20", return_subj=True)
#         systh = [i for i in setting_items if isinstance(i, p.Item) and p.is_instance_of(i, I7641["general system model"])]
#         if len(systh) != 1:
#             return False
#         systh = systh[0]
#         repth = [i for i in setting_items if isinstance(i, p.Item) and p.is_instance_of(i, I2928["general model representation"])]
#         if len(repth) != 1:
#             return False
#         repth = repth[0]

#         cond = True
#         # for each statement regarding sys in theorem
#         for statement in sum(systh.get_relations().values(), []):
#             # take only the property relations for now
#             if "property" in statement.relation.R1:
#                 rel_uri = statement.relation.uri
#                 obj = statement.object
#                 # make sure the systems has the same or more restrictive property as sys in th
#                 # if relation not existing -> False
#                 cond = cond and (len(sys.get_relations()[rel_uri]) > 0)
#                 for stm in sys.get_relations()[rel_uri]:
#                     if not p.is_subproperty(stm.object, obj):
#                         cond = False
#         # same for rep
#         for statement in sum(repth.get_relations().values(), []):
#             if "property" in statement.relation.R1:
#                 rel_uri = statement.relation.uri
#                 obj = statement.object
#                 cond = cond and (len(rep.get_relations()[rel_uri]) > 0)
#                 for stm in rep.get_relations()[rel_uri]:
#                     if not p.is_subproperty(stm.object, obj):
#                         cond = cond and False


#         return cond

#     cm.new_condition_func(cond_func, cm.sys, cm.rep, cm.th)


# def create_applies_to_relation(anchor_item, rule, sys, th):
#     res = p.RuleResult()
#     res.new_statements.append(th.set_relation(p.R80["applies to"], sys))


#     return res

# with I4147.scope("assertion") as cm:
#     cm.new_consequent_func(create_applies_to_relation, cm.rule, cm.sys, cm.th)


def apply_theorems_to_systems():
    import itertools

    theorems = p.get_all_instances_of(p.I14["mathematical proposition"])
    systems = p.get_all_instances_of(I7641["general system model"])

    def cond_func(sys, rep, th):
        # Note: most sys items here will be the systems created in the scope of a theorem. matching those doesn't make sense.
        # they have to be filtered out first
        # sys is from a setting scope:
        if sys.get_relations("R20"):
            if sys.get_relations("R20", return_obj=True)[0].R64 == "SETTING":
                return False

        scopes = th.get_inv_relations("R21", return_subj=True)
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
        systh = [
            i
            for i in setting_items
            if isinstance(i, p.Item) and p.is_instance_of(i, I7641["general system model"])
        ]
        if len(systh) != 1:
            return False
        systh = systh[0]

        repth = [
            i
            for i in setting_items
            if isinstance(i, p.Item) and p.is_instance_of(i, I2928["general model representation"])
        ]
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

        rep = sys.get_relations("irk:/ocse/0.2/control_theory#R2928", return_obj=True)
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


# ----------------------------------------------------------------------------------------------------------------------
apply_theorems_to_systems()


I5073 = p.create_item(
    R1__has_label="create I48__constraint_violation for is_opposite_of relation",
    R2__has_description="...",
    R4__is_instance_of=p.I47["constraint rule"],
)

with I5073.scope("setting") as cm:
    cm.new_var(x=p.instance_of(p.I1["general item"]))
    cm.new_var(prop1=p.instance_of(p.I11["general property"]))
    cm.new_var(prop2=p.instance_of(p.I11["general property"]))

    cm.uses_external_entities(cm.rule)

with I5073.scope("premise") as cm:
    # todo check also for subrelations like R16 - R7062
    cm.new_rel(cm.x, p.R16["has property"], cm.prop1)
    cm.new_rel(cm.x, p.R16["has property"], cm.prop2)

    def cond_func(_, prop1, prop2):
        # first argument (anchor item) can be ignored here
        cond = prop1.R43 and prop1.R43[0] == prop2
        return cond

    cm.new_condition_func(cond_func, cm.prop1, cm.prop2)


def create_constraint_violation_item(anchor_item, main_arg, rule, prop1, prop2):

    res = p.RuleResult()
    cvio: p.Item = p.instance_of(p.I48["constraint violation"])
    res.new_entities.append(cvio)
    res.new_statements.append(cvio.set_relation(p.R76["has associated rule"], rule))
    res.new_statements.append(main_arg.set_relation(p.R74["has constraint violation"], cvio))
    res.prop1 = prop1
    res.prop2 = prop2

    return res


with I5073.scope("assertion") as cm:
    cm.new_consequent_func(create_constraint_violation_item, cm.x, cm.rule, cm.prop1, cm.prop2)

# res = p.ruleengine.apply_semantic_rule(I4147, __URI__)
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


# </new_entities>


"""


      R5600
I8026      R8026
I5536      R5536
I4703      R4703
I6660      R6660
I9594      R9594
I2975      R2975
I6204      R6204
I9015      R9015
I8509      R8509
I5288      R5288
I4766      R4766
      R4147
      R6210
      R1775
      R7006
      R4432
      R8142






R9820
R1664
R5236
R9642
R4900
R5082
R2931
"""

"""
key reservoir C
I9987
I6548
I6189





"""

p.end_mod()
