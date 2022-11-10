def main():

    G = [[1,2,0,2,1,0],[2,0,1,2,0,1],[1,1,1,2,1,2]]

    #!!MUY IMPORTANTE
    q = 3

    # Matriz escalonada reducida

    m = len(G)
    n = len(G[0])

    Gre = [G[row].copy() for row in range(m)]

    # Matriz escalonada reducida
    lider = 0
    for row in range(m):
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
        invli = pow(li, -1, q)
        for a in range(n):
            Gre[row][a] *= invli
            Gre[row][a] %= q
        for j in range(m):
            if j != row:
                num = Gre[j][lider]
                for a in range(n):
                    Gre[j][a] -= num*Gre[row][a]
                    Gre[j][a] %= q
        lider += 1
    
    # Quitamos las filas de todo 0's
    remove = []
    for i in range(m):
        counter = 0
        for number in Gre[i]:
            if number != 0:
                break
            counter += 1
        if counter == n:
            remove.append(i)
    
    for row in remove:
        Gre.pop(row)


    print("G = " + str(G))
    print("Ger = " + str(Gre))

    # Matriz en forma estándar Ges=Ger' (sabiendo las columnas a cambiar)
    
    m = len(Gre)
    n = len(Gre[0])

    swiped_columns = {}

    for i in range(m):
        lider = 0
        for number in Gre[i]:
            if number == 1:
                break
            lider += 1
        if i != lider:
            swiped_columns[i] = lider
            for a in range(m):
                Gre[a][i], Gre[a][lider] = Gre[a][lider], Gre[a][i]

    print("Ges = " + str(Gre))
    print(swiped_columns)

    # Matriz Ger=[I|A], sacamos A y hacemos -A^t

    At = []

    for j in range(n-m):
        At.append([])
        for i in range(m):
            At[j].append(-Gre[i][j+m]%q)

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
    
    print("H' = " + str(H))

    # Cambiamos las columnas swiped_columns

    for key in swiped_columns:
        for a in range(m):
            H[a][key], H[a][swiped_columns[key]] = H[a][swiped_columns[key]], H[a][key]

    print("H = " + str(H))

    # Veamos si la matriz H está bien

    m = len(G)
    n = len(G[0])

    sumtotal = 0

    for Grow in range(m):
        for Hrow in range(len(H)):
            sum = 0
            for j in range(n):
                sum += G[Grow][j]*H[Hrow][j]
            if sum%q != 0:
                print("NO ESTÁ BIEN!!! :(")
            sumtotal += sum
    
    if sumtotal%q == 0:
        print("ESTÁ BIEN!!! :)")
    

    # Sacamos la distancia del codigo C

    m = len(H)
    n = len(H[0])

    d = m + 1

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
                if sum%q == 0:
                    nceros += 1
            
            if nceros == m:
                d = nlista
                break

            lista, nlista = nextCombination(lista, q)

    print("La distancia del código d es " + str(d))

    # Sacamos la tabla de síndromes
    tabla = {}
    
    lider = []
    for _ in range(n):
        lider.append(0)
    
    flag = 0
    nkey = 0
    peso, oldpeso = 0, 0
    while peso == oldpeso or flag == 0:

        sindrome = []
        for i in range(m):
            sum = 0
            for j in range(n):
                sum += lider[j]*H[i][j]
            sum %= q
            sindrome.append(sum)
        
        key = tuple(sindrome)

        # Si el síndrome no está en la tabla, lo añadimos
        if key not in tabla:
            tabla[key] = [lider.copy()]
            nkey += 1
            if nkey == q**m:
                flag = 1
        
        # Si el síndrome está en la tabla
        else:
            if peso <= weight(tabla[key][-1]):
                tabla[key].append(lider.copy())
        
        oldpeso = peso
        lider, peso = nextCombination(lider, q)
    
    print("La tabla de síndromes es " + str(tabla))



    return


def weight(lista):
    x = 0  # Indica el número de elementos distintos de 0 en lista
    for number in lista:
        if number != 0:
            x += 1
    return x


def nextCombination(lista, q):

    x = weight(lista)

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


if __name__ == "__main__":
    main()