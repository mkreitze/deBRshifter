import deBRAffGen
import deBRValidation
import deBRVisualizeAff
deBRValidation.VERBOSE = deBRAffGen.VERBOSE = False
deBRVisualizeAff.ALLPRINT = False


#
#
#
# SIMULATION PARAMETERS

ALPHABET = 2
WINDOWDIM = (2,2) #Tuple of (length,width)
APNUM = deBRAffGen.gen_apNum(ALPHABET,WINDOWDIM) # Number of aperiodic windows
ONLYSUCCESSFUL = True # True if we only want to pow = apN shifters
ALLDATA = False # True if we want to see all shifters, not just successful ones
WANTGRAPH = True # True if we want to graph the data
WANTHISTOGRAM = True # True if we want to graph the histogram of the data
#
#







# CODE TO RUN

print(f"Checking powers of shifters with A = {ALPHABET}, W = {WINDOWDIM}, apN = {APNUM}")
successful = deBRVisualizeAff.test_deBR_powers(ALPHABET,WINDOWDIM,ALLDATA,ONLYSUCCESSFUL,WANTGRAPH,WANTHISTOGRAM)
