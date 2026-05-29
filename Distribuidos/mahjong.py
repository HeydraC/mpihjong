#Grupos
class musketeer:
    def __init__(self, Id: int, suit: str, variety: str, closed: bool):
        self.Id = Id #Número menor en chows, número que se repite en los demás
        self.suit = suit #Bolas, chinos, palos, vientos, etc.
        self.variety = variety#Tipo de grupo (chow, pung, kong, ojo)
        self.closed = closed#Abierto o cerrado
    
    #Para ordenar chows (Y lo demás seguramente)
    def __eq__(self, other):
        self.Id == other.Id
    def __lt__(self, other):
        self.Id < other.Id
    def __gt__(self, other):
        self.Id > other.Id
    
    #Para imprimir el objeto
    def __str__(self): 
        return f"({self.variety} {self.suit} {self.Id} {"cerrado" if self.closed else "abierto"})"

def notWind(p):
    return p != 'E' and p != 'S' and p != 'W' and p != 'N'

def musketeers(line, i):
    if notWind(line[i][1]):
        if line[i][0] == '(':
            variety = "ojo"
        elif len(line[i]) == 13: #3 guiones + 2 corchetes + 8 letras/números
            variety = "kong"
        else:
            if line[i][2] == line[i][5]: #Las piezas tienen el mismo número
                variety = "pung"
            else:
                variety = "chow"

        if line[i][1] == 'D':
            suit = "dragon" + line[i][2]
            Id = 0 #Honor mayor
        else:
            Id = int(line[i][2])
            suit = line[i][1]
    else:
        if len(line[i]) == 9: #3 guiones + 2 corchetes + 4 letras
            variety = "kong"
        else:
            variety = "pung"
        
        suit = line[i][1]
        
        Id = 0 #Honor mayor

    if line[i][0] == '[': #Los ojo () siempre son cerrados
        closed = False
    else:
        closed = True

    return musketeer(Id, suit, variety, closed)

name = input("Indique el nombre del archivo: ")

#El proceso recibirá un rango de lineas que debe analizar e identificará las suyas con un enumerate
with open(name, "r") as file:
    for entry in file:
        allForOne = [] #Lista de grupos

        line = entry.split()

        Id = line[0]
        points = 0

        ownWind = line[1][1]
        roundWind = line[3][0]

        allForOne.append(musketeers(line, 4))

        groups = str(allForOne[0])

        i = 5

        while(line[i][0] != '<'):
            allForOne.append(musketeers(line, i))
            groups += ' ' + str(allForOne[-1])
            i += 1
        
        flowers = []
        flow = ""

        if line[i] != "<>":
            flowers.append(musketeer(int(line[i][2]), "flor", line[i][1], True))

            flow = str(flowers[0])

            i += 1

            while len(line[i]) == 2:
                flowers.append(musketeer(int(line[i][1]), "flor", line[i][0], True))
                flow += ' ' + str(flowers[-1])

                i += 1
            
            flowers.append(musketeer(int(line[i][1]), "flor", line[i][0], True))
            flow += ' ' + str(flowers[-1])

        lastPiece = line[-1]
        lastPiece = lastPiece.strip("*")

        print(line) #Así se separa la línea
        print(f"{Id} {ownWind} {roundWind} {groups} {flow + ' ' if len(flow) > 0 else ""}{lastPiece}\n")
