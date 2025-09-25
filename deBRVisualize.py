import matplotlib.pyplot as plt
import numpy as np
import sympy as symp # used to determine factors of an integer
import deBRGen
import deBRValidation


try:
  VERBOSE
except NameError:
  VERBOSE = False
else:
  print("Verbose defined elsewhere")


# Due to other analysis, we just generate the powers of the shifters.
# Stores data into file OnlySuccessful_A_L_W.txt
def test_deBR_powers(A,W, wantData = True, wantSuccessful = False, graphData = False, histogram = False, wantCycles = False):
  data = []; powers = []; dets = []
  apN = deBRGen.gen_apNum(A,W) # gets apN through mobius function

  # file shenannigans 
  output = open(f"Cycles){wantCycles}_onlyAPN){wantSuccessful}_powers_{A}_{W[0]}_{W[1]}.txt", "w")
  output.write(f"Shifters for |A| = {A}, \n Window Size = {W} \n and {apN} aperiodic windows\n")

  allSs = deBRGen.gen_allShifter(A,W) # gets all shifters from all possible circs combos

  for shifter in allSs: # walks through shifters, checking pow. Shifter[0] is the shifter, shifter[1] is the composition of circs
    deBR =  deBRGen.gen_ring(shifter[0],apN,A,W)
    pow = deBRValidation.get_cyclen(shifter[0],A,apN,W) # Note: Power value of -1 means we hit the 0 matrix, value of -2 means we never settle on I
    det = np.linalg.det(shifter[0]) # det of deBR
    det = det % A # mod A
    det = int(det) # convert to int
    
    if wantSuccessful: # could clean up and remove a repetative codeblock here. Do in future?
      if pow == apN:
        data.append([shifter[1], pow, det]) # metrics
        powers.append(pow);dets.append(det)
        output.write(f"Shifter: {shifter[0]} \n Composition: {shifter[1]}\n Power: {pow}\n Determinant: {det}\n  deBR: {deBR}\n")
      if (apN/pow)%1 == 0 and pow > 0:
        output.write(f"Windows hit: \n")
        windowsHit = deBRGen.gen_cycle(shifter[0],A,W,apN,pow)
        for window in windowsHit:
          output.write(f"{window} ")
        output.write("\n")
    elif wantData:
        data.append([shifter[1], pow, det]) # metrics
        powers.append(pow);dets.append(det)
        output.write(f"Shifter: {shifter[0]} \n Composition: {shifter[1]}\n Power: {pow}\n Determinant: {det}\n  deBR: {deBR}\n")
    elif wantCycles:
      if pow != -2 and pow != -1:
        data.append([shifter[1], pow, det]) # metrics
        powers.append(pow);dets.append(det)
        output.write(f"Shifter: {shifter[0]} \n Composition: {shifter[1]}\n Power: {pow}\n Determinant: {det}\n  deBR: {deBR}\n")
          # each shifter's data is stored as: circs, pow, det. Easier for table
  histData = [powers,dets]
  if graphData:
    graph_powers(A,W,apN,data)
  if histogram:
    gen_histogram(A,W,apN,histData)
  return(data)



def graph_powers(A,W,apN,allData):
  # data stored as [ circs, power, det]
  # very hard to show deBR. 
  fig, ax = plt.subplots(); ax.axis("off")
  title = f'Power Analysis for A = {A}, \n Window Size = {W} \n and {apN} aperiodic windows'; fig.suptitle(title) # gen title
  cols = ["Circulants", "Power", "Determinant" ]
  table = ax.table(cellText = allData, colLabels = cols,cellLoc = "center", loc = "center")
  table.set_fontsize
  for i,data in enumerate(allData):
    if (apN/data[1])%1 == 0 and data[1] > 0: 
      cell = table[(i+1),1] # highlights factors
      cell.set_facecolor("#00FF0D")
    if data[1] == apN:
      cell = table[(i+1),1] # highlights perfect lengths
      cell.set_facecolor('#FFA500')
  fig.set_size_inches(6, apN)
  table.scale(1,6/apN)
  plt.savefig(title)
  return()

def gen_histogram(A,W,apN,allData):
  # data stored as [ [powers] , [dets]]
  # very hard to show deBR. 
  fig, ax = plt.subplots(2)
  title = f'Histograms for A = {A}, W = {W}, apN = {apN}'
  fig.suptitle(title)
  bins = np.arange(-2,apN+1,1)
  ax[0].title.set_text('Powers')
  ax[0].hist(allData[0], bins)  
  ax[1].title.set_text('Determinants')
  ax[1].hist(allData[1], bins)  
  fig.set_size_inches(apN/2, 6)
  plt.savefig(title)
  return()


# Runs through all deBRs for a specific Alphabet and Window size, and checks if they are unique, aperiodic and consistent.
# allPrint prints all data to terminal output
# wantSuccessful determines if we only want to see successful deBRs, or all attempted deBRs
# wantData determines if we want to store all the data to a list 
def test_deBRs(A,W,apN,wantData,wantSuccessful, wantCycles, allPrint = False):
  data = [];
  shifters = []; circComps = []; colFacts = []; colExpansions = []; uniqueness = []; perodicities = []; consistencies = []; powers = []; deBRs = [];
  allSs = deBRGen.gen_allShifter(A,W)
  for shifter in allSs:
    deBR =  deBRGen.gen_ring(shifter[0],apN,A,W)
    factors,isAperiodic,expanded = deBRValidation.check_aperiodic(deBR,A,W)
    isConsistent = deBRValidation.check_consistency(deBR,shifter[0],A,W)
    pow = deBRValidation.get_cyclen(shifter[0],A,apN,W)
    isUnique = deBRValidation.check_unique(deBR,A,W,apN)
    if allPrint:
      print(f"Shifter used (circs composition): \n {shifter[0]} {shifter[1]}")
      print(f"Col factors: \n {factors}")
      print(f"Col base expansions: \n {expanded}")
      print(f"Unique?, Aperiodic?, Consistent? and power cycle: \n {isUnique}, {isAperiodic}, {isConsistent}, {pow}")
      print(f"Attempted deBR: \n {deBR} \n")
    elif wantSuccessful:
      if isUnique and isAperiodic:
        shifters.append(shifter[0]); circComps.append(shifter[1]);colFacts.append(factors); colExpansions.append(expanded) # components
        uniqueness.append(isUnique); perodicities.append(isAperiodic); consistencies.append(isConsistent); powers.append(pow); deBRs.append(deBR) # metrics
    elif wantData:
      shifters.append(shifter[0]); circComps.append(shifter[1]);colFacts.append(factors); colExpansions.append(expanded) # components
      uniqueness.append(isUnique); perodicities.append(isAperiodic); consistencies.append(isConsistent); powers.append(pow); deBRs.append(deBR) # metrics
      # data stored as [ shifter, circs, col factors, col expansions, uniquness, perodicity, consistency, power, deBR]
    elif wantCycles:
      if pow != -2 and pow != -1:
        shifters.append(shifter[0]); circComps.append(shifter[1]);colFacts.append(factors); colExpansions.append(expanded) # components
        uniqueness.append(isUnique); perodicities.append(isAperiodic); consistencies.append(isConsistent); powers.append(pow); deBRs.append(deBR) # metrics
      
  data = [shifters, circComps, colFacts, colExpansions, uniqueness, perodicities, consistencies, powers, deBRs]
  return(data)


def print_data(data):
  print("Data as stored:")
  print("Shifters:");print("Very ugly, wont output")# print(data[0])
  print("Circ components:");print(data[1])
  print("DeBR Column Factors:");print(data[2])
  print("DeBR Column Expansions:");print(data[3])
  print("Uniqueness:");print(data[4])
  print("Perodicities:");print(data[5])
  print("Consistencies:");print(data[6])
  print("Powers:");print(data[7])
  print("GenRings:");print("Very ugly wont output")# print(data[7])
  return(0)


def graph_deBRs(A,W,apN,allData,succData):
  # data stored as [ shifter, circs, col factors, col expansions, uniquness, perodicity, consistency, power, deBR]
  # thus for plot we want indicies, 1,3,4,5,6,7] everything else is hard to plot and visualize
  # 1 and 3 (circs and col expansions) are plotted on the same x axis, reduces visual clutter and makes patterns more apparent.
  if succData: # if we only look at successfuls, then we know they are unique, aperodic and consistent. So we only plot the circs, cols and pows
    fig, ax = plt.subplots(1)
    title = f'Successful deBRs for |A| = {A}, \n Window Size = {W}'
    fig.suptitle(title)
  else:
    fig, axs = plt.subplots(2)
    ax = axs[0]
    title = f'Attempted deBRs for |A| = {A}, \n Window Size = {W}'
    fig.suptitle(title)
  # for readability
  circYs = allData[1]; colYs = allData[3]; uniques = allData[4]; perYs = allData[5]; consYs = allData[6]; powYs = allData[7];
  xs = np.arange(len(circYs),dtype = int)
  ax.title.set_text('Circs (red), cols (blue), pows (green)')
  ax.set_yticks(np.arange(-2,A**(W[0]*W[1]),1))

  # we plot green, then red, then blue. so if no green dot, but red. green under red. if no green or red, then both under blue.
  ax.scatter(xs, powYs, color = 'green')   # plots powers

  # plots circulants of each shifter
  for xe, ye in zip(xs, circYs):
    xes = []
    for i in range(len(ye)):
      xes.append(i*(1/apN)+xe) # done to show multiplicity
    ax.scatter(xes, ye, color = 'red')

  # plots each column of each deBR
  for xe, ye in zip(xs, colYs):
    xes = []
    for i in range(len(ye)):
      xes.append(i*(1/apN)+xe) # done to show multiplicity
    ax.scatter(xes, ye, color = 'blue')

  # if wish to see other metrics
  if not succData:
    axs[1].title.set_text('Unique, aperodic and consistent?')
    axs[1].imshow(np.array([uniques,perYs,consYs]).reshape(3,(len(perYs))), cmap='prism', aspect='auto')
    axs[1].set_xticks(xs);axs[1].set_yticklabels([' ', 'U',' ', 'AP',' ', 'C', ' '])#;axs[1].set_yticks([])

  ax.set_xticks(xs)
  fig.set_size_inches(20, 8)
  plt.savefig(title)
  return()
