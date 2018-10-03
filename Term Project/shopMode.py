import pygame
import pyaudio
import speech_recognition as sr
import sys  
sys.path.append("SurfaceWorld")  

import mainGameClass 
from mainSubGameClass import SubGameClass

import threading
from ButtonClass import *

import math
import copy
import NPC


#barebone from pygame guide
class shopMode(object):
    def __init__(self,width,height,person):
        self.name=person
        stockItems=readFile("SurfaceWorld\\Character\\"+person+"\\Inventory.txt")
        playerInv=readFile("SurfaceWorld\\PlayerStats\\Inventory.txt")
        ownerInfo=readFile("SurfaceWorld\\Character\\"+person+"\\Information.txt")
        ownerInfo=ownerInfo.splitlines()
        for line in ownerInfo:
            if line.startswith("downImage:"):
                self.image=pygame.transform.rotate(pygame.transform.scale(
                    pygame.image.load(line[10:]).convert_alpha(),
                    (600,500)), 0) 
        self.playerInv={}
        self.playerInv=self.parseInventory(playerInv)
        self.buttonWidth=width//2-30
        self.buttonHeight=100
        self.width=width
        self.height=height
        self.stockItems=self.fileParseInventory(stockItems)
        self.stockButton=[]
        i=0
        for item in self.stockItems:
            button=Button((220,160,160),width//2+5,self.buttonHeight*i,self.buttonWidth,
            self.buttonHeight,item,item,255,"Cost: "+str(self.stockItems[item][0])+ 
            " Amount: "+str(self.stockItems[item][1]))
            self.stockButton.append(button)
            i+=1
        self.checkSetScroll()
        self.scrollY=None
        self.scrollX=None
        self.boxWidth=100
        self.boxHeight=100
        self.margin=20
        self.buttonInv=[]
        i=0
        for item in self.playerInv:
            x=self.margin+i*(self.boxWidth+self.margin)
            self.buttonInv.append(Button((100,100,100),x,550,self.boxWidth,
            self.boxHeight,item,item,255,"Amount: "+str(self.playerInv[item])))
            i+=1
        self.checkSetScrollX()
        self.displayText=None
            
    #checks and sets length of scroll side
    def checkSetScroll(self):
        if len(self.stockItems)*self.buttonHeight>500:
            self.lenyScroll=500/((len(self.stockItems)*self.buttonHeight-500)/self.buttonHeight)
            self.yScroll=scrollBar((255,244,244),self.width-20,0,20,self.lenyScroll,None,None,5,500)
        else:
            self.yScroll=None
            self.scrollY=None
    
    #checks and sets length of place of scroll bottom
    def checkSetScrollX(self):
        if len(self.playerInv)*(self.boxWidth+self.margin)>self.width:
            totBox=self.boxWidth+self.margin
            self.lenBar=self.width/((len(self.playerInv)*totBox-self.width)/totBox)
            self.xScroll=scrollBar((255,244,244),0,self.height-self.margin,
            self.lenBar,self.margin,None,None,self.width,10)
        else:
            self.xScroll=None
            self.scrollX=None
 
    def mousePressed(self, x, y):
        removed=None
        if self.scrollX!=None:
            x=x+self.scrollX
        if self.scrollY!=None:
            y=y+self.scrollY
        for button in self.stockButton:
            if button.buttonPressed(x,y):
                #checks enough money buy things
                if self.playerInv.get("Money",0)>self.stockItems[button.mode][0]:
                    self.displayText=button.mode+" bought!"
                    self.playerInv[button.mode]=self.playerInv.get(button.mode,0)+1
                    self.playerInv["Money"]-=self.stockItems[button.mode][0]
                    self.stockItems[button.mode][1]-=1
                    if self.stockItems[button.mode][1]<=0:
                        removed=button
                    if self.playerInv[button.mode]==1:
                        self.buttonInv.append(Button((100,100,100),self.margin+
                        (len(self.playerInv)-1)*(self.boxWidth+self.margin),
                        550,self.boxWidth,self.boxHeight,button.mode,button.mode))
                    #changes amount after item bought
                    button.text2="Cost: "+str(self.stockItems[button.mode][0])+\
                    " Amount: "+str(self.stockItems[button.mode][1])
                    self.checkSetScrollX()
                    self.updateInvValues()
                else:
                    self.displayText="You don't have enough money for that!"
            #moves buttons if something removed
            if removed!=None:
                button.yS-=self.buttonHeight   
        #takes out button if stock runs out
        if removed!=None:
            self.stockButton.remove(removed)
            del self.stockItems[removed.mode]
            self.checkSetScroll()
            
    def updateInvValues(self):
        for button in self.buttonInv:
            button.text2="Amount: "+str(self.playerInv[button.mode])
  
    def mouseMotion(self, x, y):
        for buttons in self.stockButton:
            if self.scrollY!=None:
                buttons.mouseMotion(x,y+self.scrollY)
            else:
                buttons.mouseMotion(x,y)
        for buttons in self.buttonInv:
            if self.scrollX!=None:
                buttons.mouseMotion(x+self.scrollX,y)
            else:
                buttons.mouseMotion(x,y)

    def mouseDrag(self, x, y):
        #checks if in the range of scroll bar side
        if self.yScroll!=None:
            if x>=self.yScroll.xS and y<=500:
                self.yScroll.move(None,y)
                itBy=self.lenyScroll/self.buttonHeight
                diff=y-self.lenyScroll
                self.scrollY=self.lenyScroll+diff
        #checks if in range of scroll bar bottom
        if self.xScroll!=None:
            if y>=self.height-self.margin:
                self.xScroll.move(x,None)
                itBy=self.lenBar/self.buttonHeight
                diff=x-self.lenBar
                self.scrollX=self.lenBar+diff
        
    def keyPressed(self, keyCode, modifier):
        if keyCode==pygame.K_ESCAPE:
            self.writeFile()
            mainGameClass.GameClass.mode="Game"
        return "mainGame"

    def redrawAll(self, screen):
        #draw background for buttons of shopMenu
        pygame.draw.rect(screen,(220,200,200),
        (self.width//2,0,self.width//2,500))
        #goes through shop buttons
        for button in self.stockButton:
            if self.scrollY!=None:
                if button.yS-self.scrollY<500:
                    button.drawButton(screen,y=self.scrollY)
            else:
                if button.yS<401:
                    button.drawButton(screen,y=self.scrollY)
        #draw up down scroll bar
        if self.yScroll!=None:
            self.yScroll.drawButton(screen)
        #draw inventory background
        pygame.draw.rect(screen,(220,200,200),(0,500,1200,200))
        #draws all items in inventory
        for button in self.buttonInv:
            button.drawButton(screen,x=self.scrollX)
            if self.xScroll!=None:
                self.xScroll.drawButton(screen)
        #draw shopkeeper
        screen.blit(self.image,(0,0))
        #draws messages
        if self.displayText!=None:
            font=pygame.font.SysFont("Georgia",30,bold=True)
            surf=font.render(self.displayText,False,(0,0,0))
            screen.blit(surf,(100,500)) 
            
    #splits inventory of shopkeeper in item, price, amount    
    def fileParseInventory(self,stockItems):
        contents=stockItems.splitlines()
        stockItems={}
        for line in contents:
            stuff=line.split(":")
            stockItems[stuff[0]]=[int(stuff[1]),int(stuff[2])]
        return stockItems
    
    #goes through file and splits the objects owned    
    def parseInventory(self,contents):
        contents=contents.splitlines()
        invDict={}
        for item in contents:
            if item.startswith("Build:"):
                item=item.split(":")
                invDict[item[1]]=int(item[2])
            elif item.startswith("Money:"):
                item=item.split(":")
                invDict[item[0]]=int(item[1])
        return invDict
    
    #barebone taken file course notes
    #writes to the inventory the new information after buing items
    def writeFile(self):
        path="SurfaceWorld\\PlayerStats\\Inventory.txt"
        contents=""
        for item in self.playerInv:
            if item!="Money":
                contents+="Build:%s:%d \n"%(str(item),self.playerInv[item])
            else:
                contents+="Money:%d \n"%(int(self.playerInv[item]))
        with open(path, "wt") as f:
            f.write(contents)
        #records for the character that you bought from new inventory
        path="SurfaceWorld\\Character\\"+self.name+"\\Inventory.txt"
        contents=""
        for item in self.stockItems:
            contents+="%s:%d:%d\n"%(str(item),self.stockItems[item][0],
            self.stockItems[item][1])
        with open(path, "wt") as f:
            f.write(contents)
                
    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)
        
 #taken from class notes   
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
