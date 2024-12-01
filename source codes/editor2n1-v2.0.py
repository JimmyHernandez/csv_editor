import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk, scrolledtext
import pandas as pd
import logging
from pathlib import Path
import os
import sys

# Initialize undo/redo stacks
undo_stack = []
redo_stack = []
combined_listbox = []


def save_state():
    # Save the current state of the combined listbox for undo functionality
    state = combined_listbox.get(0, tk.END)
    undo_stack.append(state)
    redo_stack.clear()

def undo():
    if undo_stack:
        state = undo_stack.pop()
        redo_stack.append(combined_listbox.get(0, tk.END))
        combined_listbox.delete(0, tk.END)
        for item in state:
            combined_listbox.insert(tk.END, item)

def redo():
    if redo_stack:
        state = redo_stack.pop()
        undo_stack.append(combined_listbox.get(0, tk.END))
        combined_listbox.delete(0, tk.END)
        for item in state:
            combined_listbox.insert(tk.END, item)

def add_column_to_combined():
    new_column = simpledialog.askstring("Agregar columna", "Ingrese el nombre de la nueva columna:")
    if new_column:
        combined_listbox.insert(tk.END, new_column)
        
def procesar_csv(archivo_csv1, campos_a_extraer1, archivo_csv2, campos_a_extraer2):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        logging.info("Validating file paths...")
        if not os.path.isfile(archivo_csv1):
            raise FileNotFoundError(f"El archivo CSV no existe: {archivo_csv1}")
        if not os.path.isfile(archivo_csv2):
            raise FileNotFoundError(f"El archivo CSV no existe: {archivo_csv2}")

        logging.info("Reading CSV files...")
        df1 = pd.read_csv(archivo_csv1)
        df2 = pd.read_csv(archivo_csv2)

        if df1.empty or df2.empty:
            raise ValueError("Uno de los archivos CSV está vacío.")

        logging.info("Extracting specified columns...")
        df_nuevo1 = df1[campos_a_extraer1]
        df_nuevo2 = df2[campos_a_extraer2]

        logging.info("Reindexing DataFrames...")
        max_rows = max(len(df_nuevo1), len(df_nuevo2))
        df_nuevo1 = df_nuevo1.reindex(range(max_rows)).fillna('')
        df_nuevo2 = df_nuevo2.reindex(range(max_rows)).fillna('')

        logging.info("Combining DataFrames...")
        df_combined = pd.concat([df_nuevo1.reset_index(drop=True), df_nuevo2.reset_index(drop=True)], axis=1)

        

        nuevo_archivo = simpledialog.askstring("Nombre del archivo de salida", "Ingrese el nombre del archivo de salida (sin la extensión .csv):")
        if not nuevo_archivo:
            raise ValueError("Debe ingresar un nombre para el archivo de salida.")

        nuevo_archivo = "".join([c for c in nuevo_archivo if c.isalpha() or c.isdigit() or c in (' ', '.', '_')]).rstrip()

        save_path = filedialog.askdirectory(title="Seleccione la ubicación para guardar el archivo")
        if not save_path:
            raise ValueError("Debe seleccionar una ubicación para guardar el archivo.")

        nuevo_archivo_path = Path(save_path) / f"{nuevo_archivo}.csv"

        contador = 1
        while nuevo_archivo_path.exists():
            nuevo_archivo_path = nuevo_archivo_path.with_stem(f"{nuevo_archivo_path.stem}_{contador}")
            logging.warning(f"El archivo {nuevo_archivo_path} ya existe. Se intentará con un nombre diferente.")
            contador += 1

        logging.info("Saving combined CSV file...")
        df_combined.to_csv(nuevo_archivo_path, index=False)

        logging.info(f"Archivo CSV combinado correctamente. Nuevo archivo: {nuevo_archivo_path}")

    except FileNotFoundError as e:
        logging.error(e)
        messagebox.showerror("Error", str(e))
    except ValueError as e:
        logging.error(f"Error al procesar el archivo CSV: {e}")
        messagebox.showerror("Error", str(e))
    except Exception as e:
        logging.error(f"Se produjo un error inesperado: {e}")
        messagebox.showerror("Error", f"Se produjo un error inesperado: {e}")
    finally:
        status_label.config(text="Proceso completado.")
        messagebox.showinfo("Proceso completado", "El proceso ha finalizado.")


def select_file1():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Store the full file path in a global variable
        global full_path_file1
        full_path_file1 = file_path
        # Display only the file name
        path_label1.config(text=os.path.basename(file_path))
        display_columns(file_path, listbox1, select_button1a, columns1)

def select_file2():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Store the full file path in a global variable
        global full_path_file2
        full_path_file2 = file_path
        # Display only the file name
        path_label2.config(text=os.path.basename(file_path))
        display_columns(file_path, listbox2, select_button2a, columns2)

def display_columns(file_path, listbox, select_button, columns):
    df = pd.read_csv(file_path)
    columns.clear()
    columns.extend(list(df.columns))

    def on_select():
        try:
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Advertencia", "Debe seleccionar al menos una columna.")
                return

            selected_columns = [columns[i] for i in selected_indices if i < len(columns)]
            if not selected_columns:
                raise IndexError("Selección de columna fuera de rango.")

            for col in selected_columns:
                combined_listbox.insert(tk.END, col)

            # Save state for undo functionality
            save_state()

        except IndexError as e:
            logging.error(f"Error de índice: {e}")
            messagebox.showerror("Error", "Selección de columna fuera de rango.")
        except Exception as e:
            logging.error(f"Se produjo un error inesperado: {e}")
            messagebox.showerror("Error", f"Se produjo un error inesperado: {e}")

    listbox.delete(0, tk.END)
    for col in columns:
        listbox.insert(tk.END, col)

    select_button.config(command=on_select)

def delete_selected_column():
    try:
        selected_index = combined_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Advertencia", "Debe seleccionar una columna para eliminar.")
            return

        combined_listbox.delete(selected_index)
        
    except Exception as e:
        logging.error(f"Se produjo un error inesperado: {e}")
        messagebox.showerror("Error", f"Se produjo un error inesperado: {e}")

def rename_column():
    try:
        selected_index = combined_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Advertencia", "Debe seleccionar una columna para renombrar.")
            return

        new_name = simpledialog.askstring("Renombrar columna", "Ingrese el nuevo nombre de la columna:")
        
        if new_name:
            combined_listbox.delete(selected_index)
            combined_listbox.insert(selected_index, new_name)
            save_state()
            
    except Exception as e:
        logging.error(f"Se produjo un error inesperado: {e}")
        messagebox.showerror("Error", f"Se produjo un error inesperado: {e}")

def move_column_up():
    try:
        selected_index = combined_listbox.curselection()
        
        if not selected_index or selected_index[0] == 0:
            return
        
        index = selected_index[0]
        
        column_value = combined_listbox.get(index)
        
        combined_listbox.delete(index)
        
        combined_listbox.insert(index - 1, column_value)
        combined_listbox.select_set(index - 1)
        save_state()
        
    except Exception as e:
        logging.error(f"Se produjo un error inesperado: {e}")
        messagebox.showerror("Error", f"Se produjo un error inesperado: {e}")

def move_column_down():
    try:
        selected_index = combined_listbox.curselection()
        
        if not selected_index or selected_index[0] == combined_listbox.size() - 1:
            return
        
        index = selected_index[0]
        
        column_value = combined_listbox.get(index)
        
        combined_listbox.delete(index)
        
        combined_listbox.insert(index + 1, column_value)
        combined_listbox.select_set(index + 1)
        save_state()
        
    except Exception as e:
        logging.error(f"Se produjo un error inesperado: {e}")
        messagebox.showerror("Error", f"Se produjo un error inesperado: {e}")

# Function to open the "About" window
def open_about_window():
    about_window = tk.Toplevel(window)
    about_window.title("About")
    about_window.geometry("300x200")
    ttk.Label(about_window, text="CSV Editor", font=("Helvetica", 16)).pack(pady=10)
    ttk.Label(about_window, text="Version 2.0").pack(pady=5)
    ttk.Label(about_window, text="Author: Jimmy Hernández Rivera").pack(pady=5)
    ttk.Label(about_window, text="A simple CSV editing tool.").pack(pady=10)

# Function to confirm and open the file----------------------------------------------------------
def confirm_and_open_file(file_path):
    if os.path.exists(file_path):
        if file_path in opened_files:
            messagebox.showinfo("File Already Open", "This file is already open.")
        else:
            if messagebox.askyesno("Open File", "Are you sure you want to open this file?"):
                try:
                    os.startfile(file_path)
                    opened_files.add(file_path)
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while opening the file: {e}")
    else:
        messagebox.showerror("Error", "File does not exist.")



# Initialize the main window------------------------------------------------------------------------
window = tk.Tk()
window.geometry("800x600")
window.title("CSV EDITOR 2")
window.config(background="white")

# Centering the main window------------------------------------------------------------------------
for i in range(5):
    window.grid_columnconfigure(i, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(10, weight=1)

# Title------------------------------------------------------------------------------------------
title_label = ttk.Label(window, text="CSV Editor 2.0", font=("Helvetica", 16), background="white")
title_label.grid(row=0, column=0, columnspan=5, pady=10)

# First file selection ---------------------------------------------------------------------------
listbox1 = tk.Listbox(window, selectmode=tk.MULTIPLE)
listbox1.grid(row=1, column=1, padx=10, pady=5)

path_label1 = ttk.Label(window, text="")
path_label1.grid(row=2, column=1, padx=10, pady=5)

select_button1 = ttk.Button(window, text="Select File 1", command=select_file1)
select_button1.grid(row=3, column=1, padx=10, pady=10)

select_button1a = ttk.Button(window, text="Add Columns to new file")
select_button1a.grid(row=4, column=1, padx=10, pady=5)

# Second file selection ------------------------------------------------------------------------
listbox2 = tk.Listbox(window, selectmode=tk.MULTIPLE)
listbox2.grid(row=1, column=2, padx=10, pady=5)

path_label2 = ttk.Label(window, text="")
path_label2.grid(row=2, column=2, padx=10, pady=5)

select_button2 = ttk.Button(window, text="Select File 2", command=select_file2)
select_button2.grid(row=3, column=2, padx=10, pady=10)

select_button2a = ttk.Button(window, text="Add Columns to new file")
select_button2a.grid(row=4, column=2, padx=10, pady=5)

# Combined columns display---------------------------------------------------------------------
combined_listbox = tk.Listbox(window)
combined_listbox.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

# Submit and Reset buttons below combined list----------------------------------------------------
submit_button = ttk.Button(window, text="Run", command=lambda: procesar_csv(full_path_file1, [columns1[i] for i in listbox1.curselection()], full_path_file2, [columns2[i] for i in listbox2.curselection()]))
submit_button.grid(row=3, column=3, pady=5)

# Buttons on the right side--------------------------------------------------------------------
button_frame = ttk.Frame(window)
button_frame.grid(row=1, column=4, rowspan=8, padx=10, pady=10, sticky="ns")

add_button_combined = ttk.Button(button_frame, text="ADD COLUMN", command=add_column_to_combined)
add_button_combined.grid(row=0, column=0, pady=5)

delete_button_combined = ttk.Button(button_frame, text="DELETE COLUMN", command=delete_selected_column)
delete_button_combined.grid(row=1, column=0, pady=5)

rename_button_combined = ttk.Button(button_frame, text="RENAME COLUMN", command=rename_column)
rename_button_combined.grid(row=2, column=0, pady=5)

move_up_button = ttk.Button(button_frame, text="MOVE UP", command=move_column_up)
move_up_button.grid(row=3, column=0, pady=5)

move_down_button = ttk.Button(button_frame, text="MOVE DOWN", command=move_column_down)
move_down_button.grid(row=4, column=0, pady=5)

undo_button = ttk.Button(button_frame, text="UNDO", command=undo)
undo_button.grid(row=5, column=0, pady=5)

about_button = ttk.Button(button_frame, text="ABOUT", command=open_about_window)
about_button.grid(row=10, column=0,pady=10)

# Open file buttons with confirmation----------------------------------------------------------
open_file_button1 = ttk.Button(window, text="Open File 1", command=lambda: confirm_and_open_file(full_path_file1))
open_file_button1.grid(row=5, column=1, pady=5)

open_file_button2 = ttk.Button(window, text="Open File 2", command=lambda: confirm_and_open_file(full_path_file2))
open_file_button2.grid(row=5, column=2, pady=5)


columns1 = []
columns2 = []

window.mainloop()
