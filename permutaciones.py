def main():
    
    lista = [0,0,0,0]
    print(lista)
    while lista != None:
        lista = nextCombination(3, lista)
        print(lista)

    return


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
                    return lista
                else:
                    # Si está al final del todo pero es distinto de q-1 sumamos 1
                    if lista[i] != q-1:
                        lista[i] += 1
                        return lista
                    # Si está al final del todo sumamos 1 a leftmost (número a la izquierda) y salimos del bucle
                    leftmost += 1
                    break
    
    # Si leftmost es igual al tamaño del vector, hemos terminado
    if leftmost == n:
        return None

    # Si leftmost es igual al número de variables añadimos un nuevo número
    if leftmost == x:
        listaret = []
        for _ in range(leftmost+1):
            listaret.append(1)
        for _ in range(n-leftmost-1):
            listaret.append(0)
        return listaret
    
    return lista

if __name__ == "__main__":
    main()