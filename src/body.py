'''
Created on 2013-5-24

@author: shaosh
'''

class Position:
    bodypart = " "
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y 
        
    def getBodypart(self):
        return self.bodypart
    
    def setBodypart(self, bodypart):
        self.bodypart = bodypart

class Body(Position):
    bodypart = "+"
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def getBodypart():
        return Body.bodypart
    getBodypart = staticmethod(getBodypart)
#     def getX(self):
#         return self.x
#     
#     def getY(self):
#         return self.y
    
    
    
#     def setX(self, x):
#         self.x = x
#     
#     def setY(self, y):
#         self.y = y 

class Target(Position):
    bodypart = "@"
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class BfsElement:
    def __init__(self, color, selfX, selfY, parentX, parentY, distance):
        self.color = color
        self.selfX = selfX
        self.selfY = selfY
        self.parentX = parentX
        self.parentY = parentY
        self.distance = distance
        
    def setColor(self, color):
        self.color = color
    
    def getColor(self):
        return self.color
    
    def setSelfX(self, selfX):
        self.selfX = selfX
     
    def getSelfX(self):
        return self.selfX
     
    def setSelfY(self, selfY):
        self.selfY = selfY
     
    def getSelfY(self):
        return self.selfY
    
    def setParentX(self, x):
        self.parentX = x
    
    def getParentX(self):
        return self.parentX
    
    def setParentY(self, y):
        self.parentY = y
            
    def getParentY(self):
        return self.parentY
    
    def setDistance(self, distance):
        self.distance = distance
    
    def getDistance(self):
        return self.distance