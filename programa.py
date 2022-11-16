##
#
# FILE: programa.py
# AUTHOR: Rubén García de la Fuente
# DATE: 11/11/2022
#
# BRIEF: Programa que recibe como argumento una matriz generadora G de un código C subespacio de
#   Fp^n (junto con la p y la n), y una lista de palabras recibidas en dicho código y realiza la
#   decodificación por síndrome de la misma.
#
##

##################################################################################################
##                                                                                              ##
##                                       FUNCIÓN PRINCIPAL                                      ##
##                                                                                              ##
##################################################################################################

##
#
# FUNCTION: syndromeDecoding
#
# DESCRIPTION: Función que recibe como argumento la matriz generadora G de un código C subespacio
#   de Fp^n (junto con la p y la n), y una lista de palabras recibidas en dicho código y realiza
#   la decodificación por síndrome de la misma.
# 
# PARAM: G -> Matriz generadora del código C
# PARAM: p -> Primo representativo del cuerpo Fp del código C
# PARAM: n -> Número de elementos de Fp en las palabras del código
# PARAM: w -> Lista de palabras recibidas del código C
# RETURN: H -> Matriz de paridad H del código C
#         d -> Distancia del código C
#         s -> Tabla completa de síndromes
#         dw -> (decoded words), palabras recibidas corregidas
#
##
def syndromeDecoding(G, p, n, w):

    # Comprobamos que p sea un número primo
    if p <= 1:
        print("ERROR: El número p ha de ser un número primo")
        return

    for num in range(2, int(p**0.5)+1):
        if p%num == 0:
            print("ERROR: El número p ha de ser un número primo")
            return
    
    # Comprobamos que G sea una matriz del cuerpo Fp^n
    for row in G:
        if len(row) != n:
            print("ERROR: El tamaño de las filas ha de coincidir con el cuerpo Fp^n")
            return
    
    # Comprobamos que las palabras w recibidas están en Fp^n
    for word in w:
        if len(word) != n:
            print("ERROR: El tamaño de las palabras ha de coincidir con el cuerpo Fp^n")
            return
    
    # Sacamos la matriz H
    H = matrixH(G, p)

    # Sacamos la distancia d
    d = distanceC(H, p)

    # Sacamos la tabla de síndromes
    s = syndromeTable(H, p)

    # Decodificamos las palabras
    dw = wordDecoding(w, H, s, p)

    return H, d, s, dw


##################################################################################################
##                                                                                              ##
##                                     FUNCIONES AUXILIARES                                     ##
##                                                                                              ##
##################################################################################################

##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##
##                                                                                              ##
##                                     CÁLCULO DE MATRIZ H                                      ##
##                                                                                              ##
##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##

##
#
# FUNCTION: matrixGre
#
# DESCRIPTION: Función que recibe como argumento una matriz G y devuelve la misma en forma
#   escalonada reducida
# 
# PARAM: G -> Matriz mxn
# PARAM: p -> Primo representativo del cuerpo Fp del código C
# RETURN: Ger -> (G row echelon) Matriz G en forma escalonada reducida
#
##
def matrixGre(G, p):

    m = len(G)
    n = len(G[0])

    Gre = [G[row].copy() for row in range(m)]

    # Matriz escalonada reducida
    lider = 0   # Representa el líder de cada fila
    # Realizamos un bucle por cada fila de G (que corresponderá a cada líder de fila)
    for row in range(m):
        # Si el líder es mayor o igual que el número de elementos de cada fila de G, salimos del
        # bucle
        if n <= lider:
            break
        i = row
        # Para cada fila, buscamos el líder por columna de arriba a abajo (a partir de la fila en
        # la que estamos), y por fila de dercha a izquierda, será el primer elemento distinto de 0
        while Gre[i][lider] == 0:
            i += 1
            # Si m es igual a i pasamos a la siguiente columna desde la fila en la que estamos
            if m == i:
                i = row
                lider += 1
                # Si el líder es igual al número de elementos de cada fila de G, salimos del bucle
                if n == lider:
                    break
        # Si el líder es igual al número de elementos de cada fila de G, salimos del bucle
        if n == lider:
            break
        # Si la fila en la que hemos encontrado el líder no es la fila en la que estamos
        # actualmente, intercambiamos ambas filas
        if i != row:
            Gre[i], Gre[row] = Gre[row], Gre[i]
        li = Gre[row][lider]    # li es el líder (número) de la fila en la que estamos
        invli = pow(li, -1, p)  # invli es el inverso multiplicativo del líder módulo p
        # Normalizamos la fila en la que estamos (hacemos que el líder sea 1)
        for a in range(n):
            Gre[row][a] *= invli
            Gre[row][a] %= p
        # Realizamos un bucle por cada fila en G
        for j in range(m):
            if j != row:
                # Si no estamos en nuestra fila cogemos el número de la misma columna del líder
                num = Gre[j][lider]
                # Hacemos la diferencia de la fila en la que estamos menos la fila del líder por
                # num (para que el resto de los números de la columna del líder sean 0)
                for a in range(n):
                    Gre[j][a] -= num*Gre[row][a]
                    Gre[j][a] %= p
        # Sumamos 1 al líder (el siguiente no puede estar en la misma columna)
        lider += 1
    
    # Quitamos las filas de todo 0's
    remove = [] # Lista con los índices de las filas que vamos a eliminar
    for i in range(m):
        counter = 0 # Representa el número de elementos que son 0 en una columna dada
        for number in Gre[i]:
            # Si algún elemento es distinto de 0 salimos del for y pasamos a la siguiente fila
            if number != 0:
                break
            counter += 1
        # Si el número de elementos que son 0 coincide con n, añadimos su índice a la lista
        if counter == n:
            remove.append(i)
    
    # Para cada índice en remove, eliminamos dicha fila de la matriz
    for row in remove:
        Gre.pop(row)

    return Gre

##
#
# FUNCTION: matrixH
#
# DESCRIPTION: Función que recibe como argumento una matriz generadora G de un código C y devuelve
#   su matriz de paridad H
# 
# PARAM: G -> Matriz generadora del código C
# PARAM: p -> Primo representativo del cuerpo Fp del código C
# RETURN: H -> Matriz de paridad del código C
#
##
def matrixH(G, p):

    # Matriz escalonada reducida
    Gre = matrixGre(G, p)

    # Matriz en forma estándar Ges=Gre' (sabiendo las columnas a cambiar)
    m = len(Gre)
    n = len(Gre[0])

    swiped_columns = {} # Diccionario conteniendo las columnas a cambiar en Gre para pasar a una
                        # matriz en forma estándar

    # Hacemos un bucle por cada fila de Gre
    for i in range(m):
        lider = 0
        # Buscamos la posición del líder de una fila dada
        for number in Gre[i]:
            if number == 1:
                break
            lider += 1
        # Si el líder no esta en la posición G[i][i] para la fila i, intercambiamos las columnas
        if i != lider:
            swiped_columns[i] = lider
            for a in range(m):
                Gre[a][i], Gre[a][lider] = Gre[a][lider], Gre[a][i]

    # Matriz Ger=[I|A], sacamos A y hacemos -A^t
    At = []

    # Sacamos la menos traspuesta de la matriz A
    for j in range(n-m):
        At.append([])
        for i in range(m):
            At[j].append(-Gre[i][j+m]%p)

    # Construimos H como H=[-A^t|I]
    H=At

    m = len(H)
    n = len(H[0]) + m

    # Concatenamos la matriz identidad a continuación de -A^t
    for i in range(m):
        for j in range(m):
            if j == i:
                H[i].append(1)
            else:
                H[i].append(0)

    # Cambiamos las columnas swiped_columns para que se corresponda con la matriz de paridad de G
    for key in swiped_columns:
        for a in range(m):
            H[a][key], H[a][swiped_columns[key]] = H[a][swiped_columns[key]], H[a][key]

    return H


##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##
##                                                                                              ##
##                                     CÁLCULO DE DISTANCIA d                                   ##
##                                                                                              ##
##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##

##
#
# FUNCTION: weight
#
# DESCRIPTION: Función que recibe como argumento un vector y devuelve su peso
# 
# PARAM: lista -> Vector del que queremos calcular su peso
# RETURN: w -> peso del vector lista
#
##
def weight(lista):
    w = 0   # Indica el número de elementos distintos de 0 en lista
    for number in lista:
        if number != 0:
            w += 1
    return w

##
#
# FUNCTION: nextCombination
#
# DESCRIPTION: Función que recibe como argumento una lista con l elementos distintos de 0. La
#   función genera todas las posibles combinaciones de l elementos distintos de 0 y menores que p
#   siguiendo un orden establecido, a continuación genera todas las posibles combinacioens de l+1
#   elementos... También siguiendo un orden establecido. Dada una lista, la función devuelve la
#   siguiente combinación de elementos junto con el número de elementos distintos de 0 de la nueva
#   combinación.
# 
# PARAM: lista -> Lista conteniendo la combinación actual
# PARAM: p -> Número siguiente al máximo que cada número dentro de la combinación puede alcanzar
# RETURN: listaret -> Lista conteniendo la siguiente combinación en el orden correspondiente
#         w -> Número de elementos distintos de 0 en la combinación devuelta
#
##
def nextCombination(lista, p):

    w = weight(lista)   # Número de elementos distintos de 0 en lista

    n = len(lista)
    
    rightmost = 0    # Indica el número de elementos distitos de 0 a la derecha
    # Realizamos un bucle por cada número distinto de 0
    for m in range(w):
        # Miramos de derecha a izquierda (desde el subconjunto n-m-1)
        for i in range(n-m-1, -1, -1):
            # Miramos si es el número al que vamos a aplicar la permutación (es distinto de 0)
            if lista[i] != 0:
                # Miramos si el número está al final del todo (de nuestro subconjunto)
                if i != n-m-1:
                    if rightmost == 0:
                        # Si rightmost es 0 podemos hacer 2 cosas:
                        # Si el elemento es distinto de p-1 sumamos 1
                        if lista[i] != p-1:
                            lista[i] += 1
                        # Si no, avanzamos una posición reseteando el número
                        else:
                            lista[i] = 1
                            lista[i], lista[i+1] = lista[i+1], lista[i]
                    else:
                        if lista[i] != p-1:
                            # Si rightmost no es 0 pero nuestro elemento es distinto de p-1 sumamos
                            # 1
                            lista[i] += 1
                            # Ahora reestablecemos los números que están a la derecha del todo a
                            # su posición original a la izquierda
                            for l in range(rightmost):
                                lista[i+1+l], lista[n-rightmost+l] = lista[n-rightmost+l], lista[i+1+l]
                                lista[i+1+l] = 1
                        else:
                            # Si rightmost no es 0 y nuestro elementos es p-1, avanzamos una
                            # posición a ese número y lo reestablecemos a 1
                            lista[i] = 1
                            lista[i], lista[i+1] = lista[i+1], lista[i]
                            # Ahora reestablecemos los números que están a la derecha del todo a
                            # su posición original a la izquierda más 1
                            for l in range(rightmost):
                                lista[i+2+l], lista[n-rightmost+l] = lista[n-rightmost+l], lista[i+2+l]
                                lista[i+2+l] = 1
                    return lista, w
                else:
                    # Si está al final del todo pero es distinto de p-1 sumamos 1
                    if lista[i] != p-1:
                        lista[i] += 1
                        return lista, w
                    # Si está al final del todo sumamos 1 a rightmost (número a la izquierda) y
                    # salimos del bucle
                    rightmost += 1
                    break
    
    # Si rightmost es igual al tamaño del vector, hemos terminado
    if rightmost == n:
        return None, w

    # Si rightmost es igual al número de variables añadimos un nuevo número
    if rightmost == w:
        listaret = []
        for _ in range(rightmost+1):
            listaret.append(1)
        for _ in range(n-rightmost-1):
            listaret.append(0)
        return listaret, w+1
    
    return lista, w

##
#
# FUNCTION: distanceC
#
# DESCRIPTION: Función que recibe como argumento la matriz de paridad de un código C y devuelve su
#   distancia
# 
# PARAM: H -> Matriz de paridad del código C
# PARAM: p -> Primo representativo del cuerpo Fp del código C
# RETURN: d -> Distancia del código C
#
##
def distanceC(H, p):

    m = len(H)
    n = len(H[0])

    d = m + 1

    # Creamos la primera combinación de columnas para comprobar si son linealmente dependientes
    lista = [1,1]
    for _ in range(2,n):
        lista.append(0)
    
    nlista = 2

    # Comprobamos si la distancia es 1 (ver si hay alguna columna 0 en H)
    for j in range(n):
        if H[0][j]%p == 0:
            zerocol = 1
            for i in range(1, m):
                if H[i][j]%p == 0:
                    zerocol += 1
                else:
                    break
            if zerocol == m:
                d = 1
                break

    # Comprobamos si la distancia es 2 o más
    if d != 1:
        # Hacemos un bucle mientras el número de combinaciones de columnas que miramos sea menor o
        # igual que m (número de filas)
        while nlista < m+1:
            nceros = 0
            # Hacemos un bucle para comprobar si la combinación actual de columnas es linealmente
            # dependiente
            for i in range(m):
                sum = 0
                for j in range(n):
                    if lista[j] != 0:
                        sum += lista[j]*H[i][j]
                # Si la combinación lineal de los elementos módulo p es 0, sumamos un 0 a nceros
                if sum%p == 0:
                    nceros += 1
            
            # Si nceros coincide con el número de filas de la matriz H implica que la combinación
            # de columnas escogida es linealmente dependiente, por lo tanto el número de columnas
            # de la combinación es la distancia del código (pues es el mínimo número de columnas
            # al haber ido de menos a más). Igualamos a d y salimos del bucle
            if nceros == m:
                d = nlista
                break

            # Pasamos a la siguiente cobinación de columnas
            lista, nlista = nextCombination(lista, p)
    
    return d


##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##
##                                                                                              ##
##                               CÁLCULO DE TABLA DE SÍNDROMES                                  ##
##                                                                                              ##
##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##

##
#
# FUNCTION: syndromeTable
#
# DESCRIPTION: Función que recibe como argumento la matriz de paridad de un código C y devuelve su
#   tabla de síndromes
# 
# PARAM: H -> Matriz de paridad del código C
# PARAM: p -> Primo representativo del cuerpo Fp del código C
# RETURN: syndromes -> Tabla de síndromes del código C
#
##
def syndromeTable(H, p):
    
    m = len(H)
    n = len(H[0])

    syndromes = {}

    # Creamos el primer líder de clase
    lider = []
    for _ in range(n):
        lider.append(0)
    

    flag, nkey, w, oldw = 0, 0, 0, 0
    # Mientras flag sea 0, es decir, mientras no hayamos encontrado todos los síndromes o no
    # hayamos acabado con todos los líderes de peso x (es decir w == oldw)
    while flag == 0 or w == oldw:
        syndrome = []
        # Multiplicamos la combinación por la matriz de paridad (sacamos el síndrome)
        for i in range(m):
            sum = 0
            for j in range(n):
                sum += lider[j]*H[i][j]
            syndrome.append(sum%p)
        
        key = tuple(syndrome)

        # Si el síndrome no está en la tabla de síndromes lo añadimos
        if key not in syndromes:
            syndromes[key] = [lider.copy()]
            # Sumamos 1 a nkey (número de síndromes)
            nkey += 1
            # Si nkey es igual al número de posibles síndromes, hemos acabado y ponemos flag a 1.
            # Solo queda terminar con el resto de combinaciones del mismo peso para comprobar si
            # alguna combinación es líder de clase
            if nkey == p**m:
                flag = 1
        
        # Si el síndrome ya está en la tabla de síndromes, comprobamos si la combinación es líder
        # de clase (mirando que su peso sea menor o igual que la última combinación añadida)
        else:
            if w <= weight(syndromes[key][-1]):
                syndromes[key].append(lider.copy())
        
        # Guardamos oldweight para comprobar si hemos acabado con los líderes de peso x (en cuyo
        # caso salimos del bucle)
        oldw = w
        # Pasamos a la siguiente combinación
        lider, w = nextCombination(lider, p)

    return syndromes


##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##
##                                                                                              ##
##                                DECODIFICACIÓN DE PALABRAS                                    ##
##                                                                                              ##
##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##

##
#
# FUNCTION: wordDecoding
#
# DESCRIPTION: Función que recibe como argumento una palabra y la tabla de síndromes de un código C
#   y devuelve la palabra decodificada
# 
# PARAM: w -> Lista de palabras a decodificar
# PARAM: H -> Matriz de paridad del código C
# PARAM: syndromes -> Tabla de síndromes del código C
# PARAM: p -> Primo representativo del cuerpo Fp del código C
# RETURN: dw -> Lista de palabras decodificadas
#
##
def wordDecoding(w, H, syndromes, p):

    dw = []

    m = len(H)
    n = len(H[0])

    # Para cada palabra w
    for word in w:
        dw.append([])
        syndrome = []

        # Calculamos el síndrome de la palabra
        for i in range(m):
            sum = 0
            for j in range(n):
                sum += word[j]*H[i][j]
            syndrome.append(sum%p)
        
        syndrome = tuple(syndrome)

        # Sacamos los líderes de clase del síndrome
        listerror = syndromes[syndrome]

        # Si únicamente hay un líder de clase, añadimos a dw la palabra decodificada
        if len(listerror) == 1:
            for e1, e2 in zip(word, listerror[0]):
                dw[-1].append((e1-e2)%p)
        
        # Si hay más de un líder de clase, añadimos a dw todas las posibles palabras decodificadas
        else:
            for error in listerror:
                dw[-1].append([])
                for e1, e2 in zip(word, error):
                    dw[-1][-1].append((e1-e2)%p)
    
    return dw


##################################################################################################
##                                                                                              ##
##                                 FUNCIONES DE COMPROBACIÓN                                    ##
##                                                                                              ##
##################################################################################################

##
#
# FUNCTION: isParityMatrix
#
# DESCRIPTION: Matriz que recibe una matriz generadora G de un código C y su matriz de paridad H y
#   comprueba si es correcta
# 
# PARAM: G -> Matriz generadora del código C
# PARAM: H -> Matriz de paridad del código C
# PARAM: p -> Primo representativo del cuerpo Fp del código C
# RETURN: True si H es la matriz de paridad de G. False si no lo es
#
##
def isParityMatrix(G, H, p):
    
    m = len(G)
    n = len(G[0])

    sumtotal = 0

    for Grow in range(m):
        for Hrow in range(len(H)):
            # Para cada fila de G y para cada fila de H multiplicamos sus elementos
            sum = 0
            for j in range(n):
                # Realizamos la suma de la mutliplicación de la fila de G por la de H
                sum += G[Grow][j]*H[Hrow][j]
            # Si la suma módulo p no es cero devolvemos False
            if sum%p != 0:
                return False
            # Sumamos sum a sumtotal
            sumtotal += sum
    
    # Si la suma total (sumtotal) módulo p es cero devolvemos False
    if sumtotal%p == 0:
        return True