import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import pandas as pd
import logging
from pathlib import Path
import os

def procesar_csv(archivo_csv, campos_a_extraer):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Validate file path
        if not os.path.isfile(archivo_csv):
            raise FileNotFoundError(f"El archivo CSV no existe: {archivo_csv}")

        df = pd.read_csv(archivo_csv)

        if df.empty:
            raise ValueError("El archivo CSV está vacío.")

        campos_inexistentes = set(campos_a_extraer) - set(df.columns)
        if campos_inexistentes:
            crear_columnas = messagebox.askyesno("Campos inexistentes", f"Los siguientes campos no existen: {campos_inexistentes}. ¿Desea crearlos?")
            if crear_columnas:
                for columna in campos_inexistentes:
                    df[columna] = None
            else:
                raise ValueError("No se crearon las columnas faltantes.")

        df_nuevo = df[campos_a_extraer]

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

        df_nuevo.to_csv(nuevo_archivo_path, index=False)

        logging.info(f"Archivo CSV editado correctamente. Nuevo archivo: {nuevo_archivo_path}")

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
        progress_bar['value'] = 100
        messagebox.showinfo("Proceso completado", "El proceso ha finalizado.")

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        path_label.config(text=file_path)
        display_columns(file_path)

def display_columns(file_path):
    df = pd.read_csv(file_path)
    columns = list(df.columns)

    def on_select():
        try:
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Advertencia", "Debe seleccionar al menos una columna.")
                return

            selected_columns = [columns[i] for i in selected_indices if i < len(columns)]
            if not selected_columns:
                raise IndexError("Selección de columna fuera de rango.")

            procesar_csv(file_path, selected_columns)
        except IndexError as e:
            logging.error(f"Error de índice: {e}")
            messagebox.showerror("Error", "Selección de columna fuera de rango.")
        except Exception as e:
            logging.error(f"Se produjo un error inesperado: {e}")
            messagebox.showerror("Error", f"Se produjo un error inesperado: {e}")

    def add_column():
        new_column = simpledialog.askstring("Agregar columna", "Ingrese el nombre de la nueva columna:")
        if new_column:
            columns.append(new_column)  # Add new column to the columns list
            listbox.delete(0, tk.END)  # Clear the listbox
            for col in columns:  # Re-populate the listbox with updated columns
                listbox.insert(tk.END, col)

    listbox.delete(0, tk.END)
    for col in columns:
        listbox.insert(tk.END, col)

    select_button.config(command=on_select)
    add_button.config(command=add_column)

def submit_file():
    file_path = path_label.cget("text")
    if file_path:
        display_columns(file_path)

def reset_fields():
    path_label.config(text="")
    listbox.delete(0, tk.END)
    status_label.config(text="")
    progress_bar['value'] = 0

window = tk.Tk()
window.geometry("500x600")
window.title("CSV EDITOR")
window.config(background="white")

label_principal = tk.Label(window, text="Newtron's CSV Editor", font=('Ink Free', 20, 'bold'), fg='black', bg='white', relief=tk.RAISED, bd=10, padx=20, pady=20)
label_principal.pack()

select_button = tk.Button(window, text="Select File", command=select_file)
select_button.pack(pady=10)

path_label = tk.Label(window, text="")
path_label.pack(pady=10)

listbox = tk.Listbox(window, selectmode=tk.MULTIPLE)
listbox.pack(pady=10)

add_button = tk.Button(window, text="Agregar Columna")
add_button.pack(pady=10)

#submit_button = tk.Button(window, text="Original List", command=submit_file)
#submit_button.pack(pady=10)

select_button = tk.Button(window, text="Run")
select_button.pack(pady=10)

reset_button = tk.Button(window, text="Reset", command=reset_fields)
reset_button.pack(pady=10)

status_label = tk.Label(window, text="")
status_label.pack(pady=10)

progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

window.mainloop()