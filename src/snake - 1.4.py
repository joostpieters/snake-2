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
@author: shaosh
'''
import curses
import random
from body import *
 
curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, 0)
curses.init_pair(2, curses.COLOR_RED, 0)
myscreen = 0
count = 0
snake = [Body(3, 1), Body(2, 1), Body(1, 1)]
height = 10
width = 60
map = [[0 for col in range(width -1)] for row in range(height - 1)]
queue = []
bfsmap = [[0 for col in range(width -1)] for row in range(height - 1)]
adjacency = [[[] for col in range(width -1)] for row in range(height - 1)]
targetx = 0
targety = 0

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
    global map
    global queue
    global bfsmap
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            pos = Position(col, row)
            map[row][col] = pos
            map[row][col].setX(col)
            map[row][col].setY(row)        
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
        if (Body(target.getX(), target.getY()) in snake) == False:
            availalbe = True
        else:
            target = Target(random.randint(1, width - 2), random.randint(1, height - 2))
    else:
        myscreen.addstr(target.getY(), target.getX(), target.getBodypart(), curses.color_pair(2))
        map[target.getY()][target.getX()].setBodypart("@")
        myscreen.refresh()
    
def printSnake():
    for i in range(0, len(snake)):
        myscreen.addstr(snake[i].getY(), snake[i].getX(), snake[i].getBodypart(), curses.color_pair(1))
    myscreen.refresh()
    
def bfs():
    global targetx
    global targety 
    initAdjacency()   
    for row in range(1, height - 1):
        for col in range(1, width - 1):
#             if (Body(col, row) in snake) == True:
#                 bfsmap[row][col] = BfsElement("black", col, row, None, None, None, None, -1)
#             else:
            bfsmap[row][col] = BfsElement("white", col, row, None, None, None, None, -1)
    bfsmap[snake[0].getY()][snake[0].getX()].setColor("gray") 
    bfsmap[snake[0].getY()][snake[0].getX()].setDistance(0)
    queue = []
    queue.append(bfsmap[snake[0].getY()][snake[0].getX()])
    
    while len(queue) != 0:
        u = queue[0]
        if map[u.getSelfY()][u.getSelfX()].getBodypart() == "@":
            targetx = u.getSelfX()
            targety = u.getSelfY()
            break
        queue.remove(queue[0])
        for i in range(0, len(adjacency[u.getSelfY()][u.getSelfX()])):
            x = adjacency[u.getSelfY()][u.getSelfX()][i].getX()
            y = adjacency[u.getSelfY()][u.getSelfX()][i].getY()
            if bfsmap[y][x].getColor() == "white":
                bfsmap[y][x].setColor("gray")
                bfsmap[y][x].setDistance(u.getDistance() + 1) 
                bfsmap[y][x].setParentX(u.getSelfX())
                bfsmap[y][x].setParentY(u.getSelfY())
                queue.append(bfsmap[y][x])
            u.setColor("black")
    x = targetx
    y = targety   
#     print(str(y) + " " + str(x))
#     print(str(snake[0].getY()) + " " + str(x) + " " + str(bfsmap[snake[0].getY()][x].getParentY()) + " " + str(bfsmap[snake[0].getY()][x].getParentX()))    
    while (x == snake[0].getX() and y == snake[0].getY()) == False:

#         print(str(1) + " " + str(y) + " " + str(x) + " " + str(bfsmap[y][x].getChildY()) + " " + str(bfsmap[y][x].getChildX()) + " " + str(bfsmap[y][x].getParentY()) + " " + str(bfsmap[y][x].getParentX())) 
        bfsmap[bfsmap[y][x].getParentY()][bfsmap[y][x].getParentX()].setChildX(x)
        bfsmap[bfsmap[y][x].getParentY()][bfsmap[y][x].getParentX()].setChildY(y)
#         print(str(2) + " " + str(y) + " " + str(x) + " " + str(bfsmap[y][x].getChildY()) + " " + str(bfsmap[y][x].getChildX()) + " " + str(bfsmap[y][x].getParentY()) + " " + str(bfsmap[y][x].getParentX())) 
        tempY = y
        tempX = x
        y = bfsmap[tempY][tempX].getParentY()
#         print(str(3) + " " + str(y) + " " + str(x) + " " + str(bfsmap[y][x].getChildY()) + " " + str(bfsmap[y][x].getChildX()) + " " + str(bfsmap[y][x].getParentY()) + " " + str(bfsmap[y][x].getParentX())) 
        x = bfsmap[tempY][tempX].getParentX()
#         print(str(4) + " " + str(y) + " " + str(x) + " " + str(bfsmap[y][x].getChildY()) + " " + str(bfsmap[y][x].getChildX()) + " " + str(bfsmap[y][x].getParentY()) + " " + str(bfsmap[y][x].getParentX())) 
#         myscreen.getch()
#     print(str(bfsmap[snake[0].getY()][snake[0].getX() - 1].getChildY()) + " " + str(bfsmap[snake[0].getY()][snake[0].getX() - 1].getChildX()))
        
def getTarget():   
    global count
    while (snake[0].getX() == targetx and snake[0].getY() == targety) == False:
        for part in range(0, len(snake)):                                       
            if part == 0:
                previousX = snake[part].getX()
                previousY = snake[part].getY()
                snake[part].setX(bfsmap[previousY][previousX].getChildX())
                snake[part].setY(bfsmap[previousY][previousX].getChildY())
            elif part == 1:
                previous = bodyMove(previousX, previousY, part)
            else:
                previous = bodyMove(previous[0], previous[1], part)
#             print(str(snake[part].getY()) + " " + str(snake[part].getX()))
#             myscreen.getch()
            myscreen.addstr(snake[part].getY(), snake[part].getX(), snake[part].getBodypart(), curses.color_pair(1))
        if targetx == snake[0].getX() and targety == snake[0].getY():
            snake.append(Body(previous[0], previous[1]))
            count += 1
            map[targety][targetx].setBodypart(" ")
            myscreen.addstr(0, 12, str(count))
            myscreen.addstr(previous[1], previous[0], Body.getBodypart(), curses.color_pair(1)) 
        else:
            myscreen.addstr(previous[1], previous[0], " ") 
        myscreen.refresh()
#         myscreen.getch()
        curses.delay_output(50)   
        
'''    if targetx >= snake[0].getX() and targety >= snake[0].getY():
        while targety > snake[0].getY():
            move("d")
        while targetx > snake[0].getX():
            move("r")  
    elif targetx <= snake[0].getX() and targety <= snake[0].getY():
        while targety < snake[0].getY():
            move("u")
        while targetx < snake[0].getX():
            move("l") 
    elif targetx > snake[0].getX() and targety < snake[0].getY():
        while targety < snake[0].getY():
            move("u")
        while targetx > snake[0].getX():
            move("r")      
    elif targetx < snake[0].getX() and targety > snake[0].getY():
        while targety > snake[0].getY():
            move("d")
        while targetx < snake[0].getX():
            move("l")'''

def move(direction):
    global count
    for part in range(0, len(snake)):                                       
        if part == 0:
            previousX = snake[part].getX()
            previousY = snake[part].getY()
            headMove(direction)
        elif part == 1:
            previous = bodyMove(previousX, previousY, part)
        else:
            previous = bodyMove(previous[0], previous[1], part)
        myscreen.addstr(snake[part].getY(), snake[part].getX(), snake[part].getBodypart(), curses.color_pair(1))
    if targetx == snake[0].getX() and targety == snake[0].getY():
        snake.append(Body(previous[0], previous[1]))
        count += 1
        map[targety][targetx].setBodypart(" ")
        myscreen.addstr(0, 12, str(count))
        myscreen.addstr(previous[1], previous[0], Body.getBodypart(), curses.color_pair(1)) 
    else:
        myscreen.addstr(previous[1], previous[0], " ") 
    myscreen.refresh()
#     myscreen.getch()
    curses.delay_output(50)        
    
    
        
def headMove(direction):
    if direction == "r":    
        snake[0].setX(snake[0].getX() + 1) 
    elif direction == "l":    
        snake[0].setX(snake[0].getX() - 1) 
    elif direction == "u":    
        snake[0].setY(snake[0].getY() - 1)
    elif direction == "d":
        snake[0].setY(snake[0].getY() + 1)
    else:
        print("Invalid direction!")
        
def bodyMove(previousX, previousY, part):
    tempX = snake[part].getX()
    tempY = snake[part].getY()
    snake[part].setX(previousX)
    snake[part].setY(previousY)
    previousX = tempX
    previousY = tempY
    previous = [previousX, previousY]
    return previous 

def play():
    while count + 3 <= (height - 2) * (width - 2):
        makeTarget()
        bfs()
        getTarget()
#         myscreen.getch()                  
 
def main():
    makeScreen() 
    init()  
    initAdjacency() 
    printSnake()
    play()
    myscreen.getch()
    curses.endwin()
    
main()