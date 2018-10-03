import pygame
import pyaudio
import speech_recognition as sr
import sys  
sys.path.append("SurfaceWorld")  
from startMenu import startMenu
from mainGameClass import GameClass
from mainSubGameClass import SubGameClass
from audioPlayerCkass import record
import threading

#barebone from pygame guide
class startGame(object):
    
    def init(self,screen):
        startMenu.init()
        self.mode="start"
        self.menu=startMenu(self.width,self.height)
        self.screen=screen

    def mousePressed(self, x, y):
        if self.mode=="start":
            mode=(self.menu.startMousePressed(x,y))
            if mode!=None:
                self.mode=mode
            if self.mode=="mainGame":
                self.mainGame=GameClass(self.width,self.height,self.screen)
            elif self.mode=="world":
                SubGameClass.init()
                self.subGame=SubGameClass(self.width,self.height)
        elif self.mode=="mainGame":
            self.mainGame.mousePressed(x,y)
            pass
        elif self.mode=="world":
            pass

     
    def mouseReleased(self, x, y):
        if self.mode=="start":
            pass
        elif self.mode=="option":
            pass
        elif self.mode=="credit":
            pass
        elif self.mode=="mainGame":
            pass
        elif self.mode=="world":
            pass
    

    def mouseMotion(self, x, y):
        if self.mode=="start":
            self.menu.startMouseMotion(x,y)
        elif self.mode=="mainGame":
            self.mainGame.mouseMotion(x,y)
        elif self.mode=="world":
            self.subGame.mouseMotion(x,y)
        

    def mouseDrag(self, x, y):
        if self.mode=="start":
            pass
        elif self.mode=="mainGame":
            self.mainGame.mouseDrag(x,y)
        elif self.mode=="world":
            pass
        elif self.mode=="buildMode":
            self.buildmode.mouseDrag(x,y)

    def keyPressed(self, keyCode, modifier):
        if self.mode=="start":
            pass
        elif self.mode=="mainGame":
            self.mode=self.mainGame.keyPressed(keyCode,modifier)
        elif self.mode=="world":
            self.mode=self.subGame.keyPressed(keyCode,modifier)
    
    def keyReleased(self, keyCode, modifier):
        if self.mode=="start":
            pass
        elif self.mode=="mainGame":
            pass
        elif self.mode=="world":
            pass
 
    def timerFired(self, dt):
        if self.mode=="start":
            pass
        elif self.mode=="mainGame":
            self.mainGame.timerFired(dt,self.isKeyPressed)
        elif self.mode=="world":
            som=self.subGame.timerFired(dt,self.isKeyPressed)
            if som=="start":
                self.mode=som

    def redrawAll(self, screen,filter):
        if self.mode=="start":
            self.menu.drawScreen(screen)
        elif self.mode=="mainGame":
            self.mainGame.drawScreen()
        elif self.mode=="world":
            self.subGame.drawScreen(screen,filter)

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=1200, height=700, fps=50, title="Architect"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        filter=pygame.surface.Surface((self.width,self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
        # stores all the keys currently being held down
        self._keys = dict()
        # call game-specific initialization
        self.init(screen)
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen,filter)
            pygame.display.flip()
            pygame.display.update()

        pygame.quit()


def main():
    game = startGame()
    game.run()
 

if __name__ == '__main__':
    main()