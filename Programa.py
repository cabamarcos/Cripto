from tkinter import *
from tkinter import messagebox
import sqlite3



#-------------------Crear Base de Datos"----------------------#

# MiConexion=sqlite3.connect("Base de Datos")

# MiCursor=MiConexion.cursor()

# MiCursor.execute("CREATE TABLE DATOSUSUARIO (NOMBRE VARCHAR(20) PRIMARY KEY, CONTRASEÑA VARCHAR(40), SALT VARCHAR(40), MARCA VARCHAR(20), MODELO VARCHAR(20), AÑO VARCHAR(4), COMBUSTIBLE VARCHAR(20), MATRICULA VARCHAR(15), BASTIDOR VARCHAR(50))")

# MiConexion.close()


root=Tk()

# Creadores=Menu(root)
# root.config(menu=Creadores, width=300, height=300)
# Creadores.add_cascade(label="Creadores Damián y Marcos")

#-----------------Funciones------------------#

def Crear():
    """Creamos registros"""

    MiConexion=sqlite3.connect("Base de Datos")
    MiCursor=MiConexion.cursor()

    #Datos=(VarNombre.get(), VarPass.get(), VarMarca.get(), VarModelo.get(), VarAño.get(), VarFuel.get(), VarMatricula.get(), VarBastidor.get())
    #MiCursor.execute("INSERT INTO DATOSUSUARIO VALUES(?,?,?,?,?,?,?,?)", Datos)
    MiCursor.execute("INSERT INTO DATOSUSUARIO VALUES('" + VarNombre.get() 
                                                    + "','" + VarPass.get() 
                                                    + "','" + VarMarca.get() 
                                                    + "','" + VarModelo.get() 
                                                    + "','" + VarAño.get() 
                                                    + "','" + VarFuel.get() 
                                                    + "','" + VarMatricula.get() 
                                                    + "','" + VarBastidor.get() + "')")
    MiConexion.commit()
    messagebox.showinfo("BBDD", "Registro insertado con éxito")

def Leer():
    """Lee los registros con un usuario y una contraseña"""

    MiConexion=sqlite3.connect("Base de Datos")
    MiCursor=MiConexion.cursor()

    MiCursor.execute("SELECT * FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get() 
                                            + "' AND CONTRASEÑA= '" + VarPass.get() +"'")

    Usuario=MiCursor.fetchall()
    
    for i in Usuario:

        VarNombre.set(i[0])
        VarPass.set(i[1])
        VarMarca.set(i[2])
        VarModelo.set(i[3])
        VarAño.set(i[4])
        VarFuel.set(i[5]) 
        VarMatricula.set(i[6])
        VarBastidor.set(i[7])
    
    MiConexion.commit()
    

def Actualizar():
    """Actualizamos el registro con ese usuario y contraseña"""

    MiConexion=sqlite3.connect("Base de Datos")
    MiCursor=MiConexion.cursor()

    MiCursor.execute("SELECT * FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get() 
                                            + "' AND CONTRASEÑA= '" + VarPass.get() +"'")

    Usuario=MiCursor.fetchall()

    for i in Usuario:
        
        VerUsuario = (i[0])
        VerPass = (i[1])

    MiConexion.commit()

    if VerUsuario == VarNombre.get() and VerPass == VarPass.get():

        MiCursor.execute("UPDATE DATOSUSUARIO SET MARCA= '" + VarMarca.get() +
                                        "', MODELO= '" + VarModelo.get() +
                                        "', AÑO= '" + VarAño.get() +
                                        "', COMBUSTIBLE= '" + VarFuel.get() +
                                        "', MATRICULA= '" + VarMatricula.get() + 
                                        "', BASTIDOR= '" + VarBastidor.get() +
                                        "' WHERE NOMBRE= '" + VarNombre.get() + "'")
        MiConexion.commit()

    messagebox.showinfo("BBDD", "Registro actualizado conéxito")

def Eliminar():
    """Eliminamos el registro con ese usuario y esa contraseña"""
    
    MiConexion=sqlite3.connect("Base de Datos")
    MiCursor=MiConexion.cursor()

    MiCursor.execute("DELETE FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get()
                                                + "' AND CONTRASEÑA= '" + VarPass.get() +"'")

    MiConexion.commit()
    messagebox.showinfo("BBDD", "Registro borrado con éxito")

    VarMarca.set("")
    VarModelo.set("")
    VarAño.set("")
    VarFuel.set("") 
    VarMatricula.set("")
    VarBastidor.set("")

def Limpiar():
    """Limpia los datos de la interfaz"""
    VarNombre.set("")
    VarPass.set("")
    VarMarca.set("")
    VarModelo.set("")
    VarAño.set("")
    VarFuel.set("") 
    VarMatricula.set("")
    VarBastidor.set("")

def Salir():
    """Salimos de la interfaz"""

    Confirmacion=messagebox.askquestion("Salir", "Confirme para salir de la aplicación")

    if Confirmacion=="yes":
        root.destroy()

#--------------------VENTANA-------------------#

Ventana=Frame(root)
Ventana.pack()

VarNombre=StringVar()
VarPass=StringVar()
VarMarca=StringVar()
VarModelo=StringVar()
VarAño=StringVar()
VarFuel=StringVar()
VarMatricula=StringVar()
VarBastidor=StringVar()

CuadroNombre=Entry(Ventana, textvariable=VarNombre)
CuadroNombre.grid(row=0, column=1, padx=10, pady=10)

CuadroPass=Entry(Ventana, textvariable=VarPass)
CuadroPass.grid(row=1, column=1, padx=10, pady=10)
CuadroPass.config(show="*")

CuadroMarca=Entry(Ventana, textvariable=VarMarca)
CuadroMarca.grid(row=3, column=1, padx=10, pady=10)

CuadroModelo=Entry(Ventana, textvariable=VarModelo)
CuadroModelo.grid(row=4, column=1, padx=10, pady=10)

CuadroAño=Entry(Ventana, textvariable=VarAño)
CuadroAño.grid(row=5, column=1, padx=10, pady=10)

CuadroFuel=Entry(Ventana, textvariable=VarFuel)
CuadroFuel.grid(row=6, column=1, padx=10, pady=10)

CuadroMatricula=Entry(Ventana, textvariable=VarMatricula)
CuadroMatricula.grid(row=7, column=1, padx=10, pady=10)

CuadroBastidor=Entry(Ventana, textvariable=VarBastidor)
CuadroBastidor.grid(row=8, column=1, padx=10, pady=10)

#------------------Texto---------------------#
LabelNombre=Label(Ventana, text="Usuario:")
LabelNombre.grid(row=0, column=0, padx=10, pady=10, sticky="e")

LabelPass=Label(Ventana, text="Contraseña:")
LabelPass.grid(row=1, column=0, padx=10, pady=10, sticky="e")

LabelSeparador=Label(Ventana, text="VEHICULO:")
LabelSeparador.grid(row=2, column=0, padx=15, pady=10, sticky="e")

LabelMarca=Label(Ventana, text="Marca:")
LabelMarca.grid(row=3, column=0, padx=10, pady=10, sticky="e")

LabelModelo=Label(Ventana, text="Modelo:")
LabelModelo.grid(row=4, column=0, padx=10, pady=10, sticky="e")

LabelAño=Label(Ventana, text="Año de fabricación:")
LabelAño.grid(row=5, column=0, padx=10, pady=10, sticky="e")

LabelFuel=Label(Ventana, text="Combustible:")
LabelFuel.grid(row=6, column=0, padx=10, pady=10, sticky="e")

LabelMatricula=Label(Ventana, text="Matricula:")
LabelMatricula.grid(row=7, column=0, padx=10, pady=10, sticky="e")

LabelBastidor=Label(Ventana, text="Nº Bastidor:")
LabelBastidor.grid(row=8, column=0, padx=10, pady=10, sticky="e")

#---------------------Botones-----------------------#

Ventana2=Frame(root)
Ventana2.pack()

BotonCrear=Button(Ventana2, text="Crear", command=Crear)
BotonCrear.grid(row=0, column=0, padx=10, pady=10)

BotonLeer=Button(Ventana2, text="Leer", command=Leer)
BotonLeer.grid(row=0, column=1, padx=10, pady=10)

BotonActualizar=Button(Ventana2, text="Actualizar", command=Actualizar)
BotonActualizar.grid(row=0, column=2, padx=10, pady=10)

BotonEliminar=Button(Ventana2, text="Eliminar", command=Eliminar)
BotonEliminar.grid(row=0, column=3, padx=10, pady=10)

BotonLimpiar=Button(Ventana2, text="Limpiar", command=Limpiar)
BotonLimpiar.grid(row=1, column=1, padx=10, pady=10)

BotonSalir=Button(Ventana2, text="Salir", command=Salir)
BotonSalir.grid(row=1, column=2, padx=10, pady=10)

root.mainloop()