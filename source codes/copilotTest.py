import tkinter as tk
from tkinter import filedialog

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        path_label.config(text=file_path)

def submit_file():
    file_path = path_label.cget("text")
    if file_path:
        # Here you can add the code to process the file
        print(f"File submitted: {file_path}")

# Create the main window
root = tk.Tk()
root.title("File Selector")

# Create a button to select a file
select_button = tk.Button(root, text="Select File", command=select_file)
select_button.pack(pady=10)

# Create a label to display the selected file path
path_label = tk.Label(root, text="")
path_label.pack(pady=10)

# Create a button to submit the file
submit_button = tk.Button(root, text="Submit File", command=submit_file)
submit_button.pack(pady=10)

# Run the application
root.mainloop()