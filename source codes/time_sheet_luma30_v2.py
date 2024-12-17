import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def centrar_ventana(ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def seleccionar_csv():
    return filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

def eliminar_columnas(df, columnas_a_eliminar):
    df.drop(columns=columnas_a_eliminar, inplace=True, errors='ignore')
    return df

def anadir_columnas(df, nuevas_columnas, root):
    opciones_wbs = {'A3092': 'Clearing Vegetation', 'A3091': 'Assessment Vegetation'}
    
    dialog = tk.Toplevel(root)
    dialog.title("Introduce los valores para las nuevas columnas")
    dialog.geometry("400x400")
    centrar_ventana(dialog)
    
    inputs = {}
    
    def actualizar_descripcion_wbs(event):
        seleccion = inputs['WBS Task Codes'].get()
        if seleccion in opciones_wbs:
            inputs['WBS Description'].set(opciones_wbs[seleccion])
    
    for columna in nuevas_columnas:
        frame = ttk.Frame(dialog, padding="10 5")
        frame.pack(pady=5, padx=10, fill='x')
        
        label = ttk.Label(frame, text=f"{columna}:")
        label.pack(side="left", padx=5)
        
        if columna == 'Project Number':
            valor = '15F019300000'
        elif columna == 'Contract Number':
            valor = '2024-L00559'
        elif columna == 'WBS Task Codes':
            seleccion = tk.StringVar()
            combobox = ttk.Combobox(frame, textvariable=seleccion, values=list(opciones_wbs.keys()))
            combobox.pack(side="left", padx=5)
            combobox.bind("<<ComboboxSelected>>", actualizar_descripcion_wbs)
            inputs[columna] = seleccion
            continue
        elif columna == 'WBS Description':
            seleccion = tk.StringVar()
            entry_widget = ttk.Entry(frame, textvariable=seleccion, state='readonly')
            entry_widget.pack(side="left", padx=5)
            inputs[columna] = seleccion
            continue
        else:
            valor = ''
        
        entrada = tk.StringVar(value=valor)
        entry_widget = ttk.Entry(frame, textvariable=entrada)
        entry_widget.pack(side="left", padx=5)
        inputs[columna] = entrada
    
    def confirmar():
        for columna in nuevas_columnas:
            df[columna] = inputs[columna].get()
        dialog.destroy()
        previsualizar_df(df, root)  # Actualizar la previsualización con los nuevos datos
    
    boton_confirmar = ttk.Button(dialog, text="Confirmar", command=confirmar)
    boton_confirmar.pack(pady=10)
    
    dialog.wait_window()
    
    return df

def renombrar_columnas(df, columnas_a_renombrar):
    df.rename(columns=columnas_a_renombrar, inplace=True)
    return df

def organizar_output(df):
    columnas_ordenadas = ['First Name', 'Last Name', 'EID', 'Day', 'Date', 'Project Name', 'Job #', 'Project Number', 'Contract Number', 'Position', 'Site', 'Coordinates', 'Task Description', 'Hours', 'Start Time', 'End Time', 'Meal Breaks', 'Total Break Time', 'WBS Task Codes', 'WBS Description']
    
    # Verificar las columnas existentes en el DataFrame
    print("Columnas del DataFrame:", df.columns)
    
    # Filtrar las columnas que existen en el DataFrame
    columnas_existentes = [col for col in columnas_ordenadas if col in df.columns]
    
    # Verificar las columnas que se van a ordenar
    print("Columnas a ordenar:", columnas_existentes)
    
    # Reorganizar el DataFrame con las columnas existentes
    return df[columnas_existentes]

def exportar_csv(df):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Éxito", f"Archivo modificado guardado como: {file_path}")

def previsualizar_df(df, root):
    previsualizacion_ventana = tk.Toplevel(root)
    previsualizacion_ventana.title("Previsualización del archivo")
    previsualizacion_ventana.geometry("1000x500")
    centrar_ventana(previsualizacion_ventana)

    frame = ttk.Frame(previsualizacion_ventana, padding="10")
    frame.pack(expand=True, fill='both')

    treeview = ttk.Treeview(frame, columns=list(df.columns), show="headings")
    for col in df.columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=100)
    
    for _, row in df.iterrows():
        treeview.insert("", "end", values=list(row))
    
    scrollbar_vertical = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
    scrollbar_horizontal = ttk.Scrollbar(frame, orient="horizontal", command=treeview.xview)
    treeview.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

    treeview.grid(row=0, column=0, sticky='nsew')
    scrollbar_vertical.grid(row=0, column=1, sticky='ns')
    scrollbar_horizontal.grid(row=1, column=0, sticky='ew')

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    boton_guardar = ttk.Button(previsualizacion_ventana, text="Guardar CSV", command=lambda: exportar_csv(df))
    boton_guardar.pack(pady=10)

def comenzar_proceso():
    file_path = seleccionar_csv()
    if file_path:
        df = pd.read_csv(file_path)
        columnas_a_eliminar = ['Classification', 'Shift', 'Pay Type', 'Breaks', 'WorkLog Name', 'Payroll Attachments']
        df = eliminar_columnas(df, columnas_a_eliminar)
        nuevas_columnas = ['Project Number', 'Contract Number', 'Coordinates', 'WBS Task Codes', 'WBS Description']
        df = anadir_columnas(df, nuevas_columnas, root)
        columnas_a_renombrar = {'Cost Code': 'Position', 'Payroll Note': 'Site', 'Cost Code #': 'Task Description'}
        df = renombrar_columnas(df, columnas_a_renombrar)
        df['Position'] = ''  # Asegurarse de que la columna Position esté presente
        df['Site'] = ''  # Asegurarse de que la columna Site esté presente
        df = organizar_output(df)
        previsualizar_df(df, root)  # Asegurarse de previsualizar el DataFrame actualizado

root = tk.Tk()
root.title("Editor de CSV")
root.geometry("400x300")
centrar_ventana(root)

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Helvetica', 12))

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Archivo", menu=file_menu)
file_menu.add_command(label="Comenzar Proceso", command=comenzar_proceso)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)

welcome_label = ttk.Label(root, text="Bienvenido al Editor de CSV", font=("Helvetica", 16))
welcome_label.pack(pady=20)

start_button = ttk.Button(root, text="Comenzar Proceso")
start_button.pack(pady=10)
start_button.config(command=comenzar_proceso)

root.mainloop()