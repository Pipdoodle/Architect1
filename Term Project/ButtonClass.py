import pygame
class Button(object):
    def __init__(self,color,xS,yS,xLen,yLen,text,mode,blend=255,text2=None):
        self.xS=xS
        self.yS=yS
        self.xLen=xLen
        self.yLen=yLen
        self.xE=xS+xLen
        self.yE=yS+yLen
        self.color=color
        self.text2=text2
        self.mode=mode
        self.blend=blend
        blend1=self.blend+20
        red,green,blue=color[0]-20,color[1]-20,color[2]-20
        if red<0:
            red =0
        if green<0:
            green=0
        if blue<0:
            blue=0
        if blend1>255:
            blend1=255
        self.color=(self.color[0],self.color[1],self.color[2],self.blend)
        self.colorStandard=self.color      
        self.colorShade=(red,green,blue,blend1)
        self.text=text
        
    def drawButton(self,screen,x=None,y=None):
        if x==None and y==None:
            pygame.gfxdraw.box(screen, pygame.Rect(self.xS,self.yS,self.xLen,self.yLen),self.color)
        elif y==None:
            pygame.gfxdraw.box(screen, pygame.Rect(self.xS-x,self.yS,self.xLen,self.yLen),self.color)
        else:
            pygame.gfxdraw.box(screen, pygame.Rect(self.xS,self.yS-y,self.xLen,self.yLen),self.color)
        if self.text!=None:
            font=pygame.font.SysFont("verdanda",20)
            text=font.render(self.text,False,(0,0,0))
            if x==None and y==None:
                screen.blit(text,(self.xS+10,self.yS+self.yLen//2))
            elif y==None:
                screen.blit(text,(self.xS-x+10,self.yS+self.yLen//2))
            else:
                screen.blit(text,(self.xS+10,self.yS-y+self.yLen//2))
        if self.text2!=None:
            font=pygame.font.SysFont("verdanda",20)
            text2=font.render(self.text2,False,(0,0,0))
            if x==None and y==None:
                screen.blit(text2,(self.xS,self.yS+self.yLen//2+20))
            elif y==None:
                screen.blit(text2,(self.xS-x,self.yS+self.yLen//2+20))
            else:
                screen.blit(text2,(self.xS,self.yS-y+self.yLen//2+20))
        
    def buttonPressed(self,x,y,scrollx=0,scrolly=0):
        if x>= self.xS-scrollx and x<= self.xE-scrollx and y>=self.yS-scrolly and y<=self.yE-scrolly:
            return True
        else:
            return False
            
    def returnMode(self):
        return self.mode
        
    #makes buttons highlight
    def mouseMotion(self,x,y,scroll=0):
        if self.buttonPressed(x,y,scroll):
            self.color=self.colorShade
        else:
            self.color=self.colorStandard

#allows movement
class scrollBar(Button):
    def __init__(self,color,xS,yS,xLen,yLen,text,mode,width,height):
        self.width=width
        self.height=height
        super(scrollBar,self).__init__(color,xS,yS,xLen,yLen,text,mode)
        
    def move(self,x=None,y=None):
        if x!=None:
            if x+self.xLen<self.width:
                self.xS=x
            else:
                self.xS=self.width-self.xLen
        if y!=None:
            if y+self.yLen<self.height:
                self.yS=y
            else:
                self.yS=self.height-self.yLen

#dissapear after certain time
class timerButton(Button):
    def __init__(self,color,xS,yS,xLen,yLen,text,mode,blend,time):
        self.time=time
        super(timerButton,self).__init__(color,xS,yS,xLen,yLen,text,mode,blend)
    
    def update(self):
        self.time-=1
        if self.time==0:
            return None
        else:
            return "good"
        