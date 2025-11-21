# ─── Imports ───────────────────────────────────────────────
import os
import numpy as np
import itertools as it
import sympy as symp # used to determine factors of an integer
import deBRConstructor
import deBRAffConstructor
import deBRGraphics
import typing as type # to make functions more clear
from numpy.typing import NDArray  # type: ignore
# ───────────────────────────────────────────────────────────

# This code:
# Generates text files: 
# All circs for arbitrary A,W for linear or affine shifters
# Outputs data onto a file

# for file saving (will make them once imported)
plotsFolder = "plots";os.makedirs(plotsFolder, exist_ok=True)
shiftersFolder = "shifters";os.makedirs(shiftersFolder, exist_ok=True)

#INFO
# Generates then stores all linear shifters
# NOTE: We check invertibility first
def store_all_linear_shifters(A: int,W: type.Tuple[int,int],beautify : bool = False):
    with open(f"{shiftersFolder}/All linear {A};{W}.txt", "w") as f: # done here to make stuff a bit more legibile
        # makes the data
        f.write(f"For {A};{W} with APN = {deBRConstructor.get_apNum(A,W)}  TW = {A**(W[0]*W[1])} \n")
        allWindows = deBRConstructor.gen_all_npWindows(A,W)
        allSubCircs = deBRConstructor.subcirc_gen_all(A,W)
        circCombos =  it.product(allSubCircs,repeat = W[1]) 
        circIntRep =  it.product(range(A**W[0]),repeat = W[1])
        idx = 0;maxSize = (A**W[0])**W[1]
        # makes and stores all components for shifters
        for circs,intRep in zip(circCombos,circIntRep):
            shifter = deBRConstructor.shifter_gen_from_circs(W,circs) # makes a single shifter
            idx+=1
            print(f"Done {idx} of {maxSize}")
            if deBRConstructor.is_invert(shifter,A): # IMPORTANT gen_cycles assumes the shifter is invertible
                cycles,rings = deBRConstructor.gen_cycles(shifter,np.copy(allWindows), A, W) # makes all cycles and rings for a shifter
                # stores all cycles
                f.write(f"Shifter: {intRep} \n")
                f.write(f"  Cycles:\n")
                for cycle in cycles:
                    f.write(str(len(cycle[1]))+" "+str(cycle[1])+"\n")
                    if beautify and len(cycle[1])>=W[1]: # stores images of all tori from cycles
                        toriFolder=f"{shiftersFolder}/All linear {A};{W}/{intRep}";os.makedirs(toriFolder, exist_ok=True)
                        tori = deBRConstructor.gen_tori(W,cycle[0])
                        deBRGraphics.beautify_matrix(tori,imageName = toriFolder+f"/{simplify_name(cycle[1])}",saveImage=True)
                # stores all rings (if they exist)
                if len(rings)>0:
                    f.write(f"  Rings: \n")
                    # stores any rings
                    for ring in rings:
                        f.write(f"R {str(ring[1])} \n")
                        deBRGraphics.beautify_matrix(ring[0],imageName = toriFolder+f"/R {simplify_name(ring[1])}",saveImage=True)
            else: 
                f.write(f"Cycles for shifter: {intRep} (NOT INVERTIBLE)\n")
    return(1)

# INFO
# 
# NOTE:
def store_all_affine_shifters(A: int,W: type.Tuple[int,int],beautify : bool = False):
    with open(f"{shiftersFolder}/All affine {A};{W}.txt", "w") as f: # done here to make stuff a bit more legibile
        # makes the data
        allWindows = deBRConstructor.gen_all_npWindows(A,W)
        allSubCircs = deBRConstructor.subcirc_gen_all(A,W)
        circCombos =  it.product(allSubCircs,repeat = W[1]) 
        circIntRep =  it.product(range(A**W[0]),repeat = W[1])
        affCol = 1
    return(1) 

# INFO:
# Deals with cycles that are too long for a human to really parse.
# NOTE: Since we have unique cycles, we are all chill with no rewriting
def simplify_name(possibleName : type.Tuple) -> str: 
    if len(possibleName) > 50:
        return(str(possibleName[1]))
    else:
        return(str(possibleName))