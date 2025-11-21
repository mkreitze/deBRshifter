# ─── Imports ───────────────────────────────────────────────
import tkinter as tk
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import matplotlib.patches as patches # type: ignore
import os
from numpy.typing import NDArray  # type: ignore
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
  ax.imshow(matrix, cmap='grey')

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
  

if __name__ == '__main__':
  # Create the main window
  root = tk.Tk()
  root.title("Shifter Cycle Visualizer")

  # User inputs for search
  aVal = tk.Label(root, text="Alphabet Size:");aValEnter = tk.Entry(root, width=10)
  lVal = tk.Label(root, text="Length of window");lValEnter = tk.Entry(root, width=10)
  wVal = tk.Label(root, text="Width of window");wValEnter = tk.Entry(root, width=10)
  aVal.pack(pady=5);aValEnter.pack(pady=5);lVal.pack(pady=5);lValEnter.pack(pady=5);
  wVal.pack(pady=5);wValEnter.pack(pady=5);


  # Create a textbox (entry widget)

  # Create a button to trigger the search
  search_button = tk.Button(root, text="Search", command=search_matrix)
  search_button.pack(pady=10)

  # Run the GUI loop
  root.mainloop()
