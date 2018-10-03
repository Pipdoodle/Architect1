import pygame
import random 
from GameObject import GameObject
import mainGameClass
class NPC(GameObject):
    def __init__(self,typ,time):
        info=readFile("SurfaceWorld\\Character\\%s\\Information.txt" %typ)
        text=readFile("SurfaceWorld\\Character\\%s\\Dialogue.txt" %typ)
        self.info={}
        self.schedule={}
        self.fileInfoParse(info)
        self.fileTextParse(text)
        self.room=self.schedule[time][0]
        self.x=self.schedule[time][1]
        self.y=self.schedule[time][2]
        self.leave=False
        self.up,self.up1=True,True
        self.down,self.down1=True,True
        self.right,self.right1=True,True
        self.left,self.left1=True,True
        self.dir="down"
        self.roomDialogue=0
        self.status="regular"
        self.steps=0
        self.name="npc"
        self.typ=typ
        self.roomTo=False
        self.object,self.object1=None,None
        self.image=self.downImage
        self.add=False
        self.time=time
        super(NPC, self).__init__(self.x,self.y,self.image,50)
        
    def fileInfoParse(self,content):
        content=content.splitlines()
        for i in range(len(content)):
            if content[i].startswith("First Name"):
                self.info["First Name"]=content[i].split(":")[1]
            elif content[i].startswith("Last Name"):
                self.info["Last Name"]=content[i].split(":")[1]
            elif content[i].startswith("Personality"):
                self.info["personality"]=content[i].split(":")[1]
            elif content[i].startswith("House"):
                self.info["house"]=content[i].split(":")[1]
            elif content[i].startswith("Money"):
                self.info["money"]=content[i].split(":")[1]
            elif content[i].startswith("Occupation"):
                self.info["occupation"]=content[i].split(":")[1]
            elif content[i].startswith("Location"):
                self.info["location"]=content[i].split(":")[1]
            elif content[i].startswith("downImage"):
                self.downImage=pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load(content[i].split(":")[1]).convert_alpha(),
                (70,95)), 0) 
            elif content[i].startswith("upImage"):
                self.upImage=pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load(content[i].split(":")[1]).convert_alpha(),
                (70,95)), 0)  
            elif content[i].startswith("leftImage"):
                self.leftImage=pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load(content[i].split(":")[1]).convert_alpha(),
                (70,95)), 0)  
            elif content[i].startswith("rightImage"):
                self.rightImage=pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load(content[i].split(":")[1]).convert_alpha(),
                (70,95)), 0)  
            elif content[i].startswith("Schedule:"):
                content1=content[i].split(":")
                self.schedule[int(content1[1])]=[content1[2],int(content1[3]),int(content1[4])]
            elif content[i].startswith("Inventory"):
                content1=content[i].split(":")
                self.inventory[content1[0]]=content1[1]
            elif content[i].startswith("Task"):
                content1=content[i].split(":")
                self.info["task"]=content1[1:]
            
    def fileTextParse(self,content):
        self.dialogueDict={}
        content=content.splitlines()
        for i in range(len(content)):
            if ":" in content[i]:
                list=[]                
                for j in range(i+1,len(content)):
                    if ":" in content[j]:
                        break
                    else:
                        list.append(content[j])
                self.dialogueDict[content[i][0:-1]]=list
  
    def action(self,special=False,person=None):        
        if special==True:
            if len(self.dialogueDict.get("customer",[]))>0 and self.roomDialogue<len(self.dialogueDict.get("customer",[])):
                dialogue=self.dialogueDict["customer"][self.roomDialogue]
                self.roomDialogue+=1
            else:
                dialogue="Hello! I don't need anything today!"
        elif len(self.dialogueDict.get(self.room,[]))>0 :
            dialogue=random.choice(self.dialogueDict[self.room])
        else:          
            dialogue=random.choice(self.dialogueDict["Random"])
        return "dialogue",dialogue
                         
    def update(self,room,roomdata,time,width,height):
        self.time=time
        if self.status!="customer" or time>=17 or time<10:
            if self.schedule[time][0]!=self.room:
                self.roomTo=self.schedule[time][0]
                if self.room!=room:
                    self.room=self.roomTo
                    self.roomDialogue=0
                    self.x=self.schedule[time][1]
                    self.y=self.schedule[time][2]
                    self.roomTo=None            
            
        if room==self.room:
            if room=="customerRoom" and self.status=="customer" and time<17:
                if self.roomDialogue>=len(self.dialogueDict.get(roomdata.special,[]))-1:
                    if self.add==False:                       
                        self.add=True
                        mainGameClass.GameClass.task.append(self.info.get("task","basic"))
                    self.target=(roomdata.exitCoord[0],roomdata.exitCoord[1])
                    self.moveToTarget()
                    if self.y>=height-self.height-1:
                        self.status="regular"
                        self.add=False
                    self.image=self.downImage
                else:
                    for objects in roomdata.objects:
                        if objects.name=="counterBottom":
                            self.target=(objects.x,objects.y)
                    self.moveToTarget()
            elif self.roomTo==None:                
                if self.steps<=0:                    
                    self.steps=random.randint(0,400)
                    self.randdir=random.choice([1,2,3,4])
                #random wandering
                if self.randdir==1:
                    if self.up==True and self.up1==True:
                        self.dir="Up"
                        self.image=self.upImage
                        self.y-=1
                    elif self.left==True and self.left1==True:
                        self.y+=1
                        self.dir="Left"
                        self.image=self.leftImage
                        self.x-=1
                    elif self.right==True and self.right1==True:
                        self.y+=1
                        self.image=self.rightImage
                        self.dir="Right"
                        self.x+=1
                    elif self.down==True and self.down1==True:
                        self.y+=1
                        self.image=self.downImage
                        self.dir="Down"
                elif self.randdir==2:
                    if self.down==True and self.down1==True:
                        self.y+=1
                        self.image=self.downImage
                        self.dir="Down"
                    elif self.left==True and self.left1==True:
                        self.y-=1
                        self.dir="Left"
                        self.image=self.leftImage
                        self.x-=1
                    elif self.right==True and self.right1==True:
                        self.y-=1
                        self.image=self.rightImage
                        self.dir="Right"
                        self.x+=1
                    elif self.up==True and self.up1==True:
                        self.y-=1
                        self.image=self.upImage
                        self.dir="Up"
                elif self.randdir==3:               
                    if self.left==True and self.left1==True:
                        self.dir="Left"
                        self.image=self.leftImage
                        self.x-=1
                    elif self.down==True and self.down1==True:
                        self.x+=1
                        self.y+=1
                        self.image=self.downImage
                        self.dir="Down"
                    elif self.up==True and self.up1==True:
                        self.x+=1
                        self.image=self.upImage
                        self.dir="Up"
                        self.y-=1
                    elif self.right==True and self.right1==True:
                        self.dir="Right"
                        self.image=self.rightImage
                        self.x+=1                    
                elif self.randdir==4:
                    if self.right==True and self.right1==True:
                        self.dir="Right"
                        self.image=self.rightImage
                        self.x+=1
                    elif self.up==True and self.up1==True:
                        self.x-=1
                        self.image=self.upImage
                        self.dir="Up"
                        self.y-=1
                    elif self.down==True and self.down1==True:
                        self.x-=1
                        self.image=self.downImage
                        self.y+=1
                        self.dir="Down"
                    elif self.left==True and self.left1==True:
                        self.dir="Left"
                        self.image=self.leftImage
                        self.x-=1
                self.steps-=1
            else:
                if self.object!=None:
                    typ,som=self.object.action(None)
                    if typ=="move":
                        self.room=self.roomTo
                        self.roomDialogue=0
                        self.x=self.schedule[time][1]
                        self.y=self.schedule[time][2]
                        self.roomTo=None
                        self.target=None
                else:
                    self.target=(roomdata.exitCoord[0],roomdata.exitCoord[1])
                    self.moveToTarget()
        super(NPC, self).update(width,height)
        return None
        
    def moveToTarget(self):
        if self.target[1]>self.y:
            if self.down==True and self.down1==True:
                self.dir="Down"
                try:
                    self.image=self.downImage
                except:
                    self.image=pygame.transform.rotate(pygame.transform.scale(
                    pygame.image.load("Images\\downProf.png").convert_alpha(),
                    (70,95)), 0)                 
                self.y+=1
        elif self.target[1]<self.y:
            if self.up==True and self.up1==True:
                self.dir="Up"
                self.image=self.upImage
                self.y-=1
        if self.target[0]>self.x:
            if self.right==True and self.right1==True:
                self.image=self.rightImage
                self.dir="Right"
                self.x+=1
        elif self.target[0]<self.x:
            if self.left==True and self.left1==True:
                self.image=self.leftImage
                self.dir="Left"
                self.x-=1
    
#taken from class notes
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

class shopOwner(NPC):
    def action(self,special=False,person=None):        
        if special!=True and self.time>=12 and self.time<=14:
            return "shop",self.typ
        else:
            return super(shopOwner,self).action(special)
 
                
           
    