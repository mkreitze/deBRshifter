# ─── Imports ───────────────────────────────────────────────
import os
import numpy as np
import itertools as it
import sympy as symp # used to determine factors of an integer
import typing as type # to make functions more clear
from numpy.typing import NDArray 
# ───────────────────────────────────────────────────────────

# This code constructs:
# aperodic window count (apNum)
# all sub-circulants 
# Singular shifter
# All shifters
# Generates all cycles
# Tori (cycles)

# INFO
# Input: W (window length,width)
# Output: S (numpy array)
# Generates general shifter, no subcircs within
def basic_shifter(W: type.Tuple[int, ...]) -> NDArray[int]:
  d = W[0]*W[1]
  S = np.eye(d)
  S = np.roll(S,-W[0],axis = 0)
  S[(d-W[0]):] = -1
  return(S)

# INFO
# INPUT: A,W (Alphabet size, Window width)
# OUTPUT: apNum (int)
# Determines number of aperodic windows through application of the mobius function. Uses 'efficient' ''sieve-based'' method. Did not look into much.
def get_apNum(A: int,W: type.Tuple[int, ...]) -> int:
  mobis = list(symp.sieve.mobiusrange(1,W[0]+1)) # we use sieve to efficiently compute factors
  apNum = 0
  facts = symp.divisors(W[0])
  for d in facts:
    apNum += (mobis[int(W[0]/d)-1])*(A**(d*W[1])) # effectively the sum
  apNum = apNum/W[0]
  return(int(apNum))

# INFO
# INPUT: A (Alphabet size) , W (window length,width)
# OUTPUT: allCircs (list of all circs as numpy arrays)
def subcirc_gen_all(A: int ,W: type.Tuple[int, ...]) -> type.List[NDArray[int]]:
  rows = it.product(range(A),repeat = W[0]) # all possible circs come from rotating all possible rows, this generates all possible rows for the given alphabet
  allCircs = []
  for row in rows:
    C = np.zeros((W[0],W[0])) # circs are of dim lxl
    for i in range(W[0]):
      C[i] = np.roll(row,i) # rotates the row 1 as we go down
    allCircs.append(C)
  return(allCircs)

# INFO (IS INEFFICIENT)
# INPUT: W, combo (subcircs that make up shifter), allCircs (every sub-circ as a numpy array in a list)
# OUTPUT: shifter (np array with composition in combo)
def shifter_gen_combo(W: type.Tuple[int, ...], combo: type.Tuple[int, ...],allCircs: type.List[NDArray[int]]) -> NDArray[int]:
  shifter = basic_shifter(W)
  circRow = []
  for subCirc in combo:
    circRow.append(allCircs[subCirc])
  shifter[-W[0]:] = np.concatenate(circRow,axis = 1) # np is
  return(shifter)
