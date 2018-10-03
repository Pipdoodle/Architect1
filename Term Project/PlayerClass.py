from GameObject import GameObject
import pygame
import RoomClass
import mainGameClass
from shopMode import shopMode
from buildMode import buildMode 
class player(GameObject):
    @staticmethod
    def init():
        player.upSprite=pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images\\upCharacter.png').convert_alpha(),
            (70,95)), 0) 
        player.downSprite=pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images\\downCharacter.png').convert_alpha(),
            (70,95)), 0) 
        player.leftSprite=pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images\\leftCharacter.png').convert_alpha(),
            (70,95)), 0) 
        player.rightSprite=pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images\\rightCharacter.png').convert_alpha(),
            (70,95)), 0) 
    
    def __init__(self,width,height,x,y,room):
        self.object,self.object1=None,None
        super(player, self).__init__(x,y,player.downSprite,50)
        self.image=player.downSprite
        self.speed=10
        self.room=room
        self.name="player"
        self.roomName=room.roomName
        self.up1,self.up=True,True
        self.down,self.down1=True,True
        self.right,self.right1=True,True
        self.left,self.left1=True,True
        self.dir="down"
        self.screenWidth=width
        self.status="player"
        self.screenHeight=height
                
    def update(self,isKeyPressed,width,height):
        if isKeyPressed(pygame.K_LEFT):
            if self.left1==True and self.left==True:
                self.dir="Left"
                self.x-=self.speed
                self.image=player.leftSprite
        elif isKeyPressed(pygame.K_RIGHT):
            if self.right==True and self.right1==True:
                self.dir="Right"
                self.x+=self.speed
                self.image=player.rightSprite
        elif isKeyPressed(pygame.K_DOWN):
            if self.down==True and self.down1==True:
                self.dir="Down"
                self.y+=self.speed
                self.image=player.downSprite
        elif isKeyPressed(pygame.K_UP):
            if self.up==True and self.up1==True:
                self.dir="Up"
                self.y-=self.speed
                self.image=player.upSprite
        super(player, self).update(width,height)
   
    def keyPressed(self, keyCode, modifier):        
        if keyCode==pygame.K_RETURN:
            if self.object!=None:
                self.processAction(self.object)
            elif self.object1!=None:
                self.processAction(self.object1)
                
    def processAction(self,object):
        type,something=object.action(False,"player")
        if type=="dialogue":
            mainGameClass.GameClass.displayText=something
        elif type=="move":
            mainGameClass.GameClass.room=something
        elif type=="shop":
            mainGameClass.GameClass.mode="shop"
            mainGameClass.GameClass.shop=shopMode(self.screenWidth,self.screenHeight,something)
        elif type=="buildMode":
            mainGameClass.GameClass.mode="buildMode"
            mainGameClass.GameClass.buildmode=buildMode(self.screenWidth,self.screenHeight)
                              
    def changePlayerRoom(self,room):
        self.room=room
        self.roomName=room.roomName
    
        
            
        
        
    
            
 