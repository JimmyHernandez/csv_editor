import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog

def seleccionar_csv():
    # Crear una ventana de diálogo para seleccionar el archivo CSV
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    return file_path

def eliminar_columnas(df, columnas_a_eliminar):
    # Eliminar columnas específicas
    df.drop(columns=columnas_a_eliminar, inplace=True, errors='ignore')
    return df

def anadir_columnas(df, nuevas_columnas, root):
    # Añadir nuevas columnas con contenido proporcionado por el usuario
    for columna in nuevas_columnas:
        if columna == 'Project Number':
            df[columna] = '15F019300000'
        else:
            contenido = simpledialog.askstring("Input", f"Introduce el contenido para la columna '{columna}':", parent=root)
            df[columna] = contenido
    return df

def renombrar_columnas(df, columnas_a_renombrar):
    # Renombrar columnas específicas
    df.rename(columns=columnas_a_renombrar, inplace=True)
    return df

def organizar_output(df):
    # Organizar el DataFrame (hardcoding)
    # Ejemplo: Reordenar columnas
    columnas_ordenadas = ['First Name', 'Last Name', 'EID', 'Day', 'Date', 'Project Name', 'Job #', 'Project Number', 'Contract Number', 'Position', 'Site', 'Coordinates', 'Task Description', 'Hours', 'Start Time', 'End Time', 'Meal Breaks', 'Total Break Time', 'WBS Task Codes']
    
    # Verificar si todas las columnas existen en el DataFrame
    columnas_existentes = [col for col in columnas_ordenadas if col in df.columns]
    df = df[columnas_existentes]
    return df

def exportar_csv(df):
    # Crear una ventana de diálogo para seleccionar la ubicación de guardado del archivo CSV
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        df.to_csv(file_path, index=False)
        print(f"Archivo modificado guardado como: {file_path}")

# Ejecución del programa

file_path = seleccionar_csv()
if file_path:
    df = pd.read_csv(file_path)
    
    # Eliminar columnas específicas (hardcoding)
    columnas_a_eliminar = ['Classification', 'Shift', 'Pay Type', 'Breaks', 'WorkLog Name', 'Payroll Attachments']
    df = eliminar_columnas(df, columnas_a_eliminar)
    
    # Crear la ventana principal para los inputs
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    
    # Añadir nuevas columnas con contenido proporcionado por el usuario
    nuevas_columnas = ['Project Number', 'Contract Number', 'Coordinates', 'WBS Task Codes']
    df = anadir_columnas(df, nuevas_columnas, root)
    
    # Renombrar columnas específicas
    columnas_a_renombrar = {'Cost Code': 'Position', 'Payroll Note': 'Site', 'Cost Code #': 'Task Description'}
    df = renombrar_columnas(df, columnas_a_renombrar)
    
    # Organizar el DataFrame
    df = organizar_output(df)
    
    # Exportar a CSV
    exportar_csv(df)
else:
    print("No se seleccionó ningún archivo.")