import pygame
import random
import os

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 350
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 50
BOX_SIZE = 40
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)
YELLOW = (200, 200, 0)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# Display mode
display_mode = 'fullscreen'

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Mini Mario Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

player_name = "Player"
max_unlocked_level = 1

# Paths
ASSETS = 'assets'

# Load images
player_img = pygame.image.load(os.path.join(ASSETS, "stickman.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

enemy_img = pygame.image.load(os.path.join(ASSETS, "spider.png")).convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))

# Load sounds
jump_sound = pygame.mixer.Sound(os.path.join(ASSETS, "jump.wav"))
score_sound = pygame.mixer.Sound(os.path.join(ASSETS, "score.wav"))
level_complete_sound = pygame.mixer.Sound(os.path.join(ASSETS, "level_complete.wav"))

def set_display_mode(mode):
    global screen, display_mode
    display_mode = mode
    if mode == 'fullscreen':
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    elif mode == 'borderless':
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)

def menu():
    global player_name
    text = ''
    input_active = False
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive

    play_btn = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 60, 200, 50)
    levels_btn = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50)
    options_btn = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 60, 200, 50)
    input_box = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 130, 200, 40)

    while True:
        screen.fill((135, 206, 235))
        title = font.render("Mini Mario Game", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

        label = font.render("Player Name:", True, BLACK)
        screen.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, SCREEN_HEIGHT//2 - 170))

        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font.render(text, True, BLACK)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))

        for btn, txt in [(play_btn, "Play"), (levels_btn, "Levels"), (options_btn, "Options")]:
            pygame.draw.rect(screen, GREEN, btn)
            label = font.render(txt, True, BLACK)
            screen.blit(label, (btn.x + btn.width//2 - label.get_width()//2, btn.y + btn.height//2 - label.get_height()//2))

        dev = font.render("DEV TEST V5", True, BLACK)
        screen.blit(dev, (10,10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = not input_active
                else:
                    input_active = False
                color = color_active if input_active else color_inactive

                if play_btn.collidepoint(event.pos):
                    player_name = text if text.strip() else "Player"
                    game(1)
                elif levels_btn.collidepoint(event.pos):
                    player_name = text if text.strip() else "Player"
                    level_select()
                elif options_btn.collidepoint(event.pos):
                    options_menu()

            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    player_name = text if text.strip() else "Player"
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < 12:
                        text += event.unicode
        clock.tick(60)

def options_menu():
    fullscreen_btn = pygame.Rect(SCREEN_WIDTH//2 -150, SCREEN_HEIGHT//2 -50, 300,50)
    borderless_btn = pygame.Rect(SCREEN_WIDTH//2 -150, SCREEN_HEIGHT//2 +20, 300,50)
    back_btn = pygame.Rect(20, SCREEN_HEIGHT -60, 100,40)

    while True:
        screen.fill((50,50,50))
        title = font.render("Options", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

        pygame.draw.rect(screen, GREEN if display_mode=='fullscreen' else GRAY, fullscreen_btn)
        pygame.draw.rect(screen, GREEN if display_mode=='borderless' else GRAY, borderless_btn)
        pygame.draw.rect(screen, GREEN, back_btn)

        for btn, txt in [(fullscreen_btn,"Fullscreen"), (borderless_btn,"Borderless Fullscreen")]:
            label = font.render(txt, True, BLACK)
            screen.blit(label, (btn.x+btn.width//2 - label.get_width()//2, btn.y+btn.height//2 - label.get_height()//2))

        back = font.render("Back", True, BLACK)
        screen.blit(back, (back_btn.x+back_btn.width//2 - back.get_width()//2, back_btn.y+back_btn.height//2 - back.get_height()//2))

        dev = font.render("DEV TEST V5", True, WHITE)
        screen.blit(dev, (10,10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if fullscreen_btn.collidepoint(event.pos): set_display_mode('fullscreen')
                elif borderless_btn.collidepoint(event.pos): set_display_mode('borderless')
                elif back_btn.collidepoint(event.pos): return
        clock.tick(60)

def level_select():
    global max_unlocked_level
    level_btns = [pygame.Rect(150+i*120, SCREEN_HEIGHT//2 -25, 100,50) for i in range(5)]

    while True:
        screen.fill((100,150,200))
        title = font.render("Select Level", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

        for idx, btn in enumerate(level_btns):
            level_num = idx+1
            pygame.draw.rect(screen, GREEN if max_unlocked_level>=level_num else GRAY, btn)
            label = font.render(f"Level {level_num}", True, BLACK)
            screen.blit(label, (btn.x+btn.width//2 - label.get_width()//2, btn.y+btn.height//2 - label.get_height()//2))

        dev = font.render("DEV TEST V5", True, WHITE)
        screen.blit(dev, (10,10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                for idx, btn in enumerate(level_btns):
                    if btn.collidepoint(event.pos) and max_unlocked_level>=idx+1:
                        game(idx+1)
        clock.tick(60)

def game(level):
    global max_unlocked_level
    level_width = 1200 if level>=2 else SCREEN_WIDTH
    player = pygame.Rect(100, GROUND_HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    player_vel_y, gravity, jump_strength = 0, 0.8, -15
    on_ground = True
    health, max_health = 3.0, 3.0
    score = 0
    enemy_spawn_event = pygame.USEREVENT +1
    pygame.time.set_timer(enemy_spawn_event, 2000)

    # Level data
    if level==4:
        boxes = [pygame.Rect(300+i*120, GROUND_HEIGHT -100, BOX_SIZE, BOX_SIZE) for i in range(8)]
        enemy_speed=10
    elif level==3:
        boxes = [pygame.Rect(300+i*150, GROUND_HEIGHT -100, BOX_SIZE, BOX_SIZE) for i in range(6)]
        enemy_speed=7
    elif level==2:
        boxes = [
            pygame.Rect(300, GROUND_HEIGHT -100, BOX_SIZE, BOX_SIZE),
            pygame.Rect(500, GROUND_HEIGHT -150, BOX_SIZE, BOX_SIZE),
            pygame.Rect(700, GROUND_HEIGHT -120, BOX_SIZE, BOX_SIZE),
            pygame.Rect(900, GROUND_HEIGHT -160, BOX_SIZE, BOX_SIZE),
            pygame.Rect(1100, GROUND_HEIGHT -130, BOX_SIZE, BOX_SIZE)
        ]
        enemy_speed=6
    else:
        boxes = [pygame.Rect(300, GROUND_HEIGHT -100, BOX_SIZE, BOX_SIZE), pygame.Rect(500, GROUND_HEIGHT -150, BOX_SIZE, BOX_SIZE)]
        enemy_speed=4

    enemies=[]
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); exit()
            elif event.type==enemy_spawn_event:
                enemies.append(pygame.Rect(level_width, GROUND_HEIGHT -ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT))

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player.x=max(0, player.x -5)
        if keys[pygame.K_RIGHT]: player.x=min(level_width -PLAYER_WIDTH, player.x +5)
        if keys[pygame.K_UP] and on_ground: player_vel_y=jump_strength; on_ground=False; jump_sound.play()

        player_vel_y+=gravity; player.y+=int(player_vel_y)
        if player.y>=GROUND_HEIGHT -PLAYER_HEIGHT: player.y=GROUND_HEIGHT -PLAYER_HEIGHT; player_vel_y=0; on_ground=True

        # Collisions
        for enemy in enemies:
            if player.colliderect(enemy): health-=0.5; enemies.remove(enemy); 
            if health<=0: game_over(score); return

        for box in boxes:
            if player.colliderect(box) and player_vel_y<0: score+=1; score_sound.play(); boxes.remove(box)
        if not boxes: level_complete_sound.play(); max_unlocked_level=max(max_unlocked_level, level+1); level_complete(score, level+1); return

        # Move enemies
        for enemy in enemies: enemy.x-=enemy_speed
        enemies = [e for e in enemies if e.x+ENEMY_WIDTH>0]

        # Camera
        cam_x=max(0, min(player.x -SCREEN_WIDTH//2, level_width -SCREEN_WIDTH))

        # Draw
        screen.fill((135,206,235))
        pygame.draw.rect(screen, GREEN, (-cam_x, GROUND_HEIGHT, level_width, SCREEN_HEIGHT -GROUND_HEIGHT))
        for box in boxes: pygame.draw.rect(screen, YELLOW, (box.x -cam_x, box.y, box.width, box.height))
        for enemy in enemies: screen.blit(enemy_img, (enemy.x -cam_x, enemy.y))
        screen.blit(player_img, (player.x -cam_x, player.y))

        screen.blit(font.render(f"Score: {score}",True,WHITE), (10,40))
        screen.blit(font.render(f"Player: {player_name} | Level: {level}",True,WHITE), (10,70))
        pygame.draw.rect(screen, RED, (10,100,150,20))
        pygame.draw.rect(screen, GREEN, (10,100,int(150*(health/max_health)),20))
        screen.blit(font.render(f"Health: {health:.1f}",True,WHITE),(10,130))
        screen.blit(font.render("DEV TEST V5",True,WHITE),(10,10))
        fps=int(clock.get_fps())
        screen.blit(font.render(f"FPS: {fps}",True,WHITE), (SCREEN_WIDTH -80,10))

        pygame.display.flip(); clock.tick(60)

def game_over(score):
    btn=pygame.Rect(SCREEN_WIDTH//2 -100, SCREEN_HEIGHT//2+40, 200,50)
    while True:
        screen.fill((0,0,0))
        screen.blit(font.render("Game Over",True,WHITE),(SCREEN_WIDTH//2 -80,100))
        screen.blit(font.render(f"Score: {score}",True,WHITE),(SCREEN_WIDTH//2 -50,160))
        pygame.draw.rect(screen, GREEN, btn)
        screen.blit(font.render("Menu",True,BLACK),(btn.x+btn.width//2 -30, btn.y+btn.height//2 -15))
        screen.blit(font.render("DEV TEST V5",True,WHITE),(10,10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(event.pos): return
        clock.tick(60)

def level_complete(score,next_level):
    btn=pygame.Rect(SCREEN_WIDTH//2 -100, SCREEN_HEIGHT//2+40, 200,50)
    while True:
        screen.fill((0,100,200))
        screen.blit(font.render("Level Complete!",True,WHITE),(SCREEN_WIDTH//2 -100,100))
        screen.blit(font.render(f"Score: {score}",True,WHITE),(SCREEN_WIDTH//2 -50,160))
        pygame.draw.rect(screen, GREEN, btn)
        screen.blit(font.render("Next Level",True,BLACK),(btn.x+btn.width//2 -60, btn.y+btn.height//2 -15))
        screen.blit(font.render("DEV TEST V5",True,WHITE),(10,10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(event.pos):
                    if next_level<=5: game(next_level)
                    else: return
        clock.tick(60)

menu()
pygame.quit()
