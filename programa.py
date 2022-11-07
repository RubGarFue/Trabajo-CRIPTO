'''Si quieres hacer algo de códigos, puedes intentar implementar la decodificación por síndrome.

I.  Entrada:

1. una matriz generadora G 
 2. varias palabras (w_1,\ldots, w_k)

Salida: 

1. matriz de paridad H
2. la distancia del código d
3. la tabla de síndrome incompleta (que corrige d-1/2 errores)
4. Decodificación de las palabras (w_1,\ldots, w_k) '''

def decodificacionSindromeBinario(n, G, w):

    # G es una matriz mxn

    m = len(G)

    for row in G:
        if len(row) != n:
            print("ERROR: El tamaño de las filas ha de coincidir con el cuerpo F2^n")
            return
    
    for word in w:
        if len(word) != n:
            print("ERROR: El tamaño de las palabras ha de coincidir con el cuerpo F2^n")
            return
    
    # Sacamos la matriz H

    H = matrizH(G, m, n)

    return H, d, t, cw

def matrizGer(G):

    m = len(G)
    n = len(G[0])

    Ger = G.copy()

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
        if i != r:
            Ger[i], Ger[r] = Ger[r], Ger[i]
        for a in range(n):
            Ger[r][a] /= Ger[r][lider]
        for j in range(m):
            if j != r:
                for a in range(n):
                    Ger[j][a] -= Ger[j][lider]*Ger[r][a]
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

    print(G)
    print(Ger)

    return Ger

def matrizH(G):

    # Matriz escalonada reducida

    Ger = matrizGer(G)

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

    print(Ger)
    print(swiped_columns)

    # Matriz Ger=[I|A], sacamos A y hacemos -A^t

    A = []

    for i in range(m):
        A.append([])
        for j in range(n-m):
            A[i].append(Ger[i][j+m])
    
    print(A)

    for i in range(m):
        for j in range(i, m):
            A[i][j], A[j][i] = -A[j][i]%2, -A[i][j]%2

    print(A)

    # Construimos H como H=[-A^t|I]

    H=A

    for i in range(m):
        for j in range(m):
            if j == i:
                H[i].append(1)
            else:
                H[i].append(0)
    
    print(H)

    # Cambiamos las columnas swiped_columns

    for key in swiped_columns:
        for a in range(m):
            H[a][key], H[a][swiped_columns[key]] = H[a][swiped_columns[key]], H[a][key]
    
    print(H)

    return H

def distanciaC(H, m, n):

    # Sacamos la distancia del codigo C

    m = len(H)
    n = len(H[0])

    d = n

    for i in range(n):
        ld = 0
        for j in range(n):
            if i != j:
                dotp = 0
                for a in range(m):
                    dotp += H[a][i] * H[a][j]
                if dotp == 0:
                    ld += 1
        if ld != 0 and ld < d:
            d = ld
    
    print(d)