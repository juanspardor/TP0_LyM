#Juan Sebastian Pardo - 201923794 - j.pardor

#Constantes
from operator import truediv


#Palabras reservadas del programa
INICIO = "PROG"
FIN = "GORP"
VARIABLES = "VAR"
METODO = "PROC"
FIN_METODO = "CORP"
CICLO_ABIERTO = "while"
HACER = "do"
DEJAR_HACER = "od"
CICLO_CERRADO = "REPEAT"
NEGACION = "not"

#Diccionario de metodos, donde la llave es el nombre y el valor es la cantidad de parametros que tiene
metodos = { "walk": 1, "jump": 1, "jumpTo": 2, "veer": 2, "look": 1, " drop": 1, "grab": 1, "get": 1, "free": 1, 
            "pop": 1, "walk": 2, "canWalk": 2}

#Lista que guarda las direcciones y sentidos validos para algunos metodos
direcciones = ["north", "south", "east", "west", "right", "left", "front", "back"]

#Diccionario de variables y su valor
variablesExistentes = {}

#Variable que guarda la cantidad total de instancias de PROC
totalProc = 0 

#Variable que guarda la cantidad total de instancias de CORP
totalCorp = 0 

#Variable que guarda la cantidad actual de instancias revisadas de PROC
cantidadProc = 0

#Variable que guarda la cantidad actual de instancias revisadas de CORP
cantidadCorp = 0

#Variable que guarda la lectura completa del archivo
inicioFinCorrecto = ""

#Cuando se haga el llamado a un metodo se revisa que exista la llave y que el numero de parametros agregados sea igual el valor que esta en el dict

#Cuando inicia un metodo, asegurarse que la siguiente linea sea '{'. D.l.c valido = false.
#Quizas tener un booleano que inidique si se abrieron los parentesis de un metodo, pero no estoy seguro de como hacer que no se putee si nunca se cierre

#Prueba para practicar lectura de archivos

f = open("EjemploEntrada.txt", "r")


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

#Funcion para declarar un bloque de instrucciones de un metodo
def declararInstruccionesMetodo(archivo, parametros):
    rta = True

    #Linea actual que se lee
    lineaAct = archivo.readline().strip()

    while (lineaAct == "}") == False:

        #Si la linea actual es "", se continua iterando
        if lineaAct == "":
            lineaAct = archivo.readline().strip()
            continue

        #Revision si es un WHILE
        if lineaAct.upper().startswith(CICLO_ABIERTO):
            lineaAct = archivo.readline().strip()
            continue

        #Revision si es un REPEAT
        if lineaAct.upper().startswith(CICLO_CERRADO):
            lineaAct = archivo.readline().strip()
            continue

        #Revision que sea una asignacion
        if lineaAct.find(":=") > - 1:

            #Si la instruccion no termina con ; el programa es invalido
            if not lineaAct.endswith(";"):
                return False

            #Si incluye ;, eliminarlo
            lineaAct.removesuffixx(";")
            
            #Hacer la particion de la linea: variable a asignar, valor a asignar
            variable = lineaAct.split(":=")[0]
            valor = lineaAct.split(":=")[1]

    return rta

#Funcion para procesar la declaracion de un PROC
def procesarPROC(programa, linea):
    rta = True
    #Si la declaracion no inicia con PROC, el programa es invalido
    if linea.startswith(METODO) == False:
        return False

    #Se obtiene la declaracion del metodo, es decir, nombre y parametros
    metodoCompleto = linea.split(METODO)[1].strip()

    #Revisar que los parametros esten entre parentesis
    if metodoCompleto.find("(") == -1 or metodoCompleto.find(")") == -1:
        return False
    
    #Se separan las partes de la declaracion de metodo: nombre y parametros
    partes = metodoCompleto.split("(")

    #Se obtiene el nombre del metodo a declarar
    nombreMetodo = partes[0]

    #Si se esta declarando un metodo ya existente, el programa es invalido
    if nombreMetodo in metodos:
        return False
    
    #Se obtienen los parametros sin limpiar, es decir, con ',' y ' )'
    parametrosSinLimpiar = partes[1].split(",")

    #Lista de los parametros limpios
    parametros = []

    #Proceso de limipar los parametros y ponerlos en la su lista correspondiente
    for x in parametrosSinLimpiar:
        parametros.append(x.removesuffix(')').strip())

    #Se agrega el metodo al diccionario de metodos, junto a su cantidad de parametros respectiva
    metodos[nombreMetodo] = len(parametros)

    #Variable para guardar la linea actual
    lineaAct = ""
    
    #Se busca el inicio del bloque de instrucciones "{"
    while (lineaAct == "{") == False:
        
        #Si antes del inicio del bloque de instrucciones hay algo disntito a "", el programa es invalido
        if not lineaAct == "":
            return False

        #Se actualiza la linea actual
        lineaAct = programa.readline().strip()

    #Una vez se entra al bloque, se inicia procesan las instrucciones
    declararInstruccionesMetodo(programa, parametros)
    return rta

#Metodo que hace la revision de las posicion de los siguientes PROC y CORP. En el dado caso que PROC este antes que CORP retorna falso
def revisionProcCorp():
    rta = True

    #Numero de instancia de CORP que se busca
    siguienteCorp = cantidadProc
    #Posicion en la que se empezara a iterar la busqueda de CORP
    locacionCorp = -1

    #Numero de instancia de PROC que se busca
    siguienteProc = cantidadProc + 1
    #Posicion en la que se empezara a iterar la busqueda de CORP
    locacionProc = -1

    #Busqueda CORP
    for i in range(0, siguienteCorp):
        locacionCorp = inicioFinCorrecto.find(FIN_METODO, locacionCorp+1)

    #Busqueda PROC
    for i in range(0, siguienteProc):
        locacionProc = inicioFinCorrecto.find(METODO, locacionProc +1)

    #Si hay un PROC antes del siguiente CORP, se retorna falso
    if locacionProc < locacionCorp:
        return False

    return rta
    
#Funcion que revisa por completo el programa a partir de un archivo de texto. Retorna true si es valido, false d.l.c
def revisarArchivo(archivo):
   
    #Valor que se retorna al final de revisar el archivo. True si es valido, False d.l.c
    valido = True

    #Numero de lineas a leer
    numero = len(archivo.readlines())
    print(str(numero))

    #Lectura del archhivo completo
    archivo.seek(0)
    global inicioFinCorrecto
    inicioFinCorrecto = archivo.read().strip()

    #Verificar que el archivo inicie y termine correctamente. Si no es correcto, termina la revision y retorna falso
    if inicioFinCorrecto.startswith(INICIO) == False or inicioFinCorrecto.endswith(FIN) == False:
        valido = False
        return valido


    #Verificar que todo bloque que se abra, se cierre. Ya sea de instrucciones o de PROC
    if not inicioFinCorrecto.count("{") == inicioFinCorrecto.count("}"):
        valido = False
        return valido

    #Verificar que todos los PROC tengan su CORP respectivo. ACA TOCA DEVOLVER EL NOT
    totalCorp = inicioFinCorrecto.count(FIN_METODO)
    totalProc = inicioFinCorrecto.count(METODO)
    if  not totalCorp == totalProc:
        valido = False
        return valido
    

    
    #Volver a iniciar la lectura del archivo
    archivo.seek(0)
    #Lectura primera linea que ya se reviso
    print(archivo.readline().strip())

    #Inicio revision del archivo completo
    for i in range(1, numero-1):
        #Lectura linea actual
        lineaAct = archivo.readline().strip()

        #Si la linea actual es "", no se revisa nada y se pasa a la siguiente iteracion
        if lineaAct == "":
            continue

        #Se revisa si la linea actual es de declaracion de variables, y en dado caso se procesa con su funcion respectiva
        if lineaAct.upper().startswith(VARIABLES) == True:
            #Si no es correcta la declaracion, no es correcto el programa
            if procesarVariables(lineaAct) == False:
                valido = False
                return valido
        
        #Para revisar un PROC toca verificar 2 cosas:
        #1. Que despues del PROC eventualmente este un CORP, no puede iniciar otro PROC.
        #Es decir, find(CORP desde act) < find(PROC desde act). FALTA HACER ESTO, TOCARIA HACER OTRA FUNCION 
        #A esa funcion se le mete inicioFinCorrecto, cantidadProc y cantidadCopr para revisar usando algun metodo de Nth substring en google
        if lineaAct.upper().startswith(METODO):
            #Aumenta la cantidad de PROC's revisados
            global cantidadProc
            cantidadProc = cantidadProc + 1

            #Si es el ulitmo PROC y el penultimo CORP, no hay necesidad de revisar que esten bien organizados
            if not cantidadProc == totalProc and cantidadCorp == totalCorp -1:

                #Se revisa si el siguiente CORP esta antes del siguiente PROC. Si esta antes, el programa es invalido
                if not revisionProcCorp():
                    valido = False
                    return valido

            #En este momento ya se puede hacer el procesamiento del PROC correctamente
            if procesarPROC(archivo, lineaAct) == False:
                valido = False
                return valido


    print(archivo.readline().strip())

    return valido


print(revisarArchivo(f))




