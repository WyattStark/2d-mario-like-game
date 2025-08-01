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
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)
YELLOW = (200, 200, 0)
BLACK = (0, 0, 0)

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mini Mario Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

player_name_global = ""
max_unlocked_level = 1  # tracks which level is unlocked

# Load images
player_img = pygame.image.load("stickman.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

enemy_img = pygame.image.load("spider.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))


def Player_name():
    return player_name_global


def menu():
    global player_name_global
    play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, 200, 50)
    levels_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''

    in_menu = True
    while in_menu:
        screen.fill((135, 206, 235))

        title_text = font.render("Mini Mario Game", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        label = font.render("Player Name:", True, BLACK)
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 - 140))

        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font.render(text, True, BLACK)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        pygame.draw.rect(screen, GREEN, play_button)
        play_text = font.render("Play", True, BLACK)
        screen.blit(play_text, (play_button.x + play_button.width // 2 - play_text.get_width() // 2,
                                play_button.y + play_button.height // 2 - play_text.get_height() // 2))

        pygame.draw.rect(screen, GREEN, levels_button)
        levels_text = font.render("Levels", True, BLACK)
        screen.blit(levels_text, (levels_button.x + levels_button.width // 2 - levels_text.get_width() // 2,
                                  levels_button.y + levels_button.height // 2 - levels_text.get_height() // 2))

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
                    game(1)
                elif levels_button.collidepoint(event.pos):
                    player_name_global = text if text else "Player"
                    level_select()

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


def level_select():
    global max_unlocked_level
    level1_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20, 100, 50)
    level2_button = pygame.Rect(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 20, 100, 50)

    in_select = True
    while in_select:
        screen.fill((100, 150, 200))

        title = font.render("Select Level", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Level 1 button (always unlocked)
        pygame.draw.rect(screen, GREEN, level1_button)
        text1 = font.render("Level 1", True, BLACK)
        screen.blit(text1, (level1_button.x + level1_button.width // 2 - text1.get_width() // 2,
                            level1_button.y + level1_button.height // 2 - text1.get_height() // 2))

        # Level 2 button: locked or unlocked
        if max_unlocked_level >= 2:
            pygame.draw.rect(screen, GREEN, level2_button)
        else:
            pygame.draw.rect(screen, GRAY, level2_button)
        text2 = font.render("Level 2", True, BLACK)
        screen.blit(text2, (level2_button.x + level2_button.width // 2 - text2.get_width() // 2,
                            level2_button.y + level2_button.height // 2 - text2.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if level1_button.collidepoint(event.pos):
                    in_select = False
                    game(1)
                elif level2_button.collidepoint(event.pos) and max_unlocked_level >= 2:
                    in_select = False
                    game(2)

        clock.tick(60)


def game_over(final_score):
    play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 50)
    in_game_over = True
    while in_game_over:
        screen.fill((0, 0, 0))

        over_text = font.render("Game Over", True, WHITE)
        screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, 100))

        name_text = font.render(f"Player: {Player_name()}", True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 160))

        score_text = font.render(f"Score: {final_score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))

        pygame.draw.rect(screen, GREEN, play_again_button)
        again_text = font.render("Menu", True, BLACK)
        screen.blit(again_text, (
            play_again_button.x + play_again_button.width // 2 - again_text.get_width() // 2,
            play_again_button.y + play_again_button.height // 2 - again_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    in_game_over = False
                    menu()

        clock.tick(60)


def level_complete(score, next_level):
    global max_unlocked_level
    next_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 50)
    in_complete = True
    while in_complete:
        screen.fill((0, 100, 200))

        complete_text = font.render("Level Complete!", True, WHITE)
        screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, 100))

        level_text = font.render(f"Next Level: {next_level}", True, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 160))

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))

        pygame.draw.rect(screen, GREEN, next_button)
        next_text = font.render("Next Level", True, BLACK)
        screen.blit(next_text, (
            next_button.x + next_button.width // 2 - next_text.get_width() // 2,
            next_button.y + next_button.height // 2 - next_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.collidepoint(event.pos):
                    max_unlocked_level = max(max_unlocked_level, next_level)
                    in_complete = False
                    game(next_level)

        clock.tick(60)


def game(level):
    player = pygame.Rect(100, GROUND_HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    player_vel_y = 0
    gravity = 0.8
    jump_strength = -15
    on_ground = True

    boxes = [pygame.Rect(300 + level * 50, GROUND_HEIGHT - 100, BOX_SIZE, BOX_SIZE),
             pygame.Rect(500 + level * 30, GROUND_HEIGHT - 150, BOX_SIZE, BOX_SIZE)]

    enemies = []
    score = 0

    enemy_spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_spawn_event, 2000)

    running = True
    while running:
        screen.fill((135, 206, 235))
        pygame.draw.rect(screen, GREEN, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == enemy_spawn_event:
                enemy = pygame.Rect(SCREEN_WIDTH, GROUND_HEIGHT - ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
                enemies.append(enemy)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5
        if keys[pygame.K_UP] and on_ground:
            player_vel_y = jump_strength
            on_ground = False

        player_vel_y += gravity
        player.y += int(player_vel_y)

        if player.y >= GROUND_HEIGHT - PLAYER_HEIGHT:
            player.y = GROUND_HEIGHT - PLAYER_HEIGHT
            player_vel_y = 0
            on_ground = True

        for enemy in enemies:
            if player.colliderect(enemy):
                running = False
                game_over(score)
                return

        for box in boxes:
            if player.colliderect(box) and player_vel_y < 0 and player.y > box.y + box.height / 2:
                score += 1
                boxes.remove(box)

        if score >= 2:
            running = False
            level_complete(score, level + 1)
            return

        for enemy in enemies:
            enemy.x -= 4
        enemies = [enemy for enemy in enemies if enemy.x + ENEMY_WIDTH > 0]

        screen.blit(player_img, player)
        for box in boxes:
            pygame.draw.rect(screen, YELLOW, box)
        for enemy in enemies:
            screen.blit(enemy_img, enemy)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        name_text = font.render(f"Player: {Player_name()} | Level: {level}", True, WHITE)
        screen.blit(name_text, (10, 40))

        pygame.display.flip()
        clock.tick(60)


# Start
menu()
pygame.quit()
