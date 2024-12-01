import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd
from tabulate import tabulate

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")
        self.root.geometry("400x200")
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Choose an Application", font=("Helvetica", 14)).pack(pady=20)

        ttk.Button(self.root, text="CSV Column Selector", command=self.open_csv_column_selector).pack(pady=10)
        # Add more buttons here for other apps
        # ttk.Button(self.root, text="Another App", command=self.open_another_app).pack(pady=10)

    def open_csv_column_selector(self):
        self.root.withdraw()  # Hide the main window
        csv_selector_window = tk.Toplevel(self.root)
        CSVColumnSelector(csv_selector_window)

    # Define methods to open other apps here
    # def open_another_app(self):
    #     self.root.withdraw()
    #     another_app_window = tk.Toplevel(self.root)
    #     AnotherApp(another_app_window)

class CSVColumnSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Column Selector")
        self.root.geometry("600x300")
        self.file_path = tk.StringVar()
        self.df = None
        self.column_vars = {}
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

        ttk.Entry(file_frame, textvariable=self.file_path, width=50).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_file).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(file_frame, text="File").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        ttk.Button(self.root, text="Select and Edit Columns", command=self.select_columns).grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def browse_file(self):
        self.file_path.set(filedialog.askopenfilename())

    def select_columns(self):
        file_path = self.file_path.get()
        if file_path:
            self.df = pd.read_csv(file_path)
            self.show_column_selection()
        else:
            messagebox.showerror("Error", "No file selected.")

    def show_column_selection(self):
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Columns")
        selection_window.geometry("1200x600")

        frame = ttk.Frame(selection_window)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.column_vars = {col: tk.BooleanVar() for col in self.df.columns}
        self.selected_order = []  # List to track the order of selected columns

        for i, (col, var) in enumerate(self.column_vars.items()):
            row = i // 3  # 3 columns
            column = i % 3
            checkbutton = ttk.Checkbutton(frame, text=col, variable=var, command=lambda col=col: self.update_selected_order(col))
            checkbutton.grid(row=row, column=column, sticky='w')

        button_frame = ttk.Frame(selection_window)
        button_frame.grid(row=1, column=0, pady=10)

        ttk.Button(button_frame, text="Display Selected Columns", command=self.display_selected_columns).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Add New Column", command=self.add_new_column).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_selections).grid(row=0, column=3, padx=5)

        self.selected_columns_text = tk.Text(selection_window, height=10, wrap='none')
        self.selected_columns_text.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        scrollbar_y = ttk.Scrollbar(selection_window, orient='vertical', command=self.selected_columns_text.yview)
        scrollbar_y.grid(row=2, column=1, sticky='ns')
        self.selected_columns_text.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(selection_window, orient='horizontal', command=self.selected_columns_text.xview)
        scrollbar_x.grid(row=3, column=0, sticky='ew')
        self.selected_columns_text.configure(xscrollcommand=scrollbar_x.set)

        ttk.Button(selection_window, text="Save Selected Columns", command=self.save_selected_columns).grid(row=4, column=0, padx=10, pady=10)

    def update_selected_order(self, column):
        if self.column_vars[column].get():
            if column not in self.selected_order:
                self.selected_order.append(column)
        else:
            if column in self.selected_order:
                self.selected_order.remove(column)
        print(f"Selected order: {self.selected_order}")  # Debugging print statement

    def display_selected_columns(self):
        selected_columns = [col for col in self.selected_order if self.column_vars[col].get()]
        print(f"Displaying columns: {selected_columns}")  # Debugging print statement
        if not selected_columns:
            messagebox.showerror("Error", "No columns selected.")
            return

        self.selected_columns_text.delete(1.0, tk.END)
        table = tabulate(self.df[selected_columns], headers='keys', tablefmt='grid')
        self.selected_columns_text.insert(tk.END, table)

    def reset_selections(self):
        # Reset all checkbuttons
        for var in self.column_vars.values():
            var.set(False)
        # Clear the text widget
        self.selected_columns_text.delete(1.0, tk.END)
        # Clear the selected order
        self.selected_order.clear()
        print("Selections reset.")  # Debugging print statement

    def add_new_column(self):
        new_column_info = simpledialog.askstring("Add New Column", "Enter the name and default value of the new column (format: name,default_value):")
        if new_column_info:
            try:
                new_column_name, default_value = new_column_info.split(',', 1)  # Split only on the first comma
                print(f"Adding new column: {new_column_name} with default value: {default_value}")  # Debugging print statement
                self.df[new_column_name] = default_value  # Save the default value as a string
                self.column_vars[new_column_name] = tk.BooleanVar(value=True)
                self.selected_order.append(new_column_name)  # Add new column to selected order
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
        for i, (col, var) in enumerate(self.column_vars.items()):
            row = i // 3  # 3 columns
            column = i % 3
            checkbutton = ttk.Checkbutton(self.root, text=col, variable=var, command=lambda col=col: self.update_selected_order(col))
            checkbutton.grid(row=row, column=column, sticky='w')

    def save_selected_columns(self):
        selected_columns = [col for col in self.selected_order if self.column_vars[col].get()]
        if not selected_columns:
            messagebox.showerror("Error", "No columns selected.")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not output_file:
            return

        try:
            self.df[selected_columns].to_csv(output_file, index=False)
            messagebox.showinfo("Success", "Selected columns saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()