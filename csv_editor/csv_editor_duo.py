import csv_editor_duo
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import pandas as pd
from tabulate import tabulate

class CSVEditorDuo:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Column Selector")
        self.root.geometry("600x300")
        self.file_path1 = tk.StringVar()
        self.file_path2 = tk.StringVar()
        self.df1 = None
        self.df2 = None
        self.column_vars1 = {}
        self.column_vars2 = {}
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TEntry', font=('Helvetica', 10))

    def create_widgets(self):
        file_frame = ttk.Frame(self.root)
        file_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        ttk.Entry(file_frame, textvariable=self.file_path1, width=50).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(file_frame, text="Browse File 1", command=lambda: self.browse_file(self.file_path1)).grid(row=0, column=1, padx=10, pady=5)
        ttk.Entry(file_frame, textvariable=self.file_path2, width=50).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(file_frame, text="Browse File 2", command=lambda: self.browse_file(self.file_path2)).grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(self.root, text="Select and Edit Columns", command=self.select_columns).grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def browse_file(self, file_path_var):
        file_path_var.set(filedialog.askopenfilename())

    def select_columns(self):
        file_path1 = self.file_path1.get()
        file_path2 = self.file_path2.get()
        if file_path1 and file_path2:
            self.df1 = pd.read_csv(file_path1)
            self.df2 = pd.read_csv(file_path2)
            self.show_column_selection()
        else:
            messagebox.showerror("Error", "Both files must be selected.")

    def show_column_selection(self):
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Columns")
        selection_window.geometry("1200x600")

        # Frame for File 1 columns
        frame1 = ttk.Frame(selection_window)
        frame1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.column_vars1 = {col: tk.BooleanVar() for col in self.df1.columns}
        self.selected_order1 = []  # List to track the order of selected columns from file 1

        for i, (col, var) in enumerate(self.column_vars1.items()):
            row = i // 13  # 13 columns per row
            column = i % 13
            checkbutton = ttk.Checkbutton(frame1, text=col, variable=var, command=lambda col=col: self.update_selected_order(col, 1))
            checkbutton.grid(row=row, column=column, sticky='w')

        # Frame for File 2 columns
        frame2 = ttk.Frame(selection_window)
        frame2.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.column_vars2 = {col: tk.BooleanVar() for col in self.df2.columns}
        self.selected_order2 = []  # List to track the order of selected columns from file 2

        for i, (col, var) in enumerate(self.column_vars2.items()):
            row = i // 13  # 13 columns per row
            column = i % 13
            checkbutton = ttk.Checkbutton(frame2, text=col, variable=var, command=lambda col=col: self.update_selected_order(col, 2))
            checkbutton.grid(row=row, column=column, sticky='w')

        button_frame = ttk.Frame(selection_window)
        button_frame.grid(row=2, column=0, pady=10)

        ttk.Button(button_frame, text="Display Selected Columns", command=self.display_selected_columns).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Add New Column", command=self.add_new_column).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_selections).grid(row=0, column=3, padx=5)

        self.selected_columns_text = tk.Text(selection_window, height=10, wrap='none')
        self.selected_columns_text.grid(row=3, column=0, padx=10, pady=10, sticky='ew')

        scrollbar_y = ttk.Scrollbar(selection_window, orient='vertical', command=self.selected_columns_text.yview)
        scrollbar_y.grid(row=3, column=1, sticky='ns')
        self.selected_columns_text.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(selection_window, orient='horizontal', command=self.selected_columns_text.xview)
        scrollbar_x.grid(row=4, column=0, sticky='ew')
        self.selected_columns_text.configure(xscrollcommand=scrollbar_x.set)

        ttk.Button(selection_window, text="Save Selected Columns", command=self.save_selected_columns).grid(row=5, column=0, padx=10, pady=10)

    def update_selected_order(self, column, file_number):
        if file_number == 1:
            if self.column_vars1[column].get():
                if column not in self.selected_order1:
                    self.selected_order1.append(column)
            else:
                if column in self.selected_order1:
                    self.selected_order1.remove(column)
            print(f"Selected order for file 1: {self.selected_order1}")  # Debugging print statement
        else:
            if self.column_vars2[column].get():
                if column not in self.selected_order2:
                    self.selected_order2.append(column)
            else:
                if column in self.selected_order2:
                    self.selected_order2.remove(column)
            print(f"Selected order for file 2: {self.selected_order2}")  # Debugging print statement

    def display_selected_columns(self):
        selected_columns1 = [col for col in self.selected_order1 if self.column_vars1[col].get()]
        selected_columns2 = [col for col in self.selected_order2 if self.column_vars2[col].get()]
        print(f"Displaying columns from file 1: {selected_columns1}")  # Debugging print statement
        print(f"Displaying columns from file 2: {selected_columns2}")  # Debugging print statement
        if not selected_columns1 and not selected_columns2:
            messagebox.showerror("Error", "No columns selected.")
            return

        self.selected_columns_text.delete(1.0, tk.END)
        if selected_columns1 or selected_columns2:
            merged_df = pd.concat([self.df1[selected_columns1], self.df2[selected_columns2]], axis=1)
            table = tabulate(merged_df, headers='keys', tablefmt='grid')
            self.selected_columns_text.insert(tk.END, table)

    def reset_selections(self):
        # Reset all checkbuttons
        for var in self.column_vars1.values():
            var.set(False)
        for var in self.column_vars2.values():
            var.set(False)
        # Clear the text widget
        self.selected_columns_text.delete(1.0, tk.END)
        # Clear the selected order
        self.selected_order1.clear()
        self.selected_order2.clear()
        print("Selections reset.")  # Debugging print statement

    def add_new_column(self):
        new_column_info = simpledialog.askstring("Add New Column", "Enter the name and default value of the new column (format: name,default_value):")
        if new_column_info:
            try:
                new_column_name, default_value = new_column_info.split(',', 1)  # Split only on the first comma
                print(f"Adding new column: {new_column_name} with default value: {default_value}")  # Debugging print statement
                self.df1[new_column_name] = default_value  # Save the default value as a string
                self.column_vars1[new_column_name] = tk.BooleanVar(value=True)
                self.selected_order1.append(new_column_name)  # Add new column to selected order
                self.update_checkbuttons()  # Update the checkbuttons
                self.display_selected_columns()  # Refresh the display of selected columns
            except ValueError:
                messagebox.showerror("Error", "Invalid format. Please use 'name,default_value'.")

    def update_checkbuttons(self):
        # Clear existing checkbuttons
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Checkbutton):
                widget.destroy()

        # Recreate checkbuttons with updated columns
        for i, (col, var) in enumerate(self.column_vars1.items()):
            row = i // 3  # 3 columns per row
            column = i % 3
            checkbutton = ttk.Checkbutton(self.root, text=col, variable=var, command=lambda col=col: self.update_selected_order(col, 1))
            checkbutton.grid(row=row, column=column, sticky='w')

        for i, (col, var) in enumerate(self.column_vars2.items()):
            row = (i + len(self.column_vars1)) // 3  # Continue from where the first set of columns ended
            column = (i + len(self.column_vars1)) % 3
            checkbutton = ttk.Checkbutton(self.root, text=col, variable=var, command=lambda col=col: self.update_selected_order(col, 2))
            checkbutton.grid(row=row, column=column, sticky='w')

    def save_selected_columns(self):
        selected_columns1 = [col for col in self.selected_order1 if self.column_vars1[col].get()]
        selected_columns2 = [col for col in self.selected_order2 if self.column_vars2[col].get()]
        if not selected_columns1 and not selected_columns2:
            messagebox.showerror("Error", "No columns selected.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not output_file:
            return

        try:
            merged_df = pd.concat([self.df1[selected_columns1], self.df2[selected_columns2]], axis=1)
            merged_df.to_csv(output_file, index=False)
            messagebox.showinfo("Success", "Selected columns saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEditorDuo(root)
    root.mainloop()
