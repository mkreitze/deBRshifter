# ─── Imports ───────────────────────────────────────────────
import deBRAffConstructor
import deBRConstructor
import numpy as np # pyright: ignore[reportMissingImports]
# ───────────────────────────────────────────────────────────


# INFO
# This code mainly just checks the 'all ones' version of a shifter for a specific alphabet size and windowsize. 
# It checks the linear, and resulting affine case, for both scenarios. Helpful to make sure the code is working as intended

W = (3,2) # defined as (length,width)
A = 2 # alphabet size
PRINTLINEAR = True
PRINTAFFINE = True
PRINTAFFINESANITY = True
LONGOUTPUT = False # prints out the windows individually, bad if A,W are bigger than 2

print(f"System for {A};{W}")

if PRINTLINEAR:

    print(f"\n FOR THE LINEAR CASE")

    print(f"\n Generic shifter (-1 denotes free): \n {deBRConstructor.basic_shifter(W)}")

    print(f"\n Number of aperodic windows: \n {deBRConstructor.get_apNum(A,W)}")

    print(f"\n All sub-circs: (notice row in base 10 is index) ")
    allSubCircs = deBRConstructor.subcirc_gen_all(A,W)
    i = 0
    for subCirc in allSubCircs:
        print(f"{subCirc}: Index {i}")
        i+=1

    print(f"\n ALLONES SHIFTER, COMPOSITION: {tuple(1 for i in range(W[1]))}")
    print("-----")
    onesShifter = deBRConstructor.shifter_gen_combo(W,tuple(1 for i in range(W[1])),allSubCircs)
    print(onesShifter)

    print(f"All generated cycles for allones shifter")
    print("-----")
    allWindows = deBRConstructor.gen_all_npWindows(A,W) # note windows are in base 10 order read bottom to top
    onesCycles,onesRings = deBRConstructor.gen_cycles(onesShifter,allWindows,A,W)
    for cycle in onesCycles:
        # prints each cycle as base 10 numbers in list 
        print(f"For Cycle {cycle[1]}:")
        if LONGOUTPUT:
            # prints each cycle as windows (turn off if A,W large)
            print(f"Windows: \n{cycle[0]}:")
        # if associated tori are desired, can be generated here
        tori = deBRConstructor.gen_tori(W,cycle[0])
        print(f"Torus associated to cycle: \n {tori}")
        print(f"Note; cycle is {deBRConstructor.is_cycle_periodic(cycle[0][0],W,A)} periodic")
        print("-----")

    print(f"Power of shifter {deBRConstructor.get_power(onesShifter,A,W,False)}")
    print("-----")

    print(f"Is shifter invertible? {deBRConstructor.is_invert(onesShifter,A)}")
    print("-----")

if PRINTAFFINE:
    print(f"\n \n \n FOR THE AFFINE CASE \n \n \n")
    print(f"Generic affine shifter (-1 denotes free): \n {deBRAffConstructor.basic_shifter(W)}")

    print(f"Number of aperodic windows (same as linear case): \n {deBRConstructor.get_apNum(A,W)}")

    print(f"All sub-circs (same as linear case):")
    allSubCircs = deBRConstructor.subcirc_gen_all(A,W)
    i = 0
    for subCirc in allSubCircs:
        print(f"{subCirc}: Index {i}")
        i+=1

    print(f"Extra affine columns:")
    affFrees = deBRAffConstructor.gen_aff_free(A,W)
    i = 0
    for affFree in affFrees:
        print(f"{affFree}: Index {i}")
        i+=1

    print(f"\n ALLONES AFFINE SHIFTER, COMPOSITION: {tuple(1 for i in range(W[1]))}")
    print("-----")
    onesShifter = deBRAffConstructor.shifter_gen_combo(W,tuple(1 for i in range(W[1])),affFrees[-1],allSubCircs)
    print(onesShifter)

    print(f"All generated cycles for allones shifter")
    print("-----")
    allWindows = deBRAffConstructor.gen_all_npWindows(A,W) # note windows are in base 10 order read bottom to top
    onesCycles,onesRings = deBRAffConstructor.gen_cycles(onesShifter,allWindows,A,W)
    for cycle in onesCycles:
        # prints each cycle as base 10 numbers in list 
        print(f"For Cycle {cycle[1]}:")
        if LONGOUTPUT:
            # prints each cycle as windows (turn off if A,W large)
            print(f"Windows: \n{cycle[0]}:")
        # if associated tori are desired, can be generated here
        tori = deBRAffConstructor.gen_tori(W,cycle[0])
        print(f"Torus associated to cycle: \n {tori}")
        print("-----")

    print(f"Power of shifter {deBRAffConstructor.get_power(onesShifter,A,W,True)}")
    print("-----")

    print(f"Is shifter invertible? {deBRAffConstructor.is_invert(onesShifter,A)}")
    print("-----")

if PRINTAFFINESANITY:
    print(f"\n \n \n FOR THE LINEAR AFFINE CASE \n \n \n")

    print(f"Generic affine shifter (-1 denotes free): \n {deBRAffConstructor.basic_shifter(W)}")

    print(f"Number of aperodic windows (same as linear case): \n {deBRConstructor.get_apNum(A,W)}")

    print(f"All sub-circs (same as linear case):")
    allSubCircs = deBRConstructor.subcirc_gen_all(A,W)
    i = 0
    for subCirc in allSubCircs:
        print(f"{subCirc}: Index {i}")
        i+=1

    print(f"Extra affine columns:")
    affFrees = deBRAffConstructor.gen_aff_free(A,W)
    i = 0
    for affFree in affFrees:
        print(f"{affFree}: Index {i}")
        i+=1

    print(f"\n ALLONES AFFINE SHIFTER, COMPOSITION: {tuple(1 for i in range(W[1]))}")
    print("-----")
    onesShifter = deBRAffConstructor.shifter_gen_combo(W,tuple(1 for i in range(W[1])),np.zeros((W[1],1),dtype=int),allSubCircs)
    print(onesShifter)

    print(f"All generated cycles for allones shifter")
    print("-----")
    allWindows = deBRAffConstructor.gen_all_npWindows(A,W) # note windows are in base 10 order read bottom to top
    onesCycles,onesRings = deBRAffConstructor.gen_cycles(onesShifter,allWindows,A,W)
    for cycle in onesCycles:
        # prints each cycle as base 10 numbers in list 
        print(f"For Cycle {cycle[1]}:")
        if LONGOUTPUT:
            # prints each cycle as windows (turn off if A,W large)
            print(f"Windows: \n{cycle[0]}:")
        # if associated tori are desired, can be generated here
        tori = deBRAffConstructor.gen_tori(W,cycle[0])
        print(f"Torus associated to cycle: \n {tori}")
        print("-----")

    print(f"Power of shifter {deBRAffConstructor.get_power(onesShifter,A,W,True)}")
    print("-----")

    print(f"Is shifter invertible? {deBRAffConstructor.is_invert(onesShifter,A)}")
    print("-----")
