import pygame
import math
from objInRoomClass import objInRoom
class RoomClass(object):
    
    def __init__(self,width,height,file):
        self.width=width
        self.height=height
        self.board=[]
        self.textBoard=[]
        self.roomName=file
        self.tilews=self.width//20
        self.tilehs=self.height//15
        temp=parseFile((readFile("SurfaceWorld\\Rooms\\"+file+".txt")))
        self.special="customer"
        self.objects=[]
        try:
            self.background=pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Images\\"+file+".png").convert_alpha(),(1200,700)), 0) 
        except:
            self.background=pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Images\\"+"Outside"+".png").convert_alpha(),(1200,700)), 0) 
        for object in temp:
            print(object)
            self.objects.append(objInRoom(object[0],int(object[1]),int(object[2]),int(object[3]),int(object[4]),int(object[5])))
        for object in self.objects:
            if "Exit" in object.actions[0]:
                self.exit1=int(object.actions[0][object.actions[0].index("Exit")+1])
                self.exit2=int(object.actions[0][object.actions[0].index("Exit")+2])
                self.exitCoord=(self.exit1,self.exit2)
                
    def drawRoom(self,screen):
        screen.blit(self.background,(0,0))        
        for object in self.objects:
            object.draw(screen)
            
#get all objects in room
def parseFile(str):
    itemList=[]
    str=str.splitlines()
    for item in str:
        item=item.split(":")
        itemList.append(item)
    return itemList

#taken from notes
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
                
    
    

    