from GameObject import GameObject
import pygame
import NPC
class objInRoom(GameObject):
    def __init__(self,name,x,y,scaleX,scaleY,rot):
        self.x=x
        self.y=y
        self.name=name
        if "Door" in name:
            try:
                image=pygame.image.load("Images\\"+name+".png")
            except:
                image=pygame.image.load("Images\\doorCust.png")
        else:
            image=pygame.image.load("Images\\"+name+".png")
        self.image=pygame.transform.rotate(pygame.transform.scale(image.convert_alpha(),
            (scaleX,scaleY)), rot) 
        super(objInRoom,self).__init__(x,y,self.image,0)
        self.actions=self.parseAction(readFile("SurfaceWorld\\Text\\"+name+".txt"))
        self.interact=set()
    
    def draw(self,screen):
        w,h=self.image.get_size()
        screen.blit(self.image,(self.x,self.y))           
        self.updateRect()
    
    def action(self,special=False,person=None):
        if (len(self.actions[0]))>0:
            if self.actions[0][0]=="emptPlot":
                return "buildMode","start"
            elif self.actions[0][0]=="Move":
                return "move",self.actions[0][1]
            elif self.actions[0][0]=="Interact":
                if person=="player":
                    for person in self.interact:
                        if person.status=="customer":
                            return person.action(True,"customer")
                      
        elif (len(self.actions[1]))>0:
            dialogue=self.actions[1][0]
            if len(self.actions[1])>1 and person=="player":
                self.actions[1].pop(0)
            return "dialogue",dialogue
        return None,None
    
    def parseAction(self,contents):
        contents=contents.splitlines()
        lines=[]
        interact=[]
        for line in contents:
            if line.startswith("Text:"):
                lines.append(line[6:])
            else:
                interact.append(line)
        return [interact,lines]

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

        
                
    
    
