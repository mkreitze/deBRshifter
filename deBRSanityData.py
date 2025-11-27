# ─── Imports ───────────────────────────────────────────────
import deBRDataGen
import deBRConstructor
import numpy as np # type: ignore
import itertools as it
# ───────────────────────────────────────────────────────────

# INFO
# This code mainly just checks the 'all ones' version of a shifter for a specific alphabet size and windowsize. 
# It checks the linear, and resulting affine case, for both scenarios. Helpful to make sure the code is working as intended

W = (2,3) # defined as (length,width)
A = 2 # alphabet size

PRINTLINEAR = True
PRINTAFFINE = False
PRINTAFFINESANITY = True

if PRINTLINEAR:
    deBRDataGen.store_all_linear_shifters(A,W,beautify=True,genHist=True)
    
if PRINTAFFINE:
    deBRDataGen.store_all_affine_shifters(A,W,True)