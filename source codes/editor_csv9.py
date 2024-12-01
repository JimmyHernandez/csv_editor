import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd

class CSVColumnSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Column Selector")
        self.root.geometry("600x300")

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
        file_frame = ttk.Frame(self.root, padding="10 10 10 10")
        file_frame.grid(row=0, column=0, columnspan=3, sticky='ew')

        ttk.Label(file_frame, text="File 1:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        ttk.Entry(file_frame, textvariable=self.file1_path, width=50).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_file1).grid(row=0, column=2, padx=10, pady=5)

        ttk.Label(file_frame, text="File 2:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        ttk.Entry(file_frame, textvariable=self.file2_path, width=50).grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_file2).grid(row=1, column=2, padx=10, pady=5)

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
            "5. Click 'Display Selected Columns' to review your selections.\n"
            "6. Click 'Save Selected Columns' to save the merged file.\n"
            "7. Use the 'Reset' button to clear all selections."
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
            self.df1 = pd.read_csv(file1)
            self.df2 = pd.read_csv(file2)

            self.df1 = self.df1.reset_index(drop=True)
            self.df2 = self.df2.reset_index(drop=True)

            self.show_column_selection(self.df1, self.df2)
        except FileNotFoundError:
            messagebox.showerror("Error", "One or more files not found.")
        except pd.errors.EmptyDataError:
            messagebox.showerror("Error", "One or more files are empty.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_column_selection(self, df1, df2):
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.title("Select Columns")
        self.selection_window.geometry("1200x600")

        # Frame 1
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
            chk = ttk.Checkbutton(scrollable_frame1, text=column, variable=var, command=self.update_canvas3)
            chk.grid(row=i, column=0, sticky='w')
            self.column_vars1[column] = var

        # Frame 2
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
            chk = ttk.Checkbutton(scrollable_frame2, text=column, variable=var, command=self.update_canvas3)
            chk.grid(row=i, column=0, sticky='w')
            self.column_vars2[column] = var

        # Frame 3
        frame3 = ttk.Frame(self.selection_window)
        frame3.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        canvas3 = tk.Canvas(frame3)
        scrollbar3 = ttk.Scrollbar(frame3, orient="vertical", command=canvas3.yview)
        self.scrollable_frame3 = ttk.Frame(canvas3)

        self.scrollable_frame3.bind(
            "<Configure>",
            lambda e: canvas3.configure(
                scrollregion=canvas3.bbox("all")
            )
        )

        canvas3.create_window((0, 0), window=self.scrollable_frame3, anchor="nw")
        canvas3.configure(yscrollcommand=scrollbar3.set)

        canvas3.pack(side="left", fill="both", expand=True)
        scrollbar3.pack(side="right", fill="y")

        # Button frame
        button_frame = ttk.Frame(self.selection_window)
        button_frame.grid(row=1, column=0, columnspan=3, pady=10)

        ttk.Button(button_frame, text="Display Selected Columns", command=self.display_selected_columns).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_selections).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Rename Columns", command=self.rename_columns).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Add New Column", command=self.add_new_column).grid(row=0, column=3, padx=5)

        self.selected_columns_text = tk.Text(self.selection_window, height=10, wrap='none')
        self.selected_columns_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

        scrollbar_y = ttk.Scrollbar(self.selection_window, orient='vertical', command=self.selected_columns_text.yview)
        scrollbar_y.grid(row=2, column=3, sticky='ns')
        self.selected_columns_text.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(self.selection_window, orient='horizontal', command=self.selected_columns_text.xview)
        scrollbar_x.grid(row=3, column=0, columnspan=3, sticky='ew')
        self.selected_columns_text.configure(xscrollcommand=scrollbar_x.set)

        ttk.Button(self.selection_window, text="Save Selected Columns", command=lambda: self.save_selected_columns(df1, df2)).grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def update_canvas3(self):
        # Clear the current widgets in canvas3
        for widget in self.scrollable_frame3.winfo_children():
            widget.destroy()

        # Create a new list to store the selected columns
        self.selected_columns_list = []

        # Collect selected columns from both column_vars1 and column_vars2
        selected_columns = [col for col, var in self.column_vars1.items() if var.get()]
        selected_columns += [col for col, var in self.column_vars2.items() if var.get()]

        # Add the selected columns to the new list
        self.selected_columns_list.extend(selected_columns)

        # Display the selected columns in canvas3 with checkboxes
        self.canvas3_vars = {}
        for i, column in enumerate(self.selected_columns_list):
            var = tk.BooleanVar()
            self.canvas3_vars[column] = var
            chk = ttk.Checkbutton(self.scrollable_frame3, text=column, variable=var)
            chk.grid(row=i, column=0, sticky='w')
        

    def reset_selections(self):
        for var in self.column_vars1.values():
            var.set(False)
        for var in self.column_vars2.values():
            var.set(False)
        self.update_canvas3()

    def rename_columns(self):
        selected_columns = [col for col, var in self.canvas3_vars.items() if var.get()]

        if not selected_columns:
            messagebox.showerror("Error", "No columns selected.")
            return

        for column in selected_columns:
            new_name = simpledialog.askstring("Rename Column", f"Enter new name for column '{column}':")
            if new_name:
                if column in self.column_vars1:
                    self.column_vars1[new_name] = self.column_vars1.pop(column)
                elif column in self.column_vars2:
                    self.column_vars2[new_name] = self.column_vars2.pop(column)
        self.update_canvas3()  # Update the list after renaming

    def add_new_column(self):
        new_column_info = simpledialog.askstring("Add New Column", "Enter the name and default value of the new column (format: name,default_value):")
        if new_column_info:
            try:
                new_column_name, default_value = new_column_info.split(',')
            except ValueError:
                messagebox.showerror("Error", "Invalid format. Please enter the data in the format: name,default_value")
                return

            self.column_vars1[new_column_name] = tk.BooleanVar(value=True)
            for df in [self.df1]:
                df[new_column_name] = default_value
            self.update_canvas3()

    def display_selected_columns(self):
        selected_columns1 = [col for col, var in self.column_vars1.items() if var.get()]
        selected_columns2 = [col for col, var in self.column_vars2.items() if var.get()]

        if not selected_columns1 and not selected_columns2:
            messagebox.showerror("Error", "No columns selected.")
            return

        try:
            # Debugging: Print selected columns and DataFrame columns
            print("Selected columns from df1:", selected_columns1)
            print("Selected columns from df2:", selected_columns2)
            print("Columns in df1:", self.df1.columns.tolist())
            print("Columns in df2:", self.df2.columns.tolist())

            # Merge the selected columns from both DataFrames
            merged_df = pd.concat([self.df1[selected_columns1], self.df2[selected_columns2]], axis=1)

            # Display the merged DataFrame in the text widget
            self.selected_columns_text.delete(1.0, tk.END)
            self.selected_columns_text.insert(tk.END, merged_df.to_string(index=False))
        except KeyError as e:
            messagebox.showerror("Error", f"Column not found: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while displaying the columns: {e}")

    def save_selected_columns(self, df1, df2):
        new_edited_list = [col for col, var in self.selected_columns_list.extend() if var.get()]
        
        if not new_edited_list:
            messagebox.showerror("Error", "No columns selected.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not output_file:
            return

        try:
            new_edited_list.to_csv(output_file, index=False)
            messagebox.showinfo("Success", "Selected columns saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVColumnSelector(root)
    root.mainloop()