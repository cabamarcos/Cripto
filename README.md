# Desarrollo de una aplicación que utilice criptografía
## Objetivo
El objetivo de esta práctica es que los alumnos conozcan y aprendan a utilizar librerías
criptográficas para así afianzar los conceptos criptográficos estudiados en teoría. Así, se
proporciona un enunciado para crear un programa/ aplicación, cuya funcionalidad ha de ser
escogida por los alumnos, pero que debe realizar una serie de operaciones criptográficas.

## Descripción
El programa que se debe implementar en esta práctica debe realizarse en Python o Java y ha de
implementar de forma obligatoria las siguientes funciones criptográficas:

• Cifrado/ descifrado simétrico y asimétrico

• Funciones hash y HMAC

• Firma digital

• Método de autenticación

En todo momento es necesario utilizar algoritmos que se utilicen en la actualidad y que no hayan
sido comprometidos. Así, por ejemplo, DES no se debe utilizar, debiéndose utilizar AES en su
lugar.

### Cifrado y descifrado simétrico o asimétrico
En algún momento, en el sistema a desarrollar se tiene que producir un cifrado y descifrado de
información, pudiéndose ver el resultado de dichas operaciones. Nótese que, si el cifrado se
aplica, por ejemplo en comunicaciones, siendo transparente para el usuario, se ha de mostrar el
resultado en un log o en un mensaje de depuración, junto con el tipo de algoritmo y la longitud
de clave utilizada.
En lo referente a la generación de claves hay que considerar lo siguiente:

• Las claves han de tener una longitud apropiada y en relación con el algoritmo que se
esté utilizando.

### Generación y almacenamiento de claves
Las claves son elementos que han de estar protegidos frente a posibles ataques, aunque hay
que considerar las diferencias entre cifrado simétrico, asimétrico, firma digital y HMAC:

• Simétrico: dado que la clave de cifrado es la misma que la de descifrado, ésta podría
estar:

  o Almacenada en un fichero/base de datos. Dado que esta clave es secreta, podría
  ocurrir que se almacenase con algún tipo de protección (por ejemplo, cifrado
  con una contraseña introducida por el usuario)

  o Recordada por el usuario y utilizada en los momentos adecuados.

• Asimétrico: la clave de cifrado y descifrado son distintas y lo más habitual es que, dada
su longitud, no sean introducidas por los usuarios, sino que se creen y posteriormente,
el usuario podría utilizarlas porque estén:

  o Almacenadas en un fichero/base de datos y se seleccione la pública o la privada,
  según corresponda. Es posible que el acceso a la clave privada esté protegido y
  que ésta sólo sea accesible a través de una contraseña.

• Firma digital: dado que se utiliza cifrado asimétrico para realizar las firmas, las
cuestiones a considerar son las anteriormente expuestas.

  o En el caso de realizar firmas se utilizarán claves asimétricas, que también
  podrían ser utilizadas para el cifrado asimétrico, pero se hará uso de una PKI
  como la posteriormente descrita para la creación de dichas claves.

• HMAC: en la generación de HMAC se utiliza una única clave, de modo que las
consideraciones son las establecidas para el cifrado simétrico.

Hay que remarcar la importancia de que las claves tengan la longitud apropiada, tal y como se
indicaba anteriormente.
