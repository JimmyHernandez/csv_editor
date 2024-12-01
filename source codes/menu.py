from tkinter import *

count =0
def click():
    global count
    count+=1
    label.config(text=count)

# The code snippet `window = Tk()` creates a new window for the GUI application using the Tkinter
# library in Python.
window = Tk()
window.geometry("500x500")
window.title("CSV EDITOR")
window.config(background="white")

# This code snippet is creating a Label widget in the GUI window. Here's a breakdown of what each
# parameter in the Label widget configuration represents:
label = Label(window,
text="Newtron's CSV Editor",
font=('Ink Free', 20, 'bold'),
fg='#fffb1f',
bg='#ff6200',
relief=RAISED, #para los bordes
bd=10, # tamaño de los bordes
padx=20,#espacion entre el borde del titulo y el titulo(x=horizontal)
pady=20,#espacion entre el borde del titulo y el titulo(y=veritcal)
)
label.pack()# para que el titulo aparesca en el mismo centro




# The code snippet you provided is creating a Button widget and a Label widget in the GUI window
# created using Tkinter in Python. Here's a breakdown of what each part of the code is doing:

button = Button(window,text='Guardar')
button.config(command=click)
button.config(font=('Ink Free',15,'bold'))
button.config(bg='#ff6200')
button.config(fg='#fffb1f')
label = Label(window,text=count)
label.pack()
button.pack()


window.mainloop()

