##
#
# FILE: prueba.py
# AUTHOR: Rubén García de la Fuente
# DATE: 11/11/2022
#
# BRIEF: Script de prueba para la función syndromeDecoding
#
##

from programa import *

##
#
# FUNCTION: main
#
# DESCRIPTION: Función principal del script
#
##
def main():

    G = []
    q = []
    n = []
    w = []

    # Ejemplo 1 (Hoja 2 Ejercicio 1 a)
    G.append([[1,1,0,0],[0,0,1,1]])
    q.append(2)
    n.append(4)
    w.append([])
    
    # Ejemplo 2 (Hoja 2 Ejercicio 1 b)
    G.append([[0,1,1,0],[1,2,0,1],[2,0,2,2]])
    q.append(3)
    n.append(4)
    w.append([])

    # Ejemplo 3 (Hoja 2 Ejercicio 1 c)
    G.append([[1,1,0,1,0,1],[0,0,1,0,1,0],[1,1,1,0,1,1],[1,0,1,1,0,1]])
    q.append(2)
    n.append(6)
    w.append([])

    # Ejemplo 4 (Hoja 2 Ejercicio 2 a)
    G.append([[1,0,0,0,0,0,0,1,1,0,0],[0,1,0,0,0,0,0,1,0,1,0],[0,0,1,0,0,0,0,0,1,1,0],[0,0,0,1,0,0,0,1,1,1,1],[0,0,0,0,1,0,0,1,1,0,1],[0,0,0,0,0,1,0,0,1,0,1],[0,0,0,0,0,0,1,1,0,0,1]])
    q.append(2)
    n.append(11)
    w.append([])

    # Ejemplo 5 (Hoja 2 Ejercicio 2 b)
    G.append([[1,2,0,2,1,0],[2,0,1,2,0,1],[1,1,1,2,1,2]])
    q.append(3)
    n.append(6)
    w.append([])

    # Ejemplo 6 (Hoja 2 Ejercicio 2 c)
    G.append([[1,1,1,0],[2,0,1,1]])
    q.append(3)
    n.append(4)
    w.append([[2,1,2,1],[1,2,0,1],[2,2,2,2]])

    # Ejemplo 7 (Hoja 2 Ejercicio 13)
    G.append([[1,0,0,1,1,1,0],[0,1,0,1,1,0,1],[0,0,1,1,0,1,1]])
    q.append(2)
    n.append(7)
    w.append([[0,0,1,1,1,1,1],[0,1,1,0,1,1,0],[0,0,0,1,1,1,1],[1,1,1,1,0,0,0]])

    # Ejemplo 8 (Hoja 2 ejercicio 14)
    G.append([[1,0,0,2,2,0],[0,1,0,2,0,2],[0,0,1,0,2,2]])
    q.append(3)
    n.append(6)
    w.append([[0,0,0,0,0,0],[1,0,0,2,0,1],[0,2,0,1,0,1],[0,1,0,0,2,1],[0,0,1,0,2,2],[1,0,0,1,1,0]])

    # Ejemplo 9 (Ejercicio 1 Parcial Códigos 2021)
    G.append([[2,0,1,2,0,1],[2,1,0,1,2,0],[2,0,1,0,2,2]])
    q.append(3)
    n.append(6)
    w.append([[0,0,0,0,2,1],[0,2,1,1,1,1],[0,0,0,2,1,0]])

    i = 1
    for G, q, n, w in zip(G,q,n,w):
        print("*** EJEMPLO " + str(i) + " ***\n")
        
        H, d, s, dw = syndromeDecoding(G, q, n, w)

        print("G = " + str(G) + "\n")

        print("H = " + str(H) + "\n")

        if isParityMatrix(G, H, q):
            print("H es matriz de paridad\n")
        else:
            print("H no es matriz de paridad\n")

        print("La distancia del código C es " + str(d) + "\n")

        print("La tabla de síndromes es:")
        for key in s:
            print(str(key) + " : " + str(s[key]))
        print("")

        if len(w) > 0:
            print("Palabras recibidas:")
            for word in w:
                print(word)
            print("")

        if len(dw) > 0:
            print("Palabras decodificadas:")
            for dword in dw:
                print(dword)
            print("")
        
        print("\n\n")

        i += 1

    return

if __name__ == "__main__":
    main()