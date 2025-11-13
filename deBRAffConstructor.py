# ─── Imports ───────────────────────────────────────────────
import os
import numpy as np
import itertools as it
import sympy as symp # used to determine factors of an integer
import deBRConstructor # redundant code: gen_apn, gen_subcircs
import typing as type # to make functions more clear
from numpy.typing import NDArray 
# ───────────────────────────────────────────────────────────

# AFFINE CODE

# This code constructs:
# All shifters
# Singular shifter
# Generates all cycles
# Tori (from cycles)

# INFO
# Input: W (window length,width)
# Output: S (numpy array)
# Generates general affine shifter, no subcircs within
def basic_shifter(W: type.Tuple[int, int]) -> NDArray[int]:
  d = W[0]*W[1]+1
  S = np.eye(d)
  S = np.roll(S,-W[0],axis = 0)
  S[(d-W[0]-1):(d-W[0]+1)] = -1
  S[-1,-1] = 1;S[-1,1] = 0
  return(S)

# INFO 
# Generates the extra vertical vector for the affine case
def gen_aff_free(A: int, W: type.Tuple[int, int]) -> NDArray[int]:
  cols = it.product(range(A),repeat = W[0])
  affCols = []
  for col in cols:
    C = np.zeros((W[0],1),dtype=int)
    for i in range(W[0]):
      C[i,0] = col[i]
    affCols.append(C)
  return(affCols)

# INFO (IS INEFFICIENT)
# INPUT: W, combo (subcircs that make up shifter), allCircs (every sub-circ as a numpy array in a list)
# OUTPUT: shifter (np array with composition in combo)
def shifter_gen_combo(W: type.Tuple[int, int], combo: type.Tuple[int, ...],allCircs: type.List[NDArray[int]]) -> NDArray[int]:
  shifter = basic_shifter(W)
  circRow = []
  for subCirc in combo:
    circRow.append(allCircs[subCirc])
  shifter[-W[0]-1:-1,0:-1] = np.concatenate(circRow,axis = 1) # np is
  return(shifter)



# INFO (true implies invert)
def is_invert(shifter: NDArray[int],A: int) -> bool:
  if (np.linalg.det(shifter)%A) == 0:
    return(False)
  else:
    return(True)

