import deBRAffConstructor
import deBRConstructor

W = (2,3) # defined as (length,width)
A = 2 # alphabet size


print(f"Generic shifter: \n {deBRConstructor.basic_shifter(W)}")

print(f"Generic affine shifter: \n {deBRAffConstructor.basic_shifter(W)}")


