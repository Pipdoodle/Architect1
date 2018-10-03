import pygame
#from online manual
class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, radius):
        super(GameObject, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.image, self.radius = x, y, image, radius
        
        self.baseImage = image.copy()  # non-rotated version of image
        w, h = image.get_size()
        self.updateRect()
      

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x , self.y , w, h)
    
    def update(self, screenWidth, screenHeight):
        self.image=self.image
        self.updateRect()
        #wrap around, and update the rectangle again
       
        if self.rect.left > screenWidth-self.width:
            self.x -=  1
        elif self.rect.right < self.width:
            self.x += 1
        if self.rect.top > screenHeight-self.height:
            self.y -=  1
        elif self.rect.bottom < self.height:
            self.y += 1
        self.updateRect()
       