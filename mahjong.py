from mpi4py import MPI
import sys
import os
from datetime import datetime
from collections import Counter

#Grupos
class musketeer:
    def __init__(self, Id: int, suit: str, variety: str, closed: bool):
        self.Id = Id #Número menor en chows, número que se repite en los demás (Para honores mayores es 0)
        self.suit = suit #Bolas, chinos, palos, vientos, etc. (Para honores mayores es lo que sale en la entrada (E, DV,...))
        self.variety = variety #Tipo de grupo (chow, pung, kung, ojo)
        self.closed = closed #Abierto o cerrado
    
    #Para imprimir el objeto
    def __str__(self): 
        return f"({self.variety} {self.suit} {self.Id} {'cerrado' if self.closed else 'abierto'})"
    
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
            if len(line[i]) == 4:
                variety = "single"
            elif line[i][2] == line[i][5]: #Las piezas tienen el mismo número
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

def is_classic(line, chowless, lastPiece, ownFlower):
    is_classic_bool = False

    #Me quedo solo con la linea del mahjong clasico o limite
    line_temp1, separador, line_temp2 = line.partition("]")
    line_temp1, separador, line_temp2 = line_temp2.partition("<")
    final_line = line_temp1

    #diccionario que me indica cuantas veces se repite cada caracter
    dic_char = Counter(final_line)
    total_pts = 0
    actions = []
    mahjong_name = "TRADICIONAL"

    if lastPiece == "B1":
        total_pts = 20000
        mahjong_name = "PESCANDO LA LUNA DEL FONDO DEL MAR"
        is_classic_bool = True

    elif ownFlower and lastPiece == "B5":
        total_pts = 20000
        mahjong_name = "LA FLOR DEL CEREZO"
        is_classic_bool = True

    #Verifico si es HIJOS DE LA NOCHE
    elif (dic_char['('] == 7 and dic_char[')'] == 7) and (dic_char['C'] == 14 or dic_char['P'] == 14 or dic_char['B'] == 14) and (dic_char['1'] + dic_char['2'] + dic_char['3'] + dic_char['4'] + dic_char['5'] + dic_char['6'] + dic_char['7'] + dic_char['8'] + dic_char['9'] == 14):
        total_pts = 7500
        mahjong_name = "HIJOS DE LA NOCHE"
        is_classic_bool = True

    #GRAN SEGUIDILLA REAL
    elif (dic_char['1'] == 1 and dic_char['2'] == 1 and dic_char['3'] == 1 and dic_char['4'] == 1 and dic_char['5'] == 1 and dic_char['6'] == 1 and dic_char['7'] == 1 and dic_char['8'] == 1 and dic_char['9'] == 1) and (dic_char['D'] == 3 and (dic_char['['] == 4 or dic_char['{'] == 4) and (dic_char['N'] == 2 or dic_char['W'] == 2 or dic_char['E'] == 2 or dic_char['S'] == 2)) and ((dic_char['B'] == 9 or dic_char['B'] == 12 or dic_char['C'] == 9 or dic_char['P'] == 9) and dic_char['('] == 1):
        if dic_char['{'] > 0:
            total_pts = 5000 
        else:
            total_pts = 2500
        mahjong_name = "GRAN SEGUIDILLA REAL"
        is_classic_bool = True

    #SIETE SAMURAIS
    elif (dic_char['('] == 7) and (dic_char['D'] + dic_char['N'] + dic_char['S'] + dic_char['E'] + dic_char['W'] + dic_char['1'] +  dic_char['9'] == 14) and (dic_char['R'] <= 2 and dic_char['V'] <= 2 and dic_char['B'] <= 2 and dic_char['N'] <= 2 and dic_char['S'] <= 2 and dic_char['E'] <= 2 and dic_char['W'] <= 2 and dic_char['1'] <= 2 and dic_char['9'] <= 2): #Me dice que los pares son de honores ases o nueves
        total_pts = 2500
        mahjong_name = "7 SAMURAIS"
        is_classic_bool = True

    #ASES Y NUEVES
    elif ((dic_char['['] + dic_char['{']) == 4 and dic_char['('] == 1) and (dic_char['1'] + dic_char['9'] == 14):
        total_pts = 5000
        mahjong_name = "ASES Y NUEVES"
        is_classic_bool = True

    #13 MARAVILLAS
    elif (dic_char['['] == 0) and ((dic_char['D'] == 3 or dic_char['D'] == 4) and (dic_char['R'] == 1 or dic_char['R'] == 2) and (dic_char['V'] == 1 or dic_char['V']) and (dic_char['B'] == 3 or dic_char['B'] == 4)) and ((dic_char['N'] == 1 or dic_char['N'] == 2) and (dic_char['E'] == 1 or dic_char['E'] == 2) and (dic_char['W'] == 1 or dic_char['W'] == 2) and (dic_char['S'] == 1 or dic_char['S'] == 2)) and ((dic_char['1'] == 3 or dic_char['1'] == 4) and (dic_char['9'] == 3 or dic_char['9'] == 4)) and (dic_char['B'] > 0 and dic_char['C'] > 0 and dic_char['P'] > 0):
        total_pts = 2500
        mahjong_name = "13 MARAVILLAS"
        is_classic_bool = True


    #JASPE IMPERIAL
    elif (dic_char['P'] + dic_char['D'] == 14) and (dic_char['2'] + dic_char['3'] + dic_char['4'] + dic_char['6'] + dic_char['8'] + dic_char['V'] == 14): #Verfico si son solo verdes
        total_pts = 5000
        mahjong_name = "JASPE VERDE"
        is_classic_bool = True

    #TIFON ORIENTAL
    elif (dic_char['['] == 4 and dic_char['('] == 1) and (dic_char['D'] == 3 and (dic_char['N'] + dic_char['E'] + dic_char['W'] + dic_char['S'] == 11)):
        total_pts = 10000
        mahjong_name = "TIFON ORIENTAL"
        is_classic_bool = True

    #ROSA DE LOS VIENTOS
    elif (dic_char['['] == 4 and dic_char['('] == 1) and (dic_char['N'] + dic_char['E'] + dic_char['W'] + dic_char['S'] == 12):
        total_pts = 10000
        mahjong_name = "ROSA DE LOS VIENTOS"
        is_classic_bool = True

    #ARMONIA CELESTE
    elif (dic_char['['] == 4 and dic_char['('] == 1) and (dic_char['D'] == 9) and (dic_char['N'] == 3 or dic_char['S'] == 3 or dic_char['E'] == 3 or dic_char['W'] == 3) and (dic_char['1'] == 2 or dic_char['9'] == 2 or dic_char['N'] == 2 or dic_char['W'] == 2 or dic_char['E'] == 2 or dic_char['S'] == 2):
        total_pts = 10000
        mahjong_name = "ARMONIA CELESTE"
        is_classic_bool = True

    #JASPE ROJO
    elif (dic_char['['] == 4 and dic_char['('] == 1) and (dic_char['P'] == 11 or dic_char['P'] == 12) and ((dic_char['D'] == 3 or dic_char['D'] == 2) and (dic_char['R'] == 3 or dic_char['R'] == 2)) and (dic_char['1'] + dic_char['5'] + dic_char['7'] + dic_char['9'] == 11 or dic_char['1'] + dic_char['5'] + dic_char['7'] + dic_char['9'] == 12):
        total_pts = 15000
        mahjong_name = "JASPE ROJO"
        is_classic_bool = True

    #BENDICION CELESTIAL
    elif (dic_char['['] == 4 and dic_char['('] == 1) and (dic_char['2'] + dic_char['4'] + dic_char['8'] == 9) and (dic_char['D'] == 3 and dic_char['B'] == 12) and (dic_char['N'] == 2 or dic_char['S'] == 2 or dic_char['E'] == 2 or dic_char['W'] == 2):
        total_pts = 15000
        mahjong_name = "BENDICION CELESTIAL"
        is_classic_bool = True

    #GRAN MURALLA CHINA
    elif (dic_char['C'] == 14) and (dic_char['1'] + dic_char['3'] + dic_char['5'] + dic_char['7'] + dic_char['9'] == 14):
        total_pts = 15000
        mahjong_name = "GRAN MURALLA CHINA"
        is_classic_bool = True

    #CIUDAD PROHIBIDA
    elif (dic_char['C'] + dic_char['R'] == 14) and (dic_char['2'] + dic_char['4'] + dic_char['6'] + dic_char['8'] + dic_char['D'] == 14):
        total_pts = 15000
        mahjong_name = "CIUDAD PROHIBIDA"
        is_classic_bool = True

    #GRANDES SAMURAIS
    elif (dic_char['('] == 7) and (dic_char['D'] + dic_char['N'] + dic_char['W'] + dic_char['E'] + dic_char['S'] == 14):
        total_pts = 20000
        mahjong_name = "GRANDES SAMURAIS"
        is_classic_bool = True

    #HIJOS UNIDOS
    elif (dic_char['('] == 7) and (dic_char['1'] + dic_char['9'] == 14):
        total_pts = 20000
        mahjong_name = "HIJOS UNIDOS"
        is_classic_bool = True

    return is_classic_bool, total_pts, mahjong_name, actions

def round_base(points):
    r = points % 10
    if r >= 5:
        return ((points // 10) + 1) * 10
    else:
        return (points // 10) * 10

def round_total(total):
    r = total % 100
    if r >= 50:
        return ((total // 100) + 1) * 100
    else:
        return (total // 100) * 100

winds = {1 : "E", 2 : "S", 3 : "W", 4 : "N"}

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if len(sys.argv) < 2:
    print("Error: Debe incluir nombre del archivo.")
    sys.exit(1)

comm.Barrier()
before_wtime = MPI.Wtime()
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
        allChow = True

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

            elif allForOne[-1].suit == roundWind:
                doubleActions.append(f"[+] 1 Doble: Pung/Kung de viento predominante ({roundWind})")
                doubles += 1
            
            if allForOne[-1].variety == "chow":
                chowLess = False
                pinta = allForOne[-1].suit
                continue
            elif allForOne[-1].variety != "ojo":
                allChow = False;
            
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
        ownFlower = False

        if len(line[i]) == 4:
            flowers.append(musketeer(int(line[i][2]), "flor", line[i][1], True))

            if winds[flowers[-1].Id] == ownWind:
                doubleActions.append(f"[+] 1 Doble: Flor propia detectada ({flowers[-1].variety}{flowers[-1].Id})")
                ownFlower = True
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
                doubleActions.append("[+] 3 Dobles: RAMILLETE (flores negras del mismo color)")
                doubles += 3
            if reds == 4:
                doubleActions.append("[+] 3 Dobles: RAMILLETE (flores rojas del mismo color)")
                doubles += 3

        lastPiece = line[-1].strip("*")

        actions = []
        name_mahjong = ""
        is_classic_bool = False
        linea_to_evaluate = "".join(line)

        is_classic_bool, points, name_mahjong, actions = is_classic(linea_to_evaluate, chowLess, lastPiece, ownFlower)

        if not is_classic_bool:
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
    
            points = round_base(points)
    
            actions.append(f"Total puntos: {total} para {points}")

            print(chowLess, allChow)
            if not honores:
                # Solo una pinta numérica (no se pueden mezclar pintas en mahjong tradicional)
                if not chowLess:
                    if allChow:  # los 4 grupos de 3 son chows
                        doubles += 4
                        doubleActions.append("[+] 4 Dobles: MAH-JONGG LIMPIO (puros chow)")
                    else:
                        doubles += 3
                        doubleActions.append("[+] 3 Dobles: MAH-JONGG LIMPIO (pungs y chow de una pinta)")
                else:
                    doubles += 5
                    doubleActions.append("[+] 5 Dobles: MAH-JONGG LIMPIO (pungs de pinta)")
            else:

                if ases and nueves:
                    doubles += 3
                    doubleActions.append(f"[+] 3 Dobles: MAH-JONGG LIMPIO Honores (Pinta {pinta} con Ases y Nueves)")
                else:
                    doubles += 2
                    doubleActions.append("[+] 2 Dobles: MAH-JONGG SUCIO (Honores con pinta)")
    
            total = points*(2**doubles)
            total_prev = total
    
            total = round_total(total)
    
            if total > 20000:
                total = 20000

            actions.extend(doubleActions)
        else:
            doubles = 0
            total = points
            total_prev = total

            actions.append(f"Total puntos: {total} para {points}")

            if ownWind == 'E' and points <= 10000:
                actions.append(f"{total}, ESTE se paga doble")
                total *= 2
                doubles = 1
                if total > 20000:
                    total = 20000

        actions.append(f"Total mano: {total_prev} para {total}")

        results.append(f"{entry} | {points} | {doubles} | {total} | {name_mahjong} | {actions}\n")

if rank != 0:
    comm.send(results, dest=0, tag=rank)
else:
    for i in range(1, size):
        results.extend(comm.recv(source=i, tag=i))

comm.Barrier()
after_wtime = MPI.Wtime()

if rank == 0:
    with open("output.txt", "w", encoding="utf-8") as f:
        f.writelines(results)
        after = datetime.now()
        f.write(f"{before.replace(microsecond=0)} | {after.replace(microsecond=0)} | {(after_wtime-before_wtime):.6f}\n")
