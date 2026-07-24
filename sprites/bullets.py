import pygame

class Bullets( pygame.sprite.Sprite):
    def __init__(self, position, direction, bullets_img):
        super().__init__()
        self.image = bullets_img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.position = position
        self.direction = direction
        self.velocity = pygame.Vector2(0,0)
    def movement(self):
        self.velocity = self.direction*10
    def delete(self):
        if self.position.x > 800 or self.position.y > 600 or self.position.x <-100 or self.position.y <-60:
            self.kill()
    def update(self):
        self.movement()
        self.position += self.velocity
        self.rect.center = self.position
        self.delete()