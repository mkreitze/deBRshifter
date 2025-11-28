# ─── Imports ───────────────────────────────────────────────
import tkinter as tk
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import matplotlib.patches as patches # type: ignore
import os
from numpy.typing import NDArray  # type: ignore
import deBRConstructor
import typing as type
from matplotlib.ticker import MaxNLocator # type: ignore
# ───────────────────────────────────────────────────────────

# INFO
# Function to handle search button click
def search_matrix():
  input_string = entry.get()
  # You can process the input_string here to generate or search matrices
  print(f"Searching for pattern: {input_string}")
  # Add your matrix logic here

# INFO
#
def beautify_matrix(matrix : NDArray[int],gridLines : bool = True, border : bool = False, saveImage : bool = False, imageName : str = 'temp.png', seeOutput : bool = False):
  if os.path.exists("imageName"):
      print("File exists, not rerendering")
      return()

  fig, ax = plt.subplots(figsize=(len(matrix[0,:])*0.2, len(matrix[:,0])*0.2))
  ax.imshow(matrix, cmap='Greys')

  if gridLines == True:
    ax.set_xticks(np.arange(matrix.shape[1]));ax.set_yticks(np.arange(matrix.shape[0]));ax.set_xticks(np.arange(-0.5, matrix.shape[1], 1), minor=True);ax.set_yticks(np.arange(-0.5, matrix.shape[0], 1), minor=True) # sets major, then minor ticks
    ax.grid(which='minor', color='orange', linestyle='-', linewidth=0.5);ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False) #draws it 

  if border == True:
    rows, cols = matrix.shape # for drawing
    rect = patches.Rectangle( (-0.5, -0.5), cols, rows, linewidth=4, edgecolor='red', facecolor='none',zorder=2) # defines rect
    ax.add_patch(rect) # draws rect
  
  if saveImage == True:
    plt.savefig(f"{imageName}.png", bbox_inches='tight', dpi=300)
  
  if seeOutput == True:
    plt.show()
  plt.close()
  return()

# INFO
# We return the variance and average of the histogram incase we want the agg data later. Also intRep is unelegantly passed here
# outputs as [aperodic var, aperodic mean], [periodic var, periodic mean]
def gen_hist_from_cycle(cycles,W: type.Tuple[int,int],A: int,imageName = "temp.png",intRep: NDArray[int] = (0,0)) -> type.List[float]:
  aperodics = []; periodics = [];aPN=deBRConstructor.get_apNum(A,W)
  for cycle in cycles:
    if deBRConstructor.is_cycle_periodic(cycle[0][0],W,A):
      periodics.append(len(cycle[1]))
    else:
      aperodics.append(len(cycle[1]))

  # makes the hist
  fig, axes = plt.subplots(2, 1, figsize=(6, 8))
  bins = np.arange(0,aPN + 2) - 0.5
  axes[0].hist(aperodics, bins=bins, color='blue', alpha=0.7);  axes[1].hist(periodics, bins=bins, color='orange', alpha=0.7)
  axes[0].set_title("Aperodic");  axes[1].set_title("Periodics")
  axes[0].set_xlabel("Cycle Length");  axes[1].set_xlabel("Cycle Length")
  axes[0].set_ylabel("Frequency");  axes[1].set_ylabel("Frequency")
  axes[0].yaxis.set_major_locator(MaxNLocator(integer=True));  axes[1].yaxis.set_major_locator(MaxNLocator(integer=True))
  plt.tight_layout()
  plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
  # Save the figure instead of showing it
  plt.savefig(f"{imageName}.png")  # full path to folder + filename
  plt.close()  # closes the figure so it doesn’t display or overlap with future plots
  return([intRep,deBRConstructor.window_to_base10(intRep,A**W[1]),np.var(aperodics),np.mean(aperodics),np.var(periodics),np.mean(periodics)])

# INFO
#
def gen_agg(aggData: type.List[type.List[float]], imageName : str = "aggTemp.png"):
  xs = [data[1] for data in aggData]
  aperodicVars = [data[2] for data in aggData]
  aperodicMeans = [data[3] for data in aggData]
  periodicVars = [data[4] for data in aggData]
  periodicMeans = [data[5] for data in aggData]
  fig, axes = plt.subplots(2, 1, figsize=(6, 8))
  axes[0].errorbar(xs, aperodicMeans, yerr=aperodicVars, fmt='o', color='blue', ecolor='lightgray', elinewidth=3, capsize=0)
  axes[0].set_title("Aperodic Cycle Lengths");  axes[0].set_xlabel("Shifter (Base 10)");  axes[0].set_ylabel("Mean Cycle Length with Variance")
  axes[1].errorbar(xs, periodicMeans, yerr=periodicVars, fmt='o', color='orange', ecolor='lightgray', elinewidth=3, capsize=0)
  axes[1].set_title("Periodic Cycle Lengths");  axes[1].set_xlabel("Shifter (Base 10)");  axes[1].set_ylabel("Mean Cycle Length with Variance")
  axes[0].yaxis.set_major_locator(MaxNLocator(integer=True));  axes[1].yaxis.set_major_locator(MaxNLocator(integer=True))
  plt.tight_layout()
  plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
  plt.savefig(f"{imageName}.png")  # full path to folder + filename
  plt.close()  # closes the figure so it doesn’t display or overlap with future plots
  return()

if __name__ == '__main__':
  # Create the main window
  root = tk.Tk()
  root.title("Shifter Cycle Visualizer")

  # User inputs for search
  aVal = tk.Label(root, text="Alphabet Size:");aValEnter = tk.Entry(root, width=10)
  lVal = tk.Label(root, text="Length of window");lValEnter = tk.Entry(root, width=10)
  wVal = tk.Label(root, text="Width of window");wValEnter = tk.Entry(root, width=10)
  aVal.pack(pady=5);aValEnter.pack(pady=5);lVal.pack(pady=5);lValEnter.pack(pady=5)
  wVal.pack(pady=5);wValEnter.pack(pady=5)


  # Create a textbox (entry widget)

  # Create a button to trigger the search
  search_button = tk.Button(root, text="Search", command=search_matrix)
  search_button.pack(pady=10)

  # Run the GUI loop
  root.mainloop()
