# Trabajo Teoría de Códigos

El trabajo consiste en la implementación de un algoritmo que realice la decodificación por síndrome. Consta de dos ficheros python, "programa.py" y "prueba.py".

El fichero "programa.py" contiene la función principal syndromeDecoding, que dado una matriz generadora G de un código C, el primo p representativo del cuerpo Fp, el tamaño n de las palabras del código y una lista w de palabras a decodificar, devuelve la matriz de paridad H, la distancia d del código C, la tabla completa de síndromes s, y una lista dw con las palabras decodificadas.
Para esto se ayuda de la utilización de una serie de funciones auxiliares (explicadas y comentadas dentro del fichero) de la que se servirá la función principal para generar el retorno.

El fichero "prueba.py" consiste en un simple script de prueba que contiene una serie de 9 ejemplos ya conocidos (a partir de ejercicios de las hojas y exámenes de años anteriores) para corroborar el correcto funcionamiento del algoritmo.