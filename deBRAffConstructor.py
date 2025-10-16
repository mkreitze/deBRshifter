# ─── Imports ───────────────────────────────────────────────
import os
import numpy as np
import itertools as it
import sympy as symp # used to determine factors of an integer
# ───────────────────────────────────────────────────────────

# AFFINE CODE

# This code constructs:
# aperodic window count (apNum)
# all sub-circulants 
# Singular shifter
# All shifters
# Generates all cycles
# Tori (cycles)

# Input: W (window length,width)
# Output: S (numpy array)
# Generates general affine shifter, no subcircs within
def basic_shifter(W):
  d = W[0]*W[1]+1
  S = np.eye(d)
  S = np.roll(S,-W[0],axis = 0)
  S[(d-W[0]-1):(d-W[0]+1)] = -1
  S[-1,-1] = 1;S[-1,1] = 0
  return(S)

