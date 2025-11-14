# ─── Imports ───────────────────────────────────────────────
import os
import numpy as np
import itertools as it
import sympy as symp # used to determine factors of an integer
import deBRConstructor
import deBRAffConstructor
import deBRGraphics
# ───────────────────────────────────────────────────────────

# This code:
# Generates text files: 
# All circs for arbitrary A,W for linear or affine shifters
# Outputs data onto a file

# for file saving 
plotsFolder = "plots";os.makedirs(plotsFolder, exist_ok=True)
shiftersFolder = "shifters";os.makedirs(shiftersFolder, exist_ok=True)

#INFO
# Generates then stores all linear shifters
def store_all_linear_shifters(A: int,W: type.tuple[int,int],beautify: bool):
    allWindows = deBRConstructor.gen_all_npWindows(A,W)
    allSubCircs = deBRConstructor.subcirc_gen_all(A,W)
    circCombos = it.product(allSubCircs, repeat = W[1]) 
    for combo in circCombos:
        shifterFolder = str(combo);os.makedirs(shiftersFolder+"\ "+shifterFolder, exist_ok=True)
        shifter = deBRConstructor.shifter_gen_combo(W,combo,allSubCircs)
        shifterCycles = deBRConstructor.gen_cycles(shifter ,allWindows,A,W)
        if beautify:
            1
    return(1)

