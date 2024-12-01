import pandas as pd
import os
from tkinter import filedialog

def procesar_csv(archivo_csv, campos_a_extraer):
    """
    Lee un archivo CSV, selecciona los campos especificados y guarda un nuevo CSV.

    Args:
        archivo_csv (str): Ruta al archivo CSV de entrada.
        campos_a_extraer (list): Lista de nombres de columnas a extraer.
    """

    try:
        # Leer el archivo CSV
        df = pd.read_csv(archivo_csv)

        # Validar si el DataFrame está vacío
        if df.empty:
            raise ValueError("El archivo CSV está vacío.")

        # Validar si todos los campos a extraer existen en el DataFrame
        campos_inexistentes = set(campos_a_extraer) - set(df.columns)
        if campos_inexistentes:
            # Preguntar al usuario si desea crear las columnas faltantes
            crear_columnas = input(f"Los siguientes campos no existen: {campos_inexistentes}. ¿Desea crearlos? (s/n): ")
            if crear_columnas.lower() == 's':
                # Crear las columnas faltantes con valores NaN
                for columna in campos_inexistentes:
                    df[columna] = None
            else:
                raise ValueError("No se crearon las columnas faltantes.")

        # Seleccionar los campos deseados
        df_nuevo = df[campos_a_extraer]

        # Pedir al usuario que ingrese el nombre del archivo de salida
        nuevo_archivo = input("Ingrese el nombre del archivo de salida (incluyendo la extensión .csv): ")

        # Generar un nombre de archivo único si ya existe
        contador = 1
        while os.path.exists(nuevo_archivo):
            nuevo_archivo = nuevo_archivo.rsplit('.', 1)[0] + f"_{contador}" + ".csv"
            print(f"El archivo {nuevo_archivo} ya existe. Se intentará con un nombre diferente.")
            contador += 1

        # Guardar el nuevo DataFrame en un archivo CSV
        df_nuevo.to_csv(nuevo_archivo, index=False)

        print(f"Archivo CSV editado correctamente. Nuevo archivo: {nuevo_archivo}")

    except FileNotFoundError:
        print(f"No se encontró el archivo CSV: {archivo_csv}")
    except ValueError as e:
        print(f"Error al procesar el archivo CSV: {e}")

def seleccionar_archivo():
    """Abre un diálogo para seleccionar el archivo CSV."""
    archivo_seleccionado = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if archivo_seleccionado:
        # Llama a la función procesar_csv con el archivo seleccionado
        procesar_csv(archivo_seleccionado, campos_deseados)
    else:
        print("No se seleccionó ningún archivo.")

# Ejemplo de uso:
archivo_entrada = "C:\\Users\\jimmy\\OneDrive\\Documents\\Development AMD\\demos\\original\\raken_og.csv"
campos_deseados =  [
              "Last Name",	
              "First Name",	
              "EID",
              "Day",	
              "Date",	
              "Project Name",	
              "Job #",
              "Classification",	
              "Pay Type",
              "Hours",
              "Start Time",	
              "End Time",
              "Meal Breaks",	
              "Total",
              "Break Time",	
              "WorkLog Name",	
              "Task Description",	
              "WO #",            
            ]

procesar_csv(archivo_entrada, campos_deseados)
    
