# ─── Imports ───────────────────────────────────────────────
import os
import numpy as np
import itertools as it
import sympy as symp # used to determine factors of an integer
import typing as type # to make functions more clear
from numpy.typing import NDArray 
import time
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

# INFO (true implies invert)
def is_invert(shifter: NDArray[int],A: int) -> bool:
  if (np.linalg.det(shifter)%A) == 0:
    return(False)
  else:
    return(True)

# INFO (from internet)
# Turns base 10 into base n
# From https://mathspp.com/blog/base-conversion-in-python
# might be incredibly slow.
def to_base(number, base):
    if not number:
        return [0]
    
    digits = []
    while number:
        digits.append(number % base)
        number //= base
    return list(reversed(digits))

# INFO 
# stuff
def gen_all_npWindows(A: int,W: type.Tuple[int, ...])-> type.List[NDArray[int]]:
  windows = it.product(range(A),repeat = W[0]*W[1])
  npWindows = []
  for window in windows:
    npWin = np.array(window,dtype=int).reshape(-1,1)
    npWindows.append(npWin)
  return(npWindows)

# INFO
# 
def window_to_base10(window,A):
  base10 = (A ** np.arange(start = len(window)-1,stop = -1, step = -1))
  return((base10@window).astype(int)[0])
  

# INFO (can be done with casting, rolling and - but probably not efficient)
#
def gen_cycles(shifter: NDArray[int],allNpWindows: type.List[NDArray[int]], A : int,W : type.Tuple[int,...]):
  cycles = []
  for window in allNpWindows:
    if window[0] != -1:
      cycle = [];base10Cycle=[]
      cycle.append(window);base10Cycle.append(window_to_base10(window,A))
      tempWindow = np.copy(window)
      tempWindow = (shifter@tempWindow)%A
      while not np.array_equal(tempWindow,window):
        allNpWindows[window_to_base10(tempWindow,A)][0] = -1
        cycle.append(tempWindow);base10Cycle.append(window_to_base10(tempWindow,A))
        tempWindow = (shifter@tempWindow)%A
      cycles.append([np.array(cycle),np.array(base10Cycle)])
  return(cycles)


# INFO
# 
def get_power(shifter,A,W):
  I = np.eye(W[0]*W[1])
  tempShifter = np.copy(shifter)
  pow = 1
  while not np.array_equal(tempShifter, I) and pow < A**(W[0]*W[1]):
    tempShifter = (shifter@tempShifter)%A
    pow += 1
  return(pow)