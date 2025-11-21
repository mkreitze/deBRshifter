# ─── Imports ───────────────────────────────────────────────
import os
import numpy as np # type: ignore
import itertools as it
import sympy as symp # type: ignore # used to determine factors of an integer
import deBRConstructor # redundant code: gen_apn, gen_subcircs, window_to_base10
import typing as type # to make functions more clear
from numpy.typing import NDArray  # type: ignore
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
def shifter_gen_combo(W: type.Tuple[int, int], comboCirc: type.Tuple[int, ...],comboCol:  NDArray[int], allCircs: type.List[NDArray[int]]) -> NDArray[int]:
  shifter = basic_shifter(W)
  circRow = []
  for subCirc in comboCirc:
    circRow.append(allCircs[subCirc])
  shifter[-W[0]-1:-1,0:-1] = np.concatenate(circRow,axis = 1) # np is
  shifter[-W[0]-1:-1,-1:] = comboCol # affine column
  return(shifter)

# INFO 
# stuff
def gen_all_npWindows(A: int,W: type.Tuple[int, ...])-> type.List[NDArray[int]]:
  windows = it.product(range(A),repeat = W[0]*W[1])
  npWindows = []
  for window in windows:
    temp = np.array(window,dtype=int).reshape(-1,1)
    npWin = np.ones((W[0]*W[1]+1,1),dtype=int)
    npWin[0:-1] = temp
    npWindows.append(npWin)
  return(npWindows)

# INFO (can be done with casting, rolling and - but probably not efficient)
# Literally just changed window_to_base10(tempWindow,A) to deBRConstructor.window_to_base10(tempWindow[:-1],A)
def gen_cycles(shifter: NDArray[int],allNpWindows: type.List[NDArray[int]], A : int,W : type.Tuple[int,...]) -> type.Tuple[type.List[type.List[NDArray[int]]],type.List[type.List[NDArray[int]]]]:
  cycles = []
  rings = []
  ringCondition = deBRConstructor.get_apNum(A,W)

  for window in allNpWindows:
    if window[0] != -1:
      cycle = [];base10Cycle=[]
      cycle.append(window);base10Cycle.append(deBRConstructor.window_to_base10(window[:-1],A))
      tempWindow = np.copy(window)
      tempWindow = (shifter@tempWindow)%A
      while not np.array_equal(tempWindow,window):
        allNpWindows[deBRConstructor.window_to_base10(tempWindow[:-1],A)][0] = -1
        cycle.append(tempWindow);base10Cycle.append(deBRConstructor.window_to_base10(tempWindow[:-1],A))
        tempWindow = (shifter@tempWindow)%A
    if len(base10Cycle) == ringCondition:
      rings.append(cycles)
      cycles.append([np.array(cycle).astype(int),np.array(base10Cycle)])
  return(cycles,rings)

# INFO
# Note, we do not actually _generate_ the tori here, just use the cycle
def gen_tori(W: type.Tuple[int,...], cycle: NDArray[int]) -> NDArray[int]:
  if len(cycle) < W[1]:
    return(-1)
  deBR = np.zeros((W[0],len(cycle)),dtype=int)
  for i in range(len(cycle)):
    temp = np.copy(cycle[i]) # to make sure it doesnt mess up the stored data
    temp = temp[:-1].reshape((W[0],W[1]), order="F")
    deBR[:,i] = temp[:,0] # copys each column of the torus
  return(deBR)

# INFO
# 
def get_power(shifter: NDArray[int],A: int,W: type.Tuple[int,...], VERBOSE = False) -> int:
  I = np.eye(W[0]*W[1]+1)
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

