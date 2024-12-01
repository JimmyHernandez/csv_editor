import pandas as pd
import logging
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, ttk

def procesar_csv(archivo_csv, campos_a_extraer):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
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

    except FileNotFoundError:
        logging.error(f"No se encontró el archivo CSV: {archivo_csv}")
    except ValueError as e:
        logging.error(f"Error al procesar el archivo CSV: {e}")
    except Exception as e:
        logging.error(f"Se produjo un error inesperado: {e}")
    finally:
        progress_window = tk.Toplevel(root)
        progress_window.title("Proceso Completado")
        status_label = tk.Label(progress_window, text="Proceso completado.")
        status_label.pack(pady=10)
        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
        progress_bar.pack(pady=10)
        progress_bar['value'] = 100
        messagebox.showinfo("Proceso completado", "El proceso ha finalizado.")

def reset_gui():
    for widget in root.winfo_children():
        widget.destroy()
    create_main_gui()

def create_main_gui():
    global root
    root = tk.Tk()
    root.title("Procesador de CSV")
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    select_button = ttk.Button(frame, text="Seleccionar Archivo CSV", command=select_file)
    select_button.grid(row=0, column=0, pady=10, padx=10)

    global path_label
    path_label = ttk.Label(frame, text="")
    path_label.grid(row=1, column=0, pady=10, padx=10)

    submit_button = ttk.Button(frame, text="Procesar Archivo", command=process_file)
    submit_button.grid(row=2, column=0, pady=10, padx=10)

    reset_button = ttk.Button(frame, text="Restablecer", command=reset_gui)
    reset_button.grid(row=3, column=0, pady=10, padx=10)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        path_label.config(text=file_path)

def process_file():
    file_path = path_label.cget("text")
    if file_path:
        campos_a_extraer = simpledialog.askstring("Campos a extraer", "Ingrese los nombres de las columnas a extraer, separados por comas:")
        if campos_a_extraer:
            campos_a_extraer_list = [campo.strip() for campo in campos_a_extraer.split(",")]
            procesar_csv(file_path, campos_a_extraer_list)

create_main_gui()
root.mainloop()