# ─── Imports ───────────────────────────────────────────────
import deBRDataGen
import deBRConstructor
import numpy as np # type: ignore
import itertools as it
# ───────────────────────────────────────────────────────────

# INFO
# This code mainly just checks the 'all ones' version of a shifter for a specific alphabet size and windowsize. 
# It checks the linear, and resulting affine case, for both scenarios. Helpful to make sure the code is working as intended


W = (2,2) # defined as (length,width)
A = 2 # alphabet size

PRINTLINEAR = False
PRINTAFFINE = True
PRINTAFFINESANITY = True

if PRINTLINEAR:
    print(f"\n FOR THE LINEAR CASE")
    deBRDataGen.store_all_linear_shifters(A,W,beautify=True,genHist=True,genOneLook=True)
    
if PRINTAFFINE:
    print(f"\n FOR THE AFFINE CASE")
    deBRDataGen.store_all_affine_shifters(A,W,beautify=True,genHist=True,genOneLook=True)