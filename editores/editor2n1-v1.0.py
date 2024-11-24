import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import pandas as pd
import logging
from pathlib import Path
import os

def procesar_csv(archivo_csv1, campos_a_extraer1, archivo_csv2, campos_a_extraer2):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Validate file paths
        if not os.path.isfile(archivo_csv1):
            raise FileNotFoundError(f"El archivo CSV no existe: {archivo_csv1}")
        if not os.path.isfile(archivo_csv2):
            raise FileNotFoundError(f"El archivo CSV no existe: {archivo_csv2}")

        df1 = pd.read_csv(archivo_csv1)
        df2 = pd.read_csv(archivo_csv2)

        if df1.empty or df2.empty:
            raise ValueError("Uno de los archivos CSV está vacío.")

        df_nuevo1 = df1[campos_a_extraer1]
        df_nuevo2 = df2[campos_a_extraer2]

        # Ensure both DataFrames have the same number of rows by padding the shorter DataFrame
        max_rows = max(len(df_nuevo1), len(df_nuevo2))
        df_nuevo1 = df_nuevo1.reindex(range(max_rows))
        df_nuevo2 = df_nuevo2.reindex(range(max_rows))

        # Combine the selected columns from both files horizontally
        df_combined = pd.concat([df_nuevo1.reset_index(drop=True), df_nuevo2.reset_index(drop=True)], axis=1)

        nuevo_archivo = simpledialog.askstring("Nombre del archivo de salida", "Ingrese el nombre del archivo de salida (sin la extensión .csv):")
        if not nuevo_archivo:
            raise ValueError("Debe ingresar un nombre para el archivo de salida.")

        # Sanitize file name
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

def add_column_to_combined():
    new_column = simpledialog.askstring("Agregar columna", "Ingrese el nombre de la nueva columna:")
    if new_column:
        combined_listbox.insert(tk.END, new_column)

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

# Function to open the "About" window
def open_about_window():
    about_window = tk.Toplevel(window)
    about_window.title("About")
    about_window.geometry("300x200")
    ttk.Label(about_window, text="CSV Editor", font=("Helvetica", 16)).pack(pady=10)
    ttk.Label(about_window, text="Version 1.0").pack(pady=5)
    ttk.Label(about_window, text="Author: Jimmy Hernández Rivera").pack(pady=5)
    ttk.Label(about_window, text="A simple CSV editing tool.").pack(pady=10)


window = tk.Tk()
window.geometry("800x600")
window.title("CSV EDITOR 1.0")
window.config(background="white")

# Centering the main window
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(10, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(4, weight=1)

label_principal = tk.Label(window, text="Newtron's CSV Editor 1.0", font=('Ink Free', 20, 'bold'))
label_principal.grid(row=0, column=1)

# First file selection
select_button1 = tk.Button(window, text="Select File 1", command=select_file1)
select_button1.grid(row=4, column=0, pady=10)

path_label1 = tk.Label(window, text="")
path_label1.grid(row=2, column=0, pady=10)

listbox1 = tk.Listbox(window, selectmode=tk.MULTIPLE)
listbox1.grid(row=3, column=0, pady=10)

select_button1a = tk.Button(window, text="Seleccionar Columnas")
select_button1a.grid(row=5, column=0, pady=10)

# Second file selection
select_button2 = tk.Button(window, text="Select File 2", command=select_file2)
select_button2.grid(row=4, column=1, pady=10)

path_label2 = tk.Label(window, text="")
path_label2.grid(row=2, column=1, pady=10)

listbox2 = tk.Listbox(window, selectmode=tk.MULTIPLE)
listbox2.grid(row=3, column=1, pady=10)

select_button2a = tk.Button(window, text="Seleccionar Columnas")
select_button2a.grid(row=5, column=1, pady=10)

# Combined columns display
combined_filename = tk.Label(window, text="New CSV file")
combined_filename.grid(row=2, column=2, pady=10)

combined_listbox = tk.Listbox(window)
combined_listbox.grid(row=3, column=2, columnspan=1, pady=10)

# Add and delete column buttons for combined list
add_button_combined = tk.Button(window, text="Agregar Columna", command=add_column_to_combined)
add_button_combined.grid(row=4, column=2, pady=10)

delete_button_combined = tk.Button(window, text="Eliminar Columna", command=delete_selected_column)
delete_button_combined.grid(row=5, column=2, pady=10)

# Submit and reset buttons
submit_button = tk.Button(window, text="Submit File", command=lambda: procesar_csv(full_path_file1, [columns1[i] for i in listbox1.curselection()], full_path_file2, [columns2[i] for i in listbox2.curselection()]))
submit_button.grid(row=10, column=1,pady=10)

about_button = ttk.Button(window, text="ABOUT", command=open_about_window)
about_button.grid(row=12, column=1,pady=10)

columns1 = []
columns2 = []

window.mainloop()