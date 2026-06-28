import pygame
import random
import time
import sys

pygame.init()
pygame.mixer.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emoji Shooter")

FPS = 60
GAME_TIME = 30

BG_COLOR = (25, 25, 25)  
BLACK = (225, 235,245
         )

clock = pygame.time.Clock()

# ---------------- FONTS ----------------
font = pygame.font.SysFont("Segoe UI Emoji", 48)
small_font = pygame.font.SysFont("Segoe UI", 28)
big_font = pygame.font.SysFont("Segoe UI", 60)

# ---------------- GAME OBJECTS ----------------
PLAYER = "🔫"
TARGETS = ["😂", "😍", "😎"]

player_x = WIDTH // 2
player_y = HEIGHT - 80
player_speed = 7

bullets = []
targets = []

score = 0

# ---------------- FUNCTIONS ----------------
def draw_text(text, font, x, y):
    win.blit(font.render(text, True, BLACK), (x, y))

def start_screen():
    while True:
        win.fill(BG_COLOR)
        draw_text("Emoji Shooter", big_font, 240, 200)
        draw_text("Press ENTER to Start", small_font, 290, 300)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def end_screen():
    while True:
        win.fill(BG_COLOR)
        draw_text("Game Over", big_font, 260, 200)
        draw_text(f"Final Score : {score}", small_font, 300, 280)
        draw_text("Best of Luck 👍", small_font, 320, 330)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

def create_targets():
    for _ in range(5):
        targets.append({
            "x": random.randint(50, WIDTH - 50),
            "y": random.randint(-150, -50),
            "speed": random.randint(2, 5),
            "emoji": random.choice(TARGETS)
        })

# ---------------- GAME START ----------------
create_targets()
start_screen()
start_time = time.time()

running = True
while running:
    clock.tick(FPS)
    win.fill(BG_COLOR)

    remaining_time = GAME_TIME - int(time.time() - start_time)
    if remaining_time <= 0:
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += player_speed
    if keys[pygame.K_SPACE] and len(bullets) < 5:
        bullets.append([player_x + 20, player_y])

    # Player
    win.blit(font.render(PLAYER, True, BLACK), (player_x, player_y))

    # Bullets
    for bullet in bullets[:]:
        bullet[1] -= 10
        pygame.draw.circle(win, BLACK, (bullet[0], bullet[1]), 5)
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Targets
    for t in targets:
        t["y"] += t["speed"]
        win.blit(font.render(t["emoji"], True, BLACK), (t["x"], t["y"]))

        for bullet in bullets[:]:
            if t["x"] < bullet[0] < t["x"] + 40 and t["y"] < bullet[1] < t["y"] + 40:
                bullets.remove(bullet)
                score += 1
                t["y"] = random.randint(-150, -50)
                t["x"] = random.randint(50, WIDTH - 50)

        if t["y"] > HEIGHT:
            t["y"] = random.randint(-150, -50)
            t["x"] = random.randint(50, WIDTH - 50)

    # UI
    draw_text(f"Score : {score}", small_font, 10, 10)
    draw_text(f"Time : {remaining_time}", small_font, WIDTH - 140, 10)

    pygame.display.update()

end_screen()
pygame.quit()
sys.exit()
