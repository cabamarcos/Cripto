from tkinter import *
from tkinter import messagebox
import sqlite3
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt #https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#cryptography.hazmat.primitives.kdf.scrypt.Scrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC #https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/#cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC
from cryptography.fernet import Fernet #https://cryptography.io/en/latest/fernet/#
import base64
from cryptography.hazmat.primitives.asymmetric import rsa #https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#generation
import json
from cryptography.hazmat.primitives import serialization #https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/#cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric import padding #https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#key-loading
import shutil #https://www.delftstack.com/es/howto/python/how-to-delete-files-and-directories-in-python/
from cryptography.hazmat.primitives.serialization import load_pem_public_key #https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/#cryptography.hazmat.primitives.serialization.load_pem_public_key
from cryptography import x509 #https://cryptography.io/en/latest/x509/tutorial/#creating-a-self-signed-certificate
from cryptography.x509.oid import NameOID #https://cryptography.io/en/latest/x509/tutorial/#creating-a-self-signed-certificate
import datetime
#-------------------Crear Base de Datos----------------------#

# MiConexion=sqlite3.connect(r"C:\Users\Damián\Desktop\Damián\AAINFORMÁTICA\AA-CURSOS\3º\1º Cuatri\Criptografía y Seguridad Informática\Proyecto\Cripto2\Cripto\Base de Datos") # DAMIÁN
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
    try:
        """Creamos registros"""

        MiConexion=sqlite3.connect(r"C:\Users\Damián\Desktop\Damián\AAINFORMÁTICA\AA-CURSOS\3º\1º Cuatri\Criptografía y Seguridad Informática\Proyecto\Cripto2\Cripto\Base de Datos") # DAMIÁN
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
            salt=salt2,
            iterations=390000,
        )
        bytekey2=VarPass.get().encode()
        #bytekey2=bytes(VarPass.get(), "ascii")

        keyFernet = base64.urlsafe_b64encode(kdf.derive(bytekey2))
        #---------------------------------------------

        f = Fernet(keyFernet)

        marca = VarMarca.get().encode()
        modelo = VarModelo.get().encode()
        año = VarAño.get().encode()
        fuel = VarFuel.get().encode()
        matricula = VarMatricula.get().encode()
        bastidor = VarBastidor.get().encode()

        tokenMarca = f.encrypt(marca).hex()
        tokenModelo = f.encrypt(modelo).hex()
        tokenAño = f.encrypt(año).hex()
        tokenFuel = f.encrypt(fuel).hex()
        tokenMatricula = f.encrypt(matricula).hex()
        tokenBastidor = f.encrypt(bastidor).hex()


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


        '''Creamos carpeta del usuario y guardamos la clave privada y publica'''

        os.mkdir("C:\\Users\\Damián\\Desktop\\Damián\\AAINFORMÁTICA\\AA-CURSOS\\3º\\1º Cuatri\Criptografía y Seguridad Informática\\Proyecto\\Cripto2\\Cripto\\" + VarNombre.get()) #Creamos un directorio para guardar los txt
        
        #os.mkdir(VarNombre.get()) #Creamos un directorio para guardar los txt #MARCOS

        #Hacer clave privada con contraseña RSA

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        privatepem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(bytekey)
        )

        #print(privatepem) @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        #Crear archivo json con la clave privada
        
        with open("C:\\Users\\Damián\\Desktop\\Damián\\AAINFORMÁTICA\\AA-CURSOS\\3º\\1º Cuatri\Criptografía y Seguridad Informática\\Proyecto\\Cripto2\\Cripto\\" + VarNombre.get() + "\\clave_privada.json", "w") as f: #DAMIÁN
            json.dump(privatepem.hex(), f)

        #Hacer clave publica desde clave privada RSA

        public_key = private_key.public_key()
        publicpem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        #print(publicpem) @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        #Crear archivo json con la clave publica

        with open("C:\\Users\\Damián\\Desktop\\Damián\\AAINFORMÁTICA\\AA-CURSOS\\3º\\1º Cuatri\Criptografía y Seguridad Informática\\Proyecto\\Cripto2\\Cripto\\" + VarNombre.get() + "\\clave_publica.json", "w") as f: #DAMIÁN
            json.dump(publicpem.hex(), f)

    except:
        messagebox.showerror("Error", "El nombre de usuario ya existente")
        
def Leer():
    """Lee los registros con un usuario y una contraseña"""

    MiConexion=sqlite3.connect(r"C:\Users\Damián\Desktop\Damián\AAINFORMÁTICA\AA-CURSOS\3º\1º Cuatri\Criptografía y Seguridad Informática\Proyecto\Cripto2\Cripto\Base de Datos") # DAMIÁN
    #MiConexion=sqlite3.connect("Base de Datos") # MARCOS

    MiCursor=MiConexion.cursor()

    MiCursor.execute("SELECT * FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get() +"'")

    Usuario=MiCursor.fetchall()

    for i in Usuario:

        hexkey =(i[1])
        hexsalt1 =(i[2])
        hexsalt2 =(i[3])

    # ----SCRIPT---------------------------------
    salt1=bytes.fromhex(hexsalt1)
    key=bytes.fromhex(hexkey)

    kdf = Scrypt(
    salt=salt1,
    length=32,
    n=2**14,
    r=8,
    p=1,
    )
    bytekey=VarPass.get().encode() #Extraemos la contraseña de la interfaz gráficay la codificamos en bytes

    try:
        kdf.verify(bytekey, key) #bytekey es la contraseña que introduce el usuario en el panel y key es la contraseña original

        #---------PBKDF2HMC---------------------------------
        salt2=bytes.fromhex(hexsalt2)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt2,
            iterations=390000,
        )
        bytekey2=VarPass.get().encode()

        keyFernet = base64.urlsafe_b64encode(kdf.derive(bytekey2))


        MiCursor.execute("SELECT * FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get() +"'")

        Usuario=MiCursor.fetchall()
        for i in Usuario:

            marca = (i[4])
            modelo = (i[5])
            año = (i[6])
            fuel = (i[7])
            matricula = (i[8])
            bastidor = (i[9])

        MiConexion.commit()

        #--------------FERNET-------------------------------
        bmarca = bytes.fromhex(marca)
        bmodelo = bytes.fromhex(modelo)
        baño = bytes.fromhex(año)
        bfuel = bytes.fromhex(fuel)
        bmatricula = bytes.fromhex(matricula)
        bbastidor = bytes.fromhex(bastidor)

        f = Fernet(keyFernet)

        aMarca = f.decrypt(bmarca).decode()
        aModelo = f.decrypt(bmodelo).decode()
        aAño = f.decrypt(baño).decode()
        aFuel = f.decrypt(bfuel).decode()
        aMatricula = f.decrypt(bmatricula).decode()
        aBastidor = f.decrypt(bbastidor).decode()

        #------------------------------------------------

        VarMarca.set(aMarca)
        VarModelo.set(aModelo)
        VarAño.set(aAño)
        VarFuel.set(aFuel)
        VarMatricula.set(aMatricula)
        VarBastidor.set(aBastidor)

        """ROTACIÓN DE CLAVES"""

        #TOKEN Y SALT 1

        salt = os.urandom(16)
        hexsalt1 = salt.hex()

        kdf = Scrypt(

            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
        )

        bytekey=VarPass.get().encode()
        key = kdf.derive(bytekey)
        hexkey=key.hex()

        MiCursor.execute("UPDATE DATOSUSUARIO SET CONTRASEÑA= '" + hexkey +
                                        "', SALT= '" + hexsalt1 +
                                        "' WHERE NOMBRE= '" + VarNombre.get() + "'")

        MiConexion.commit()

        #-------------------------------------------------------------------------------------

        #SALT 2

        salt2 = os.urandom(16)
        hexsalt2 = salt2.hex()

        # derive
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt2,
            iterations=390000,
        )
        bytekey2=VarPass.get().encode()

        keyFernet = base64.urlsafe_b64encode(kdf.derive(bytekey2))
        #---------------------------------------------

        f = Fernet(keyFernet)

        marca = VarMarca.get().encode()
        modelo = VarModelo.get().encode()
        año = VarAño.get().encode()
        fuel = VarFuel.get().encode()
        matricula = VarMatricula.get().encode()
        bastidor = VarBastidor.get().encode()

        tokenMarca = f.encrypt(marca).hex()
        tokenModelo = f.encrypt(modelo).hex()
        tokenAño = f.encrypt(año).hex()
        tokenFuel = f.encrypt(fuel).hex()
        tokenMatricula = f.encrypt(matricula).hex()
        tokenBastidor = f.encrypt(bastidor).hex()

        MiCursor.execute("UPDATE DATOSUSUARIO SET SALT2= '" + hexsalt2 +
                                        "', MARCA= '" + tokenMarca +
                                        "', MODELO= '" + tokenModelo +
                                        "', AÑO= '" + tokenAño +
                                        "', COMBUSTIBLE= '" + tokenFuel +
                                        "', MATRICULA= '" + tokenMatricula +
                                        "', BASTIDOR= '" + tokenBastidor +
                                        "' WHERE NOMBRE= '" + VarNombre.get() + "'")
        MiConexion.commit()


    except:
       messagebox.showwarning("BBDD", "Error al introducir la contraseña")

def Actualizar():
    """Actualizamos el registro con ese usuario y contraseña"""

    MiConexion=sqlite3.connect(r"C:\Users\Damián\Desktop\Damián\AAINFORMÁTICA\AA-CURSOS\3º\1º Cuatri\Criptografía y Seguridad Informática\Proyecto\Cripto2\Cripto\Base de Datos") # DAMIÁN
    #MiConexion=sqlite3.connect("Base de Datos") # MARCOS

    MiCursor=MiConexion.cursor()

    MiCursor.execute("SELECT * FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get() +"'")

    Usuario=MiCursor.fetchall()

    for i in Usuario:

        hexkey =(i[1])
        hexsalt1=(i[2])
        hexsalt2=(i[3])


    MiConexion.commit()

    # ----SCRIPT---------------------------------
    salt1=bytes.fromhex(hexsalt1)
    key=bytes.fromhex(hexkey)

    kdf = Scrypt(
    salt=salt1,
    length=32,
    n=2**14,
    r=8,
    p=1,
    )

    bytekey=VarPass.get().encode() #Extraemos la contraseña de la interfaz gráficay la codificamos en bytes

    try:
        kdf.verify(bytekey, key) #bytekey es la contraseña que introduce el usuario en el panel y key es la contraseña original

        #---------PBKDF2HMC---------------------------------
        salt2=bytes.fromhex(hexsalt2)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt2,
            iterations=390000,
        )
        bytekey2=VarPass.get().encode()

        keyFernet = base64.urlsafe_b64encode(kdf.derive(bytekey2))

        f = Fernet(keyFernet)

        marca = VarMarca.get().encode()
        modelo = VarModelo.get().encode()
        año = VarAño.get().encode()
        fuel = VarFuel.get().encode()
        matricula = VarMatricula.get().encode()
        bastidor = VarBastidor.get().encode()

        tokenMarca = f.encrypt(marca).hex()
        tokenModelo = f.encrypt(modelo).hex()
        tokenAño = f.encrypt(año).hex()
        tokenFuel = f.encrypt(fuel).hex()
        tokenMatricula = f.encrypt(matricula).hex()
        tokenBastidor = f.encrypt(bastidor).hex()


        MiCursor.execute("UPDATE DATOSUSUARIO SET MARCA= '" + tokenMarca +
                                        "', MODELO= '" + tokenModelo +
                                        "', AÑO= '" + tokenAño +
                                        "', COMBUSTIBLE= '" + tokenFuel +
                                        "', MATRICULA= '" + tokenMatricula +
                                        "', BASTIDOR= '" + tokenBastidor +
                                        "' WHERE NOMBRE= '" + VarNombre.get() + "'")
        MiConexion.commit()



        """ROTACIÓN DE CLAVES"""

        #SALT 1 Y TOKEN DE CONTRASEÑA

        salt = os.urandom(16)
        hexsalt1 = salt.hex()

        kdf = Scrypt(

            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
        )

        bytekey=VarPass.get().encode()
        key = kdf.derive(bytekey)
        hexkey=key.hex()

        MiCursor.execute("UPDATE DATOSUSUARIO SET CONTRASEÑA= '" + hexkey +
                                        "', SALT= '" + hexsalt1 +
                                        "' WHERE NOMBRE= '" + VarNombre.get() + "'")

        MiConexion.commit()

        #---------------------------------------------------------------------------------------------

        #SALT 2

        salt2 = os.urandom(16)
        hexsalt2 = salt2.hex()

        # derive
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt2,
            iterations=390000,
        )
        bytekey2=VarPass.get().encode()

        keyFernet = base64.urlsafe_b64encode(kdf.derive(bytekey2))
        #---------------------------------------------

        f = Fernet(keyFernet)

        marca = VarMarca.get().encode()
        modelo = VarModelo.get().encode()
        año = VarAño.get().encode()
        fuel = VarFuel.get().encode()
        matricula = VarMatricula.get().encode()
        bastidor = VarBastidor.get().encode()

        tokenMarca = f.encrypt(marca).hex()
        tokenModelo = f.encrypt(modelo).hex()
        tokenAño = f.encrypt(año).hex()
        tokenFuel = f.encrypt(fuel).hex()
        tokenMatricula = f.encrypt(matricula).hex()
        tokenBastidor = f.encrypt(bastidor).hex()

        MiCursor.execute("UPDATE DATOSUSUARIO SET SALT2= '" + hexsalt2 +
                                        "', MARCA= '" + tokenMarca +
                                        "', MODELO= '" + tokenModelo +
                                        "', AÑO= '" + tokenAño +
                                        "', COMBUSTIBLE= '" + tokenFuel +
                                        "', MATRICULA= '" + tokenMatricula +
                                        "', BASTIDOR= '" + tokenBastidor +
                                        "' WHERE NOMBRE= '" + VarNombre.get() + "'")
        MiConexion.commit()


        messagebox.showinfo("BBDD", "Registro actualizado conéxito")
    except:
        messagebox.showwarning("BBDD", "Error al introducir la contraseña")

def Eliminar():
    """Eliminamos el registro con ese usuario y esa contraseña"""

    MiConexion=sqlite3.connect(r"C:\Users\Damián\Desktop\Damián\AAINFORMÁTICA\AA-CURSOS\3º\1º Cuatri\Criptografía y Seguridad Informática\Proyecto\Cripto2\Cripto\Base de Datos") # DAMIÁN
    #MiConexion=sqlite3.connect("Base de Datos") # MARCOS

    MiCursor=MiConexion.cursor()

    MiCursor.execute("SELECT * FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get() +"'")

    Usuario=MiCursor.fetchall()

    for i in Usuario:

        hexkey =(i[1])
        hexsalt =(i[2])

    MiConexion.commit()

    salt=bytes.fromhex(hexsalt)
    key=bytes.fromhex(hexkey)

    kdf = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1,
    )

    bytekey=VarPass.get().encode() #Extraemos la contraseña de la interfaz gráficay la codificamos en bytes

    try:
        kdf.verify(bytekey, key) #bytekey es la contraseña que introduce el usuario en el panel y key es la contraseña original

        #BORRAMOS EL DIRECTORIO DEL USUARIO
        shutil.rmtree("C:\\Users\\Damián\\Desktop\\Damián\\AAINFORMÁTICA\\AA-CURSOS\\3º\\1º Cuatri\Criptografía y Seguridad Informática\\Proyecto\\Cripto2\\Cripto\\" + VarNombre.get())

        #BORRAMOS EL REGISTRO DE LA BBDD
        MiCursor.execute("DELETE FROM DATOSUSUARIO WHERE NOMBRE= '" + VarNombre.get() +"'")

        MiConexion.commit()
        messagebox.showinfo("BBDD", "Registro borrado con éxito")


        VarMarca.set("")
        VarModelo.set("")
        VarAño.set("")
        VarFuel.set("")
        VarMatricula.set("")
        VarBastidor.set("")

    except:
        messagebox.showwarning("BBDD", "Error al introducir la contraseña")

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

def Certificado():

    Leer() #Llamamos a la función leer para extraer los datos del usuario

    """Creamos un txt con los datos del usuario y vehículo"""

    txt=open("C:\\Users\\Damián\\Desktop\\Damián\\AAINFORMÁTICA\\AA-CURSOS\\3º\\1º Cuatri\Criptografía y Seguridad Informática\\Proyecto\\Cripto2\\Cripto\\" + VarNombre.get() + "\\" + VarNombre.get() + ".txt", "w") #Creamos un txt con el nombre del usuario

    txt.write("Nombre: " + VarNombre.get() + "\n" +
                "Marca: " + VarMarca.get() + "\n" +
                "Modelo: " + VarModelo.get() + "\n" +
                "Año: " + VarAño.get() + "\n" +
                "Combustible: " + VarFuel.get() + "\n" +
                "Matrícula: " + VarMatricula.get() + "\n" +
                "Bastidor: " + VarBastidor.get() + "\n")

    txt.close() #Cerramos el txt

    """Firmamos el txt con la clave privada del usuario"""

    #Serializar txt

    txt=open("C:\\Users\\Damián\\Desktop\\Damián\\AAINFORMÁTICA\\AA-CURSOS\\3º\\1º Cuatri\Criptografía y Seguridad Informática\\Proyecto\\Cripto2\\Cripto\\" + VarNombre.get() + "\\" + VarNombre.get() + ".txt", "r")

    message=txt.read().encode()

    txt.close()

    #Cargamos la clave privada del usuario

    with open("C:\\Users\\Damián\\Desktop\\Damián\\AAINFORMÁTICA\\AA-CURSOS\\3º\\1º Cuatri\Criptografía y Seguridad Informática\\Proyecto\\Cripto2\\Cripto\\" + VarNombre.get() + "\\clave_privada.json", "r") as f:
        privatepemhex=json.load(f)

    #Pasamos la clave privada a bytes
    privatepem=bytes.fromhex(privatepemhex)

    #Deserializamos la clave privada
    private_key = serialization.load_pem_private_key(
        privatepem,
        password=VarPass.get().encode(),
    )

    #Firmamos el txt
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    #Guardamos la firma en un json
    with open("C:\\Users\\Damián\\Desktop\\Damián\\AAINFORMÁTICA\\AA-CURSOS\\3º\\1º Cuatri\Criptografía y Seguridad Informática\\Proyecto\\Cripto2\\Cripto\\" + VarNombre.get() + "\\firma.json", "w") as f:
        json.dump(signature.hex(), f)

    
    """Creacion del certificado Autofirmado"""

    #Cargamos la clave privada del usuario
    with open("C:\\Users\\Damián\\Desktop\\Damián\\AAINFORMÁTICA\\AA-CURSOS\\3º\\1º Cuatri\Criptografía y Seguridad Informática\\Proyecto\\Cripto2\\Cripto\\" + VarNombre.get() + "\\clave_privada.json", "r") as f:
        privatepemhex=json.load(f)

    #Pasamos la clave privada a bytes
    privatepem=bytes.fromhex(privatepemhex)

    #Deserializamos la clave privada
    private_key = serialization.load_pem_private_key(
        privatepem,
        password=VarPass.get().encode(),
    )

    #Creamos certificado autofirmado
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"ES"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Madrid"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Leganés"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"UC3M"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"uc3m.es"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        # Our certificate will be valid for 10 days
        datetime.datetime.utcnow() + datetime.timedelta(days=10)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    # Sign our certificate with our private key
    ).sign(private_key, hashes.SHA256())

    certpem=cert.public_bytes(serialization.Encoding.PEM)
    #Guardamos el certificado en un json
    with open("C:\\Users\\Damián\\Desktop\\Damián\\AAINFORMÁTICA\\AA-CURSOS\\3º\\1º Cuatri\Criptografía y Seguridad Informática\\Proyecto\\Cripto2\\Cripto\\" + VarNombre.get() + "\\certificado.json", "w") as f:
        json.dump(certpem.hex(), f)
    

    """Verificacion del certificado"""

    #Cargamos el certificado
    with open("C:\\Users\\Damián\\Desktop\\Damián\\AAINFORMÁTICA\\AA-CURSOS\\3º\\1º Cuatri\Criptografía y Seguridad Informática\\Proyecto\\Cripto2\\Cripto\\" + VarNombre.get() + "\\certificado.json", "r") as f:
        certpemhex=json.load(f)
    #Pasamos el certificado a bytes
    certpem=bytes.fromhex(certpemhex)
    #Deserializamos el certificado
    cert = x509.load_pem_x509_certificate(certpem) 
    #Obtenemos la clave publica del certificado
    public_key=cert.public_key() 
    #Serializamos la clave publica
    publicpem=public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    #Funcion para verificar el certificado:
    try:
        issuer_public_key = load_pem_public_key(publicpem) #Como el CA(issuer) es el mismo que el usuario(subject) usamos la misma clave publica

        issuer_public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            # Depends on the algorithm used to create the certificate
            padding.PKCS1v15(),
            cert.signature_hash_algorithm,
        )
        messagebox.showinfo("Certificado", "El certificado es válido")
    except:
        messagebox.showwarning("Certificado", "El certificado no es válido")


    """Verificamos la firma"""

    # #Deserializamos la clave publica extraida del certificado
    public_key = load_pem_public_key(publicpem)

    #Cargamos la firma
    with open("C:\\Users\\Damián\\Desktop\\Damián\\AAINFORMÁTICA\\AA-CURSOS\\3º\\1º Cuatri\Criptografía y Seguridad Informática\\Proyecto\\Cripto2\\Cripto\\" + VarNombre.get() + "\\firma.json", "r") as f:
        signaturehex=json.load(f)

    #Pasamos la firma a bytes
    signature=bytes.fromhex(signaturehex)

    #Cargamos el mensaje
    txt=open("C:\\Users\\Damián\\Desktop\\Damián\\AAINFORMÁTICA\\AA-CURSOS\\3º\\1º Cuatri\Criptografía y Seguridad Informática\\Proyecto\\Cripto2\\Cripto\\" + VarNombre.get() + "\\" + VarNombre.get() + ".txt", "r")

    message=txt.read().encode()

    txt.close()
    
    try:
        #Verificamos la firma
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        messagebox.showinfo("Firma", "La firma es válida")        
    except:
        messagebox.showwarning("Firma", "La firma no es válida")


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

BotonSalir=Button(Ventana2, text="Certificado", command=Certificado)
BotonSalir.grid(row=1, column=2, padx=10, pady=10)

root.mainloop()