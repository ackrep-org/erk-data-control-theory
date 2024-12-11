"""
created: 2022-11-30
original author Carsten Knoll <firstname.lastname@tu-dresden.de>

This module collects knowledge about people and institutions related to control theory. It thus contains personal data,
however only such which is considered to be publicly available already elsewhere (e.g. institution websites, wikidata).

If you want to be deleted from or added to this file please create a pull-request (preferred) or contact the author(s).
"""

import pyirk as p


__URI__ = "irk:/ocse/0.2/agents"

keymanager = p.KeyManager(keyseed=1239)
p.register_mod(__URI__, keymanager)
p.start_mod(__URI__)


R7781 = p.create_relation(
    R1__has_label="has family name",
    R2__has_description="part of the full name of a person",
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/wiki/Property:P734",
)


R7782 = p.create_relation(
    R1__has_label="has given name",
    R2__has_description="first name or another given name of this person",
    R18__has_usage_hint=[
        "this relation is non-functional, i.e. a person can have multiple given names; order matters",
        "if given name is unknown, it is acceptable to use initials here",
    ],
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/wiki/Property:P735",
)


R3474 = p.create_relation(
    R1__has_label="has ORCID",
    R2__has_description="specifies the orcid of a researcher",
    R18__has_usage_hint="This can be used if no wikidata entry is yet available",
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/wiki/Property:P496",
)


R3475 = p.create_relation(
    R1__has_label="has DBLP author ID",
    R2__has_description="specifies the DBLP author ID of a researcher",
    R18__has_usage_hint="This can be used if neither wikidata nor ORCID is yet available",
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/wiki/Property:P2456",
)


I7435 = p.create_item(
    R1__has_label="human",
    R2__has_description="human being",
    R4__is_instance_of=p.I2["Metaclass"],
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/entity/Q5",
)


def create_person(given_name: str, family_name: str, r2: str, r33=None, r3474=None, r3475=None):
    """
    This is a convenience function that simplifies the creation of items for humans
    """
    item_key = p.get_key_str_by_inspection()

    r1 = f"{given_name} {family_name}"
    item: p.Item = p.create_item(
        item_key,
        R1__has_label=r1,
        R2__has_description=r2,
        R4__is_instance_of=I7435["human"],
        R7781__has_family_name=family_name,
        R7782__has_given_name=given_name,
    )

    if r33:
        assert isinstance(r33, str)
        item.set_relation(p.R33["has corresponding wikidata entity"], r33)
    if r3474:
        assert isinstance(r3474, str)
        item.set_relation(R3474["has ORCID"], r3474)
    if r3475:
        assert isinstance(r3475, str)
        item.set_relation(R3475["has DBLP author ID"], r3475)

    return item


I2746 = create_person("Rudolf", "Kalman", "electrical engineer and mathematician")


I1342 = p.create_item(
    R1__has_label="academic institution",
    R2__has_description="educational institution dedicated to education and research",
    R4__is_instance_of=p.I2["Metaclass"],
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/entity/Q4671277",
)


I9942 = p.create_item(
    R1__has_label="Stanford University",
    R2__has_description="private research university in California, USA",
    R4__is_instance_of=I1342["academic institution"],
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/entity/Q41506",
)


I7301 = p.create_item(
    R1__has_label="ETH Zürich",
    R2__has_description="Swiss Federal Institute of Technology in Zürich",
    R4__is_instance_of=I1342["academic institution"],
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/entity/Q11942",
)


R1833 = p.create_relation(
    R1__has_label="has employer",
    R2__has_description="specifies for which entity (organization/person) the subject works",
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/entity/P108",
)


# the following is for testing qualifiers:

start_time = p.QualifierFactory(p.R48["has start time"])
end_time = p.QualifierFactory(p.R49["has end time"])

I2746["Rudolf Kalman"].set_relation(
    R1833["has employer"], I9942["Stanford University"], qualifiers=[start_time("1964"), end_time("1971")]
)


I2746["Rudolf Kalman"].set_relation(
    R1833["has employer"], I7301["ETH Zürich"], qualifiers=[start_time("1973"), end_time("1997")]
)

I4720 = create_person("Klaus", "Röbenack", "electrical engineer and mathematician")

I8124 = create_person("Carsten", "Knoll", "engineer and researcher")
I8124.set_relation(p.R33["has corresponding wikidata entity"], "http://www.wikidata.org/entity/Q110983632")


I2478 = p.create_item(
    R1__has_label="TU Dresden",
    R2__has_description="Dresden University of Technology",
    R4__is_instance_of=I1342["academic institution"],
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/entity/Q158158",
)


I2276 = create_person("Aurel", "Stodola", "Slovak scientist")
I2276.set_relation("R33__has_corresponding_wikidata_entity", "https://www.wikidata.org/entity/Q666875")


R6876 = p.create_relation(
    R1__has_label="is named after",
    R2__has_description="specifies that the subject is an eponym named after the object",
    R33__has_corresponding_wikidata_entity="https://www.wikidata.org/entity/P138",
)


I2151 = create_person("Aleksandr", "Lyapunov", "mathematician and physicist")
I2151.set_relation(p.R33["has corresponding wikidata entity"], "https://www.wikidata.org/wiki/Q310788")

I1257 = create_person(
    "Joseph Pierre", "LaSalle", "mathematician", r33="https://www.wikidata.org/wiki/Q15455952"
)

I8430 = create_person(
    "Eduardo Daniel", "Sontag", "mathematician", r33="https://www.wikidata.org/wiki/Q3709600"
)

I7906 = create_person("Rudolf", "Lipschitz", "mathematician", r33="https://www.wikidata.org/wiki/Q77322")

I4853 = create_person("Sophus", "Lie", "mathematician", r33="https://www.wikidata.org/wiki/Q30769")

I7115 = create_person("Michel", "Fliess", "computer scientist", r33="https://www.wikidata.org/wiki/Q3309635")

I3474 = create_person("Joachim", "Rudolph", "engineer", r3474="https://orcid.org/0000-0001-8402-2458")

I8885 = create_person("Frank", "Allgöwer", "engineer", r33="https://www.wikidata.org/wiki/Q1238632")

I1639 = create_person("Frank", "Woittennek", "engineer", r3474="https://orcid.org/0000-0001-8268-9582")

I9437 = create_person("Albrecht", "Gensior", "engineer", r3474="https://orcid.org/0000-0002-4276-6819")

I1635 = create_person("Johannes", "Reuter", "engineer", r3474="https://orcid.org/0000-0003-2069-5682")

I5667 = create_person("Kathrin", "Flaßkamp", "engineer", r3474="https://orcid.org/0000-0001-5983-1907")

I8521 = create_person("Jan", "Winkler", "engineer", r3474="https://orcid.org/0000-0001-9499-0030")

I3973 = create_person("Kurt", "Schlacher", "engineer", r3474="https://orcid.org/0000-0002-9497-8258")

I7642 = create_person("Hugues", "Mounier", "engineer", r3474="https://orcid.org/0000-0002-7069-3119")

I3749 = create_person("Gerta", "Zimmer", "engineer", r3475="https://dblp.org/pid/189/9499.html")

I3520 = create_person("Jörg", "Raisch", "engineer", r33="https://www.wikidata.org/wiki/Q107287703")

I1690 = create_person("Nicole", "Gehring", "engineer", r33="https://www.wikidata.org/wiki/Q60780539")

I3238 = create_person("Matthias", "Franke", "engineer", r33="https://www.wikidata.org/wiki/Q57423172")

I9404 = create_person("Kurt", "Reinschke", "engineer", r33="https://www.wikidata.org/wiki/Q106238929")

I2377 = create_person("Andreas", "Kugi", "engineer", r33="https://www.wikidata.org/wiki/Q102409925")

I6176 = create_person("Alberto", "Isidori", "control theorist", r33="https://www.wikidata.org/wiki/Q3608377")

I8526 = create_person("Jens", "Saak", "researcher", r33="https://www.wikidata.org/wiki/Q87670704")

I4329 = create_person("Jürgen", "Adamy", "researcher", r33="https://www.wikidata.org/wiki/Q99739075")

I7718 = create_person("Joachim", "Deutscher", "researcher", r3474="https://orcid.org/0000-0001-6596-6066")

I4722 = create_person("Knut", "Graichen", "researcher", r33="https://www.wikidata.org/wiki/Q102409924")

I6846 = create_person("Thomas", "Meurer", "researcher", r33="https://www.wikidata.org/wiki/Q60576394")

I7912 = create_person("Stefan", "Ecklebe", "engineer", r3474="https://orcid.org/0000-0002-4911-1233")

I3867 = create_person("Timm", "Faulwasser", "researcher", r33="https://www.wikidata.org/wiki/Q56426088")

I6334 = create_person("Rolf", "Findeisen", "researcher", r33="https://www.wikidata.org/wiki/Q56426090")

I4666 = create_person("Daniel", "Gerbet", "engineer", r3474="https://orcid.org/0000-0002-8527-8727")

I6725 = create_person("Claus", "Hillermeier", "engineer", r33="https://www.wikidata.org/wiki/Q112355168")

I9170 = create_person("Peter", "Hippe", "engineer", r3475="https://dblp.org/pid/20/7860.html")

I7086 = create_person("Abdurrahman", "Irscheid", "engineer", r3474="https://orcid.org/0000-0002-5913-2468")

I4786 = create_person("Paul", "Kotyczka", "engineer", r3474="https://orcid.org/0000-0002-6669-6368")

I3764 = create_person("Boris", "Lohmann", "engineer", r33="https://www.wikidata.org/wiki/Q59543808")

I8739 = create_person("Victor", "Lopez", "engineer", r3474="https://orcid.org/0000-0003-3989-4091")

I9992 = create_person("Matthias", "Müller", "engineer", r3474="https://orcid.org/0000-0002-4911-9526")

I4854 = create_person("Amine", "Othmane", "engineer", r3475="https://dblp.org/pid/306/0282.html")

I3431 = create_person("Karl", "Worthmann", "mathematician", r33="https://www.wikidata.org/wiki/Q102403582")

I1361 = create_person("Jens", "Wurm", "engineer", r3474="https://orcid.org/0000-0002-6760-7160")

I7328 = create_person("Julius", "Fiedler", "engineer", r3474="https://orcid.org/0009-0009-0163-9600")

I4258 = create_person(
    "Arjan", "van der Schaft", "control theorist", r33="https://www.wikidata.org/wiki/Q22280351"
)

I3191 = create_person("Volker", "Mehrmann", "control theorist", r33="mathematician")

I3820 = create_person("Lars", "Grüne", "researcher", r33="https://www.wikidata.org/wiki/Q102179115")

I4579 = create_person("Oliver", "Sawodny", "researcher", r3474="https://orcid.org/0000-0002-6910-2473")

I1373 = create_person(
    "Peter", "Eberhard", "mechanical engineer", r3474="https://www.wikidata.org/wiki/Q56514424"
)

I8599 = create_person("Jörg", "Fehr", "researcher", r33="https://www.wikidata.org/wiki/Q102440929")

I2682 = create_person("Moritz", "Schulze Darup", "researcher", r3474="https://orcid.org/0000-0002-1868-4098")

I4141 = create_person("Markus", "Schöberl", "researcher", r3474="https://orcid.org/0000-0001-7559-2619")

I1233 = create_person("Bernd", "Kolar", "researcher", r3474="https://orcid.org/0000-0001-9710-8445")

I6487 = create_person("Wolfgang", "Kemmetmüller", "researcher", r3474="https://orcid.org/0000-0001-7825-5917")

I4122 = create_person("Stefan", "Palis", "researcher", r3474="https://orcid.org/0000-0002-1941-2289")

I4024 = create_person("Lothar", "Kilz", "engineer", r3474="https://orcid.org/0000-0003-1219-8037")

I6943 = create_person("Matthias", "Konz", "engineer", r3474="https://orcid.org/0000-0003-3512-2297")

I9576 = create_person("Christoph", "Ament", "researcher", r3474="https://orcid.org/0000-0002-6396-4355")

I2705 = create_person("Arnim", "Kargl", "researcher", r3474="https://orcid.org/0009-0003-0824-339X")

I5642 = create_person("Alexander", "Schaum", "researcher", r33="https://www.wikidata.org/wiki/Q103830185")

I1479 = create_person("Veit", "Hagenmeyer", "researcher", r33="https://www.wikidata.org/wiki/Q92362390")

I6641 = create_person("Christian", "Bohn", "researcher", r3475="https://dblp.org/pid/26/3901.html")

I1974 = create_person("Julian", "Berberich", "researcher", r3474="https://orcid.org/0000-0001-6366-6238")

I3289 = create_person("Tobias", "Glück", "researcher", r3474="https://orcid.org/0000-0003-1497-6138")

I6284 = create_person("Andreas", "Völz", "researcher", r3474="https://orcid.org/0009-0006-2017-2389")

I6082 = create_person("Marcus", "Riesmeier", "researcher", r3475="https://dblp.org/pid/189/1747.html")

I6276 = create_person("Peter", "Benner", "researcher", r33="https://www.wikidata.org/wiki/Q26838423")

I9152 = create_person("Lutz", "Gröll", "researcher", r3475="https://dblp.org/pid/57/757.html")

I7867 = create_person("Harald", "Aschemann", "researcher", r3474="https://dblp.org/pid/13/1059.html")

I3511 = create_person("Miroslav", "Krstić", "researcher", r33="https://www.wikidata.org/wiki/Q6873980")

I4357 = create_person("Jean", "Lévine", "researcher", r33="https://www.wikidata.org/wiki/Q102162024")

I4657 = create_person("Pierre", "Rouchon", "researcher", r33="https://www.wikidata.org/wiki/Q102162023")

I8937 = create_person("Philippe", "Martin", "researcher", r33="https://www.wikidata.org/wiki/Q102396724")

I3477 = create_person("Michael", "Zeitz", "researcher", r33="https://www.wikidata.org/wiki/Q102337611")

I5057 = create_person("Ernst Dieter", "Gilles", "researcher", r33="https://www.wikidata.org/wiki/Q1357858")

I9833 = create_person("Richard", "Murray", "researcher", r33="https://www.wikidata.org/wiki/Q41048386")

I6533 = create_person("Maximilian", "Gerwien", "researcher", r3475="https://dblp.org/pid/258/0769.html")

I2973 = create_person("Jean-Jacques", "Slotine", "researcher", r33="https://www.wikidata.org/wiki/Q33197264")

I1906 = create_person("Mark W.", "Spong", "researcher", r33="https://www.wikidata.org/wiki/Q6770174")

I6139 = create_person("Robert", "Seifried", "researcher", r3474="https://orcid.org/0000-0001-5795-7610")

I6734 = create_person("John", "Baillieul", "researcher", r33="https://www.wikidata.org/wiki/Q19955733")

I5760 = create_person("Andrew David", "Lewis", "researcher", r33="https://www.wikidata.org/wiki/Q102312710")

I8789 = create_person("Muruhan", "Rathinam", "researcher", r33="https://www.wikidata.org/wiki/Q88336591")

I4402 = create_person(
    "S. Shankar", "Shankar", "researcher", r3475="https://dblp.org/pid/s/ShankarSastry.html"
)

I6309 = create_person("Giuseppe", "Oriolo", "researcher", r33="https://www.wikidata.org/wiki/Q50864904")

I4578 = create_person(
    "Henk",
    "Nijmeijer",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q102253589",
    r3475="https://dblp.org/pid/75/4680.html",
)

I1960 = create_person(
    "Witold",
    "Respondek",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q102231063",
    r3475="https://dblp.org/pid/36/4681.html",
)

I3772 = create_person(
    "Florentina",
    "Nicolau",
    "researcher",
    r3474="https://orcid.org/0000-0001-5580-8849",
    r3475="https://dblp.org/pid/143/6152.html",
)

I5575 = create_person(
    "Jan",
    "Lunze",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q1269292",
    r3475="https://dblp.org/pid/05/6089.html",
)

I5093 = create_person("Günter", "Ludyk", "researcher", r33="https://www.wikidata.org/wiki/Q56027049")

I2934 = create_person(
    "Gilmer L.",
    "Blankenship",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q102404879",
    r3475="https://dblp.org/pid/01/3786.html",
)

I6489 = create_person(
    "Harry",
    "Kwatny",
    "engineer",
    r33="https://www.wikidata.org/wiki/Q28086053",
    r3475="https://dblp.org/pid/86/4797.html",
)

I6490 = create_person("Klaus", "Janschek", "researcher", r3475="https://dblp.org/pid/70/5404.html")

I9650 = create_person(
    "Rolf",
    "Isermann",
    "engineer",
    r33="https://www.wikidata.org/wiki/Q1513529",
    r3475="https://dblp.org/pid/95/5975.html",
)

I1683 = create_person(
    "Malo L. J.",
    "Hautus",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q102205835",
    r3475="https://dblp.org/pid/33/2916.html",
)

I8855 = create_person(
    "Jan Camiel",
    "Willems",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q15429591",
    r3475="https://dblp.org/pid/54/2783.html",
)

I2288 = create_person(
    "Stefan",
    "Trenn",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q102354249",
    r3475="https://dblp.org/pid/77/8131.html",
)

I1760 = create_person("Otto", "Föllinger", "researcher", r33="https://www.wikidata.org/wiki/Q126359")

# TODO: https://en.wikipedia.org/wiki/Ackermann%27s_formula https://www.wikidata.org/wiki/Q42417197
I2339 = create_person("Jürgen", "Ackermann", "researcher", r3475="https://dblp.org/pid/03/8092.html")

I3142 = create_person("Tobias", "Zaiczek", "researcher", r3475="https://dblp.org/pid/75/11054.html")

I5404 = create_person("Klemens", "Fritzsche", "researcher", r3475="https://dblp.org/pid/190/6473.html")

I8157 = create_person(
    "Sunil K.",
    "Agrawal",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q27063027",
    r3475="https://dblp.org/pid/122/1844.html",
)

I5669 = create_person(
    "Rogelio",
    "Lozano",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q112404548",
    r3475="https://dblp.org/pid/25/3367.html",
)

I9439 = create_person(
    "Isabelle",
    "Fantoni",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q112404547",
    r3475="https://dblp.org/pid/37/1797.html",
)

I3991 = create_person(
    "Alessandro",
    "De Luca",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q88501421",
    r3475="https://dblp.org/pid/95/1233-1.html",
)

I5420 = create_person(
    "Giuseppe",
    "Conte",
    "researcher",
    r3474="https://orcid.org/0000-0001-6615-1539",
    r3475="https://dblp.org/pid/33/4439.html",
)

I8609 = create_person(
    "Claude H.",
    "Moog",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q102405059",
    r3475="https://dblp.org/pid/48/25.html",
)

I1360 = create_person(
    "Ravi N.",
    "Banavar",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q103370835",
    r3475="https://dblp.org/pid/44/5767.html",
)

I9849 = create_person(
    "Anna Maria",
    "Perdon",
    "researcher",
    r3474="https://orcid.org/0000-0001-5679-555X",
    r3475="https://dblp.org/pid/40/476.html",
)

I8033 = create_person(
    "Sriram",
    "Sankaranarayanan",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q93947056",
    r3474="https://orcid.org/0000-0001-7315-4340",
    r3475="https://dblp.org/pid/82/1542.html",
)

I9161 = create_person(
    "Olfa",
    "Boubaker",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q95603570",
    r3475="https://dblp.org/pid/45/9836.html",
)

# TODO: examine wikidata page (many useful properties)
I8259 = create_person(
    "Francesco",
    "Bullo",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q57020529",
    r3475="https://dblp.org/pid/39/6707.html",
)

I8905 = create_person("Andrea", "Bacciotti", "researcher", r3475="https://dblp.org/pid/25/6392.html")

I3512 = create_person("Marco", "Sabatini", "researcher", r3474="", r3475="https://dblp.org/pid/70/6163.html")

I7856 = create_person("Luisa", "Mazzi", "researcher", r3474="", r3475="https://dblp.org/pid/98/8143.html")

I1451 = create_person(
    "Christopher I.",
    "Byrnes",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q5591426",
    r3475="https://dblp.org/pid/47/1166.html",
)

I1324 = create_person(
    "Dennis S.",
    "Bernstein",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q68334606",
    r3475="https://dblp.org/pid/53/6254.html",
)

I8461 = create_person(
    "Anthony",
    "Bloch",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q102188472",
    r3475="https://dblp.org/pid/02/6645.html",
)

I1252 = create_person(
    "Roger W.",
    "Brockett",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q7359064",
    r3475="https://dblp.org/pid/47/3380.html",
)

I2026 = create_person(
    "Katsuhisa",
    "Furuta",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q18235077",
    r3475="https://dblp.org/pid/57/895.html",
)

I9169 = create_person(
    "Karl Johan",
    "Åström",
    "control theorist",
    r3474="https://www.wikidata.org/wiki/Q462685",
    r3475="https://dblp.org/pid/93/8098.html",
)

I7780 = create_person(
    "N. Harris",
    "McClamroch",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q102156340",
    r3475="https://dblp.org/pid/03/1935.html",
)

I9526 = create_person("Bodo", "Heimann", "researcher", r3475="https://dblp.org/pid/86/2842.html")

I9049 = create_person(
    "Kazuhiro",
    "Sato",
    "researcher",
    r3474="https://orcid.org/0000-0003-1895-6548",
    r3475="https://dblp.org/pid/86/806.html",
)

I1314 = create_person(
    "Petar V.",
    "Kokotovic",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q7171760",
    r3475="https://dblp.org/pid/77/2290.html",
)

I9005 = create_person(
    "Mrdjan",
    "Jankovic",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q102354678",
    r3475="https://dblp.org/pid/07/6166.html",
)

I7204 = create_person(
    "Rodolphe",
    "Sepulchre",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q86483928",
    r3475="https://dblp.org/pid/54/461.html",
)

I9543 = create_person("Felix", "Antritter", "researcher", r3475="https://dblp.org/pid/62/1221.html")

I5318 = create_person(
    "Michiel",
    "Van Nieuwstadt",
    "researcher",
    r3474="https://orcid.org/0000-0002-6100-422X",
    r3475="https://dblp.org/pid/202/5645.html",
)

I8560 = create_person("William A.", "Wolovich", "researcher", r3475="https://dblp.org/pid/27/5698.html")

I9336 = create_person(
    "George",
    "Labahn",
    "researcher",
    r33="https://www.wikidata.org/wiki/Q102271968",
    r3475="https://dblp.org/pid/l/GeorgeLabahn.html",
)

I1511 = create_person(
    "Nikolaï Gouryevitch", "Tchetaev", "mathematician", r33="https://www.wikidata.org/wiki/Q4514946"
)

I7934 = create_person("Nikolai", "Krasovsky", "mathematician", r33="https://www.wikidata.org/wiki/Q3710069")

# template for creating more entries (then use pyirk -ik)
# <new_entities>
# _newitemkey_ = create_person("", "", "researcher", r33="", r3475="")
# </new_entities>


I6591 = p.create_item(
    R1__has_label="source document",
    R2__has_description="type for items that represent books, papers etc",
    R4__is_instance_of=p.I2["Metaclass"],
)

R8433 = p.create_relation(
    R1__has_label="has authors",
    R2__has_description="...",
    R8__has_domain_of_argument_1=I6591["source document"],
    R11__has_range_of_result=I7435["human"],
)

R8434 = p.create_relation(
    R1__has_label="has title",
    R2__has_description="...",
    R8__has_domain_of_argument_1=I6591["source document"],
    R11__has_range_of_result=p.I19["language-specified string literal"],
)

R8435 = p.create_relation(
    R1__has_label="has year",
    R2__has_description="...",
    R8__has_domain_of_argument_1=I6591["source document"],
    R11__has_range_of_result=p.I37["integer number"],
)

R8436 = p.create_relation(
    R1__has_label="has DOI",
    R2__has_description="...",
    R8__has_domain_of_argument_1=I6591["source document"],
    R11__has_range_of_result=p.I52["string"],
)


def create_source(title: str, authors, year: int, doi: str = None):
    """
    This is a convenience function that simplifies the creation of a published source (paper, book, ...)
    """
    item_key = p.get_key_str_by_inspection()

    if not isinstance(authors, (list, tuple)):
        authors = [authors]

    for author in authors:
        assert isinstance(author, p.Item)
    assert len(authors) > 0

    first_authors_name = authors[0].R7781__has_family_name[0]
    if len(authors) > 1:
        suffix = "_etal"
    else:
        suffix = ""

    r1 = f"{year}_{first_authors_name}{suffix}"
    r2 = f"publication '{title}' by {first_authors_name}{suffix.replace('_', ' ')}"
    new_item: p.Item = p.create_item(
        item_key,
        R1__has_label=r1,
        R2__has_description=r2,
        R4__is_instance_of=I6591["source document"],
        R8433__has_authors=authors,
        R8434__has_title=title,
        R8435__has_year=year,
    )

    if doi:
        new_item.set_relation(R8436["hasDOI"], doi)
    return new_item


I9700 = create_person(
    "Hassan", "Khalil", "electrical engineer", r33="https://www.wikidata.org/wiki/Q102278369"
)

I7558 = create_source("Nonlinear Systems", I9700["Hassan Khalil"], 2002)


I7800 = p.create_item(
    R1__has_label="source segment",
    R2__has_description="type to represent a segment (chapter, section, ...) of an I6591__source_document instance",
    R4__is_instance_of=p.I2["Metaclass"],
)


R8437 = p.create_relation(
    R1__has_label="has segment specification",
    R2__has_description="...",
    R8__has_domain_of_argument_1=I7800["source segment"],
    R11__has_range_of_result=p.I52["string"],
)


SOURCE_SEGMENT_CACHE = {}


@p.wrap_function_with_search_uri_context
def get_source_segment(source_doc: p.Item, segment_specification: str):
    """
    :param segment_specification:   str, e.g. "Chapter 3" or "Section 2.5.2" or "Page 84"

    This is a convenience function which creates (or returns an existing) item
    representing a segment of a source document (section, chapter, page, ...)
    """

    r1 = f"{source_doc.R1__has_label} -- {segment_specification}"
    key = (source_doc.uri, segment_specification)
    if item := SOURCE_SEGMENT_CACHE.get(key):
        pass
    else:
        item = p.instance_of(I7800["source segment"], r1=r1)
        SOURCE_SEGMENT_CACHE[key] = item
        item.R8437__has_segment_specification = segment_specification
    return item


R8439 = p.create_relation(
    R1__has_label="is described by source",
    R2__has_description="specifies that the subject (e.g. a theorem) is described by some source document",
    R8__has_domain_of_argument_1=p.I46["knowledge artifact"],
    R11__has_range_of_result=[I7800["source segment"], I6591["source document"]],
)


p.end_mod()

"""
key reservoir created with: `pyirk -l agents1.py ag -nk 100`

I7934      R7934
I6514      R6514
I8469      R8469
I5543      R5543
I2792      R2792
I8019      R8019
I6589      R6589
I7064      R7064
I6656      R6656
I1928      R1928

I6009      R6009
I3563      R3563
I8388      R8388
I2175      R2175
I9157      R9157
I9661      R9661
I6612      R6612
I9318      R9318
I4247      R4247
I6854      R6854
I3131      R3131
I7191      R7191
I3791      R3791
I3963      R3963
I8266      R8266
I6860      R6860
I3806      R3806
I8337      R8337
I1969      R1969
I3088      R3088
I1173      R1173
I3948      R3948
I4757      R4757
I1943      R1943
I8189      R8189
I2777      R2777
I1236      R1236
I7447      R7447
I6181      R6181
I7364      R7364
I3552      R3552
I7965      R7965
I9438      R9438
I1098      R1098
I9216      R9216
I2888      R2888


"""
