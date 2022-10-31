from tkinter import *
from tkinter import messagebox
import sqlite3
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt #https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#cryptography.hazmat.primitives.kdf.scrypt.Scrypt
from cryptography.hazmat.primitives import hashes            
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC #https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC
from cryptography.fernet import Fernet #https://cryptography.io/en/latest/fernet/#



#-------------------Crear Base de Datos"----------------------#

# MiConexion=sqlite3.connect(r"C:\Users\Damián\Desktop\Damián\AAINFORMÁTICA\AA-CURSOS\3º\1º Cuatri\Criptografía y Seguridad Informática\Proyecto\Cripto\Base de Datos") # DAMIÁN
# #MiConexion=sqlite3.connect("Base de Datos") # MARCOS
# MiCursor=MiConexion.cursor()

# MiCursor.execute("CREATE TABLE DATOSUSUARIO (NOMBRE VARCHAR(255) PRIMARY KEY, CONTRASEÑA VARCHAR(255), SALT VARCHAR(255), SALT2 VARCHAR(255), MARCA VARCHAR(255), MODELO VARCHAR(255), AÑO VARCHAR(255), COMBUSTIBLE VARCHAR(255), MATRICULA VARCHAR(255), BASTIDOR VARCHAR(255))")

# MiConexion.close()

root=Tk()

# Creadores=Menu(root)
# root.config(menu=Creadores, width=300, height=300)
# Creadores.add_cascade(label="Creadores Damián y Marcos")

#-----------------Funciones------------------#

def Crear():
    """Creamos registros"""

    MiConexion=sqlite3.connect(r"C:\Users\Damián\Desktop\Damián\AAINFORMÁTICA\AA-CURSOS\3º\1º Cuatri\Criptografía y Seguridad Informática\Proyecto\Cripto\Base de Datos") # DAMIÁN
    #MiConexion=sqlite3.connect("Base de Datos") # MARCOS

    MiCursor=MiConexion.cursor()

    #SALT 1 PARA TOKEN DE CONTRASEÑA
    salt = os.urandom(16)
    strsalt = salt.hex()

    kdf = Scrypt(

        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    )

    bytekey=VarPass.get().encode()
    key = kdf.derive(bytekey)
    strkey=key.hex()
    #-------------------------------

    #SALT 2 PARA CIFRADO SIMETRICO

    salt2 = os.urandom(16)
    strsalt2 = salt2.hex()

    # derive
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    bytekey2=VarPass.get().encode()
    
    key2 = kdf.derive(bytekey2)
    strkey2=key2.hex()
    #---------------------------------------------
    keyPRUEBA = Fernet.generate_key()
    print(key2)
    print(type(key2))
    print(keyPRUEBA)
    print(type(keyPRUEBA))

    #key = base64.urlsafe_b64encode(kdf.derive(password))

    f = Fernet(strkey2)
    #marca = VarMarca.get().encode()
    #modelo = VarModelo.get().encode()
    #año = VarAño.get().encode()
    #fuel = VarFuel.get().encode()
    #matricula = VarMatricula.get().encode()
    #bastidor = VarBastidor.get().encode()

    tokenMarca = f.encrypt(VarMarca.get().encode())
    tokenModelo = f.encrypt(VarModelo.get().encode())
    tokenAño = f.encrypt(VarAño.get().encode())
    tokenFuel = f.encrypt(VarFuel.get().encode())
    tokenMatricula = f.encrypt(VarMatricula.get().encode())
    tokenBastidor = f.encrypt(VarBastidor.get().encode())
    
    MiCursor.execute("INSERT INTO DATOSUSUARIO VALUES('" + VarNombre.get() 
                                                    + "','" + strkey
                                                    + "','" + strsalt
                                                    + "','" + strsalt2
                                                    + "','" + tokenMarca
                                                    + "','" + tokenModelo
                                                    + "','" + tokenAño
                                                    + "','" + tokenFuel 
                                                    + "','" + tokenMatricula 
                                                    + "','" + tokenBastidor + "')")
    MiConexion.commit()
    messagebox.showinfo("BBDD", "Registro insertado con éxito")

def Leer():
    """Lee los registros con un usuario y una contraseña"""

    MiConexion=sqlite3.connect(r"C:\Users\Damián\Desktop\Damián\AAINFORMÁTICA\AA-CURSOS\3º\1º Cuatri\Criptografía y Seguridad Informática\Proyecto\Cripto\Base de Datos") # DAMIÁN
    #MiConexion=sqlite3.connect("Base de Datos") # MARCOS

    MiCursor=MiConexion.cursor()

    MiCursor.execute("SELECT * FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get() +"'")

    Usuario=MiCursor.fetchall()
    
    for i in Usuario:

        hexsalt=(i[2])
    
    #key=bytes.fromhex(hexkey)    
    salt=bytes.fromhex(hexsalt)

    kdf = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1,
    )
    #kdf.verify(b'VarPass.get()', key)
    bytekey=VarPass.get().encode()
    key = kdf.derive(bytekey)
    strkey=key.hex()

    MiCursor.execute("SELECT * FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get() 
                                            + "' AND CONTRASEÑA= '" + strkey +"'")

    Usuario=MiCursor.fetchall()
    
    for i in Usuario:

        VarMarca.set(i[4])
        VarModelo.set(i[5])
        VarAño.set(i[6])
        VarFuel.set(i[7]) 
        VarMatricula.set(i[8])
        VarBastidor.set(i[9])
    
    MiConexion.commit()

    
def Actualizar():
    """Actualizamos el registro con ese usuario y contraseña"""

    MiConexion=sqlite3.connect(r"C:\Users\Damián\Desktop\Damián\AAINFORMÁTICA\AA-CURSOS\3º\1º Cuatri\Criptografía y Seguridad Informática\Proyecto\Cripto\Base de Datos") # DAMIÁN
    #MiConexion=sqlite3.connect("Base de Datos") # MARCOS

    MiCursor=MiConexion.cursor()

    MiCursor.execute("SELECT * FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get() +"'")

    Usuario=MiCursor.fetchall()
    
    for i in Usuario:

        hexsalt=(i[2])

    MiConexion.commit()
    
    #key=bytes.fromhex(hexkey)    
    salt=bytes.fromhex(hexsalt)

    kdf = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1,
    )
    #kdf.verify(b'VarPass.get()', key)
    bytekey=VarPass.get().encode()
    key = kdf.derive(bytekey)
    strkey=key.hex()


    MiCursor.execute("SELECT * FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get() 
                                            + "' AND CONTRASEÑA= '" + strkey +"'")

    Usuario=MiCursor.fetchall()

    for i in Usuario:
        
        VerUsuario = (i[0])
        VerPass = (i[1])

    MiConexion.commit()

    if VerUsuario == VarNombre.get() and VerPass == strkey:

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
    
    MiConexion=sqlite3.connect(r"C:\Users\Damián\Desktop\Damián\AAINFORMÁTICA\AA-CURSOS\3º\1º Cuatri\Criptografía y Seguridad Informática\Proyecto\Cripto\Base de Datos") # DAMIÁN
    #MiConexion=sqlite3.connect("Base de Datos") # MARCOS

    MiCursor=MiConexion.cursor()

    MiCursor.execute("SELECT * FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get() +"'")

    Usuario=MiCursor.fetchall()
    
    for i in Usuario:

        hexsalt=(i[2])

    MiConexion.commit()
    
    #key=bytes.fromhex(hexkey)    
    salt=bytes.fromhex(hexsalt)

    kdf = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1,
    )
    #kdf.verify(b'VarPass.get()', key)
    bytekey=VarPass.get().encode()
    key = kdf.derive(bytekey)
    strkey=key.hex()

    MiCursor.execute("SELECT * FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get() 
                                            + "' AND CONTRASEÑA= '" + strkey +"'")

    Usuario=MiCursor.fetchall()

    for i in Usuario:
        
        VerUsuario = (i[0])
        VerPass = (i[1])

    MiConexion.commit()

    if VerUsuario == VarNombre.get() and VerPass == strkey:

        MiCursor.execute("DELETE FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get()
                                                + "' AND CONTRASEÑA= '" + strkey +"'")
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