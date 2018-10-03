
import os.path
import pygame
from ButtonClass import Button
import PlayerClass
import audioPlayerCkass 
import RoomClass
import threading
class SubGameClass (object):
    value=0
    
    def init():
      
        SubGameClass.background=pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images\\forest2.png').convert_alpha(),
            (1200,700)),0)
        SubGameClass.dot=pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images\\dot3.png').convert_alpha(),
            (100,100)),0)
        
        pass
            
    def __init__(self,width,height):
        self.stream=audioPlayerCkass.playSound("Audio\\Violet.wav")
        self.mouseX=0
        self.mouseY=0
        subThread=threading.Thread(target=audioPlayerCkass.record,args=("audiorecordtest.txt",))
        subThread.daemon=True
        subThread.start()
        self.width=width
        self.height=height
        self.room=RoomClass.RoomClass(width,height,"bedroom")
        PlayerClass.player.init()
        self.player=PlayerClass.player(width,height,400,400,self.room)
        self.num=0
        self.playerGroup=pygame.sprite.GroupSingle(self.player)
        self.background=SubGameClass.background
        self.dot=SubGameClass.dot
        self.textStream=[["Hello?",3],["Is anyone there?",6],
        ["I'll be good I promise!",2],["Don't leave me!",2],
        ["Please",10],["In the end I guess I'm always alone.",4],
        ["What did I do so wrong to deserve this?",3],["I'm sorry",15]]
        self.timer=0
        self.text=self.textStream[self.num][0]
        
    def keyPressed(self, keyCode, modifier):
        possMode=self.player.keyPressed(keyCode,modifier)
        if keyCode==pygame.K_ESCAPE:
            return "start"
        if possMode!=None:
            return possMode
        return "world"
        
    def mouseMotion(self,x,y):
        self.mouseX=x
        self.mouseY=y
    
    def drawScreen(self,screen,filter):
        filter.fill((255-SubGameClass.value,255-SubGameClass.value,255-SubGameClass.value))
        if SubGameClass.value!=0:
            scale=self.value/10
            self.dot=pygame.transform.rotate(pygame.transform.scale(
                        pygame.image.load('Images\\dot3.png').convert_alpha(),
                        (int(100*scale),int(100*scale))),0)
            filter.blit(self.dot,(self.player.x-int(100*scale/2),self.player.y-int(100*scale/2)))
           
            #pygame.transform.scale(filter,(100*scale,100*scale))
           
        screen.blit(self.background,(0,0))
        screen.blit(filter,(0,0),special_flags=pygame.BLEND_RGBA_SUB)

        font=pygame.font.SysFont("pristina",30,bold=True)
        text=str(self.text)
        surf=font.render(text,False,(210,210,210))
        i=len(self.textStream)//2
        xblit,yblit=450,50
        if self.num+1<i:
            xblit+=50*(self.num+1)
        else:
            xblit-=50*(self.num+1)
        yblit+=50*self.num
        screen.blit(surf,(xblit,yblit))
        
    def timerFired(self,dt,isKeyPressed):
        self.playerGroup.update(isKeyPressed,self.width,self.height)
        self.timer+=1
        if self.timer==self.textStream[self.num][1]*100:
            self.num+=1
            self.timer=0
            self.text=self.textStream[self.num][0]
        if self.num==len(self.textStream)-1:
            return "start"
        return "mainGame"
       