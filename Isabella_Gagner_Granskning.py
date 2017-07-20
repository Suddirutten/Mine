# P-uppgift, MineSweeper, kodskelett version 2
# Isabella Gagner
# 2017-07-14

# Programmet ska vara ett minesweeperprogram
# Användaren ska kunna:
## Bestämma hur stor spelplan hen vill ha
## Kunna fuska sig fram och visa alla minor med ett kommando
## Kunna flagga där hen tänkt ut att det ligger minor
## Plocka fram rutor som visar siffor som berättar hur många minor som ligger runt
## Vanliga minesweeper visar nya rutor om man klickar i en ruta som inte har minor nära
# Olika färger på siffror som i original-minesweeper?
# Ska kunna se timer på programmet för att se hur lång tid det tagit (main-programmet)
# I en fil ska olika användare och deras poäng kunna lagras,
#för att kunna skapa en lista över de bästa användarna och printa ut deras tider

import random

#En klass som skapar ett bräde med värde null i varje ruta
class Board():
    
    #Init gör en matris med värde null i alla rutor
    def __init__(self, row, col, isFound = False):
        self.board = [[False for x in range(col)] for y in range(row)]
        self.row = row
        self.col = col
        self.isFound = False
        
    #Skapar iterator för matrisen (så att jag kan iterera över brädet)
    def __iter__(self):
        return iter(self.board)

    #Returnerar stringen av bräda
    def str(self):
        mening = []
        for i in range (1,row-1):
            for j in range (1,col-1):
                mening.append(str(self.getObj(i,j)))
        lenn = int(self.size()/(col-2))
        n = 0
        mening_lista = []
        while n < col:
            mening_lista.append('    '.join(mening[n*lenn:(n+1)*lenn]))
            n+=1
        return '\n'.join(mening_lista)
    
    #Lägger till ett objekt på aktuell plats
    #Inparametrar: rad, kolumn, objektet som ska läggas till
    def putObj(self,row,col,obj):
        self.board[row][col] = obj

    #Lägger en Square på alla platser i brädet
    def placeSquares(self):
        for i in range(self.row):
            for j in range(self.col):
                ruta = Square()
                self.putObj(i,j,ruta)

    #Returnerar objektet på en viss plats i brädet
    def getObj(self, row, col):
        return self.board[row][col]
    
    #Returnerar totalt antal rutor i brädet
    def size(self):
        size = (self.col-2)*(self.row-2)
        return size
            
    #Räknar antalet minor runt rutan man tittar på
    #Inparameter: rad och kolumn
    #Utparameter: antal grannar rutan har
    def getNeighbour(self,row,col):
        n = 0
        for i in range (row-1, row+2):
            for j in range (col-1, col+2):
                if i == row and j == col: #rutan vi tittar på räknas ej
                    n = n
                elif self.getObj(i,j).value == True: #om grannen är True
                    n += 1                          #ökar antal grannar
        self.getObj(row,col).neighbour = n #ändrar antal grannar i rutan
        return n

    #Placerar ut minor på slumpmässiga platser
    def placeMines(self, mine):
        n = 0
        while n < mine: #placerar bara minor i inre området
            i = random.randrange(1,self.row-1)
            j = random.randrange(1,self.col-1)
            if self.getObj(i,j).value == True: #om där redan finns en mina
                n = n   #så ökas inte antalet minor
            else:
                self.getObj(i,j).putMine() #annars läggs en mina där
                n +=1
                
    #Visar alla värden i ett bräde
    def showAll(self):
        for i in range(self.row):
            for j in range(self.col):
                self.getObj(i,j).showValue()
                
    #Gömmer alla värden i ett bräde
    def hideAll(self):
        for i in range(self.row):
            for j in range(self.col):
                self.getObj(i,j).hideValue()

    #Öppnar rutor kring rutan man vill öppna (rekursion)
    def search(self,row,col):
        #Räkna antalet bomber runt rutan:
        n = self.getObj(row,col).neighbour
        #Om rad och kolumn är utanför brädet: avbryt
        if row > self.row and col > self.col:
            return
        #Om rutan redan syns: avbryt
        elif self.getObj(row,col).isHidden == False:
            return
        #Om där finns en bomb: avbryt
        elif self.getObj(row,col).value == True:
            return
        #Om antalet grannar är större än noll: Visa rutan och avbryt
        elif n > 0:
            self.getObj(row,col).isHidden = False
            return
        #Annars: fortsätt söka runt rutan
        for (drow,dcol) in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
            self.search(row+drow,col+dcol)
           
        
        
        
class Square():

    def __init__(self):
        self.value = False
        self.isFlagged = False
        self.isFound = False
        self.isHidden = True
        self.neighbour = 0

    #Returnerar strängen av rutan man undersöker
    def __str__(self):
        if self.isFlagged:
            return 'F'
        elif self.isFound:
            return 'F.M.!'       
        elif self.isHidden:
            return '*'
        elif self.isHidden == False:
            if self.value == True:
                return 'M'
            else:
                return str(self.neighbour)

    #Visar rutans värde
    def showValue(self):
        self.isHidden = False

    #Gömmer rutans värde
    def hideValue(self):
        self.isHidden = True

    #Placerar en mina i rutan
    def putMine(self):
        self.value = True

    #Placerar en flagga i rutan
    def flag(self):
        self.isFlagged = True

    #Visar att minan är hittad
    def found(self):
        self.isFound = True

    #Ändrar antalet grannar för rutan
    def neighbour(self, neighbour):
        self.neighbour = neighbour

#En klass som skapar användare
class Player():

    #Skapar en spelare
    def __init__(self, name, time):
        self.name = name
        self.time = time

    def __str__(self):
        return 'Namn: ' +self.name +'. Bästa tid: ' + str(self.time) + ' sek.\n'

    def newTime(self, newTime):
        self.time = newTime

    #Öppnar en fil och skriver in spelarens HighScore + namn i filen
    def highScore(self):
        file = 'MineSweeperPlayers.txt'
        file = open(file,'w') 
        file.append(str(self))
        file.close() 

    #Returnerar det som finns på filen (sorterat, så den som har bäst tid är först)
    def printHighScore(file):
        return string


run = True
while run:
    row = int(input('Hur många rader och kolumner vill du ha din spelplan på?')) + 2
    col = row
    
    bräda = Board(row,col)
    bräda.placeSquares()
    bol = True
    while bol == True:
        minor = int(input('Hur många minor vill du ha på din spelplan?'))
        if minor >= bräda.size():
            print ('Hmm, du kan inte ha fler eller lika många minor som du har rutor. Prova igen!')
            maxSize = bräda.size()-1
            print('Max är:',maxSize)
        else:
            bol = False
    bräda.placeMines(minor) #sätter ut alla minor
    for i in range(1,row-1): #räknar grannarna på alla rutor (förutom en ram av nollor runt)
        for j in range(1,col-1):
            bräda.getNeighbour(i,j)
     
    bräda.showAll() #visar alla värden
    
    print(bräda.str()) #printar ut alla visade värden      
    bräda.hideAll() #gömmer värdena igen
    print(bräda.str())
    rad = int(input('Vilken ruta vill du börja med att öppna? Ange rad:'))
    kol = int(input('Ange kolumn:'))
    if bräda.getObj(rad,kol).value == True: #om där finns en bomb
        bräda.getObj(rad,kol).value = False #placera om bomben, trist att dö på första försöket
        bräda.placeMines(1)
    bräda.getObj(rad,kol).isHidden = False #visa rutans värde

    bräda.search(rad,kol)
    print (bräda.str())
    print()

    run = False


#Input: Hur många rader och kolumner som användaren vill spela med
#Skapar ett bräde av det
#Sätter ut minor på brädet, antal minor proportionellt mot storleken av brädet
#Låter användaren klicka i någon ruta, en andel av spelplanen visas då (ej minor)

