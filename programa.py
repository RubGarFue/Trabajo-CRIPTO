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
# PARAM: G -> Matriz generadora del código C
# PARAM: q -> Primo representativo del cuerpo Fq del código C
# PARAM: n -> Número de elementos de Fq en las palabras del código
# PARAM: w -> Lista de palabras recibidas del código C
# RETURN: H -> Matriz de paridad H del código C
#         d -> Distancia del código C
#         t -> Tabla incompleta de síndromes
#         dw -> (decoded words), palabras recibidas corregidas
#
##
def syndromeDecoding(G, q, n, w):

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
    H = matrixH(G, q)

    # Sacamos la distancia d
    d = distanceC(H, q)

    # Sacamos la tabla de síndromes
    t = syndromeTable(H, q)

    # Decodificamos las palabras
    dw = wordDecoding(w, q)

    return H, d, t, dw


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
# PARAM: q -> Primo representativo del cuerpo Fq del código C
# RETURN: Ger -> (G row echelon) Matriz G en forma escalonada reducida
#
##
def matrixGre(G, q):

    m = len(G)
    n = len(G[0])

    Gre = [G[row].copy() for row in range(m)]

    # Matriz escalonada reducida
    lider = 0   # Representa el líder de cada fila
    # Realizamos un bucle por cada fila de G (que corresponderá a cada líder de fila)
    for row in range(m):
        # Si el líder es mayor o igual que el número de elementos de cada fila deG, salimos del
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
        invli = pow(li, -1, q)  # invli es el inverso multiplicativo del líder módulo q
        # Normalizamos la fila en la que estamos (hacemos que el líder sea 1)
        for a in range(n):
            Gre[row][a] *= invli
            Gre[row][a] %= q
        # Realizamos un bucle por cada fila en G
        for j in range(m):
            if j != row:
                # Si no estamos en nuestra fila cogemos el número de la misma columna del líder
                num = Gre[j][lider]
                # Hacemos la diferencia de la fila en la que estamos menos la fila del líder por
                # num (para que el resto de los números de la columna del líder sean 0)
                for a in range(n):
                    Gre[j][a] -= num*Gre[row][a]
                    Gre[j][a] %= q
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
# PARAM: q -> Primo representativo del cuerpo Fq del código C
# RETURN: H -> Matriz de paridad del código C
#
##
def matrixH(G, q):

    # Matriz escalonada reducida
    Gre = matrixGre(G, q)

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
            At[j].append(-Gre[i][j+m]%q)

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
# FUNCTION: nextCombination
#
# DESCRIPTION: Función que recibe como argumento una lisita con l elementos distintos de 0. La
#   función genera todas las posibles combinaciones de l elementos distintos de 0 y menores que q
#   siguiendo un orden establecido, a continuación genera todas las posibles combinacioens de l+1
#   elementos... También siguiendo un orden establecido. Dada una lista, la función devuelve la
#   siguiente combinación de elementos junto con el número de elementos distintos de 0 de la nueva
#   combinación.
# 
# PARAM: lista -> Lista conteniendo la combinación actual
# PARAM: q -> Número siguiente al máximo que cada número dentro de la combinación puede alcanzar
# RETURN: listaret -> Lista conteniendo la siguiente combinación en el orden correspondiente
#         x -> Número de elementos distintos de 0 en la combinación devuelta
#
##
def nextCombination(lista, q):

    x = 0   # Indica el número de elementos distintos de 0 en lista
    for number in lista:
        if number != 0:
            x += 1

    n = len(lista)
    
    rightmost = 0    # Indica el número de elementos distitos de 0 a la derecha
    # Realizamos un bucle por cada número distinto de 0
    for m in range(x):
        # Miramos de derecha a izquierda (desde el subconjunto n-m-1)
        for i in range(n-m-1, -1, -1):
            # Miramos si es el número al que vamos a aplicar la permutación (es distinto de 0)
            if lista[i] != 0:
                # Miramos si el número está al final del todo (de nuestro subconjunto)
                if i != n-m-1:
                    if rightmost == 0:
                        # Si rightmost es 0 podemos hacer 2 cosas:
                        # Si el elemento es distinto de q-1 sumamos 1
                        if lista[i] != q-1:
                            lista[i] += 1
                        # Si no, avanzamos una posición reseteando el número
                        else:
                            lista[i] = 1
                            lista[i], lista[i+1] = lista[i+1], lista[i]
                    else:
                        if lista[i] != q-1:
                            # Si rightmost no es 0 pero nuestro elemento es distinto de q-1 sumamos
                            # 1
                            lista[i] += 1
                            # Ahora reestablecemos los números que están a la derecha del todo a
                            # su posición original a la izquierda
                            for l in range(rightmost):
                                lista[i+1+l], lista[n-rightmost+l] = lista[n-rightmost+l], lista[i+1+l]
                                lista[i+1+l] = 1
                        else:
                            # Si rightmost no es 0 y nuestro elementos es q-1, avanzamos una
                            # posición a ese número y lo reestablecemos a 1
                            lista[i] = 1
                            lista[i], lista[i+1] = lista[i+1], lista[i]
                            # Ahora reestablecemos los números que están a la derecha del todo a
                            # su posición original a la izquierda más 1
                            for l in range(rightmost):
                                lista[i+2+l], lista[n-rightmost+l] = lista[n-rightmost+l], lista[i+2+l]
                                lista[i+2+l] = 1
                    return lista, x
                else:
                    # Si está al final del todo pero es distinto de q-1 sumamos 1
                    if lista[i] != q-1:
                        lista[i] += 1
                        return lista, x
                    # Si está al final del todo sumamos 1 a rightmost (número a la izquierda) y
                    # salimos del bucle
                    rightmost += 1
                    break
    
    # Si rightmost es igual al tamaño del vector, hemos terminado
    if rightmost == n:
        return None, x

    # Si rightmost es igual al número de variables añadimos un nuevo número
    if rightmost == x:
        listaret = []
        for _ in range(rightmost+1):
            listaret.append(1)
        for _ in range(n-rightmost-1):
            listaret.append(0)
        return listaret, x+1
    
    return lista, x

##
#
# FUNCTION: distanceC
#
# DESCRIPTION: Función que recibe como argumento la matriz de paridad de un código C y devuelve su
#   distancia
# 
# PARAM: H -> Matriz de paridad del código C
# PARAM: q -> Primo representativo del cuerpo Fq del código C
# RETURN: d -> Distancia del código C
#
##
def distanceC(H, q):

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
                # Si la combinación lineal de los elementos módulo q es 0, sumamos un 0 a nceros
                if sum%q == 0:
                    nceros += 1
            
            # Si nceros coincide con el número de filas de la matriz H implica que la combinación
            # de columnas escogida es linealmente dependiente, por lo tanto el número de columnas
            # de la combinación es la distancia del código (pues es el mínimo número de columnas
            # al haber ido de menos a más). Igualamos a d y salimos del bucle
            if nceros == m:
                d = nlista
                break

            # Pasamos a la siguiente cobinación de columnas
            lista, nlista = nextCombination(lista, q)
    
    return d


##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##
##                                                                                              ##
##                               CÁLCULO DE TABLA DE SÍNDROMES                                  ##
##                                                                                              ##
##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##

def syndromeTable(H):
    return


##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##
##                                                                                              ##
##                                DECODIFICACIÓN DE PALABRAS                                    ##
##                                                                                              ##
##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##

def wordDecoding(w):
    return


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
# PARAM: q -> Primo representativo del cuerpo Fq del código C
# RETURN: True si H es la matriz de paridad de G. False si no lo es
#
##
def isParityMatrix(G, H, q):
    
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
            # Si la suma módulo q no es cero devolvemos False
            if sum%q != 0:
                return False
            # Sumamos sum a sumtotal
            sumtotal += sum
    
    # Si la suma total (sumtotal) módulo q es cero devolvemos False
    if sumtotal%q == 0:
        return True