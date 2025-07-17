import sympy as symp
import itertools as it
import numpy as np
import matplotlib.pyplot as plt
import collections as coll
from matplotlib.colors import ListedColormap
# INPUT: A; Alphabet, W; Window dimensions (standard work)
# OUTPUT: All 
def gen_p_windows(A,W):
    pWins = []
    facts = symp.divisors(W[0])
    facts.pop() # remove W[0] itself
    for d in facts:
    # note because the factors can themselves share factors, we are doing double work. I reason determining all UNIQUE factors will take more computation time than just doing the double work
        r = int(W[0]/d)
        repeatedPart = it.product(range(A),repeat = d*W[1])
        for repeat in repeatedPart:
            perWin = np.tile(np.array(repeat).reshape((d,W[1])),(r,1)) # generates perodic window: tiles the repeated piece vertically
            expWin = A**(np.array(np.arange(W[0]*W[1]-1,-1,-1)).reshape(W)) # generates expo convolution: Counts backwards, reforms
            exp = np.sum(perWin*expWin) # exponentiates and then sums all entries 
            pWins.append(exp)
    uniquePWins = np.unique(pWins)
    return(uniquePWins)

def imshow_via_mask(array,max,A,W): # A and W are just for title
    mask = np.isin(np.arange(max), array).astype(int)
    img = mask.reshape(1,-1)
    # METHOD 1
    # plt.figure(figsize = (10,2))
    # plt.imshow(img,cmap=ListedColormap(["white","orange"]), aspect='auto')
    # importantVals = np.where(mask == 1)[0]
    # plt.xticks(ticks = importantVals, labels = importantVals)
    # plt.yticks([])
    # plt.title(f"Perodic Windows for {A} {W}")
    # plt.savefig(f"Perodic Windows for {A} {W}")

    # METHOD 2
    importantVals = np.where(mask == 1)[0]
    plt.figure(figsize = (10,2))
    for x in importantVals:
        plt.bar(x,1,width=1.5,color='orange')
    plt.xlim(0,len(mask))
    plt.xticks(ticks = importantVals, labels = importantVals)
    plt.yticks([])
    plt.title(f"Perodic Windows for {A} {W}")
    plt.savefig(f"Perodic Windows for {A} {W}")

    return



#SIMULATION PARAMS

#there has to be some function, or something cool going on here. I am COMPLETELY unsure of what it is. 

As = [2,3]           
Ls = [2,3,4]
Ws = [2,3,4]
fileName = f"Periodic Windows As{As[0]},{As[-1]} Ls{Ls[0]},{Ls[-1]} Ws{Ws[0]},{Ws[-1]}"

# combines the factors of each periodic window counting one each (as repeated prime decomp messing what im looking for here) 
def combineDicts(facts):
    combinedFacts = coll.Counter() # Counter; supposedly a fast way to keep these all counted
    for f in facts: 
        for prime in f:
            combinedFacts[prime] += 1 # "flattening"
    combinedFacts = dict(sorted(combinedFacts.items()))
    return(combinedFacts)

# Takes a base 10  number and converts it to a 
def toBase(original,newBase,numOfDigits):
    digits = []
    while original > 0: 
        digits.append(original%newBase)
        original //= newBase
    while len(digits) < numOfDigits:
        digits.append(0)
    return list(reversed(digits))

with open(f"{fileName}.txt","w") as file:
    file.write(f"Perodic Windows for: \n A{As} \n L{Ls} \n W{Ws} \n")


for idx,A in enumerate(As):
    for idx2,W in enumerate(Ws):
        for idx3,L in enumerate(Ls):
            print(f"Non linear progress bar: {idx/len(As)*100}% As {idx2/len(Ws)*100}% Ws {idx3/len(Ls)*100}% Ls ")
            pWins = gen_p_windows(A,(L,W))
            maxNum = A**(L*W)-1
            imshow_via_mask(pWins,maxNum,A,(L,W));print(pWins) # generates our.. somewhat useful... images

            primePWs = pWins[np.vectorize(symp.isprime)(pWins)];print(primePWs) # finds the primes in the list (secondary thing tbh)

            facts = np.vectorize(symp.factorint)(pWins); # print(facts) # determines prime factorization of every pWin. VERY UGLY TO PRINT

            combinedFacts = combineDicts(facts);print(combinedFacts);print(len(pWins)) # checks occurance of each pWin's factors flattening to 1 contribution max per element

            primeWithSpecialOccurance = [p for p, count in combinedFacts.items() if count == len(pWins)-1];print(primeWithSpecialOccurance) # checks if these primes occur at least once in each pWin rep

            specialWindows = []
            for specialPrime in primeWithSpecialOccurance:
                specialWindows.append(np.array(toBase(specialPrime,A,L*W)).reshape(L,W))
            looksNice= np.hstack(specialWindows);print(f"Special 'window factors' (W = {W}): \n {looksNice}") # Turns these back into windows. As they are "window factors?" almost?

            with open(f"{fileName}.txt","a") as file:
                file.write(f"A {A} L {L} W {W} \n")
                file.write(f"{pWins}\n")
                file.write(f"{primePWs}\n")
                file.write(f"{combinedFacts}\n Number of primes: {len(pWins)} \n ")
                file.write(f"Every perodic window has the following factor (with 0 exception): {primeWithSpecialOccurance} \n")
                file.write(f"\"Function\": {A} {L} {W} -> {primeWithSpecialOccurance} \n")
                file.write(f"Special 'prime windows' (W= {W}): \n {looksNice} \n")

