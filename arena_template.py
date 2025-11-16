# File for making the arena template

import pygame # type: ignore
import sys
import time
from canvas import draw_character
import math
from attacks import RockAttack, PaperProjectile, ScissorsCone

# 1. ---- Launch canvas and get drawing + label ----
image_path, label = draw_character()

print("You drew:", label)
print("Image saved as:", image_path)

# 2. ---- Setup Pygame Arena ----
pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPS Battle Arena")

clock = pygame.time.Clock()
# Variable for sprite size
size_number = 75
size = (size_number, size_number)

# --- Fighter class ---
class Fighter:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size))
        self.x = x
        self.y = y
        self.health = 100
        self.speed = 5 # movement speed in pixels per frame
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        bar_width = size_number
        bar_height = 10
        fill = (self.health / 100) * bar_width
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 20, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 20, fill, bar_height))
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

        # Keep inside the screen
        self.x = max(0, min(self.x, WIDTH - size_number))  # WIDTH - sprite width
        self.y = max(20, min(self.y, HEIGHT - size_number))  # HEIGHT - sprite height + heatlh bar offset

# --- Create fighters ---
player = Fighter(image_path, 100, 300)
# TEMPORARY enemy
enemy  = Fighter("scissors1.png", 700, 300)

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
    """Simple example: attacker always deals 1 damage every second"""
    defender.health -= 1
    if defender.health < 0:
        defender.health = 0

# --- Game Loop ---
running = True
while running:
    clock.tick(60)
    attacks = []

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

    # Player movement
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0

    if keys[pygame.K_LEFT]:
        dx -= player.speed
    if keys[pygame.K_RIGHT]:
        dx += player.speed
    if keys[pygame.K_UP]:
        dy -= player.speed
    if keys[pygame.K_DOWN]:
        dy += player.speed

    player.move(dx, dy)

    # Normalize diagonal movement
    if dx != 0 and dy != 0:
        dx /= math.sqrt(2)
        dy /= math.sqrt(2)

    # Handle attacks
    if keys[pygame.K_SPACE]:
        # test prints
        # print("Attack!")
        if label == "rock":
            attacks.append(RockAttack(player))
        elif label == "paper":
            mx, my = pygame.mouse.get_pos()
            attacks.append(PaperProjectile(player.x+75, player.y+75, mx, my))
        elif label == "scissors":
            mx, my = pygame.mouse.get_pos()
            attacks.append(ScissorsCone(player, (mx, my)))
    
    # Update and draw attacks
    for attack in attacks[:]:  # copy to safely remove
        attack.update()
        attack.draw(screen)
        if not attack.active:
            attacks.remove(attack)


    # Win detection
    if player.health <= 0:
        print("Enemy wins!")
        running = False
    if enemy.health <= 0:
        print("Player wins!")
        running = False
    
    # QUIT on ESCAPE
    if keys[pygame.K_ESCAPE]:
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()