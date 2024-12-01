import tkinter as tk

def procesar_datos():
    # Obtener el valor ingresado en el campo de texto
    nombre_archivo = entrada_archivo.get()
    # ... resto de tu código ...

ventana = tk.Tk()
ventana.title("Procesador de CSV")

etiqueta_archivo = tk.Label(ventana, text="Ingrese el nombre del archivo CSV:")
etiqueta_archivo.pack()

entrada_archivo = tk.Entry(ventana)
entrada_archivo.pack()

boton_procesar = tk.Button(ventana, text="Procesar", command=procesar_datos)
boton_procesar.pack()

ventana.mainloop()