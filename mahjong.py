#Grupos
class musketeer:
    def __init__(self, Id: int, suit: str, variety: str, closed: bool):
        self.Id = Id #Número menor en chows, número que se repite en los demás (Para honores mayores es 0)
        self.suit = suit #Bolas, chinos, palos, vientos, etc. (Para honores mayores es lo que sale en la entrada (E, DV,...))
        self.variety = variety #Tipo de grupo (chow, pung, kung, ojo)
        self.closed = closed #Abierto o cerrado
    
    #Para imprimir el objeto
    def __str__(self): 
        return f"({self.variety} {self.suit} {self.Id} {"cerrado" if self.closed else "abierto"})"
    
    def getPoints(self, p):
        action = ""
        points = 0
        if self.variety == "chow" or self.variety == "ojo":
            return points, action
        
        if self.variety == "pung":
            action += "pung "
            points = 2
        else:
            action += "kung "
            points = 8
        
        if self.closed:
            points *= 2
            action += "cerrado "
        else:
            action += "abierto "

        if self.Id == 1 or self.Id == 9 or self.Id == 0:
            points *= 2
            action += "honor "
        else:
            action += "pinta "
        
        action = f"{p + points} " + action + f"{points}"
        
        return points, action


def notWind(p):
    return p != 'E' and p != 'S' and p != 'W' and p != 'N'

def musketeers(line, i):
    if notWind(line[i][1]):
        if line[i][0] == '(':
            variety = "ojo"
        elif len(line[i]) == 13: #3 guiones + 2 corchetes + 8 letras/números
            variety = "kung"
        else:
            if line[i][2] == line[i][5]: #Las piezas tienen el mismo número
                variety = "pung"
            else:
                variety = "chow"

        if line[i][1] == 'D':
            suit = line[i][1] + line[i][2]
            Id = 0 #Honor mayor
        else:
            Id = int(line[i][2])
            suit = line[i][1]
    else:
        if line[i][0] == '(':
            variety = "ojo"
        elif len(line[i]) == 9: #3 guiones + 2 corchetes + 4 letras
            variety = "kung"
        else:
            variety = "pung"
        
        suit = line[i][1]
        
        Id = 0 #Honor mayor

    if line[i][0] == '[': #Los ojo () siempre son cerrados
        closed = False
    else:
        closed = True

    return musketeer(Id, suit, variety, closed)

from mpi4py import MPI
import itertools
import sys
import os
from datetime import datetime

winds = {1 : "E", 2 : "S", 3 : "W", 4 : "N"}

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if len(sys.argv) < 2:
    print("Error: Debe incluir nombre del archivo.")
    sys.exit(1)

if rank == 0:
    before = datetime.now()

name = sys.argv[1]

results = []

file_size = os.path.getsize(name)
chunk_size = file_size // size

start_byte = rank * chunk_size
end_byte = (rank + 1) * chunk_size if rank != size - 1 else file_size

with open(name, "rb") as file:
    file.seek(start_byte)

    if rank != 0:
        file.readline()
        start_byte = file.tell()

    while file.tell() < end_byte:
        raw_line = file.readline()
        if not raw_line:
            break 

        entry = raw_line.decode('utf-8').strip()

        allForOne = [] #Lista de grupos

        line = entry.split()

        Id = line[0]
        points = 0
        doubles = 0

        doubleActions = []

        ownWind = line[1][1]
        roundWind = line[3][0]

        chowLess = True

        ases = False
        nueves = False
        pinta = ''
        honores = False

        i = 4

        while(line[i][0] != '<'):
            allForOne.append(musketeers(line, i))
            i += 1

            if allForOne[-1].suit == ownWind:
                doubleActions.append(f"[+] 1 Doble: Pung/Kung de viento propio ({ownWind})")
                doubles += 1
            
            if allForOne[-1].variety == "chow":
                chowLess = False
                pinta = allForOne[-1].suit
                continue
            
            if allForOne[-1].Id == 0:
                if allForOne[-1].suit[0] == 'D' and allForOne[-1].variety != "ojo":
                    doubleActions.append(f"[+] 1 Doble: Pung/Kung de Dragon ({allForOne[-1].suit})")
                    doubles += 1
                    
                honores = True
                
            elif allForOne[-1].Id == 1:
                ases = True
            elif allForOne[-1].Id == 9:
                nueves = True
            else:
                pinta = allForOne[-1].suit
                
        flowers = []

        if len(line[i]) == 4:
            flowers.append(musketeer(int(line[i][2]), "flor", line[i][1], True))

            if winds[flowers[-1].Id] == ownWind:
                doubleActions.append(f"[+] 1 Doble: Flor propia detectada ({flowers[-1].variety}{flowers[-1].Id})")
                doubles += 1
        elif line[i] != "<>":
            flowers.append(musketeer(int(line[i][2]), "flor", line[i][1], True))

            blacks = 0
            reds = 0

            if flowers[-1].variety == 'G':
                blacks += 1
            else:
                reds += 1
            
            if winds[flowers[-1].Id] == ownWind:
                doubleActions.append(f"[+] 1 Doble: Flor propia detectada ({flowers[-1].variety}{flowers[-1].Id})")
                doubles += 1

            i += 1
            

            while len(line[i]) == 2:
                flowers.append(musketeer(int(line[i][1]), "flor", line[i][0], True))
                
                if flowers[-1].variety == 'G':
                    blacks += 1
                else:
                    reds += 1

                if winds[flowers[-1].Id] == ownWind:
                    doubleActions.append(f"[+] 1 Doble: Flor propia detectada ({flowers[-1].variety}{flowers[-1].Id})")
                    doubles += 1

                i += 1
            
            flowers.append(musketeer(int(line[i][1]), "flor", line[i][0], True))

            if flowers[-1].variety == 'G':
                blacks += 1
            else:
                reds += 1

            if winds[flowers[-1].Id] == ownWind:
                doubleActions.append(f"[+] 1 Doble: Flor propia detectada ({flowers[-1].variety}{flowers[-1].Id})")
                doubles += 1

            if blacks == 4:
                doubles += 3
            if reds == 4:
                doubles += 3

        lastPiece = line[-1].strip("*")

        actions = []

        for piece in allForOne:
            piecePoints, action = piece.getPoints(points)
            points += piecePoints
            if action != "":
                actions.append(action)

        if chowLess:
            points += 30
            actions.append(f"{points} mahjong sin chow 30")
        else:
            points += 20
            actions.append(f"{points} mahjong con chow 20")
        
        points += len(flowers) * 4

        actions.append(f"{points} flores: {len(flowers)} para {len(flowers)*4} puntos")

        total = points

        dig = points%10
        if dig >= 5:
            points += 10
        points = (points//10)*10

        actions.append(f"Total puntos: {total} para {points}")

        if honores and (not ases or not nueves):
            doubleActions.append("[+] 2 Dobles: MAH-JONGG SUCIO (Honores con pinta)")
            doubles += 2
        elif honores and ases and nueves:
            doubleActions.append(f"[+] 3 Dobles: MAH-JONGG LIMPIO Honores (Pinta {pinta} con Ases y Nueves)")
            doubles += 3
        elif not honores and chowLess:
            doubleActions.append("[+] 5 Dobles: MAH-JONGG LIMPIO (Solo Pungs/Kungs de una pinta)")
            doubles += 5
        else:
            doubleActions.append("[+] 3 Dobles: MAH-JONGG LIMPIO (Pungs y Chows de una pinta)")
            doubles += 3

        total = points*(2**doubles)
        total_prev = total

        total = total // 10
        dig = total%10
        if dig >= 5:
            total += 10
        total = (total//10)*100

        if total > 20000:
            total = 20000

        actions.extend(doubleActions)

        actions.append(f"Total mano: {total_prev} para {total}")

        results.append(f"{entry} | {points} | {doubles} | {total} | TRADICIONAL | {actions}")

if rank != 0:
    comm.send(results, dest=0, tag=rank)
else:
    for i in range(1, size):
        results.extend(comm.recv(source=i, tag=i))
    
    after = datetime.now()
    
    for entry in results:
        print(entry)
    
    
    print(f"{before.replace(microsecond=0)} | {after.replace(microsecond=0)} | {(after-before).total_seconds()}")
