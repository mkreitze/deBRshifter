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

# INFO (from internet) NOT USED
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
def gen_all_npWindows(A: int,W: type.Tuple[int, int])-> type.List[NDArray[int]]:
  windows = it.product(range(A),repeat = W[0]*W[1])
  npWindows = []
  for window in windows:
    npWin = np.array(window,dtype=int).reshape(-1,1)
    npWindows.append(npWin)
  return(npWindows)

# INFO outputs vertical vector
# from copilot. Please review
def convert_to_base_a(num: int, base: int, n_digits):
    if base < 2:
        raise ValueError("Base must be at least 2.")
    if num < 0:
        raise ValueError("Number must be non-negative.")

    digits = []
    while num > 0:
        digits.append(num % base)
        num //= base

    # Pad with leading zeros to ensure n_digits length
    while len(digits) < n_digits:
        digits.append(0)

    # If the number requires more than n_digits, raise an error
    if len(digits) > n_digits:
        raise ValueError(f"Number too large to fit in {n_digits} digits for base {base}.")

    # Reverse to get the correct order
    return np.array(digits[::-1]).reshape((-1,1), order="F")  # vertical vector


# INFO 
# checks if the first window in a cycle is periodic or aperiodic 
def is_cycle_periodic(window: NDArray[int],W: type.Tuple[int, int],A: int) -> bool:
  divisors = symp.divisors(W[1])
  temp = np.reshape(window,(W),order="F") # reshapes original window
  for divisor in divisors[:-1]:
    windowToRoll = np.roll(np.copy(temp),divisor,axis=0) # checks if same
    temp2 = temp-windowToRoll
    if np.all(temp2 == 0):
      return(True) # checks all rotations
  return(False)

# INFO 
# 
def window_to_base10(window: NDArray[int],A: int) -> int:
  base10 = (A ** np.arange(start = len(window)-1,stop = -1, step = -1))
  return((base10@window).astype(int)[0])  

# INFO (can be done with casting, rolling and - but probably not efficient)
#
def gen_cycles(shifter: NDArray[int],allNpWindows: type.List[NDArray[int]], A : int,W : type.Tuple[int,...]) -> type.List[type.List[NDArray[int]]]:
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
      cycles.append([np.array(cycle).astype(int),np.array(base10Cycle)])
  return(cycles)


# INFO
# Note, we do not actually _generate_ the tori here, just use the cycle to fill it in
# Ouput of -1 implies we have a cycle smaller than the window width. Leads to impossible tori
def gen_tori(W: type.Tuple[int,...], cycle: NDArray[int]) -> NDArray[int]:
  if len(cycle) < W[1]:
    return(-1)
  deBR = np.zeros((W[0],len(cycle)),dtype=int)
  for i in range(len(cycle)):
    temp = np.copy(cycle[i]) # to make sure it doesnt mess up the stored data
    temp = temp.reshape((W[0],W[1]), order="F")
    deBR[:,i] = temp[:,0] # copys each column of the torus
  return(deBR)

# INFO
# 
def get_power(shifter: NDArray[int],A: int,W: type.Tuple[int,...], VERBOSE = False) -> int:
  I = np.eye(W[0]*W[1])
  tempShifter = np.copy(shifter)
  pow = 1
  while not np.array_equal(tempShifter, I) and pow < A**(W[0]*W[1]):
    if VERBOSE:
      print(f"Shifter to the power of {pow}: \n {tempShifter}")
    tempShifter = (shifter@tempShifter)%A
    pow += 1
  if VERBOSE:
    print(f"Shifter to the power of {pow}: \n {tempShifter}")
  return(pow)

# INFO (true implies invert)
# 
def is_invert(shifter: NDArray[int],A: int) -> bool:
  if (np.linalg.det(shifter)%A) == 0:
    return(False)
  else:
    return(True)
  
