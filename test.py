import deBR

# SIMULTAION SETTINGS
VERBOSE = True
ALPHABET = 2 #Size of alphabet
WINDOWDIM = (2,2) #Tuple of (length,width)

# prints general window
WINIT = deBR.gen_initWindow(WINDOWDIM)
if VERBOSE:
  print(f"Initial window for size {WINDOWDIM}: \n {WINIT}")

# Determines number of aperodic windows
APNUM = deBR.gen_apNum(ALPHABET,WINDOWDIM)

# Generates generic shifter
A = deBR.gen_shifter(WINDOWDIM)

# testing
# testing given pc