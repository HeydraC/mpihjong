# mpihjong
Evaluación del puntaje de mahjongs mediante algoritmos distribuidos

Se ejecuta de forma:

**mpirun -n <número de procesos> python mahjong.py <nombre del archivo>**

Ejm:

**mpirun -n 4 python mahjong.py manos_maestro.txt**

Los grupos de 2, 3 o 4 elementos se guardan como la clase **musketeer** de forma:
        self.Id = Id #Número menor en chows, número que se repite en los demás (Para honores mayores es 0)
        self.suit = suit #Bolas, chinos, palos, vientos, etc. (Para honores mayores es lo que sale en la entrada (E, GV,...))
        self.variety = variety #Tipo de grupo (chow, pung, kung, ojo)
        self.closed = closed #Abierto o cerrado

También se usó **musketeer** para almacenar flores en **flowers**, no sé si eso vaya a ser útil.

Ahora mismo sólo está implementada la evaluación de mahjongs tradicionales.

En el repositorio están los archivos de prueba **manos_maestro.txt** con los casos que puso el profe en el campus (**soluciones_maestro.txt**) y **sample.txt** con el caso de prueba del enunciado del proyecto.

**No sé pq, pero los ojos no valen puntos en los ejemplos que puso el profe así que lo implementé así**

## MPI
Se dividen los bytes del archivo entre los procesos a ejecutar, cada proceso lee líneas del archivo hasta pasarse de su número de bytes.

El proceso 0 toma el instante de inicio y de fin y reporta el tiempo de ejecución.

Todos los procesos evalúan su pedazo de archivo y agregan los resultados a la lista **results**, el proceso 0 recopila las listas de todos los demás para imprimirlas.
