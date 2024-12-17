import tkinter as tk
from tkinter import filedialog
from tkinter import *
import pandas as pd
import logging
from pathlib import Path
from tkinter import simpledialog, messagebox, ttk

def procesar_csv(archivo_csv, campos_a_extraer):
    """
    Lee un archivo CSV, selecciona los campos especificados y guarda un nuevo CSV.

    Args:
        archivo_csv (str): Ruta al archivo CSV de entrada.
        campos_a_extraer (list): Lista de nombres de columnas a extraer.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Crear la ventana principal de Tkinter
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal

        # Leer el archivo CSV
        df = pd.read_csv(archivo_csv)

        # Validar si el DataFrame está vacío
        if df.empty:
            raise ValueError("El archivo CSV está vacío.")

        # Validar si todos los campos a extraer existen en el DataFrame
        campos_inexistentes = set(campos_a_extraer) - set(df.columns)
        if campos_inexistentes:
            # Preguntar al usuario si desea crear las columnas faltantes
            crear_columnas = messagebox.askyesno("Campos inexistentes", f"Los siguientes campos no existen: {campos_inexistentes}. ¿Desea crearlos?")
            if crear_columnas:
                # Crear las columnas faltantes con valores NaN
                for columna in campos_inexistentes:
                    df[columna] = None
            else:
                raise ValueError("No se crearon las columnas faltantes.")

        # Seleccionar los campos deseados
        df_nuevo = df[campos_a_extraer]

        # Pedir al usuario que ingrese el nombre del archivo de salida
        nuevo_archivo = simpledialog.askstring("Nombre del archivo de salida", "Ingrese el nombre del archivo de salida (sin la extensión .csv):")

        # Validar el nombre del archivo de salida
        if not nuevo_archivo:
            raise ValueError("Debe ingresar un nombre para el archivo de salida.")

        # Pedir al usuario que seleccione la ubicación para guardar el archivo
        save_path = filedialog.askdirectory(title="Seleccione la ubicación para guardar el archivo")
        if not save_path:
            raise ValueError("Debe seleccionar una ubicación para guardar el archivo.")

        # Generar la ruta completa del archivo de salida
        nuevo_archivo_path = Path(save_path) / f"{nuevo_archivo}.csv"

        # Generar un nombre de archivo único si ya existe
        contador = 1
        while nuevo_archivo_path.exists():
            nuevo_archivo_path = nuevo_archivo_path.with_stem(f"{nuevo_archivo_path.stem}_{contador}")
            logging.warning(f"El archivo {nuevo_archivo_path} ya existe. Se intentará con un nombre diferente.")
            contador += 1

        # Guardar el nuevo DataFrame en un archivo CSV
        df_nuevo.to_csv(nuevo_archivo_path, index=False)

        logging.info(f"Archivo CSV editado correctamente. Nuevo archivo: {nuevo_archivo_path}")

    except FileNotFoundError:
        logging.error(f"No se encontró el archivo CSV: {archivo_csv}")
    except ValueError as e:
        logging.error(f"Error al procesar el archivo CSV: {e}")
    except Exception as e:
        logging.error(f"Se produjo un error inesperado: {e}")
    finally:
        # Crear una ventana para la barra de progreso después de que el proceso haya terminado
        progress_window = tk.Toplevel(root)
        progress_window.title("Proceso Completado")

        # Crear una etiqueta para mostrar el estado final
        status_label = tk.Label(progress_window, text="Proceso completado.")
        status_label.pack(pady=10)

        # Crear una barra de progreso completa
        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
        progress_bar.pack(pady=10)
        
        progress_bar['value'] = 100  # Establecer la barra de progreso al 100%

        messagebox.showinfo("Proceso completado", "El proceso ha finalizado.")
        
def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        path_label.config(text=file_path)

def submit_file():
    file_path = path_label.cget("text")
    if file_path:
        # Here you can add the code to process the file
        procesar_csv(file_path,
        [
             "Last Name",	
              "First Name",	
              "EID",
              "Day",	
              "Date",	
              "Project Name",	
              "Job #",
              "Project Number",
              "Contract Number",
              "Position",
              "Site",
              "Task Description",              
              "Pay Type",
              "Hours",
              "Start Time",	
              "End Time",
              "Meal Breaks",	
              "Total Break Time",	
              "WorkLog Name",
              "WBS Task Codes",
              "WBS Description",
                     
        ])
        print(f"File submitted: {file_path}")

# CREACION DE VENTANA
window = Tk()
window.geometry("500x500")
window.title("CSV EDITOR")
window.config(background="white")

# LABEL PRINCIPAL (LOGO)
label_principal = Label(window,
text="Newtron's CSV Editor",
font=('Ink Free', 20, 'bold'),
fg='black',
bg='white',
relief=RAISED, #para los bordes
bd=10, # tamaño de los bordes
padx=20,#espacion entre el borde del titulo y el titulo(x=horizontal)
pady=20,#espacion entre el borde del titulo y el titulo(y=veritcal)
)
label_principal.pack()# para que el titulo aparesca en el mismo centro

# SELECCIONAR ARCHIVO
select_button = tk.Button(window, text="Select File", command=select_file)
select_button.pack(pady=10)

# Create a label to display the selected file pathclear
path_label = tk.Label(window, text="")
path_label.pack(pady=10)


# Create a button to submit the file
submit_button = tk.Button(window, text="Submit File", command=submit_file)
submit_button.pack(pady=10)

window.mainloop()
