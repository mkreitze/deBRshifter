import deBRAffConstructor
import deBRConstructor
import numpy as np


W = (2,3) # defined as (length,width)
A = 2 # alphabet size


print(f"Generic shifter (-1 denotes free): \n {deBRConstructor.basic_shifter(W)}")

print(f"Generic affine shifter (-1 denotes free): \n {deBRAffConstructor.basic_shifter(W)}")

print(f"Number of aperodic windows: \n {deBRConstructor.get_apNum(A,W)}")

print(f"All sub-circs: (notice row in base 10 is index) ")
allSubCircs = deBRConstructor.subcirc_gen_all(A,W)
i = 0
for subCirc in allSubCircs:
    print(f"{subCirc}: Index {i}")
    i+=1

print(f"Shifter with circ comp {tuple(1 for i in range(W[1]))}")
onesShifter = deBRConstructor.shifter_gen_combo(W,tuple(1 for i in range(W[1])),allSubCircs)
print(onesShifter)

print(f"Is shifter invertible? {deBRConstructor.is_invert(onesShifter,A)}")

print(f"All generated cycles for shifter")
allWindows = deBRConstructor.gen_all_npWindows(A,W) # note windows are in base 10 order read bottom to top
onesCycles = deBRConstructor.gen_cycles(onesShifter,allWindows,A,W)
for cycle in onesCycles:
    # print(cycle[0])
    print(cycle[1])
    # if associated tori are desired, can be generated here
    window = deBRConstructor.convert_to_base_a(cycle[1][0],A,W[0]*W[1]);tori = deBRConstructor.gen_tori(onesShifter,A,W,len(cycle[1]),window)
    print(f"Torus associated to cycle: \n {tori}")
    print("Next")

print(f"Power of shifter {deBRConstructor.get_power(onesShifter,A,W)}")



# print(f"Affine Shifter with circ comp {tuple(1 for i in range(W[1]))}")
# onesShifter = deBRAffConstructor.shifter_gen_combo(W,tuple(1 for i in range(W[1])),allSubCircs)
# print(onesShifter)

# print(f"Is shifter invertible? {deBRAffConstructor.is_invert(onesShifter,A)}")

# print(f"All generated cycles for shifter")

# print(f"Power of shifter")

