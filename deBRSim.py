
import deBRGen
import deBRValidation
import deBRVisualize

deBRValidation.VERBOSE = deBRGen.VERBOSE = False
deBRVisualize.ALLPRINT = False
ALPHABET = 2
WINDOWDIM = (2,2) #Tuple of (length,width)

APNUM = deBRGen.gen_apNum(ALPHABET,WINDOWDIM) # Number of aperiodic windows
allData = deBRVisualize.test_deBRs(ALPHABET,WINDOWDIM,APNUM,True,False)
# data stored as [ shifter, circs, col factors, col expansions, uniquness, perodicity, consistency, power, deBR]
deBRVisualize.print_data(allData)
deBRVisualize.graph_deBRs(ALPHABET,WINDOWDIM,APNUM,allData,False)



print("Only successfuls")
successful = deBRVisualize.test_deBRs(ALPHABET,WINDOWDIM,APNUM,False,True)
deBRVisualize.print_data(successful)
deBRVisualize.graph_deBRs(ALPHABET,WINDOWDIM,APNUM,successful,True)

