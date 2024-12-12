# Ontology of Control Systems Engineering (OCSE)

This repo contains formally represented knowledge of the domain of *Control Engineering*, including relevant sections of mathematics. It is still in **early stage of development**.


## History and Background

Until 2022-10-01 the repo with primary URL (<https://github.com/ackrep-org/ocse/>) held the OWL-based version 0.1 of the OCSE, which was referenced in some publications. The current version of the OCSE (0.2) is developed using the [IRK framework](https://github.com/ackrep-org/pyirk-core) and is thus incompatible. Version 0.1 is now available under <https://github.com/ackrep-org/ocse-0.1>.

## Tips:

- Use `pytest` (executed in the root directory of this repo) to run the OCSE unittests.
- Use `pyirk -ac` to generate `.ac_candidates.txt` file used for [autocompletion](https://github.com/ackrep-org/irk-fzf) in *code* editor.
- Use `pyirk -l control_theory1.py ct -i` to load OCSE in interactive mode
- Use `pytest -s tests/test_quick.py` to run only the tests in the `test_quick` module (speeds up test-driven development)


# Coding style

We use `black -l 110 ./` to ensure coding style consistency.
