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

#Funcion para procesar una linea que inica con VAR
def procesarVariables(linea):

    #Revisar que si sea VAR y no alguna combinacion de minusculas y mayusculas
    if linea.startswith(VARIABLES) == False:
        return False
    #Si la linea no termina con ;, no es valido el programa
    if linea.endswith(";") == False:
        return False
    linea = linea.removesuffix(';')

    #Se tokeniza la linea
    partes = linea.split()

    #Se agregan las variables al diccionario de variables existentes
    for i in range(1, len(partes)):
            #A la variable actual se le elimina la coma
            actual = partes[i].removesuffix(',')
            
            #Se revisa si la variable actual ya fue declarada, y si lo fue, no es valido el programa
            if actual in variablesExistentes:
                return False
            
            #Se agrega correctamente la variable con un valor inicial de null
            variablesExistentes[actual] = None

    #En caso de estar bien la linea, se retorna verdadero
    return True

    
#Funcion que revisa por completo el programa a partir de un archivo de texto. Retorna true si es valido, false d.l.c
def revisarArchivo(archivo):
   
    #Valor que se retorna al final de revisar el archivo. True si es valido, False d.l.c
    valido = True

    #Numero de lineas a leer
    numero = len(archivo.readlines())
    print(str(numero))

    #Lectura del archhivo completo, para revisar que PROG y GORP esten presents
    archivo.seek(0)
    inicioFinCorrecto = archivo.read().strip()
    

    #Verificar que el archivo inicie y termine correctamente. Si no es correcto, termina la revision y retorna falso
    if inicioFinCorrecto.startswith(INICIO) == False or inicioFinCorrecto.endswith(FIN) == False:
        valido = False
        return valido

    #Volver a iniciar la lectura del archivo
    archivo.seek(0)
    #Lectura primera linea que ya se reviso
    print(archivo.readline().strip())

    #Inicio revision del archivo completo
    for i in range(1, numero-1):
        lineaAct = archivo.readline().strip()
        if lineaAct.upper().startswith(VARIABLES) == True:
            if procesarVariables(lineaAct) == False:
                valido = False
                return valido
            

    pruebaLecturaAparte(archivo)
    print(archivo.readline().strip())

    return valido


print(revisarArchivo(f))




