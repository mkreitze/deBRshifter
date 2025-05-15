import deBRGen
import deBRValidation
import deBRVisualize
deBRValidation.VERBOSE = deBRGen.VERBOSE = False
deBRVisualize.ALLPRINT = False


#
#
#
# SIMULATION PARAMETERS

ALPHABET = 3
WINDOWDIM = (2,2) #Tuple of (length,width)
APNUM = deBRGen.gen_apNum(ALPHABET,WINDOWDIM) # Number of aperiodic windows
ONLYSUCCESSFUL = False # True if we only want to pow = apN shifters
ALLDATA = True # True if we want to see all shifters, not just successful ones
WANTGRAPH = True # True if we want to graph the data
WANTHISTOGRAM = True # True if we want to graph the histogram of the data
#
#







# CODE TO RUN

print(f"Checking powers of shifters with A = {ALPHABET}, W = {WINDOWDIM}, apN = {APNUM}")
successful = deBRVisualize.test_deBR_powers(ALPHABET,WINDOWDIM,ALLDATA,ONLYSUCCESSFUL,WANTGRAPH,WANTHISTOGRAM)
