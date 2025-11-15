# File for making the arena template

import pygame # type: ignore
import sys
import time
from canvas import draw_character

# 1. ---- Launch canvas and get drawing + label ----
image_path, label = draw_character()

print("You drew:", label)
print("Image saved as:", image_path)

# 2. ---- Setup Pygame Arena ----
pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPS Battle Arena")

clock = pygame.time.Clock()

# --- Fighter class ---
class Fighter:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.x = x
        self.y = y
        self.health = 100
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = 150
        bar_height = 15
        fill = (self.health / 100) * bar_width
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 20, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 20, fill, bar_height))

# --- Create fighters ---
player = Fighter(image_path, 100, 300)
# TEMPORARY enemy
enemy  = Fighter("scissors1.png", 550, 300)

# # --- Example fighters ---
# player = Fighter("rock1.png", 100, 300)       # ← replace your own images

# Rules for RPS
def rps_result(p1, p2):
    if p1 == p2: return 0
    if p1 == "rock"     and p2 == "scissors": return 1
    if p1 == "scissors" and p2 == "paper":    return 1
    if p1 == "paper"    and p2 == "rock":     return 1
    return -1

# --- Battle logic example ---
last_hit_time = time.time()

def rps_damage(attacker, defender):
    """Simple example: attacker always deals 10 damage every second"""
    defender.health -= 10
    if defender.health < 0:
        defender.health = 0

# --- Game Loop ---
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background
    screen.fill((30, 30, 30))

    # Every second, apply damage
    if time.time() - last_hit_time > 1:
        rps_damage(player, enemy)
        rps_damage(enemy, player)
        last_hit_time = time.time()

    # Draw fighters
    player.draw(screen)
    enemy.draw(screen)

    # Win detection
    if player.health <= 0:
        print("Enemy wins!")
        running = False
    if enemy.health <= 0:
        print("Player wins!")
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()