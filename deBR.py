# SIMULTAION SETTINGS
VERBOSE = True
ALPHABET = 2 #Size of alphabet
WINDOWDIM = (2,2) #Tuple of (length,width)

# IMPORTS
import numpy as np
from numpy.linalg import matrix_power
import itertools as it
import sympy as symp # used to determine factors of an integer
import matplotlib.pyplot as plt



# Input: A (alphabet), W (generic window dimensions)
# Output: W0, initial aperodic window
def gen_initWindow(W):
  W0 = np.zeros(W)
  W0[-1,-1] = 1
  W0 = W0.reshape((-1, 1), order="F") # effectively the vec command
  return(W0)

# INPUT: A,W (Alphabet size, Window width)
# OUTPUT: apNum (int)
# Determines number of aperodic windows through application of the mobius function
def gen_apNum(A,W):
  mobis = list(symp.sieve.mobiusrange(1,W[0]+1)) # we use sieve to efficiently compute factors
  apNum = 0
  facts = symp.divisors(W[0])
  for d in facts:
    apNum += (mobis[int(W[0]/d)-1])*(A**(d*W[1])) # effectively the sum
  apNum = apNum/W[0]
  if VERBOSE:
    print(f"L: {W[0]} W: {W[1]} \nFactors of L: {facts}")
    print(f"Mobious evaluations {mobis} \nFactors responsible {facts} \nNumber of aperodic windows: {apNum} ")
  return(int(apNum))

# Input: W (window length,width)
# Output: S (numpy array)
# Generates general shifter, not intialized by any circs
def gen_shifter(W):
  d = W[0]*W[1]
  S = np.eye(d)
  S = np.roll(S,-W[0],axis = 0)
  S[(d-W[0]):] = -1
  if VERBOSE:
    print(f"Generic shifter matrix S (-1 represents free indicies): \n {S}")
  return(S)