import deBRDataGen
import numpy as np


# INFO
# This code mainly just checks the 'all ones' version of a shifter for a specific alphabet size and windowsize. 
# It checks the linear, and resulting affine case, for both scenarios. Helpful to make sure the code is working as intended

W = (2,2) # defined as (length,width)
A = 2 # alphabet size

deBRDataGen. store_all_linear_shifters(A,W)