import pygame 
from sys import exit
from random import choice, randint, uniform
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((800,600))
is_running = True
clock = pygame.time.Clock()
bullets = pygame.sprite.Group()
font_dir = 'font/Pixeltype.ttf'
Font = pygame.font.Font(font_dir, 20)
asteroid_image_large = pygame.image.load('PNG/Retina/meteor_large.png').convert_alpha()
asteroid_image_medium = pygame.image.load(r'PNG\Retina\meteor_detailedSmall.png').convert_alpha()
asteroid_image_small = pygame.image.load(r'PNG\Retina\meteor_tiny.png').convert_alpha()
asteroid_image_large = pygame.transform.scale(asteroid_image_large,(90,90))
asteroid_image_medium = pygame.transform.scale(asteroid_image_medium,(90,90))
asteroid_image_small = pygame.transform.scale(asteroid_image_small,(120,120))
bullets_img = pygame.image.load(r'PNG\Retina\effect_yellow.png').convert_alpha()
bullets_img=pygame.transform.scale(bullets_img, (10,10))
ship_img =  pygame.image.load(r'PNG\Retina\ship_E.png').convert_alpha()
ship_rect = ship_img.get_rect(center=(400,300))
pygame.mixer.music.load("sound/bgm.ogg")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
thrust = pygame.mixer.Sound('sound/thrust.wav')
thrust.set_volume(0.5)
game_over_sound = pygame.mixer.Sound('sound/game_over.wav')
game_over_sound.set_volume(0.4)
big_explosion = pygame.mixer.Sound('sound/bangLarge.wav')
medium_explosion = pygame.mixer.Sound('sound/bangMedium.wav')
small_explosion = pygame.mixer.Sound('sound/bangSmall.wav')
fire_sound = pygame.mixer.Sound('sound/fire.wav')
fire_sound.set_volume(0.5)
class Asteroids(pygame.sprite.Sprite):
    def __init__(self, stage=3, position=None, Velocity=None):
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
class Bullets( pygame.sprite.Sprite):
    def __init__(self, position, direction):
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
class Ship(pygame.sprite.Sprite):
    def __init__(self):
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
    def movement(self):
        keys = pygame.key.get_pressed()
        movements = ( keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]  or keys[pygame.K_UP])
        if movements and not self.engine :
            thrust.play(-1)
            self.engine = True
        elif not movements and self.engine :
            thrust.stop()
            self.engine = False
        if keys[pygame.K_LEFT]:
            self.angle += 5
            
            
        if keys[pygame.K_RIGHT]:
            self.angle -= 5
            
            
        if keys[pygame.K_UP]:
            forward = pygame.Vector2(0,-1)
            forward.rotate_ip(-self.angle)
            acceleration = forward*0.05
            self.velocity += acceleration
    
    def fire(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot >= 150:
                fire_bullets()
                fire_sound.play()
                self.last_shot = now
        
    def pos_angle(self):
        
        return (self.position, self.angle)
        
        
    def update(self):
        self.movement()
        self.fire()
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
        
ship = pygame.sprite.GroupSingle()
ship.add(Ship())
asteroids= pygame.sprite.Group()
asteroids.add(Asteroids())
spawn_asteroid = pygame.USEREVENT +1
pygame.time.set_timer(spawn_asteroid,3000)
background = pygame.image.load('PNG/background.jpg').convert_alpha()
background = pygame.transform.grayscale(background)
background = pygame.transform.scale_by(background,0.5)
score = 0
Menu = 0
playing = 1
game_over = 2
game_state = Menu
Title_font = pygame.font.Font(font_dir, 100)
menu_font = pygame.font.Font(font_dir, 70)
def fire_bullets():
    quantities = ship.sprite.pos_angle()
    forward = pygame.Vector2(0,-1)
    forward.rotate_ip(-quantities[1])
    position = quantities[0] + forward*25
    bullets.add(Bullets(position,forward))
def bullet_collision(bullets, asteroids):
    global score
    collision =pygame.sprite.groupcollide(bullets, asteroids, True, False, pygame.sprite.collide_mask)
    for  value in collision.values():
        for asteroid in value:
            if asteroid.stage == 3:
                asteroids.add(Asteroids(2, asteroid.position, asteroid.velocity.rotate(35)))
                asteroids.add(Asteroids(2, asteroid.position, asteroid.velocity.rotate(-35)))
                big_explosion.play()
                asteroid.kill()
            elif asteroid.stage == 2:
                asteroids.add(Asteroids(1, asteroid.position, asteroid.velocity.rotate(35)))
                asteroids.add(Asteroids(1, asteroid.position, asteroid.velocity.rotate(-35)))
                medium_explosion.play()
                asteroid.kill()
            elif asteroid.stage == 1:
                score += 5
                small_explosion.play()
                asteroid.kill()
def gameover(score_surf, score_rect):
    Score = score_surf
    Score_rect = score_rect
    screen.blit(background, (0,0))
    text_1 = Title_font.render('GAME OVER!', False, "white")
    
    play_game = menu_font.render("Press R To Restart",False,'white')
    screen.blit(text_1, text_1.get_rect(center = (400,125)))
    screen.blit(Score, Score_rect)
    screen.blit(play_game, play_game.get_rect(center =(400,450)))

    
def ship_collision(ship, asteroids):
    global game_state
    collision = pygame.sprite.groupcollide(ship,asteroids,True, False, pygame.sprite.collide_mask) 
    if collision:
        thrust.stop()
        game_over_sound.play()
        pygame.mixer.music.stop()
        game_state = game_over
        
def menu():
    screen.blit(background, (0,0))
    game_text = Title_font.render("ASTEROIDS",False,'white')
    game_text_rect = game_text.get_rect(center = (400,125))
    screen.blit(ship_img,ship_rect)
    screen.blit(game_text,game_text_rect )
    play_game = menu_font.render("Press Space To Play",False,'white')
    play_game_rect = play_game.get_rect(center = (400,450))
    screen.blit(play_game, play_game_rect)
    
def restart():
    global score  
    asteroids.empty()
    asteroids.add(Asteroids())
    bullets.empty()
    ship.add(Ship())
    score = 0
    pygame.mixer.music.play(-1)

while is_running:
    
    Score_surf = menu_font.render(f"Score: {score}",False, 'white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_state == Menu:
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = playing

        elif game_state == playing:
            if event.type == spawn_asteroid:
                asteroids.add(Asteroids(3))

        elif game_state == game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    game_state = playing

    if game_state == Menu:
        menu()
        
    if game_state == playing:
        screen.blit(background, (0,0))
        ship.update()
        asteroids.update()
        bullets.update()
        bullets.draw(screen)
        ship.draw(screen)
        asteroids.draw(screen)
        bullet_collision(bullets,asteroids)
        ship_collision(ship, asteroids)
        Score_rect_playing = Score_surf.get_rect(topleft=(20,20))
        screen.blit(Score_surf, Score_rect_playing)
    if game_state == game_over:
        Score_rect = Score_surf.get_rect(center = (400, 200))
        gameover(Score_surf,Score_rect)
    pygame.display.update()
    clock.tick(60)