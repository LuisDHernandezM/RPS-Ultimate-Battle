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

# ====== TEMPORARY bypassing canvas for testing ======
label = "paper" # TEMPORARY for testing without canvas
print("You drew:", label)
# print("Image saved as:", image_path) 

# 2. ---- Setup Pygame Arena ----
pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 1500, 800
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
        self.speed = 4 # movement speed in pixels per frame

        # cooldowns for each attack type
        self.cooldowns = {
            "rock": 2, # seconds
            "paper": 1.25, 
            "scissors": 1.5 
        }
        self.last_attack_time = 0
        self.attack_cooldown = 0.7  # default cooldown
        self.label = label  # "rock", "paper", or "scissors"
    
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
    
    def can_attack(self):
        cd = self.cooldowns[self.label]        # choose correct cooldown
        return (time.time() - self.last_attack_time) >= cd

    def trigger_attack(self):
        self.last_attack_time = time.time()
    

# --- Create fighters ---
player = Fighter("player_drawing.png", 100, 300)
# TEMPORARY enemy
enemy  = Fighter("scissors1.png", 700, 300)
enemy.label = "scissors"  # TEMPORARY enemy label

# Rules for RPS
def rps_result(p1, p2):
    if p1 == p2: return 0 # tie
    # p1 wins cases
    if p1 == "rock"     and p2 == "scissors": return 1
    if p1 == "scissors" and p2 == "paper":    return 1
    if p1 == "paper"    and p2 == "rock":     return 1
    # p2 wins cases
    if p1 == "rock"     and p2 == "paper": return -1
    if p1 == "scissors" and p2 == "rock":    return -1
    if p1 == "paper"    and p2 == "scissors": return -1

    return KeyError("Invalid RPS inputs")

# --- Battle logic example ---
last_hit_time = time.time()

def rps_damage(attacker, defender):
    """Simple example: attacker always deals 1 damage every second"""
    defender.health -= 0.75
    if defender.health < 0:
        defender.health = 0

# List to hold active attacks in the game
attacks = []

# -------------------------- Game Loop ------------------------------------
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

    # Player movement
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0

    if keys[pygame.K_a]:
        dx -= player.speed
    if keys[pygame.K_d]:
        dx += player.speed
    if keys[pygame.K_w]:
        dy -= player.speed
    if keys[pygame.K_s]:
        dy += player.speed

    player.move(dx, dy)

    # Normalize diagonal movement
    if dx != 0 and dy != 0:
        dx /= math.sqrt(2)
        dy /= math.sqrt(2)

    # Handle attacks
    if keys[pygame.K_SPACE] and player.can_attack():
        player.trigger_attack()

        if label == "rock":
            attacks.append(RockAttack(player))

        elif label == "paper":
            mx, my = pygame.mouse.get_pos()
            attacks.append(PaperProjectile(player.x+75, player.y+75, mx, my))

        elif label == "scissors":
            mx, my = pygame.mouse.get_pos()
            attacks.append(ScissorsCone(player, (mx, my)))

     
    # Update and draw attacks
    for attack in attacks[:]:                  # iterate over a shallow copy
        attack.update()
        # collision detection per attack - only once per attack
        if attack.check_collision(enemy) and not attack.has_hit:
            if isinstance(attack, RockAttack):
                if rps_result("rock", enemy.label) == 1:
                    enemy.health -= 15
                    attack.has_hit = True
                elif rps_result("rock", enemy.label) == -1:
                    enemy.health -= 5
                    attack.has_hit = True
                else:
                    enemy.health -= 10
                    attack.has_hit = True
            elif isinstance(attack, PaperProjectile):
                if rps_result("paper", enemy.label) == 1:
                    enemy.health -= 12
                    # print("Paper dealt -12!")
                    # print("Enemy type:", enemy.label)
                    attack.has_hit = True
                    attack.active = False  # deactivate projectile on hit
                elif rps_result("paper", enemy.label) == -1:
                    enemy.health -= 4
                    # print("Paper dealt -4!")
                    # print("Enemy type:", enemy.label)
                    attack.has_hit = True
                    attack.active = False
                else:
                    enemy.health -= 8
                    # print("Paper dealt -8!")
                    # print("Enemy type:", enemy.label)
                    attack.has_hit = True
                    attack.active = False
            elif isinstance(attack, ScissorsCone):
                if rps_result("scissors", enemy.label) == 1:
                    enemy.health -= 18
                    attack.has_hit = True
                elif rps_result("scissors", enemy.label) == -1:
                    enemy.health -= 6
                    attack.has_hit = True
                else:
                    enemy.health -= 10
                    attack.has_hit = True
        if attack.active:
            attack.draw(screen)
        else:
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