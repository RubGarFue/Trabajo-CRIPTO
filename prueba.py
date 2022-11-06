def main():

    G = [[1,0,1,1,0],[0,1,0,1,1]]

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

    print(G)
    print(Ger)

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

    At = []

    for j in range(n-m):
        At.append([])
        for i in range(m):
            At[j].append(-Ger[i][j+m]%2)

    print(At)

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
    
    print(H)

    # Cambiamos las columnas swiped_columns

    for key in swiped_columns:
        for a in range(m):
            H[a][key], H[a][swiped_columns[key]] = H[a][swiped_columns[key]], H[a][key]
    
    print(H)

    # Veamos si la matriz H está bien

    m = len(G)
    n = len(G[0])

    sumtotal = 0

    for Grow in range(m):
        for Hrow in range(len(H)):
            sum = 0
            for j in range(n):
                sum += G[Grow][j]*H[Hrow][j]
            if sum%2 != 0:
                print("NO ESTÁ BIEN :(\n")
            sumtotal += sum
    
    if sumtotal%2 == 0:
        print("ESTÁ BIEN!!! :)")
    

    # Sacamos la distancia del codigo C
    # ARREGLAR!!!

    m = len(H)
    n = len(H[0])

    d = m + 1
    q = 2   # Fq

    for i in range(m+1):
        ld = 0
        for column in range(n):

            for set in range(i):

    
    print(d)


if __name__ == "__main__":
    main()