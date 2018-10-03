from Vector import Vector
class Point(object):
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
        self.pointValue=(x,y,z)
        
        
    def drawPoint(self):
       print(self.pointValue)
        
    def AddVector(self,vector):
        if isinstance(vector,Vector):
            return Point(self.x+other.x,self.y+other.y,self.z+other.z)
    
    def SubtractVector(self,vector):
        if isinstance(vector,Vector):
            return Point(self.x-other.x,self.y-other.y,self.z-other.z)
    
    def createVector(self,other):
        if ininstance(other,Point):
            return Vector(self.x-other.x,self.y-other.y,self.z-other.z)
    

        
        
        