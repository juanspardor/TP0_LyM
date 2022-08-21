#Juan Sebastian Pardo - 201923794 - j.pardor
#Juan Sebastian Grillo

import sys

#Constantes
INICIO = "PROG"
FIN = "GORP"
VARIABLES = "VAR"
METODO = "PROC"

#Diccionario de metodos, donde la llave es el nombre y el valor es la cantidad de parametros que tiene
metodos = { "walk": 1, "jump": 1, "jumpTo": 2, "veer": 2, "look": 1, " drop": 1, "grab": 1, "get": 1, "free": 1, 
            "pop": 1, "walk": 2, "canWalk": 2}

#Diccionario de variables y su valor
variablesExistentes = {}



#Al leer la primera linea, revisar que sea PROG. D.l.c valido = false
#Al leer la ultima linea, revisar que sea GORP. D.l.c valido = false


#Tener un diccionario con las variables donde la llave es el nombre y el valor es el valor asignacio. Iniciamos con valor = null

#Tener un diccionario con los metodos, donde la llave es el nombre y el valor es el numero de parametros. 
#Cuando se haga el llamado a un metodo se revisa que exista la llave y que el numero de parametros agregados sea igual el valor que esta en el dict

#Cuando inicia un metodo, asegurarse que la siguiente linea sea '{'. D.l.c valido = false.
#Quizas tener un booleano que inidique si se abrieron los parentesis de un metodo, pero no estoy seguro de como hacer que no se putee si nunca se cierre

#Prueba para practicar lectura de archivos

f = open("EjemploEntrada.txt", "r")

#Revisar que continue la lectura a partir del punto que se llego por ultima vez en otra funcion
def pruebaLecturaAparte(X):
    print(X.readline().strip())


#Funcion que revisa por completo el programa a partir de un archivo de texto. Retorna true si es valido, false d.l.c
def revisarArchivo(archivo):
   
    #Valor que se retorna al final de revisar el archivo. True si es valido, False d.l.c
    valido = True

    #Lectura del archhivo completo, para revisar que PROG y GORP esten presents
    inicioFinCorrecto = archivo.read().strip()
    archivo.readlines()

    #Verificar que el archivo inicie y termine correctamente. Si no es correcto, termina la revision y retorna falso
    if inicioFinCorrecto.startswith(INICIO) == False or inicioFinCorrecto.endswith(FIN) == False:
        valido = False
        return valido

    #Volver a iniciar la lectura del archivo
    archivo.seek(0)
    print(archivo.readline().strip())
    pruebaLecturaAparte(archivo)
    print(archivo.readline().strip())

    return valido


print(revisarArchivo(f))




