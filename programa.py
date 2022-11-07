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

##################################################################
##                                                              ##
##                       FUNCIÓN PRINCIPAL                      ##
##                                                              ##
##################################################################

##
#
# FUNCTION:
#
# DESCRIPTION:
# 
# PARAM: n
# PARAM: q
# PARAM: G
# PARAM: w
# RETURN:
#
##
def syndromeDecoding(n, q, G, w):

    # G es una matriz mxn

    m = len(G)

    # Comprobamos que q sea un número primo
    for num in range(2, int(q^0.5)+1):
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


##################################################################
##                                                              ##
##                     FUNCIONES AUXILIARES                     ##
##                                                              ##
##################################################################

##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##
##                                                              ##
##                     CÁLCULO DE MATRIZ H                      ##
##                                                              ##
##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##

# TODO: Por ahora la función no realiza escalonamientos de cuerpos finitos
##
#
# FUNCTION:
#
# DESCRIPTION:
# 
# PARAM: G
# RETURN:
#
##
def matrixGre(G):

    m = len(G)
    n = len(G[0])

    Ger = [G[row].copy() for row in range(m)]

    # Matriz escalonada reducida
    lider = 0
    for r in range(m):
        if n <= lider:
            break
        i = r
        while Ger[i][lider] == 0:
            i += 1
            if m == i:
                i = r
                lider += 1
                if n == lider:
                    break
        if n == lider:
            break
        if i != r:
            Ger[i], Ger[r] = Ger[r], Ger[i]
        li = Ger[r][lider]
        for a in range(n):
            Ger[r][a] /= li
        for j in range(m):
            if j != r:
                li = Ger[j][lider]
                for a in range(n):
                    Ger[j][a] -= li*Ger[r][a]
        lider += 1
    
    # Quitamos las columnas de todo 0
    remove = []
    for i in range(m):
        counter = 0
        for number in Ger[i]:
            if number != 0:
                break
            counter += 1
        if counter == n:
            remove.append(i)
    
    for row in remove:
        Ger.pop(row)

    return Ger

# TODO: Por ahora la función no calcula matriz H de cuerpos finitos
##
#
# FUNCTION:
#
# DESCRIPTION:
# 
# PARAM: G
# RETURN:
#
##
def matrixH(G):

    # Matriz escalonada reducida
    Ger = matrixGre(G)

    # Matriz en forma estándar Ges=Ger' (sabiendo las columnas a cambiar)
    m = len(Ger)
    n = len(Ger[0])

    swiped_columns = {}

    for i in range(m):
        lider = 0
        for number in Ger[i]:
            if number == 1:
                break
            lider = lider + 1
        if i != lider:
            swiped_columns[i] = lider
            for a in range(m):
                Ger[a][i], Ger[a][lider] = Ger[a][lider], Ger[a][i]

    # Matriz Ger=[I|A], sacamos A y hacemos -A^t
    At = []

    for j in range(n-m):
        At.append([])
        for i in range(m):
            At[j].append(-Ger[i][j+m]%2)

    # Construimos H como H=[-A^t|I]
    H=At

    m = len(H)
    n = len(H[0]) + m

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


##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##
##                                                              ##
##                     CÁLCULO DE DISTANCIA d                   ##
##                                                              ##
##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##

##
#
# FUNCTION:
#
# DESCRIPTION:
# 
# PARAM: H
# RETURN:
#
##
def nextCombination(q, lista):

    x = 0
    for number in lista:
        if number != 0:
            x += 1

    n = len(lista)
    
    leftmost = 0 # Indica el numero de números distitos de 0 a la izquierda
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
                            # Si leftmost no es 0 pero nuestro elemento es distinto de q-1 sumamos 1
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
                    # Si está al final del todo sumamos 1 a leftmost (número a la izquierda) y salimos del bucle
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
    
    return lista

##
#
# FUNCTION:
#
# DESCRIPTION:
# 
# PARAM: H
# RETURN:
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
        if H[0][j] == 0%q:
            zerocol = 1
            for i in range(m):
                if H[i][j] == 0%q:
                    zerocol += 1
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


##################################################################
##                                                              ##
##                 FUNCIONES DE COMPROBACIÓN                    ##
##                                                              ##
##################################################################

##
#
# FUNCTION:
#
# DESCRIPTION:
# 
# PARAM: q
# PARAM: G
# PARAM: H
# RETURN:
#
##
def areCorrect(q, G, H):
    
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