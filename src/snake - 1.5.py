'''
Created on 2013-5-24
Version 1.0
1. Move right and down is completed. 
2. Need to combine and eliminate the repeated codes 

Version 1.1
1. Complete simple version: the snake can eat things without considering body

Version 1.2
1. Change hard coded movement to the path along the BFS, but the snake will still bite itself
2. init() -> init() + initAdjacency()

Version 1.3
1. Body(x, y) in snake ==> search(x, y). If use Body(x, y) in snake, it will only compare the address but not the x and y
2. Ignoring the snake body in adjacency list in bfs() will prevent the snake from biting itself.
3. The snake will not bite itself.  
4. Delete move() and headMover()
5. Next step: Wander

Version 1.4
1. Add recon() to detect if the snake can see its own tail after eating the food
2. Change the position of bfs()
3. Add snakePointer to bfs() and search()

Version 1.5
1. Chasing tail is almost done. 
2. RuntimeError: maximum recursion depth exceeded
@author: shaosh
'''
import curses
import random
from body import *
 
curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, 0)
curses.init_pair(2, curses.COLOR_RED, 0)
curses.init_pair(3, curses.COLOR_YELLOW, 0)
myscreen = 0
count = 0
snake = [Body(3, 1), Body(2, 1), Body(1, 1)]
height = 10
width = 20
matrix = [[0 for col in range(width -1)] for row in range(height - 1)]
# queue = []
bfsmap = [[0 for col in range(width -1)] for row in range(height - 1)]
wandermap = [[0 for col in range(width -1)] for row in range(height - 1)]
adjacency = [[[] for col in range(width -1)] for row in range(height - 1)]
targetx = 0
targety = 0
FOOD = 0
TAIL = 1
PLAY = 0
GETTAIL = 1

def makeScreen():
    global myscreen 
    global snake
    myscreen = curses.newwin(height, width, 0, 0)
    myscreen.border("*", "*", "*", "*", "*", "*", "*", "*") 
    curses.curs_set(0)
    myscreen.addstr(0, 5, "Count: ")
    myscreen.addstr(0, 12, str(count))
    
    myscreen.refresh()

def init():
    global matrix
#     global queue
    global bfsmap
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            pos = Position(col, row)
            matrix[row][col] = pos
            matrix[row][col].setX(col)
            matrix[row][col].setY(row)        
            myscreen.addstr(row, col, pos.getBodypart())
    myscreen.refresh()

def initAdjacency():
    global adjacency
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            if row == 1 and col == 1:
                adjacency[row][col].append(Position(col + 1, row))
                adjacency[row][col].append(Position(col, row + 1))
            elif row == 1 and col == width - 2:
                adjacency[row][col].append(Position(col - 1, row))
                adjacency[row][col].append(Position(col, row + 1))
            elif row == height - 2 and col == 1:
                adjacency[row][col].append(Position(col + 1, row))
                adjacency[row][col].append(Position(col, row - 1))
            elif row == height - 2 and col == width - 2:
                adjacency[row][col].append(Position(col - 1, row))
                adjacency[row][col].append(Position(col, row - 1))
            elif row == 1:
                adjacency[row][col].append(Position(col - 1, row))
                adjacency[row][col].append(Position(col + 1, row))
                adjacency[row][col].append(Position(col, row + 1))
            elif row == height - 2:
                adjacency[row][col].append(Position(col - 1, row))
                adjacency[row][col].append(Position(col + 1, row))
                adjacency[row][col].append(Position(col, row - 1))
            elif col == 1:
                adjacency[row][col].append(Position(col, row + 1))
                adjacency[row][col].append(Position(col, row - 1))
                adjacency[row][col].append(Position(col + 1, row))
            elif col == width - 2:
                adjacency[row][col].append(Position(col, row + 1))
                adjacency[row][col].append(Position(col, row - 1))
                adjacency[row][col].append(Position(col - 1, row))
            else:
                adjacency[row][col].append(Position(col, row + 1))
                adjacency[row][col].append(Position(col, row - 1))
                adjacency[row][col].append(Position(col - 1, row))
                adjacency[row][col].append(Position(col + 1, row))
                
def makeTarget():
    availalbe = False
    target = Target(random.randint(1, width - 2), random.randint(1, height - 2))
    while availalbe == False:
        if search(target.getX(), target.getY(), snake) == False:
            availalbe = True
        else:
            target = Target(random.randint(1, width - 2), random.randint(1, height - 2))
    else:
        myscreen.addstr(target.getY(), target.getX(), target.getBodypart(), curses.color_pair(2))
        matrix[target.getY()][target.getX()].setBodypart("@")
        myscreen.refresh()
    
def printSnake():
#     snake[0].setBodypart("O")
#     snake[len(snake) - 1].setBodypart("X")
    for i in range(0, len(snake)):
        myscreen.addstr(snake[i].getY(), snake[i].getX(), snake[i].getBodypart(), curses.color_pair(1))
    myscreen.refresh()
    
def bfs(bfsType, snakePointer):
    global targetx
    global targety
    global bfsmap
    found = False  
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            if bfsType == FOOD:
                bfsmap[row][col] = BfsElement("white", col, row, None, None, None, None, -1)
            elif bfsType == TAIL:
                bfsmap[row][col].setColor("white")
    bfsmap[snakePointer[0].getY()][snakePointer[0].getX()].setColor("gray") 
    if bfsType == FOOD: 
        bfsmap[snakePointer[0].getY()][snakePointer[0].getX()].setDistance(0)
    queue = []
    queue.append(bfsmap[snakePointer[0].getY()][snakePointer[0].getX()])
    
    while len(queue) != 0:
        u = queue[0]
        if matrix[u.getSelfY()][u.getSelfX()].getBodypart() == "@" and bfsType == FOOD:
            targetx = u.getSelfX()
            targety = u.getSelfY()
            found = True
            break
        queue.remove(queue[0])
        for i in range(0, len(adjacency[u.getSelfY()][u.getSelfX()])):
            x = adjacency[u.getSelfY()][u.getSelfX()][i].getX()
            y = adjacency[u.getSelfY()][u.getSelfX()][i].getY()
            if x == snakePointer[len(snakePointer) - 1].getX() and  y == snakePointer[len(snakePointer) - 1].getY() and bfsType == TAIL:
                return True
            if (search(x, y, snakePointer) == False and bfsType == FOOD) or (searchTail(x, y, snakePointer) == False and bfsType == TAIL):
                if bfsmap[y][x].getColor() == "white":
                    bfsmap[y][x].setColor("gray")
                    if bfsType == FOOD: 
                        bfsmap[y][x].setDistance(u.getDistance() + 1)
                        bfsmap[y][x].setParentX(u.getSelfX())
                        bfsmap[y][x].setParentY(u.getSelfY())
                    queue.append(bfsmap[y][x])
        u.setColor("black")
    if found == False:
        return False
    if bfsType == FOOD:
        x = targetx
        y = targety   
        while (x == snakePointer[0].getX() and y == snakePointer[0].getY()) == False:
            bfsmap[bfsmap[y][x].getParentY()][bfsmap[y][x].getParentX()].setChildX(x)
            bfsmap[bfsmap[y][x].getParentY()][bfsmap[y][x].getParentX()].setChildY(y)
            tempY = y
            tempX = x
            y = bfsmap[tempY][tempX].getParentY()
            x = bfsmap[tempY][tempX].getParentX()
    return True

def bfsWander(adjx, adjy, tailx, taily):
    global wandermap
    found = False  
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            wandermap[row][col] = BfsElement("white", col, row, None, None, None, None, -1)
    wandermap[taily][tailx].setColor("gray") 
    wandermap[taily][tailx].setDistance(0)
    wandermap[taily][tailx].setParentX(tailx)
    wandermap[taily][tailx].setParentY(taily)
    queue = []
    queue.append(wandermap[taily][tailx])
    
    while len(queue) != 0:
        u = queue[0]
        if u.getSelfY() == adjy and u.getSelfX() == adjx:
            found = True
            break
        queue.remove(queue[0])
        for i in range(0, len(adjacency[u.getSelfY()][u.getSelfX()])):
            x = adjacency[u.getSelfY()][u.getSelfX()][i].getX()
            y = adjacency[u.getSelfY()][u.getSelfX()][i].getY()
            if (search(x, y, snake) == False):
                if wandermap[y][x].getColor() == "white":
                    wandermap[y][x].setColor("gray")
                    wandermap[y][x].setDistance(u.getDistance() + 1)
                    wandermap[y][x].setParentX(u.getSelfX())
                    wandermap[y][x].setParentY(u.getSelfY())
                    queue.append(wandermap[y][x])
        u.setColor("black")
#     if found == False:
#         package = [False, wandermap[adjy][adjx].getDistance()]
#         return package
    package = [found, wandermap[adjy][adjx].getDistance()]
    return package

def recon():
    virtualSnake = []
    for i in range(0, len(snake)):
        virtualSnake.append(Body(snake[i].getX(), snake[i].getY()))
    
    while (virtualSnake[0].getX() == targetx and virtualSnake[0].getY() == targety) == False:
        for part in range(0, len(virtualSnake)):                                       
            if part == 0:
                previousX = virtualSnake[part].getX()
                previousY = virtualSnake[part].getY()
                virtualSnake[part].setX(bfsmap[previousY][previousX].getChildX())
                virtualSnake[part].setY(bfsmap[previousY][previousX].getChildY())
            elif part == 1:
                previous = bodyMove(previousX, previousY, part, virtualSnake)
            else:
                previous = bodyMove(previous[0], previous[1], part, virtualSnake)
#             myscreen.addstr(virtualSnake[part].getY(), virtualSnake[part].getX(), virtualSnake[part].getBodypart(), curses.color_pair(2))
#         myscreen.addstr(previous[1], previous[0], " ") 
        if targetx == virtualSnake[0].getX() and targety == virtualSnake[0].getY():
            virtualSnake.append(Body(previous[0], previous[1]))
#             myscreen.addstr(previous[1], previous[0], Body.getBodypart(), curses.color_pair(2))
#         myscreen.refresh()
#         curses.delay_output(50)
#     myscreen.getch()
    return bfs(TAIL, virtualSnake)
        
def getTarget():   
    global count
    if bfs(FOOD, snake) == True:
        while (snake[0].getX() == targetx and snake[0].getY() == targety) == False:
            if bfs(FOOD, snake) == True:
                if recon() == True:
                    for part in range(0, len(snake)):                                       
                        if part == 0:
                            previousX = snake[part].getX()
                            previousY = snake[part].getY()
                            snake[part].setX(bfsmap[previousY][previousX].getChildX())
                            snake[part].setY(bfsmap[previousY][previousX].getChildY())
                        elif part == 1:
                            previous = bodyMove(previousX, previousY, part, snake)
                        else:
                            previous = bodyMove(previous[0], previous[1], part, snake)
                        myscreen.addstr(snake[part].getY(), snake[part].getX(), snake[part].getBodypart(), curses.color_pair(1))
                    if targetx == snake[0].getX() and targety == snake[0].getY():
                        snake.append(Body(previous[0], previous[1]))
                        count += 1
                        matrix[targety][targetx].setBodypart(" ")
                        myscreen.addstr(0, 12, str(count))
                        myscreen.addstr(previous[1], previous[0], Body.getBodypart(), curses.color_pair(1)) 
                    else:
                        myscreen.addstr(previous[1], previous[0], " ") 
                    myscreen.refresh()
                    curses.delay_output(100)
                else:
                    getTail()
                    break
            else:
                getTail()
                break
    else:
        getTail()

def getTail():
    global wandermap
    tailX = snake[len(snake) - 1].getX()
    tailY = snake[len(snake) - 1].getY()
    tailAvailable = False
    getfood = False
    max = -1
    maxAdj = -1
    for i in range(0, len(adjacency[snake[0].getY()][snake[0].getX()])):
        package = bfsWander(adjacency[snake[0].getY()][snake[0].getX()][i].getX(), adjacency[snake[0].getY()][snake[0].getX()][i].getY(), tailX, tailY)
        if package[0] == True:
            tailAvailable = True
        if package[1] > max:
            max = package[1]
            maxAdj = i
    if tailAvailable == True:
        bfsWander(adjacency[snake[0].getY()][snake[0].getX()][maxAdj].getX(), adjacency[snake[0].getY()][snake[0].getX()][maxAdj].getY(), tailX, tailY)
        wandermap[snake[0].getY()][snake[0].getX()].setParentX(adjacency[snake[0].getY()][snake[0].getX()][maxAdj].getX())
        wandermap[snake[0].getY()][snake[0].getX()].setParentY(adjacency[snake[0].getY()][snake[0].getX()][maxAdj].getY()) 
#         print(str(wandermap[snake[0].getY()][snake[0].getX()].getParentY()) + " " + str(wandermap[snake[0].getY()][snake[0].getX()].getParentX()))       
#         myscreen.getch()
        for part in range(0, len(snake)):                                       
            if part == 0:
                previousX = snake[part].getX()
                previousY = snake[part].getY()
                snake[part].setX(adjacency[previousY][previousX][maxAdj].getX())
                snake[part].setY(adjacency[previousY][previousX][maxAdj].getY())
            elif part == 1:
                previous = bodyMove(previousX, previousY, part, snake)
            else:
                previous = bodyMove(previous[0], previous[1], part, snake)
            myscreen.addstr(snake[part].getY(), snake[part].getX(), snake[part].getBodypart(), curses.color_pair(1))
        myscreen.addstr(previous[1], previous[0], " ") 
        while (snake[0].getX() == tailX and snake[0].getY() == tailY) == False:
            if bfs(FOOD, snake) == True and recon() == True:
                getTarget()
                getfood = True
                break
            else:
                for part in range(0, len(snake)):                                       
                    if part == 0:
                        previousX = snake[part].getX()
                        previousY = snake[part].getY()
                        if wandermap[previousY][previousX].getParentX() == None or wandermap[previousY][previousX].getParentY() == None:
                            print("none" + " " + str(previousY) + " " + str(previousX))
                            myscreen.getch()
                        snake[part].setX(wandermap[previousY][previousX].getParentX())
                        snake[part].setY(wandermap[previousY][previousX].getParentY())
                    elif part == 1:
                        previous = bodyMove(previousX, previousY, part, snake)
                    else:
                        previous = bodyMove(previous[0], previous[1], part, snake)
#                     print(str(snake[part].getY()) + " " + str(snake[part].getX()))
                    myscreen.addstr(snake[part].getY(), snake[part].getX(), snake[part].getBodypart(), curses.color_pair(1))
                myscreen.addstr(previous[1], previous[0], " ") 
                myscreen.refresh()
                curses.delay_output(100)
                if snake[0].getX() == tailX and snake[0].getY() == tailY:
                    break
        if bfs(FOOD, snake) == True and recon() == True and getfood == False:
            getTarget()
        elif getfood == False:
            getTail()
    else:
        print("can't see tail")
        myscreen.getch()       
                    
                    
def bodyMove(previousX, previousY, part, snakePointer):
    tempX = snakePointer[part].getX()
    tempY = snakePointer[part].getY()
    snakePointer[part].setX(previousX)
    snakePointer[part].setY(previousY)
    previousX = tempX
    previousY = tempY
    previous = [previousX, previousY]
    return previous 

def search(x, y, snakePointer):
    for i in range(0, len(snakePointer)):
        if snakePointer[i].getX() == x and snakePointer[i].getY() == y:
            return True
    return False

def searchTail(x, y, snakePointer):
    for i in range(0, len(snakePointer) - 1):
        if snakePointer[i].getX() == x and snakePointer[i].getY() == y:
            return True
    return False
        
def play():
    while count + 3 <= (height - 2) * (width - 2):
        makeTarget()
        getTarget()              
 
def main():
    makeScreen() 
    init()  
    initAdjacency() 
    printSnake()
    play()
    myscreen.getch()
    curses.endwin()
    
main()