# ─── Imports ───────────────────────────────────────────────
import os
import numpy as np
import itertools as it
import sympy as symp # used to determine factors of an integer
# ───────────────────────────────────────────────────────────

# This code:
# Generates text files: 
# All invertible circs for A,W
# All circs with certain cycle lengths of A,W
# Things to print: 
# Circ fingerprint
# Prints cycles, powers
# Prints tori for each cycle


# for file saving 
folder_path = "plots"
os.makedirs(folder_path, exist_ok=True)


