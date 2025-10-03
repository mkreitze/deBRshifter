import tkinter as tk

def search_matrix():
  input_string = entry.get()
  # You can process the input_string here to generate or search matrices
  print(f"Searching for pattern: {input_string}")
  # Add your matrix logic here

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
