#Juan Sebastian Pardo - 201923794 - j.pardor

#ARCHIVO PARA EJECUTAR EL PROYECTO.
#PARA EJECUTAR:
# - Si el archivo esta en el mismo directorio que este .py, solo poner el nombre como primer parametro
# - Si el archivo esta en otro directorio, poner la direccion como primer parametro
programaARevisar = open("EjemploEntrada.txt", "r")

#Palabras reservadas del programa
INICIO = "PROG"
FIN = "GORP"
VARIABLES = "VAR"
METODO = "PROC"
FIN_METODO = "CORP"
CICLO_ABIERTO = "while"
HACER = "do"
DEJAR_HACER = "od"
CICLO_CERRADO = "repeatTimes"
FIN_CICLO_CERRADO = "per"
NEGACION = "not"
INICIO_CONDICIONAL = "if"
FIN_CONDICIONAL = "fi"
DE_LO_CONTRARIO = ""

#Diccionario de metodos, donde la llave es el nombre y el valor es la cantidad de parametros que tiene
metodos = { "walk1": 1, "jump": 1, "jumpTo": 2, "veer": 1, "look": 1, "drop": 1, "grab": 1, "get": 1, "free": 1, 
            "pop": 1, "walk2": 2, "canWalk": 2, "isFacing": 1, "isValid": 2}

#Lista de metodos que tienen como parametro una diraccion o sentido
metodosDireccionales = ["veer", "look", "walk2"]

#Lista de condicionales
condicinales = ["canWalk", "isFacing", "isValid"]


#Lista que guarda las direcciones y sentidos validos para algunos metodos
parametrosVeer = ["left", "right", "around"]
parametrosLook = ["north", "south", "east", "west"]
parametrosWalk = ["left", "right", "front", "back", "north", "south", "east", "west"]
parametrosIsValid = ["walk", "jump", "grab", "pop", "pick", "free", "drop"]

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

#Funcion para procesar el llamado a un metodo EXISTENTE. Tiene 3 parametros, en orden:
# 1. nombreMetodo: nombre del metodo a validar
# 2. parametrosLlamado: lista con los parametros que estaban en el llamado directo (en el readline)
# 3. parametrosProc: en el caso que venga de un bloque de instrucciones despues de un PROC, es una lista con los parametros del PROC. Si no lo es, es vacia
def validarInstruccion(nombreMetodo, parametrosLlamado, parametrosProc):
    rta = True
    
    #Primero se revisa si el metodo hace parte de los direccionales, ya que estos tienen mas restricciones en los parametros
    if nombreMetodo in metodosDireccionales or nombreMetodo in condicinales:
        
        #Se verifica si es veer
        if nombreMetodo == "veer":
            #Si el parametro no hace parte del conjunto de valores esperados, el programa es invalido
            if not parametrosLlamado[0] in parametrosVeer:
                return False
            return rta

        #Se verifica si es look
        if nombreMetodo == "look":
            #Si el parametro no hace parte del conjunto de valores esperados, el programa es invalido
            if not parametrosLlamado[0] in parametrosLook:
                return False
            return rta

        #Se verifica si es walk
        if nombreMetodo == "walk2":
            #Si el primer parametro no hace parte del conjunto de valores esperados, el programa es invalido
            if not parametrosLlamado[0] in parametrosWalk:
                return False

            #Para el segundo parametro toca revisar que sea un digito, o que sea un variable existente o un parametro que llega de la definicion de un PROC
            esDigito = parametrosLlamado[1].isdigit()
            esVariableYaDefinida = parametrosLlamado[1] in variablesExistentes
            esParametroDeEntrada = parametrosLlamado[1] in parametrosProc

            #Si todos estos son falsos, el programa es invalido 
            if not(esDigito or esVariableYaDefinida or esParametroDeEntrada):
                return False
            return rta

        #Se verifica si es isValid
        if nombreMetodo == "isValid":
            #Si el parametro no hace parte de los valores esperados, el programa es invalido
            if not parametrosLlamado[0] in parametrosIsValid:
                return False
            return rta

        #Se verifica si es isFacing
        if nombreMetodo == "isFacing":
            #Si el parametro no hace parte de los valores esperados, el programa es invalido
            if not parametrosLlamado[0] in parametrosLook:
                return False
            return rta

        #Se verifica si es canWalk
        if nombreMetodo == "canWalk":
            #Si el primer parametro no hace parte del conjunto de valores esperados, el programa es invalido
            if not parametrosLlamado[0] in parametrosWalk:
                return False

            #Para el segundo parametro toca revisar que sea un digito, o que sea un variable existente o un parametro que llega de la definicion de un PROC
            esDigito = parametrosLlamado[1].isdigit()
            esVariableYaDefinida = parametrosLlamado[1] in variablesExistentes
            esParametroDeEntrada = parametrosLlamado[1] in parametrosProc

            #Si todos estos son falsos, el programa es invalido 
            if not(esDigito or esVariableYaDefinida or esParametroDeEntrada):
                return False
            return rta

    #Si no es uno de los metodos direccionales, es otro de los metodos predefinidos, que aceptan direcciones o sentidos 
    
    #Primero se revisa jumpTo, ya que tiene 2 parametros
    if nombreMetodo == "jumpTo":
        #Para cada uno de sus parametros, tiene que ser un digito, una variable existente, o un parametro que llega desde PROC
        for paramAct in parametrosLlamado:
            esDigito = paramAct.isdigit()
            esVariableYaDefinida = paramAct in variablesExistentes
            esParametroDeEntrada = paramAct in parametrosProc
            #Si todos estos son falsos, el programa es invalido 
            if not(esDigito or esVariableYaDefinida or esParametroDeEntrada):
                return False
            return rta

    #El resto de metodos no-direccionales, solo tienen 1 parametro para revisar
    #Para dicho parametro toca revisar que sea un digito, o que sea un variable existente o un parametro que llega de la definicion de un PROC
    esDigito = parametrosLlamado[0].isdigit()
    esVariableYaDefinida = parametrosLlamado[0] in variablesExistentes
    esParametroDeEntrada = parametrosLlamado[0] in parametrosProc

    #Si todos estos son falsos, el programa es invalido 
    if not(esDigito or esVariableYaDefinida or esParametroDeEntrada):
            return False

    return rta 

#Funcion para procesar una instruccion while o if - else. El parametro parametrosProc esta en el caso que se llame a la funcion desde un bloque de instruccion de un PROC
def validarWhile(linea, parametrosProc):
    rta = True

    #Posicion en la linea de do
    posDo  = linea.find(HACER)

    #Posicion inicio bloque
    posInicio = linea.find("{")

    #Posicion fin bloque 
    posFin = linea.find("}")

    #Si los brackets del bloque de instrucciones estan en un orden incorrecto el programa es invalido
    if posInicio > posFin:
        return False

    #Se valida que el bloque de instrucciones este entre do y od. Es decir, '{' y '}' antes de od y despues de od
    despuesDo = (posInicio > posDo) and (posFin > posDo)
    if not despuesDo:
        return False

    #Se hace la division para revisar primero la condicion y posteriormente el bloque de instrucciones
    divisionGrande = linea.split(HACER)

    #Seccion de la condicion
    seccionCondicion = divisionGrande[0].strip()

    #Seccion del bloque de instrucciones 
    seccionBloque = divisionGrande[1].strip()

    #REVISION CONDICION-----------------
    seccionCondicion = seccionCondicion.removeprefix(CICLO_ABIERTO).strip()

    #Si la condicion no esta entre parentesis o hay algun tipo de texto diferente, el programa es invalido
    if not seccionCondicion.startswith("(") and seccionCondicion.endswith(")"):
        return False

    #Se elimina el primer y ultimo parentesis
    seccionCondicion = seccionCondicion.removeprefix("(").strip()
    seccionCondicion = seccionCondicion.removesuffix(")").strip()

    #Se revisa si hay un not
    if seccionCondicion.lower().startswith(NEGACION):
        #Si no esta escrito exactamente 'not' el programa es invalido
        if not seccionCondicion.startswith(NEGACION):
            return False

        #Si hay un not se elemina
        seccionCondicion = seccionCondicion.removeprefix(NEGACION).strip()
        
        #Si no se inicia y termina la condicion con parentesis o hay algo disntinto, el programa es invalido
        if not seccionCondicion.startswith("(") and seccionCondicion.endswith(")"):
            return False

        #Se elimina el primer y ultimo parentesis
        seccionCondicion = seccionCondicion.removeprefix("(").strip()
        seccionCondicion = seccionCondicion.removesuffix(")").strip()

    #Una vez procesada la posible existencia de un not, se verifica la condicion en si
    #Si la condicion no termina en parentesis, el programa es invalido
    if not seccionCondicion.endswith(")"):
        return False
    
    #Si la condicion no tiene (, el programa es invalido
    if not seccionCondicion.find("(") > -1:
        return False

    #Separacion del nombre de la condicion y sus parametros
    nombreCondicion = seccionCondicion.split("(")[0].strip()

    #Parametros en el llamado a la condicion. Se inicia con la particion entre parametros con comas
    parametrosFragmentados = seccionCondicion.split("(")[1].removesuffix(")").strip().split(",")

    #Lista que tendra los parametros individuales
    parametrosLinea = []
            
    #Ciclo para agregar los parametros individuales a su lista respectiva
    for x in parametrosFragmentados:
        parametrosLinea.append(x.strip())
    
    #Si la condicion no esta en la lista de condiciones, el programa es invalido
    if not nombreCondicion in condicinales:
        return False
    
    #Si el numero de parametros de la condicion no es igual al determinado, el programa es invalido
    if not metodos[nombreCondicion] == len(parametrosLinea):
        return False

    #Si la condicion en si no es valida, el programa no es valido
    if not validarInstruccion(nombreCondicion, parametrosLinea, parametrosProc):
        return False
    
    #REVISION BLOQUE    -----------------
    #Eliminar od para quedar con el bloque unicamente
    seccionBloque = seccionBloque.removesuffix("od").strip()

    #Si el bloque no inicia y termina con { }, el programa es invalido
    if not seccionBloque.startswith("{") and seccionBloque.endswith("}"):
        return False

    #Eliminacion de brackets
    seccionBloque = seccionBloque.removeprefix("{").strip()
    seccionBloque = seccionBloque.removesuffix("}").strip()

    #Si la ultima instruccion del bloque no termina en ;, el programa es invalido
    if not seccionBloque.endswith(";"):
        return False
    
    #Se hace la separacion de instrucciones en el caso que haya mas de una
    instrucciones = seccionBloque.split(";")
    instrucciones.pop()
    #Revision individual de cada instruccion
    for instruccionActual in instrucciones:
        
        instruccionActual = instruccionActual.strip()
        #Si la instruccion no tiene ( y termina en ), el programa es invalido
        if not instruccionActual.find("(") > -1 and instruccionActual.endswith(")"):
            return False
        
        #Eliminar ; al final de la instruccion
        instruccionActual = instruccionActual.removesuffix(")")

        #Separacion del nombre del metodo y sus parametros
        nombreMetodo = instruccionActual.split("(")[0].strip()

        #Parametros en el llamado al metodo. Se inicia con la particion entre parametros con comas
        parametrosFragmentados = instruccionActual.split("(")[1].strip().split(",")

        #Lista que tendra los parametros individuales
        parametrosLinea = []
            
        #Ciclo para agregar los parametros individuales a su lista respectiva
        for x in parametrosFragmentados:
            parametrosLinea.append(x.strip())

        #Dado que el metodo dos tiene un parametro opcional, toca ajustar el "nombre" para procesarlo correctamente
        if nombreMetodo == "walk" and len(parametrosLinea) == 1:
            nombreMetodo = "walk1"
            
        if nombreMetodo == "walk" and len(parametrosLinea) == 2:
            nombreMetodo = "walk2"

        #Si el nombre del metodo no esta en los metodos existentes, el programa es invalido
        if not nombreMetodo in metodos:
            return False

        #Si el numero de parametros no es igual al numero esperado, el programa es invalido
        if not metodos[nombreMetodo] == len(parametrosLinea):
            return False
            
        #En este punto, se sabe que el metodo pertenece a los metodos existentes, asi que toca revisar que el numero/tipo de parametros es correcto
        #Si la instruccion no es valida, el programa es invalido
        if not validarInstruccion(nombreMetodo, parametrosLinea, parametrosProc):
            return False

    return rta





#Funcion para declarar un bloque de instrucciones de un metodo
def procesarBloqueInstrucciones(archivo, parametros):
    rta = True

    #Linea actual que se lee
    lineaAct = archivo.readline().strip()

    #Se revisa cada una de las lineas dentro del bloque de instrucciones
    while (lineaAct == "}") == False:
        print(lineaAct)
        print("Estoy aca")
        #Si la linea actual es "", se continua iterando
        if lineaAct == "":
            lineaAct = archivo.readline().strip()
            continue

        #Revision si es un WHILE
        if lineaAct.startswith(CICLO_ABIERTO) and lineaAct.endswith(DEJAR_HACER):
            #Si no se cuenta con do y od, el programa no es valido
            if not lineaAct.find(HACER) > -1 and lineaAct.find(DEJAR_HACER) > -1:
                return False

            #Si no se cuenta con los brackets del bloque de isntrucciones, el programa no es valido
            if not lineaAct.find("{") > -1 and lineaAct.find("}") > -1:
                return False

            if not validarWhile(lineaAct, parametros):
                return False

            lineaAct = archivo.readline().strip()
            continue

        #Revision si es un REPEAT
        if lineaAct.startswith(CICLO_CERRADO) and lineaAct.startswith(FIN_CICLO_CERRADO):
            lineaAct = archivo.readline().strip()
            continue
        
        #Revision si es un condicional
        if lineaAct.startswith(INICIO_CONDICIONAL) and lineaAct.endswith(FIN_CONDICIONAL):


            lineaAct = archivo.readline().strip()
            continue
        #Revision que sea una asignacion
        if lineaAct.find(":=") > - 1:

            #Si la instruccion no termina con ; el programa es invalido
            if not lineaAct.endswith(";"):
                return False

            #Si incluye ;, eliminarlo
            lineaAct = lineaAct.removesuffix(";")
            
            #Hacer la particion de la linea: variable a asignar, valor a asignar
            variable = lineaAct.split(":=")[0].strip()
            valor = lineaAct.split(":=")[1].strip()

            #Revision que el valor sea un digito
            if not valor.isdigit():
                return False

            #Si la asignacion es a una de las variables que entra por parametro no pasa nada
            if variable in parametros:
                lineaAct = archivo.readline().strip()
                continue
            
            #Si la variable no es una variables globales, el programa es invalido
            if not variable in variablesExistentes:
                return False

            #Ya al descartar todas las opciones de asignacion, si se llega hasta este punto, la asignacion es a una variable global
            variablesExistentes[variable] = valor

            #Se actualiza la linea actual y se itera
            lineaAct = archivo.readline().strip()
            continue

        #Revision si es uno de los metodos existentes
        #Si la instruccion no termina con ; el programa es invalido
        if not lineaAct.endswith(";"):
            return False
        
        #Si tiene dos parentesis, es un llamado a un metodo, por lo que se valida
        if (lineaAct.count("(")== 1 and lineaAct.endswith(");") == 1):

            #Si la posicion de los parentesis es incorrecta, el programa es invalido
            if lineaAct.find("(") > lineaAct.find(")"):
                return False
            #Eliminar ; al final de la instruccion
            lineaAct = lineaAct.removesuffix(");")

            #Separacion del nombre del metodo y sus parametros
            nombreMetodo = lineaAct.split("(")[0].strip()

            #Parametros en el llamado al metodo. Se inicia con la particion entre parametros con comas
            parametrosFragmentados = lineaAct.split("(")[1].strip().split(",")

            #Lista que tendra los parametros individuales
            parametrosLinea = []
            
            #Ciclo para agregar los parametros individuales a su lista respectiva
            for x in parametrosFragmentados:
                parametrosLinea.append(x.strip())

            #Dado que el metodo dos tiene un parametro opcional, toca ajustar el "nombre" para procesarlo correctamente
            if nombreMetodo == "walk" and len(parametrosLinea) == 1:
                nombreMetodo = "walk1"
            
            if nombreMetodo == "walk" and len(parametrosLinea) == 2:
                nombreMetodo = "walk2"

            #Si el nombre del metodo no esta en los metodos existentes, el programa es invalido
            if not nombreMetodo in metodos:
                return False

            #Si el numero de parametros no es igual al numero esperado, el programa es invalido
            if not metodos[nombreMetodo] == len(parametrosLinea):
                return False
            
            #En este punto, se sabe que el metodo pertenece a los metodos existentes, asi que toca revisar que el numero/tipo de parametros es correcto
            #Si la instruccion no es valida, el programa es invalido
            if not validarInstruccion(nombreMetodo, parametrosLinea, parametros):
                return False
            
            #Si la instruccion es valida, se continua iterando
            lineaAct = archivo.readline().strip()
            continue   
        #Si se llego hasta este punto, la linea dentro del bloque de instrucciones no pertenece a la sintaxis del programa, y este es invalido
        return False
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

    #Una vez se entra al bloque, se inicia procesan las instrucciones. Si estas son invalidas, el programa es invalido
    if not procesarBloqueInstrucciones(programa, parametros):
        return False
    
    #Actualizar la linea actual
    lineaAct = programa.readline().strip()

    #Al ser el bloque de instrucciones valido, se busca CORP para terminar de revisar el metodo. 
    while (lineaAct == FIN_METODO) == False:
        #Si alguna linea en el medio es distitna a "", el programa es invalido
        if not lineaAct == "":
            return False
        
        #Se actualiza la linea actual
        lineaAct = programa.readline().strip()
    
    #Como se llego a CORP, se actualiza la cantidad de instancias revisadas
    global cantidadCorp
    cantidadCorp = cantidadCorp + 1

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
        

        #Si la linea actual es un parentesis que abre un bloque de instrucciones, se hace su revision respectiva
        if lineaAct == "{":

            #Se hace el procesamiento de un bloque de instrucciones, y como no es apartir de un PROC, no hay listas de parametros
            #Si el bloque de instrucciones no es valido, el programa no es valido
            if not procesarBloqueInstrucciones(archivo, []):
                return False


    print(archivo.readline().strip())

    return valido

#Realizacion del proyecto para parsear el programa que se quiere validar
print(revisarArchivo(programaARevisar))




