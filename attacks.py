# File that handles the different attack mechanics

import pygame # type: ignore
import math
import time

WIDTH, HEIGHT = 1500, 800
size_number = 75


# ============================ Base Attack Class ============================

class Attack:
    def __init__(self, x, y):
        self.x = x - (75 // 2)
        self.y = y - (75 // 2)
        self.active = True
        self.has_hit = False
        self.owner = None  # to be set when created
        
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
        self.radius = 100 # How far it reaches
        self.duration = 30 # How long it stays (15 frames → ~0.25s if 60 FPS).
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
    def __init__(self, x, y, target_x, target_y, speed=12, radius=8, max_bounces=2):
        # x,y should be center of spawn (floats)
        super().__init__(x, y)
        # compute normalized direction toward target
        dx = float(target_x) - self.x
        dy = float(target_y) - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            # fallback direction if mouse exactly on spawn
            dx, dy = 1.0, 0.0
            dist = 1.0
        self.vx = (dx / dist) * speed
        self.vy = (dy / dist) * speed

        self.radius = radius
        self.bounces = 0
        self.max_bounces = max_bounces

        # small cooldown so bounce logic can't trigger immediately on spawn
        self._just_spawned_frames = 2
        self._just_spawned_time = time.time()  # store spawn time
        self.grace_period = 1  # 1 seconds immunity for owner
        

        # debugging
        # print(f"[PaperProjectile] spawn ({self.x:.1f},{self.y:.1f}) -> target ({target_x},{target_y}) vx={self.vx:.2f}, vy={self.vy:.2f}")

    def update(self):
        # move
        self.x += self.vx
        self.y += self.vy

        # reduce spawn grace frames
        if self._just_spawned_frames > 0:
            self._just_spawned_frames -= 1

        # bounce if hitting walls (consider radius)
        bounced = False
        if self.x - self.radius <= 0 and self.vx < 0:
            self.x = self.radius + 1
            self.vx *= -1
            bounced = True
        elif self.x + self.radius >= WIDTH and self.vx > 0:
            self.x = WIDTH - self.radius - 1
            self.vx *= -1
            bounced = True

        if self.y - self.radius <= 0 and self.vy < 0:
            self.y = self.radius + 1
            self.vy *= -1
            bounced = True
        elif self.y + self.radius >= HEIGHT and self.vy > 0:
            self.y = HEIGHT - self.radius - 1
            self.vy *= -1
            bounced = True

        if bounced and self._just_spawned_frames <= 0:
            self.bounces += 1

        if self.bounces > self.max_bounces:
            self.active = False

    def draw(self, screen):
        # convert position to ints for drawing
        pygame.draw.circle(screen, (255, 215, 0), (int(self.x), int(self.y)), self.radius)
        # optional: draw velocity vector for debugging
        # end_x = int(self.x + self.vx*2)
        # end_y = int(self.y + self.vy*2)
        # pygame.draw.line(screen, (255,0,0), (int(self.x),int(self.y)), (end_x,end_y), 2)

    def check_collision(self, target):
        # ignore collisions with owner during grace period
        if target == self.owner and time.time() - self._just_spawned_time < self.grace_period:
            return False
        tx = target.x + size_number/2
        ty = target.y + size_number/2
        dist = math.hypot(tx - self.x, ty - self.y) # distance between centers
        return dist <= (self.radius + max(size_number, size_number)/2) # collision check



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