import pygame
import pyaudio
import speech_recognition as sr
import sys  
sys.path.append("SurfaceWorld")  
from startMenu import startMenu
import mainGameClass 
from mainSubGameClass import SubGameClass
from audioPlayerCkass import micRecord1
import threading
from ButtonClass import *
from General3DObject import Cube
import math
import copy
import os
import random

#barebone from pygame guide
class buildMode(object):

    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.margin=10
        self.rotx=10313
        self.rotz=10313
        self.roty=10313
        self.boxSize=700
        self.boxWidth=100
        self.boxHeight=100
        self.currentPiece=None
        self.currentPieceX=5
        self.currentPieceY=5
        self.currentPieceZ=5
        self.pieces=[]
        brick=(132,31,39)
        wood=(130,82,1)
        door=(182,156,67)
        window=(135,206,250)
        self.allItemDict={"Brick":[[[brick,brick]],[[brick,brick]]],\
        "Wood":[[[wood],[wood]],[[wood],[wood]]],"Door":[[[door]]],\
        "Window":[[[window]]], \
        "Table":[[[wood]]],"Bed":[[[(233,15,50)]]],"FirePlace":[[[(255,0,0)]]],\
        "Roof":[[[(120,15,1)]]],"Steel":[[[(210,210,210)],[(210,210,210)]]],\
        "Glass": 
        [[[(135,206,250)]]],"Moss":[[[(95,105,7)]]],"Chocolate":[[[wood]]],\
        "Candy":[[[(255,20,147)]]],"Stone":[[[(210,210,210)]]]}
        self.boardSurface=pygame.Surface((self.width,self.height))
        self.items=self.parseInventory(readFile("SurfaceWorld\\PlayerStats\\Inventory.txt"))
        self.buttonList=[]
        self.exitButton=Button((100,100,100),20,20,self.boxWidth,self.boxHeight//2,"Exit","mainGame")
        i=0
        for item in self.items:
            x=self.margin+i*(self.boxWidth+self.margin)
            y=self.margin*2+self.height*(6/8)
            self.buttonList.append(Button((100,100,100),x,y,self.boxWidth,self.boxHeight,item,item,255,str(self.items[item])))
            i+=1
        self.scrollX=0
        self.scroll=None
        self.checkSetScrollX()
        self.board=[]
        for i in range(10):
            boardRow=[]
            for j in range(10):
                boardCol=[]
                for z in range(10):
                    boardCol.append("None")
                boardRow.append(boardCol)
            self.board.append(boardRow)
        self.board1=copy.deepcopy(self.board)
        self.boardSurface=pygame.Surface((self.width,self.height))
        self.drawBoard()
        self.money=None
    
    #checks and sets length of place of scroll bottom
    def checkSetScrollX(self):
        if len(self.items)*(self.boxWidth+self.margin)>self.width:
            totBox=self.boxWidth+self.margin
            self.lenBar=self.width/((len(self.items)*totBox-self.width)/totBox)
            self.scroll=scrollBar((255,244,244),0,self.height-self.margin,
            self.lenBar,self.margin,None,None,self.width,10)
        else:
            self.scrollX=0
            self.scroll=None
            
    def mousePressed(self, x, y,tasks):
        removed=None
        for button in self.buttonList:
            if button.buttonPressed(x,y):
                if self.currentPiece==None:
                    #sets to list of type of piece
                    self.currentPiece=self.allItemDict[button.mode]
                    self.pieces.append(button.mode)
                    self.movePiece(0,0,0)
                    self.drawBoard()
                    self.items[button.mode]-=1
                    if self.items[button.mode]<=0:
                        removed=button
            #moves box if something has been removed
            if removed!=None:
                button.xS-=self.boxWidth+self.margin
        #removes from inventory
        if removed!=None:
            self.buttonList.remove(removed)
            del self.items[removed.mode]
        self.checkSetScrollX()
        if self.exitButton.buttonPressed(x,y):
            task=self.evalBuild(tasks)
            if task!=None:
                tasks.remove(task)
                self.writeFile()
            return "mainGame",tasks
        return None,None

    def mouseMotion(self, x, y):
        for buttons in self.buttonList:
            buttons.mouseMotion(x+self.scrollX,y)
        self.exitButton.mouseMotion(x,y)

    def mouseDrag(self, x, y):
        if self.scroll!=None:
            if y>=self.scroll.yS:
                self.scroll.move(x,None)
                totBox=self.boxWidth+self.margin
                self.lenBar=self.width/((len(self.items)*totBox-self.width)/totBox)
                itBy=self.lenBar/totBox
                diff=x-self.lenBar
                self.scrollX=self.lenBar+diff
        if y<250:
            if x>self.width/2:
                self.roty+=10
            else:
                self.roty-=10
            self.drawBoard()
        elif y<400:
            if x>self.width/2:
                self.rotx+=10
            else:
                self.rotx-=10
            self.drawBoard()
        elif y<650:
            if x>self.width/2:
                self.rotz+=10
            else:
                self.rotz-=10
            self.drawBoard()
        
    def keyPressed(self, keyCode, modifier):
        if self.currentPiece!=None:
            #xdirection
            if keyCode==pygame.K_LEFT:
                self.movePiece(-1,0,0)
                self.drawBoard()
            if keyCode==pygame.K_RIGHT:
                self.movePiece(1,0,0)
                self.drawBoard()
            #ydirection
            if keyCode==pygame.K_UP:
                self.movePiece(0,1,0)
                self.drawBoard()
            if keyCode==pygame.K_DOWN:
                self.movePiece(0,-1,0)
                self.drawBoard()
            #zdirection
            if keyCode==pygame.K_w:
                self.movePiece(0,0,1)
                self.drawBoard()
            if keyCode==pygame.K_s:
                self.movePiece(0,0,-1)
                self.drawBoard()
            if keyCode==pygame.K_RETURN:
                if self.isValid():
                    self.board1=copy.deepcopy(self.board)                    
                    self.currentPiece=None
                    self.currentPieceX=0
                    self.currentPieceY=0
                    self.currentPieceZ=0
                    
    #checks for overlapping pieces                
    def isValid(self):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                for depth in range(len(self.board)):
                    if self.board[row][col][depth]==(100,100,100):
                        return False
        return True
        
    def timerFired(self,dt):
        pass

    def movePiece(self, dx,dy,dz):
        maxRow=max(len(row) for row in self.currentPiece)
        maxRow=0
        maxCol=0
        maxDepth=0
        #finds lengths
        for row in self.currentPiece:
            if maxRow<len(row):
                maxRow=len(row)
            for col in row:
                if len(col)>maxCol:
                    maxCol=len(col)
                for depth in col:
                    if not isinstance(depth,tuple):
                        depthLen=len(depth) 
                    else:
                        if not(isinstance(depth[0],int)):
                            depthLen=len(depth) 
                        else:
                            depthLen=1
                    if maxDepth<depthLen:
                        maxDepth=depthLen
        #boundcheck
        if self.currentPieceX+dx+(maxRow-1)<len(self.board)-1 and self.currentPieceX+dx>=0:
            self.currentPieceX+=dx
        if self.currentPieceY+dy+(maxCol-1)<len(self.board)-1 and self.currentPieceY+dy>=0:
            self.currentPieceY+=dy
        if self.currentPieceZ+dz+(maxDepth-1)<len(self.board)-1 and self.currentPieceZ+dz>=0:
            self.currentPieceZ+=dz
        self.board=copy.deepcopy(self.board1)
        cont=True
        for x in range(len(self.currentPiece)):
            for y in range(len(self.currentPiece[x])):
                for z in range(len(self.currentPiece[x][y])):
                    if self.board[self.currentPieceX+x][self.currentPieceY+y][self.currentPieceZ+z]!="None":
                        self.board[self.currentPieceX+x][self.currentPieceY+y][self.currentPieceZ+z]=(100,100,100)
                    else:
                        self.board[self.currentPieceX+x][self.currentPieceY+y][self.currentPieceZ+z]=self.currentPiece[x][y][z]
        
    def evalBuild(self,tasks):
        #checks if tasks is right
        tasks.sort()
        for task in tasks:
            task.sort()
            self.pieces.sort()
            if task==self.pieces:
                return task
        return None
        
    def processList(L):
        dictElems=dict()
        dictElems1=dict()
        list=[]
        list1=[]
        for item in L:
            if item[0] not in list:
                list.append[item]
            elif item[0] in list:
                som=tuple(list)
                dictElems[dictElems.get(som,0)]+=1
                list=[]
            if item[1] not in list1:
                list1.append[item]
            elif item[1] in list1:
                som1=tuple(list)
                dictElems1[dictElems1.get(som1,0)]+=1
                list1=[]
        return dictElems,dictElems1       
      
    def drawBoard(self):
        self.boardSurface=pygame.Surface((self.width,self.height))
        margin=20
        marginx=self.width/3
        width=40
        height=40
        cx=marginx+20*10
        cy=margin+20*10
        cz=margin+20*10
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                for depth in range(len(self.board)):
                    x=marginx+col*width
                    y=margin+row*height
                    z=margin+depth*width
                    self.cubeBoard=Cube(x,y,z,width,height,width)
                    color=self.board[row][col][depth]
                    self.cubeBoard.drawObject(self.boardSurface,0,0,0,math.radians(self.rotx),math.radians(self.roty),math.radians(self.rotz),cx,cy,cz,color)
  

    def redrawAll(self, screen):
        screen.blit(self.boardSurface,(0,0))
        pygame.draw.rect(screen,(255,231,97),(0,self.height*(6/8),self.width,self.height/4))
        for button in self.buttonList:
            button.drawButton(screen,x=self.scrollX)
        self.exitButton.drawButton(screen)
        if self.scroll!=None:
            self.scroll.drawButton(screen)

    #parse through inventory
    def parseInventory(self,contents):
        contents=contents.splitlines()
        invDict={}
        for item in contents:
            if item.startswith("Build:"):
                item=item.split(":")
                invDict[item[1]]=int(item[2])
            elif item.startswith("Money:"):
                item=item.split(":")
                self.money=int(item[1])
        return invDict
            
    #parse through all items
    def parseItem(self,itemStr):
         if itemStr=="Brick":
             color=(132,31,39)
             brickShape=[["True","True"],["True","True"]]
             return brickShape
        
    #barebone taken file course notes
    def writeFile(self):
        #writes to inventory new info
        path="SurfaceWorld\\PlayerStats\\Inventory.txt"
        contents=""
        for item in self.items:
            contents+="Build:%s:%d \n"%(str(item),self.items[item])
        if self.money==None:
            self.money=0
        contents+="Money:%d"%(self.money+1000)
        with open(path, "wt") as f:
            f.write(contents)
        path="SurfaceWorld\\Rooms\\"+mainGameClass.GameClass.room+".txt"
        contents=readFile(path)
        contents=contents.splitlines()
        for item in contents:
            #checks for first empt plot and sets that to a house
            if item.startswith("emptplot"):
                info=item.split(":")
                newItem=["house",info[1],info[2],info[3],info[4],info[5]]
                contents.remove(item)
                newContent="%s:%d:%d:%d:%d:%d \n"%(newItem[0],int(newItem[1]),int(newItem[2]),int(newItem[3]),int(newItem[4]),int(newItem[5]))
                break
        for newItem in contents:
            newItem=newItem.split(":")
            newContent+="%s:%d:%d:%d:%d:%d \n"%(newItem[0],int(newItem[1]),int(newItem[2]),int(newItem[3]),int(newItem[4]),int(newItem[5]))
        with open(path,"wt")as f:
            f.write(newContent)
        #add new area
        self.evalNewAreaNeeded()
    
    def evalNewAreaNeeded(self):
        room,num=self.findEmptyRoom()
        #num of new room
        num+=1
        RS,BT,TP,LS=True,True,True,True
        if room!=None:
            #number of original outside
            numo=int(room[7:-4])
            content=readFile("SurfaceWorld\\Rooms\\"+room)
            content=content.splitlines()
            for item in content:
                #check what side is open
                if "Door" in item:
                    cont=item.split(":")
                    if int(cont[1])>=1100:
                        RS=False
                    elif int(cont[2])>=650:
                        BT=False
                    elif int(cont[2])<=100:
                        TP=False
                    elif int(cont[1])<=100:
                        LS=False
            #makes random choice of direction 
            newDirec=False
            while newDirec!=True:
                newDirec=random.choice([RS,BT,TP,LS])
            if newDirec==RS:
                newContent=["DoorR"+str(num),1150,350,100,100,0]
            elif newDirec==LS:
                newContent=["DoorL"+str(num),0,350,50,100,0]
            elif newDirec==TP:
                newContent=["DoorT"+str(num),600,0,50,59,0]
            elif newDirec==BT:
                newContent=["DoorB"+str(num),600,680,50,50,0]
            totalContent=""
            for item in content:
                totalContent+=item+"\n"
            totalContent+="%s:%d:%d:%d:%d:%d \n"%(newContent[0],int(newContent[1]),int(newContent[2]),int(newContent[3]),int(newContent[4]),int(newContent[5]))
            #writes to the current room file and adds new door to new area
            with open("SurfaceWorld\\Rooms\\"+room,"wt+") as f:
                f.write(totalContent)
            #creates file for door
            info="Move\nOutside"+str(num)   
            with open("SurfaceWorld\\Text\\"+newContent[0]+".txt","wt+") as f:
                f.write(info)
            #create door for new room, opp of original
            if newDirec==RS:
                new=["DoorL"+str(numo),0,350,50,100,0]
            elif newDirec==LS:
                new=["DoorR"+str(numo),1150,350,100,100,0]
            elif newDirec==TP:
                new=["DoorB"+str(numo),600,680,50,50,0]
            elif newDirec==BT:
                new=["DoorT"+str(numo),600,0,50,59,0]
            totalContent="%s:%d:%d:%d:%d:%d\n"%(new[0],int(new[1]),int(new[2]),int(new[3]),int(new[4]),int(new[5]))
            totalContent+="%s:%d:%d:%d:%d:%d\n"%("emptplot",400,200,400,200,0)
            #create new room with new door
            with open("SurfaceWorld\\Rooms\\Outside"+str(num)+".txt","wt+") as f:
                f.write(totalContent)
            info="Move\nOutside"+str(numo)
            with open("SurfaceWorld\\Text\\"+new[0]+".txt","wt+") as f:
                f.write(info)

    def findEmptyRoom(self):
        #checks for the first empty outside area that has room to add rooms
        path="SurfaceWorld\\Rooms"
        numOfOutsides=-1
        found=False
        file=None
        for filename in os.listdir(path):
            if "Outside" in filename:
                numOfOutsides+=1
                content=readFile((path + "/" + filename))
                content=content.splitlines()
                i=0
                for item in content:
                    if "Door" in item:
                        i+=1
                if i<4:
                    if found==False:
                        file=filename
                        found=True
        return file,numOfOutsides
        
            
        
    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)
    

#taken from class notes
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
        
