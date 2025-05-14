import pygame
import random
import time
import os

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Beko's Space Adventure")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
explosion_color = (255, 165, 0)  # Orange color for explosions

# Load images
current_dir = os.path.dirname(os.path.abspath(__file__))
player_image = pygame.image.load(os.path.join(current_dir, "characters", "ship1.png"))
enemy_image = pygame.image.load(os.path.join(current_dir, "characters", "kling.png"))
enemy_image.set_colorkey((255, 255, 255))  # Set white as the transparent color key
background_image = pygame.image.load(os.path.join(current_dir, "characters", "space3.jpeg"))

# Define player properties
player_width = 30
player_height = 50
player_x = width // 2 - player_width // 2
player_y = height - player_height - 10
player_speed = 9

# Define enemy properties
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemies = []

# Define bullet properties
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Define enemy bullet properties
enemy_bullet_width = 5
enemy_bullet_height = 10
enemy_bullet_speed = 5
enemy_bullets = []

# Define bullet firing properties
bullet_firing_delay = 350  # Delay between bullets in milliseconds
last_bullet_time = 0

# Define enemy spawning properties
enemy_spawn_delay = 800  # Delay between enemy spawns in milliseconds
last_enemy_spawn_time = 0

# Define enemy bullet firing properties
enemy_bullet_firing_delay = 1000  # Delay between enemy bullets in milliseconds
last_enemy_bullet_time = 0

# Define explosion properties
explosions = []
explosion_duration = 200  # Duration of the explosion in milliseconds

# Define scoreboard properties
score = 0
font = pygame.font.Font(None, 36)

# Function to display the start screen
def show_start_screen():
    title_font = pygame.font.Font(None, 80)
    start_font = pygame.font.Font(None, 40)

    title_text = title_font.render("BEKO'S SPACE ADVENTURE", True, white)
    start_text = start_font.render("Press any key to start", True, white)

    title_rect = title_text.get_rect(center=(width // 2, height // 2 - 50))
    start_rect = start_text.get_rect(center=(width // 2, height // 2 + 50))

    screen.blit(background_image, (0, 0))
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)

    # Display player character at the bottom of the screen
    screen.blit(player_image, (player_x, player_y))

    # Display enemies in different colors at the top of the screen
    for i in range(5):
        enemy_x = i * (enemy_width + 20) + (width // 2 - (5 * (enemy_width + 20)) // 2)
        enemy_y = 50
        enemy_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        colored_enemy_image = enemy_image.copy()
        colored_enemy_image.fill(enemy_color, special_flags=pygame.BLEND_MULT)
        screen.blit(colored_enemy_image, (enemy_x, enemy_y))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                waiting = False
                return True

# Function to display the blinking "BLAST OFF!!!" message
def show_blast_off_message():
    blast_off_font = pygame.font.Font(None, 100)
    blast_off_text = blast_off_font.render("BLAST OFF!!!", True, white)
    blast_off_rect = blast_off_text.get_rect(center=(width // 2, height // 2))

    blink_duration = 0.1  # Duration of each blink in seconds
    num_blinks = 10  # Number of blinks

    for _ in range(num_blinks):
        screen.fill(black)
        screen.blit(blast_off_text, blast_off_rect)
        pygame.display.flip()
        time.sleep(blink_duration)

        screen.fill(black)
        pygame.display.flip()
        time.sleep(blink_duration)

# Function to display the "GAME OVER" message
def show_game_over_message():
    game_over_font = pygame.font.Font(None, 80)
    game_over_text = game_over_font.render("GAME OVER", True, white)
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))

    screen.blit(background_image, (0, 0))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

def main():
    global player_x, game_over, score, last_bullet_time, last_enemy_spawn_time, last_enemy_bullet_time
    
    # Game loop
    running = True
    game_over = False
    clock = pygame.time.Clock()

    if not show_start_screen():
        return
    
    show_blast_off_message()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            # Move the player
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < width - player_width:
                player_x += player_speed

            # Fire bullets
            current_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE] and current_time - last_bullet_time >= bullet_firing_delay:
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y
                bullets.append((bullet_x, bullet_y))
                last_bullet_time = current_time

            # Move bullets
            for i, (bullet_x, bullet_y) in enumerate(bullets[:]):
                bullet_y -= bullet_speed
                bullets[i] = (bullet_x, bullet_y)

                # Remove bullets that go off the screen
                if bullet_y < 0:
                    bullets.pop(i)
                    break

            # Spawn enemies
            current_time = pygame.time.get_ticks()
            if current_time - last_enemy_spawn_time >= enemy_spawn_delay:
                enemy_x = random.randint(0, width - enemy_width)
                enemy_y = 0
                enemy_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                enemies.append((enemy_x, enemy_y, enemy_color))
                last_enemy_spawn_time = current_time

            # Move enemies
            for i, (enemy_x, enemy_y, enemy_color) in enumerate(enemies[:]):
                enemy_y += enemy_speed
                enemies[i] = (enemy_x, enemy_y, enemy_color)

                # Remove enemies that go off the screen
                if enemy_y > height:
                    enemies.pop(i)
                    break

            # Enemy firing bullets
            current_time = pygame.time.get_ticks()
            if current_time - last_enemy_bullet_time >= enemy_bullet_firing_delay:
                for enemy_x, enemy_y, _ in enemies:
                    enemy_bullet_x = enemy_x + enemy_width // 2 - enemy_bullet_width // 2
                    enemy_bullet_y = enemy_y + enemy_height
                    enemy_bullets.append((enemy_bullet_x, enemy_bullet_y))
                last_enemy_bullet_time = current_time

            # Move enemy bullets
            for i, (enemy_bullet_x, enemy_bullet_y) in enumerate(enemy_bullets[:]):
                enemy_bullet_y += enemy_bullet_speed
                enemy_bullets[i] = (enemy_bullet_x, enemy_bullet_y)

                # Remove enemy bullets that go off the screen
                if enemy_bullet_y > height:
                    enemy_bullets.pop(i)
                    break

            # Check for collision between player bullets and enemies
            for i, (enemy_x, enemy_y, enemy_color) in enumerate(enemies[:]):
                for j, (bullet_x, bullet_y) in enumerate(bullets[:]):
                    if (
                        enemy_x < bullet_x < enemy_x + enemy_width
                        and enemy_y < bullet_y < enemy_y + enemy_height
                    ):
                        enemies.pop(i)
                        bullets.pop(j)
                        explosions.append((enemy_x, enemy_y, pygame.time.get_ticks()))
                        score += 100  # Increase the score by 100
                        break

            # Check for collision between player and enemy bullets
            for i, (enemy_bullet_x, enemy_bullet_y) in enumerate(enemy_bullets[:]):
                if (
                    player_x < enemy_bullet_x < player_x + player_width
                    and player_y < enemy_bullet_y < player_y + player_height
                ):
                    # Player hit by enemy bullet
                    game_over = True
                    show_game_over_message()
                    break

            # Update explosions
            for i, (explosion_x, explosion_y, start_time) in enumerate(explosions[:]):
                if pygame.time.get_ticks() - start_time >= explosion_duration:
                    explosions.pop(i)
                    break

            # Clear the screen
            screen.blit(background_image, (0, 0))

            # Draw the player
            screen.blit(player_image, (player_x, player_y))

            # Draw enemies
            for enemy_x, enemy_y, enemy_color in enemies:
                colored_enemy_image = enemy_image.copy()
                colored_enemy_image.fill(enemy_color, special_flags=pygame.BLEND_MULT)
                screen.blit(colored_enemy_image, (enemy_x, enemy_y))

            # Draw bullets
            for bullet_x, bullet_y in bullets:
                pygame.draw.rect(screen, white, (bullet_x, bullet_y, bullet_width, bullet_height))

            # Draw enemy bullets
            for enemy_bullet_x, enemy_bullet_y in enemy_bullets:
                pygame.draw.rect(screen, white, (enemy_bullet_x, enemy_bullet_y, enemy_bullet_width, enemy_bullet_height))

            # Draw explosions
            for explosion_x, explosion_y, start_time in explosions:
                elapsed_time = pygame.time.get_ticks() - start_time
                if elapsed_time < explosion_duration // 2:
                    pygame.draw.circle(screen, explosion_color, (explosion_x + enemy_width // 2, explosion_y + enemy_height // 2), 10)

            # Draw the scoreboard
            score_text = font.render("Score: " + str(score), True, white)
            score_rect = score_text.get_rect(topright=(width - 10, 10))
            screen.blit(score_text, score_rect)

            # Update the screen
            pygame.display.update()

        # Set the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()

if __name__ == "__main__":
    main() 