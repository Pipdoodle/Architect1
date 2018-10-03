from numpy import *
from math import *
import pygame
class Vector(object):
    def __init__(self,x1,y1,z1,x0=0,y0=0,z0=0):
        self.x0=x0
        self.y0=y0
        self.z0=z0
        self.x1=x1
        self.y1=y1
        self.z1=z1
        self.vecValue=[self.x0-self.x1,self.y0-self.z1,self.z0-self.z1]
        
    def drawVector(self,screen):
        pygame.draw.line(screen,(255,0,255),(self.x0,self.y0),(self.x1,self.y1),1)
        
    def addVector(self,other):
        if isinstance(other,Vector):
            return Vector(self.x+other.x,self.y+other.y,self.z+other.z)
        return None
    
    def subtractVector(self,other):
        if isinstance(other,Vector):
            return Vector(self.x-other.x,self.y-other.y,self.z-other.z)
        return None
        
    def rotateVectorXY(self,thta):
        rotMat=matrix([math.cos(thta),-math.sin(thta),0],[math.sin(thta),math.cos(thta),0],[0,0,1])
        sel.vecValue=rotMat*matrix[self.vecValue]
    
    def rotateVectorYZ(self,theta):
        rotMat=matrix([1,0,0],[0,math.cos(theta),-math.sin(theta)],[0, math.sin(theta),math.cos(theta)])
        sel.vecValue=rotMat*matrix[self.vecValue]
    
        
    def rotateVectorXZ(self,theta):
        rotMat-matrix([math.cos(theta),0,math.sin(theta)],[0,1,0],[-math.sin(theta),0,math.cos(theta)])
        sel.vecValue=rotMat*matrix[self.vecValue]
    
    def scaleVector(self,scaleFac):
        scalMat=[[scaleFac[0],0,0],[0,scaleFac[1],0],[0,0,scaleFac[2]]]
        sel.vecValue=scalMat*matrix[self.vecValue]