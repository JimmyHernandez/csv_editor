import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog, Menu
import pandas as pd
from tabulate import tabulate
from time import strftime 

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Newtron Solutions")
        self.root.geometry("650x350")
        #self.root.configure(bg='#00a5b5') 
        self.create_widgets()

    def create_widgets(self):
        file_frame2 = ttk.Frame(self.root)
        file_frame2.pack(padx=10, pady=35)
        text_var = tk.StringVar()
        text_var.set("CSV EDITOR")
        label = tk.Label(file_frame2,
                textvariable=text_var, 
                 #bg="#00a5b5",      
                 height=3,              
                 width=20,              
                 bd=3,                  
                 font=("Arial", 20), 
                 cursor="hand2",   
                 fg="Black",             
                 padx=15,               
                 pady=15,                
                 justify=tk.CENTER,    
                 relief=tk.RAISED,     
                 underline=0,           
                 wraplength=250         
                )
        label.pack(pady=20) 
        button = ttk.Button(file_frame2, text="Open CSV- Single Editor", command=self.open_csv_single_editor)
        button.pack(pady=10)
        button.configure(style="TButton")

        # Apply the same background color to ttk widgets
        style1 = ttk.Style()
        #style1.configure("TButton", background='#00a5b5')
        style1.configure("TButton", font=("Arial", 14))
        #style1.configure("TFrame", background='#00a5b5')
        
        # Creating Menubar 
        menubar = Menu(self.root) 
        
        # Adding File Menu and commands 
        file = Menu(menubar, tearoff = 0) 
        menubar.add_cascade(label ='File', menu = file) 
        #file.add_command(label ='New File', command = None) 
        #file.add_command(label ='Open...', command = None) 
        #file.add_command(label ='Save', command = None) 
        file.add_separator() 
        file.add_command(label ='Exit', command = self.root.destroy) 
        
        # Adding Edit Menu and commands 
        #edit = Menu(menubar, tearoff = 0) 
        #menubar.add_cascade(label ='Edit', menu = edit) 
        #edit.add_command(label ='Cut', command = None) 
        #edit.add_command(label ='Copy', command = None) 
        #edit.add_command(label ='Paste', command = None) 
        #edit.add_command(label ='Select All', command = None) 
        #edit.add_separator() 
        #edit.add_command(label ='Find...', command = None) 
        #edit.add_command(label ='Find again', command = None) 
        
        # Adding Help Menu 
        help_ = Menu(menubar, tearoff = 0) 
        menubar.add_cascade(label ='Help', menu = help_) 
        help_.add_command(label ='Intrucciones', command = None) 
        help_.add_separator() 
        help_.add_command(label ='About CSV Editor', command = None) 

        self.root.config(menu = menubar) 

    def open_csv_single_editor(self):
        self.root.withdraw()  # Hide the main window
        editor_window = tk.Toplevel(self.root)
        #editor_window.configure(bg='#00a5b5')
        CSVEditorSingle(editor_window, self.show_main_window)  # Pass the function to show the main window

    def show_main_window(self):
        self.root.deiconify()


class CSVEditorSingle:
    def __init__(self, root, go_back_to_main):
        self.root = root
        self.go_back_to_main = go_back_to_main
        self.root.title("CSV Column Selector")
        self.root.geometry("700x400")
        self.file_path = tk.StringVar()
        self.df = None
        self.column_vars = {}
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style2 = ttk.Style()
        style2.configure('TButton', font=('Helvetica', 12), background='SystemButtonFace')
        style2.configure('TLabel', font=('Helvetica', 15))
        style2.configure('TEntry', font=('Helvetica', 15))

    def create_widgets(self):
        file_frame = ttk.Frame(self.root)

        text_var = tk.StringVar()
        text_var.set("Single Editor")

        label = tk.Label(file_frame,
                         textvariable=text_var,
                         height=3,
                         width=30,
                         bd=3,
                         font=("Arial", 20),
                         cursor="hand2",
                         fg="red",
                         padx=15,
                         pady=15,
                         justify=tk.CENTER,
                         relief=tk.RAISED,
                         underline=0,
                         wraplength=250
                         )
        label.pack(pady=20)

        file_frame.pack(padx=10, pady=35)
        ttk.Entry(file_frame, textvariable=self.file_path, width=75).pack(fill=tk.X)
        ttk.Button(file_frame, text="Browse File", command=self.browse_file).pack(pady=5)
        ttk.Button(file_frame, text="Select and Edit Columns", command=self.select_columns).pack(pady=5)
        ttk.Button(file_frame, text="Main Menu", command=self.go_back).pack(pady=5)

    def browse_file(self):
        self.file_path.set(filedialog.askopenfilename())

    def select_columns(self):
        file_path = self.file_path.get()
        if file_path:
            self.df = pd.read_csv(file_path)
            self.df = self.df.apply(lambda x: x.str.strip() if x.dtype == "object" else x).replace('', None)
            self.show_column_selection()
        else:
            messagebox.showerror("Error", "No file selected.")

    def show_column_selection(self):
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.title("Select Columns")
        self.selection_window.geometry("1200x600")

        frame = ttk.Frame(self.selection_window)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.column_vars = {col: tk.BooleanVar() for col in self.df.columns}
        self.selected_order = []

        for i, (col, var) in enumerate(self.column_vars.items()):
            row = i // 13
            column = i % 13
            checkbutton = ttk.Checkbutton(frame, text=col, variable=var, command=lambda col=col: self.update_selected_order(col))
            checkbutton.grid(row=row, column=column, sticky='w')

        button_frame = ttk.Frame(self.selection_window)
        button_frame.grid(row=1, column=0, pady=10)

        ttk.Button(button_frame, text="Display Selected Columns", command=self.display_selected_columns).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Add New Column", command=self.add_new_column).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_selections).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Back", command=self.go_back).grid(row=0, column=4, padx=5)

        self.selected_columns_text = tk.Text(self.selection_window, height=10, wrap='none')
        self.selected_columns_text.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        scrollbar_y = ttk.Scrollbar(self.selection_window, orient='vertical', command=self.selected_columns_text.yview)
        scrollbar_y.grid(row=2, column=1, sticky='ns')
        self.selected_columns_text.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(self.selection_window, orient='horizontal', command=self.selected_columns_text.xview)
        scrollbar_x.grid(row=3, column=0, sticky='ew')
        self.selected_columns_text.configure(xscrollcommand=scrollbar_x.set)

        ttk.Button(self.selection_window, text="Save Selected Columns", command=self.save_selected_columns).grid(row=4, column=0, padx=10, pady=10)

    def update_selected_order(self, col):
        if self.column_vars[col].get():
            self.selected_order.append(col)
        else:
            self.selected_order.remove(col)

    def display_selected_columns(self):
        selected_columns = [col for col, var in self.column_vars.items() if var.get()]
        self.selected_columns_text.delete(1.0, tk.END)
        self.selected_columns_text.insert(tk.END, ', '.join(selected_columns))

    def show_column_selection(self):
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.title("Select Columns")
        self.selection_window.geometry("1200x600")

        frame = ttk.Frame(self.selection_window)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.column_vars = {col: tk.BooleanVar() for col in self.df.columns}
        self.selected_order = []  # List to track the order of selected columns

        for i, (col, var) in enumerate(self.column_vars.items()):
            row = i // 13  # 13 columns
            column = i % 13
            checkbutton = ttk.Checkbutton(frame, text=col, variable=var, command=lambda col=col: self.update_selected_order(col))
            checkbutton.grid(row=row, column=column, sticky='w')

        button_frame = ttk.Frame(self.selection_window)
        button_frame.grid(row=1, column=0, pady=10)

        ttk.Button(button_frame, text="Display Selected Columns", command=self.display_selected_columns).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Add New Column", command=self.add_new_column).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_selections).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Back", command=self.go_back).grid(row=0, column=4, padx=5)  # Back button

        self.selected_columns_text = tk.Text(self.selection_window, height=10, wrap='none')
        self.selected_columns_text.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        scrollbar_y = ttk.Scrollbar(self.selection_window, orient='vertical', command=self.selected_columns_text.yview)
        scrollbar_y.grid(row=2, column=1, sticky='ns')
        self.selected_columns_text.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(self.selection_window, orient='horizontal', command=self.selected_columns_text.xview)
        scrollbar_x.grid(row=3, column=0, sticky='ew')
        self.selected_columns_text.configure(xscrollcommand=scrollbar_x.set)

        ttk.Button(self.selection_window, text="Save Selected Columns", command=self.save_selected_columns).grid(row=4, column=0, padx=10, pady=10)

    def go_back(self):
        self.root.destroy()
        self.go_back_to_main()

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
            row = i // 13  # 13 columns
            column = i % 13
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

def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()