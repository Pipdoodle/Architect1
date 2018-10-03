
import os.path
import pygame
from ButtonClass import *
import PlayerClass
import RoomClass
import datetime
import random
import pygame.gfxdraw

from NPC import *

class GameClass (object):
    displayText=None
    room=None
    mode="Game"
    shop=None
    task=[]
    buildmode=None
    def init():        
        pass
        
    def __init__(self,width,height,screen):
        PlayerClass.player.init()
        self.width=width
        self.height=height
        self.initTime()
        self.tasks=[]
        self.room=RoomClass.RoomClass(width,height,self.roomName)
        self.player=PlayerClass.player(self.width,self.height,int(self.playerX),int(self.playerY),self.room)
        self.playerGroup=pygame.sprite.GroupSingle(self.player)
        self.screen=screen
        self.roomsurface=pygame.Surface((width,height))
        self.drawRoom()
        self.font=pygame.font.SysFont("Calibri",20)
        self.timer=0
        self.initNPC()
        self.tag=None
        self.optionButton=Button((62,38,12),1050,25,130,100,None,None,150)
        self.name="Player"
        self.introText=["Architect","Planner","Designer","Creator","With destruction: beginning","A new society emerges","And so the architect's job begins"]
    
    #does some inniting
    def initTime(self):
        self.realTimePast={}
        self.gameTime={}
        currentPlace=readFile("SurfaceWorld\\PlayerStats\\playerInfo.txt")
        self.fileParse(currentPlace)
        self.introText=None
        self.realTimeNow={"Day":datetime.datetime.now().day,"Month": datetime.datetime.now().month, "Year":datetime.datetime.now().year}
        self.processTime()
    
    #inits NPCs
    def initNPC(self):
        npc=shopOwner("ImmortalMammal",self.gameTime["Hour"])
        self.npcList=[]
        self.npcList.append(npc)
        npc=NPC("Amy",self.gameTime["Hour"])
        self.npcList.append(npc)
        npc=NPC("Katie",self.gameTime["Hour"])
        self.npcList.append(npc)
        npc=NPC("Kim",self.gameTime["Hour"])
        self.npcList.append(npc)
        self.customer=None
        self.npcGroup=pygame.sprite.Group()
        self.objects=self.room.objects
        self.objectGroup=pygame.sprite.Group()
        for objects in self.objects:
            self.objectGroup.add(objects)
        
    def keyPressed(self, keyCode, modifier):
        if GameClass.mode=="Game":
            possMode=self.player.keyPressed(keyCode,modifier)
            if keyCode==pygame.K_ESCAPE:
                self.writeFile()
                if self.gameTime["Hour"]>=10:
                    self.writeCrackFile()
                return "start"
            if possMode!=None:
                self.writeFile()
                return possMode
            return "mainGame"
        elif GameClass.mode=="start":
            return "mainGame"
        elif GameClass.mode=="option":
            if keyCode==pygame.K_ESCAPE:
                GameClass.mode="Game"
            return "mainGame"
        elif GameClass.mode=="shop":
            GameClass.shop.keyPressed(keyCode,modifier)
            return "mainGame"
        elif GameClass.mode=="buildMode":
            GameClass.buildmode.keyPressed(keyCode,modifier)
            return "mainGame"

    def mousePressed(self, x, y):
        if GameClass.mode=="Game":
            if self.optionButton.buttonPressed(x,y)==True:
                GameClass.mode="option"
        elif GameClass.mode=="shop":
            GameClass.shop.mousePressed(x,y)
        elif GameClass.mode=="buildMode":
            poss,som=GameClass.buildmode.mousePressed(x,y,self.tasks)
            if poss=="mainGame":
                self.setRoom()
                GameClass.mode="Game"
                self.tasks=som
                    
    def mouseMotion(self, x, y):
        if GameClass.mode=="Game":
            self.optionButton.mouseMotion(x,y)
        if GameClass.mode=="shop":
            GameClass.shop.mouseMotion(x,y)
        elif GameClass.mode=="buildMode":
            GameClass.buildmode.mouseMotion(x,y)
            
    def mouseDrag(self, x, y):
        if GameClass.mode=="shop":
            GameClass.shop.mouseDrag(x,y)
        elif GameClass.mode=="buildMode":
            GameClass.buildmode.mouseDrag(x,y)
    
    def drawRoom(self):       
        self.room.drawRoom(self.roomsurface)
    
    def drawScreen(self):
        if GameClass.mode=="Game":
            self.drawStandard()
        elif GameClass.mode=="start":
            pygame.draw.rect(self.screen,(0,0,0),(0,0,1200,700))
            font=pygame.font.SysFont("vivaldi",50,bold=True)
            text=(self.introText[0])
            surf=font.render(text,False,(255,255,255))
            self.screen.blit(surf,(self.width/4,self.height//2))
        elif GameClass.mode=="shop":
            GameClass.shop.redrawAll(self.screen)
        elif GameClass.mode=="option":
            self.drawStandard()
            pygame.gfxdraw.box(self.screen, pygame.Rect(200,200,800,400), (255,160,122,175))
            font=pygame.font.SysFont("pristina",40,bold=True)
            text="Orders to Fufill"
            surf=font.render(text,False,(210,220,210))
            self.screen.blit(surf,(400,210))
            text="Date:  %d\\%d\\%d"%(self.gameTime["Month"],self.gameTime["Day"],self.gameTime["Year"])
            surf=font.render(text,False,(210,210,210))
            self.screen.blit(surf,(700,550))
            for i in range(len(self.tasks)):
                font=pygame.font.SysFont("pristina",30,bold=True)
                text=",".join(self.tasks[i])
                surf=font.render(text,False,(210,210,210))
                self.screen.blit(surf,(400,270+(i*40)))
        elif GameClass.mode=="buildMode":
            GameClass.buildmode.redrawAll(self.screen)
    
    #always normally drawn
    def drawStandard(self):
        self.screen.blit(self.roomsurface,(0,0))
        self.playerGroup.draw(self.screen)
        if GameClass.displayText!=None:
            textSurface=self.font.render(GameClass.displayText,False,(0,0,0))
            self.screen.blit(textSurface,(100,self.height-100))
        font=pygame.font.SysFont("Georgia",40,bold=True)
        if self.gameTime["Minute"]//10==0:
            min="0"+str(self.gameTime["Minute"])
        else:
            min=str(self.gameTime["Minute"])
        time="%d:%s"%(self.gameTime["Hour"],min)
        timeSurface=font.render(time,False,(255,255,255))
        self.optionButton.drawButton(self.screen)
        self.screen.blit(timeSurface,(1065,50))        
        if len(self.npcGroup)>0:
            self.npcGroup.draw(self.screen)
        if self.tag!=None:
            self.tag.drawButton(self.screen)
            font=pygame.font.SysFont("pristina",30,bold=True)
            text="New Order Filed!"
            surf=font.render(text,False,(210,210,210))
            self.screen.blit(surf,(460,25))
        font=pygame.font.SysFont("pristina",30,bold=True)
        roomNameSurf=font.render(self.roomName,False,(0,0,0))
        self.screen.blit(roomNameSurf,(1000,650))
        
    
    def timerFired(self,dt,isKeyPressed):
        if GameClass.mode=="Game":
            self.playerGroup.update(isKeyPressed,self.width,self.height)    
            if GameClass.room!=self.roomName:
                self.setRoom()
            if len(GameClass.task)>0:
                self.tasks.append(GameClass.task.pop())
                self.tag=timerButton((255,160,122),self.width//2-150,0,300,100,None,None,175,100)
            if self.tag!=None:
                som=self.tag.update()
                if som==None:
                    self.tag=None
            self.timer+=1
            if self.timer%10==0:
                self.gameTime["Minute"]+=1
                self.timeFix()
            for npc in self.npcList:
                npc.update(self.roomName,self.room,self.gameTime["Hour"],self.width,self.height)
                if npc.room==self.roomName:
                    if npc not in self.npcGroup:
                        self.npcGroup.add(npc)
                else:
                    if npc in self.npcGroup:
                        self.npcGroup.remove(npc)
            #adds customers
            if self.customer==None:
                if self.roomName=="customerRoom":
                    if self.gameTime["Hour"]>=10 and self.gameTime["Hour"]<17:
                        self.customer=random.choice(self.npcList)
                        self.customer.room="customerRoom"
                        self.customer.status="customer"
                        if self.customer not in self.npcGroup:
                            self.npcGroup.add(self.customer)
                        self.customer.x=self.width//2
                        self.customer.y=self.height-100
            for npc in self.npcGroup:
                self.collideObject(npc)
            if self.npcGroup!=None:
                self.collideChar()
            self.collideObject(self.player)           
        elif GameClass.mode=="start":
            self.timer+=1
            if self.timer%100==0:
                self.introText.pop(0)
                if len(self.introText)==0:
                    GameClass.mode="Game"
        elif GameClass.mode=="buildMode":
            GameClass.buildmode.timerFired(dt)
            
    #check object collision
    def collideObject(self,person):
        collided=False
        if self.room.objects!=None:
            for object in self.objectGroup:
                if pygame.sprite.collide_rect(person,object):
                    person.object=object
                    object.interact.add(person)
                    type,fill=object.action()
                    collided=True
                    if type!="move":
                        if person.dir=="Left":
                            person.left=False
                        elif person.dir=="Right":
                            person.right=False
                        elif person.dir=="Up":
                            person.up=False
                        elif person.dir=="Down":
                            person.down=False
        if collided==False:
            for object in self.objectGroup:
                if person in object.interact:
                    object.interact.remove(person)
            person.left=True
            person.right=True
            person.down=True
            person.up=True
            person.object=None
            
    #people collision        
    def collideChar(self):
        collided=False
        for char in self.npcGroup:            
            if pygame.sprite.collide_rect(self.player,char):
                self.player.object1=char
                collided=True
                if self.player.dir=="Left":
                    self.player.left1=False
                    char.right1=False
                elif self.player.dir=="Right":
                    self.player.right1=False
                    char.left1=False
                elif self.player.dir=="Up":
                    self.player.up1=False
                    char.down1=False
                elif self.player.dir=="Down":
                    self.player.down1=False
                    char.up1=False
        if collided==False:
            self.player.left1=True
            self.player.right1=True
            self.player.down1=True
            self.player.up1=True
            self.player.object1=None     
            for char in self.npcGroup:
                char.up1=True
                char.down1=True
                char.left1=True
                char.right1=True
    
    #parse player info
    def fileParse(self,content):
        content=content.splitlines()
        for line in content:
            if line.startswith("Room: "):
                self.roomName=line[6:]
                GameClass.room=self.roomName
            elif line.startswith("PlayerX: "):
                self.playerX=line[9:]
            elif line.startswith("PlayerY: "):
                self.playerY=line[9:]
            elif line.startswith("Month: "):
                if line[7:]!="None":
                    self.realTimePast["Month"]=int(line[7:])
                else:
                    self.realTimePast["Month"]="None"
            elif line.startswith("Day: "):
                if line[5:]!="None":
                    self.realTimePast["Day"]=int(line[5:])
                else:
                    self.realTimePast["Day"]="None"
            elif line.startswith("Year: "):
                if line[6:]!="None":
                    self.realTimePast["Year"]=int(line[6:])
                else:
                    self.realTimePast["Year"]="None"
            elif line.startswith("GameDay: "):
                if line[9:]!="None":
                    self.gameTime["Day"]=int(line[9:])
                else:
                    self.gameTime["Day"]="None"
            elif line.startswith("GameMonth: "):
                if line[11:]!="None":
                    self.gameTime["Month"]=int(line[11:])
                else:
                    self.gameTime["Month"]="None"
            elif line.startswith("GameYear: "):
                if line[10:]!="None":
                    self.gameTime["Year"]=int(line[10:])
                else:
                    self.gameTime["Year"]="None"
            elif line.startswith("GameHour: "):
                if line[10:]!="None":
                    self.gameTime["Hour"]=int(line[10:])
                else:
                    self.gameTime["Hour"]="None"
            elif line.startswith("GameMinute: "):                
                if line[12:]!="None":
                    self.gameTime["Minute"]=int(line[12:])
                else:
                    self.gameTime["Minute"]="None"
            elif line.startswith("Tasks:"):
                self.tasks.append(content.split(":")[1])
                
    #changes room
    def setRoom(self):
        self.roomName=GameClass.room
        self.room=RoomClass.RoomClass(self.width,self.height,GameClass.room)
        self.drawRoom()
        self.player.changePlayerRoom(self.room)
        self.objects=self.room.objects
        self.objectGroup=pygame.sprite.Group()
        for objects in self.objects:
            self.objectGroup.add(objects)
        GameClass.displayText=None
        
    #changes time, checks current time and changes time correspondingly
    def processTime(self):
        if self.gameTime["Day"]=="None":
            GameClass.mode="start"
            self.gameTime["Day"]=self.realTimeNow["Day"]
            self.gameTime["Month"]=self.realTimeNow["Month"]
            self.gameTime["Year"]=self.realTimeNow["Year"]
            self.gameTime["Hour"]=8
            self.gameTime["Minute"]=0
        else:
            yearDif=abs(self.realTimePast["Year"]-self.realTimeNow["Year"])
            monthDif=self.realTimePast["Month"]-self.realTimeNow["Month"]
            dayDif=self.realTimePast["Day"]-self.realTimeNow["Day"]
            totMonth=monthDif+yearDif*12
            avgDayInMonth=30
            totDay=monthDif*avgDayInMonth+dayDif
            dayPast=totDay/12
            if dayPast>365:
                self.gameTime["Year"]+=dayPast//365
                dayPast%=365
            if dayPast>30:
                self.gameTime["Month"]+=dayPast//30
            dayPast%=30
            hours=dayPast%1*24
            minutes=hours%1*60
            self.gameTime["Minute"]+=int(minutes)
            self.gameTime["Hour"]+=int(hours)
            self.gameTime["Day"]+=int(dayPast)
            self.timeFix()
    
    #fixes time based on overnumbers
    def timeFix(self):
        if self.gameTime["Minute"]>=60:
            self.gameTime["Hour"]+=1
            self.gameTime["Minute"]-=60
        if self.gameTime["Hour"]>24:
            self.gameTime["Day"]+=1
            self.customer=None
            self.gameTime["Hour"]-=24
        if self.gameTime["Day"]>30:
            self.gameTime["Month"]+=1
            self.gameTime["Day"]-=30
        if self.gameTime["Month"]>12:
            self.gameTime["Year"]+=1
            self.gameTime["Month"]-=12
                    
    #creates cracks
    def writeCrackFile(self):
        path="SurfaceWorld\\Cracks.txt"
        content=readFile(path)
        x=random.randint(0,900)
        y=random.randint(0,600)
        stuff=content+"\n"+"%d,%d"%(x,y)
        with open(path,"wt") as f:
            f.write(stuff)
        
    #modified from class notes, writes player info
    def writeFile(self):
        path="SurfaceWorld\\PlayerStats\\PlayerInfo.txt"
        content="Room: %s"%(self.roomName)
        content+="\nPlayerX: %s"%self.player.x
        content+="\nPlayerY: %s"%self.player.y
        content+="\nMonth: %s"%self.realTimeNow["Month"]
        content+="\nDay: %s"%self.realTimeNow["Day"]
        content+="\nYear: %s"%self.realTimeNow["Year"]
        for key in self.gameTime:
            content+="\nGame%s: %s"%(key,self.gameTime[key]) 
        with open(path,"wt") as f:
            f.write(content)
            
#taken class notes
def readFile(path):
    with open(path, "rt") as f:
        return f.read()