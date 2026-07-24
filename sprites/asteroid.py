import pygame
from random import choice, uniform, randint
class Asteroids(pygame.sprite.Sprite):
    def __init__(self,asteroid_image_large,asteroid_image_medium,asteroid_image_small, stage=
                3, position=None, Velocity=None,):
        super().__init__()
        self.image_large = asteroid_image_large
        self.image_medium = asteroid_image_medium
        self.image_small = asteroid_image_small
        if stage ==3:
            self.image = self.image_large
        elif stage== 2:
            self.image = self.image_medium
        elif stage ==1:
            self.image = self.image_small
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        
        if position is None:
            self.spawn()
        else:
            self.position = pygame.Vector2(position)
            self.velocity = pygame.Vector2(Velocity)
        self.health = 1
        self.stage = stage
    def spawn(self):
        edge = ['top','bottom','left','right']
        edge = choice(edge)
        
        if edge == 'top':
            self.position = pygame.Vector2(randint(0,800),-5)
            direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
            direction = direction.normalize()
            self.velocity = direction*2
        elif edge == 'bottom':
            self.position = pygame.Vector2(randint(0,800),605)
            direction = pygame.Vector2(uniform(-0.5,0.5),-1)
            direction = direction.normalize()
            self.velocity = direction*2
        elif edge == 'left':
            self.position = pygame.Vector2(-5,randint(0,600))
            direction = pygame.Vector2(1,uniform(-0.5,0.5))
            direction = direction.normalize()
            self.velocity = direction*2
        elif edge == 'right':
            self.position = pygame.Vector2(805,randint(0,600))
            direction = pygame.Vector2(-1,uniform(-0.5,0.5))
            direction = direction.normalize()
            self.velocity = direction*2
            
        
    def wrap(self):
        radius = self.rect.width //2
        if self.position.x > 800 + radius :
            self.position.x = -radius
            
        if self.position.y > 600+radius :
            self.position.y = -radius
            
        if self.position.x < 0 -radius :
            self.position.x = 800+radius
            
        if self.position.y < 0-radius :
            self.position.y = 600 +radius
            
    
    def update(self):
        self.position += self.velocity
        self.wrap()
        self.rect.center = self.position