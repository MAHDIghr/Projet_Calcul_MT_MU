PYTHON=python3

# ========================
# TESTS UNITAIRES
# ========================

unit_tests:
	$(PYTHON) machine_de_turing/test_machine_de_turing.py
	$(PYTHON) machine_universelle/test_machine_universille.py


# ========================
# TESTS PAR QUESTION
# ========================

test_q1:
	$(PYTHON) main.py q1

test_q2:
	$(PYTHON) main.py q2

test_q3:
	$(PYTHON) main.py q3

test_q4:
	$(PYTHON) main.py q4

test_q5:
	$(PYTHON) main.py q5

test_q6:
	$(PYTHON) main.py q6

test_q7:
	$(PYTHON) main.py q7

test_q8:
	$(PYTHON) main.py q8

test_q9:
	$(PYTHON) main.py q9

test_q10:
	$(PYTHON) main.py q10


# ========================
# TESTS GLOBAL
# ========================

tests:
	$(PYTHON) main.py all


# ========================
# ALL (unit + fonctionnels)
# ========================

all: unit_tests tests