import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd


class CsvMerger:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Merger")

        # Create labels and input fields for file paths
        self.file1_label = tk.Label(root, text="Select first CSV file:")
        self.file1_label.pack(pady=5)
        self.file1_path = tk.StringVar()
        self.file1_entry = tk.Entry(root, textvariable=self.file1_path, width=50)
        self.file1_entry.pack(pady=5)
        self.file1_button = tk.Button(root, text="Browse", command=self.browse_file1)
        self.file1_button.pack(pady=5)

        self.file2_label = tk.Label(root, text="Select second CSV file:")
        self.file2_label.pack(pady=5)
        self.file2_path = tk.StringVar()
        self.file2_entry = tk.Entry(root, textvariable=self.file2_path, width=50)
        self.file2_entry.pack(pady=5)
        self.file2_button = tk.Button(root, text="Browse", command=self.browse_file2)
        self.file2_button.pack(pady=5)

        # Create label and input field for output file path
        self.output_label = tk.Label(root, text="Save merged CSV file to:")
        self.output_label.pack(pady=5)
        self.output_path = tk.StringVar()
        self.output_entry = tk.Entry(root, textvariable=self.output_path, width=50)
        self.output_entry.pack(pady=5)
        self.output_button = tk.Button(root, text="Browse", command=self.browse_output)
        self.output_button.pack(pady=5)

        # Create a button to trigger the merging process
        self.merge_button = tk.Button(root, text="Merge CSV Files", command=self.merge_csv)
        self.merge_button.pack(pady=20)

    def browse_file1(self):
        self.file1_path.set(filedialog.askopenfilename(title="Select the first CSV file", filetypes=[("CSV files", "*.csv")]))

    def browse_file2(self):
        self.file2_path.set(filedialog.askopenfilename(title="Select the second CSV file", filetypes=[("CSV files", "*.csv")]))

    def browse_output(self):
        self.output_path.set(filedialog.asksaveasfilename(title="Save the merged CSV file", filetypes=[("CSV files", "*.csv")]))

    
    def merge_csv(self):
        file1 = self.file1_path.get()
        file2 = self.file2_path.get()
        output_file = self.output_path.get()

        if not all([file1, file2, output_file]):
            messagebox.showerror("Error", "Please select all files.")
            return

        try:
            df1 = pd.read_csv(file1)
            df2 = pd.read_csv(file2)

            # Reset indices to ensure correct merging
            df1 = df1.reset_index(drop=True)
            df2 = df2.reset_index(drop=True)

            # Merge DataFrames, setting column names explicitly
            merged_df = pd.concat([df1, df2], axis=1)
            
           # merged_df.columns = [f"Column_{i}" for i in range(len(merged_df.columns))]  # Assign clear column names
           # Drop any unnamed columns
            merged_df = merged_df.loc[:, ~merged_df.columns.str.contains('^Unnamed')]


            # Save the merged DataFrame to the specified output file
            merged_df.to_csv(output_file, index=False)
            messagebox.showinfo("Success", "Files merged successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "One or more files not found.")

        # Clear file paths after successful merge (optional)
        self.file1_path.set("")
        self.file2_path.set("")
        self.output_path.set("")


if __name__ == "__main__":
    root = tk.Tk()
    csv_merger = CsvMerger(root)
    root.mainloop()