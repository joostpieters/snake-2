'''
Created on 2013-5-24
Version 1.0
1. Move right and down is completed. 
2. Need to combine and eliminate the repeated codes 
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
height = 20
width = 60
# map = [[0] * (width - 1)] * (height - 1)
map = [[0 for col in range(width -1)] for row in range(height - 1)]
queue = []
# bfsmap = [[0] * (width - 1)] * (height - 1)
bfsmap = [[0 for col in range(width -1)] for row in range(height - 1)]
# adjacency = [[[]] * (width - 1)] * (height - 1)
adjacency = [[[] for col in range(width -1)] for row in range(height - 1)]
targetx = 0
targety = 0

def makeScreen():
    global myscreen 
    global snake
    global count
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
    global adjacency
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            pos = Position(col, row)
#             map.append(pos)
#             print(str(row) + " " + str(col))
            map[row][col] = pos
            map[row][col].setX(col)
            map[row][col].setY(row)
#             print(str(row) + " " + str(col) + " " + str(map[1][1].getY()) + " " + str(map[1][1].getX()))           
            myscreen.addstr(row, col, pos.getBodypart())
#         myscreen.getch()
    myscreen.refresh()
    
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
#     myscreen.addstr(5, 1, str(target.getY()))
#     myscreen.addstr(5, 10, str(target.getX()))
    while availalbe == False:
        if (Body(target.getX(), target.getY()) in snake) == False:
            availalbe = True
        else:
            target = Target(random.randint(1, width - 2), random.randint(1, height - 2))
    else:
        myscreen.addstr(target.getY(), target.getX(), target.getBodypart(), curses.color_pair(2))
#         map[(width - 2) * (target.getY() - 1) + target.getX()].setBodypart("@")
        map[target.getY()][target.getX()].setBodypart("@")
        myscreen.refresh()
    
def printSnake():
    for i in range(0, len(snake)):
        myscreen.addstr(snake[i].getY(), snake[i].getX(), snake[i].getBodypart(), curses.color_pair(1))
    myscreen.refresh()
    
def bfs():
    global targetx
    global targety
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            bfsmap[row][col] = BfsElement("white", col, row, None, None, -1)
#             print(str(row) + " " + str(col) + " " + str(bfsmap[1][1].getSelfY()) + " " + str(bfsmap[1][1].getSelfX()))
#             myscreen.getch()

    
#     myscreen.addstr(14, 1, str(bfsmap[1][3].getSelfY()))
#     myscreen.addstr(14, 10, str(bfsmap[1][3].getSelfX()))
    bfsmap[snake[0].getY()][snake[0].getX()].setColor("gray") 
    bfsmap[snake[0].getY()][snake[0].getX()].setDistance(0)
#     myscreen.addstr(15, 1, str(snake[0].getY()))
#     myscreen.addstr(15, 10, str(snake[0].getX()))
#     myscreen.addstr(16, 1, str(bfsmap[snake[0].getY()][snake[0].getX()].getSelfY()))
#     myscreen.addstr(16, 10, str(bfsmap[snake[0].getY()][snake[0].getX()].getSelfX()))
#     myscreen.addstr(16, 20, str(bfsmap[snake[0].getY()][snake[0].getX()].getColor()))
#     myscreen.addstr(16, 30, str(bfsmap[snake[0].getY()][snake[0].getX()].getDistance()))
#     myscreen.addstr(17, 1, str(bfsmap[snake[1].getY()][snake[1].getX()].getSelfY()))
#     myscreen.addstr(17, 10, str(bfsmap[snake[1].getY()][snake[1].getX()].getSelfX()))
#     myscreen.addstr(17, 20, str(bfsmap[snake[1].getY()][snake[1].getX()].getColor()))
#     myscreen.addstr(17, 30, str(bfsmap[snake[1].getY()][snake[1].getX()].getDistance()))
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
            
#     myscreen.addstr(5, 1, str(targety))
#     myscreen.addstr(5, 10, str(targetx))
#     print(map[targety][targetx].getBodypart())
        
def getTarget():
#     myscreen.addstr(9, 1, str(targety))
#     myscreen.addstr(9, 10, str(targetx))
    
    if targetx > snake[0].getX() and targety > snake[0].getY():
        if snake[0].getX() >= snake[1].getX():
            while targetx > snake[0].getX():
                for part in range(0, len(snake)):                                       
                    if part == 0:
                        previousX = snake[part].getX()
                        previousY = snake[part].getY()
                        snake[part].setX(snake[part].getX() + 1)
                    elif part == 1:
                        previous = restMove(previousX, previousY, part)
                    else:
                        previous = restMove(previous[0], previous[1], part)
                    myscreen.addstr(snake[part].getY(), snake[part].getX(), snake[part].getBodypart(), curses.color_pair(1))
                myscreen.addstr(previous[1], previous[0], " ") 
                myscreen.refresh()
                curses.delay_output(50)
            while targety > snake[0].getY():
                for part in range(0, len(snake)):                    
                    if part == 0:
                        previousX = snake[part].getX()
                        previousY = snake[part].getY()
                        snake[part].setY(snake[part].getY() + 1)
                    elif part == 1:
                        previous = restMove(previousX, previousY, part)
                    else:
                        previous = restMove(previous[0], previous[1], part)
                    myscreen.addstr(snake[part].getY(), snake[part].getX(), snake[part].getBodypart(), curses.color_pair(1))
                if targety > snake[0].getY():
                    myscreen.addstr(previous[1], previous[0], " ") 
                else:
                    snake.append(Body(previous[0], previous[1]))
                    myscreen.addstr(previous[1], previous[0], Body.getBodypart(), curses.color_pair(1)) 
                myscreen.refresh()
                curses.delay_output(50)
            
                        
                        
#         if snake[0].getX() < snake[1].getX():
#             while targety > snake[0].getY():
                
        

#         while targetx > snake[0].getX():
#             for part in range(0, len(snake)):
#                snake[part].setX(snake[part].getX() + 1)
#                myscreen.addstr(snake[part].getY(), snake[part].getX(), snake[part].getBodypart(), curses.color_pair(1))
#             myscreen.addstr(snake[len(snake) - 1].getY(), snake[len(snake) - 1].getX() - 1, " ") 
#             myscreen.refresh()
#             curses.delay_output(50)
        
#     elif targetx > snake[0].getX() and targety < snake[0].getY(): 
#     
#     elif targetx < snake[0].getX() and targety > snake[0].getY():
#         
#     else:
                 

'''def printTarget(target):
    myscreen.addstr(target.getX(), target.getY(), target.getBodypart())
    myscreen.refresh()
'''    

'''
myscreen.refresh()
myscreen.getch()'''
def restMove(previousX, previousY, part):
    tempX = snake[part].getX()
    tempY = snake[part].getY()
    snake[part].setX(previousX)
    snake[part].setY(previousY)
    previousX = tempX
    previousY = tempY
    previous = [previousX, previousY]
    return previous                   
 
def main():
    makeScreen() 
    init()   
    printSnake()
    makeTarget()
    bfs()
    getTarget()
    myscreen.getch()
    curses.endwin()
    
main()