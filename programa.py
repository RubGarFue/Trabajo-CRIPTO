##
#
# FILE:
# AUTHOR:
# DATE:
#
# BRIEF:
#
##

'''Si quieres hacer algo de códigos, puedes intentar implementar la decodificación por síndrome.

I.  Entrada:

1. una matriz generadora G 
 2. varias palabras (w_1,\ldots, w_k)

Salida: 

1. matriz de paridad H
2. la distancia del código d
3. la tabla de síndrome incompleta (que corrige d-1/2 errores)
4. Decodificación de las palabras (w_1,\ldots, w_k) '''

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
#   de Fq^n (junto con la q y la n), y una lista de palabras recibidas en dicho código y realiza
#   la decodificación por síndrome de la misma.
# 
# PARAM: n -> Número de elementos de Fq en las palabras del código
# PARAM: q -> Primo representativo del cuerpo Fq del código
# PARAM: G -> Matriz generadora del código C
# PARAM: w -> Lista de palabras recibidas del código C
# RETURN: H -> Matriz de paridad H del código C
#         d -> Distancia del código C
#         t -> Tabla incompleta de síndromes
#         cw -> (corrected words), palabras recibidas corregidas
#
##
def syndromeDecoding(n, q, G, w):

    # G es una matriz mxn

    m = len(G)

    # Comprobamos que q sea un número primo
    if q <= 1:
        print("ERROR: El número q ha de ser un número primo")
        return

    for num in range(2, int(q**0.5)+1):
        if q%num == 0:
            print("ERROR: El número q ha de ser un número primo")
            return
    
    # Comprobamos que G sea una matriz del cuerpo Fq^n
    for row in G:
        if len(row) != n:
            print("ERROR: El tamaño de las filas ha de coincidir con el cuerpo Fq^n")
            return
    
    # Comprobamos que las palabras w recibidas están en Fq^n
    for word in w:
        if len(word) != n:
            print("ERROR: El tamaño de las palabras ha de coincidir con el cuerpo Fq^n")
            return
    
    # Sacamos la matriz H
    H = matrixH(G)

    # Sacamos la distancia d
    d = distanceC(H)

    return H, d, t, cw


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

# TODO: Por ahora la función no realiza escalonamientos de cuerpos finitos
##
#
# FUNCTION: matrixGre
#
# DESCRIPTION: Función que recibe como argumento una matriz G y devuelve la misma en forma
#   escalonada reducida
# 
# PARAM: G -> Matriz mxn
# RETURN: Ger -> (G row echelon) Matriz G en forma escalonada reducida
#
##
def matrixGre(G):

    m = len(G)
    n = len(G[0])

    Gre = [G[row].copy() for row in range(m)]

    # Matriz escalonada reducida
    lider = 0 # Representa el líder de cada fila
    # Realizamos un bucle por cada fila de G
    for row in range(m):
        # Si el líder es mayor que el número de elementos de G, significa que la fila es todo 0's
        # y pasamos a la siguiente fila
        if n <= lider:
            break
        i = row
        while Gre[i][lider] == 0:
            i += 1
            if m == i:
                i = row
                lider += 1
                if n == lider:
                    break
        if n == lider:
            break
        if i != row:
            Gre[i], Gre[row] = Gre[row], Gre[i]
        li = Gre[row][lider]
        for a in range(n):
            # TODO: Aquí hay que definir el inverso multiplicativo, no dividir!!!
            # TODO: Hay que poner un int(---) delante de la división para que los numeros que aparecen en H sean int
            Gre[row][a] /= li
        for j in range(m):
            if j != row:
                li = Gre[j][lider]
                for a in range(n):
                    Gre[j][a] -= li*Gre[row][a]
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

# TODO: Por ahora la función no calcula matriz H de cuerpos finitos
##
#
# FUNCTION: matrixH
#
# DESCRIPTION: Función que recibe como argumento una matriz generadora G de un código C y devuelve
#   su matriz de paridad H
# 
# PARAM: G -> Matriz generadora del código C
# RETURN: H -> Matriz de paridad del código C
#
##
def matrixH(G):

    # Matriz escalonada reducida
    Gre = matrixGre(G)

    # Matriz en forma estándar Ges=Gre' (sabiendo las columnas a cambiar)
    m = len(Gre)
    n = len(Gre[0])

    swiped_columns = {}

    for i in range(m):
        lider = 0
        for number in Gre[i]:
            if number == 1:
                break
            lider = lider + 1
        if i != lider:
            swiped_columns[i] = lider
            for a in range(m):
                Gre[a][i], Gre[a][lider] = Gre[a][lider], Gre[a][i]

    # Matriz Ger=[I|A], sacamos A y hacemos -A^t
    At = []

    for j in range(n-m):
        At.append([])
        for i in range(m):
            At[j].append(-Gre[i][j+m]%2)

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

    # Cambiamos las columnas swiped_columns
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
# FUNCTION: nextCombination
#
# DESCRIPTION: Función que recibe como argumento una lisita con l elementos distintos de 0. La
#   función genera todas las posibles combinaciones de l elementos distintos de 0 y menores que q
#   siguiendo un orden establecido, a continuación genera todas las posibles combinacioens de l+1
#   elementos... También siguiendo un orden establecido. Dada una lista, la función devuelve la
#   siguiente combinación de elementos junto con el número de elementos distintos de 0 de la nueva
#   combinación.
# 
# PARAM: q -> Número siguiente al máximo que cada número dentro de la combinación puede alcanzar
# PARAM: lista -> Lista conteniendo la combinación actual
# RETURN: listaret -> Lista conteniendo la siguiente combinación en el orden correspondiente
#         x -> Número de elementos distintos de 0 en la combinación devuelta
#
##
def nextCombination(q, lista):

    x = 0   # Indica el número de elementos distintos de 0 en lista
    for number in lista:
        if number != 0:
            x += 1

    n = len(lista)
    
    leftmost = 0    # Indica el número de elementos distitos de 0 a la izquierda
    # Realizamos un bucle por cada número distinto de 0
    for m in range(x):
        # Miramos de derecha a izquierda (desde el subconjunto n-m-1)
        for i in range(n-m-1, -1, -1):
            # Miramos si es el número al que vamos a aplicar la permutación (es distinto de 0)
            if lista[i] != 0:
                # Miramos si el número está al final del todo (de nuestro subconjunto)
                if i != n-m-1:
                    if leftmost == 0:
                        # Si leftmost es 0 podemos hacer 2 cosas:
                        # Si el elemento es distinto de q-1 sumamos 1
                        if lista[i] != q-1:
                            lista[i] += 1
                        # Si no, avanzamos una posición reseteando el número
                        else:
                            lista[i] = 1
                            lista[i], lista[i+1] = lista[i+1], lista[i]
                    else:
                        if lista[i] != q-1:
                            # Si leftmost no es 0 pero nuestro elemento es distinto de q-1 sumamos
                            # 1
                            lista[i] += 1
                            # Ahora reestablecemos los 
                            for l in range(leftmost):
                                lista[i+1+l], lista[n-leftmost+l] = lista[n-leftmost+l], lista[i+1+l]
                                lista[i+1+l] = 1
                        else:
                            lista[i] = 1
                            lista[i], lista[i+1] = lista[i+1], lista[i]
                            for l in range(leftmost):
                                lista[i+2+l], lista[n-leftmost+l] = lista[n-leftmost+l], lista[i+2+l]
                                lista[i+2+l] = 1
                    return lista, x
                else:
                    # Si está al final del todo pero es distinto de q-1 sumamos 1
                    if lista[i] != q-1:
                        lista[i] += 1
                        return lista, x
                    # Si está al final del todo sumamos 1 a leftmost (número a la izquierda) y
                    # salimos del bucle
                    leftmost += 1
                    break
    
    # Si leftmost es igual al tamaño del vector, hemos terminado
    if leftmost == n:
        return None, x

    # Si leftmost es igual al número de variables añadimos un nuevo número
    if leftmost == x:
        listaret = []
        for _ in range(leftmost+1):
            listaret.append(1)
        for _ in range(n-leftmost-1):
            listaret.append(0)
        return listaret, x
    
    return lista, x

##
#
# FUNCTION: distanceC
#
# DESCRIPTION: Función que recibe como argumento la matriz de paridad de un código C y devuelve su
#   distancia
# 
# PARAM: H -> Matriz de paridad del código C
# RETURN: d -> Distancia del código C
#
##
def distanceC(H):

    m = len(H)
    n = len(H[0])

    d = m + 1
    q = 2

    lista = [1,1]
    for _ in range(2,n):
        lista.append(0)
    
    nlista = 2

    # Comprobamos si la distancai es 1 (ver si hay alguna columna 0 en H)
    for j in range(n):
        if H[0][j]%q == 0:
            zerocol = 1
            for i in range(1, m):
                if H[i][j]%q == 0:
                    zerocol += 1
                else:
                    break
            if zerocol == m:
                d = 1
                break

    # Comprobamos si la distancia es 2 o más
    if d != 1:
        while nlista < m+1:
            nceros = 0
            for i in range(m):
                sum = 0
                for j in range(n):
                    if lista[j] != 0:
                        sum += lista[j]*H[i][j]
                if sum%2 == 0:
                    nceros += 1
            
            if nceros == m:
                d = nlista
                break

            lista, nlista = nextCombination(q, lista)
    
    return d


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
# PARAM: q -> Primo representativo del cuerpo Fq del código
# PARAM: G -> Matriz generadora del código C
# PARAM: H -> Matriz de paridad del código C
# RETURN: True si H es la matriz de paridad de G. False si no lo es
#
##
def isParityMatrix(q, G, H):
    
    m = len(G)
    n = len(G[0])

    sumtotal = 0

    for Grow in range(m):
        for Hrow in range(len(H)):
            sum = 0
            for j in range(n):
                sum += G[Grow][j]*H[Hrow][j]
            if sum%q != 0:
                return False
            sumtotal += sum
    
    if sumtotal%q == 0:
        return True