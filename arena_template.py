# Wrote by Luis D. Hernandez with assistance from ChatGPT and GenAI
# Date: December 2025
# File for making the arena template

import pygame  # type: ignore
import time
from canvas import *

# --- Window setup ---
WIDTH, HEIGHT = 1500, 800

# Clock setup
clock = pygame.time.Clock()

# Variable for sprite size
size_number = 75
size = (size_number, size_number)

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


def rps_damage(attacker, defender):
    """Simple example: attacker always deals 1 damage every second"""
    defender.health -= 0.75
    if defender.health < 0:
        defender.health = 0


# --- Battle logic example ---
last_hit_time = time.time()
