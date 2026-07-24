import pygame
from sprites.bullets import Bullets

class Ship(pygame.sprite.Sprite):
    def __init__(self, ship_img, ship_moving1, ship_moving2, thrust, bullets_img,fire_sound ):
        super().__init__()
        self.engine = False
        self.original_image = ship_img
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = (400,300))
        self.position = pygame.Vector2(400,300)
        self.angle = 0
        self.velocity = pygame.Vector2(0, 0)
        self.last_shot= 0
        self.radius = self.rect.width // 2
        self.ship_lives = 3
        self.invincible = False
        self.invincible_start = 0
        self.moving1 = ship_moving1
        self.moving2 = ship_moving2
        self.thrust = thrust
        self.fire_sound = fire_sound
        self.bullet = bullets_img
    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot < 150:
            return None

        self.last_shot = now

        forward = pygame.Vector2(0, -1)
        forward.rotate_ip(-self.angle)

        position = self.position + forward * 25
        return Bullets(position, forward, self.bullet)
    def movement(self):
        keys = pygame.key.get_pressed()
        movements = ( keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]  or keys[pygame.K_UP])
        if movements and not self.engine :
            self.thrust.play(-1)
            self.engine = True
        elif not movements and self.engine :
            self.thrust.stop()
            self.engine = False
        if keys[pygame.K_LEFT]:
            self.angle += 5
            
            
        if keys[pygame.K_RIGHT]:
            self.angle -= 5
            
            
        if keys[pygame.K_UP]:
            self.engine_uptime = pygame.time.get_ticks()
            forward = pygame.Vector2(0,-1)
            forward.rotate_ip(-self.angle)
            acceleration = forward*0.05
            self.velocity += acceleration
    
        
        
    def update(self):
        self.movement()
        if self.engine:
            if (pygame.time.get_ticks() // 160) %2:
                self.image = pygame.transform.rotate(self.moving1,self.angle)

            else:
                self.image = pygame.transform.rotate(self.moving2,self.angle)

            
        else:
            self.image = pygame.transform.rotate(self.original_image,self.angle )
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.position)
        self.velocity *= 0.99
        if self.velocity.length() > 9:
            self.velocity.scale_to_length(9)
        self.position += self.velocity
        if self.position.x > 800 +self.radius:
            self.position.x = 0-self.radius
        if self.position.x < 0-self.radius:
            self.position.x = 800+self.radius
        if self.position.y > 600+self.radius:
            self.position.y = 0-self.radius
        if self.position.y < 0-self.radius:
            self.position.y = 600+self.radius
        self.rect.center = self.position
        if self.invincible:
            elapsed = pygame.time.get_ticks() - self.invincible_start

            if elapsed > 3000:
                self.invincible = False
