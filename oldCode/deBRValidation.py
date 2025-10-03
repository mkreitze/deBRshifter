
# IMPORTS
import numpy as np
import deBRConstructor
from numpy.linalg import matrix_power
import itertools as it
import sympy as symp # used to determine factors of an integer
import matplotlib.pyplot as plt

try:
  VERBOSE
except NameError:
  VERBOSE = False
else:
  print("Verbose defined elsewhere") 

# INPUT: deBR (numpy array), shifter (numpy array), A (int), W (window length,width)
# OUTPUT: isConsistent (boolean)
def check_consistency(deBR,shifter,A,W):
  deBR = np.roll(deBR,1,axis = 1) # rolls to prevent read runoff
  finalWin = deBR[0:W[0],0:W[1]]
  finalWin = finalWin.reshape((-1, 1), order="F") # final window
  firstWin = (shifter@finalWin)%A
  if VERBOSE:
    print("Testing consistency")
    print("Final window")
    print(finalWin)
    print("Expected initial window")
    print(deBRConstructor.gen_initWindow(W))
    print("Generated initial window through shifter")
    print(firstWin)
    print(f"Thus consistency is {bool((firstWin == deBRConstructor.gen_initWindow(W)).all())}")
  return(bool((firstWin == deBRConstructor.gen_initWindow(W)).all()))

# INPUT: deBR (numpy array), A (alphabet size), W (window (length,width))
# OUTPUT: factDeBR (numpy array), winFacts (dictionary)
# Based Expands and determines column factors. It outputs these column factors and the important factors for the deBR
def base_expansion(deBR,A,W):
  pows = A ** np.arange(W[0])
  pows = pows.reshape((-1, 1), order="F")
  deBRMult = np.multiply(deBR,pows)
  deBRExpanded = np.cumsum(deBRMult,axis = 0)[W[0]-1]
  factorize = np.vectorize(symp.factorint)
  factDeBR = factorize(deBRExpanded.astype(int))

  c = W[0]
  cFacts = symp.factorint(c)
  cFacts.update({1: 1})
  winFacts = {}
  for k in cFacts:
    if k != c: # very annoying case with 2?
      newVal = (A**c - 1)/(A**k - 1)
      winFacts.update({int(newVal) : 1})
  winFacts.update({0: 1}) # dont forget zero
  if VERBOSE:
    print(f"deBR to check: \n {deBR}")
    print(f"Powers for base expansion: \n {pows}")
    print(f"Powers applied: \n {deBRMult}")
    print(f"Base Expanded deBR: \n {deBRExpanded}")
    print(f" Factors of deBR: \n {factDeBR}")
    print(f"Factors to check for: \n {winFacts}")
  return(factDeBR,winFacts,deBRExpanded.astype(int).tolist())

# Checks all dictionaries if there is w repeated shared factors
# INPUT: deBR (numpy array), A (int), W (tuple (length, width))
# OUTPUT: factDeBR (numpy array), aPerodic (bool)
# checks a deBR if its column factors repeat in such a way that a perodic window appers
def check_aperiodic(deBR,A,W):
  factDeBR,winFacts,expanded = base_expansion(deBR,A,W)
  i = 0
  importantFacts = dict(winFacts)
  aPeriodic = True

  for factors in factDeBR:
    if len(factors) == 0: # the factorization sends out an empty dictionary for 1, this accounts for this
      factors.update({1:1})
    simKey = importantFacts.keys() & factors.keys()
    if len(simKey) > 0:
      i+=1
      simKey = dict(factors)
    else:
      i = 0
    if VERBOSE:
      print(f"Currect factor set: {factors}")
      print(f"Factors to look for: {importantFacts}")
      print(f"Similar keys: {simKey}")
      print(f"Consecutive : {i}")
    if i >= W[1]:
      aPeriodic = False
      break
  outPutFactors = []
  for factors in factDeBR:
    outPutFactors += (list(factors.keys()))

  if VERBOSE:
    print(f"Thus aperiodicity is {aPeriodic}")
  return(outPutFactors,aPeriodic,expanded) # review outPutFactors and expanded. weird output

# INPUT shifter (numpy array), A (int), apN (int), W (tuple (length, width))
# OUTPUT i (int)
# Checks which power produces I, value of -1 means all 0s, value of -2 means powers repeat
def get_cyclen(shifter,A,apN,W):
    I = np.eye(shifter.shape[0])
    zero = np.zeros(shifter.shape)
    i=1 # identity matrix not possible, but start from 1 for cleaner doc output
    temp = np.copy(shifter)
    while (not np.array_equal(temp,I)):
      old = np.copy(temp)
      temp = (old@shifter)%A
      i+=1
      if VERBOSE:
        print(f"Power {i}: \n {temp}")
      if np.array_equal(temp,zero): # checks for 0 matrix
        i = -1
        break
      if i > apN+1: # if this pops, the matricies are cycling themselves.
        i = -2
        break
      
      temp = np.copy(temp)
    if VERBOSE:
      print(f"Power for matrix: {i}")
    return(i)


# INPUT: deBR (numpy), A (int), W (tuple (l,w)), apN (int)
# OUTPUT: isUnique (bool)
# Tiles deBR, then cuts it up. Uses numpy 'unique' command to condense one row of windows (issue detected?)
def check_unique(deBR,A,W,apN):
  tiled = np.tile(deBR,(2,2))
  shape = (tiled.shape[0] - 1, tiled.shape[1] - 1, 2, 2)  # 2x2 submatrices
  strides = tiled.strides * 2  # Each step will be 2 rows and 2 columns
  submatricies= np.lib.stride_tricks.as_strided(tiled, shape=shape, strides=strides)
  relevantSubMatricies = submatricies[0:W[1],0:apN]
  uniqueSubMatricies = np.unique(relevantSubMatricies,axis = 1)
  isUnique = bool(uniqueSubMatricies.shape == relevantSubMatricies.shape)
  if VERBOSE:
    print(f"DeBR we are convolving: \n {deBR}")
    print(f"Tiling of deBR: \n {tiled}")
    print(f"Genreated Submatricies: \n {relevantSubMatricies}")
    print(f"Dimension of Submatricies: \n {relevantSubMatricies.shape}")
    print(f"Unique submatricies: \n {uniqueSubMatricies}")
    print(f"Dimension of unique submatricies: \n {uniqueSubMatricies.shape}")
    print(f"Expected number of unique submatricies: \n {apN}")
    print(f"Thus is unique?: \n {isUnique}")
  return(isUnique)

