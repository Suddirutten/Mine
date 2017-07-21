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
import sys
sys.setrecursionlimit(1500)

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
        square = self.getObj(row,col)
        #Om rad och kolumn är utanför brädet: avbryt
        if row > (self.row-2) or row<2 or col > (self.col-2) or col<2:
            return;
        #Om rutan redan syns: avbryt
        if square.isHidden == False:
            return;
        #Om där finns en bomb: avbryt
        if square.value == True:
            return;
        #Räkna antalet bomber runt rutan:
        n = square.neighbour
        #Om antalet grannar är större än noll: Visa rutan och avbryt
        if n > 0:
            square.isHidden = False
            return;
        square.isHidden = False
        #Sen: fortsätt söka runt rutan
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
    board = Board(row,col)
    board.placeSquares()
    while True:
        mines = int(input('Hur många minor vill du ha på din spelplan?'))
        if mines >= board.size():
            print ('Hmm, du kan inte ha fler eller lika många minor som du har rutor. Prova igen!')
            maxSize = board.size()-1
            print('Max är:',maxSize)
        else:
            break;
    board.placeMines(mines) #sätter ut alla minor
    for i in range(1,row-1): #räknar grannarna på alla rutor
        for j in range(1,col-1):
            board.getNeighbour(i,j)
     
    board.showAll() #visar alla värden
    print(board.str()) #printar ut alla visade värden      
    board.hideAll() #gömmer värdena igen
    print(board.str())
    
    while True:
        row2 = int(input('Vilken ruta vill du börja med att öppna? Ange rad:'))
        col2 = int(input('Ange kolumn:'))
        if row2 > board.row:
            print('Luring! Du kan inte välja en rad som inte finns. Prova igen.')
        elif col2 > board.col:
            print('Luring! Du kan inte välja en kolumn som inte finns. Prova igen')
        else:
            break;
    if board.getObj(row2,col2).value == True: #om där finns en bomb
        board.getObj(row2,col2).value = False #placera om bomben, trist att dö på första försöket
        board.placeMines(1)
##    board.getObj(row2,col2).isHidden = False #visa rutans värde
    board.search(row2,col2) #metoden som ej fungerar
    print(board.str()) #printa ut brädan igen
    running = True
    mines_found = 0
    while mines_found != mines:
        while True:
            print('Vill du flagga en ruta eller öppna en?')
            choice = input('Skriv "F" för att flagga en ruta, "Ö" för att öppna en:')
            if choice.lower() is not 'F'.lower() or choice.lower() is not 'Ö'.lower():
                print('Oj, det måste blivit fel när du valde Öppna eller Flagga. Prova igen.')
                break;
            else:
                break;
        if choice == 'F':
            row3 = int(input('Vilken ruta vill du flagga? Ange rad:'))
            col3 = int(input('Ange kolumn:'))
            board.getObj(row3,col3).isFlagged = True
            board.getObj(row3,col3).isHidden = False
            if board.getObj(row3,col3).value == True:
                mines_found +=1
        if choice == 'Ö':
            row4 = int(input('Vilken ruta vill du öppna? Ange rad:'))
            col4 = int(input('Ange kolumn:'))
            if board.getObj(row4,col4).value == True:
                print ('GAME OVER')
                print(board.str())
                inputt = input('Vill du spela igen?')
                if inputt == 'Ja':
                    run = False;
                elif inputt == 'Nej':
                    run = False;
            else:
                board.search(row4,col4)
                
    print('Omg du vann du är bäst i hela världen')        
    print (board.str())
    print()

    run = False


#Input: Hur många rader och kolumner som användaren vill spela med
#Skapar ett bräde av det
#Sätter ut minor på brädet, antal minor proportionellt mot storleken av brädet
#Låter användaren klicka i någon ruta, en andel av spelplanen visas då (ej minor)

