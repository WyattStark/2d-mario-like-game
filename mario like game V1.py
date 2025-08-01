import pygame
import random

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
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (200, 200, 0)
BLACK = (0, 0, 0)

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wyatts Mini Mario Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def menu():
    play_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 25, 200, 50)
    in_menu = True
    while in_menu:
        screen.fill((135, 206, 235))  # background color

        # Draw title
        title_text = font.render("Wyatts Mini Mario Game", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))

        # Draw play button
        pygame.draw.rect(screen, GREEN, play_button)
        play_text = font.render("Play", True, BLACK)
        screen.blit(play_text, (play_button.x + play_button.width//2 - play_text.get_width()//2,
                                play_button.y + play_button.height//2 - play_text.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    in_menu = False

        clock.tick(60)

def game():
    player = pygame.Rect(100, GROUND_HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    player_vel_y = 0
    gravity = 0.8
    jump_strength = -15
    on_ground = True

    boxes = [pygame.Rect(300, GROUND_HEIGHT - 100, BOX_SIZE, BOX_SIZE),
             pygame.Rect(500, GROUND_HEIGHT - 150, BOX_SIZE, BOX_SIZE)]

    enemies = []
    score = 0

    enemy_spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_spawn_event, 2000)  # spawn every 2 seconds

    running = True
    while running:
        screen.fill((135, 206, 235))  # sky blue

        # Draw ground
        pygame.draw.rect(screen, GREEN, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == enemy_spawn_event:
                enemy = pygame.Rect(SCREEN_WIDTH, GROUND_HEIGHT - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
                enemies.append(enemy)

        # Handle keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5
        if keys[pygame.K_UP] and on_ground:
            player_vel_y = jump_strength
            on_ground = False

        # Apply gravity
        player_vel_y += gravity
        player.y += int(player_vel_y)

        # Check ground collision
        if player.y >= GROUND_HEIGHT - PLAYER_HEIGHT:
            player.y = GROUND_HEIGHT - PLAYER_HEIGHT
            player_vel_y = 0
            on_ground = True

        # Check box collisions from below
        for box in boxes:
            if (player.colliderect(box) and
                player_vel_y < 0 and
                player.y > box.y + box.height / 2):
                score += 1
                boxes.remove(box)

        # Move enemies
        for enemy in enemies:
            enemy.x -= 4
        enemies = [enemy for enemy in enemies if enemy.x + ENEMY_WIDTH > 0]

        # Draw player
        pygame.draw.rect(screen, RED, player)

        # Draw boxes
        for box in boxes:
            pygame.draw.rect(screen, YELLOW, box)

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, BLUE, enemy)

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

# Run menu first, then game
menu()
game()
pygame.quit()
