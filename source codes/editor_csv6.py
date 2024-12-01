import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

class CSVColumnSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Column Selector")
        self.root.geometry("600x400")

        self.file1_path = tk.StringVar()
        self.file2_path = tk.StringVar()
        self.output_path = tk.StringVar()

        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a modern theme
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.configure('TLabel', font=('Helvetica', 10))
        self.style.configure('TEntry', font=('Helvetica', 10))

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        ttk.Label(self.root, text="File 1:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        ttk.Entry(self.root, textvariable=self.file1_path, width=50).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(self.root, text="Browse", command=self.browse_file1).grid(row=0, column=2, padx=10, pady=5)

        ttk.Label(self.root, text="File 2:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        ttk.Entry(self.root, textvariable=self.file2_path, width=50).grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(self.root, text="Browse", command=self.browse_file2).grid(row=1, column=2, padx=10, pady=5)

        ttk.Button(self.root, text="Merge and Select Columns", command=self.merge_and_select_columns).grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Instructions", command=self.show_instructions)

        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="About", command=self.show_about)

    def show_instructions(self):
        instructions = (
            "1. Click 'Browse' to select the first CSV file.\n"
            "2. Click 'Browse' to select the second CSV file.\n"
            "3. Click 'Merge and Select Columns' to open the column selection window.\n"
            "4. Select the columns you want to include from each file.\n"
            "5. Click 'Save Selected Columns' to save the merged file.\n"
            "6. Use the 'Reset' button to clear all selections."
        )
        messagebox.showinfo("Instructions", instructions)

    def show_about(self):
        about_text = (
            "CSV Column Selector\n"
            "Version 1.0\n"
            "Developed by [Your Name]\n"
            "This application allows you to merge columns from two CSV files and save the selected columns into a new CSV file."
        )
        messagebox.showinfo("About", about_text)

    def browse_file1(self):
        self.file1_path.set(filedialog.askopenfilename())

    def browse_file2(self):
        self.file2_path.set(filedialog.askopenfilename())

    def merge_and_select_columns(self):
        file1 = self.file1_path.get()
        file2 = self.file2_path.get()

        if not all([file1, file2]):
            messagebox.showerror("Error", "Please select both files.")
            return

        try:
            df1 = pd.read_csv(file1)
            df2 = pd.read_csv(file2)

            df1 = df1.reset_index(drop=True)
            df2 = df2.reset_index(drop=True)

            self.show_column_selection(df1, df2)
        except FileNotFoundError:
            messagebox.showerror("Error", "One or more files not found.")

    def show_column_selection(self, df1, df2):
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.title("Select Columns")
        self.selection_window.geometry("800x400")

        frame1 = ttk.Frame(self.selection_window)
        frame1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        canvas1 = tk.Canvas(frame1)
        scrollbar1 = ttk.Scrollbar(frame1, orient="vertical", command=canvas1.yview)
        scrollable_frame1 = ttk.Frame(canvas1)

        scrollable_frame1.bind(
            "<Configure>",
            lambda e: canvas1.configure(
                scrollregion=canvas1.bbox("all")
            )
        )

        canvas1.create_window((0, 0), window=scrollable_frame1, anchor="nw")
        canvas1.configure(yscrollcommand=scrollbar1.set)

        canvas1.pack(side="left", fill="both", expand=True)
        scrollbar1.pack(side="right", fill="y")

        self.column_vars1 = {}
        for i, column in enumerate(df1.columns):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(scrollable_frame1, text=column, variable=var)
            chk.grid(row=i, column=0, sticky='w')
            self.column_vars1[column] = var

        frame2 = ttk.Frame(self.selection_window)
        frame2.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        canvas2 = tk.Canvas(frame2)
        scrollbar2 = ttk.Scrollbar(frame2, orient="vertical", command=canvas2.yview)
        scrollable_frame2 = ttk.Frame(canvas2)

        scrollable_frame2.bind(
            "<Configure>",
            lambda e: canvas2.configure(
                scrollregion=canvas2.bbox("all")
            )
        )

        canvas2.create_window((0, 0), window=scrollable_frame2, anchor="nw")
        canvas2.configure(yscrollcommand=scrollbar2.set)

        canvas2.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")

        self.column_vars2 = {}
        for i, column in enumerate(df2.columns):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(scrollable_frame2, text=column, variable=var)
            chk.grid(row=i, column=0, sticky='w')
            self.column_vars2[column] = var

        button_frame = ttk.Frame(self.selection_window)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save Selected Columns", command=lambda: self.save_selected_columns(df1, df2)).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_selections).grid(row=0, column=1, padx=5)

    def reset_selections(self):
        for var in self.column_vars1.values():
            var.set(False)
        for var in self.column_vars2.values():
            var.set(False)

    def save_selected_columns(self, df1, df2):
        selected_columns1 = [col for col, var in self.column_vars1.items() if var.get()]
        selected_columns2 = [col for col, var in self.column_vars2.items() if var.get()]

        if not selected_columns1 or not selected_columns2:
            messagebox.showerror("Error", "No columns selected.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not output_file:
            return

        merged_df = pd.concat([df1[selected_columns1], df2[selected_columns2]], axis=1)
        merged_df.to_csv(output_file, index=False)
        messagebox.showinfo("Success", "Selected columns saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVColumnSelector(root)
    root.mainloop()