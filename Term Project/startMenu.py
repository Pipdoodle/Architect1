
import os.path
import pygame
from ButtonClass import Button
class startMenu(object):
    
    @staticmethod
    def init():
        startMenu.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('Images\\menuImage.png').convert_alpha(),
            (1200,750)), 0)
        startMenu.crackImage=pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load("Images\\crack.png").convert_alpha(),(300,50)),45)
    
    def __init__(self,width,height):
        self.width=width
        self.height=height
        red=(255,165,79)
        info=readFile("SurfaceWorld\\Cracks.txt")
        info=info.splitlines()
        self.cracks=[]
        for item in info:
            new=item.split(",")
            self.cracks.append([int(new[0]),int(new[1])])
        buttonStart=Button(red,self.width/2-200,400,400,50,"Play","mainGame",150 )
        self.buttonList=[buttonStart]
        
    def startMouseMotion(self,x,y):
        for buttons in self.buttonList:
            buttons.mouseMotion(x,y)
                    
    def startMousePressed(self,x,y):
        for buttons in self.buttonList:
            if buttons.buttonPressed(x,y):
                if buttons.text=="New Game":
                    pass
                return buttons.returnMode()
        for crack in self.cracks:
            if x>=crack[0] and x<=crack[0]+300:
                if y>=crack[1] and y<=crack[1]+100:
                    return "world"
        return None
                
    def drawScreen(self,screen):
        screen.blit(self.image,(0,0))
        for crack in self.cracks:
            screen.blit(startMenu.crackImage,(crack[0],crack[1]))
        for i in range(len(self.buttonList)):
            self.buttonList[i].drawButton(screen)
        font=pygame.font.SysFont("pristina",100,bold=True)
        text="Architect"
        surf=font.render(text,False,(255,255,255))
        screen.blit(surf,(450,100))
        
#Taken from class notes        
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
        
#Taken from class notes
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)