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
3. Need to assign different sign for parts in different moving direction
4. Need to solve can't see tail and can't see food

Version 1.6
1. RuntimeError is solved by increasing the setrecursionlimit
2. Head: O, Tail: X
3. It seems the situation that snake can't see tail and can't see food will not happen
4. Head-Food-Tail can't be solved. When it happens, game over.  

Version 1.7
1. Delete redundant codes, and add comments. 
2. Correct a bug that Head-Food-Tail determination is wrong.

@author: shaosh
'''
import curses
import random
import sys
from body import *
 
sys.setrecursionlimit(5000)  #set the recursion limit since there will be many recursions between getTarget() and getTail()
curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, 0)
curses.init_pair(2, curses.COLOR_RED, 0)
myscreen = 0
count = 0   #Count how many food the snake has eaten
snake = [Body(3, 1), Body(2, 1), Body(1, 1)]   #default snake has three parts
height = 8
width = 15
matrix = [[0 for col in range(width -1)] for row in range(height - 1)]  #2D array on which the snake runs 
bfsmap = [[0 for col in range(width -1)] for row in range(height - 1)]  #2D array for BFS
wandermap = [[0 for col in range(width -1)] for row in range(height - 1)]   #2D array for BFS to chase the tail
adjacency = [[[] for col in range(width -1)] for row in range(height - 1)]  #2D array which stores the adjacency list of each point in the matrix
targetx = 0 
targety = 0
FOOD = 0
TAIL = 1

def makeScreen():   #function used to generate the area on which the snake runs
    global myscreen 
    global snake
    myscreen = curses.newwin(height, width, 0, 0)
    myscreen.border("*", "*", "*", "*", "*", "*", "*", "*") 
    curses.curs_set(0)
    myscreen.addstr(0, 5, "Count: ")
    myscreen.addstr(0, 12, str(count))    
    myscreen.refresh()

def init(): #initialize the matrix
    global matrix
    global bfsmap
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            pos = Position(col, row)
            matrix[row][col] = pos
            matrix[row][col].setX(col)
            matrix[row][col].setY(row)        
            myscreen.addstr(row, col, pos.getBodypart())
    myscreen.refresh()

def initAdjacency():    #initialize the adjacency list
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
                
def makeTarget():   #randomly generate the food and print it.
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
    
def printSnake():   #print the snake at the very beginning of the game
    snake[0].setBodypart("O")
    for i in range(0, len(snake)):
        myscreen.addstr(snake[i].getY(), snake[i].getX(), snake[i].getBodypart(), curses.color_pair(1))
    myscreen.refresh()
     
def bfs(bfsType, snakePointer): #bfs for discover the food or tail 
    global targetx
    global targety
    global bfsmap
    global count
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
            #When the tail is discovered and there is no Head-Food-Tail situation, return true
            if x == snakePointer[len(snakePointer) - 1].getX() and  y == snakePointer[len(snakePointer) - 1].getY() and bfsType == TAIL and isHeadFoodTail(u.getSelfX(), u.getSelfY(), snake) == False:
                return True
            #When there is no Head-Food-Tail situation, print related info and game over
            elif bfsType == TAIL and isHeadFoodTail(u.getSelfX(), u.getSelfY(), snake):
                if count + 3 + 1 == (height - 2) * (width - 2):
                    snake[0].setX(targetx) 
                    snake[0].setY(targety)
                    myscreen.addstr(targety, targetx, snake[0].getBodypart(), curses.color_pair(1))
                    count += 1
                    myscreen.addstr(0, 12, str(count))
                    print("The ground is full and game is over")
                    sys.exit()
                print("No solution. Game Over")
                sys.exit()
            #color white nodes into gray and enqueue the new gray nodes. When bfs for Food, the snake body will not be accessed; when 
            #bfs for Tail, the snake body except the tail will not be accessed. 
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
    if bfsType == FOOD: #generated the path from snake head to food, using the parent location. Actually this step can be deleted if we do bfs from food to snake head
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

def bfsWander(adjx, adjy, tailx, taily):    #bfs for chasing the tail. It discovers the path from the adjacent position of the head to the tail 
    global wandermap
    found = False  
    allAdjSnake = True
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
    package = [found, wandermap[adjy][adjx].getDistance()]  #return the distance so that the snake can compare which adjacent position has the longest path
    return package

def recon():    #send out a virtual snake to detect if the path generated by bfs is safe, i.e., after the snake ate the food, if it can still see its tail. 
                #If it can see its tail, it can still be alive by chasing its tail even when it can't see the food. 
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
        if targetx == virtualSnake[0].getX() and targety == virtualSnake[0].getY():
            virtualSnake.append(Body(previous[0], previous[1]))
    return bfs(TAIL, virtualSnake)
        
def getTarget():   #Move the snake to eat the food according the path discovered by bfs()
    global count
    if bfs(FOOD, snake) == True:
        while (snake[0].getX() == targetx and snake[0].getY() == targety) == False:
            if bfs(FOOD, snake) == True:    #After each step do bfs again so that the snake can find the best path
                if recon() == True: #Before movement, it first sends out a virtual snake to see if this path is safe.
                    for part in range(0, len(snake)):                                       
                        if part == 0:   #Move the snake head based on the child node in bfsmap
                            previousX = snake[part].getX()
                            previousY = snake[part].getY()
                            snake[part].setX(bfsmap[previousY][previousX].getChildX())
                            snake[part].setY(bfsmap[previousY][previousX].getChildY())
                        elif part == 1:
                            previous = bodyMove(previousX, previousY, part, snake)  #Move the snake part to the position which used to be occupied by the part in front of it
                        else:
                            previous = bodyMove(previous[0], previous[1], part, snake)
                        myscreen.addstr(snake[part].getY(), snake[part].getX(), snake[part].getBodypart(), curses.color_pair(1))
                    if targetx == snake[0].getX() and targety == snake[0].getY():   #Eat the food and extend the snake body 
                        snake[len(snake) - 1].setBodypart("+")
                        snake.append(Body(previous[0], previous[1]))
                        snake[len(snake) - 1].setBodypart("X")
                        count += 1
                        matrix[targety][targetx].setBodypart(" ")   #delete the food in the matrix, so that the snake can discover the newly produced food
                        myscreen.addstr(0, 12, str(count))
                        myscreen.addstr(previous[1], previous[0], Body.getTailpart(), curses.color_pair(1)) 
                    else:
                        myscreen.addstr(previous[1], previous[0], " ")  
                    myscreen.refresh()
                    curses.delay_output(100)
                else:   #if the path is not safe, just chase its tails and go to eat the food when the path is safe
                    getTail()
                    break   #break otherwise it might chase its tail forever after eating the food
            else: #if it can't see the food, just chase its tails and go to eat the food when the path is safe
                getTail()
                break
    else:   #if it can't see the food, just chase its tails and go to eat the food when the path is safe
        getTail()

def getTail():  #direct the snake to chase its tail
    global wandermap
    tailX = snake[len(snake) - 1].getX()
    tailY = snake[len(snake) - 1].getY()
    tailAvailable = False
    getfood = False
    max = -1
    maxAdj = -1
    for i in range(0, len(adjacency[snake[0].getY()][snake[0].getX()])):    #Call bfsWander() to discover the path from an adjacent position to its tail and choose the one has the longest path, 
                                                                            #so that the snake can move as long as possible to get better chance to discover the food
        package = bfsWander(adjacency[snake[0].getY()][snake[0].getX()][i].getX(), adjacency[snake[0].getY()][snake[0].getX()][i].getY(), tailX, tailY)
        if package[0] == True:
            tailAvailable = True
        if package[1] > max:
            max = package[1]
            maxAdj = i
    if tailAvailable == True:   #When there is a path to its tail, chase it
        bfsWander(adjacency[snake[0].getY()][snake[0].getX()][maxAdj].getX(), adjacency[snake[0].getY()][snake[0].getX()][maxAdj].getY(), tailX, tailY)#establish the longest path 
        wandermap[snake[0].getY()][snake[0].getX()].setParentX(adjacency[snake[0].getY()][snake[0].getX()][maxAdj].getX())#establish path from snake head to its adjacent position
        wandermap[snake[0].getY()][snake[0].getX()].setParentY(adjacency[snake[0].getY()][snake[0].getX()][maxAdj].getY()) 
        for part in range(0, len(snake)):   #move snake head to its adjacent position                                       
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
            if bfs(FOOD, snake) == True and recon() == True:    #When chasing the tail, if it finds a safe path to eat the food, go to eat it
                getTarget()
                getfood = True
                break   #after ate the food, no longer chase its tail
            else:
                for part in range(0, len(snake)):                                       
                    if part == 0:
                        previousX = snake[part].getX()
                        previousY = snake[part].getY()
                        snake[part].setX(wandermap[previousY][previousX].getParentX())
                        snake[part].setY(wandermap[previousY][previousX].getParentY())
                    elif part == 1:
                        previous = bodyMove(previousX, previousY, part, snake)
                    else:
                        previous = bodyMove(previous[0], previous[1], part, snake)
                    myscreen.addstr(snake[part].getY(), snake[part].getX(), snake[part].getBodypart(), curses.color_pair(1))
                myscreen.addstr(previous[1], previous[0], " ") 
                myscreen.refresh()
                curses.delay_output(100)
                if snake[0].getX() == tailX and snake[0].getY() == tailY:
                    break
        if bfs(FOOD, snake) == True and recon() == True and getfood == False:   #When it gets to the original tail position and there is a safe path for the food, go to eat it.
            getTarget()
        elif getfood == False:  #if the food has not been eaten and there is no safe path, continue to chase the tail 
            getTail()
    else:
        print("can't see tail")
        myscreen.getch()       
                    
                    
def bodyMove(previousX, previousY, part, snakePointer): #function to move the snake body except head
    tempX = snakePointer[part].getX()
    tempY = snakePointer[part].getY()
    snakePointer[part].setX(previousX)
    snakePointer[part].setY(previousY)  
    previousX = tempX
    previousY = tempY
    previous = [previousX, previousY]
    return previous 

def search(x, y, snakePointer): #check if certain position is occupied by the snake
    for i in range(0, len(snakePointer)):
        if snakePointer[i].getX() == x and snakePointer[i].getY() == y:
            return True
    return False

def searchTail(x, y, snakePointer): #check if certain position is occupied by the snake (tail is not included)
    for i in range(0, len(snakePointer) - 1):
        if snakePointer[i].getX() == x and snakePointer[i].getY() == y:
            return True
    return False

def isHeadFoodTail(x, y, snakePointer): #check if current situation is Head-Food-Tail which can't be solved.
    head = False
    body = True
    tail = False
    food = False
    if matrix[y][x].getBodypart() == "@":
        for i in range(0, len(adjacency[y][x])):
            if adjacency[y][x][i].getX() == snakePointer[0].getX() and adjacency[y][x][i].getY() == snakePointer[0].getY():
                head = True
            elif adjacency[y][x][i].getX() == snakePointer[len(snakePointer) - 1].getX() and adjacency[y][x][i].getY() == snakePointer[len(snakePointer) - 1].getY():
                tail = True
            if search(adjacency[y][x][i].getX(), adjacency[y][x][i].getY(), snakePointer) == False:
                body = False
        
        if head == True and tail == True and body == True:
            print(body)
            return True
    return False
    
def play(): #When there is space, keep moving and generating food
    while count + 3 <= (height - 2) * (width - 2):
        makeTarget()
        getTarget()             
 
def main(): #driver
    makeScreen() 
    init()  
    initAdjacency() 
    printSnake()
    play()
    myscreen.getch()
    curses.endwin()
    
main()