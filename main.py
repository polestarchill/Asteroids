import pygame 
from sys import exit
from random import choice, randint, uniform
from sprites.ship import Ship
from sprites.asteroid import Asteroids
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Asteroids')
is_running = True
clock = pygame.time.Clock()
font_dir = 'font/Pixeltype.ttf'
Font = pygame.font.Font(font_dir, 20)
asteroid_image_large = pygame.image.load('Assets/Retina/meteor_large.png').convert_alpha()
asteroid_image_medium = pygame.image.load(r'Assets\Retina\meteor_detailedSmall.png').convert_alpha()
asteroid_image_small = pygame.image.load(r'Assets\Retina\meteor_tiny.png').convert_alpha()
asteroid_image_large = pygame.transform.smoothscale(asteroid_image_large,(90,90))
asteroid_image_medium = pygame.transform.smoothscale(asteroid_image_medium,(90,90))
asteroid_image_small = pygame.transform.smoothscale(asteroid_image_small,(120,120))
ship_moving1 = pygame.image.load(r'Assets\Retina/ship_moving1.png').convert_alpha()
ship_moving1 = pygame.transform.smoothscale_by(ship_moving1, 0.8)
ship_moving2 = pygame.image.load(r'Assets\Retina/ship_moving2.png').convert_alpha()
ship_moving2 = pygame.transform.smoothscale_by(ship_moving2, 0.8)
bullets_img = pygame.image.load(r'Assets\Retina\effect_purple.png').convert_alpha()
bullets_img=pygame.transform.scale(bullets_img, (10,10))
ship_img =  pygame.image.load(r'Assets\Retina\ship_E.png').convert_alpha()
ship_img = pygame.transform.smoothscale_by(ship_img, 0.8)
ship_rect = ship_img.get_rect(center=(400,300))

pygame.mixer.music.load("sound/bgm.ogg")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
thrust = pygame.mixer.Sound('sound/thrust.wav')
thrust.set_volume(0.5)
ship_explode_sound = pygame.mixer.Sound('sound/ship_explode.wav')
ship_explode_sound.set_volume(0.2)
game_over_sound = pygame.mixer.Sound('sound/game_over.wav')
game_over_sound.set_volume(0.2)
big_explosion = pygame.mixer.Sound('sound/bangLarge.wav')
medium_explosion = pygame.mixer.Sound('sound/bangMedium.wav')
small_explosion = pygame.mixer.Sound('sound/bangSmall.wav')
fire_sound = pygame.mixer.Sound('sound/fire.wav')
fire_sound.set_volume(0.5)
pygame.display.set_icon(ship_img)


ship = pygame.sprite.GroupSingle()
ship.add(Ship(ship_img, ship_moving1, ship_moving2, thrust,bullets_img, fire_sound))
bullets = pygame.sprite.Group()
asteroids= pygame.sprite.Group()
asteroids.add(Asteroids(asteroid_image_large,asteroid_image_medium,asteroid_image_small))
spawn_asteroid = pygame.USEREVENT +1
pygame.time.set_timer(spawn_asteroid,3000)
background = pygame.image.load('Assets/background.jpg').convert_alpha()
background = pygame.transform.grayscale(background)
background = pygame.transform.scale_by(background,0.5)
SCORE = 0
MENU = 0
PLAYING = 1
GAMEOVER = 2
game_state = MENU
death_time = 0
gameover_played = False
Title_font = pygame.font.Font(font_dir, 100)
menu_font = pygame.font.Font(font_dir, 70)


def bullet_collision(bullets, asteroids):
    global SCORE
    collision =pygame.sprite.groupcollide(bullets, asteroids, True, False, pygame.sprite.collide_mask)
    for  value in collision.values():
        for asteroid in value:
            if asteroid.stage == 3:
                asteroids.add(Asteroids(asteroid_image_large, asteroid_image_medium, asteroid_image_small, 2, asteroid.position, asteroid.velocity.rotate(35)))
                asteroids.add(Asteroids(asteroid_image_large, asteroid_image_medium, asteroid_image_small,2, asteroid.position, asteroid.velocity.rotate(-35)))
                big_explosion.play()
                asteroid.kill()
            elif asteroid.stage == 2:
                asteroids.add(Asteroids(asteroid_image_large, asteroid_image_medium, asteroid_image_small,1, asteroid.position, asteroid.velocity.rotate(35)))
                asteroids.add(Asteroids(asteroid_image_large, asteroid_image_medium, asteroid_image_small,1, asteroid.position, asteroid.velocity.rotate(-35)))
                medium_explosion.play()
                asteroid.kill()
            elif asteroid.stage == 1:
                SCORE += 5
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


    
def ship_collision(asteroids,ship_given=ship):
    global game_state, death_time
    collision = pygame.sprite.groupcollide(ship,asteroids,False, False, pygame.sprite.collide_mask) 
    if collision and not ship.sprite.invincible:
        ship.sprite.ship_lives -= 1
        ship_explode_sound.play()
        if ship.sprite.ship_lives <=0:
            thrust.stop()
            death_time = pygame.time.get_ticks()
            pygame.mixer.music.stop()
            game_state = GAMEOVER
        else:
            ship.sprite.position = pygame.Vector2(400, 300)
            ship.sprite.velocity = pygame.Vector2(0, 0)

            ship.sprite.invincible = True
            ship.sprite.invincible_start = pygame.time.get_ticks()
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
    global SCORE  
    asteroids.empty()
    asteroids.add(Asteroids(asteroid_image_large, asteroid_image_medium, asteroid_image_small))
    bullets.empty()
    ship.add(Ship(ship_img, ship_moving1, ship_moving2, thrust,bullets_img, fire_sound))
    SCORE = 0
    game_over_sound.stop()
    pygame.mixer.music.play(-1)
def draw_lives():
    ship_img_hud = pygame.transform.smoothscale_by(ship_img, 0.8)
    for i in range(ship.sprite.ship_lives):
        ship_rect = ship_img.get_rect(topright=(780 - i * 40, 20))
        screen.blit(ship_img_hud, ship_rect)
def ship_invincibility():
    if ship.sprite.invincible:        
        if (pygame.time.get_ticks() // 150) % 2 == 0:
            ship.draw(screen)
    else:
        ship.draw(screen)
def display_score():
    Score_rect_playing = Score_surf.get_rect(topleft=(20,30))
    screen.blit(Score_surf, Score_rect_playing)
while is_running:
    
    Score_surf = menu_font.render(f"Score: {SCORE}",False, 'white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_state == MENU:
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = PLAYING

        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = ship.sprite.shoot()
                    if bullet:
                        bullets.add(bullet)
                        fire_sound.play()
            if event.type == spawn_asteroid:
                asteroids.add(Asteroids(asteroid_image_large, asteroid_image_medium, asteroid_image_small))

        elif game_state == GAMEOVER:
            if pygame.time.get_ticks() - death_time > 700 and not gameover_played :
                ship_explode_sound.stop()
                game_over_sound.play()
                gameover_played = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    game_state = PLAYING

    if game_state == MENU:
        menu()
        
    if game_state == PLAYING:
        screen.blit(background, (0,0))
        ship.update()
        asteroids.update()
        bullets.update()
        bullets.draw(screen)
        asteroids.draw(screen)
        ship_invincibility()
        bullet_collision(bullets,asteroids)
        ship_collision(asteroids)
        draw_lives()
        display_score()
    if game_state == GAMEOVER:
        Score_rect = Score_surf.get_rect(center = (400, 200))
        gameover(Score_surf,Score_rect)
    pygame.display.update()
    clock.tick(60)