# mpihjong
Evaluación del puntaje de mahjongs mediante algoritmos distribuidos

Se ejecuta de forma
**mpirun -n <número de procesos> python mahjong.py <nombre del archivo>**
Ejm:
mpirun -n 4 python mahjong.py manos_maestro.txt

Los grupos de 2, 3 o 4 elementos se guardan como la clase musketeer

## MPI
Se dividen los bytes del archivo entre los procesos a ejecutar, cada proceso lee líneas del archivo hasta pasarse de su número de bytes.

El proceso 0 toma el instante de inicio y de fin y reporta el tiempo de ejecución.

Todos los procesos evalúan su pedazo de archivo y agregan los resultados a la lista **results**, el proceso 0 recopila las listas de todos los demás para imprimirlas.
