# ─── Imports ───────────────────────────────────────────────
import os
import numpy as np
import itertools as it
import sympy as symp # used to determine factors of an integer
# ───────────────────────────────────────────────────────────

# This code:
# Generates text files: 
# All circs for arbitrary A,W for linear or affine shifters
# Outputs data onto a file

# for file saving 
folder_path = "plots"
os.makedirs(folder_path, exist_ok=True)


