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
pygame.display.set_caption("Mini Mario Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

player_name_global = ""  # global variable to store the player's name

def Player_name():
    """Return the current player's name"""
    return player_name_global

def menu():
    global player_name_global
    play_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 40, 200, 50)
    input_box = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 25, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''

    in_menu = True
    while in_menu:
        screen.fill((135, 206, 235))  # background color

        # Draw title
        title_text = font.render("Mini Mario Game", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))

        # Draw input box label
        label = font.render("Player Name:", True, BLACK)
        screen.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, SCREEN_HEIGHT//2 - 60))

        # Draw input box
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font.render(text, True, BLACK)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))

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
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

                if play_button.collidepoint(event.pos):
                    player_name_global = text if text else "Player"
                    in_menu = False

            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        player_name_global = text
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 12:
                            text += event.unicode

        clock.tick(60)

def game_over(final_score):
    play_again_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 40, 200, 50)
    in_game_over = True
    while in_game_over:
        screen.fill((0, 0, 0))  # black background

        # Draw "Game Over" text
        over_text = font.render("Game Over", True, WHITE)
        screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, 100))

        # Draw player name
        name_text = font.render(f"Player: {Player_name()}", True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH//2 - name_text.get_width()//2, 160))

        # Draw final score
        score_text = font.render(f"Score: {final_score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 200))

        # Draw play again button
        pygame.draw.rect(screen, GREEN, play_again_button)
        again_text = font.render("Play Again", True, BLACK)
        screen.blit(again_text, (play_again_button.x + play_again_button.width//2 - again_text.get_width()//2,
                                 play_again_button.y + play_again_button.height//2 - again_text.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    in_game_over = False
                    game()  # restart the game

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
    pygame.time.set_timer(enemy_spawn_event, 2000)

    running = True
    while running:
        screen.fill((135, 206, 235))

        # Draw ground
        pygame.draw.rect(screen, GREEN, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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

        # Check collision with enemies
        for enemy in enemies:
            if player.colliderect(enemy):
                running = False
                game_over(score)
                return

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

        # Draw score and player name
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        name_text = font.render(f"Player: {Player_name()}", True, WHITE)
        screen.blit(name_text, (10, 40))

        pygame.display.flip()
        clock.tick(60)

# Run menu first, then game
menu()
game()
pygame.quit()