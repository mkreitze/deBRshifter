import deBRGen
import deBRValidation
import deBRGenData

# SIMULTAION SETTINGS
deBRValidation.VERBOSE = deBRGen.VERBOSE = True # Need to define VERBOSE for deBRGen and deBRValidation to work
ALPHABET = 2
WINDOWDIM = (2,2) #Tuple of (length,width)

# GENERATION OF SHIFTER AND DEBR
# prints general window
WINIT = deBRGen.gen_initWindow(WINDOWDIM)

# Determines number of aperodic windows
APNUM = deBRGen.gen_apNum(ALPHABET,WINDOWDIM)

# Generates generic shifter
A = deBRGen.gen_shifter(WINDOWDIM)

# Generates all sub-circ matricies
Cs = deBRGen.gen_subcircs(ALPHABET,WINDOWDIM)

# Generates all shifters with inputted sub-circ matricies
allSs = deBRGen.gen_allShifter(ALPHABET,WINDOWDIM)

j=5 # 5/6 produce good deBR
AdeBR = deBRGen.gen_ring(allSs[j][0],APNUM,ALPHABET,WINDOWDIM) # note 0 to grab numpy array

# VALIDATION OF DEBR

# Checks if a single deBR is consistent
isConsistent = deBRValidation.check_consistency(AdeBR,allSs[j][0],ALPHABET,WINDOWDIM)

# Checks for aperodic windows
A,B,C = deBRValidation.check_aperiodic(AdeBR,ALPHABET,WINDOWDIM)
print(A)
print(B)
print(C) # output odd

# Determines power for repetition
pow = deBRValidation.get_cyclen(allSs[j][0],ALPHABET,APNUM,WINDOWDIM)

# Checks if every window is unique
uniqueness = deBRValidation.check_unique(AdeBR,ALPHABET,WINDOWDIM,APNUM)

# Visualizes data
deBRValidation.VERBOSE = deBRGen.VERBOSE = False
deBRGenData.ALLPRINT = True
allData = deBRGenData.test_deBRs(ALPHABET,WINDOWDIM,APNUM,False,False)
print(allData) #should be empty as we don't want anything stored


