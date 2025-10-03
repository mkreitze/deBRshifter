
# IMPORTS
import numpy as np
from numpy.linalg import matrix_power
import itertools as it
import sympy as symp # used to determine factors of an integer
import matplotlib.pyplot as plt




# Input: A (alphabet), W (generic window dimensions)
# Output: W0, initial aperodic window 
# Note; we use 00...1 as must always exists
def gen_initWindow(W,VERBOSE = False):
  W0 = np.zeros(W)
  W0[-1,-1] = 1
  W0 = W0.reshape((-1, 1), order="F") # effectively the vec command
  if VERBOSE:
    print(f"Initial window for size {W}: \n {W0}")
  return(W0)

# INPUT: A,W (Alphabet size, Window width)
# OUTPUT: apNum (int)
# Determines number of aperodic windows through application of the mobius function. Uses 'efficient' ''sieve-based'' method. Did not look into much.
def gen_apNum(A,W):
  mobis = list(symp.sieve.mobiusrange(1,W[0]+1)) # we use sieve to efficiently compute factors
  apNum = 0
  facts = symp.divisors(W[0])
  for d in facts:
    apNum += (mobis[int(W[0]/d)-1])*(A**(d*W[1])) # effectively the sum
  apNum = apNum/W[0]
  if VERBOSE:
    print(f"L: {W[0]} W: {W[1]} \nFactors of L: {facts}")
    print(f"Mobius evaluations {mobis} \nFactors responsible {facts} \nNumber of aperodic windows: {apNum} ")
  return(int(apNum))

# Input: W (window length,width)
# Output: S (numpy array)
# Generates general shifter, no subcircs within
def gen_shifter(W):
  d = W[0]*W[1]
  S = np.eye(d)
  S = np.roll(S,-W[0],axis = 0)
  S[(d-W[0]):] = -1
  if VERBOSE:
    print(f"Generic shifter matrix S (-1 represents free indicies): \n {S}")
  return(S)

# INPUT: A (Alphabet size) , W (window length,width)
# OUTPUT: allCircs (list of all circs as numpy arrays)
def gen_subcircs(A,W):
  rows = it.product(range(A),repeat = W[0]) # all possible circs come from rotating all possible rows, this generates all possible rows for the given alphabet
  allCircs = []
  for row in rows:
    C = np.zeros((W[0],W[0])) # circs are of dim lxl
    for i in range(W[0]):
      C[i] = np.roll(row,i) # rotates the row 1 as we go down
    allCircs.append(C)
  if VERBOSE:
    rows = it.product(range(A),repeat = W[0]) # has to be in verbose, as printing the rows destroys iterator
    print("All possible circ rows:")
    for row in rows:
      print(row)
    print("All possible circs:")
    for C in allCircs:
      print(C)
    print("Number of circs:")
    print(len(allCircs))
  return(allCircs)

# To record circs in a shifter, we base expand as needed
# code for base expansion https://mathspp.com/blog/base-conversion-in-python
# might be incredibly slow.
def to_base(number, base):
    if not number:
        return [0]

    digits = []
    while number:
        digits.append(number % base)
        number //= base
    return list(reversed(digits))

#INPUT:  A (Alphabet size) , W (window length,width)
#OUTPUT allShifters (list in format: [shifter , circs in order as they made it up] )
# Due to itertools method, circs are ordered arbitrarily. I.e "circ 5" does not really have meaning
def gen_allShifter(A,W):
  allShifters = []
  genericShifter = gen_shifter(W)
  Cs = gen_subcircs(A,W)
  d = np.arange(len(Cs))
  circCombos = it.product(Cs, repeat = W[1]) # generates all circ combinations, with replacement
  circNum = 0
  for circCombo in circCombos:
    circComp = to_base(circNum,A**W[0])
    for i in range(W[1] - len(to_base(circNum,A**W[0]))):
      circComp.insert(0,0)
    shifter = np.copy(genericShifter) # Matt paranoia
    shifter[-W[0]:] = np.concatenate(circCombo, axis = 1) # sticks in circ
    allShifters.append([shifter,circComp])
    circNum += 1
  if VERBOSE:
    print("All possible shifters (with circ make ups):")
    for shifter in allShifters:
      print(shifter)
  if VERBOSE:
    print(f"Total number of shifters: {len(allShifters)}")
    print(f"Expected number of shifters: {A**W[0]**W[1]}")
  return(allShifters)

# INPUT: shifter (numpy array), apN (int), A (int), W (window length,width)
# OUTPUT: deBR (numpy array)
def gen_ring(shifter,apN,A,W):
  deBR = np.zeros((W[0],apN)) # np array to rep deBR
  deBR[(W[0]-1),(W[1]-1)] = 1 # generates initial window... no need for gen_initWindow
  if VERBOSE:
    print(f"Shifter used: \n {shifter}")
  for i in range(apN-W[1]):
    nextWin = deBR[0:W[0],i:i+W[1]]
    nextWin = nextWin.reshape((-1, 1), order="F") # vec command
    if VERBOSE:
      print("window to start")
      print(nextWin)
    nextWin = (shifter@nextWin)%A # because of multiple commands, verbose is horrible
    if VERBOSE:
      print("window after application")
      print(nextWin)
    deBR[:,i+W[1]:i+W[1]+1]= np.reshape(nextWin[-W[0]:],(W[0],1))
    if VERBOSE:
      print("updating deBR")
      print(deBR)
  if VERBOSE:
    print(f"Attempted deBR: \n {deBR}")
  return(deBR)


def gen_cycle(shifter,A,W,apN,l):
  windowsHit = []
  initWin = np.zeros(W[0]*W[1])
  initWin[-1] = 1
  initWin = initWin.reshape((-1, 1), order="F") 
  expo = np.arange(W[0]*W[1])
  print(l)
  for i in range(l+1):
    print(initWin)
    initWin = (shifter@initWin)%A
    temp = expo@initWin
    windowsHit.append(temp)
  return(windowsHit)