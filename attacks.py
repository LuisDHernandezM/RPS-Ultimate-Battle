# File that handles the different attack mechanics

import pygame # type: ignore
import math

class Attack:
    def __init__(self, x, y):
        self.x = x - (75 // 2)
        self.y = y - (75 // 2)
        self.active = True
    
    # Updating attacks position, lifetime, etc.
    def update(self):
        pass
    
    # Rendering the attack on screen
    def draw(self, screen):
        pass
    
    # Checking collision with a target
    def check_collision(self, target):
        pass

# ============================ Rock Attack ============================

# Appears around the player, damaging anyone in range
class RockAttack(Attack):
    def __init__(self, player):
        super().__init__(player.x + 75, player.y + 75)
        self.radius = 400 # How far it reaches
        self.duration = 15 # How long it stays (15 frames → ~0.25s if 60 FPS).
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame >= self.duration:
            self.active = False

    # Draw a circle outline around the player
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius, 0)

    # Check if target is within the radius
    def check_collision(self, target):
        tx = target.x + 75
        ty = target.y + 75
        dist = math.hypot(tx - self.x, ty - self.y)
        return dist <= self.radius + 75
    

# ============================ Paper Attack ============================

# Projectile shoots toward the mouse when created. Bounces off walls up to 2 times.
class PaperProjectile(Attack):
    def __init__(self, x, y, target_x, target_y):
        super().__init__(x, y)
        angle = math.atan2(target_y - y, target_x - x)

        # Velocity vectors
        speed = 10
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)

        self.radius = 40 # Size of the projectile
        self.bounces = 0 # Number of bounces so far
        self.max_bounces = 2 # Max bounces allowed

    # Update position and handle bouncing
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x <= 0 or self.x >= 800 - self.radius:
            self.vx *= -1
            self.bounces += 1
        if self.y <= 0 or self.y >= 600 - self.radius:
            self.vy *= -1
            self.bounces += 1
        if self.bounces > self.max_bounces:
            self.active = False

    # Draw the projectile as a yellow circle
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius)

    # Check collision with target
    def check_collision(self, target):
        tx = target.x + 75
        ty = target.y + 75
        dist = math.hypot(tx - self.x, ty - self.y)
        return dist <= self.radius + 75


# ============================ Scissors Attack ============================

# Draws a triangle (cone) in the direction of the mouse. Damages anyone in the cone area.
class ScissorsCone(Attack):
    def __init__(self, player, mouse_pos):
        super().__init__(player.x + 75, player.y + 75)
        self.angle = math.atan2(mouse_pos[1] - self.y, mouse_pos[0] - self.x) # Direction of the cone
        self.radius = 150 # Length of the cone
        self.width = math.pi / 4 # Width of the cone in radians (45 degrees)
        self.duration = 20 # How long it stays (20 frames → ~0.33s if 60 FPS).
        self.frame = 0  

    # Update lifetime
    def update(self):
        self.frame += 1
        if self.frame >= self.duration:
            self.active = False

    # Draw the cone as a filled triangle
    def draw(self, screen):
        end_x = self.x + math.cos(self.angle) * self.radius
        end_y = self.y + math.sin(self.angle) * self.radius
        left_x = self.x + math.cos(self.angle - self.width/2) * self.radius
        left_y = self.y + math.sin(self.angle - self.width/2) * self.radius
        right_x = self.x + math.cos(self.angle + self.width/2) * self.radius
        right_y = self.y + math.sin(self.angle + self.width/2) * self.radius
        pygame.draw.polygon(screen, (255, 255, 0), [(self.x, self.y), (left_x, left_y), (right_x, right_y)], 0)

    # Check if target is within the cone area
    def check_collision(self, target):
        tx = target.x + 75
        ty = target.y + 75
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)
        if dist > self.radius + 75:
            return False
        angle_to_target = math.atan2(dy, dx)
        angle_diff = (angle_to_target - self.angle + math.pi*2) % (math.pi*2)
        if angle_diff > math.pi:
            angle_diff -= 2*math.pi
        return abs(angle_diff) < self.width/2