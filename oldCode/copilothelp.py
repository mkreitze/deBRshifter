import tkinter as tk
from tkinter import filedialog

def string_to_matrix(s, cols=3):
  nums = [int(ch) for ch in s if ch.isdigit()]
  return [nums[i:i+cols] for i in range(0, len(nums), cols)]

def display_matrix(matrix):
  for widget in matrix_frame.winfo_children():
    widget.destroy()
  for r, row in enumerate(matrix):
    for c, val in enumerate(row):
      cell = tk.Label(matrix_frame, text=str(val), width=4, height=2, borderwidth=1, relief="solid")
      cell.grid(row=r, column=c, padx=2, pady=2)

def load_file():
  file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
  if file_path:
    with open(file_path, 'r') as f:
      data = f.read()
      matrix = string_to_matrix(data)
      display_matrix(matrix)

# GUI setup
root = tk.Tk()
root.title("Matrix Pattern Viewer")

load_button = tk.Button(root, text="Load Matrix from File", command=load_file)
load_button.pack(pady=10)

matrix_frame = tk.Frame(root)
matrix_frame.pack(pady=10)

root.mainloop()
